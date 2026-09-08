# -*- coding: utf-8 -*-
"""Hari 4 — lima jenis JOIN, dan jumlah baris sebagai alat pemeriksa."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Periksa dulu versi mesin basis datamu",
    blok("aksi", "Sel baru. Jangan menebak — periksa.", "LAKUKAN"),
    kode('''import sqlite3
print("SQLite versi", sqlite3.sqlite_version)'''),
    blok("hasil", "<pre><code>SQLite versi 3.45.1</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau versimu berbeda, itu tidak apa-apa</strong> — yang penting "
                    "3.39 atau lebih baru. <code>RIGHT JOIN</code> dan <code>FULL OUTER JOIN</code> "
                    "baru didukung SQLite sejak 3.39 (rilis 2022). Kalau versimu lebih tua, "
                    "lewati dua langkah itu; sisanya tetap bisa kamu kerjakan."))

langkah("Kebiasaan yang layak kamu bawa ke tempat kerja",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Sebelum memakai fitur SQL yang jarang, <strong>cek dulu apakah mesinnya "
                  "mendukung</strong>. Satu baris, dua detik.</p>", "REFLEKS"),
    "<p>PostgreSQL, BigQuery, dan SQL Server mendukung kelima JOIN sejak lama. MySQL "
    "<strong>tidak punya <code>FULL OUTER JOIN</code> sama sekali</strong> dan harus ditiru "
    "dengan <code>UNION</code>. Perbedaan dialek seperti ini yang membuat query “yang tadi "
    "jalan” tiba-tiba gagal di tempat kerja baru.</p>")

langkah("Layar merah yang akan sering kamu temui",
    blok("aksi", "Sel baru. Dua tabel, dua kolom bernama sama.", "LAKUKAN"),
    kode('''q("""SELECT id FROM pelanggan p
     JOIN pesanan o ON o.pelanggan_id = p.id""")'''),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': ambiguous column "
                  "name: id</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("catatan", "<code>pelanggan</code> punya <code>id</code>, <code>pesanan</code> juga. SQL "
                    "tidak mau menebak yang mana yang kamu maksud — dan itu bagus. Tulis "
                    "<code>p.id</code> atau <code>o.id</code>, jangan <code>id</code> saja."),
    "<p><strong>Setiap kali layarmu merah karena ini</strong>, obatnya selalu sama: beri awalan "
    "alias ke kolomnya.</p>")

langkah("JOIN pertama: hanya yang cocok di kedua sisi",
    blok("aksi", "Sel baru. Hitung barisnya, jangan lihat isinya dulu.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris
     FROM pelanggan p JOIN pesanan o ON o.pelanggan_id = p.id""")'''),
    blok("hasil", "<pre><code>   baris\n0    388</code></pre>", "HARUS MUNCUL"),
    "<p>388 dari 400 pesanan. <code>JOIN</code> polos yang kamu tulis itu sama dengan "
    "<code>INNER JOIN</code> — hanya pasangan yang cocok di kedua sisi yang lolos.</p>")

langkah("LEFT JOIN: semua yang di kiri tetap ada",
    blok("aksi", "Sel baru. Ganti satu kata.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris
     FROM pelanggan p LEFT JOIN pesanan o ON o.pelanggan_id = p.id""")'''),
    blok("hasil", "<pre><code>   baris\n0    391</code></pre>", "HARUS MUNCUL"),
    "<p>391 = 388 + 3. Tiga tambahan itu <strong>Andi, Bagus, dan Vira</strong> dari kemarin — "
    "pelanggan yang tidak punya pesanan tetap muncul, dengan kolom kanan berisi "
    "<code>NULL</code>.</p>")

langkah("RIGHT JOIN: semua yang di kanan tetap ada",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris
     FROM pelanggan p RIGHT JOIN pesanan o ON o.pelanggan_id = p.id""")'''),
    blok("hasil", "<pre><code>   baris\n0    400</code></pre>", "HARUS MUNCUL"),
    "<p>400 = 388 + 12. Dua belas tambahan itu pesanan tamu yang <code>pelanggan_id</code>-nya "
    "<code>NULL</code>. Hasilnya <strong>seluruh 400 pesanan</strong>.</p>")

langkah("FULL OUTER JOIN: semua dari dua sisi",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris
     FROM pelanggan p FULL OUTER JOIN pesanan o ON o.pelanggan_id = p.id""")'''),
    blok("hasil", "<pre><code>   baris\n0    403</code></pre>", "HARUS MUNCUL"),
    "<p>403 = 388 + 3 + 12. Tidak ada yang tertinggal dari sisi mana pun, dan kamu bisa "
    "menjelaskan tiap sukunya.</p>")

langkah("CROSS JOIN: semua kombinasi, tanpa syarat",
    blok("aksi", "Sel baru. Perhatikan: tidak ada <code>ON</code>.", "LAKUKAN"),
    kode('q("SELECT COUNT(*) AS baris FROM pelanggan CROSS JOIN produk")'),
    blok("hasil", "<pre><code>   baris\n0    140</code></pre>", "HARUS MUNCUL"),
    "<p>140 = 20 pelanggan × 7 produk. Kamu memasangkan setiap pelanggan dengan setiap produk, "
    "tanpa syarat apa pun.</p>")

langkah("Kelima angka itu bisa kamu buktikan sendiri",
    blok("aksi", "Cocokkan tabel ini dengan lima angka yang barusan kamu jalankan.", "LAKUKAN"),
    tabel(["Jenis", "Baris", "Dari mana angkanya"],
          [["<code>INNER</code>", "388", "Hanya pasangan yang cocok di kedua sisi"],
           ["<code>LEFT</code>", "391", "388 + 3 pelanggan yang tidak punya pesanan"],
           ["<code>RIGHT</code>", "400", "388 + 12 pesanan tamu = seluruh 400 pesanan"],
           ["<code>FULL OUTER</code>", "403", "388 + 3 + 12 = semua dari dua sisi"],
           ["<code>CROSS</code>", "140", "20 pelanggan × 7 produk, tanpa syarat sama sekali"]],
          kelas_n=(1,)),
    "<p>Kamu sudah tahu dua fakta itu dari dua hari sebelumnya: 12 pesanan tanpa "
    "<code>pelanggan_id</code>, dan 3 pelanggan tanpa pesanan. Semuanya menyambung.</p>")

langkah("Ini refleks yang paling banyak menyelamatkanmu",
    blok("aksi", "Baca, lalu ucapkan dengan suara keras.", "LAKUKAN"),
    blok("hasil", "<p><strong>Sebelum melihat isi hasil JOIN, hitung dulu barisnya dan tanyakan: "
                  "angka ini masuk akal tidak?</strong></p>", "SATU KALIMAT"),
    "<p>JOIN yang benar hampir selalu menghasilkan jumlah baris yang <em>bisa kamu jelaskan "
    "asalnya</em>. Kalau tidak bisa kamu jelaskan, biasanya ada baris yang berlipat ganda.</p>",
    blok("catatan", "Ini pemeriksaan “tie-out” yang sudah kamu lakukan bertahun-tahun sebelum "
                    "menyerahkan kertas kerja, cuma dengan nama lain. Di Modul M10 kamu "
                    "menuliskannya sebagai <em>test</em> otomatis yang dijalankan dbt tiap kali "
                    "datanya diperbarui — bentuk yang sama, tapi tidak perlu kamu ingat lagi."))

langkah("Bahaya nomor satu: hitung omzetnya dulu, yang benar",
    blok("aksi", "Sel baru. Ini angka acuan yang benar — catat.", "LAKUKAN"),
    kode('''q("""SELECT SUM(i.jumlah*i.harga_saat_itu) AS omzet
     FROM pesanan o JOIN item i ON i.pesanan_id = o.id
     WHERE o.status='selesai'""")'''),
    blok("hasil", "<pre><code>      omzet\n0  35739000</code></pre>", "HARUS MUNCUL"),
    "<p>Rp 35.739.000. Kamu akan bertemu angka ini lagi di Hari 7, dari jalan yang sama sekali "
    "berbeda.</p>")

langkah("Sekarang tambahkan satu JOIN yang kelihatan tidak berbahaya",
    blok("aksi", "Sel baru. Kamu ingin ikut menampilkan data kunjungan, jadi kamu sambungkan "
                 "tabelnya. Perhitungan omzetnya tidak kamu sentuh sama sekali.", "LAKUKAN"),
    kode('''q("""SELECT SUM(i.jumlah*i.harga_saat_itu) AS omzet
     FROM pesanan o JOIN item i ON i.pesanan_id = o.id
     JOIN kunjungan k ON k.pelanggan_id = o.pelanggan_id
     WHERE o.status='selesai'""")'''),
    blok("hasil", "<pre><code>       omzet\n0  274456000</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "Rp 274.456.000. <strong>Tujuh setengah kali lipat</strong>, dari satu baris "
                   "yang kamu tambahkan tanpa menyentuh rumusnya. Dan tidak ada tulisan merah "
                   "sama sekali."))

langkah("Buktikan penyebabnya dengan menghitung baris",
    blok("aksi", "Sel baru. Query yang sama, tapi hitung barisnya.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris
     FROM pesanan o JOIN item i ON i.pesanan_id = o.id
     JOIN kunjungan k ON k.pelanggan_id = o.pelanggan_id
     WHERE o.status='selesai'""")'''),
    blok("hasil", "<pre><code>   baris\n0   5532</code></pre>", "HARUS MUNCUL"),
    "<p>5.532 baris, dari 788 baris item. Satu pelanggan punya belasan kunjungan, jadi tiap "
    "baris item digandakan sebanyak kunjungan pelanggannya. <strong>Jumlah barisnya sudah "
    "berteriak sebelum angka rupiahnya sempat berbohong</strong> — asal kamu menghitungnya.</p>")

langkah("Pilih jenis JOIN dari bunyi pertanyaannya",
    blok("aksi", "Salin tabel ini ke catatanmu.", "LAKUKAN"),
    tabel(["Pertanyaannya berbunyi", "Jenisnya"],
          [["“…pelanggan yang pernah memesan”", "<code>INNER JOIN</code>"],
           ["“semua pelanggan, berikut pesanannya kalau ada”", "<code>LEFT JOIN</code>"],
           ["“pelanggan yang belum pernah memesan”",
            "<code>LEFT JOIN</code> + <code>WHERE … IS NULL</code>, atau <code>NOT EXISTS</code>"],
           ["“apa saja yang tidak cocok di antara dua sistem”",
            "<code>FULL OUTER JOIN</code>, atau <code>EXCEPT</code> dua arah (Hari 7)"],
           ["“tiap cabang dipasangkan dengan tiap produk”",
            "<code>CROSS JOIN</code> — untuk membuat kerangka lengkap"]]),
    "<p><code>RIGHT JOIN</code> hampir tidak pernah perlu ditulis. <code>A RIGHT JOIN B</code> "
    "sama persis dengan <code>B LEFT JOIN A</code>, dan yang kedua jauh lebih mudah dibaca "
    "karena tabel utamanya disebut duluan. Kenali bentuknya supaya bisa membaca kode orang "
    "lain, lalu tulis sendiri selalu dengan <code>LEFT</code>.</p>")

langkah("CROSS JOIN terlihat tidak berguna sampai kamu butuh yang nol",
    blok("aksi", "Sel baru. Hitung berapa kombinasi cabang × produk yang benar-benar laku dalam "
                 "dua minggu pertama Januari.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris FROM (
       SELECT o.cabang, i.produk_id
       FROM pesanan o JOIN item i ON i.pesanan_id = o.id
       WHERE o.tanggal BETWEEN '2024-01-01' AND '2024-01-14'
       GROUP BY o.cabang, i.produk_id)""")'''),
    blok("hasil", "<pre><code>   baris\n0     20</code></pre>", "HARUS MUNCUL"),
    "<p>Dua puluh baris di layarmu. Tapi ada 3 cabang × 7 produk = <strong>21 kombinasi</strong>. Satu "
    "kombinasi hilang dari laporanmu — bukan tampil sebagai nol, tapi <em>tidak ada "
    "barisnya</em>.</p>")

langkah("Buat kerangkanya dulu, baru tempelkan datanya",
    blok("aksi", "Sel baru. <code>CROSS JOIN</code> membuat semua kombinasi lebih dulu.",
         "LAKUKAN"),
    kode('''q("""
WITH laku AS (
  SELECT o.cabang, i.produk_id, COUNT(*) AS n
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.tanggal BETWEEN '2024-01-01' AND '2024-01-14'
  GROUP BY o.cabang, i.produk_id)
SELECT c.cabang, p.nama, COALESCE(l.n, 0) AS terjual
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN produk p
LEFT JOIN laku l ON l.cabang = c.cabang AND l.produk_id = p.id
WHERE COALESCE(l.n, 0) = 0
""")'''),
    blok("hasil", "<pre><code>    cabang        nama  terjual\n"
                  "0  Seturan  Cheesecake        0</code></pre>", "HARUS MUNCUL"),
    "<p>Ketemu. Selama dua minggu itu Seturan <strong>tidak menjual satu pun Cheesecake</strong>. "
    "Tanpa kerangka, temuan itu tidak punya baris untuk ditempati — dan yang tidak punya baris "
    "tidak akan pernah ditanyakan siapa pun.</p>",
    blok("catatan", "Ini pola yang sama seperti membuat lead schedule kosong lebih dulu, lalu "
                    "mengisinya dari buku besar. Yang tetap kosong justru yang paling menarik."))

HARI4 = {
  "n": "HARI 4", "tab": "4",
  "judul": "Lima jenis JOIN, dan cara membuktikan mana yang benar",
  "waktu": "± 60 menit",
  "tujuan": "memilih jenis JOIN dari bunyi pertanyaannya, dan memeriksa hasilnya lewat jumlah "
            "baris — bukan lewat perasaan.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> hitung jumlah baris tiap JOIN dan jelaskan asal "
           "angkanya sebelum melihat isinya · <code>LEFT</code> = inner + yang yatim di kiri · "
           "<code>FULL</code> = inner + yatim kiri + yatim kanan · tulis <code>LEFT</code>, "
           "jangan <code>RIGHT</code> · <code>CROSS JOIN</code> membuat kerangka supaya yang "
           "bernilai nol tetap punya baris.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 4 dari 8.</strong> Jawab dengan "
           "suara: <em>tabel A punya 100 baris, tabel B punya 250 baris. "
           "<code>A LEFT JOIN B</code> menghasilkan 260 baris. Apa artinya?</em></p>"
           "<details><summary>Kunci</summary><p>260 &gt; 100, jadi ada baris kiri yang "
           "berpasangan dengan lebih dari satu baris kanan — kuncinya di B tidak unik. Kalau "
           "kamu menjumlahkan nilai setelah JOIN ini, angkanya berlipat, persis seperti omzet "
           "Rp 274 juta tadi.</p></details>",
}
