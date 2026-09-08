# -*- coding: utf-8 -*-
"""Hari 1 — apa yang sebenarnya dikerjakan OVER (PostgreSQL)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buka kembali basis datanya",
    blok("aksi", "VS Code, sambungan <code>senja</code> yang kamu buat di Level 1. Berkas baru: "
                 "<code>senja/l2-hari-1.sql</code>.", "LAKUKAN"),
    kode("SELECT count(*) AS pesanan FROM pesanan;"),
    keluaran(H, "h1_sambung"),
    blok("catatan", "<strong>Kalau muncul <code>relation \"pesanan\" does not exist</code>, itu "
                    "wajar</strong> — sambunganmu menunjuk ke basis data yang salah, atau "
                    "<code>senja.sql</code> belum dimuat. Ulangi langkah 5–8 di Level 1 Hari 1, "
                    "lalu kembali ke sini."))

langkah("Lihat bahannya dulu, sebelum menghitung apa pun",
    blok("aksi", "Satu query pendek. Kamu akan memakai angka-angka ini sepanjang minggu.",
         "LAKUKAN"),
    kode("""SELECT to_char(tanggal,'YYYY-MM') AS bulan, count(*) AS pesanan
FROM pesanan WHERE status='selesai' GROUP BY 1 ORDER BY 1;"""),
    keluaran(H, "h1_lihat_bulan"),
    "<p>Enam bulan, 362 pesanan selesai. <strong>Kenali bentuk datamu sebelum kamu menghitung "
    "apa pun darinya</strong> — kebiasaan yang sama seperti membaca neraca saldo sebelum "
    "menyentuh satu akun pun.</p>")

langkah("GROUP BY meringkas, dan itu memang gunanya",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''SELECT cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai_cabang
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai' GROUP BY cabang ORDER BY cabang;'''),
    keluaran(H, "h1_group_by"),
    "<p>Tiga baris, dari 788 baris item. Rinciannya hilang — dan untuk pertanyaan “berapa total "
    "tiap cabang”, itu justru yang kamu mau. Sama seperti neraca saldo: kamu memang tidak ingin "
    "melihat tiap jurnal di situ.</p>")

langkah("Satu angka pembanding yang kamu simpan",
    blok("aksi", "Jumlahkan seluruh baris item, tanpa menyaring status.", "LAKUKAN"),
    kode("SELECT sum(jumlah * harga_saat_itu) AS semua_item FROM item;"),
    keluaran(H, "h1_item_semua"),
    "<p>Rp 39.407.000 — lebih besar dari Rp 35.739.000 yang kamu hitung tadi, karena angka ini "
    "<strong>ikut menghitung pesanan yang dibatalkan</strong>. Selisihnya Rp 3.668.000, dan itu "
    "harus bisa kamu jelaskan sebelum kamu memakai angka mana pun di antara keduanya.</p>",
    blok("catatan", "Kamu sudah terbiasa: dua angka yang beda cuma boleh lewat kalau kamu bisa "
                    "menyebut sebabnya. Di kertas kerja itu kolom rekonsiliasi; di sini "
                    "kalimatnya sama."))

langkah("Pertanyaan yang GROUP BY tidak bisa jawab",
    blok("aksi", "Baca sekali. Jangan ketik apa-apa dulu.", "LAKUKAN"),
    blok("hasil", "<p><em>“Tiap baris item itu berapa persen dari total cabangnya?”</em></p>",
         "PERTANYAANNYA"),
    "<p>Untuk menjawabnya kamu butuh <strong>baris aslinya dan totalnya berdampingan</strong>. "
    "<code>GROUP BY</code> sudah membuang baris aslinya sebelum kamu sempat memakainya.</p>")

langkah("Window function menghitung tanpa membuang satu baris pun",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''SELECT o.id, o.cabang,
       i.jumlah * i.harga_saat_itu AS nilai_baris,
       sum(i.jumlah * i.harga_saat_itu) OVER (PARTITION BY o.cabang) AS nilai_cabang,
       round(i.jumlah * i.harga_saat_itu * 100.0 /
             sum(i.jumlah * i.harga_saat_itu) OVER (PARTITION BY o.cabang), 3) AS persen
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai' ORDER BY o.cabang, o.id LIMIT 6;'''),
    keluaran(H, "h1_window"),
    "<p>Barisnya utuh, dan totalnya ikut menempel di sebelahnya — seperti kamu menaruh kolom "
    "“% terhadap total” di sebelah kanan kertas kerja, tanpa menghapus satu baris pun.</p>")

langkah("Buktinya ada di kolom keempat",
    blok("aksi", "Bandingkan <code>nilai_cabang</code> di atas dengan hasil GROUP BY di "
                 "langkah 2.", "LAKUKAN"),
    blok("hasil", "<p><strong>12.665.000</strong> berulang di tiap baris — angka yang sama "
                  "persis dengan hasil GROUP BY tadi.</p>", "YANG HARUS TERLIHAT"),
    "<p>Itu bukti bahwa keduanya menghitung hal yang sama. Bedanya cuma window function "
    "<strong>menempelkannya ke tiap baris</strong>, bukan menggantikan barisnya.</p>")

langkah("Empat kata yang memberitahumu jawabannya window function",
    blok("aksi", "Salin ke catatanmu, lalu ucapkan kalimat pertamanya dengan suara keras.",
         "LAKUKAN"),
    blok("hasil", "<p>GROUP BY menjawab <em>“berapa totalnya”</em>. Window function menjawab "
                  "<em>“berapa bagian baris ini dari totalnya”</em>.</p>", "SATU KALIMAT"),
    tabel(["Kalau pertanyaannya mengandung…", "Alatnya"],
          [["“dibanding”, “berapa persen dari”", "window function"],
           ["“peringkat ke berapa”, “tiga teratas per…”", "window function"],
           ["“dibanding bulan sebelumnya”, “selisih dari yang lalu”", "window function"],
           ["“berjalan”, “kumulatif”, “rata-rata bergerak”", "window function"]]),
    "<p>Empat kata itu — <strong>dibanding, peringkat, sebelumnya, berjalan</strong> — hampir "
    "selalu berarti kamu tidak boleh membuang barisnya.</p>")

langkah("Layar merah pertamamu minggu ini — dan itu disengaja",
    blok("aksi", "Coba saring pakai window function.", "LAKUKAN"),
    kode("SELECT cabang FROM pesanan\nWHERE row_number() OVER (ORDER BY id) = 1;"),
    keluaran(H, "h1_merah_window_where"),
    "<p>Kamu sudah punya penjelasannya dari Level 1 Hari 6: <code>WHERE</code> berjalan "
    "<strong>sebelum</strong> baris-barisnya lengkap dikumpulkan, jadi tidak ada “urutan” yang "
    "bisa dinomori.</p>")

langkah("HAVING pun ditolak — dan itu memberitahumu urutannya",
    blok("aksi", "Coba pindahkan ke <code>HAVING</code>.", "LAKUKAN"),
    kode('''SELECT cabang, count(*) FROM pesanan
GROUP BY cabang HAVING row_number() OVER () = 1;'''),
    keluaran(H, "h1_merah_window_group"),
    kode('''FROM → WHERE → GROUP BY → HAVING → WINDOW → SELECT → ORDER BY → LIMIT
                                    ^^^^^^
                       di sini, hampir paling akhir''', salin=False),
    "<p>Window function dihitung <strong>setelah</strong> <code>HAVING</code>. Jadi kamu tidak "
    "bisa menyaring dengan hasilnya di query yang sama. Obatnya selalu satu: <strong>bungkus "
    "dengan CTE, lalu saring di luarnya</strong> — pola yang kamu pakai berkali-kali di Level 3.</p>")

langkah("Tiga bagian di dalam OVER",
    blok("aksi", "Salin tabel ini. Kamu akan kembali ke sini sepanjang minggu.", "LAKUKAN"),
    tabel(["Bagian", "Artinya", "Kalau kamu hilangkan"],
          [["<code>PARTITION BY</code>", "Bagi jadi kelompok, hitung ulang tiap kelompok",
            "Seluruh tabel jadi satu kelompok"],
           ["<code>ORDER BY</code>", "Urutkan di dalam kelompok",
            "Tidak ada urutan — dan frame jadi seluruh kelompok"],
           ["<code>ROWS</code>/<code>RANGE</code>/<code>GROUPS</code> (frame)",
            "Baris mana saja yang ikut dihitung",
            "Bawaannya berubah tergantung ada <code>ORDER BY</code> atau tidak"]]),
    "<p>Baris ketiga itu isi seluruh Hari 2, dan <strong>hampir tidak pernah diajarkan</strong>. "
    "Modul M6 tidak pernah menyebutnya sama sekali.</p>")

langkah("Buktikan baris pertama tabel itu",
    blok("aksi", "Hilangkan <code>PARTITION BY</code>-nya.", "LAKUKAN"),
    kode('''SELECT o.cabang, i.jumlah * i.harga_saat_itu AS nilai_baris,
       sum(i.jumlah * i.harga_saat_itu) OVER () AS semua_cabang
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai' ORDER BY o.cabang, o.id LIMIT 3;'''),
    keluaran(H, "h1_over_kosong"),
    "<p>35.739.000 — total seluruh cabang, angka yang sama dengan yang kamu hitung di Level 1. "
    "<code>OVER ()</code> yang kosong berarti “satu kelompok berisi semuanya”. Kalau angkamu "
    "berbeda, kamu sedang menyambung ke basis data yang lain.</p>")

langkah("Buat dulu bahan yang akan kamu pakai",
    blok("aksi", "Ini isi CTE yang kamu pakai di langkah berikutnya. Lihat sendiri isinya dulu.",
         "LAKUKAN"),
    kode("""SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status='selesai' GROUP BY 1 ORDER BY 1;"""),
    keluaran(H, "h1_cte_bulanan"),
    "<p>Enam baris, satu per bulan. <strong>Selalu jalankan isi CTE-mu sendiri sebelum "
    "membungkusnya</strong> — kalau ada yang salah di sini, kamu akan menghabiskan setengah jam "
    "menyalahkan window function yang sebenarnya benar.</p>",
    blok("catatan", "Kebiasaan ini sama dengan menyiapkan skedul pendukung sebelum mengisi lead "
                    "schedule: kamu memeriksa bahannya lebih dulu, bukan angka akhirnya."))

langkah("Sekarang buktikan baris kedua, dan bersiaplah terkejut",
    blok("aksi", "Dua kolom, bedanya cuma dua kata.", "LAKUKAN"),
    kode('''WITH b AS (SELECT to_char(o.tanggal,'YYYY-MM') AS bulan,
                  sum(i.jumlah * i.harga_saat_itu) AS nilai
           FROM pesanan o JOIN item i ON i.pesanan_id = o.id
           WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
       sum(nilai) OVER ()               AS tanpa_order_by,
       sum(nilai) OVER (ORDER BY bulan) AS pakai_order_by
FROM b ORDER BY bulan;'''),
    keluaran(H, "h1_order_by_diam"),
    blok("bahaya", "Kolom ketiga memberi <strong>total</strong>. Kolom keempat memberi "
                   "<strong>running total</strong>. Yang kamu tambahkan cuma dua kata: "
                   "<code>ORDER BY bulan</code>."))

langkah("Dua kata itu diam-diam memasang frame",
    blok("aksi", "Baca sekali, pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Menambahkan <code>ORDER BY</code> ke dalam <code>OVER</code> tidak cuma "
                  "mengurutkan. Ia <strong>mengubah frame</strong> dari “seluruh kelompok” "
                  "menjadi “dari awal sampai baris ini”.</p>", "YANG SEBENARNYA TERJADI"),
    "<p>Itu sebabnya <code>sum(...) OVER (PARTITION BY x)</code> memberi total, sedangkan "
    "<code>sum(...) OVER (PARTITION BY x ORDER BY y)</code> memberi running total — perubahan "
    "besar dari menambahkan dua kata yang kelihatannya cuma soal urutan.</p>",
    blok("catatan", "Kalau kamu pernah bingung kenapa angka kumulatifmu tiba-tiba jadi total, "
                    "atau sebaliknya, <strong>ini penyebabnya</strong>. Besok kamu akan melihat "
                    "sisi yang lebih halus lagi dari frame yang sama."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis query yang menampilkan, untuk <strong>Januari 2024</strong>: nilai "
                 "penjualan tiap cabang, dan berapa persen tiap cabang dari total Januari. "
                 "Pakai window function, bukan dua query.", "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>WITH b AS (SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,\n"
    "                  sum(i.jumlah * i.harga_saat_itu) AS nilai\n"
    "           FROM pesanan o JOIN item i ON i.pesanan_id = o.id\n"
    "           WHERE o.status='selesai' GROUP BY 1,2)\n"
    "SELECT cabang, bulan, nilai,\n"
    "       round(nilai * 100.0 / sum(nilai) OVER (PARTITION BY bulan), 1) AS persen_bulan\n"
    "FROM b WHERE bulan = '2024-01' ORDER BY cabang;</code></pre></div>"
    + keluaran(H, "h1_kunci", tag="HASILNYA") +
    "<p>Pemeriksaanmu: 47,5 + 21,0 + 31,5 = <strong>100,0</strong>. Kalau jumlahnya bukan 100, "
    "partisimu salah — kemungkinan besar kamu memakai <code>PARTITION BY cabang</code> padahal "
    "yang dibagi adalah bulannya.</p>"
    "<p>Perhatikan juga <code>WHERE bulan = '2024-01'</code> berada <strong>di luar</strong> "
    "CTE. Kalau penyaring itu kamu taruh di dalam, hasilnya tetap sama di sini — tapi begitu "
    "kamu menyaring <em>setelah</em> window function menghitung, urutannya jadi penting. Itu "
    "bahan Level 3.</p></details>")

HARI1 = {
  "n": "HARI 1", "tab": "1",
  "judul": "Apa yang sebenarnya dikerjakan OVER",
  "waktu": "± 50 menit",
  "tujuan": "menjelaskan beda window function dan <code>GROUP BY</code> dalam satu kalimat, dan "
            "tahu kapan hanya window function yang bisa menjawab.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> GROUP BY meringkas dan membuang baris; window "
           "function menghitung sambil menyimpan semua baris · <code>PARTITION BY</code> = "
           "kelompok, <code>ORDER BY</code> = urutan <em>dan</em> diam-diam mengubah frame · "
           "window function berjalan setelah <code>WHERE</code> dan <code>HAVING</code>, jadi "
           "tidak bisa dipakai di sana.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 1 dari 8.</strong> Jawab dengan "
           "suara, satu kalimat: <em>apa beda <code>GROUP BY</code> dan window function?</em></p>"
           "<details><summary>Kunci</summary><p><code>GROUP BY</code> meringkas banyak baris "
           "jadi satu; window function menghitung hal yang sama tanpa membuang baris.</p></details>",
}
