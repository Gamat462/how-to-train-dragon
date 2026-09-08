# -*- coding: utf-8 -*-
"""Hari 6 — WHERE vs HAVING, urutan eksekusi, FILTER, dan ROLLUP."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bedanya cuma satu kalimat",
    blok("aksi", "Berkas <code>senja/hari-6.sql</code>. Baca sekali, hafalkan.", "LAKUKAN"),
    blok("hasil", "<p><code>WHERE</code> menyaring <strong>baris</strong>, sebelum "
                  "dikelompokkan. <code>HAVING</code> menyaring <strong>kelompok</strong>, "
                  "sesudah dihitung.</p>", "SATU KALIMAT"),
    "<p><code>HAVING</code> tidak pernah muncul di Modul M1–M6, padahal ia setengah dari cara "
    "menyaring di SQL. Hari ini kamu menutup separuh itu.</p>")

langkah("Dua penyaring dalam satu query, mengerjakan hal berbeda",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''SELECT cabang, count(*) AS pesanan
FROM pesanan
WHERE status = 'selesai'          -- saring BARIS dulu
GROUP BY cabang
HAVING count(*) > 100             -- saring KELOMPOK sesudahnya
ORDER BY pesanan DESC;'''),
    keluaran(H, "h6_where_having"),
    "<p><code>WHERE</code> membuang pesanan yang dibatalkan <em>sebelum apa pun dihitung</em>. "
    "<code>HAVING</code> membuang cabang yang pesanannya 100 ke bawah — dan itu hanya bisa "
    "dinilai <em>setelah</em> jumlahnya ada.</p>")

langkah("Sekarang tukar tempatnya, dengan sengaja",
    blok("aksi", "Taruh <code>count(*)</code> di dalam <code>WHERE</code>.", "LAKUKAN"),
    kode("SELECT cabang FROM pesanan WHERE count(*) > 100 GROUP BY cabang;"),
    keluaran(H, "h6_merah_count_where"),
    "<p>Bukan karena aturannya rewel padamu. Saat <code>WHERE</code> dijalankan, pengelompokan "
    "<strong>belum terjadi</strong> — jadi <code>count(*)</code> belum punya arti apa pun. Tidak "
    "ada yang bisa dihitung dari satu baris.</p>",
    blok("catatan", "Perhatikan bahasa pesannya: <em>aggregate functions are not allowed in "
                    "WHERE</em>. PostgreSQL menyebut namanya — bukan sekadar “misuse”. Pesan "
                    "error yang bisa dibaca adalah salah satu alasan orang memilih PostgreSQL."))

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
    blok("aksi", "<code>ORDER BY</code> memakai alias yang dibuat di baris pertama.", "LAKUKAN"),
    kode('''SELECT cabang, count(*) AS pesanan FROM pesanan
GROUP BY cabang ORDER BY pesanan DESC;'''),
    keluaran(H, "h6_alias_order_by"),
    "<p>Jalan, karena <code>ORDER BY</code> berjalan setelah <code>SELECT</code>. Sekarang kamu "
    "tidak lagi perlu menghafal aturan ini — kamu bisa menurunkannya sendiri dari tabel di "
    "langkah sebelumnya, kapan pun kamu lupa.</p>")

langkah("Sekarang buktikan bagian yang “belum ada”",
    blok("aksi", "Pakai alias yang sama di <code>WHERE</code>.", "LAKUKAN"),
    kode("SELECT harga*2 AS dobel FROM produk WHERE dobel > 30000;"),
    keluaran(H, "h6_merah_alias_where"),
    "<p>Persis seperti yang diramalkan tabel urutan tadi. Alias <code>dobel</code> baru lahir di "
    "langkah 5; <code>WHERE</code> berjalan di langkah 2.</p>",
    blok("catatan", "<strong>SQLite mengizinkan query ini.</strong> Kalau kamu pernah menulisnya "
                    "di SQLite dan berhasil, itu bukan ingatanmu yang salah — itu kelonggaran "
                    "SQLite yang ditolak PostgreSQL, SQL Server, dan sebagian besar mesin lain. "
                    "Pindah ke PostgreSQL membuat kebiasaan itu patah <em>di layarmu sendiri</em>, "
                    "bukan di wawancara."))

langkah("Dua cara memperbaikinya",
    blok("aksi", "Yang pertama: tulis ulang perhitungannya.", "LAKUKAN"),
    kode("SELECT nama, harga*2 AS dobel FROM produk WHERE harga*2 > 30000 ORDER BY harga;"),
    keluaran(H, "h6_tulis_ulang"),
    "<p>Berhasil, tapi rumusnya ditulis dua kali. Kalau nanti rumusnya berubah dan kamu hanya "
    "mengubah salah satunya, query-mu jadi salah tanpa memberi tanda.</p>")

langkah("Cara kedua, dan ini yang dipakai orang berpengalaman",
    blok("aksi", "Bungkus dengan CTE, lalu saring di luarnya.", "LAKUKAN"),
    kode('''WITH d AS (SELECT nama, harga*2 AS dobel FROM produk)
SELECT * FROM d WHERE dobel > 30000 ORDER BY dobel;'''),
    keluaran(H, "h6_cte"),
    blok("catatan", "Rumusnya ditulis <strong>sekali</strong>, dan nama <code>dobel</code> sudah "
                    "ada waktu <code>WHERE</code> di luar dijalankan — karena bagi query luar, "
                    "<code>d</code> adalah tabel biasa. Pola “hitung di dalam, saring di luar” "
                    "ini akan kamu pakai puluhan kali di Level 2 dan 3."))

langkah("Layar merah yang sering muncul saat menumpuk hasil",
    blok("aksi", "Salah ketik yang wajar: mengurutkan pakai kolom yang tidak ikut dipilih.",
         "LAKUKAN"),
    kode('''SELECT cabang FROM pesanan
UNION ALL SELECT kanal FROM pesanan
ORDER BY status;'''),
    keluaran(H, "h6_merah_order_union"),
    "<p>Setelah <code>UNION</code>, yang tersisa hanyalah kolom hasil — <code>status</code> "
    "sudah tidak ada lagi. Ini bentuk lain dari pelajaran yang sama: <strong>urutan jalannya "
    "menentukan apa yang masih tersedia</strong>.</p>")

langkah("FILTER: menghitung beberapa hal dalam satu lintasan",
    blok("aksi", "Berapa pesanan tiap cabang, berapa yang selesai, berapa yang batal — dalam "
                 "satu tabel.", "LAKUKAN"),
    kode('''SELECT cabang,
       count(*)                                 AS semua_pesanan,
       count(*) FILTER (WHERE status='selesai') AS selesai,
       count(*) FILTER (WHERE status='batal')   AS batal
FROM pesanan GROUP BY cabang ORDER BY cabang;'''),
    keluaran(H, "h6_filter"),
    "<p>Dengan <code>WHERE</code> saja kamu harus menjalankan tiga query lalu menggabungkannya "
    "sendiri. Di sini kamu cukup satu lintasan, satu tabel.</p>")

langkah("Sekarang temuannya kelihatan",
    blok("aksi", "Ubah jadi persentase.", "LAKUKAN"),
    kode('''SELECT cabang,
       round(100.0 * count(*) FILTER (WHERE status='batal') / count(*), 1) AS persen_batal
FROM pesanan GROUP BY cabang ORDER BY persen_batal DESC;'''),
    keluaran(H, "h6_persen_batal"),
    "<p>Ketiga cabang <em>menyelesaikan</em> pesanan hampir sama banyak (122, 120, 120). Tapi "
    "Seturan membatalkan <strong>13%</strong>, dua kali lipat Dago. Seturan menerima pesanan "
    "paling banyak dan kehilangan paling banyak.</p>",
    blok("catatan", "Perhatikan: temuan ini tidak terlihat sama sekali di tabel “jumlah pesanan "
                    "selesai per cabang”. Ia baru muncul ketika kamu menghitung yang "
                    "<em>gagal</em>, bukan yang berhasil."))

langkah("Kalau mesinnya tidak punya FILTER",
    blok("aksi", "Cara lama yang berfungsi di mana saja.", "LAKUKAN"),
    kode('''SELECT cabang, sum(CASE WHEN status='selesai' THEN 1 ELSE 0 END) AS selesai
FROM pesanan GROUP BY cabang ORDER BY cabang;'''),
    keluaran(H, "h6_case_when"),
    "<p>Angkanya sama persis dengan yang kamu dapat tadi. <code>FILTER (WHERE ...)</code> adalah "
    "SQL standar dan didukung PostgreSQL sejak versi 9.4. BigQuery tidak punya — di sana pakai "
    "<code>COUNTIF(...)</code>. <code>sum(CASE WHEN ...)</code> lebih panjang, berfungsi di mana "
    "saja, dan banyak dipakai di kode lama yang akan kamu warisi.</p>")

langkah("Subtotal tanpa menulis query kedua: ROLLUP",
    blok("aksi", "Ini yang membuat laporan berbentuk seperti kertas kerja. Jalankan.", "LAKUKAN"),
    kode('''SELECT COALESCE(cabang, 'SEMUA CABANG') AS cabang,
       COALESCE(kanal,  'semua kanal')  AS kanal,
       count(*) AS pesanan
FROM pesanan WHERE status = 'selesai'
GROUP BY ROLLUP (cabang, kanal)
ORDER BY GROUPING(cabang), cabang, GROUPING(kanal), kanal;'''),
    keluaran(H, "h6_rollup"),
    "<p>Rincian per kanal, <strong>subtotal per cabang</strong>, dan <strong>total "
    "keseluruhan</strong> — dari satu query. Angka 362 di baris terakhir adalah seluruh pesanan "
    "selesai, dan kamu akan bertemu angka itu lagi besok.</p>",
    blok("catatan", "<code>ROLLUP</code> membuat baris subtotal, dan di baris itu kolom yang "
                    "sedang “ditotal” bernilai <code>NULL</code>. <code>COALESCE</code> mengubah "
                    "<code>NULL</code> itu jadi label yang bisa dibaca — inilah salah satu dari "
                    "sedikit tempat <code>COALESCE</code> memang tepat dipakai."))

langkah("Kenapa ORDER BY-nya memakai GROUPING()",
    blok("aksi", "Baca sekali, lalu coba hapus <code>GROUPING(cabang)</code> dari "
                 "<code>ORDER BY</code>-nya dan lihat ke mana baris totalnya pindah.", "LAKUKAN"),
    blok("hasil", "<p><code>GROUPING(cabang)</code> bernilai <strong>0</strong> untuk baris "
                  "rincian dan <strong>1</strong> untuk baris subtotal. Mengurutkan dengannya "
                  "membuat subtotal selalu jatuh <em>di bawah</em> kelompoknya.</p>",
         "YANG DIKERJAKANNYA"),
    "<p>Tanpa itu, baris “SEMUA CABANG” akan diurutkan menurut abjad dan mendarat di antara "
    "Kemang dan Seturan — laporan yang terlihat kacau padahal angkanya benar.</p>")

langkah("GROUPING SETS: pilih sendiri subtotal mana yang kamu mau",
    blok("aksi", "<code>ROLLUP</code> membuat hierarki. <code>GROUPING SETS</code> membuat "
                 "persis yang kamu sebut.", "LAKUKAN"),
    kode('''SELECT COALESCE(cabang, '(total)') AS cabang,
       COALESCE(kanal,  '(total)') AS kanal,
       count(*) AS pesanan
FROM pesanan WHERE status = 'selesai'
GROUP BY GROUPING SETS ((cabang), (kanal), ())
ORDER BY GROUPING(cabang), GROUPING(kanal), cabang, kanal;'''),
    keluaran(H, "h6_grouping_sets"),
    "<p>Tiga tabel dalam satu: total per cabang, total per kanal, dan total keseluruhan — tanpa "
    "kombinasi cabang×kanal yang tidak kamu minta.</p>",
    blok("catatan", "<strong>Pemeriksaanmu:</strong> 122+120+120 = 362, dan 110+116+136 = 362. "
                    "Dua jalan berbeda ke angka yang sama. Kalau salah satunya tidak tutup, "
                    "ada baris yang tersaring keluar tanpa kamu sadari."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis satu query yang menampilkan, <strong>per kanal</strong> (Dine-in, "
                 "Take-away, Ojol): jumlah pesanan seluruhnya dan jumlah yang batal — tapi hanya "
                 "kanal yang pesanannya lebih dari 120.", "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>SELECT kanal, count(*) AS semua,\n"
    "       count(*) FILTER (WHERE status='batal') AS batal\n"
    "FROM pesanan GROUP BY kanal HAVING count(*) &gt; 120 ORDER BY kanal;</code></pre></div>"
    + keluaran(H, "h6_kunci", tag="HASILNYA") +
    "<p>Dine-in tersaring keluar oleh <code>HAVING</code>. Perhatikan bahwa syarat “lebih dari "
    "120” harus di <code>HAVING</code>, bukan <code>WHERE</code> — ia menilai kelompok, bukan "
    "baris.</p>"
    "<p>Dan satu bacaan lagi: Ojol membatalkan 12,8%, Take-away 9,3%. Kalau kamu menyerahkan "
    "tabel ini, sebutkan angka persennya — atasanmu tidak akan menghitungnya sendiri.</p>"
    "</details>")

HARI6 = {
  "n": "HARI 6", "tab": "6",
  "judul": "WHERE, HAVING, urutan jalannya, dan subtotal",
  "waktu": "± 60 menit",
  "tujuan": "menyebut urutan SQL dijalankan (bukan urutan ditulis), dan membuat laporan "
            "bersubtotal dengan <code>ROLLUP</code> tanpa menulis query kedua.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> urutan jalannya <code>FROM → WHERE → GROUP BY → "
           "HAVING → SELECT → ORDER BY → LIMIT</code>, dan alias lahir di langkah kelima · "
           "PostgreSQL menolak alias di <code>WHERE</code>, jadi pakai CTE · "
           "<code>count(*) FILTER (WHERE ...)</code> menghitung beberapa hal dalam satu lintasan · "
           "<code>ROLLUP</code> memberi subtotal, dan <code>GROUPING()</code> menjaga urutannya.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 6 dari 8.</strong> Jawab dengan "
           "suara: <em>apa beda <code>WHERE</code> dan <code>HAVING</code>, dan kenapa "
           "<code>count(*)</code> tidak boleh ada di <code>WHERE</code>?</em></p>"
           "<details><summary>Kunci</summary><p><code>WHERE</code> menyaring baris sebelum "
           "<code>GROUP BY</code>; <code>HAVING</code> menyaring kelompok sesudahnya. "
           "<code>count(*)</code> belum punya arti saat <code>WHERE</code> berjalan, karena "
           "kelompoknya belum terbentuk.</p></details>",
}
