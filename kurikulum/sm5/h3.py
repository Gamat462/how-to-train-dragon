# -*- coding: utf-8 -*-
"""Hari 3 — HAVING, pemecah seri, dan pertanyaan yang belum selesai."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Soal 4 — kerjakan dulu",
    blok("aksi", "Sepuluh menit.", "LAKUKAN"),
    kode("SOAL 4  Pelanggan mana yang memesan lebih dari 25 kali?", salin=False),
    blok("catatan", "Kelihatannya paling gampang di antara semua soal minggu ini. Ia menyimpan "
                    "<strong>tiga</strong> jebakan."))

langkah("Coba dengan WHERE, dan lihat penolakannya",
    blok("aksi", "Tulis pakai <code>WHERE</code> — dengan sengaja. Jalankan.", "LAKUKAN"),
    kode("""SELECT pl.nama FROM pelanggan pl
JOIN pesanan p ON p.pelanggan_id = pl.id
WHERE COUNT(*) > 25 GROUP BY pl.id"""),
    blok("bahaya", "<pre><code>OperationalError: misuse of aggregate: COUNT()</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Baca pesannya: <em>misuse of aggregate</em> — kamu memakai fungsi agregat di tempat "
    "yang salah. <code>WHERE</code> menyaring baris <strong>sebelum</strong> dikelompokkan, "
    "jadi saat ia bekerja <code>COUNT(*)</code> belum ada.</p>",
    blok("catatan", "<strong>Ini error yang ramah</strong>, dan kamu beruntung mendapatkannya. "
                    "Dua jebakan berikutnya di soal yang sama <em>tidak</em> memberi pesan "
                    "apa pun."))

langkah("Kunci soal 4",
    blok("aksi", "Ganti <code>WHERE</code> jadi <code>HAVING</code>, dan perhatikan dua hal "
                 "lain yang ikut berubah.", "LAKUKAN"),
    kode("""SELECT pl.nama, COUNT(*) AS pesanan
FROM pelanggan pl JOIN pesanan p ON p.pelanggan_id = pl.id
GROUP BY pl.id, pl.nama
HAVING COUNT(*) > 25
ORDER BY pesanan DESC, pl.nama"""),
    blok("hasil", "<pre><code>     nama  pesanan\n0    Rina       32\n1    Lita       30\n"
                  "2   Dimas       26\n3  Hendra       26</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau punyamu memberi lima baris</strong>, kamu memakai "
                    "<code>&gt;= 25</code>, bukan <code>&gt; 25</code>. Itu wajar terjadi dan "
                    "gampang dilewatkan — bacalah soalnya sekali lagi, bukan query-mu."),
    "<p><code>HAVING</code> menyaring <strong>kelompok</strong>, sesudah pengelompokan. Dua "
    "langkah berikutnya membongkar dua hal lain di query itu.</p>")

langkah("Jebakan kedua: GROUP BY nama saja",
    blok("aksi", "Bikin data uji: satu pelanggan kedua yang namanya juga Rina.", "LAKUKAN"),
    kode("""con.executescript(\"\"\"
CREATE TEMP TABLE pel2 AS SELECT * FROM pelanggan;
CREATE TEMP TABLE pes2 AS SELECT * FROM pesanan;
INSERT INTO pel2 (id, nama, kota) VALUES (99, 'Rina', 'Bandung');
UPDATE pes2 SET pelanggan_id = 99
 WHERE id IN (SELECT id FROM pesanan WHERE pelanggan_id = 1 LIMIT 5);
\"\"\")"""),
    blok("hasil", "<p>Tidak ada yang tercetak. Sekarang ada dua Rina: id 1 dan id 99.</p>",
         "HARUS MUNCUL"),
    "<p>Di data aslinya kebetulan tidak ada nama kembar. <strong>“Kebetulan tidak terjadi” "
    "bukan alasan untuk menulis query yang salah</strong> — jadi kita buat kebetulannya.</p>")

langkah("Sekarang lihat dua orang menjadi satu",
    blok("aksi", "Jalankan dua versi, bandingkan.", "LAKUKAN"),
    kode("""q = "FROM pel2 pl JOIN pes2 p ON p.pelanggan_id=pl.id WHERE pl.nama='Rina'"
print(pd.read_sql(f"SELECT pl.nama, COUNT(*) AS pesanan {q} GROUP BY pl.nama", con))
print(pd.read_sql(f"SELECT pl.id, pl.nama, COUNT(*) AS pesanan {q} GROUP BY pl.id, pl.nama", con))"""),
    blok("hasil", "<pre><code>   nama  pesanan\n0  Rina       32\n\n"
                  "   id  nama  pesanan\n0   1  Rina       27\n1  99  Rina        5</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "<strong>32 lawan 27+5.</strong> Yang pertama melaporkan satu pelanggan "
                   "hebat; yang kedua melaporkan dua pelanggan biasa. Tidak ada error, dan "
                   "angkanya sama-sama masuk akal dibaca."),
    "<p>Karena itu <code>GROUP BY pl.id, pl.nama</code> — kelompokkan menurut yang "
    "<strong>unik</strong>, bukan menurut yang <em>enak dibaca</em>.</p>")

langkah("Jebakan ketiga: urutan yang berubah sendiri",
    blok("aksi", "Lihat lagi hasil soal 4. Dimas dan Hendra sama-sama 26.", "LAKUKAN"),
    kode("""ORDER BY pesanan DESC              -- urutan Dimas & Hendra TIDAK DIJAMIN
ORDER BY pesanan DESC, pl.nama     -- dijamin, selamanya""", salin=False),
    blok("catatan", "<strong>Di laporan yang dikirim tiap hari ke klien</strong>, urutan yang "
                    "berubah sendiri tanpa sebab adalah pertanyaan yang tidak enak dijawab. "
                    "Selalu beri pemecah seri, dan pilih kolom yang unik."))

langkah("Soal 5 — kerjakan dulu",
    blok("aksi", "Sepuluh menit.", "LAKUKAN"),
    kode("SOAL 5  Tiga bulan dengan omzet tertinggi.", salin=False))

langkah("Kunci soal 5",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""SELECT substr(p.tanggal,1,7) AS bulan,
       SUM(i.jumlah * i.harga_saat_itu) AS omzet
FROM pesanan p JOIN item i ON i.pesanan_id = p.id
WHERE p.status = 'selesai'
GROUP BY bulan ORDER BY omzet DESC LIMIT 3"""),
    blok("hasil", "<pre><code>     bulan    omzet\n0  2024-02  6351000\n1  2024-05  6272000\n"
                  "2  2024-01  5968000</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau kamu menulis <code>ORDER BY omzet DESC</code> tapi lupa "
                    "<code>LIMIT 3</code></strong>, kamu dapat enam baris, bukan tiga. Itu bukan "
                    "error dan hasilnya tetap benar — cuma bukan yang diminta. Membaca soal "
                    "sampai habis termasuk bagian yang dinilai."),
    "<p>Empat baris, semua kandidat bisa menulisnya. <strong>Query-nya selesai; "
    "pertanyaannya belum.</strong></p>")

langkah("Kalimat yang membuatmu diingat",
    blok("aksi", "Ucapkan ini keras-keras sebelum melanjutkan.", "LAKUKAN"),
    blok("hasil", "<p>“Februari menang tipis dari Mei — 6.351.000 lawan 6.272.000, beda 1,3%. "
                  "Tapi Februari 2024 punya 29 hari dan Mei punya 31. Selisih setipis ini bisa "
                  "jadi cuma soal jumlah hari. <strong>Mau aku hitung per hari?</strong>”</p>",
         "YANG KAMU UCAPKAN"),
    "<p>Lalu hitung — karena hasilnya bukan yang kamu duga.</p>")

langkah("Hitung per hari yang benar-benar ada pesanan",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""SELECT substr(p.tanggal,1,7) AS bulan,
       SUM(i.jumlah * i.harga_saat_itu) AS omzet,
       COUNT(DISTINCT p.tanggal) AS hari_ada_pesanan,
       ROUND(SUM(i.jumlah * i.harga_saat_itu) * 1.0
             / COUNT(DISTINCT p.tanggal)) AS per_hari_aktif
FROM pesanan p JOIN item i ON i.pesanan_id = p.id
WHERE p.status = 'selesai'
GROUP BY bulan ORDER BY omzet DESC"""),
    blok("hasil", "<pre><code>     bulan    omzet  hari_ada_pesanan  per_hari_aktif\n"
                  "0  2024-02  6351000                25        254040.0\n"
                  "1  2024-05  6272000                23        272696.0\n"
                  "2  2024-01  5968000                28        213143.0\n"
                  "3  2024-06  5820000                22        264545.0\n"
                  "4  2024-04  5754000                25        230160.0\n"
                  "5  2024-03  5574000                28        199071.0</code></pre>",
         "HARUS MUNCUL"),
    "<p><strong>Pemenangnya berganti.</strong> Mei 272.696, Februari 254.040 — karena Februari "
    "punya 25 hari berpesanan dan Mei cuma 23.</p>")

langkah("Tiga cara membagi, tiga pemenang, dan ketiganya benar",
    blok("aksi", "Baca tabel ini, lalu tutup halaman.", "LAKUKAN"),
    tabel(["Cara membaca", "Pemenang", "Angkanya"],
          [["Omzet mentah", "Februari", "6.351.000 (unggul 1,3%)"],
           ["Dibagi hari kalender", "Februari", "219.000 lawan 202.323 (unggul 8%)"],
           ["Dibagi hari yang ada pesanan", "<strong>Mei</strong>", "272.696 lawan 254.040"]]),
    "<p>Ketiganya menjawab pertanyaan yang sedikit berbeda. <strong>Yang salah cuma satu hal: "
    "menyebut salah satunya “bulan terbaik” tanpa mengatakan yang mana yang kamu maksud.</strong></p>",
    blok("catatan", "<strong>Catatan kinerja dari Level 4:</strong> <code>substr()</code> di "
                    "<code>GROUP BY</code> tidak apa-apa — pengelompokan memang menyentuh semua "
                    "baris. Yang mematikan index adalah <code>substr()</code> di "
                    "<code>WHERE</code>. Tahu bedanya adalah tanda kamu paham alasannya, bukan "
                    "hafal aturannya."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Pesan error apa yang muncul kalau COUNT(*) ditaruh di WHERE?
2. Kenapa GROUP BY pl.id, pl.nama — bukan pl.nama saja?
3. Kenapa ORDER BY selalu perlu pemecah seri?
4. Tiga cara membaca "bulan terbaik", dan mana yang benar?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>misuse of aggregate: COUNT()</code> — pakai <code>HAVING</code>. "
    "2. Dua orang bernama sama akan digabung jadi satu, tanpa error. "
    "3. Tanpa itu urutan baris yang nilainya sama tidak dijamin dan bisa berubah antar-jalankan. "
    "4. Omzet mentah, per hari kalender, per hari yang ada pesanan — <strong>ketiganya "
    "benar</strong>; yang salah adalah tidak menyebut yang mana.</p></details>")

HARI3 = {
  "n": "HARI 3", "tab": "3",
  "judul": "HAVING, nama kembar, dan pertanyaan yang belum selesai",
  "waktu": "± 75 menit",
  "tujuan": "menyelesaikan dua soal lagi, dan menemukan bahwa satu soal yang terlihat paling "
            "gampang justru menyimpan tiga jebakan — hanya satu di antaranya yang memberi "
            "pesan error.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu error yang kamu picu sendiri "
           "(<code>misuse of aggregate</code>), dua kesalahan diam di query yang sama, dan satu "
           "kalimat yang membuat pewawancara mengingatmu — <em>“mau aku hitung per hari?”</em></p>"
           "<p style=\"margin-top:8px\">Besok tingkat yang dipakai untuk posisi berpengalaman: "
           "window function, tanpa contoh di depanmu.</p>",
}
