# -*- coding: utf-8 -*-
"""Hari 7 — ujian akhir: satu brief klien."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Baca briefnya. Itu saja isinya.",
    blok("aksi", "Sediakan dua jam. Kerjakan berurutan, jangan lompat ke kuncinya.", "LAKUKAN"),
    kode("""Dari:     Pemilik Kopi Senja
Perihal:  Cabang mana yang sebaiknya kami tutup?

Halo, kami sedang mempertimbangkan menutup satu cabang tahun ini.
Tolong lihat datanya dan beri tahu cabang mana yang paling lemah.
Datanya ada di senja.db. Terima kasih.""", salin=False),
    "<p>Satu kalimat, dan keputusan yang menyangkut pekerjaan orang. <strong>Ini bentuk "
    "take-home test yang sesungguhnya diberikan</strong>, dan bentuk permintaan klien yang "
    "sesungguhnya datang.</p>")

langkah("Sebelum satu pun SELECT: tulis lima hal di kertas",
    blok("aksi", "Jangan sentuh keyboard sampai kertasmu terisi.", "LAKUKAN"),
    kode("""TIGA pemeriksaan yang akan kujalankan lebih dulu:
1. ___
2. ___
3. ___

DUA pertanyaan yang akan kuajukan ke pemiliknya:
1. ___
2. ___""", salin=False),
    blok("bahaya", "<strong>Kandidat yang langsung mengetik</strong> akan mendapat jawaban yang "
                   "benar secara SQL dan salah secara pekerjaan. Kamu punya keunggulan di sini "
                   "justru karena kamu terbiasa merencanakan prosedur sebelum menguji."))

langkah("Bandingkan dengan daftarku",
    blok("aksi", "Baru sekarang boleh dibuka.", "LAKUKAN"),
    "<details><summary>Buka daftarku</summary>"
    "<p><strong>Tiga pemeriksaan sebelum menghitung apa pun:</strong></p>"
    "<p>1. Jalankan <code>uji_mutu.py</code> dari Level 4. Kalau data kasir dan sistem tidak "
    "cocok, angka omzet per cabang belum bisa dipercaya.</p>"
    "<p>2. Periksa kelengkapan kolom yang akan kupakai — terutama <code>harga_beli</code>, karena "
    "“lemah” hampir pasti soal laba, bukan cuma omzet.</p>"
    "<p>3. Periksa rentang tanggalnya. Kalau satu cabang baru buka bulan April, membandingkan "
    "totalnya dengan cabang yang buka sejak Januari adalah membandingkan dua hal berbeda.</p>"
    "<p><strong>Dua pertanyaan ke pemiliknya:</strong></p>"
    "<p>1. “Lemah itu maksudnya omzet paling kecil, laba paling kecil, atau tren paling turun? "
    "Ketiganya bisa menunjuk cabang yang berbeda.”</p>"
    "<p>2. “Apa ada biaya per cabang — sewa, gaji, listrik — yang tidak ada di basis data ini?”</p>"
    "</details>",
    blok("catatan", "<strong>Pertanyaan kedua yang paling penting, dan paling sering dilewati.</strong> "
                    "Data yang kamu punya <em>tidak bisa</em> menjawab pertanyaan yang diajukan. "
                    "Mengatakannya di awal adalah pekerjaan; menyembunyikannya dan tetap memberi "
                    "jawaban adalah masalah."))

langkah("Jalankan dulu dua pemeriksaan yang barusan kamu tulis",
    blok("aksi", "Dua baris, dua puluh detik. Sebelum menghitung apa pun.", "LAKUKAN"),
    kode('print(con.execute("SELECT MIN(tanggal), MAX(tanggal) FROM pesanan").fetchone())\n'
         'print(con.execute("SELECT COUNT(*) FROM produk WHERE harga_beli IS NULL").fetchone()[0])'),
    blok("hasil", "<pre><code>('2024-01-01', '2024-06-29')\n2</code></pre>", "HARUS MUNCUL"),
    "<p>Rentangnya sama untuk semua cabang — aman, tidak ada cabang yang baru buka. "
    "Tapi <strong>dua produk tidak punya <code>harga_beli</code></strong>, dan kamu baru saja "
    "menemukannya <em>sebelum</em> menghitung apa pun.</p>",
    blok("catatan", "<strong>Kalau kamu melewatkan langkah ini</strong>, kamu tetap akan "
                    "menemukannya — tiga langkah lagi, sesudah menulis laporan yang salah. "
                    "Dua puluh detik di depan menghemat setengah jam di belakang."))

langkah("U1 — laba kotor per cabang. Kerjakan dulu.",
    blok("aksi", "Dua puluh menit.", "LAKUKAN"),
    kode("U1  Laba kotor tiap cabang: omzet, HPP, dan selisihnya.", salin=False))

langkah("Kunci U1 — rapi, meyakinkan, dan salah",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""SELECT p.cabang,
       SUM(i.jumlah * i.harga_saat_itu) AS omzet,
       SUM(i.jumlah * pr.harga_beli)    AS hpp,
       SUM(i.jumlah * (i.harga_saat_itu - pr.harga_beli)) AS laba_kotor
FROM pesanan p
JOIN item   i  ON i.pesanan_id = p.id
JOIN produk pr ON pr.id = i.produk_id
WHERE p.status = 'selesai'
GROUP BY p.cabang ORDER BY laba_kotor DESC"""),
    blok("hasil", "<pre><code>    cabang     omzet      hpp  laba_kotor\n"
                  "0   Kemang  11669000  2701000     5148000\n"
                  "1     Dago  12665000  2719000     5062000\n"
                  "2  Seturan  11405000  2455000     4724000</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau angkamu cocok, jangan lega dulu.</strong> Cocok dengan punyaku "
                    "cuma berarti kamu tidak salah ketik — itu tidak sama dengan benar. "
                    "Dua langkah lagi kamu akan tahu bedanya."),
    "<p>Siap dikirim. <strong>Dan salah.</strong> Sebelum lanjut: hitung margin Dago di "
    "kalkulator.</p>")

langkah("Aritmetika kepala yang menyelamatkanmu",
    blok("aksi", "Satu pembagian.", "LAKUKAN"),
    kode("(12665000 - 2719000) / 12665000 * 100", salin=False),
    blok("hasil", "<pre><code>78,5 %</code></pre>", "HITUNGANMU"),
    blok("bahaya", "<strong>Margin kotor 78% untuk kedai kopi tidak masuk akal.</strong> "
                   "Angka yang terlalu bagus adalah gejala, bukan kabar baik. Aritmetika ini "
                   "gratis, butuh sepuluh detik, dan ia yang menyelamatkanmu."),
    "<p>Kamu sudah melakukan ini bertahun-tahun waktu membaca laporan keuangan klien. "
    "<strong>Lakukan yang sama pada keluaran query-mu sendiri.</strong></p>")

langkah("Lupa satu baris ON, dan omzetmu jadi 399 kali lipat",
    blok("aksi", "Hapus <code>ON i.pesanan_id = p.id</code> dari U1 — dengan sengaja. "
                 "Jalankan dua-duanya.", "LAKUKAN"),
    kode('''benar = "FROM pesanan p JOIN item i ON i.pesanan_id=p.id WHERE p.status='selesai'"
salah = "FROM pesanan p JOIN item i                       WHERE p.status='selesai'"
for nama, f in [("benar", benar), ("lupa ON", salah)]:
    n = con.execute(f"SELECT SUM(i.jumlah*i.harga_saat_itu) {f}").fetchone()[0]
    print(f"  {nama:8} {n:>16,}")'''),
    blok("bahaya", "<pre><code>  benar          35,739,000\n  lupa ON    14,265,334,000</code></pre>",
         "HARUS MUNCUL — DAN TIDAK ADA TULISAN MERAH SAMA SEKALI"),
    blok("bahaya", "<strong>399 kali lipat, dan SQL menerimanya tanpa berkedip.</strong> "
                   "<code>JOIN</code> tanpa <code>ON</code> memasangkan <em>tiap</em> pesanan "
                   "dengan <em>tiap</em> item: 400 × 788 = 315.200 baris."),
    "<p>Di angka sebesar ini kamu akan menyadarinya. <strong>Yang berbahaya adalah "
    "<code>ON</code> yang salah kolom</strong> — hasilnya cuma beberapa kali lipat, masih "
    "terlihat wajar, dan tidak ada yang curiga.</p>",
    blok("aksi", "Biasakan menghitungnya. Cuma satu baris:", "LAKUKAN"),
    kode('print(con.execute("SELECT COUNT(*) FROM pesanan p JOIN item i ON i.pesanan_id=p.id").fetchone()[0])'),
    blok("hasil", "<pre><code>788</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>788 = jumlah baris tabel <code>item</code>.</strong> Itu yang kamu "
                    "harapkan dari join induk-ke-rinci: satu baris hasil per baris rinci. "
                    "Kalau angkamu lebih besar, join-mu menggandakan sesuatu — dan kamu tahu itu "
                    "sebelum menghitung omzet apa pun."))

langkah("U2 — cari penyebabnya",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""SELECT pr.nama, COUNT(*) AS baris_item,
       SUM(i.jumlah * i.harga_saat_itu) AS omzet_terdampak
FROM item i
JOIN produk  pr ON pr.id = i.produk_id
JOIN pesanan p  ON p.id  = i.pesanan_id
WHERE pr.harga_beli IS NULL AND p.status = 'selesai'
GROUP BY pr.nama"""),
    blok("hasil", "<pre><code>           nama  baris_item  omzet_terdampak\n"
                  "0    Cheesecake          90          6300000\n"
                  "1  Matcha Latte         105          6630000</code></pre>", "HARUS MUNCUL"),
    "<p>Ketemu. Dua produk tanpa <code>harga_beli</code>, menyumbang "
    "<strong>12.930.000</strong> — sekitar <strong>36%</strong> dari total omzet 35.739.000.</p>")

langkah("Dan inilah bagian terpenting di seluruh ujian ini",
    blok("aksi", "Baca pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Di U1, <code>SUM(i.jumlah * pr.harga_beli)</code> <strong>tidak error dan "
                  "tidak memberi peringatan apa pun.</strong> SQL <em>melewati</em> baris yang "
                  "<code>NULL</code> saat menjumlahkan.</p>", "KENAPA ANGKANYA RAPI"),
    "<p>Jadi omzetnya lengkap 100%, HPP-nya cuma dari 64% barang, dan selisihnya kamu sebut "
    "“laba kotor”. <strong>Angka itu bukan laba kotor apa pun</strong> — ia campuran dua hal "
    "yang tidak boleh dikurangkan.</p>",
    blok("bahaya", "<strong>Ini sudah tiga kali muncul di jalur ini.</strong> "
                   "<code>.sum()</code> pada tabel kosong memberi 0. <code>NOT IN</code> dengan "
                   "<code>NULL</code> memberi nol baris. <code>SUM</code> atas kolom setengah "
                   "kosong memberi angka yang rapi. <em>Tidak ada satu pun yang gagal dengan "
                   "berisik.</em>"))

langkah("U3 — cara melaporkannya dengan jujur",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""SUM(CASE WHEN pr.harga_beli IS NOT NULL
         THEN i.jumlah * i.harga_saat_itu ELSE 0 END) AS omzet_ada_hpp"""),
    "<p>Itu potongan kuncinya: <strong>jumlahkan omzet hanya dari baris yang HPP-nya ada</strong>. "
    "Sekarang pasang dia ke query lengkapnya.</p>",
    kode("""SELECT p.cabang,
  SUM(i.jumlah * i.harga_saat_itu) AS omzet,
  SUM(CASE WHEN pr.harga_beli IS NOT NULL
           THEN i.jumlah * i.harga_saat_itu ELSE 0 END) AS omzet_ada_hpp,
  ROUND(100.0 * SUM(CASE WHEN pr.harga_beli IS NOT NULL
                         THEN i.jumlah * i.harga_saat_itu ELSE 0 END)
        / SUM(i.jumlah * i.harga_saat_itu), 1) AS cakupan_persen,
  SUM(i.jumlah * (i.harga_saat_itu - pr.harga_beli)) AS laba_kotor_sebagian
FROM pesanan p
JOIN item   i  ON i.pesanan_id = p.id
JOIN produk pr ON pr.id = i.produk_id
WHERE p.status = 'selesai' GROUP BY p.cabang ORDER BY omzet DESC"""),
    blok("hasil", "<pre><code>    cabang     omzet  omzet_ada_hpp  cakupan_persen  laba_kotor_sebagian\n"
                  "0     Dago  12665000        7781000            61.4              5062000\n"
                  "1   Kemang  11669000        7849000            67.3              5148000\n"
                  "2  Seturan  11405000        7179000            62.9              4724000</code></pre>",
         "HARUS MUNCUL"),
    "<p>Kolom <code>cakupan_persen</code> mengubah “laba kotor Dago 5.062.000” jadi "
    "<strong>“laba kotor dari 61,4% omzet Dago”</strong>. Yang kedua bisa kamu "
    "pertanggungjawabkan; yang pertama tidak.</p>",
    blok("catatan", "<strong>Cakupannya berbeda-beda per cabang</strong> — 61,4% sampai 67,3%. "
                    "Artinya membandingkan ketiga angka laba kotor itu satu sama lain juga tidak "
                    "sah. Nama kolomnya <code>laba_kotor_sebagian</code>, dan penamaan itu bukan "
                    "kesopanan — itu bagian dari kebenarannya."))

langkah("U4 dan U5 — dua sudut yang tidak butuh harga_beli",
    blok("aksi", "Jalankan U4 dulu: berapa persen omzet datang dari 3 pelanggan terbesar.", "LAKUKAN"),
    kode("""WITH per_pel AS (
  SELECT p.cabang, p.pelanggan_id, SUM(i.jumlah*i.harga_saat_itu) AS nilai
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status='selesai' AND p.pelanggan_id IS NOT NULL
  GROUP BY p.cabang, p.pelanggan_id),
beri_peringkat AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY cabang ORDER BY nilai DESC) AS urutan,
            SUM(nilai)   OVER (PARTITION BY cabang) AS total_cabang
  FROM per_pel)
SELECT cabang, SUM(nilai) AS tiga_teratas, MAX(total_cabang) AS total,
       ROUND(100.0*SUM(nilai)/MAX(total_cabang),1) AS persen
FROM beri_peringkat WHERE urutan<=3 GROUP BY cabang ORDER BY persen DESC"""),
    blok("hasil", "<pre><code>    cabang  tiga_teratas     total  persen\n"
                  "0   Kemang       3759000  11534000    32.6\n"
                  "1     Dago       3652000  12174000    30.0\n"
                  "2  Seturan       3109000  11101000    28.0</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Perhatikan <code>total</code> Kemang di sini: 11.534.000</strong>, "
                    "lebih kecil dari omzetnya di U3 (11.669.000). Selisihnya pesanan yang "
                    "<code>pelanggan_id</code>-nya kosong, yang sengaja kamu buang. "
                    "Selisih yang kamu <em>ketahui sebabnya</em> bukan masalah; selisih yang "
                    "kamu tidak sadari ada, itu masalah."))

langkah("U5 — dan sekarang gambarnya berbalik",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""WITH bulanan AS (
  SELECT p.cabang, substr(p.tanggal,1,7) AS bulan,
         SUM(i.jumlah*i.harga_saat_itu) AS omzet
  FROM pesanan p JOIN item i ON i.pesanan_id=p.id
  WHERE p.status='selesai' GROUP BY p.cabang, bulan)
SELECT cabang,
  SUM(CASE WHEN bulan<='2024-03' THEN omzet ELSE 0 END) AS kuartal_1,
  SUM(CASE WHEN bulan>='2024-04' THEN omzet ELSE 0 END) AS kuartal_2,
  SUM(CASE WHEN bulan>='2024-04' THEN omzet ELSE 0 END)
  - SUM(CASE WHEN bulan<='2024-03' THEN omzet ELSE 0 END) AS selisih
FROM bulanan GROUP BY cabang ORDER BY selisih"""),
    blok("hasil", "<pre><code>    cabang  kuartal_1  kuartal_2  selisih\n"
                  "0     Dago    6851000    5814000 -1037000\n"
                  "1  Seturan    5745000    5660000   -85000\n"
                  "2   Kemang    5297000    6372000  1075000</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Dago — yang omzetnya paling besar — satu-satunya yang turun tajam</strong> "
    "(−15%). Kemang — yang paling kecil — satu-satunya yang naik. Omzet menunjuk Kemang; "
    "tren menunjuk Dago.</p>")

langkah("Tulis balasannya — enam kalimat, bukan enam tabel",
    blok("aksi", "Maksimal 200 kata. Tulis sendiri dulu, baru buka versiku.", "LAKUKAN"),
    "<details><summary>Bandingkan dengan versiku</summary>"
    + kode("""Halo Pak/Bu,

Sebelum menjawab, satu hal yang perlu saya sampaikan: data harga beli
untuk Cheesecake dan Matcha Latte kosong. Kedua produk itu menyumbang
Rp 12.930.000 atau 36% dari omzet, jadi laba kotor per cabang BELUM
bisa dihitung dengan benar. Kalau data itu bisa dilengkapi, saya
kirimkan angka labanya dalam sehari.

Dari yang bisa dihitung sekarang:
- Dago beromzet paling besar (Rp 12,7 juta) TAPI paling cepat turun:
  kuartal 2 anjlok Rp 1,04 juta atau 15% dibanding kuartal 1.
- Kemang beromzet paling kecil (Rp 11,7 juta) tapi satu-satunya yang
  NAIK, +Rp 1,08 juta. Risikonya: 32,6% omzetnya dari 3 pelanggan saja.
- Seturan datar di kedua sisi.

Saran saya: jangan tutup apa pun berdasarkan omzet, karena omzet
menunjuk Kemang dan tren menunjuk Dago. Yang perlu diketahui dulu
adalah biaya sewa dan gaji per cabang - keduanya tidak ada di data ini,
dan keputusan tutup-buka ditentukan oleh itu, bukan oleh omzet.""", salin=False)
    + "</details>",
    blok("hasil", "<p><strong>Yang TIDAK ada di balasan itu: nama cabang yang harus ditutup.</strong> "
                  "Karena datanya memang tidak bisa menjawab itu.</p>", "PERHATIKAN"),
    "<p>Dan yang <strong>ADA</strong>: satu masalah data yang mereka belum tahu, dua temuan yang "
    "bertentangan dan dijelaskan pertentangannya, satu permintaan yang jelas, dan satu tenggat. "
    "Itu balasan yang membuat orang menyewamu lagi.</p>")

langkah("Nilai dirimu sendiri, dengan aturan yang keras",
    blok("aksi", "Centang <strong>hanya</strong> kalau kamu bisa mengerjakannya sekarang, di "
                 "basis data kosong, tanpa membuka halaman ini.", "LAKUKAN"),
    tabel(["Level", "Kalau ini bisa kamu lakukan tanpa contekan…"],
          [["L1", "Menyambung tiga tabel dan tahu kenapa <code>LEFT</code> bukan "
            "<code>INNER</code> · menjelaskan kenapa <code>NOT IN</code> berbahaya · menghitung "
            "<code>NULL</code> di sebuah kolom"],
           ["L2", "<code>ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)</code> dari nol · "
            "bedanya dengan <code>RANK</code> · total berjalan dengan <code>ROWS</code> eksplisit "
            "· <code>LAG</code> untuk pertumbuhan bulanan"],
           ["L3", "Deduplikasi dengan <code>ROW_NUMBER</code> · top-N per kelompok · "
            "<em>gaps-and-islands</em> · median tanpa <code>MEDIAN</code> · pivot dengan "
            "<code>SUM(CASE WHEN …)</code> — dan untuk tiap pola, menyebut keputusan bisnis "
            "yang tersembunyi di dalamnya"],
           ["L4", "Membaca <code>EXPLAIN QUERY PLAN</code> dan membedakan <code>SCAN</code> dari "
            "<code>SEARCH</code> · menyebut tiga cara membunuh index tanpa sadar · menjelaskan "
            "aturan kolom terkiri · memakai <code>BEGIN</code>/<code>ROLLBACK</code> dengan benar "
            "· menulis berkas uji mutu berambang"],
           ["L5", "Menyebut asumsi sebelum mengetik · mencocokkan total dengan angka yang "
            "diketahui · menolak menjawab yang datanya tidak mendukung"]]),
    blok("catatan", "<strong>“Pernah baca dan paham” tidak dihitung.</strong> Yang tidak "
                    "tercentang bukan kegagalan — itu daftar latihanmu minggu depan, dan "
                    "sekarang isinya jelas."))

langkah("Cara membaca hasil rubrikmu",
    blok("aksi", "Hitung centangmu per level, lalu baca baris yang sesuai.", "LAKUKAN"),
    tabel(["Kalau tercentang penuh sampai…", "Artinya untukmu"],
          [["<strong>L1–L2</strong>", "sudah cukup untuk melamar posisi data analyst pemula "
            "di Indonesia"],
           ["<strong>L1–L3</strong>", "lolos hampir semua tes SQL <em>live coding</em>"],
           ["<strong>L4</strong>", "membedakanmu dari kandidat lain yang juga bisa menulis "
            "window function"],
           ["<strong>L5</strong>", "tidak diuji di tes SQL mana pun — ia diuji di bulan ketiga "
            "bekerja, ketika ada yang bertanya “angka ini dari mana?”"]]),
    blok("catatan", "<strong>Kalau banyak yang belum tercentang, itu hasil yang benar, bukan "
                    "kabar buruk.</strong> Tidak ada yang menguasai lima level ini dalam sekali "
                    "baca. Cara memperbaikinya bukan mengulang membaca — tapi menutup halamannya, "
                    "membuka <code>senja.db</code>, dan mencoba menulis ulang satu query yang "
                    "belum tercentang dari nol. Gagal, buka kuncinya, tutup lagi, ulangi besok. "
                    "Itu satu-satunya cara yang bekerja, dan ia bekerja untuk semua orang."))

langkah("Dari SQLite ke basis data yang dipakai perusahaan",
    blok("aksi", "Baca tabel ini sekali, supaya kamu tidak terkejut di hari pertama kerja.", "LAKUKAN"),
    tabel(["Hal", "SQLite (yang kamu pakai)", "PostgreSQL / BigQuery / SQL Server"],
          [["Alias di <code>WHERE</code>", "Boleh — kamu buktikan sendiri di Hari 2",
            "<strong>Ditolak.</strong> Kebiasaan yang hanya SQLite izinkan; jangan dibawa."],
           ["Tipe kolom", "Longgar — angka bisa masuk ke kolom teks",
            "Ketat. Salah tipe = error. Ini kabar baik: kesalahan ketahuan lebih awal."],
           ["Tanggal", "Teks <code>'2024-01-31'</code> + fungsi <code>date()</code>",
            "Tipe <code>DATE</code> sungguhan, <code>DATE_TRUNC</code>, "
            "<code>INTERVAL '1 month'</code>. Lebih enak, konsepnya sama."],
           ["<code>QUALIFY</code>, <code>GROUPING SETS</code>", "Tidak ada",
            "Ada (<code>QUALIFY</code> di BigQuery/Snowflake) — jalan pintas untuk yang tadi "
            "butuh dua CTE."],
           ["Foreign key", "Mati kecuali dinyalakan tiap koneksi", "Selalu menyala."],
           ["Membaca rencana", "<code>EXPLAIN QUERY PLAN</code>",
            "<code>EXPLAIN ANALYZE</code> — lebih rinci, dengan waktu sungguhan per langkah."]]),
    blok("catatan", "<strong>Cara pindah yang paling murah:</strong> pasang PostgreSQL lewat "
                    "Docker, muat ulang <code>senja.db</code> ke dalamnya, lalu jalankan ulang "
                    "<strong>soal 6 sampai 9</strong>. Yang berubah cuma beberapa nama fungsi. "
                    "Setelah itu kamu boleh menulis “PostgreSQL” di CV-mu tanpa berbohong, karena "
                    "kamu memang sudah menjalankan window function di atasnya."))

langkah("Dua hal berikutnya yang paling menambah nilai jualmu",
    blok("aksi", "Baca urutannya. Urutan itu penting.", "LAKUKAN"),
    "<p><strong>1. dbt.</strong> Cara industri menyusun transformasi SQL jadi berkas-berkas "
    "berurutan, dengan pengujian bawaan. Berkas <code>uji_mutu.py</code> dari Level 4 adalah "
    "versi buatan tanganmu dari apa yang dilakukan dbt — <strong>kamu sudah paham gunanya "
    "sebelum melihat alatnya</strong>, dan itu urutan belajar yang benar.</p>",
    "<p><strong>2. Satu proyek nyata dengan data publik Indonesia.</strong> BPS, Kemenkeu, atau "
    "data terbuka pemda. Bukan latihan lagi: ambil data yang berantakan sungguhan, bersihkan, "
    "dan tulis <em>satu</em> temuan yang tidak terlihat dari angka mentahnya. Itu yang masuk "
    "portofolio, dan itu yang ditanyakan di wawancara.</p>",
    blok("catatan", "<strong>Ke mana lagi setelah ini.</strong> SQL-mu sudah cukup untuk bekerja. "
                    "Yang belum selesai ada di tempat lain di rute ini: "
                    "<strong>Bekal Data Klien</strong> untuk data yang datang sebagai Excel "
                    "berantakan, <strong>Bekal Kirim Hasil</strong> untuk mengantarkannya sampai "
                    "ke tangan klien, <strong>Bekal Rahasia Klien</strong> sebelum klien "
                    "pertamamu, dan <strong>Jalur Freelance</strong> untuk mengubah semua ini "
                    "jadi penghasilan."))

HARI7 = {
  "n": "HARI 7", "tab": "7",
  "judul": "Ujian akhir: satu brief klien, lima level sekaligus",
  "waktu": "± 120 menit",
  "tujuan": "mengerjakan pekerjaan analis yang lengkap dari satu kalimat permintaan — dan "
            "menemukan bahwa jawaban yang benar dimulai dengan <strong>menolak "
            "menjawabnya</strong>.",
  "langkah": L,
  "tutup_judul": "Jalur SQL Mahir selesai — kelima level",
  "tutup": "<p><strong>Tiga puluh lima hari</strong>, dari <code>SELECT</code> pertama sampai "
           "menolak menjawab brief klien yang datanya tidak sanggup. Kalau kamu sampai di sini "
           "dan balasanmu mirip versiku, jalur SQL-nya selesai. "
           "<strong>Bukan karena kamu hafal semua sintaks</strong> — kamu tidak, dan tidak "
           "perlu.</p>"
           "<p style=\"margin-top:8px\">Tapi karena kamu menjalankan pemeriksaan sebelum "
           "menghitung, menemukan lubang yang tidak memunculkan error, dan menolak memberi "
           "jawaban yang tidak didukung datanya. <strong>Itu tiga hal yang tidak bisa ditanyakan "
           "di wawancara sintaks, dan tiga hal yang menentukan apakah kamu dipanggil lagi.</strong></p>"
           "<p style=\"margin-top:8px\">Yang kamu bawa keluar bukan hafalan sintaks — sintaks bisa "
           "dicari kapan saja. Yang kamu bawa keluar adalah tiga kebiasaan yang tidak bisa "
           "dicari: <strong>menyebut asumsi sebelum menjawab, mencocokkan total sebelum "
           "mengirim, dan mengukur sebelum menyimpulkan.</strong></p>"
           "<p style=\"margin-top:8px\">Dan satu hal yang berlaku untuk seluruh jalur ini: "
           "<strong>tiap angka yang kamu baca di lima level ini dihasilkan dengan menjalankan "
           "kodenya, bukan dengan mengingat-ingat.</strong> Kalau ada satu kebiasaan yang layak "
           "kamu bawa dari halaman-halaman ini ke pekerjaanmu, itu dia.</p>",
}
