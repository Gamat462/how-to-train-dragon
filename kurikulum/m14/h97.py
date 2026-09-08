# -*- coding: utf-8 -*-
"""Hari 97 — soal SQL wawancara, dikerjakan sungguhan.
Semua keluaran di kotak HARUS MUNCUL diperoleh dengan menjalankan querynya di
DuckDB 1.5.5 pada basis data wawancara.duckdb yang dibuat buat_soal_sql.py."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Siapkan basis data latihannya",
    blok("aksi", "Salin <code>data-dan-skrip/minggu-14/buat_soal_sql.py</code> dari paket zip. "
                 "Pasang DuckDB, lalu jalankan.", "LAKUKAN"),
    kode("pip install duckdb\npython buat_soal_sql.py"),
    blok("hasil", kode("""pengguna: 120
pesanan : 346
pengguna tanpa pesanan: 14""", salin=False), "HARUS MUNCUL"),
    "<p>Berkas <code>wawancara.duckdb</code> muncul. Isinya dua tabel — "
    "<code>pengguna(id, nama, tanggal_daftar, kota)</code> dan "
    "<code>pesanan(id, user_id, tanggal, nilai)</code> — bentuk yang paling sering dipakai "
    "soal wawancara.</p>",
    blok("catatan", "<strong>Kenapa DuckDB, bukan BigQuery:</strong> ia berjalan di berkas lokal, "
                    "tanpa akun dan tanpa biaya, dan sintaksnya sangat dekat dengan Postgres dan "
                    "BigQuery. Yang kamu latih di sini terpakai apa adanya di wawancara."))

langkah("Siapkan cara menjalankan query",
    blok("aksi", "Salin juga <code>jalankan.py</code> dari folder yang sama. Lalu buat berkas "
                 "<code>query.sql</code> berisi satu baris ini, simpan, dan jalankan.", "LAKUKAN"),
    kode("SELECT COUNT(*) AS pesanan, MIN(tanggal) AS awal, MAX(tanggal) AS akhir FROM pesanan;"),
    kode("python jalankan.py"),
    blok("hasil", kode("""┌─────────┬────────────┬────────────┐
│ pesanan │    awal    │   akhir    │
│  int64  │    date    │    date    │
├─────────┼────────────┼────────────┤
│     346 │ 2025-10-05 │ 2026-06-30 │
└─────────┴────────────┴────────────┘""", salin=False), "HARUS MUNCUL"),
    "<p><strong>Alur kerjamu sepanjang hari ini:</strong> tulis SQL di <code>query.sql</code> → "
    "simpan → <code>python jalankan.py</code> → bandingkan dengan kotak HARUS MUNCUL. Sama seperti "
    "papan tulis di wawancara, cuma ada tombol jalankan.</p>",
    blok("catatan", "<strong>Selalu lakukan ini lebih dulu di wawancara sungguhan.</strong> "
                    "Sebelum menjawab, tanyakan atau periksa rentang datanya. Kandidat yang "
                    "menulis <code>WHERE tanggal >= '2026-01-01'</code> pada data yang mulai "
                    "Oktober 2025 menjawab pertanyaan yang berbeda dari yang ditanyakan."))

langkah("SOAL 1 — pelanggan yang hilang. Kerjakan dulu, jangan buka jawabannya",
    blok("aksi", "<strong>Cari pelanggan yang belanja di Maret 2026 tapi tidak di April 2026.</strong> "
                 "Beri dirimu 10 menit. Tulis sendiri, jalankan sendiri.", "LAKUKAN"),
    "<p>Tiga langkah berikut memandumu <em>tanpa</em> memberi jawabannya. Kerjakan dulu; kalau "
    "macet, ikuti langkah-langkah itu.</p>",
    blok("catatan", "<strong>Di wawancara sungguhan, ucapkan ini keras-keras sebelum mengetik:</strong> "
                    "<em>\"Saya akan ambil pembeli Maret, ambil pembeli April, lalu cari yang ada di "
                    "daftar pertama tapi tidak di kedua.\"</em> Pewawancara menilai rencananya, "
                    "bukan cuma hasilnya."))

langkah("Bangun jawaban Soal 1 selapis demi selapis",
    blok("aksi", "Jalankan yang paling sederhana dulu — jangan langsung menulis query akhir.", "LAKUKAN"),
    kode("""SELECT COUNT(DISTINCT user_id) AS pembeli_maret FROM pesanan
WHERE tanggal >= DATE '2026-03-01' AND tanggal < DATE '2026-04-01';"""),
    blok("hasil", kode("""┌───────────────┐
│ pembeli_maret │
│     int64     │
├───────────────┤
│            38 │
└───────────────┘""", salin=False), "HARUS MUNCUL"),
    "<p>38 orang belanja di Maret. Ganti tanggalnya ke April dan kamu dapat <strong>39</strong>. "
    "Dua angka ini yang membatasi jawaban akhirmu — hasilnya tidak mungkin lebih dari 38.</p>",
    blok("catatan", "<strong>Perhatikan <code>&lt; DATE '2026-04-01'</code>, bukan "
                    "<code>&lt;= '2026-03-31'</code>.</strong> Kalau kolomnya suatu hari berubah "
                    "jadi bertipe waktu, versi kedua diam-diam membuang seluruh transaksi tanggal "
                    "31 setelah pukul 00:00."))

langkah("Sambungkan keduanya dan lihat NULL-nya",
    blok("aksi", "Jalankan ini, lalu perhatikan kolom kanan.", "LAKUKAN"),
    kode("""SELECT m.user_id, a.user_id AS user_april
FROM (SELECT DISTINCT user_id FROM pesanan
      WHERE tanggal >= DATE '2026-03-01' AND tanggal < DATE '2026-04-01') m
LEFT JOIN (SELECT DISTINCT user_id FROM pesanan
      WHERE tanggal >= DATE '2026-04-01' AND tanggal < DATE '2026-05-01') a
  ON a.user_id = m.user_id
ORDER BY m.user_id LIMIT 6;"""),
    blok("hasil", kode("""┌─────────┬────────────┐
│ user_id │ user_april │
│  int32  │   int32    │
├─────────┼────────────┤
│       6 │       NULL │
│      10 │       NULL │
│      11 │         11 │
│      13 │       NULL │
│      16 │       NULL │
│      20 │       NULL │
└─────────┴────────────┘""", salin=False), "HARUS MUNCUL"),
    "<p><strong>NULL di kolom kanan artinya \"tidak ketemu di April\".</strong> Itulah seluruh isi "
    "pola <em>anti-join</em>: LEFT JOIN dulu supaya yang tidak berpasangan tetap muncul, lalu "
    "saring yang kanannya kosong.</p>")

langkah("Saring, dan Soal 1 selesai",
    blok("aksi", "Tambahkan satu baris <code>WHERE</code> pada query tadi.", "LAKUKAN"),
    kode("WHERE a.user_id IS NULL"),
    blok("hasil", kode("""┌────────┐
│ hilang │
│ int64  │
├────────┤
│     24 │
└────────┘""", salin=False), "HARUS MUNCUL (kalau dibungkus COUNT)"),
    "<p><strong>24 pelanggan hilang dari 38 pembeli Maret.</strong> Angkanya masuk akal: lebih "
    "kecil dari 38, seperti yang kamu perkirakan di langkah 4.</p>",
    blok("catatan", "<strong>Kebiasaan yang membedakan kandidat:</strong> setelah dapat angka, "
                    "ucapkan apakah ia masuk akal. \"24 dari 38, sekitar 63% tidak kembali — itu "
                    "tinggi, saya akan cek apakah April memang bulan sepi.\" Itu bunyi analis, "
                    "bukan bunyi orang yang menghafal sintaks."))

langkah("Jebakan NOT IN — buktikan sendiri, jangan percaya",
    blok("aksi", "Banyak orang menjawab Soal 1 dengan <code>NOT IN</code>. Jalankan ini untuk "
                 "melihat kenapa itu berbahaya.", "LAKUKAN"),
    kode("""SELECT 'NOT IN' AS cara, COUNT(*) AS hasil
FROM (VALUES (1),(2),(3)) t(x) WHERE x NOT IN (SELECT * FROM (VALUES (2),(NULL)) s(y))
UNION ALL
SELECT 'NOT EXISTS', COUNT(*)
FROM (VALUES (1),(2),(3)) t(x)
WHERE NOT EXISTS (SELECT 1 FROM (VALUES (2),(NULL)) s(y) WHERE s.y = t.x);"""),
    blok("hasil", kode("""┌────────────┬───────┐
│    cara    │ hasil │
│  varchar   │ int64 │
├────────────┼───────┤
│ NOT IN     │     0 │
│ NOT EXISTS │     2 │
└────────────┴───────┘""", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Jawaban yang benar adalah 2, dan <code>NOT IN</code> memberi 0 — "
                   "tanpa satu pun peringatan.</strong> Satu NULL di dalam subquery membuat "
                   "seluruh hasil kosong, karena <code>x NOT IN (2, NULL)</code> tidak pernah "
                   "bisa dipastikan benar. Ini bug diam yang membuat laporan kosong dan tidak "
                   "ada yang tahu kenapa."),
    "<p>Menyebutkan ini di wawancara — sambil menunjukkan angkanya — adalah nilai tambah yang "
    "jarang diberikan pelamar junior.</p>")

langkah("SOAL 2 — tiga pelanggan terbesar tiap kota",
    blok("aksi", "<strong>Untuk tiap kota, cari 3 pelanggan dengan total belanja terbesar.</strong> "
                 "Kerjakan sendiri dulu. Kalau macet, mulai dari yang paling sederhana:</p>", "LAKUKAN"),
    kode("""SELECT u.kota, u.nama, SUM(p.nilai) AS belanja
FROM pesanan p JOIN pengguna u ON p.user_id = u.id
GROUP BY u.kota, u.nama
ORDER BY belanja DESC LIMIT 5;"""),
    blok("hasil", kode("""┌──────────┬─────────────────┬─────────┐
│   kota   │      nama       │ belanja │
│ varchar  │     varchar     │ int128  │
├──────────┼─────────────────┼─────────┤
│ Jakarta  │ Farhan Ramadhan │ 7566000 │
│ Surabaya │ Jihan Pratama   │ 4916000 │
│ Surabaya │ Gita Saputra    │ 4652000 │
│ Surabaya │ Citra Saputra   │ 4401000 │
│ Surabaya │ Bella Pratama   │ 4177000 │
└──────────┴─────────────────┴─────────┘""", salin=False), "HARUS MUNCUL"),
    "<p>Perhatikan masalahnya: <code>LIMIT 5</code> mengambil lima teratas <em>keseluruhan</em>, "
    "empat di antaranya dari Surabaya. Yang diminta tiga teratas <strong>per kota</strong>. "
    "Itulah yang tidak bisa dilakukan <code>LIMIT</code>.</p>")

langkah("Beri nomor urut di dalam tiap kota",
    blok("aksi", "Bungkus query tadi sebagai CTE, lalu tambahkan satu kolom.", "LAKUKAN"),
    kode("ROW_NUMBER() OVER (PARTITION BY kota ORDER BY belanja DESC) AS rn"),
    blok("hasil", kode("""┌─────────┬────────────────┬─────────┬───────┐
│  kota   │      nama      │ belanja │  rn   │
│ varchar │    varchar     │ int128  │ int64 │
├─────────┼────────────────┼─────────┼───────┤
│ Bandung │ Hana Ramadhan  │ 3661000 │     1 │
│ Bandung │ Andi Ramadhan  │ 3633000 │     2 │
│ Bandung │ Naufal Pratama │ 3621000 │     3 │
│ Bandung │ Gita Ramadhan  │ 3520000 │     4 │
│ Bandung │ Irfan Wijaya   │ 3419000 │     5 │
└─────────┴────────────────┴─────────┴───────┘""", salin=False), "HARUS MUNCUL"),
    "<p>Nomornya mulai ulang dari 1 di tiap kota — itulah arti <code>PARTITION BY</code>. "
    "Sekarang saring dengan <code>WHERE rn &lt;= 3</code> di lapisan berikutnya, dan Soal 2 "
    "selesai: 12 baris, tiga per kota.</p>",
    blok("bahaya", "<strong><code>WHERE rn &lt;= 3</code> tidak bisa ditaruh di query yang sama.</strong> "
                   "Fungsi jendela dihitung <em>setelah</em> <code>WHERE</code>, jadi kolomnya "
                   "belum ada saat penyaringan berjalan. Harus dibungkus jadi CTE kedua. Ini "
                   "kesalahan yang hampir semua orang buat sekali seumur hidup."),
    blok("catatan", "<strong>Pertanyaan lanjutan yang hampir pasti datang:</strong> \"bagaimana "
                    "kalau ada nilai seri di posisi ketiga?\" Jawab: <code>ROW_NUMBER</code> "
                    "memilih sembarang satu, <code>RANK</code> menyertakan semua yang seri. Lalu "
                    "tanyakan balik: <em>\"yang diinginkan bisnisnya yang mana?\"</em> — itu "
                    "jawaban terbaiknya."))

langkah("SOAL 3 — retensi, dan satu kata yang mengubah hasilnya jadi 100%",
    blok("aksi", "<strong>Dari pelanggan yang mendaftar tiap bulan, berapa persen yang belanja "
                 "lagi di bulan berikutnya?</strong> Kerjakan dulu, lalu jalankan versi ini.", "LAKUKAN"),
    kode("""WITH kohor AS (
  SELECT id AS user_id, DATE_TRUNC('month', tanggal_daftar) AS bulan_daftar FROM pengguna
), aktif AS (
  SELECT DISTINCT user_id, DATE_TRUNC('month', tanggal) AS bulan_aktif FROM pesanan
)
SELECT k.bulan_daftar, COUNT(DISTINCT k.user_id) AS ukuran_kohor,
       COUNT(DISTINCT a.user_id) AS kembali,
       ROUND(100.0*COUNT(DISTINCT a.user_id)/COUNT(DISTINCT k.user_id),1) AS retensi
FROM kohor k
LEFT JOIN aktif a ON a.user_id = k.user_id
     AND a.bulan_aktif = k.bulan_daftar + INTERVAL 1 MONTH
GROUP BY k.bulan_daftar ORDER BY k.bulan_daftar;"""),
    blok("hasil", kode("""┌─────────────────────┬──────────────┬─────────┬─────────┐
│    bulan_daftar     │ ukuran_kohor │ kembali │ retensi │
│      timestamp      │    int64     │  int64  │ double  │
├─────────────────────┼──────────────┼─────────┼─────────┤
│ 2025-10-01 00:00:00 │           25 │       7 │    28.0 │
│ 2025-11-01 00:00:00 │           26 │      11 │    42.3 │
│ 2025-12-01 00:00:00 │           23 │       3 │    13.0 │
│ 2026-01-01 00:00:00 │           23 │       9 │    39.1 │
│ 2026-02-01 00:00:00 │           23 │      11 │    47.8 │
└─────────────────────┴──────────────┴─────────┴─────────┘""", salin=False), "HARUS MUNCUL"),
    "<p>Retensi bulan pertama antara 13% dan 48%. Kohor Desember paling buruk — angka seperti "
    "itulah yang jadi temuan di laporanmu.</p>")

langkah("Ganti satu kata, dan lihat kebohongannya",
    blok("aksi", "Ubah <code>LEFT JOIN</code> jadi <code>INNER JOIN</code>. Ganti satu kata saja, "
                 "jalankan lagi.", "LAKUKAN"),
    kode("INNER JOIN aktif a ON a.user_id = k.user_id"),
    blok("hasil", kode("""┌─────────────────────┬──────────────┬─────────┬─────────┐
│    bulan_daftar     │ ukuran_kohor │ kembali │ retensi │
│      timestamp      │    int64     │  int64  │ double  │
├─────────────────────┼──────────────┼─────────┼─────────┤
│ 2025-10-01 00:00:00 │            7 │       7 │   100.0 │
│ 2025-11-01 00:00:00 │           11 │      11 │   100.0 │
│ 2025-12-01 00:00:00 │            3 │       3 │   100.0 │
│ 2026-01-01 00:00:00 │            9 │       9 │   100.0 │
│ 2026-02-01 00:00:00 │           11 │      11 │   100.0 │
└─────────────────────┴──────────────┴─────────┴─────────┘""", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Retensi 100% di setiap kohor.</strong> INNER JOIN membuang pelanggan "
                   "yang tidak kembali — sehingga penyebutnya ikut menyusut, dan yang tersisa "
                   "cuma orang yang kembali. Kolom <code>ukuran_kohor</code> berubah dari 25 jadi "
                   "7 tanpa ada yang memberitahu."),
    "<p><strong>Ini bukan sekadar \"hasilnya agak lebih baik\" — hasilnya mustahil, dan tetap "
    "terlihat rapi.</strong> Sebutkan alasan ini keras-keras saat menulis LEFT JOIN di wawancara; "
    "itu satu kalimat yang menunjukkan kamu tahu apa yang kamu hindari.</p>")

langkah("SOAL 4 — jeda antar pesanan, dan NULL yang wajib disaring",
    blok("aksi", "<strong>Hitung rata-rata selisih hari antara dua pesanan berturut-turut tiap "
                 "pelanggan.</strong> Kerjakan dulu. Lalu lihat bentuk mentahnya untuk satu orang.", "LAKUKAN"),
    kode("""SELECT user_id, tanggal,
       LAG(tanggal) OVER (PARTITION BY user_id ORDER BY tanggal) AS sebelumnya
FROM pesanan WHERE user_id = 24 ORDER BY tanggal;"""),
    blok("hasil", kode("""┌─────────┬────────────┬────────────┐
│ user_id │  tanggal   │ sebelumnya │
│  int32  │    date    │    date    │
├─────────┼────────────┼────────────┤
│      24 │ 2026-04-19 │ NULL       │
│      24 │ 2026-04-21 │ 2026-04-19 │
│      24 │ 2026-05-05 │ 2026-04-21 │
│      24 │ 2026-05-07 │ 2026-05-05 │
│      24 │ 2026-05-31 │ 2026-05-07 │
│      24 │ 2026-06-15 │ 2026-05-31 │
│      24 │ 2026-06-19 │ 2026-06-15 │
└─────────┴────────────┴────────────┘""", salin=False), "HARUS MUNCUL"),
    "<p><strong>Baris pertama tiap pelanggan selalu NULL</strong> — tidak ada pesanan sebelumnya. "
    "Tujuh pesanan menghasilkan enam jeda, bukan tujuh.</p>")

langkah("Hitung berapa NULL yang harus dibuang",
    blok("aksi", "Jalankan ini untuk seluruh tabel sebelum menghitung rata-rata.", "LAKUKAN"),
    kode("""WITH jeda AS (
  SELECT user_id, tanggal - LAG(tanggal) OVER (PARTITION BY user_id ORDER BY tanggal) AS d
  FROM pesanan
)
SELECT COUNT(*) AS semua, COUNT(d) AS ada_isinya, COUNT(*) - COUNT(d) AS null_nya FROM jeda;"""),
    blok("hasil", kode("""┌───────┬────────────┬──────────┐
│ semua │ ada_isinya │ null_nya │
│ int64 │   int64    │  int64   │
├───────┼────────────┼──────────┤
│   346 │        240 │      106 │
└───────┴────────────┴──────────┘""", salin=False), "HARUS MUNCUL"),
    "<p><strong>106 dari 346 baris kosong</strong> — itu 106 pelanggan yang punya pesanan. "
    "Tambahkan <code>WHERE d IS NOT NULL</code> sebelum <code>AVG(d)</code>, dan Soal 4 selesai.</p>",
    blok("catatan", "<strong>Sebenarnya <code>AVG</code> di SQL sudah mengabaikan NULL,</strong> "
                    "jadi rata-ratanya kebetulan benar. Yang salah adalah kalau kamu memakai "
                    "<code>COUNT(*)</code> sebagai jumlah jeda, atau menghitung sendiri "
                    "<code>SUM(d)/COUNT(*)</code> — di situ 106 baris kosong ikut jadi penyebut. "
                    "Menyebut hal ini di wawancara jauh lebih berkesan daripada sekadar menulis "
                    "<code>IS NOT NULL</code>."))

langkah("Lima langkah mengerjakan soal SQL di depan orang",
    blok("aksi", "Baca lima langkah ini, lalu kerjakan ulang Soal 1 sambil "
                 "<strong>mengucapkan tiap langkahnya keras-keras</strong>.", "LAKUKAN"),
    tabel(["Langkah", "Yang kamu ucapkan", "Yang dinilai"],
          [["1", "ulangi soalnya dengan kalimatmu sendiri", "menangkap salah paham sebelum menulis 20 baris salah"],
           ["2", "tanyakan yang ambigu", "pesanan batal dihitung? zona waktu? kalau seri?"],
           ["3", "ucapkan rencana sebelum mengetik", "\"kumpulkan per pelanggan, beri peringkat, saring\""],
           ["4", "tulis bertahap, tunjukkan hasil tiap lapis", "cara kerja yang bisa dipercaya, bukan tebakan besar"],
           ["5", "periksa kasus khusus di akhir", "NULL, nilai seri, pembagian nol"]]),
    blok("catatan", "<strong>Kandidat yang langsung mengetik dalam diam sering kalah</strong> dari "
                    "kandidat yang berpikir keras walau jawabannya sedikit lebih lambat. Yang "
                    "dinilai adalah apakah kamu bisa diajak bekerja, dan itu cuma terlihat kalau "
                    "kamu bersuara."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini dan tutup terminalmu. Buka lagi, dan kerjakan keempat soal "
                 "dari nol tanpa melihat apa pun.", "LAKUKAN"),
    "<p>Empat pola yang harus keluar dari ingatan: <strong>anti-join</strong> (LEFT JOIN + "
    "IS NULL) · <strong>peringkat per kelompok</strong> (ROW_NUMBER + PARTITION BY, disaring di "
    "CTE kedua) · <strong>retensi</strong> (LEFT JOIN wajib) · <strong>jeda</strong> (LAG + "
    "kesadaran baris pertama NULL).</p>",
    blok("catatan", "<strong>Angkanya juga harus cocok:</strong> 24 · 12 baris · retensi "
                    "13–48% · 106 baris NULL. Kalau angkamu beda, querymu beda — dan itu "
                    "informasi, bukan kegagalan."))

HARI97 = {
  "n": "HARI 97",
  "tab": "97",
  "judul": "Empat soal SQL wawancara — dijalankan, bukan dibaca",
  "waktu": "± 75 menit",
  "tujuan": "mengerjakan empat pola SQL yang paling sering diuji di wawancara pada basis data "
            "sungguhan, dan membuktikan sendiri dua bug diam yang menjatuhkan kandidat.",
  "langkah": L,
  "tutup_judul": "Hari 97 selesai.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> anti-join = LEFT JOIN + <code>IS NULL</code> · "
           "<code>NOT IN</code> + NULL = hasil kosong diam-diam · <code>WHERE rn &lt;= 3</code> "
           "harus di CTE terpisah · retensi dengan INNER JOIN = 100% palsu · LAG menghasilkan "
           "NULL di baris pertama tiap partisi.</p>"
           "<p style=\"margin-top:8px\">Basis datanya jangan dihapus. Besok dipakai lagi, dan "
           "sesudah itu tiap kali kamu mau memanaskan tangan sebelum wawancara.</p>",
}
