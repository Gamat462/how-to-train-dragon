# -*- coding: utf-8 -*-
"""Hari 7 — operasi himpunan, rekonsiliasi dua sistem, dan satu soal terapan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Menyamping dengan JOIN, ke bawah dengan himpunan",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
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
    "<p>Bawaan orang adalah menulis <code>UNION</code>, dan itu hampir selalu keliru.</p>")

langkah("Buktikan apa yang ditelan UNION",
    blok("aksi", "Sel baru. Bayangkan dua transaksi sah yang kebetulan identik.", "LAKUKAN"),
    kode('''q("""SELECT 'A' AS x, 10000 AS n
     UNION     SELECT 'A', 10000
     UNION     SELECT 'B', 20000""")'''),
    blok("hasil", "<pre><code>   x      n\n0  A  10000\n1  B  20000</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "Tiga baris masuk, <strong>dua baris keluar</strong>. Kalau kamu menumpuk "
                   "penjualan Januari dan Februari dengan <code>UNION</code>, dua transaksi yang "
                   "kebetulan sama persis (produk sama, harga sama, jumlah sama) dianggap satu. "
                   "<strong>Uangnya hilang dari laporan tanpa jejak.</strong>"),
    "<p>Ganti satu kata jadi <code>UNION ALL</code> dan jalankan lagi: tiga baris, "
    "<code>A</code> muncul dua kali. Itu yang benar.</p>")

langkah("Layar merah yang menyelamatkanmu",
    blok("aksi", "Sel baru. Tumpuk dua hasil yang jumlah kolomnya tidak sama.", "LAKUKAN"),
    kode('q("SELECT id, nama FROM produk UNION ALL SELECT id FROM pelanggan")'),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': SELECTs to the left "
                  "and right of UNION ALL do not have the same number of result "
                  "columns</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
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
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""
WITH buku AS (
  SELECT o.id, SUM(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT 'selesai di pembukuan' AS keterangan, COUNT(*) AS jumlah FROM buku
UNION ALL SELECT 'baris di ekspor kasir', COUNT(*) FROM pesanan_kasir
UNION ALL SELECT 'id cocok',
  (SELECT COUNT(*) FROM buku b JOIN pesanan_kasir k ON k.id = b.id)
UNION ALL SELECT 'hanya di pembukuan',
  (SELECT COUNT(*) FROM (SELECT id FROM buku EXCEPT SELECT id FROM pesanan_kasir))
UNION ALL SELECT 'hanya di kasir',
  (SELECT COUNT(*) FROM (SELECT id FROM pesanan_kasir EXCEPT SELECT id FROM buku))
""")'''),
    blok("hasil", "<pre><code>              keterangan  jumlah\n0   selesai di pembukuan     362\n"
                  "1  baris di ekspor kasir     361\n2               id cocok     359\n"
                  "3     hanya di pembukuan       3\n4         hanya di kasir       2</code></pre>",
         "HARUS MUNCUL"),
    "<p>Lima angka, satu query. Sebelum kamu membacanya, perhatikan bahwa keempat angka terakhir "
    "seharusnya bisa kamu jumlahkan sendiri jadi dua angka pertama.</p>")

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
    blok("aksi", "Sel baru. <code>INTERSECT</code>, supaya kamu tidak percaya pada satu query "
                 "saja.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS id_di_dua_sisi FROM (
       SELECT id FROM pesanan WHERE status='selesai'
       INTERSECT SELECT id FROM pesanan_kasir)""")'''),
    blok("hasil", "<pre><code>   id_di_dua_sisi\n0             359</code></pre>", "HARUS MUNCUL"),
    "<p>359 lagi, dan kamu sampai ke sana lewat jalan yang sama sekali berbeda. Itu cara kamu "
    "tahu angkanya bukan kebetulan.</p>")

langkah("Tunjukkan barisnya, bukan cuma jumlahnya",
    blok("aksi", "Sel baru. <code>EXCEPT</code> dua arah.", "LAKUKAN"),
    kode('''q("""
SELECT 'hanya pembukuan' AS sisi, id FROM (
  SELECT id FROM pesanan WHERE status='selesai'
  EXCEPT SELECT id FROM pesanan_kasir)
UNION ALL
SELECT 'hanya kasir', id FROM (
  SELECT id FROM pesanan_kasir
  EXCEPT SELECT id FROM pesanan WHERE status='selesai')
""")'''),
    blok("hasil", "<pre><code>              sisi    id\n0  hanya pembukuan     7\n"
                  "1  hanya pembukuan    88\n2  hanya pembukuan   251\n"
                  "3      hanya kasir  9001\n4      hanya kasir  9002</code></pre>",
         "HARUS MUNCUL"),
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
    blok("aksi", "Sel baru. Bandingkan nilai untuk id yang ada di kedua sisi.", "LAKUKAN"),
    kode('''q("""
WITH buku AS (
  SELECT o.id, SUM(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT b.id, b.nilai AS pembukuan, k.nilai AS kasir, k.nilai - b.nilai AS selisih
FROM buku b JOIN pesanan_kasir k ON k.id = b.id
WHERE b.nilai <> k.nilai
ORDER BY ABS(k.nilai - b.nilai) DESC
""")'''),
    blok("hasil", "<pre><code>    id  pembukuan   kasir  selisih\n"
                  "0   12      54000  104000    50000\n"
                  "1  199      80000   55000   -25000</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "Dua baris ini <strong>tidak akan pernah ditemukan oleh <code>EXCEPT</code> "
                   "pada id</strong>. Id-nya cocok sempurna; yang berbeda hanya angkanya. "
                   "Rekonsiliasi yang berhenti di “id mana yang hilang” selalu melewatkan jenis "
                   "kesalahan ini — dan justru inilah yang paling sering terjadi di dunia nyata."))

langkah("Tie-out: menjelaskan setiap rupiah selisihnya",
    blok("aksi", "Sel baru. Ini bagian yang membedakan analis dari orang yang cuma menjalankan "
                 "query.", "LAKUKAN"),
    kode('''q("""
WITH buku AS (
  SELECT o.id, SUM(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT 'Total pembukuan' AS keterangan, (SELECT SUM(nilai) FROM buku) AS rupiah
UNION ALL SELECT '(-) hanya di pembukuan',
  -(SELECT COALESCE(SUM(nilai),0) FROM buku WHERE id NOT IN (SELECT id FROM pesanan_kasir))
UNION ALL SELECT '(+) hanya di kasir',
  (SELECT COALESCE(SUM(nilai),0) FROM pesanan_kasir WHERE id NOT IN (SELECT id FROM buku))
UNION ALL SELECT '(+/-) selisih nilai id sama',
  (SELECT COALESCE(SUM(k.nilai-b.nilai),0) FROM buku b JOIN pesanan_kasir k ON k.id=b.id)
UNION ALL SELECT '= Total kasir', (SELECT SUM(nilai) FROM pesanan_kasir)
""")'''),
    blok("hasil", "<pre><code>                    keterangan    rupiah\n"
                  "0              Total pembukuan  35739000\n"
                  "1       (-) hanya di pembukuan   -222000\n"
                  "2           (+) hanya di kasir    195000\n"
                  "3  (+/-) selisih nilai id sama     25000\n"
                  "4                = Total kasir  35737000</code></pre>", "HARUS MUNCUL"),
    "<details><summary>Query ini memakai <code>NOT IN</code> dua kali — kenapa di sini aman?</summary>"
    "<p>Karena <code>pesanan_kasir.id</code> dan <code>buku.id</code> keduanya kunci utama, jadi "
    "tidak mungkin <code>NULL</code>. Tapi <strong>“kebetulan aman” bukan alasan yang baik</strong>; "
    "orang berikutnya yang menyalin pola ini ke kolom lain akan kena. Versi yang tidak bergantung "
    "pada kebetulan:</p>"
    "<div class=\"kode\"><pre><code>-(SELECT COALESCE(SUM(nilai),0) FROM buku b\n"
    "   WHERE NOT EXISTS (SELECT 1 FROM pesanan_kasir k WHERE k.id = b.id))\n\n"
    " (SELECT COALESCE(SUM(nilai),0) FROM pesanan_kasir k\n"
    "   WHERE NOT EXISTS (SELECT 1 FROM buku b WHERE b.id = k.id))</code></pre></div>"
    "<pre><code>   hanya_pembukuan  hanya_kasir\n0          -222000       195000</code></pre>"
    "<p>Hasilnya sama persis. Bedanya, versi ini tetap benar kalau suatu hari kolomnya boleh "
    "<code>NULL</code>.</p></details>")

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
    blok("catatan", "Di Freelance 11 ini disebut “Pemeriksaan Angka” — satu-satunya "
                    "lini jasa yang hampir tidak punya saingan di Indonesia. Hari ini kamu baru "
                    "saja mengerjakan versi lengkapnya."))

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
    blok("aksi", "Sel baru. Jalankan, lalu periksa angkanya terhadap Hari 6.", "LAKUKAN"),
    kode('''q("""
SELECT o.cabang,
       COUNT(*) FILTER (WHERE o.status='selesai')     AS pesanan_selesai,
       COUNT(*) FILTER (WHERE o.status='batal')       AS pesanan_batal,
       COUNT(DISTINCT o.pelanggan_id)                 AS pelanggan_unik,
       SUM(CASE WHEN o.status='selesai'
                THEN i.jumlah * i.harga_saat_itu END) AS nilai_selesai
FROM pesanan o
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY o.cabang ORDER BY o.cabang
""")'''),
    blok("hasil", "<pre><code>    cabang  pesanan_selesai  pesanan_batal  pelanggan_unik  nilai_selesai\n"
                  "0     Dago              238             15              17       12665000\n"
                  "1   Kemang              242             19              17       11669000\n"
                  "2  Seturan              239             35              17       11405000</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "Karena ada <code>JOIN</code> ke <code>item</code>, satu pesanan berisi 3 item "
                   "muncul sebagai 3 baris. Jadi <code>COUNT(*)</code> menghitung "
                   "<strong>item</strong>, bukan pesanan: Dago tercatat 238, padahal Hari 6 sudah "
                   "membuktikan angkanya <strong>122</strong>."))

langkah("Kenapa laporan separuh benar lebih berbahaya daripada laporan salah",
    blok("aksi", "Baca sekali, pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Kolom <code>nilai_selesai</code> justru <strong>benar</strong> "
                  "(12.665.000). <code>SUM</code> menjumlahkan tiap baris item satu kali, jadi ia "
                  "tidak ikut berlipat.</p>", "YANG MEMBUATNYA MAHAL"),
    "<p>Nilai rupiahnya tepat dan bisa dicocokkan dengan pembukuan, sehingga siapa pun yang "
    "memeriksa totalnya akan menyimpulkan laporan ini beres — sementara jumlah pesanannya dua "
    "kali lipat dari kenyataan, dan setiap “rata-rata per pesanan” yang dihitung darinya salah "
    "setengahnya.</p>",
    blok("catatan", "<strong>Kalau angka barismu tidak masuk akal, jangan pernah membiarkannya "
                    "lewat karena totalnya cocok.</strong> Itu pelajaran Hari 4, muncul kembali "
                    "dalam bentuk yang lebih licin."))

langkah("Versi yang benar: hitung di dua tingkat, baru gabungkan",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""
WITH nilai_per_pesanan AS (
  SELECT o.id, o.cabang, o.status, o.pelanggan_id,
         (SELECT COALESCE(SUM(i.jumlah * i.harga_saat_itu), 0)
          FROM item i WHERE i.pesanan_id = o.id) AS nilai
  FROM pesanan o)
SELECT cabang,
       COUNT(*) FILTER (WHERE status='selesai')   AS pesanan_selesai,
       COUNT(*) FILTER (WHERE status='batal')     AS pesanan_batal,
       COUNT(DISTINCT pelanggan_id)               AS pelanggan_unik,
       SUM(nilai) FILTER (WHERE status='selesai') AS nilai_selesai
FROM nilai_per_pesanan
GROUP BY cabang ORDER BY cabang
""")'''),
    blok("hasil", "<pre><code>    cabang  pesanan_selesai  pesanan_batal  pelanggan_unik  nilai_selesai\n"
                  "0     Dago              122              8              17       12665000\n"
                  "1   Kemang              120             12              17       11669000\n"
                  "2  Seturan              120             18              17       11405000</code></pre>",
         "HARUS MUNCUL"),
    "<p>122, 120, 120 — cocok dengan angka yang kamu hitung di Hari 6. <strong>Itu "
    "pemeriksaanmu.</strong></p>",
    blok("catatan", "Syarat kedua terpenuhi tanpa penyaring tambahan: "
                    "<code>COUNT(DISTINCT pelanggan_id)</code> mengembalikan 17, bukan 20, karena "
                    "<code>COUNT DISTINCT</code> mengabaikan <code>NULL</code>. Itu pelajaran "
                    "Hari 2, bekerja untukmu tanpa diminta."))

langkah("Pemeriksaan silang terakhir",
    blok("aksi", "Jumlahkan ketiga cabang dengan tangan.", "LAKUKAN"),
    kode('12.665.000 + 11.669.000 + 11.405.000 = 35.739.000  ✓', salin=False),
    blok("hasil", "<p>Sama dengan total pembukuan di langkah 12, dan sama dengan omzet yang kamu "
                  "hitung di Hari 4. <strong>Tiga jalan berbeda, satu angka.</strong></p>",
         "TUTUP"),
    "<p>Itu cara kamu tahu ketiganya benar — bukan karena kamu merasa benar, tapi karena tiga "
    "perhitungan yang tidak saling bergantung membawamu ke tempat yang sama.</p>")

HARI7 = {
  "n": "HARI 7", "tab": "7",
  "judul": "Operasi himpunan: merekonsiliasi dua sistem",
  "waktu": "± 75 menit",
  "tujuan": "membandingkan dua sumber data dengan <code>EXCEPT</code>, <code>INTERSECT</code>, "
            "dan <code>UNION</code>, lalu menyusun tie-out yang menjelaskan setiap rupiah "
            "selisihnya.",
  "langkah": L,
  "tutup_judul": "SQL Mahir Level 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa hari ini:</strong> <code>UNION ALL</code> sebagai bawaan — "
           "<code>UNION</code> diam-diam membuang transaksi kembar yang sah · <code>EXCEPT</code> "
           "dua arah menemukan yang hilang di tiap sisi · id cocok belum berarti nilainya cocok · "
           "dan selisih bersih selalu lebih kecil daripada masalah yang sebenarnya.</p>"

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
           "mengosongkan, <code>UNION</code> yang menelan transaksi — ketahuan dari jumlah baris "
           "yang tidak bisa dijelaskan.</p>"
           "<p style=\"margin-top:8px\"><strong>Kalau ada satu dari delapan soal ingatan yang "
           "belum bisa kamu jawab dengan suara</strong>, ulangi harinya sebelum lanjut. Level 2 "
           "berdiri di atas semua ini.</p>"
           "<p style=\"margin-top:8px\"><strong>Berikutnya di Level 2:</strong> window function "
           "sampai tuntas — <code>ROWS BETWEEN</code> dan bedanya dengan <code>RANGE</code>, "
           "<code>LEAD</code>, <code>NTILE</code>, <code>FIRST_VALUE</code>, persentil, dan "
           "recursive CTE untuk menelusuri hierarki sampai ke dasarnya. Modul M6 baru menyentuh "
           "permukaannya.</p>",
}
