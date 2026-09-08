# -*- coding: utf-8 -*-
"""Hari 7 — himpunan, rekonsiliasi, kerangka tanggal, dan satu soal terapan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Menyamping dengan JOIN, ke bawah dengan himpunan",
    blok("aksi", "Berkas <code>senja/hari-7.sql</code>. Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p><code>JOIN</code> menambah <strong>kolom</strong>. Operasi himpunan "
                  "menumpuk hasil dan menambah <strong>baris</strong>.</p>", "BEDANYA"),
    "<p>Syaratnya cuma satu: <strong>jumlah dan urutan kolomnya harus sama</strong>. Nama "
    "kolomnya boleh berbeda — yang dipakai adalah nama dari bagian pertama.</p>")

langkah("Empat operasi, dan yang mana yang bawaanmu",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    tabel(["Operasi", "Artinya", "Baris kembar"],
          [["<code>UNION ALL</code>", "Tumpuk apa adanya",
            "Dibiarkan — <strong>dan ini yang biasanya kamu mau</strong>"],
           ["<code>UNION</code>", "Tumpuk lalu buang kembar",
            "Dibuang (mahal — perlu mengurutkan seluruh hasil)"],
           ["<code>INTERSECT</code>", "Hanya yang ada di kedua sisi", "Dibuang"],
           ["<code>EXCEPT</code>", "Ada di kiri, tidak ada di kanan", "Dibuang"]]),
    "<p>Bawaan orang adalah menulis <code>UNION</code>, dan itu hampir selalu keliru.</p>",
    blok("catatan", "Di Oracle dan SQL Server, <code>EXCEPT</code> bernama <code>MINUS</code>. "
                    "Gagasannya sama; namanya saja yang berbeda."))

langkah("Buktikan apa yang ditelan UNION",
    blok("aksi", "Bayangkan dua transaksi sah yang kebetulan identik.", "LAKUKAN"),
    kode('''SELECT 'A' AS x, 10000 AS n
UNION     SELECT 'A', 10000
UNION     SELECT 'B', 20000;'''),
    keluaran(H, "h7_union_buang"),
    blok("bahaya", "Tiga baris masuk, <strong>dua baris keluar</strong>. Kalau kamu menumpuk "
                   "penjualan Januari dan Februari dengan <code>UNION</code>, dua transaksi yang "
                   "kebetulan sama persis (produk sama, harga sama, jumlah sama) dianggap satu. "
                   "<strong>Uangnya hilang dari laporan tanpa jejak.</strong>"))

langkah("Ganti satu kata dan uangnya kembali",
    blok("aksi", "Jalankan versi <code>UNION ALL</code>-nya.", "LAKUKAN"),
    kode('''SELECT 'A' AS x, 10000 AS n
UNION ALL SELECT 'A', 10000
UNION ALL SELECT 'B', 20000;'''),
    keluaran(H, "h7_union_all"),
    "<p>Tiga baris, <code>A</code> muncul dua kali. Itu yang benar — <strong>dan itu yang lebih "
    "cepat</strong>, karena tidak perlu mengurutkan seluruh hasil untuk mencari kembar.</p>")

langkah("Layar merah yang menyelamatkanmu",
    blok("aksi", "Tumpuk dua hasil yang jumlah kolomnya tidak sama.", "LAKUKAN"),
    kode("SELECT id, nama FROM produk UNION ALL SELECT id FROM pelanggan;"),
    keluaran(H, "h7_merah_kolom"),
    blok("catatan", "<strong>Ini pesan error yang ramah.</strong> SQL memeriksa jumlah kolom, "
                    "tapi <em>tidak</em> memeriksa apakah artinya cocok — menumpuk kolom "
                    "<code>harga</code> di atas kolom <code>jumlah</code> akan lolos tanpa "
                    "sepatah kata pun. Urutan kolom tetap tanggung jawabmu."))

langkah("Kasusnya: dua sistem yang seharusnya sama",
    blok("aksi", "Baca sekali, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p><code>pesanan_kasir</code> adalah <strong>ekspor dari mesin kasir</strong>. "
                  "<code>pesanan</code> + <code>item</code> adalah <strong>pembukuannya</strong>. "
                  "Keduanya seharusnya sama.</p>", "DUANYA HARUS TUTUP"),
    "<p>Pertanyaan pertama selalu sama, dan bukan “berapa selisihnya”: <strong>berapa banyak "
    "yang cocok, dan berapa yang tidak?</strong></p>")

langkah("Hitung dulu, jangan langsung ke rupiah",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH buku AS (
  SELECT o.id, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT 'selesai di pembukuan' AS keterangan, count(*) AS jumlah FROM buku
UNION ALL SELECT 'baris di ekspor kasir', count(*) FROM pesanan_kasir
UNION ALL SELECT 'id cocok',
  (SELECT count(*) FROM buku b JOIN pesanan_kasir k ON k.id = b.id)
UNION ALL SELECT 'hanya di pembukuan',
  (SELECT count(*) FROM (SELECT id FROM buku EXCEPT SELECT id FROM pesanan_kasir) x)
UNION ALL SELECT 'hanya di kasir',
  (SELECT count(*) FROM (SELECT id FROM pesanan_kasir EXCEPT SELECT id FROM buku) y);'''),
    keluaran(H, "h7_hitung_cocok"),
    "<p>Lima angka, satu query. Sebelum kamu membacanya, perhatikan bahwa keempat angka terakhir "
    "seharusnya bisa kamu jumlahkan sendiri jadi dua angka pertama.</p>",
    blok("catatan", "PostgreSQL <strong>mewajibkan</strong> subquery di <code>FROM</code> punya "
                    "nama — itulah <code>x</code> dan <code>y</code> di dua baris terakhir. Kalau "
                    "kamu lupa, errornya berbunyi <em>subquery in FROM must have an alias</em>. "
                    "SQLite tidak mewajibkannya; ini salah satu error pertama yang menyambut "
                    "pendatang."))

langkah("Periksa angkanya sendiri sebelum melangkah",
    blok("aksi", "Hitung di kepalamu, jangan pakai kalkulator.", "LAKUKAN"),
    kode('''359 + 3 = 362   ✓ (semua yang di pembukuan terjelaskan)
359 + 2 = 361   ✓ (semua yang di kasir terjelaskan)''', salin=False),
    "<p>Tidak ada baris yang tidak terjelaskan. Kalau salah satu penjumlahan itu tidak tutup, "
    "<strong>ada yang salah di query-mu, bukan di datanya</strong> — dan kamu tahu itu sebelum "
    "melihat satu rupiah pun.</p>",
    blok("bahaya", "Perhatikan bahwa selisih jumlah barisnya cuma <strong>satu</strong> "
                   "(362 lawan 361). Kalau kamu berhenti di situ — “cuma beda 1, dibulatkan "
                   "saja” — kamu melewatkan lima masalah yang berbeda."))

langkah("Cara kedua menghitung yang cocok",
    blok("aksi", "<code>INTERSECT</code>, supaya kamu tidak percaya pada satu query saja.",
         "LAKUKAN"),
    kode('''SELECT count(*) AS id_di_dua_sisi FROM (
  SELECT id FROM pesanan WHERE status = 'selesai'
  INTERSECT SELECT id FROM pesanan_kasir) x;'''),
    keluaran(H, "h7_intersect"),
    "<p>359 lagi, dan kamu sampai ke sana lewat jalan yang sama sekali berbeda. Itu cara kamu "
    "tahu angkanya bukan kebetulan.</p>")

langkah("Tunjukkan barisnya, bukan cuma jumlahnya",
    blok("aksi", "<code>EXCEPT</code> dua arah.", "LAKUKAN"),
    kode('''SELECT 'hanya pembukuan' AS sisi, id FROM (
  SELECT id FROM pesanan WHERE status='selesai'
  EXCEPT SELECT id FROM pesanan_kasir) a
UNION ALL
SELECT 'hanya kasir', id FROM (
  SELECT id FROM pesanan_kasir
  EXCEPT SELECT id FROM pesanan WHERE status='selesai') b
ORDER BY 1 DESC, 2;'''),
    keluaran(H, "h7_except"),
    "<p>Lima nomor yang bisa kamu tanyakan ke orangnya besok pagi. Jumlah tidak bisa "
    "ditindaklanjuti siapa pun; <strong>nomor bisa</strong>.</p>")

langkah("Baca bentuk id-nya",
    blok("aksi", "Lihat lagi kelima nomor di atas. Ada pola yang berbicara.", "LAKUKAN"),
    blok("hasil", "<p>7, 88, dan 251 terlihat wajar. Tapi <strong>9001 dan 9002 jelas beda "
                  "pola</strong> — kemungkinan besar transaksi yang diinput manual di kasir, "
                  "bukan lewat sistem pesanan.</p>", "YANG DILIHAT MATA"),
    blok("catatan", "Itu <strong>petunjuk, bukan kesimpulan</strong>. Yang menjawab tetap "
                    "orangnya. Menulis “kemungkinan input manual” di kertas kerja itu sah; "
                    "menulis “input manual” tanpa konfirmasi itu tidak."))

langkah("Id cocok belum berarti nilainya cocok",
    blok("aksi", "Bandingkan nilai untuk id yang ada di kedua sisi.", "LAKUKAN"),
    kode('''WITH buku AS (
  SELECT o.id, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT b.id, b.nilai AS pembukuan, k.nilai AS kasir, k.nilai - b.nilai AS selisih
FROM buku b JOIN pesanan_kasir k ON k.id = b.id
WHERE b.nilai <> k.nilai
ORDER BY abs(k.nilai - b.nilai) DESC;'''),
    keluaran(H, "h7_nilai_beda"),
    blok("bahaya", "Dua baris ini <strong>tidak akan pernah ditemukan oleh <code>EXCEPT</code> "
                   "pada id</strong>. Id-nya cocok sempurna; yang berbeda hanya angkanya. "
                   "Rekonsiliasi yang berhenti di “id mana yang hilang” selalu melewatkan jenis "
                   "kesalahan ini — dan justru inilah yang paling sering terjadi di dunia nyata."))

langkah("Tie-out: menjelaskan setiap rupiah selisihnya",
    blok("aksi", "Ini bagian yang membedakan analis dari orang yang cuma menjalankan query.",
         "LAKUKAN"),
    kode('''WITH buku AS (
  SELECT o.id, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT 'Total pembukuan' AS keterangan, (SELECT sum(nilai) FROM buku) AS rupiah
UNION ALL SELECT '(-) hanya di pembukuan',
  -(SELECT COALESCE(sum(nilai),0) FROM buku b
     WHERE NOT EXISTS (SELECT 1 FROM pesanan_kasir k WHERE k.id = b.id))
UNION ALL SELECT '(+) hanya di kasir',
  (SELECT COALESCE(sum(nilai),0) FROM pesanan_kasir k
     WHERE NOT EXISTS (SELECT 1 FROM buku b WHERE b.id = k.id))
UNION ALL SELECT '(+/-) selisih nilai id sama',
  (SELECT COALESCE(sum(k.nilai - b.nilai),0)
     FROM buku b JOIN pesanan_kasir k ON k.id = b.id)
UNION ALL SELECT '= Total kasir', (SELECT sum(nilai) FROM pesanan_kasir);'''),
    keluaran(H, "h7_tieout"),
    blok("catatan", "Perhatikan bahwa tie-out ini memakai <code>NOT EXISTS</code>, bukan "
                    "<code>NOT IN</code> — walaupun di sini <code>NOT IN</code> kebetulan aman "
                    "(kedua <code>id</code>-nya kunci utama, jadi tidak mungkin "
                    "<code>NULL</code>). <strong>“Kebetulan aman” bukan alasan yang baik:</strong> "
                    "orang berikutnya yang menyalin pola ini ke kolom lain akan kena."))

langkah("Periksa penjumlahannya sendiri",
    blok("aksi", "Hitung dengan tangan. Ini bukan formalitas.", "LAKUKAN"),
    kode('35.739.000 − 222.000 + 195.000 + 25.000 = 35.737.000  ✓', salin=False),
    blok("hasil", "<p>Selisih bersihnya cuma <strong>Rp 2.000</strong> — angka yang, kalau "
                  "dilihat sendirian, terlihat seperti pembulatan yang bisa diabaikan.</p>",
         "YANG SEBENARNYA TERJADI"),
    "<p>Padahal di baliknya ada <strong>Rp 442.000</strong> pergerakan dari lima masalah "
    "berbeda yang saling menutupi. Selisih bersih hampir selalu lebih kecil daripada selisih "
    "yang sebenarnya.</p>")

langkah("Ini kertas kerja yang sudah kamu buat bertahun-tahun",
    blok("aksi", "Baca sekali, lalu berhenti sebentar.", "LAKUKAN"),
    blok("hasil", "<p>Bentuknya sama persis dengan rekonsiliasi yang kamu buat di KAP: "
                  "<strong>saldo A, daftar penyebab, saldo B, dan jumlahnya harus tutup.</strong> "
                  "Yang berubah cuma bahasanya.</p>", "YANG KAMU BAWA DARI KAP"),
    "<p>Yang bernilai bukan menemukan selisihnya — komputer bisa. Yang bernilai adalah "
    "<strong>bersikeras bahwa selisih bersih Rp 2.000 tidak boleh dilaporkan sebelum keempat "
    "penyebabnya berdiri sendiri-sendiri</strong>. Kebanyakan kandidat data analyst tidak punya "
    "refleks itu.</p>",
    blok("catatan", "Di Freelance 11 ini disebut “Pemeriksaan Angka” — satu-satunya lini jasa "
                    "yang hampir tidak punya saingan di Indonesia. Hari ini kamu baru saja "
                    "mengerjakan versi lengkapnya."))

langkah("Soal terapan: laporan yang tidak boleh bohong",
    blok("aksi", "Buat satu query yang menampilkan, <strong>per cabang</strong>: jumlah pesanan "
                 "selesai, jumlah pesanan batal, jumlah pelanggan unik yang pernah memesan di "
                 "sana, dan nilai penjualan selesai.", "KERJAKAN, ± 30 MENIT"),
    blok("bahaya", "Tiga syarat, dan ketiganya menjebak:<br>"
                   "1. Pesanan tamu (<code>pelanggan_id</code> <code>NULL</code>) "
                   "<strong>tetap dihitung</strong> di jumlah pesanan dan nilai — mereka pembeli "
                   "sungguhan.<br>"
                   "2. Tapi <strong>tidak</strong> dihitung sebagai pelanggan unik, karena kita "
                   "tidak tahu mereka siapa.<br>"
                   "3. Cabang tetap muncul walaupun ada angka yang nol."),
    "<p>Kerjakan sampai kamu punya jawaban sebelum membuka dua langkah berikutnya. Dua langkah "
    "itu berisi jawabannya.</p>")

langkah("Versi yang paling wajar ditulis — dan separuhnya salah",
    blok("aksi", "Jalankan, lalu periksa angkanya terhadap Hari 6.", "LAKUKAN"),
    kode('''SELECT o.cabang,
       count(*) FILTER (WHERE o.status='selesai')     AS pesanan_selesai,
       count(*) FILTER (WHERE o.status='batal')       AS pesanan_batal,
       count(DISTINCT o.pelanggan_id)                 AS pelanggan_unik,
       sum(CASE WHEN o.status='selesai'
                THEN i.jumlah * i.harga_saat_itu END) AS nilai_selesai
FROM pesanan o
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY o.cabang ORDER BY o.cabang;'''),
    keluaran(H, "h7_terapan_salah"),
    blok("bahaya", "Karena ada <code>JOIN</code> ke <code>item</code>, satu pesanan berisi 3 item "
                   "muncul sebagai 3 baris. Jadi <code>count(*)</code> menghitung "
                   "<strong>item</strong>, bukan pesanan: Dago tercatat 238, padahal Hari 6 sudah "
                   "membuktikan angkanya <strong>122</strong>."))

langkah("Kenapa laporan separuh benar lebih berbahaya daripada laporan salah",
    blok("aksi", "Baca sekali, pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Kolom <code>nilai_selesai</code> justru <strong>benar</strong> "
                  "(12.665.000). <code>sum</code> menjumlahkan tiap baris item satu kali, jadi ia "
                  "tidak ikut berlipat.</p>", "YANG MEMBUATNYA MAHAL"),
    "<p>Nilai rupiahnya tepat dan bisa dicocokkan dengan pembukuan, sehingga siapa pun yang "
    "memeriksa totalnya akan menyimpulkan laporan ini beres — sementara jumlah pesanannya dua "
    "kali lipat dari kenyataan, dan setiap “rata-rata per pesanan” yang dihitung darinya salah "
    "setengahnya.</p>",
    blok("catatan", "<strong>Kalau angka barismu tidak masuk akal, jangan pernah membiarkannya "
                    "lewat karena totalnya cocok.</strong> Itu pelajaran Hari 4, muncul kembali "
                    "dalam bentuk yang lebih licin."))

langkah("Versi yang benar: hitung di dua tingkat, baru gabungkan",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH nilai_per_pesanan AS (
  SELECT o.id, o.cabang, o.status, o.pelanggan_id,
         (SELECT COALESCE(sum(i.jumlah * i.harga_saat_itu), 0)
          FROM item i WHERE i.pesanan_id = o.id) AS nilai
  FROM pesanan o)
SELECT cabang,
       count(*) FILTER (WHERE status='selesai')   AS pesanan_selesai,
       count(*) FILTER (WHERE status='batal')     AS pesanan_batal,
       count(DISTINCT pelanggan_id)               AS pelanggan_unik,
       sum(nilai) FILTER (WHERE status='selesai') AS nilai_selesai
FROM nilai_per_pesanan
GROUP BY cabang ORDER BY cabang;'''),
    keluaran(H, "h7_terapan_benar"),
    "<p>122, 120, 120 — cocok dengan angka yang kamu hitung di Hari 6. <strong>Itu "
    "pemeriksaanmu.</strong></p>",
    blok("catatan", "Syarat kedua terpenuhi tanpa penyaring tambahan: "
                    "<code>count(DISTINCT pelanggan_id)</code> mengembalikan 17, bukan 20, karena "
                    "<code>count DISTINCT</code> mengabaikan <code>NULL</code>. Itu pelajaran "
                    "Hari 2, bekerja untukmu tanpa diminta."))

langkah("Pemeriksaan silang terakhir",
    blok("aksi", "Jumlahkan ketiga cabang dengan tangan.", "LAKUKAN"),
    kode('12.665.000 + 11.669.000 + 11.405.000 = 35.739.000  ✓', salin=False),
    blok("hasil", "<p>Sama dengan total pembukuan di tie-out tadi, dan sama dengan omzet yang "
                  "kamu hitung di Hari 4. <strong>Tiga jalan berbeda, satu angka.</strong></p>",
         "TUTUP"),
    "<p>Itu cara kamu tahu ketiganya benar — bukan karena kamu merasa benar, tapi karena tiga "
    "perhitungan yang tidak saling bergantung membawamu ke tempat yang sama.</p>")

HARI7 = {
  "n": "HARI 7", "tab": "7",
  "judul": "Operasi himpunan, rekonsiliasi, dan hari yang hilang",
  "waktu": "± 80 menit",
  "tujuan": "membandingkan dua sumber data dengan <code>EXCEPT</code>, <code>INTERSECT</code>, "
            "dan <code>UNION</code>, menyusun tie-out yang menjelaskan setiap rupiah selisihnya, "
            "lalu membuat kerangka tanggal dengan <code>generate_series</code>.",
  "langkah": L,
  "tutup_judul": "SQL Mahir Level 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa hari ini:</strong> <code>UNION ALL</code> sebagai bawaan — "
           "<code>UNION</code> diam-diam membuang transaksi kembar yang sah · <code>EXCEPT</code> "
           "dua arah menemukan yang hilang di tiap sisi · id cocok belum berarti nilainya cocok · "
           "selisih bersih selalu lebih kecil daripada masalah yang sebenarnya · dan syarat "
           "tambahan di <code>LEFT JOIN</code> harus di <code>ON</code>, bukan "
           "<code>WHERE</code>.</p>"

           "<p style=\"margin-top:8px\"><strong>Soal ingatan 7 dari 8.</strong> "
           "<em>Kenapa <code>UNION ALL</code> lebih aman daripada <code>UNION</code> untuk "
           "menumpuk data penjualan dua bulan?</em></p>"
           "<details><summary>Kunci</summary><p><code>UNION</code> membuang baris yang identik. "
           "Dua transaksi berbeda yang kebetulan sama persis (produk, jumlah, harga, tanggal "
           "sama) akan dianggap satu, dan uangnya hilang dari total tanpa jejak.</p></details>"

           "<p style=\"margin-top:8px\"><strong>Soal ingatan 8 dari 8.</strong> "
           "<em>Dua sistem dibandingkan. Semua id cocok. Apakah rekonsiliasinya selesai?</em></p>"
           "<details><summary>Kunci</summary><p>Belum. Id yang cocok masih bisa berbeda "
           "nilainya — dan itu jenis selisih yang paling sering terjadi. Bandingkan nilainya "
           "secara terpisah.</p></details>"

           "<p style=\"margin-top:14px\"><strong>Tujuh hari ini tidak menambah satu pun kata "
           "kunci yang “keren”.</strong> Yang ditambahkannya adalah hal-hal yang membuat query "
           "diam-diam salah — dan kemampuan mencurigainya sebelum ada yang menegur.</p>"
           "<p style=\"margin-top:8px\">Yang paling berharga dari Level 1: kebiasaan menghitung "
           "jumlah baris dan menjelaskan asalnya sebelum melihat isi hasilnya. Hampir semua "
           "kesalahan SQL yang mahal — JOIN yang melipatgandakan, <code>NOT IN</code> yang "
           "mengosongkan, <code>UNION</code> yang menelan transaksi, <code>LEFT JOIN</code> yang "
           "diam-diam jadi <code>INNER</code> — ketahuan dari jumlah baris yang tidak bisa "
           "dijelaskan.</p>"
           "<p style=\"margin-top:8px\"><strong>Kalau ada satu dari delapan soal ingatan yang "
           "belum bisa kamu jawab dengan suara</strong>, ulangi harinya sebelum lanjut. Level 2 "
           "berdiri di atas semua ini.</p>"
           "<p style=\"margin-top:8px\"><strong>Berikutnya di Level 2:</strong> window function "
           "sampai tuntas — <code>ROWS BETWEEN</code> dan bedanya dengan <code>RANGE</code>, "
           "<code>LEAD</code>, <code>NTILE</code>, <code>FIRST_VALUE</code>, persentil, dan "
           "recursive CTE untuk menelusuri hierarki sampai ke dasarnya. Modul M6 baru menyentuh "
           "permukaannya.</p>",
}
