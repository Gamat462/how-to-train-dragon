# -*- coding: utf-8 -*-
"""Hari 5 — median tanpa MEDIAN, total berjalan, dan sepuluh pertanyaan lisan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Soal 8 — kerjakan dulu",
    blok("aksi", "Lima belas menit.", "LAKUKAN"),
    kode("""SOAL 8  Berapa MEDIAN nilai satu pesanan?
        (SQLite tidak punya fungsi MEDIAN. Itu bagian dari soalnya.)""", salin=False),
    blok("catatan", "Petunjuk: kamu sudah punya semua bahannya dari Hari 4."))

langkah("Buktikan dulu bahwa fungsinya memang tidak ada",
    blok("aksi", "Coba cara yang paling wajar. Jalankan.", "LAKUKAN"),
    kode('con.execute("SELECT MEDIAN(harga) FROM produk").fetchone()'),
    blok("bahaya", "<pre><code>OperationalError: no such function: MEDIAN</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Sekarang kamu tahu soalnya sungguhan, bukan jebakan kata-kata. <code>MEDIAN</code> "
    "memang tidak ada di SQLite — begitu juga di beberapa basis data lain yang akan kamu "
    "temui.</p>",
    blok("catatan", "<strong>Di PostgreSQL ada penggantinya</strong> "
                    "(<code>PERCENTILE_CONT(0.5)</code>), tapi menuliskannya juga tidak "
                    "sesederhana <code>AVG</code>. Pola yang kamu pelajari di dua langkah "
                    "berikutnya berlaku di mana pun."))

langkah("Kunci soal 8, bagian 1 — beri nomor urut",
    blok("aksi", "Bikin CTE-nya, lalu lihat lima baris pertamanya.", "LAKUKAN"),
    kode("""WITH nilai AS (
  SELECT p.id, SUM(i.jumlah * i.harga_saat_itu) AS total
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status = 'selesai' GROUP BY p.id
)
SELECT total, ROW_NUMBER() OVER (ORDER BY total) AS n, COUNT(*) OVER () AS jml
FROM nilai LIMIT 3"""),
    blok("hasil", "<pre><code>   total  n  jml\n0  10000  1  362\n1  10000  2  362\n"
                  "2  10000  3  362</code></pre>", "HARUS MUNCUL"),
    "<p>Kolom <code>jml</code> berisi 362 di <strong>tiap baris</strong> — itulah "
    "<code>COUNT(*) OVER ()</code> dengan kurung kosong: menempelkan angka total ke setiap baris "
    "tanpa <code>JOIN</code> tambahan.</p>")

langkah("Kunci soal 8",
    blok("aksi", "Jalankan, lalu baca baris <code>WHERE</code>-nya baik-baik.", "LAKUKAN"),
    kode("""WITH nilai AS (
  SELECT p.id, SUM(i.jumlah * i.harga_saat_itu) AS total
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status = 'selesai' GROUP BY p.id
),
urut AS (
  SELECT total,
         ROW_NUMBER() OVER (ORDER BY total) AS n,
         COUNT(*)     OVER ()               AS jml
  FROM nilai
)
SELECT ROUND(AVG(total)) AS median
FROM urut
WHERE n IN ((jml + 1) / 2, (jml + 2) / 2)"""),
    blok("hasil", "<pre><code>    median\n0  90000.0</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau punyamu mengeluarkan dua baris, bukan satu</strong>, "
                    "<code>AVG</code>-mu hilang — tanpa dia, query ini mengembalikan kedua baris "
                    "tengahnya, bukan rata-ratanya. Itu wajar terjadi dan gampang dilewatkan."),
    "<p>Perhatikan <code>COUNT(*) OVER ()</code> dengan kurung kosong: itu cara menempelkan "
    "angka total ke <strong>tiap baris</strong> tanpa <code>JOIN</code> tambahan.</p>")

langkah("Kenapa triknya bekerja untuk ganjil dan genap sekaligus",
    blok("aksi", "Hitung di kertas untuk dua kasus.", "LAKUKAN"),
    tabel(["Jumlah baris", "<code>(jml+1)/2</code>", "<code>(jml+2)/2</code>", "Yang terjadi"],
          [["7 (ganjil)", "4", "4", "baris yang sama, diambil sekali"],
           ["8 (genap)", "4", "5", "dua baris tengah, lalu <code>AVG</code> merata-ratakannya"]]),
    "<p>Dan justru <strong>pembagian bilangan bulat</strong> yang kemarin merusak persentasemu "
    "adalah yang membuat trik ini bekerja. Satu query, tanpa <code>CASE</code>.</p>")

langkah("Sekarang bagian yang membuat soal ini berharga",
    blok("aksi", "Hitung rata-ratanya juga, dan bandingkan.", "LAKUKAN"),
    kode("""WITH nilai AS (
  SELECT p.id, SUM(i.jumlah * i.harga_saat_itu) AS total
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status='selesai' GROUP BY p.id)
SELECT COUNT(*) AS pesanan, ROUND(AVG(total)) AS rata_rata,
       MIN(total) AS terkecil, MAX(total) AS terbesar
FROM nilai"""),
    blok("hasil", "<pre><code>   pesanan  rata_rata  terkecil  terbesar\n"
                  "0      362    98727.0     10000    308000</code></pre>", "HARUS MUNCUL"),
    "<p>Median 90.000, rata-rata 98.727 — <strong>rata-rata lebih tinggi 9,7%</strong>, ditarik "
    "ke atas oleh pesanan besar sampai 308.000. Separuh pesanan sebenarnya di bawah 90.000.</p>",
    blok("hasil", "<p>Kalau klien bertanya “berapa biasanya orang belanja di sini?”, "
                  "<strong>90.000 lebih jujur daripada 98.727.</strong></p>", "YANG KAMU JAWAB"))

langkah("Agregat di dalam agregat — dan cara yang benar",
    blok("aksi", "Coba jumlahkan sebuah hitungan langsung. Sengaja.", "LAKUKAN"),
    kode('con.execute("SELECT SUM(COUNT(*)) FROM pesanan").fetchone()'),
    blok("bahaya", "<pre><code>OperationalError: misuse of aggregate function COUNT()</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("aksi", "Cara yang benar: hitung dulu di dalam, jumlahkan di luar.", "LAKUKAN"),
    kode('con.execute("""SELECT SUM(n) FROM\n'
         '  (SELECT COUNT(*) AS n FROM pesanan GROUP BY cabang)""").fetchone()'),
    blok("hasil", "<pre><code>(400,)</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Agregat tidak bisa dibungkus agregat</strong> dalam satu tingkat — ia butuh "
    "tingkat kedua, persis seperti rata-rata per pesanan di Hari 2 dan top-N di Hari 4. "
    "Kalau kamu mulai melihat pola ini, kamu sudah berpikir seperti orang yang menulis SQL "
    "setiap hari.</p>")

langkah("Soal 9 — kerjakan dulu",
    blok("aksi", "Lima belas menit.", "LAKUKAN"),
    kode("SOAL 9  Omzet tiap bulan, disertai total berjalan sejak awal tahun.", salin=False))

langkah("Kunci soal 9",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""WITH bulanan AS (
  SELECT substr(p.tanggal,1,7) AS bulan,
         SUM(i.jumlah * i.harga_saat_itu) AS omzet
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status = 'selesai' GROUP BY bulan
)
SELECT bulan, omzet,
       SUM(omzet) OVER (ORDER BY bulan
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total_berjalan
FROM bulanan ORDER BY bulan"""),
    blok("hasil", "<pre><code>     bulan    omzet  total_berjalan\n0  2024-01  5968000         5968000\n"
                  "1  2024-02  6351000        12319000\n2  2024-03  5574000        17893000\n"
                  "3  2024-04  5754000        23647000\n4  2024-05  6272000        29919000\n"
                  "5  2024-06  5820000        35739000</code></pre>", "HARUS MUNCUL"),
    "<p>Periksa: <strong>35.739.000</strong> di baris terakhir. Bandingkan dengan soal 1 — "
    "12.665.000 + 11.669.000 + 11.405.000 = 35.739.000. Cocok.</p>")

langkah("Baris ROWS itu wajib, dan ini pertanyaan jebakan favorit",
    blok("aksi", "Baca sekali. Ini yang membedakan hafal dari paham.", "LAKUKAN"),
    blok("hasil", "<p>Tanpa <code>ROWS …</code>, bawaan SQL bukan “tanpa bingkai” melainkan "
                  "<code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code> — dan "
                  "<code>RANGE</code> memperlakukan <strong>semua baris dengan nilai urut yang "
                  "sama</strong> sebagai satu kesatuan.</p>", "YANG HARUS KAMU TAHU"),
    blok("bahaya", "Di sini tiap bulan unik, jadi hasilnya <em>kebetulan</em> sama. Begitu ada "
                   "dua baris dengan bulan yang sama, <code>RANGE</code> menjumlahkan keduanya "
                   "sekaligus di kedua baris, dan total berjalanmu melompat. "
                   "<strong>Selalu tulis <code>ROWS</code> secara eksplisit.</strong>"))

langkah("Sekarang berhenti mengetik. Jawab dengan suara keras.",
    blok("aksi", "Lima pertanyaan pertama. Baca soalnya, <strong>ucapkan jawabanmu "
                 "bersuara</strong>, baru buka kuncinya.", "LAKUKAN"),
    kode("""1. Apa bedanya WHERE dan HAVING?
2. Apa bedanya INNER JOIN dan LEFT JOIN?
3. Kenapa COUNT(*) dan COUNT(kolom) bisa beda?
4. Apa itu window function, dan kapan dipakai?
5. Kenapa NULL = NULL tidak menghasilkan benar?""", salin=False),
    blok("catatan", "<strong>Mengucapkan itu keterampilan yang terpisah dari mengetahui</strong>, "
                    "dan wawancara menguji yang pertama. Kalau kamu merasa konyol bersuara "
                    "sendirian, itu normal — dan jauh lebih murah daripada merasa konyol di "
                    "depan pewawancara."))

langkah("Kunci lima pertanyaan pertama",
    blok("aksi", "Baca, lalu ulangi bersuara sekali lagi dengan kalimatmu sendiri.", "LAKUKAN"),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p><strong>1.</strong> <code>WHERE</code> menyaring baris sebelum dikelompokkan; "
    "<code>HAVING</code> menyaring kelompok sesudahnya. <em>Nilai tambah:</em> “kalau saringannya "
    "bisa ditaruh di <code>WHERE</code>, taruh di situ — lebih sedikit yang harus dikelompokkan.”</p>"
    "<p><strong>2.</strong> <code>INNER</code> hanya menyimpan baris yang punya pasangan di kedua "
    "tabel; <code>LEFT</code> menyimpan semua baris kiri dan mengisi <code>NULL</code>. "
    "<em>Nilai tambah:</em> “pertanyaan ‘siapa yang belum pernah pesan’ cuma bisa dijawab dengan "
    "<code>LEFT JOIN … WHERE kanan.id IS NULL</code> atau <code>NOT EXISTS</code>. "
    "<code>INNER JOIN</code> menghapus persis orang yang sedang dicari.”</p>"
    "<p><strong>3.</strong> <code>COUNT(*)</code> menghitung baris; <code>COUNT(kolom)</code> "
    "menghitung baris yang kolomnya bukan <code>NULL</code>. <em>Nilai tambah:</em> “di "
    "<code>senja.db</code>, 400 lawan 388 — selisih dua angka itu cara tercepat menghitung "
    "<code>NULL</code>.”</p>"
    "<p><strong>4.</strong> Fungsi yang menghitung dari sekelompok baris <strong>tanpa "
    "menggabungkan barisnya</strong>. <code>GROUP BY</code> memberi 3 baris dari 400; window "
    "function tetap memberi 400.</p>"
    "<p><strong>5.</strong> <code>NULL</code> berarti “tidak diketahui”. Dua hal yang sama-sama "
    "tidak diketahui belum tentu sama. <em>Nilai tambah:</em> “itu juga yang membuat "
    "<code>NOT IN</code> berbahaya.”</p></details>",
    blok("aksi", "Buktikan jawaban nomor 3 sendiri:", "LAKUKAN"),
    kode('print(con.execute("SELECT COUNT(*), COUNT(pelanggan_id) FROM pesanan").fetchone())'),
    blok("hasil", "<pre><code>(400, 388)</code></pre>", "HARUS MUNCUL"))

langkah("Lima pertanyaan berikutnya",
    blok("aksi", "Sama caranya: ucapkan dulu, baru buka.", "LAKUKAN"),
    kode("""6.  Apa itu index, dan kapan TIDAK dipakai?
7.  Apa itu transaksi, dan kapan kamu memerlukannya?
8.  Apa bedanya VIEW dan tabel ringkasan?
9.  Query-mu lambat. Apa yang kamu lakukan pertama?
10. Bagaimana kamu tahu hasil query-mu benar?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p><strong>6.</strong> Daftar terurut supaya basis data melompat langsung ke barisnya. "
    "Tidak terpakai kalau kolomnya dibungkus fungsi, <code>LIKE</code>-nya diawali <code>%</code>, "
    "atau ia bukan kolom terkiri index gabungan. <em>Nilai tambah:</em> “aku pernah mengukurnya: "
    "39 ms jadi 0,006 ms — tapi tiga index membuat berkasnya dua kali lebih besar dan penulisan "
    "tiga kali lebih lambat.”</p>"
    "<p><strong>7.</strong> Sekumpulan perintah yang berhasil semua atau gagal semua. "
    "<em>Nilai tambah:</em> “sama seperti jurnal — debit dan kredit dicatat bersama atau tidak "
    "sama sekali.”</p>"
    "<p><strong>8.</strong> <code>VIEW</code> query yang diberi nama, selalu terbaru tapi "
    "selambat aslinya. Tabel ringkasan cepat dibaca tapi basi. <em>Nilai tambah:</em> “tabel "
    "ringkasanku selalu bawa kolom waktu pembuatannya.”</p>"
    "<p><strong>9.</strong> Jalankan <code>EXPLAIN QUERY PLAN</code> dan cari <code>SCAN</code> "
    "pada tabel besar — <strong>bukan</strong> langsung menambah index. <em>Nilai tambah:</em> "
    "“yang paling sering kutemukan subquery berkorelasi; pernah kuukur 6,2 detik jadi 6 "
    "milidetik cuma dengan memindahkannya ke CTE.”</p>"
    "<p><strong>10.</strong> Lihat langkah berikutnya — ini yang terpenting.</p></details>")

langkah("Pertanyaan nomor 10, dan kenapa cuma kamu yang bisa menjawabnya",
    blok("aksi", "Baca jawabannya, lalu ucapkan bersuara tiga kali.", "LAKUKAN"),
    blok("hasil", "<p>“Aku cocokkan totalnya dengan angka yang sudah diketahui. Kalau tabel "
                  "pesanan berisi 400 baris dan 38 batal, hasil per cabang harus berjumlah 362 — "
                  "dan aku periksa itu tiap kali. Lalu aku punya berkas pemeriksaan mutu yang "
                  "jalan sebelum apa pun dikirim: baris yatim, nilai tidak masuk akal, dan "
                  "rekonsiliasi dengan sistem lain. Tiap pemeriksaan punya batas, jadi kalau "
                  "angkanya naik dari kemarin aku tahu di hari yang sama.”</p>",
         "JAWABAN YANG KAMU SIAPKAN"),
    blok("catatan", "<strong>Kalau kamu cuma bisa menyiapkan satu jawaban dari sepuluh, siapkan "
                    "yang ini.</strong> Sembilan pertanyaan pertama bisa dijawab siapa pun yang "
                    "belajar seminggu. Yang ini cuma bisa dijawab orang yang pernah mengirim "
                    "angka salah — atau yang cukup berhati-hati untuk tidak pernah melakukannya. "
                    "Latar auditmu membuat jawaban ini terdengar wajar dari mulutmu."))

HARI5 = {
  "n": "HARI 5", "tab": "5",
  "judul": "Dua soal terakhir, lalu berhenti mengetik dan mulai bicara",
  "waktu": "± 80 menit",
  "tujuan": "menyelesaikan soal yang fungsinya tidak ada di SQLite, dan menjawab sepuluh "
            "pertanyaan konsep <strong>dengan suara keras</strong> — pendek, benar, dan tidak "
            "terdengar seperti hafalan.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> dua pola yang jarang dikuasai kandidat (median "
           "tanpa <code>MEDIAN</code>, dan <code>ROWS</code> yang eksplisit), dan sepuluh jawaban "
           "lisan yang sudah pernah keluar dari mulutmu — bukan cuma lewat di matamu.</p>"
           "<p style=\"margin-top:8px\">Besok tidak ada soal SQL sama sekali. Besok satu "
           "kalimat pertanyaan, dan enam jawaban yang semuanya benar.</p>",
}
