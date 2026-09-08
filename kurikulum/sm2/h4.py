# -*- coding: utf-8 -*-
"""Hari 4 — peringkat, kuartil, persentil, dan median sungguhan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Tiga fungsi peringkat, tiga jawaban berbeda",
    blok("aksi", "Berkas <code>senja/l2-hari-4.sql</code>. Empat nilai, dua di antaranya seri.",
         "LAKUKAN"),
    kode('''WITH t(nama, nilai) AS (VALUES ('a',30),('b',20),('c',20),('d',10))
SELECT nama, nilai,
  row_number() OVER (ORDER BY nilai DESC) AS row_number,
  rank()       OVER (ORDER BY nilai DESC) AS rank,
  dense_rank() OVER (ORDER BY nilai DESC) AS dense_rank
FROM t ORDER BY nilai DESC, nama;'''),
    keluaran(H, "h4_tiga_peringkat"),
    "<p><code>b</code> dan <code>c</code> seri di nilai 20. Perhatikan <strong>baris "
    "terakhir</strong> — di situlah ketiganya berpisah: 4, 4, dan 3.</p>")

langkah("Kapan pakai yang mana",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    tabel(["Fungsi", "Untuk yang seri", "Nomor berikutnya", "Pakai kalau"],
          [["<code>row_number</code>", "Dipaksa berbeda (2, 3)", "Berurutan",
            "Butuh <strong>tepat satu</strong> baris per kelompok — dedup, ambil yang terbaru"],
           ["<code>rank</code>", "Sama (2, 2)", "Melompat ke 4",
            "Peringkat kompetisi — dua juara kedua, tidak ada juara ketiga"],
           ["<code>dense_rank</code>", "Sama (2, 2)", "Lanjut ke 3",
            "Butuh tingkatan rapat tanpa lompatan — misal “3 tingkat harga teratas”"]]),
    "<p>Salah memilih di antara ketiganya adalah salah satu kesalahan yang paling sering lolos "
    "sampai ke laporan, karena angkanya tetap “terlihat seperti peringkat”.</p>")

langkah("ROW_NUMBER yang seri urutannya tidak dijamin",
    blok("aksi", "Baca sekali, lalu ingat baik-baik.", "LAKUKAN"),
    blok("bahaya", "<code>b</code> dan <code>c</code> sama-sama bernilai 20. Yang mana dapat "
                   "nomor 2 <strong>ditentukan mesin, dan bisa berubah antar-jalankan</strong>."),
    "<p>Kalau kamu memakai <code>row_number() = 1</code> untuk memilih “satu baris per "
    "pelanggan”, pastikan <code>ORDER BY</code>-nya memecah seri sampai tuntas — tambahkan kolom "
    "pemecah seperti <code>ORDER BY tanggal DESC, id DESC</code>.</p>",
    blok("catatan", "Tanpa itu, hasil query-mu tidak stabil, dan itu jenis bug yang muncul "
                    "sesekali lalu hilang lagi — jenis yang paling melelahkan untuk dilacak."))

langkah("Dedup: satu baris terakhir per pelanggan",
    blok("aksi", "Pola yang paling sering dipakai di pekerjaan nyata.", "LAKUKAN"),
    kode('''SELECT * FROM (
  SELECT o.pelanggan_id, o.id, o.tanggal,
         row_number() OVER (PARTITION BY o.pelanggan_id
                            ORDER BY o.tanggal DESC, o.id DESC) AS n
  FROM pesanan o WHERE o.pelanggan_id IS NOT NULL) x
WHERE n = 1 ORDER BY pelanggan_id LIMIT 5;'''),
    keluaran(H, "h4_dedup"),
    "<p>Perhatikan bentuknya: window function dihitung di <strong>dalam</strong>, penyaringnya "
    "di <strong>luar</strong>. Itu obat dari layar merah Hari 1 — dan kamu akan menulis bentuk "
    "ini puluhan kali.</p>",
    blok("catatan", "Di Level 1 kamu mengerjakan hal yang sama dengan <code>DISTINCT ON</code>. "
                    "Dua-duanya benar. <code>DISTINCT ON</code> lebih pendek tapi khas "
                    "PostgreSQL; <code>row_number</code> lebih panjang tapi berjalan di semua "
                    "mesin — dan itulah yang ditanyakan di wawancara."))

langkah("Berapa orang yang akan kamu bagi",
    blok("aksi", "Periksa penyebutnya dulu. Ini kebiasaan dari Level 1 Hari 2.", "LAKUKAN"),
    kode("""SELECT count(DISTINCT pelanggan_id) AS pelanggan_pernah_belanja
FROM pesanan WHERE status='selesai' AND pelanggan_id IS NOT NULL;"""),
    keluaran(H, "h4_jumlah_pelanggan"),
    "<p>Tujuh belas, bukan dua puluh. Tiga pelanggan belum pernah memesan, dan pesanan tamu "
    "tidak punya <code>pelanggan_id</code>. <strong>Angka 17 ini yang harus kamu lihat lagi "
    "di hasil langkah berikutnya</strong> — kalau bukan 17, ada yang salah.</p>")

langkah("Lihat lima pembelanja terbesar dulu",
    blok("aksi", "Sebelum membagi orang jadi kelompok, lihat sebarannya.", "LAKUKAN"),
    kode("""SELECT p.nama, sum(i.jumlah * i.harga_saat_itu) AS belanja
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
JOIN pelanggan p ON p.id = o.pelanggan_id
WHERE o.status='selesai' GROUP BY p.nama ORDER BY belanja DESC LIMIT 5;"""),
    keluaran(H, "h4_cte_belanja"),
    "<p>Dari 2,97 juta turun ke 2,57 juta — <strong>tidak ada yang mendominasi</strong>. Kalau "
    "pembelanja teratasmu sepuluh kali lipat yang kedua, seluruh rata-rata di laporanmu jadi "
    "menyesatkan, dan kamu harus menyebut median. Lihat sebarannya dulu, selalu.</p>")

langkah("Satu angka lagi supaya sebarannya punya konteks",
    blok("aksi", "Rata-rata berapa kali tiap pelanggan memesan.", "LAKUKAN"),
    kode("""SELECT round(avg(n), 1) AS rata2_pesanan_per_pelanggan FROM (
  SELECT pelanggan_id, count(*) AS n FROM pesanan
  WHERE status='selesai' AND pelanggan_id IS NOT NULL GROUP BY 1) x;"""),
    keluaran(H, "h4_pesanan_per_orang"),
    "<p>Sekitar 21 pesanan per pelanggan dalam enam bulan. Angka itu membuat belanja Rp 2 juta "
    "jadi masuk akal — dan <strong>kalau kamu tidak menghitungnya, kamu tidak punya cara tahu "
    "apakah angka besar tadi wajar atau ganjil.</strong></p>")

langkah("NTILE: membagi pelanggan jadi empat kelompok",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id)
SELECT p.nama, b.belanja,
  ntile(4)      OVER (ORDER BY b.belanja DESC) AS kuartil,
  rank()        OVER (ORDER BY b.belanja DESC) AS peringkat,
  round(percent_rank() OVER (ORDER BY b.belanja)::numeric, 2) AS persentil
FROM b JOIN pelanggan p ON p.id = b.pelanggan_id
ORDER BY b.belanja DESC;'''),
    keluaran(H, "h4_ntile"),
    "<p>Tujuh belas pelanggan kamu bagi empat. Perhatikan Fajar dapat persentil <strong>0,00</strong> "
    "dan Dimas <strong>1,00</strong> — nilai terendah selalu tepat 0, tertinggi selalu tepat 1, "
    "karena rumusnya (peringkat − 1) / (jumlah baris − 1).</p>")

langkah("Lihat NTILE bekerja di tabel yang kecil dulu",
    blok("aksi", "Tujuh produk kamu bagi tiga. Hitung sendiri anggotanya sebelum melihat.",
         "LAKUKAN"),
    kode("SELECT nama, harga, ntile(3) OVER (ORDER BY harga) AS kelompok FROM produk;"),
    keluaran(H, "h4_ntile_kecil"),
    "<p>7 dibagi 3 tidak bulat, jadi kelompok 1 dapat tiga anggota dan sisanya dua. "
    "<strong>Kamu bisa memeriksanya dengan jari</strong> — dan begitu kamu percaya di tabel "
    "tujuh baris, kamu boleh mempercayainya di tabel tujuh belas.</p>")

langkah("Hitung anggotanya, jangan percaya “dibagi rata”",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id),
k AS (SELECT ntile(4) OVER (ORDER BY belanja DESC) AS kuartil FROM b)
SELECT kuartil, count(*) AS anggota FROM k GROUP BY kuartil ORDER BY kuartil;'''),
    keluaran(H, "h4_anggota_kuartil"),
    "<p>17 tidak habis dibagi 4, dan <code>ntile</code> membagikan sisanya ke kelompok-kelompok "
    "<strong>paling awal</strong>. Kuartil 1 dapat 5 orang, sisanya 4.</p>")

langkah("NTILE menyamakan jumlah anggota, bukan mencari batas bermakna",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("bahaya", "Kalau tiga orang belanjanya nyaris sama tapi kebetulan jatuh di batas, dua "
                   "masuk kuartil 1 dan satu masuk kuartil 2 — padahal selisihnya tidak berarti "
                   "apa-apa."),
    "<p><code>ntile</code> menjawab <em>“siapa 25% teratas”</em>, bukan <em>“siapa yang "
    "belanjanya besar”</em>. Dua pertanyaan yang berbeda.</p>")

langkah("Kalau yang kamu butuhkan batas yang bermakna",
    blok("aksi", "Ambang bisnis datang dari bisnis, bukan dari pembagian rata.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id)
SELECT CASE WHEN belanja >= 2000000 THEN 'di atas 2 juta'
            ELSE 'di bawah 2 juta' END AS kelompok, count(*) AS orang
FROM b GROUP BY 1 ORDER BY 1;'''),
    keluaran(H, "h4_case_when"),
    "<p>Sembilan dan delapan. Angka Rp 2 juta itu <strong>keputusan</strong>, dan keputusan harus "
    "datang dari orang yang memakai laporannya — lalu kamu tulis di laporannya. Sama seperti "
    "ambang materialitas: bukan kamu yang menentukan sendiri, tapi kamu yang wajib "
    "mencantumkannya.</p>")

langkah("Median: yang paling sering diminta, dan tidak ada fungsinya",
    blok("aksi", "Coba cara yang paling wajar dulu.", "LAKUKAN"),
    kode("SELECT median(harga) FROM produk;"),
    keluaran(H, "h4_merah_median"),
    "<p>Tidak ada <code>median()</code> di SQL standar, dan PostgreSQL tidak menambahkannya. "
    "Yang ada bentuknya berbeda — dan lebih kuat.</p>")

langkah("percentile_cont: median dan persentil apa pun",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id)
SELECT round(avg(belanja))                                  AS rata_rata,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY belanja) AS median,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY belanja) AS median_baris_nyata,
       percentile_cont(0.9) WITHIN GROUP (ORDER BY belanja) AS persentil_90
FROM b;'''),
    keluaran(H, "h4_median"),
    "<p>Rata-rata Rp 2.047.588, median Rp 2.005.000. <code>WITHIN GROUP (ORDER BY ...)</code> "
    "adalah bentuk khusus untuk fungsi yang perlu <strong>data terurut</strong>, dan itu "
    "sebabnya bentuknya tidak seperti <code>avg()</code> biasa.</p>",
    blok("catatan", "<code>percentile_cont</code> <strong>menghitung</strong> nilainya (bisa di "
                    "antara dua baris, jadi hasilnya pecahan). <code>percentile_disc</code> "
                    "<strong>memilih</strong> baris yang benar-benar ada. Untuk gaji, harga, "
                    "atau apa pun yang harus berupa nilai nyata, pakai <code>disc</code>."))

langkah("Kenapa median lebih jujur daripada rata-rata",
    blok("aksi", "Baca sekali. Ini yang kamu ucapkan di wawancara.", "LAKUKAN"),
    blok("hasil", "<p>Rata-rata bisa ditarik satu pelanggan raksasa. Median tidak bisa. Kalau "
                  "keduanya jauh berbeda, <strong>selisih itu sendiri adalah temuan</strong>.</p>",
         "KALIMAT YANG DINILAI"),
    "<p>Di sini keduanya berdekatan (2.047.588 lawan 2.005.000), jadi sebarannya cukup rata — "
    "dan itu <em>juga</em> temuan yang kamu laporkan: tidak ada pelanggan yang mendominasi, "
    "jadi kehilangan satu klien tidak akan merobohkan angkanya.</p>",
    blok("catatan", "Ini alasan kurikulum ini memakai median untuk angka gaji, bukan angka "
                    "terbaik yang pernah dilaporkan orang. Aturan yang sama berlaku untuk "
                    "laporan yang kamu buat."))

langkah("Layar merah kecil yang mengingatkan NTILE butuh angka",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("SELECT ntile() OVER (ORDER BY harga) FROM produk;"),
    keluaran(H, "h4_merah_ntile"),
    "<p><code>ntile</code> harus diberi tahu <strong>berapa kelompok</strong>. Pesan errornya "
    "menyebut “tidak ada fungsi <code>ntile()</code>” — PostgreSQL mencari fungsi tanpa "
    "argumen, dan memang tidak ada.</p>")

langkah("Kerjakan sendiri",
    blok("aksi", "Tampilkan <strong>dua pelanggan dengan belanja terbesar di tiap cabang</strong>, "
                 "berikut peringkatnya. Pakai <code>dense_rank</code>, dan ingat bahwa penyaring "
                 "peringkat harus di luar.", "KERJAKAN, ± 15 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>WITH b AS (\n"
    "  SELECT o.cabang, o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja\n"
    "  FROM pesanan o JOIN item i ON i.pesanan_id = o.id\n"
    "  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL\n"
    "  GROUP BY o.cabang, o.pelanggan_id)\n"
    "SELECT cabang, nama, belanja, peringkat FROM (\n"
    "  SELECT b.cabang, p.nama, b.belanja,\n"
    "         dense_rank() OVER (PARTITION BY b.cabang ORDER BY b.belanja DESC) AS peringkat\n"
    "  FROM b JOIN pelanggan p ON p.id = b.pelanggan_id) x\n"
    "WHERE peringkat &lt;= 2 ORDER BY cabang, peringkat;</code></pre></div>"
    + keluaran(H, "h4_kunci", tag="HASILNYA") +
    "<p>Tiga cabang × 2 = enam baris. <strong>Kalau kamu mendapat lebih dari enam</strong>, itu "
    "bukan kesalahan — artinya ada seri di peringkat 2, dan <code>dense_rank</code> memang "
    "memberi nomor yang sama untuk seri. Kalau kamu butuh tepat dua per cabang apa pun yang "
    "terjadi, ganti ke <code>row_number</code> dan tambahkan pemecah seri.</p>"
    "<p>Besok kamu akan melihat cara ketiga untuk soal yang sama — <code>LATERAL</code>, yang "
    "sering lebih cepat karena berhenti setelah dua baris, bukan memberi peringkat kepada "
    "semua orang lalu membuang sisanya.</p></details>")

HARI4 = {
  "n": "HARI 4", "tab": "4",
  "judul": "Peringkat, kuartil, persentil, dan median sungguhan",
  "waktu": "± 60 menit",
  "tujuan": "memilih di antara tiga fungsi peringkat yang hasilnya berbeda saat ada seri, dan "
            "menghitung median serta persentil dengan <code>percentile_cont</code>.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>row_number</code> memaksa nomor unik (dan "
           "tidak stabil kalau seri tidak dipecah), <code>rank</code> melompat setelah seri, "
           "<code>dense_rank</code> tidak melompat · selalu tambahkan kolom pemecah seri · "
           "<code>ntile</code> menyamakan jumlah anggota, bukan mencari batas bermakna · median "
           "ditulis <code>percentile_cont(0.5) WITHIN GROUP (ORDER BY x)</code>.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 4 dari 8.</strong> Jawab dengan "
           "suara: <em>nilai 30, 20, 20, 10. Berapa nomor untuk baris terakhir menurut "
           "<code>row_number</code>, <code>rank</code>, dan <code>dense_rank</code>?</em></p>"
           "<details><summary>Kunci</summary><p><code>row_number</code> = 4, <code>rank</code> = 4 "
           "(melompat, karena dua baris berbagi peringkat 2), <code>dense_rank</code> = 3.</p></details>",
}
