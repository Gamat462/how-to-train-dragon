# -*- coding: utf-8 -*-
"""Hari 3 — LAG, LEAD, WINDOW, dan jebakan LAST_VALUE."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("LAG melihat ke belakang, LEAD ke depan",
    blok("aksi", "Berkas <code>senja/l2-hari-3.sql</code>. Modul M6 sudah memperkenalkan "
                 "<code>lag</code>; <code>lead</code> tidak pernah disebut di sana.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  lag(nilai)  OVER (ORDER BY bulan) AS bulan_lalu,
  lead(nilai) OVER (ORDER BY bulan) AS bulan_depan,
  round((nilai - lag(nilai) OVER (ORDER BY bulan)) * 100.0
        / lag(nilai) OVER (ORDER BY bulan), 1) AS tumbuh_persen
FROM b ORDER BY bulan;'''),
    keluaran(H, "h3_lag_lead"),
    "<p>Baris pertama <code>bulan_lalu</code>-nya <code>NULL</code>, baris terakhir "
    "<code>bulan_depan</code>-nya <code>NULL</code> — tidak ada yang sebelum Januari dan tidak "
    "ada setelah Juni. <strong>Itu benar, bukan kerusakan.</strong></p>")

langkah("Menulis LAG tiga kali itu boros — dan ada obatnya",
    blok("aksi", "Query yang sama, ditulis dengan klausa <code>WINDOW</code>.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  lag(nilai) OVER w AS bulan_lalu,
  round((nilai - lag(nilai) OVER w) * 100.0 / lag(nilai) OVER w, 1) AS tumbuh_persen
FROM b
WINDOW w AS (ORDER BY bulan)
ORDER BY bulan;'''),
    keluaran(H, "h3_window_clause"),
    "<p>Definisi jendelanya kamu tulis <strong>sekali</strong>, kamu beri nama <code>w</code>, "
    "lalu kamu pakai berkali-kali. Angkanya sama persis dengan langkah 1 — cocokkan sendiri "
    "sebelum lanjut.</p>",
    blok("catatan", "Klausa <code>WINDOW</code> ditulis <strong>setelah</strong> "
                    "<code>GROUP BY</code>/<code>HAVING</code> dan <strong>sebelum</strong> "
                    "<code>ORDER BY</code>. Ia bukan soal kecepatan — mesinnya sudah menghitung "
                    "sekali saja. Ia soal keterbacaan, dan soal tidak salah mengetik salah satu "
                    "dari tiga salinan."))

langkah("LAG bisa melompat lebih dari satu, dan punya nilai bawaan",
    blok("aksi", "Dua argumen tambahan yang jarang dipakai orang.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  lag(nilai, 1)    OVER (ORDER BY bulan) AS satu_bulan_lalu,
  lag(nilai, 2)    OVER (ORDER BY bulan) AS dua_bulan_lalu,
  lag(nilai, 1, 0) OVER (ORDER BY bulan) AS dengan_bawaan_nol
FROM b ORDER BY bulan LIMIT 4;'''),
    keluaran(H, "h3_lag_default"),
    blok("bahaya", "Kolom terakhir menunjukkan <strong>0</strong> untuk Januari. Argumen ketiga "
                   "itu menggoda dan berbahaya: ia mengubah “tidak ada pembanding” jadi “nol "
                   "rupiah”, dan pertumbuhanmu jadi tak terhingga atau −100%. "
                   "<strong>Hampir tidak pernah pakai argumen ketiga untuk angka uang.</strong>"))

langkah("Cara yang jujur menutup lubang di baris pertama",
    blok("aksi", "Jadikan teks, bukan angka.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan,
  COALESCE(round((nilai - lag(nilai) OVER w) * 100.0 / lag(nilai) OVER w, 1)::text,
           'tidak ada pembanding') AS tumbuh
FROM b WINDOW w AS (ORDER BY bulan) ORDER BY bulan LIMIT 3;'''),
    keluaran(H, "h3_coalesce_teks"),
    "<p>Ini pelajaran Level 1 Hari 2 yang muncul lagi: bulan pertama bukan “tumbuh 0%”, "
    "melainkan <strong>tidak diketahui</strong>. Perbedaan itu penting justru saat orang lain "
    "membaca laporanmu tanpa bertanya kepadamu.</p>")

langkah("Layar merah yang mengingatkan window function butuh jendela",
    blok("aksi", "Hilangkan <code>OVER</code>-nya.", "LAKUKAN"),
    kode('''SELECT bulan, lag(nilai) FROM
 (SELECT to_char(tanggal,'YYYY-MM') AS bulan, count(*) AS nilai
  FROM pesanan GROUP BY 1) x;'''),
    keluaran(H, "h3_merah_lag_tanpa_over"),
    "<p><code>lag</code> bukan fungsi biasa. Tanpa <code>OVER</code>, PostgreSQL tidak tahu "
    "“sebelumnya” itu relatif terhadap urutan apa.</p>")

langkah("Lihat dulu tabel yang akan kamu pakai",
    blok("aksi", "Tujuh produk, diurutkan dari termurah. Ingat baris pertama dan terakhirnya.",
         "LAKUKAN"),
    kode("SELECT nama, harga FROM produk ORDER BY harga;"),
    keluaran(H, "h3_produk_urut"),
    "<p>Termurah 10.000 (Teh Manis), termahal 30.000 (Cheesecake). Dua angka itu yang seharusnya "
    "kamu dapat di langkah berikutnya — dan salah satunya tidak akan kamu dapat.</p>")

langkah("Catat dua angka ini sebelum melangkah",
    blok("aksi", "Satu baris. Kamu akan mencocokkannya sebentar lagi.", "LAKUKAN"),
    kode("SELECT max(harga) AS termahal, min(harga) AS termurah FROM produk;"),
    keluaran(H, "h3_termahal"),
    "<p>30.000 dan 10.000. <strong>Kalau langkah berikutnya memberimu angka lain untuk “nilai "
    "terakhir”, kamu sudah tahu ia salah</strong> — bukan karena aku bilang begitu, tapi karena "
    "kamu punya angka pembandingnya.</p>")

langkah("LAST_VALUE yang tidak memberi nilai terakhir",
    blok("aksi", "Ini jebakan window function yang paling sering ditanyakan di wawancara, dan "
                 "paling sering bikin orang bingung berjam-jam.", "LAKUKAN"),
    kode('''SELECT nama, harga,
  first_value(harga) OVER (ORDER BY harga) AS first_v,
  last_value(harga)  OVER (ORDER BY harga) AS last_v_tanpa_frame,
  last_value(harga)  OVER (ORDER BY harga
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_v_dengan_frame
FROM produk ORDER BY harga;'''),
    keluaran(H, "h3_last_value"),
    "<p>Lihat kolom ketiga. <code>last_value</code> tanpa frame mengembalikan "
    "<strong>harga baris itu sendiri</strong> — 10000, 15000, 18000, dan seterusnya. Bukan "
    "30000, angka yang kamu catat dua langkah lalu. <strong>Kalau kamu bingung di sini, itu "
    "wajar</strong>: hampir semua orang bingung, dan penjelasannya ada di langkah berikutnya.</p>")

langkah("Penyebabnya persis pelajaran kemarin",
    blok("aksi", "Baca sekali, pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Frame bawaannya adalah “dari awal sampai baris ini”. Jadi saat SQL mencari "
                  "“nilai terakhir <em>di dalam frame</em>”, frame-nya berakhir di baris yang "
                  "sedang dihitung — maka nilai terakhirnya ya baris itu sendiri.</p>",
         "SATU SEBAB, DUA GEJALA"),
    "<p><code>first_value</code> tidak kena karena “nilai pertama” memang selalu di awal frame, "
    "dan awal frame-nya tetap dari baris paling awal. Itu sebabnya <code>first_value</code> "
    "terlihat “berfungsi” dan <code>last_value</code> terlihat “rusak” — padahal keduanya "
    "mengikuti aturan yang sama.</p>")

langkah("Cara yang dipakai orang berpengalaman: hindari LAST_VALUE",
    blok("aksi", "Balik urutannya, pakai <code>first_value</code>.", "LAKUKAN"),
    kode('''SELECT nama, harga, first_value(harga) OVER (ORDER BY harga DESC) AS termahal
FROM produk ORDER BY harga LIMIT 3;'''),
    keluaran(H, "h3_first_value_dibalik"),
    "<p>30000 tanpa perlu menulis frame sama sekali. Lebih pendek, dan <strong>tidak ada yang "
    "bisa lupa</strong>.</p>",
    blok("catatan", "Perbaikan yang satunya wajib ditulis penuh: "
                    "<code>ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING</code>. "
                    "Tidak ada jalan pintas. Kalau kamu melihat <code>last_value</code> tanpa "
                    "frame di kode orang lain, itu hampir pasti bug."))

langkah("nth_value: ketika yang kamu cari bukan yang pertama",
    blok("aksi", "Siapa produk termahal kedua?", "LAKUKAN"),
    kode('''SELECT nama, harga,
  nth_value(nama, 2) OVER (ORDER BY harga DESC
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS termahal_kedua
FROM produk ORDER BY harga DESC LIMIT 3;'''),
    keluaran(H, "h3_nth_value"),
    blok("bahaya", "<code>nth_value</code> kena jebakan yang <strong>sama persis</strong> seperti "
                   "<code>last_value</code>: tanpa frame penuh, ia mencari “yang kedua di dalam "
                   "frame sampai baris ini” — dan untuk baris pertama, yang kedua itu belum ada. "
                   "Kalau kamu menghapus dua baris <code>ROWS BETWEEN</code> di atas, kolomnya "
                   "berisi <code>NULL</code> di baris pertama."))

langkah("Kerjakan sendiri",
    blok("aksi", "Buat query yang menampilkan tiap produk berikut <strong>produk termurah dan "
                 "termahal di kategorinya</strong> (Minuman / Makanan). Pakai "
                 "<code>PARTITION BY</code>, dan hindari <code>last_value</code>.",
         "KERJAKAN, ± 12 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>SELECT nama, kategori, harga,\n"
    "  first_value(nama) OVER (PARTITION BY kategori ORDER BY harga)      AS termurah,\n"
    "  first_value(nama) OVER (PARTITION BY kategori ORDER BY harga DESC) AS termahal\n"
    "FROM produk ORDER BY kategori, harga;</code></pre></div>"
    + keluaran(H, "h3_kunci", tag="HASILNYA") +
    "<p>Dua <code>first_value</code> dengan arah urutan berlawanan, tanpa satu pun frame "
    "ditulis — dan hasilnya benar di semua baris.</p>"
    "<p>Versi yang lebih rapi memakai klausa <code>WINDOW</code> dua kali:</p>"
    "<div class=\"kode\"><pre><code>WINDOW naik AS (PARTITION BY kategori ORDER BY harga),\n"
    "       turun AS (PARTITION BY kategori ORDER BY harga DESC)</code></pre></div>"
    "<p>lalu <code>first_value(nama) OVER naik</code> dan "
    "<code>first_value(nama) OVER turun</code>.</p></details>")

HARI3 = {
  "n": "HARI 3", "tab": "3",
  "judul": "LAG, LEAD, WINDOW, dan jebakan LAST_VALUE",
  "waktu": "± 55 menit",
  "tujuan": "membandingkan baris dengan baris sebelum dan sesudahnya, memberi nama pada jendela, "
            "dan tahu kenapa <code>last_value</code> hampir selalu salah kalau ditulis apa adanya.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>lead</code> = kebalikan <code>lag</code> · "
           "baris pertama/terakhir menghasilkan <code>NULL</code>, dan itu “tidak ada "
           "pembanding”, bukan nol · klausa <code>WINDOW</code> menamai jendela supaya tidak "
           "ditulis tiga kali · <code>last_value</code> dan <code>nth_value</code> tanpa frame "
           "penuh selalu keliru — balik urutannya dan pakai <code>first_value</code>.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 3 dari 8.</strong> Jawab dengan "
           "suara: <em>kenapa <code>last_value(x) OVER (ORDER BY x)</code> tidak memberi nilai "
           "terakhir, dan sebutkan dua cara memperbaikinya.</em></p>"
           "<details><summary>Kunci</summary><p>Karena frame bawaannya berakhir di baris yang "
           "sedang dihitung, jadi “nilai terakhir dalam frame” adalah baris itu sendiri. "
           "Perbaikan: tulis <code>ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED "
           "FOLLOWING</code>, atau balik urutannya dan pakai <code>first_value</code>.</p></details>",
}
