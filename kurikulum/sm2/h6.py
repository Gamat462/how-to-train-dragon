# -*- coding: utf-8 -*-
"""Hari 6 — kerangka waktu dua dimensi dan LATERAL."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Rentang tanggal datamu, sebelum kamu membuat kerangka",
    blok("aksi", "Satu baris.", "LAKUKAN"),
    kode("SELECT min(tanggal) AS awal, max(tanggal) AS akhir FROM pesanan;"),
    keluaran(H, "h6_rentang"),
    "<p>Januari sampai akhir Juni 2024. <strong>Kerangka yang kamu buat tidak boleh lebih luas "
    "dari ini tanpa alasan</strong> — kalau kamu membuat deret sampai Desember, laporanmu akan "
    "penuh nol yang artinya “belum ada data”, bukan “tidak ada penjualan”. Dua hal yang sangat "
    "berbeda bagi orang yang membaca laporanmu.</p>")

langkah("Kerangka dua dimensi: tiap tanggal × tiap cabang",
    blok("aksi", "Berkas <code>senja/l2-hari-6.sql</code>. Gabungkan "
                 "<code>generate_series</code> dari Level 1 dengan <code>CROSS JOIN</code>.",
         "LAKUKAN"),
    kode('''SELECT d::date AS tanggal, c.cabang,
       COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
FROM generate_series(DATE '2024-01-01', DATE '2024-01-03', INTERVAL '1 day') AS d
CROSS JOIN (SELECT DISTINCT cabang FROM pesanan) c
LEFT JOIN pesanan o ON o.tanggal = d::date AND o.cabang = c.cabang AND o.status='selesai'
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY d, c.cabang ORDER BY d, c.cabang;'''),
    keluaran(H, "h6_kerangka_2d"),
    "<p>Sembilan baris: 3 tanggal × 3 cabang, <strong>tanpa satu pun yang hilang</strong>. Angka "
    "tanggal 3 cocok dengan yang kamu lihat di Hari 2 (217.000 / 160.000 / 66.000) — itu "
    "pemeriksaannya.</p>",
    blok("catatan", "<code>generate_series</code> adalah kemewahan PostgreSQL. Di SQLite dan "
                    "beberapa mesin lain kamu harus membuat deret tanggalnya dengan "
                    "<strong>recursive CTE</strong> — bentuk yang sudah kamu kuasai kemarin:"
                    "<br><code>WITH RECURSIVE tgl(d) AS (SELECT DATE '2024-01-01' "
                    "UNION ALL SELECT d + 1 FROM tgl WHERE d &lt; DATE '2024-01-03')</code>"
                    "<br>Gagasannya sama; yang berbeda cuma berapa baris yang harus kamu "
                    "ketik."))

langkah("Kenapa bentuk ini yang dibutuhkan hampir semua dashboard",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Alat visualisasi <strong>tidak bisa menggambar sesuatu yang tidak ada "
                  "barisnya</strong>. Ia akan menyambung garis melewati hari kosong, atau "
                  "menghilangkan cabang dari legenda di bulan ia tidak berjualan.</p>",
         "AKIBAT KALAU KERANGKANYA TIDAK ADA"),
    "<p>Membuat kerangka lengkap lebih dulu adalah langkah yang membedakan laporan yang benar "
    "dari laporan yang <em>terlihat</em> benar.</p>")

langkah("Bahan kerangkamu: daftar cabang",
    blok("aksi", "Satu baris.", "LAKUKAN"),
    kode("SELECT DISTINCT cabang FROM pesanan ORDER BY 1;"),
    keluaran(H, "h6_cabang"),
    "<p>Tiga cabang. Dikalikan 3 tanggal, kerangkamu <strong>harus</strong> berisi 9 baris — dan "
    "tadi memang 9. Ini pemeriksaan perkalian yang sama seperti kamu memeriksa lead schedule: "
    "jumlah barisnya harus bisa kamu ramalkan sebelum query-nya jalan.</p>")

langkah("Ramalkan ukuran kerangkanya sebelum mengisinya",
    blok("aksi", "Lima hari × tiga cabang. Berapa baris seharusnya?", "LAKUKAN"),
    kode("""SELECT count(*) AS baris_kerangka
FROM generate_series(DATE '2024-01-01', DATE '2024-01-05', INTERVAL '1 day') AS d
CROSS JOIN (SELECT DISTINCT cabang FROM pesanan) c;"""),
    keluaran(H, "h6_cte_lengkap"),
    "<p>Lima belas. <strong>Angka itu kamu tahu sebelum menyentuh data penjualan</strong> — dan "
    "kalau hasil akhirmu nanti bukan 15 baris, kamu tidak perlu menebak di mana salahnya.</p>")

langkah("Kerangka + window function: kumulatif per cabang",
    blok("aksi", "Sekarang gabungkan dua alat minggu ini.", "LAKUKAN"),
    kode('''WITH lengkap AS (
  SELECT d::date AS tanggal, c.cabang,
         COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
  FROM generate_series(DATE '2024-01-01', DATE '2024-01-05', INTERVAL '1 day') AS d
  CROSS JOIN (SELECT DISTINCT cabang FROM pesanan) c
  LEFT JOIN pesanan o ON o.tanggal = d::date AND o.cabang = c.cabang AND o.status='selesai'
  LEFT JOIN item i ON i.pesanan_id = o.id
  GROUP BY d, c.cabang)
SELECT tanggal, cabang, nilai,
       sum(nilai) OVER (PARTITION BY cabang ORDER BY tanggal
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
FROM lengkap ORDER BY cabang, tanggal LIMIT 10;'''),
    keluaran(H, "h6_kumulatif_per_cabang"),
    "<p>Garis kumulatif per cabang yang <strong>tidak pernah datar palsu</strong>: hari tanpa "
    "penjualan tetap punya baris, jadi grafiknya mendatar di tempat yang benar, bukan melompat "
    "melewati hari itu.</p>",
    blok("catatan", "Di sini <code>ROWS</code> dan <code>RANGE</code> memberi angka yang sama, "
                    "karena setelah dipartisi per cabang tiap tanggal cuma punya satu baris. "
                    "Frame-nya tetap ditulis — supaya pembaca berikutnya tidak perlu menebak."))

langkah("Soal yang paling sering ditanyakan: top-N per kelompok",
    blok("aksi", "Dua produk terlaris di tiap cabang. Cara pertama: window function, seperti "
                 "kemarin.", "LAKUKAN"),
    kode('''SELECT cabang, nama, terjual FROM (
  SELECT o.cabang, p.nama, sum(i.jumlah) AS terjual,
         row_number() OVER (PARTITION BY o.cabang
                            ORDER BY sum(i.jumlah) DESC, p.nama) AS n
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  JOIN produk p ON p.id = i.produk_id
  WHERE o.status = 'selesai'
  GROUP BY o.cabang, p.nama) x
WHERE n <= 2 ORDER BY cabang, terjual DESC;'''),
    keluaran(H, "h6_lateral_vs_window"),
    "<p>Perhatikan <code>ORDER BY sum(i.jumlah) DESC</code> <em>di dalam</em> "
    "<code>OVER</code> — window function boleh mengurutkan pakai hasil agregat, karena ia "
    "berjalan setelah <code>GROUP BY</code>.</p>")

langkah("Cara kedua: LATERAL, subquery yang boleh menoleh ke kiri",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''SELECT c.cabang, t.nama, t.terjual
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN LATERAL (
  SELECT p.nama, sum(i.jumlah) AS terjual
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  JOIN produk p ON p.id = i.produk_id
  WHERE o.cabang = c.cabang AND o.status = 'selesai'
  GROUP BY p.nama ORDER BY sum(i.jumlah) DESC, p.nama LIMIT 2) t
ORDER BY c.cabang, t.terjual DESC;'''),
    keluaran(H, "h6_lateral"),
    "<p>Hasilnya <strong>sama persis</strong> dengan langkah sebelumnya. Yang berbeda adalah cara "
    "kamu berpikir: “untuk tiap cabang, jalankan query kecil ini”. Kamu sudah pernah bekerja "
    "begitu — satu prosedur, diulang per akun.</p>")

langkah("Satu kata yang membuat LATERAL bekerja",
    blok("aksi", "Lihat baris <code>WHERE o.cabang = c.cabang</code> di dalam subquery-nya.",
         "LAKUKAN"),
    blok("hasil", "<p>Subquery biasa <strong>tidak boleh</strong> menyebut kolom dari tabel di "
                  "sebelah kirinya. <code>LATERAL</code> mencabut larangan itu.</p>",
         "YANG DIKERJAKANNYA"),
    "<p>Karena itu <code>LIMIT 2</code> di dalamnya berarti “dua teratas <em>untuk cabang "
    "ini</em>”, bukan dua teratas dari seluruh tabel.</p>")

langkah("Buktikan larangannya, dengan sengaja",
    blok("aksi", "Hapus kata <code>LATERAL</code>, jalankan.", "LAKUKAN"),
    kode('''SELECT c.cabang, t.nama
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN (
  SELECT p.nama FROM produk p WHERE p.id = length(c.cabang) LIMIT 1) t;'''),
    keluaran(H, "h6_merah_lateral"),
    "<p>Tanpa <code>LATERAL</code>, subquery itu dievaluasi sendirian — dan bagi dia, "
    "<code>c</code> tidak ada.</p>",
    blok("catatan", "Setiap kali kamu melihat <em>invalid reference to FROM-clause entry</em>, "
                    "pertanyaannya selalu sama: <strong>apakah aku sedang menoleh ke kiri?</strong> "
                    "Kalau ya, tambahkan <code>LATERAL</code>."))

langkah("Kapan pakai yang mana",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    tabel(["Cara", "Pakai kalau", "Hati-hati"],
          [["<code>row_number</code> + saring di luar",
            "Kelompoknya banyak dan datanya sudah teragregasi",
            "Memberi nomor ke <em>semua</em> baris lalu membuang sebagian besar"],
           ["<code>CROSS JOIN LATERAL … LIMIT n</code>",
            "Kelompoknya sedikit, tiap kelompok datanya banyak",
            "Query kecilnya dijalankan sekali per kelompok"],
           ["<code>DISTINCT ON</code> (Level 1)", "Cuma butuh <strong>satu</strong> baris per "
            "kelompok", "Khas PostgreSQL — tidak bisa dibawa ke mesin lain"]]),
    "<p>Ketiganya benar. Yang ditanyakan di wawancara biasanya yang pertama, karena itu yang "
    "berjalan di semua mesin — tapi menyebut dua yang lain menunjukkan kamu tahu ada "
    "pilihan.</p>")

langkah("LEAD untuk menemukan lubang di deret tanggal",
    blok("aksi", "Berapa hari jarak terjauh antara dua hari jualan di Januari?", "LAKUKAN"),
    kode('''WITH hari AS (
  SELECT DISTINCT tanggal FROM pesanan WHERE status='selesai'
    AND tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-31')
SELECT tanggal, lead(tanggal) OVER (ORDER BY tanggal) AS berikutnya,
       lead(tanggal) OVER (ORDER BY tanggal) - tanggal AS jeda_hari
FROM hari
ORDER BY jeda_hari DESC NULLS LAST, tanggal
LIMIT 5;'''),
    keluaran(H, "h6_gap_hari"),
    "<p>Tiga kali jeda dua hari. Karena kolom <code>tanggal</code> bertipe <code>date</code>, "
    "mengurangkannya langsung menghasilkan <strong>jumlah hari</strong> — bukan teks, bukan "
    "detik.</p>",
    blok("catatan", "<code>NULLS LAST</code> di <code>ORDER BY</code> penting di sini: baris "
                    "terakhir tidak punya “berikutnya”, jadi jedanya <code>NULL</code>. Tanpa "
                    "<code>NULLS LAST</code>, PostgreSQL menaruhnya di atas pada urutan "
                    "<code>DESC</code> — dan baris kosong itu akan menempati tempat teratas "
                    "laporanmu."))

langkah("Kerjakan sendiri",
    blok("aksi", "Untuk <strong>seluruh Januari</strong>, hitung: berapa hari kalender, berapa "
                 "hari tanpa transaksi, rata-rata harian menghitung semua hari, dan rata-rata "
                 "harian hanya menghitung hari jualan.", "KERJAKAN, ± 15 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>WITH lengkap AS (\n"
    "  SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai\n"
    "  FROM generate_series(DATE '2024-01-01', DATE '2024-01-31', INTERVAL '1 day') AS d\n"
    "  LEFT JOIN pesanan o ON o.tanggal = d::date AND o.status='selesai'\n"
    "  LEFT JOIN item i ON i.pesanan_id = o.id\n"
    "  GROUP BY d)\n"
    "SELECT count(*) AS hari_kalender,\n"
    "       count(*) FILTER (WHERE nilai = 0) AS hari_tanpa_transaksi,\n"
    "       round(avg(nilai))                          AS rata2_semua_hari,\n"
    "       round(avg(nilai) FILTER (WHERE nilai &gt; 0)) AS rata2_hari_jualan\n"
    "FROM lengkap;</code></pre></div>"
    + keluaran(H, "h6_kunci", tag="HASILNYA") +
    "<p>Tiga hari tanpa transaksi dari 31 hari. Selisih kedua rata-ratanya cuma 11% di sini — "
    "kecil, tapi <strong>itu karena kamu memeriksanya</strong>. Di bulan yang kedainya tutup "
    "seminggu, selisih itu bisa 30% dan tidak ada yang memberitahumu.</p>"
    "<p>Kalimat yang ikut ke laporan: “rata-rata harian Rp 192.516 dihitung atas 31 hari "
    "kalender, termasuk 3 hari tanpa transaksi.” Satu kalimat, dan pembacamu tidak perlu "
    "menebak.</p></details>")

HARI6 = {
  "n": "HARI 6", "tab": "6",
  "judul": "Kerangka waktu, LATERAL, dan top-N per kelompok",
  "waktu": "± 60 menit",
  "tujuan": "membuat kerangka tanggal × kategori yang lengkap, dan mengambil N teratas per "
            "kelompok dengan tiga cara yang berbeda.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>generate_series</code> + "
           "<code>CROSS JOIN</code> membuat kerangka dua dimensi · kerangka dulu, window "
           "function sesudahnya · top-N per kelompok punya tiga jalan "
           "(<code>row_number</code>, <code>LATERAL</code>, <code>DISTINCT ON</code>) · dan "
           "<code>LATERAL</code> adalah izin untuk menoleh ke kiri.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 6 dari 8.</strong> Jawab dengan "
           "suara: <em>kenapa syarat tambahan di <code>LEFT JOIN</code> harus ditaruh di "
           "<code>ON</code> dan bukan <code>WHERE</code>?</em></p>"
           "<details><summary>Kunci</summary><p>Syarat di <code>WHERE</code> dijalankan setelah "
           "JOIN selesai, jadi baris kiri yang tidak punya pasangan (nilainya <code>NULL</code>) "
           "ikut terbuang — <code>LEFT JOIN</code>-nya berubah jadi <code>INNER JOIN</code>, dan "
           "hari-hari kosong lenyap dari kerangkamu.</p></details>",
}
