# -*- coding: utf-8 -*-
"""Hari 1 — baca lowongan seperti kertas kerja, lalu terima "ekspor ERP" pertamamu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Modul ini beda: satu lowongan sungguhan, bukan latihan umum",
    blok("aksi", "Baca sekali. Tidak ada yang perlu diketik.", "LAKUKAN"),
    "<p>Kamu melamar <strong>Analyst | Tax Data Automation (Python & SQL)</strong> di "
    "Deloitte (Melbourne, boleh Sydney/Perth). Lima hari ini bukan pelajaran baru dari nol — "
    "isinya <strong>menerjemahkan apa yang sudah kamu kuasai ke bahasa persis yang dipakai "
    "lowongan ini</strong>, menutup dua-tiga celah yang genuinely belum ada, dan menulis "
    "kalimat CV serta jawaban wawancara yang siap pakai.</p>",
    blok("catatan", "Satu kalimat dari lowongannya, dibaca dua kali: <em>\"You do not need to "
                    "arrive as a Tax or AI specialist. We are looking for strong Python and SQL "
                    "foundations, careful reasoning and a willingness to learn.\"</em> Itu "
                    "persis modal yang sedang kamu bangun."))

langkah("Sepuluh syarat wajib, diterjemahkan satu per satu",
    blok("aksi", "Salin tabel ini ke catatanmu. Ini kerangka seluruh modul.", "LAKUKAN"),
    tabel(["Syarat lowongan (bahasa aslinya)", "Sudah kamu punya dari"],
          [["1-2 tahun pengalaman data engineering/automation",
            "Portofolio: Studi Kasus Nyata, Bekal Data Klien, Migas L1-L5 — <em>proyek</em> "
            "menggantikan tahun kalau kamu bisa membuktikannya"],
           ["Python & SQL kuat untuk ELT dan rules-based processing",
            "M1-M3, M6, Python Produksi, SQL Mahir L1-L2"],
           ["Polars, Pandas, DuckDB", "Pandas (M3) ya, DuckDB (SQL Produksi) ya. "
            "<strong>Polars — celah, hari 5</strong>"],
           ["Relational data, data quality, ETL/ELT patterns",
            "M2 JOIN, M9, M10 dbt, seluruh jalur SQL Mahir"],
           ["Validasi & rekonsiliasi pakai reference/golden dataset, automated tests",
            "SQL Mahir L1 Hari 7 (tie-out) + Python Produksi (pytest) — <strong>hari 4 "
            "modul ini</strong>"],
           ["Data-quality & anomaly controls, troubleshoot produksi",
            "SQL Mahir L1 Hari 2 (NULL), Python Produksi (bug nyata pandas 3)"],
           ["Workshop requirement dengan Tax SME, jadi aturan yang bisa diuji",
            "Ini yang KAP-mu <em>sudah</em> lakukan bertahun-tahun — cuma ganti nama"],
           ["Penalaran logis: kalkulasi, klasifikasi, precedence, exception",
            "Hari 2-3 modul ini, dibangun baru dari nol memakai bahasa persis lowongan ini"],
           ["Git, code review, automated testing, CI/CD, dokumentasi teknis",
            "M11 Git & Otomasi, Python Produksi"],
           ["Komunikasi jelas, rasa ingin tahu, belajar mandiri",
            "Tidak diukur kode — dibuktikan lewat cara kamu menjawab wawancara"]]),
    "<p>Delapan dari sepuluh baris sudah ada tautannya. <strong>Itu bukan kebetulan</strong> — "
    "lowongan ini persis menguji apa yang rute ini bangun sejak Hari 1.</p>")

langkah("Empat hal yang disebut \"nilai lebih\", bukan wajib",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    tabel(["Nilai lebih (advantageous)", "Status"],
          [["Pengalaman pajak, akuntansi, atau data ERP",
            "<strong>Kamu sudah punya ini — dari KAP, bukan dari kursus manapun</strong>"],
           ["Rules engine, decision table", "Dibangun hari 2-3 modul ini"],
           ["Azure, Docker, Kubernetes, Airflow", "Celah — hari 5, dibahas secukupnya"],
           ["Deteksi anomali statistik", "M7 Statistik Lanjutan sudah menyentuhnya"],
           ["Tool AI, LLM API, evaluation harness, agentic workflow",
            "Celah nama, tapi <strong>bukan celah pengalaman</strong> — tunggu hari 5"]]),
    blok("catatan", "Baris pertama tabel ini yang paling sering diabaikan pelamar lain. "
                    "Ribuan orang bisa menulis SQL. <strong>Yang tahu bedanya PPh final dan "
                    "PPh progresif tanpa membuka Google jauh lebih sedikit</strong> — dan kamu "
                    "salah satunya."))

langkah("Lowongan mengirimimu \"ekspor ERP\" pertama — buka sambunganmu",
    blok("aksi", "VS Code, sambungan <code>senja</code> yang sudah ada dari SQL Mahir L1. "
                 "Berkas baru: <code>senja/pjk-hari-1.sql</code>.", "LAKUKAN"),
    kode("SELECT * FROM pjk_wp ORDER BY id;"),
    keluaran(H, "h0_lihat_wp"),
    "<p>Tujuh wajib pajak. Kolom <code>jenis</code> membedakan orang pribadi biasa "
    "(<code>perorangan</code>) dari usaha kecil (<code>umkm</code>) — bedanya menentukan "
    "aturan mana yang berlaku, dan itu inti hari 2-3.</p>",
    blok("catatan", "<strong>Kalau hasilmu bukan tujuh baris</strong>, itu wajar kalau kamu "
                    "belum menjalankan <code>pjk_data.sql</code> dari paket zip. Jalankan "
                    "sekali, lalu ulangi query ini."))

langkah("Kenali dulu bentuknya, sebelum menghitung apa pun",
    blok("aksi", "Berapa banyak tiap jenis? Jalankan.", "LAKUKAN"),
    kode("SELECT jenis, count(*) FROM pjk_wp GROUP BY jenis;"),
    keluaran(H, "h1_hitung_jenis"),
    "<p>Empat <code>perorangan</code>, tiga <code>umkm</code>. Kecil, tapi cukup untuk "
    "menunjukkan pola precedence dan exception yang jadi inti dua hari berikutnya.</p>")

langkah("Lihat juga aturan tarifnya — ini \"decision table\" yang disebut lowongan",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("SELECT * FROM pjk_lapisan ORDER BY urutan;"),
    keluaran(H, "h0_lihat_lapisan"),
    blok("bahaya", "<strong>Angka di tabel ini disederhanakan untuk latihan, bukan untuk "
                   "SPT sungguhan.</strong> Struktur lapisannya benar (progresif, lima "
                   "tingkat), tapi jangan dipakai mengisi pajak orang beneran — selalu cek "
                   "PMK/UU HPP yang berlaku."),
    "<p>Lima baris, lima tarif berjenjang. Ini <strong>persis</strong> yang disebut lowongan "
    "sebagai \"rules engine\" atau \"decision table\" — tabel yang isinya aturan, bukan data "
    "transaksi.</p>")

langkah("Kiriman ulang dari klien — dan ERP-nya menolak",
    blok("aksi", "Bayangkan sistem sumbernya mengirim ulang baris yang sama, tanpa sengaja. "
                 "Jalankan.", "LAKUKAN"),
    kode("INSERT INTO pjk_wp (id, nama, jenis, penghasilan_tahunan)\n"
         "VALUES (1, 'Rina (kiriman ulang)', 'perorangan', 45000000);"),
    keluaran(H, "h1_merah_duplikat"),
    blok("catatan", "<strong>Layar merah ini kabar baik.</strong> <code>id</code> adalah kunci "
                    "utama; PostgreSQL menolak baris kedua yang mengklaim id yang sama. Tanpa "
                    "penjaga ini, data klien bisa terhitung dua kali tanpa siapa pun sadar — "
                    "persis risiko yang kamu cari waktu memeriksa duplikasi transaksi di "
                    "audit."))

langkah("Ekspor Excel klien, dengan pemisah ribuan ala Indonesia",
    blok("aksi", "Data keuangan dari ERP sering datang sebagai teks berformat, bukan angka "
                 "murni. Jalankan.", "LAKUKAN"),
    kode("INSERT INTO pjk_wp (nama, jenis, penghasilan_tahunan)\n"
         "VALUES ('Tono', 'perorangan', '1.250.000.000');"),
    keluaran(H, "h1_merah_format_erp"),
    "<p>PostgreSQL membaca <code>1.250.000.000</code> sebagai teks, bukan sebagai satu miliar "
    "dua ratus lima puluh juta — titiknya bukan pemisah ribuan bagi mesin, dan angkanya "
    "ditolak mentah-mentah.</p>",
    blok("bahaya", "Kalau kolomnya bertipe <code>text</code> alih-alih <code>bigint</code>, "
                   "insert ini <strong>akan berhasil</strong> — dan kamu baru sadar ada masalah "
                   "waktu mencoba menjumlahkannya nanti. Kesalahan yang ditolak di depan pintu "
                   "selalu lebih murah daripada yang lolos lalu meledak di laporan."))

langkah("Dua error ini adalah jawaban wawancara, bukan cuma latihan",
    blok("aksi", "Baca sekali, lalu ucapkan dengan suara keras seolah menjawab pewawancara.",
         "LAKUKAN"),
    blok("hasil", "<p>\"Saya pernah membuktikan sendiri dua kegagalan data ERP yang paling "
                  "umum — kiriman duplikat dan angka berformat lokal — dengan memicu keduanya "
                  "di PostgreSQL dan membaca pesan errornya baris demi baris.\"</p>",
         "KALIMAT WAWANCARA"),
    "<p>Lowongan ini menyebut <em>\"diagnosing and resolving production issues\"</em> sebagai "
    "tugas harian. Dua langkah barusan <strong>persis itu</strong>, dalam bentuk kecil.</p>")

langkah("Draf kalimat CV pertamamu",
    blok("aksi", "Salin ke catatan lamaranmu. Ini draf — hari 5 kamu tulis versi final.",
         "LAKUKAN"),
    blok("hasil", "<p>\"Membangun dan menguji basis data aturan (rules table) di PostgreSQL "
                  "untuk kasus penghitungan bertingkat, termasuk penanganan kesalahan data "
                  "sumber (duplikasi, format angka) yang umum terjadi pada ekspor ERP/Excel "
                  "klien.\"</p>", "DRAF CV #1"),
    blok("catatan", "Kalimat ini jujur — semuanya baru saja kamu jalankan sendiri, hari ini, "
                    "bukan klaim kosong. Itu bedanya CV yang tahan ditanya lebih dalam waktu "
                    "wawancara."))

HARI1 = {
  "n": "HARI 1", "tab": "1",
  "judul": "Baca lowongan seperti kertas kerja, lalu terima ekspor ERP pertamamu",
  "waktu": "± 45 menit",
  "tujuan": "memetakan tiap syarat lowongan Deloitte ke modul yang sudah kamu selesaikan, dan "
            "memicu dua kesalahan data ERP yang paling umum di PostgreSQL.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> delapan dari sepuluh syarat wajib sudah "
           "tertutup modul lain · pengalaman KAP-mu ada di kolom \"nilai lebih\" tanpa kamu "
           "sadari · dua error ERP sungguhan (duplikat, format angka) sudah kamu picu dan "
           "baca sendiri.</p>"
           "<p style=\"margin-top:8px\">Besok: precedence dan kalkulasi bertingkat — bagian "
           "\"penalaran logis\" yang paling sering ditanya di wawancara posisi ini.</p>",
}
