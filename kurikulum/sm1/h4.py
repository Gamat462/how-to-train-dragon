# -*- coding: utf-8 -*-
"""Hari 4 — lima jenis JOIN dan jumlah baris sebagai alat pemeriksa (PostgreSQL)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Layar merah yang akan paling sering kamu temui",
    blok("aksi", "Berkas <code>senja/hari-4.sql</code>. Dua tabel, dua kolom bernama sama.",
         "LAKUKAN"),
    kode("SELECT id FROM pelanggan p\nJOIN pesanan o ON o.pelanggan_id = p.id;"),
    keluaran(H, "h4_merah_ambigu"),
    blok("catatan", "<code>pelanggan</code> punya <code>id</code>, <code>pesanan</code> juga. "
                    "PostgreSQL tidak mau menebak yang mana yang kamu maksud — dan itu bagus. "
                    "Tulis <code>p.id</code> atau <code>o.id</code>, jangan <code>id</code> saja."),
    "<p><strong>Setiap kali layarmu merah karena ini</strong>, obatnya selalu sama: beri awalan "
    "alias ke kolomnya.</p>")

langkah("JOIN pertama: hanya yang cocok di kedua sisi",
    blok("aksi", "Hitung barisnya, jangan lihat isinya dulu.", "LAKUKAN"),
    kode("SELECT count(*) AS baris\nFROM pelanggan p JOIN pesanan o ON o.pelanggan_id = p.id;"),
    keluaran(H, "h4_inner"),
    "<p>388 dari 400 pesanan. <code>JOIN</code> polos yang kamu tulis itu sama dengan "
    "<code>INNER JOIN</code> — hanya pasangan yang cocok di kedua sisi yang lolos.</p>")

langkah("LEFT JOIN: semua yang di kiri tetap ada",
    blok("aksi", "Ganti satu kata.", "LAKUKAN"),
    kode("SELECT count(*) AS baris\nFROM pelanggan p LEFT JOIN pesanan o ON o.pelanggan_id = p.id;"),
    keluaran(H, "h4_left"),
    "<p>391 = 388 + 3. Tiga tambahan itu <strong>Andi, Bagus, dan Vira</strong> dari kemarin — "
    "pelanggan yang tidak punya pesanan tetap muncul, dengan kolom kanan berisi "
    "<code>NULL</code>.</p>")

langkah("RIGHT JOIN: semua yang di kanan tetap ada",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("SELECT count(*) AS baris\nFROM pelanggan p RIGHT JOIN pesanan o ON o.pelanggan_id = p.id;"),
    keluaran(H, "h4_right"),
    "<p>400 = 388 + 12. Dua belas tambahan itu pesanan tamu yang <code>pelanggan_id</code>-nya "
    "<code>NULL</code>. Hasilnya <strong>seluruh 400 pesanan</strong>.</p>")

langkah("FULL OUTER JOIN: semua dari dua sisi",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("SELECT count(*) AS baris\nFROM pelanggan p FULL OUTER JOIN pesanan o ON o.pelanggan_id = p.id;"),
    keluaran(H, "h4_full"),
    "<p>403 = 388 + 3 + 12. Tidak ada yang tertinggal dari sisi mana pun, dan kamu bisa "
    "menjelaskan tiap sukunya.</p>",
    blok("catatan", "PostgreSQL mendukung kelima JOIN sejak lama. <strong>MySQL tidak punya "
                    "<code>FULL OUTER JOIN</code> sama sekali</strong> dan harus ditiru dengan "
                    "<code>UNION</code> — perbedaan dialek yang membuat query “yang tadi jalan” "
                    "tiba-tiba gagal di tempat kerja baru."))

langkah("CROSS JOIN: semua kombinasi, tanpa syarat",
    blok("aksi", "Perhatikan: tidak ada <code>ON</code>.", "LAKUKAN"),
    kode("SELECT count(*) AS baris FROM pelanggan CROSS JOIN produk;"),
    keluaran(H, "h4_cross"),
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
    blok("aksi", "Ini angka acuan yang benar — catat.", "LAKUKAN"),
    kode('''SELECT sum(i.jumlah * i.harga_saat_itu) AS omzet
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai';'''),
    keluaran(H, "h4_omzet"),
    "<p>Rp 35.739.000. Kamu akan bertemu angka ini lagi di Hari 7, dari jalan yang sama sekali "
    "berbeda.</p>")

langkah("Sekarang tambahkan satu JOIN yang kelihatan tidak berbahaya",
    blok("aksi", "Kamu ingin ikut menampilkan data kunjungan, jadi kamu sambungkan tabelnya. "
                 "Perhitungan omzetnya tidak kamu sentuh sama sekali.", "LAKUKAN"),
    kode('''SELECT sum(i.jumlah * i.harga_saat_itu) AS omzet
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
JOIN kunjungan k ON k.pelanggan_id = o.pelanggan_id
WHERE o.status = 'selesai';'''),
    keluaran(H, "h4_omzet_lipat"),
    blok("bahaya", "Rp 274.456.000. <strong>Tujuh setengah kali lipat</strong>, dari satu baris "
                   "yang kamu tambahkan tanpa menyentuh rumusnya. Dan tidak ada tulisan merah "
                   "sama sekali."))

langkah("Buktikan penyebabnya dengan menghitung baris",
    blok("aksi", "Query yang sama, tapi hitung barisnya.", "LAKUKAN"),
    kode('''SELECT count(*) AS baris
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
JOIN kunjungan k ON k.pelanggan_id = o.pelanggan_id
WHERE o.status = 'selesai';'''),
    keluaran(H, "h4_baris_lipat"),
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
    blok("aksi", "Hitung berapa kombinasi cabang × produk yang benar-benar laku dalam dua "
                 "minggu pertama Januari.", "LAKUKAN"),
    kode('''SELECT count(*) AS baris FROM (
  SELECT o.cabang, i.produk_id
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-14'
  GROUP BY o.cabang, i.produk_id) x;'''),
    keluaran(H, "h4_tanpa_kerangka"),
    "<p>Dua puluh baris di layarmu. Tapi ada 3 cabang × 7 produk = <strong>21 "
    "kombinasi</strong>. Satu kombinasi hilang dari laporanmu — bukan tampil sebagai nol, tapi "
    "<em>tidak ada barisnya</em>.</p>",
    blok("catatan", "<code>DATE '2024-01-01'</code> itu cara PostgreSQL menulis tanggal secara "
                    "tegas. Kolom <code>tanggal</code> di sini bertipe <code>date</code>, bukan "
                    "teks — jadi <code>BETWEEN</code> membandingkan tanggal sungguhan, bukan "
                    "urutan huruf."))

langkah("Buat kerangkanya dulu, baru tempelkan datanya",
    blok("aksi", "<code>CROSS JOIN</code> membuat semua kombinasi lebih dulu.", "LAKUKAN"),
    kode('''WITH laku AS (
  SELECT o.cabang, i.produk_id, count(*) AS n
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-14'
  GROUP BY o.cabang, i.produk_id)
SELECT c.cabang, p.nama, COALESCE(l.n, 0) AS terjual
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN produk p
LEFT JOIN laku l ON l.cabang = c.cabang AND l.produk_id = p.id
WHERE COALESCE(l.n, 0) = 0;'''),
    keluaran(H, "h4_kerangka_nol"),
    "<p>Ketemu. Selama dua minggu itu Seturan <strong>tidak menjual satu pun "
    "Cheesecake</strong>. Tanpa kerangka, temuan itu tidak punya baris untuk ditempati — dan "
    "yang tidak punya baris tidak akan pernah ditanyakan siapa pun.</p>",
    blok("catatan", "Ini pola yang sama seperti membuat lead schedule kosong lebih dulu, lalu "
                    "mengisinya dari buku besar. Yang tetap kosong justru yang paling menarik."))

langkah("Masalah yang sama, bentuk lain: hari yang tidak ada",
    blok("aksi", "Hitung penjualan harian minggu pertama Januari.", "LAKUKAN"),
    kode('''SELECT o.tanggal, sum(i.jumlah * i.harga_saat_itu) AS nilai
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-07'
GROUP BY o.tanggal ORDER BY o.tanggal;'''),
    keluaran(H, "h7_tanpa_kerangka_harian"),
    "<p>Lima baris untuk tujuh hari. <strong>2 dan 7 Januari tidak muncul sama sekali</strong> — "
    "bukan muncul sebagai nol. <code>GROUP BY</code> hanya bisa mengelompokkan baris yang ada.</p>")

langkah("generate_series: membuat hari yang tidak ada",
    blok("aksi", "PostgreSQL bisa membuat deret tanggal sendiri. Jalankan.", "LAKUKAN"),
    kode('''SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
FROM generate_series(DATE '2024-01-01', DATE '2024-01-07', INTERVAL '1 day') AS d
LEFT JOIN pesanan o ON o.tanggal = d::date AND o.status = 'selesai'
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY d ORDER BY d;'''),
    keluaran(H, "h7_gen_series"),
    "<p>Tujuh baris untuk tujuh hari. 2 dan 7 Januari muncul sebagai <strong>nol</strong>, bukan "
    "hilang. Tanpa kerangka ini kamu akan mendapat lima baris dan tidak pernah tahu dua hari itu "
    "ada.</p>",
    blok("catatan", "<code>generate_series</code> adalah salah satu alasan orang menyukai "
                    "PostgreSQL. Di SQLite kamu harus menulis recursive CTE untuk hal yang sama; "
                    "di sini satu baris cukup."))

langkah("Satu kata di tempat yang salah, dan kerangkanya runtuh",
    blok("aksi", "Pindahkan <code>o.status = 'selesai'</code> dari <code>ON</code> ke "
                 "<code>WHERE</code>, lalu hitung barisnya.", "LAKUKAN"),
    kode('''SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
FROM generate_series(DATE '2024-01-01', DATE '2024-01-07', INTERVAL '1 day') AS d
LEFT JOIN pesanan o ON o.tanggal = d::date
LEFT JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai'
GROUP BY d ORDER BY d;'''),
    keluaran(H, "h7_gen_series_rusak"),
    blok("bahaya", "Dari 7 baris turun jadi <strong>5</strong>. Dua hari nol lenyap, dan "
                   "<strong>tidak ada pesan apa pun</strong>. Syarat di <code>WHERE</code> "
                   "dijalankan <em>setelah</em> JOIN, jadi baris kiri yang tidak punya pasangan "
                   "(nilainya <code>NULL</code>) ikut terbuang — <code>LEFT JOIN</code>-mu "
                   "berubah jadi <code>INNER JOIN</code>."),
    "<p>Ini salah satu bug JOIN paling umum di dunia, dan sekarang kamu bisa mengenalinya dari "
    "<strong>jumlah baris</strong> — persis kebiasaan yang kamu bangun di langkah 7 dan 11 tadi.</p>")

langkah("Akibatnya pada angka yang kamu laporkan",
    blok("aksi", "Dua rata-rata dari data yang sama.", "LAKUKAN"),
    kode('''WITH lengkap AS (
  SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
  FROM generate_series(DATE '2024-01-01', DATE '2024-01-07', INTERVAL '1 day') AS d
  LEFT JOIN pesanan o ON o.tanggal = d::date AND o.status = 'selesai'
  LEFT JOIN item i ON i.pesanan_id = o.id
  GROUP BY d)
SELECT round(avg(nilai))                          AS rata2_7_hari_kalender,
       round(avg(nilai) FILTER (WHERE nilai > 0)) AS rata2_hari_ada_transaksi
FROM lengkap;'''),
    keluaran(H, "h7_rata2_dua_cara"),
    "<p>Rp 240.714 lawan Rp 337.000 — <strong>selisih 40%</strong>, dari satu keputusan tentang "
    "hari kosong. Dan seperti biasa, tidak ada yang salah dari keduanya; yang salah adalah tidak "
    "menyebutkan yang mana.</p>")

HARI4 = {
  "n": "HARI 4", "tab": "4",
  "judul": "Lima jenis JOIN, dan kerangka yang membuat nol tetap terlihat",
  "waktu": "± 70 menit",
  "tujuan": "memilih jenis JOIN dari bunyi pertanyaannya, memeriksa hasilnya lewat jumlah "
            "baris, dan membuat kerangka supaya baris bernilai nol tetap punya tempat.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> hitung jumlah baris tiap JOIN dan jelaskan asal "
           "angkanya sebelum melihat isinya · <code>LEFT</code> = inner + yang yatim di kiri · "
           "<code>FULL</code> = inner + yatim kiri + yatim kanan · tulis <code>LEFT</code>, "
           "jangan <code>RIGHT</code> · <code>CROSS JOIN</code> dan "
           "<code>generate_series</code> membuat kerangka supaya yang bernilai nol tetap "
           "punya baris · dan syarat tambahan di <code>LEFT JOIN</code> ditaruh di "
           "<code>ON</code>, bukan <code>WHERE</code>.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 4 dari 8.</strong> Jawab dengan "
           "suara: <em>tabel A punya 100 baris, tabel B punya 250 baris. "
           "<code>A LEFT JOIN B</code> menghasilkan 260 baris. Apa artinya?</em></p>"
           "<details><summary>Kunci</summary><p>260 &gt; 100, jadi ada baris kiri yang "
           "berpasangan dengan lebih dari satu baris kanan — kuncinya di B tidak unik. Kalau "
           "kamu menjumlahkan nilai setelah JOIN ini, angkanya berlipat, persis seperti omzet "
           "Rp 274 juta tadi.</p></details>",
}
