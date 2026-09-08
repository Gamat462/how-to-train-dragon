# -*- coding: utf-8 -*-
"""Hari 6 — WHERE vs HAVING, urutan yang sebenarnya dijalankan, dan FILTER."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bedanya cuma satu kalimat",
    blok("aksi", "Baca sekali, hafalkan.", "LAKUKAN"),
    blok("hasil", "<p><code>WHERE</code> menyaring <strong>baris</strong>, sebelum dikelompokkan. "
                  "<code>HAVING</code> menyaring <strong>kelompok</strong>, sesudah "
                  "dihitung.</p>", "SATU KALIMAT"),
    "<p><code>HAVING</code> tidak pernah muncul di Modul M1–M6 yang sudah kamu kerjakan, padahal "
    "ia setengah dari cara menyaring di SQL. Hari ini kamu menutup separuh itu.</p>")

langkah("Dua penyaring dalam satu query, mengerjakan hal berbeda",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT cabang, COUNT(*) AS pesanan
     FROM pesanan
     WHERE status = 'selesai'          -- saring BARIS dulu
     GROUP BY cabang
     HAVING COUNT(*) > 100             -- saring KELOMPOK sesudahnya
     ORDER BY pesanan DESC""")'''),
    blok("hasil", "<pre><code>    cabang  pesanan\n0     Dago      122\n1  Seturan      120\n"
                  "2   Kemang      120</code></pre>", "HARUS MUNCUL"),
    "<p><code>WHERE</code> membuang pesanan yang dibatalkan <em>sebelum apa pun dihitung</em>. "
    "<code>HAVING</code> membuang cabang yang pesanannya 100 ke bawah — dan itu hanya bisa "
    "dinilai <em>setelah</em> jumlahnya ada.</p>")

langkah("Sekarang tukar tempatnya, dengan sengaja",
    blok("aksi", "Sel baru. Taruh <code>COUNT(*)</code> di dalam <code>WHERE</code>.", "LAKUKAN"),
    kode('q("SELECT cabang FROM pesanan WHERE COUNT(*) > 100 GROUP BY cabang")'),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': misuse of "
                  "aggregate: COUNT()</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Bukan karena aturannya rewel padamu. Saat <code>WHERE</code> dijalankan, pengelompokan "
    "<strong>belum terjadi</strong> — jadi <code>COUNT(*)</code> belum punya arti apa pun. "
    "Tidak ada yang bisa dihitung dari satu baris.</p>")

langkah("SQL tidak dijalankan sesuai urutan tulisannya",
    blok("aksi", "Salin tabel ini ke catatanmu. Ini yang menjelaskan hampir semua error SQL yang "
                 "terasa acak.", "LAKUKAN"),
    tabel(["Urutan kamu menulis", "Urutan mesin menjalankan", "Yang terjadi"],
          [["<code>SELECT</code>", "1. <code>FROM</code> / <code>JOIN</code>",
            "Tabel disiapkan dan digabung"],
           ["<code>FROM</code>", "2. <code>WHERE</code>", "Baris disaring satu per satu"],
           ["<code>WHERE</code>", "3. <code>GROUP BY</code>", "Baris dikumpulkan jadi kelompok"],
           ["<code>GROUP BY</code>", "4. <code>HAVING</code>", "Kelompok disaring"],
           ["<code>HAVING</code>", "5. <code>SELECT</code>",
            "<strong>Alias baru lahir di sini</strong>"],
           ["<code>ORDER BY</code>", "6. <code>ORDER BY</code>", "Hasil akhir diurutkan"],
           ["<code>LIMIT</code>", "7. <code>LIMIT</code>", "Dipotong sekian baris"]]),
    "<p>Baris kelima menjelaskan segalanya. Nama alias yang kamu buat di <code>SELECT</code> "
    "<strong>belum ada</strong> waktu <code>WHERE</code> dijalankan — tapi <strong>sudah "
    "ada</strong> waktu <code>ORDER BY</code> dijalankan.</p>")

langkah("Buktikan bagian yang “sudah ada”",
    blok("aksi", "Sel baru. <code>ORDER BY</code> memakai alias yang dibuat di baris pertama.",
         "LAKUKAN"),
    kode('''q("""SELECT cabang, COUNT(*) AS pesanan FROM pesanan
     GROUP BY cabang ORDER BY pesanan DESC""")'''),
    blok("hasil", "<pre><code>    cabang  pesanan\n0  Seturan      138\n1   Kemang      132\n"
                  "2     Dago      130</code></pre>", "HARUS MUNCUL"),
    "<p>Jalan, karena <code>ORDER BY</code> berjalan setelah <code>SELECT</code>. Sekarang kamu "
    "tidak lagi perlu menghafal aturan ini — kamu bisa menurunkannya sendiri dari tabel di "
    "langkah sebelumnya, kapan pun kamu lupa.</p>")

langkah("Satu tempat di mana SQLite berbohong kepadamu",
    blok("aksi", "Sel baru. Menurut tabel tadi, ini seharusnya gagal.", "LAKUKAN"),
    kode('q("SELECT harga*2 AS dobel FROM produk WHERE dobel > 30000")'),
    blok("hasil", "<pre><code>   dobel\n0  44000\n1  36000\n2  50000\n3  60000\n"
                  "4  52000</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Jalan — dan itulah masalahnya.</strong> SQLite sengaja longgar dan "
                   "mengizinkannya. PostgreSQL menolak query ini dengan "
                   "<code>column \"dobel\" does not exist</code>, begitu juga SQL Server dan "
                   "sebagian besar mesin lain."))

langkah("Kenapa kelonggaran itu mahal",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    "<p>Query yang kamu uji dan berhasil di latihan ini <strong>bisa gagal begitu dipindahkan "
    "ke basis data klien atau ke BigQuery</strong>. Dan memindahkan query antar mesin adalah "
    "pekerjaan sehari-hari analis, bukan hal langka.</p>",
    blok("hasil", "<p>Aturan yang aman di mana pun: <strong>jangan pakai alias di "
                  "<code>WHERE</code></strong>. Tulis ulang perhitungannya "
                  "(<code>WHERE harga*2 &gt; 30000</code>), atau bungkus dengan CTE.</p>",
         "YANG KAMU LAKUKAN"))

langkah("Cara yang aman, dan lebih terbaca",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""WITH d AS (SELECT nama, harga*2 AS dobel FROM produk)
     SELECT * FROM d WHERE dobel > 30000""")'''),
    blok("hasil", "<pre><code>           nama  dobel\n0     Kopi Susu  44000\n1     Americano  36000\n"
                  "2     Croissant  50000\n3    Cheesecake  60000\n"
                  "4  Matcha Latte  52000</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau sebuah query akan dipakai lebih dari sekali, jalankan sekali "
                    "di mesin tujuannya sebelum diserahkan.</strong> “Jalan di SQLite” bukan "
                    "jaminan apa pun."))

langkah("Empat perbedaan dialek yang paling sering menggigit",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    tabel(["Hal", "Yang perlu kamu ingat"],
          [["Alias di <code>WHERE</code>",
            "SQLite mengizinkan; PostgreSQL, SQL Server, BigQuery menolak"],
           ["Tanda kutip",
            "SQL standar: kutip tunggal untuk teks. Kutip ganda berarti <em>nama kolom</em>"],
           ["Penggabungan teks", "<code>||</code> di SQLite/PostgreSQL, "
            "<code>CONCAT()</code> di MySQL dan BigQuery"],
           ["Fungsi tanggal", "Namanya berbeda di hampir tiap mesin — selalu cek dokumentasinya"]]),
    "<p>Kamu tidak perlu menghafal semua dialek. Kamu cuma perlu <strong>tahu bahwa dialek itu "
    "ada</strong>, supaya kamu menguji sebelum menjanjikan.</p>")

langkah("Layar merah yang sering muncul saat menumpuk hasil",
    blok("aksi", "Sel baru. Salah ketik yang wajar: mengurutkan pakai kolom yang tidak ikut "
                 "dipilih.", "LAKUKAN"),
    kode('''q("""SELECT cabang FROM pesanan
     UNION ALL SELECT kanal FROM pesanan
     ORDER BY status""")'''),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': 1st ORDER BY term "
                  "does not match any column in the result set</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Setelah <code>UNION</code>, yang tersisa hanyalah kolom hasil — <code>status</code> "
    "sudah tidak ada lagi. Ini bentuk lain dari pelajaran yang sama: <strong>urutan jalannya "
    "menentukan apa yang masih tersedia</strong>.</p>")

langkah("FILTER: menghitung beberapa hal dalam satu lintasan",
    blok("aksi", "Sel baru. Berapa pesanan tiap cabang, berapa yang selesai, berapa yang batal "
                 "— dalam satu tabel.", "LAKUKAN"),
    kode('''q("""SELECT cabang,
       COUNT(*)                                 AS semua_pesanan,
       COUNT(*) FILTER (WHERE status='selesai') AS selesai,
       COUNT(*) FILTER (WHERE status='batal')   AS batal
     FROM pesanan GROUP BY cabang ORDER BY cabang""")'''),
    blok("hasil", "<pre><code>    cabang  semua_pesanan  selesai  batal\n"
                  "0     Dago            130      122      8\n"
                  "1   Kemang            132      120     12\n"
                  "2  Seturan            138      120     18</code></pre>", "HARUS MUNCUL"),
    "<p>Dengan <code>WHERE</code> saja kamu harus menjalankan tiga query lalu menggabungkannya "
    "sendiri. Di sini kamu cukup satu lintasan, satu tabel.</p>")

langkah("Sekarang temuannya kelihatan",
    blok("aksi", "Sel baru. Ubah jadi persentase.", "LAKUKAN"),
    kode('''q("""SELECT cabang,
       ROUND(100.0*COUNT(*) FILTER (WHERE status='batal')/COUNT(*),1) AS persen_batal
     FROM pesanan GROUP BY cabang ORDER BY persen_batal DESC""")'''),
    blok("hasil", "<pre><code>    cabang  persen_batal\n0  Seturan          13.0\n"
                  "1   Kemang           9.1\n2     Dago           6.2</code></pre>",
         "HARUS MUNCUL"),
    "<p>Ketiga cabang <em>menyelesaikan</em> pesanan hampir sama banyak (122, 120, 120). Tapi "
    "Seturan membatalkan <strong>13%</strong>, dua kali lipat Dago. Seturan menerima pesanan "
    "paling banyak dan kehilangan paling banyak.</p>",
    blok("catatan", "Perhatikan: temuan ini tidak terlihat sama sekali di tabel “jumlah pesanan "
                    "selesai per cabang”. Ia baru muncul ketika kamu menghitung yang "
                    "<em>gagal</em>, bukan yang berhasil."))

langkah("Kalau mesinnya tidak punya FILTER",
    blok("aksi", "Sel baru. Cara lama yang berfungsi di mana saja.", "LAKUKAN"),
    kode('''q("""SELECT cabang,
       SUM(CASE WHEN status='selesai' THEN 1 ELSE 0 END) AS selesai
     FROM pesanan GROUP BY cabang ORDER BY cabang""")'''),
    blok("hasil", "<pre><code>    cabang  selesai\n0     Dago      122\n1   Kemang      120\n"
                  "2  Seturan      120</code></pre>", "HARUS MUNCUL"),
    "<p>Angkanya sama persis dengan yang kamu dapat tadi. <code>FILTER (WHERE ...)</code> adalah "
    "SQL standar dan didukung "
    "SQLite (sejak 3.30) serta PostgreSQL. BigQuery tidak punya — di sana pakai "
    "<code>COUNTIF(status='selesai')</code>. <code>SUM(CASE WHEN ...)</code> lebih panjang, "
    "berfungsi di mana saja, dan banyak dipakai di kode lama yang akan kamu warisi.</p>")

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis satu query yang menampilkan, <strong>per kanal</strong> (Dine-in, "
                 "Take-away, Ojol): jumlah pesanan seluruhnya dan jumlah yang batal — tapi hanya "
                 "kanal yang pesanannya lebih dari 120.", "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>q(\"\"\"SELECT kanal, COUNT(*) AS semua,\n"
    "       COUNT(*) FILTER (WHERE status='batal') AS batal\n"
    "     FROM pesanan GROUP BY kanal HAVING COUNT(*) &gt; 120 ORDER BY kanal\"\"\")"
    "</code></pre></div>"
    "<pre><code>       kanal  semua  batal\n0       Ojol    133     17\n"
    "1  Take-away    150     14</code></pre>"
    "<p>Dine-in tersaring keluar oleh <code>HAVING</code>. Perhatikan bahwa syarat “lebih dari "
    "120” harus di <code>HAVING</code>, bukan <code>WHERE</code> — ia menilai kelompok, bukan "
    "baris.</p>"
    "<p>Dan satu bacaan lagi: Ojol membatalkan 12,8%, Take-away 9,3%. Kalau kamu menyerahkan "
    "tabel ini, sebutkan angka persennya — atasanmu tidak akan menghitungnya sendiri.</p>"
    "</details>")

HARI6 = {
  "n": "HARI 6", "tab": "6",
  "judul": "WHERE, HAVING, dan urutan yang sebenarnya dijalankan",
  "waktu": "± 55 menit",
  "tujuan": "menyebut urutan SQL dijalankan (bukan urutan ditulis), dan tahu kenapa itu "
            "menjelaskan hampir semua pesan error yang membingungkan.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> urutan jalannya <code>FROM → WHERE → GROUP BY → "
           "HAVING → SELECT → ORDER BY → LIMIT</code>, dan alias lahir di langkah kelima · "
           "SQLite mengizinkan alias di <code>WHERE</code>, PostgreSQL tidak — jangan pakai · "
           "<code>COUNT(*) FILTER (WHERE ...)</code> menghitung beberapa hal dalam satu "
           "lintasan.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 6 dari 8.</strong> Jawab dengan "
           "suara: <em>apa beda <code>WHERE</code> dan <code>HAVING</code>, dan kenapa "
           "<code>COUNT(*)</code> tidak boleh ada di <code>WHERE</code>?</em></p>"
           "<details><summary>Kunci</summary><p><code>WHERE</code> menyaring baris sebelum "
           "<code>GROUP BY</code>; <code>HAVING</code> menyaring kelompok sesudahnya. "
           "<code>COUNT(*)</code> belum punya arti saat <code>WHERE</code> berjalan, karena "
           "kelompoknya belum terbentuk.</p></details>",
}
