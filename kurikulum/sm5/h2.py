# -*- coding: utf-8 -*-
"""Hari 2 — lima soal live coding."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Pasang pengatur waktu, sungguhan",
    blok("aksi", "Buka jam di HP-mu. Sepuluh menit per soal, dan berhenti saat bunyi.", "LAKUKAN"),
    blok("hasil", "<p><strong>Tulis dulu, jalankan, baru buka kunci.</strong></p>",
         "ATURAN MAIN"),
    "<p>Kalau kamu membuka kuncinya lebih dulu, kamu sedang membaca — bukan berlatih. Dan "
    "wawancara tidak menyediakan tombol buka kunci.</p>",
    blok("catatan", "<strong>Kalau bunyi sebelum kamu selesai, itu normal</strong> dan justru "
                    "informasi yang kamu butuhkan: kamu sekarang tahu soal mana yang perlu "
                    "kamu latih lagi. Catat waktunya, jangan hapus."))

langkah("Soal 1 — kerjakan dulu",
    blok("aksi", "Sepuluh menit, mulai sekarang.", "LAKUKAN"),
    kode("""SOAL 1  Berapa omzet tiap cabang, dan berapa pesanan yang menghasilkannya?
        Urutkan dari yang terbesar. Hitung hanya pesanan yang selesai.""", salin=False),
    blok("bahaya", "Sebelum mengetik: sebutkan asumsimu keras-keras. Berapa tabel yang kamu "
                   "butuhkan, dan apa yang kamu buang?"))

langkah("Kunci soal 1",
    blok("aksi", "Bandingkan dengan punyamu. Jangan disalin sebelum punyamu sudah ada.", "LAKUKAN"),
    kode("""SELECT p.cabang,
       SUM(i.jumlah * i.harga_saat_itu) AS omzet,
       COUNT(DISTINCT p.id)             AS pesanan
FROM pesanan p
JOIN item i ON i.pesanan_id = p.id
WHERE p.status = 'selesai'
GROUP BY p.cabang
ORDER BY omzet DESC"""),
    blok("hasil", "<pre><code>    cabang     omzet  pesanan\n"
                  "0     Dago  12665000      122\n"
                  "1   Kemang  11669000      120\n"
                  "2  Seturan  11405000      120</code></pre>", "HARUS MUNCUL"),
    "<p>Kalau angkamu cocok, lanjut. Kalau kolom <code>pesanan</code>-mu jauh lebih besar, "
    "langkah berikutnya menjelaskan kenapa.</p>")

langkah("Buang kata DISTINCT, dan lihat apa yang terjadi",
    blok("aksi", "Ganti <code>COUNT(DISTINCT p.id)</code> jadi <code>COUNT(*)</code>. "
                 "Jalankan.", "LAKUKAN"),
    kode("""SELECT p.cabang, COUNT(*) AS pesanan_salah
FROM pesanan p JOIN item i ON i.pesanan_id = p.id
WHERE p.status = 'selesai' GROUP BY p.cabang"""),
    blok("hasil", "<pre><code>    cabang  pesanan_salah\n0     Dago            238\n"
                  "1   Kemang            242\n2  Seturan            239</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "<strong>238 lawan 122 — dua kali lipat, tanpa error.</strong> Karena kamu "
                   "menyambung ke <code>item</code>, satu pesanan berisi tiga produk muncul "
                   "sebagai tiga baris. Ini kesalahan nomor satu di semua query yang "
                   "menggabungkan tabel induk dengan tabel rincinya."))

langkah("Sekarang periksa jawabanmu — langkah 4 dari kerangka",
    blok("aksi", "Hitung di kalkulator, lalu jalankan pembandingnya.", "LAKUKAN"),
    kode("print(con.execute(\"SELECT COUNT(*), SUM(status='batal') FROM pesanan\").fetchone())"),
    blok("hasil", "<pre><code>(400, 38)</code></pre>", "HARUS MUNCUL"),
    blok("hasil", "<pre><code>122 + 120 + 120  =  362\n362 + 38         =  400 &#10003;</code></pre>",
         "YANG HARUS COCOK"),
    "<p>Ucapkan ini keras-keras di wawancara: <em>“122 + 120 + 120 = 362, dan tabel pesanan "
    "berisi 400 baris dengan 38 batal. Cocok.”</em> Itu satu kalimat, dan kamu akan diingat "
    "karenanya.</p>")

langkah("Sebut satu kolom yang ada di dua tabel",
    blok("aksi", "Kedua tabel punya kolom <code>id</code>. Sebut tanpa awalan — sengaja.", "LAKUKAN"),
    kode('con.execute("SELECT id FROM pesanan p JOIN item i ON i.pesanan_id = p.id").fetchall()'),
    blok("bahaya", "<pre><code>OperationalError: ambiguous column name: id</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p><em>ambiguous</em> — SQL tidak mau menebak untukmu, dan itu bagus. Tulis "
    "<code>p.id</code> atau <code>i.id</code>.</p>",
    blok("catatan", "<strong>Biasakan memberi awalan pada SEMUA kolom</strong> begitu ada lebih "
                    "dari satu tabel, bahkan yang tidak ambigu. Kamu menulisnya sekali; kamu "
                    "membacanya berkali-kali."))

langkah("Soal 2 — kerjakan dulu",
    blok("aksi", "Sepuluh menit lagi.", "LAKUKAN"),
    kode("SOAL 2  Produk apa saja yang tidak pernah dipesan sama sekali?", salin=False),
    blok("catatan", "Petunjuk satu-satunya: kamu sudah menyelesaikan bentuk soal ini kemarin, "
                    "dengan nama yang berbeda."))

langkah("Kunci soal 2, dan hasil yang bikin panik",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""SELECT pr.id, pr.nama FROM produk pr
WHERE NOT EXISTS (SELECT 1 FROM item i WHERE i.produk_id = pr.id)"""),
    blok("hasil", "<pre><code>Empty DataFrame\nColumns: [id, nama]\nIndex: []</code></pre>",
         "HARUS MUNCUL"),
    blok("catatan", "<strong>Kosong, dan itu jawabannya.</strong> Ketujuh produk pernah dipesan. "
                    "Soal ini ada di sini justru karena hasil kosong membuat banyak orang panik "
                    "dan mulai mengubah-ubah query yang sebenarnya sudah benar."))

langkah("Buktikan bahwa kosong itu benar",
    blok("aksi", "Jangan percaya kosong begitu saja. Jalankan versi terbaliknya.", "LAKUKAN"),
    kode("""SELECT pr.nama, COUNT(i.id) AS baris_item, SUM(i.jumlah) AS unit
FROM produk pr LEFT JOIN item i ON i.produk_id = pr.id
GROUP BY pr.id, pr.nama ORDER BY baris_item DESC"""),
    blok("hasil", "<pre><code>           nama  baris_item  unit\n"
                  "0    Roti Bakar         137   326\n1  Matcha Latte         111   267\n"
                  "2     Teh Manis         110   252\n3     Americano         109   279\n"
                  "4     Croissant         108   253\n5    Cheesecake         107   256\n"
                  "6     Kopi Susu         106   274</code></pre>", "HARUS MUNCUL"),
    "<p>Ketujuhnya punya angka di atas nol. <strong>Sekarang kamu bisa bilang “tidak ada” "
    "dengan yakin</strong>, bukan dengan harap-harap cemas.</p>")

langkah("Alias di WHERE: SQLite mengizinkan, dan itu jebakannya",
    blok("aksi", "Jalankan dua baris ini. Yang pertama berhasil, yang kedua merah.", "LAKUKAN"),
    kode('print(len(con.execute("SELECT harga AS h FROM produk WHERE h > 20000").fetchall()))\n'
         'con.execute("SELECT SUM(jumlah) AS t FROM item WHERE t > 5").fetchall()'),
    blok("bahaya", "<pre><code>4\nOperationalError: misuse of aggregate: SUM()</code></pre>",
         "HARUS MUNCUL — ANGKA DULU, LALU TULISAN MERAH"),
    "<p>Baris pertama <strong>berhasil</strong> — SQLite mengizinkanmu memakai alias "
    "<code>h</code> di <code>WHERE</code>. Baris kedua gagal, tapi bukan karena aliasnya: "
    "karena <code>SUM()</code> adalah agregat, dan agregat memang tidak boleh di "
    "<code>WHERE</code>.</p>",
    blok("bahaya", "<strong>Dan justru baris pertama yang berbahaya buatmu.</strong> "
                   "<code>SELECT x AS y … WHERE y &gt; 5</code> adalah kelonggaran khas SQLite. "
                   "<strong>PostgreSQL, BigQuery, dan SQL Server menolaknya</strong> — di sana "
                   "alias baru ada di <code>SELECT</code>, yang jalan setelah <code>WHERE</code>. "
                   "Kebiasaan yang kamu bangun di SQLite akan patah di hari pertama kerja."),
    blok("catatan", "<strong>Alias BOLEH dipakai di <code>ORDER BY</code></strong> di mana pun, "
                    "karena <code>ORDER BY</code> berjalan paling akhir. Kamu sudah memakainya di "
                    "soal 1: <code>ORDER BY omzet DESC</code>. Pakai alias di <code>ORDER BY</code>, "
                    "jangan di <code>WHERE</code> — dan kamu aman di semua basis data."))

langkah("Soal 3 — dan bacalah soalnya dua kali",
    blok("aksi", "Sepuluh menit. Ada satu kata di soal ini yang menentukan seluruh "
                 "jawabannya.", "LAKUKAN"),
    kode("""SOAL 3  Berapa rata-rata NILAI SATU PESANAN di tiap kanal penjualan?
        (Perhatikan baik-baik: rata-rata per pesanan, bukan per baris item.)""", salin=False),
    blok("bahaya", "Kalau kamu langsung menulis <code>AVG(i.jumlah * i.harga_saat_itu)</code>, "
                   "berhenti — langkah berikutnya menunjukkan berapa jauh melesetnya."))

langkah("Jalankan versi yang salah dulu, supaya kamu merasakannya",
    blok("aksi", "Ini jawaban yang paling sering ditulis kandidat.", "LAKUKAN"),
    kode("""SELECT p.kanal, ROUND(AVG(i.jumlah * i.harga_saat_itu)) AS rata_salah
FROM pesanan p JOIN item i ON i.pesanan_id = p.id
WHERE p.status = 'selesai' GROUP BY p.kanal ORDER BY rata_salah DESC"""),
    blok("hasil", "<pre><code>       kanal  rata_salah\n0    Dine-in     51239.0\n"
                  "1  Take-away     50193.0\n2       Ojol     47748.0</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "<strong>Angkanya wajar-wajar saja, dan meleset separuh.</strong> Ini "
                   "rata-rata <em>per baris item</em>, bukan per pesanan. Tidak ada yang akan "
                   "memberitahumu."))

langkah("Kunci soal 3 — dua tingkat, dan di situlah nilainya",
    blok("aksi", "Perhatikan CTE-nya: pesanan dijadikan satu baris dulu.", "LAKUKAN"),
    kode("""WITH nilai AS (
  SELECT p.id, p.kanal, SUM(i.jumlah * i.harga_saat_itu) AS total
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status = 'selesai'
  GROUP BY p.id, p.kanal          -- SATU BARIS per pesanan dulu
)
SELECT kanal, COUNT(*) AS pesanan, ROUND(AVG(total)) AS rata_rata
FROM nilai GROUP BY kanal ORDER BY rata_rata DESC"""),
    blok("hasil", "<pre><code>       kanal  pesanan  rata_rata\n0    Dine-in      110   103409.0\n"
                  "1       Ojol      116    97966.0\n2  Take-away      136    95588.0</code></pre>",
         "HARUS MUNCUL"),
    "<p>103.409 lawan 51.239 — <strong>dua kali lipat</strong>. Dan periksa lagi: "
    "110 + 116 + 136 = 362, cocok dengan soal 1.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Kenapa COUNT(*) salah setelah JOIN ke tabel rinci?
2. Angka apa yang kamu cocokkan untuk membuktikan soal 1 benar?
3. Apa yang kamu lakukan ketika hasil query-mu kosong?
4. Kenapa rata-rata per pesanan butuh CTE?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Satu pesanan berisi N produk jadi N baris; <code>COUNT(*)</code> menghitungnya N kali "
    "— pakai <code>COUNT(DISTINCT p.id)</code>. "
    "2. 122+120+120 = 362, dan 400 − 38 batal = 362. "
    "3. <strong>Buktikan kosong itu benar</strong> dengan query terbalik — jangan langsung "
    "percaya, jangan langsung panik. "
    "4. Karena <code>AVG</code> langsung merata-ratakan <em>baris item</em>; pesanan harus "
    "dijadikan satu baris dulu.</p></details>")

HARI2 = {
  "n": "HARI 2", "tab": "2",
  "judul": "Tiga soal live coding, dan tiga cara mereka menjebakmu",
  "waktu": "± 70 menit",
  "tujuan": "menyelesaikan soal tingkat dasar–menengah di bawah pengatur waktu, dan mengenali "
            "tiga kesalahan yang <strong>tidak memunculkan error</strong>: "
            "<code>COUNT(*)</code> setelah join, panik pada hasil kosong, dan rata-rata di "
            "tingkat yang salah.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> tiga soal yang sudah kamu kerjakan di bawah "
           "tekanan waktu, dan satu kebiasaan yang lebih berharga daripada ketiganya — "
           "<strong>menjumlahkan hasilmu dan mencocokkannya dengan angka yang sudah kamu "
           "ketahui</strong>.</p>"
           "<p style=\"margin-top:8px\">Besok dua soal lagi, dan satu error yang sengaja kamu "
           "picu sendiri.</p>",
}
