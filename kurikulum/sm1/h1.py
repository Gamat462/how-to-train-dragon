# -*- coding: utf-8 -*-
"""Hari 1 — sambungkan VS Code ke PostgreSQL, muat senja.sql, temui NULL."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Apa yang kamu tutup minggu ini",
    blok("aksi", "Baca sekali. Tidak ada yang perlu diketik.", "LAKUKAN"),
    "<p>M1, M2, dan M6 sudah membawamu dari nol sampai bisa menulis query bertingkat. Yang "
    "belum pernah disinggung justru hal-hal yang membuat query-mu <strong>diam-diam "
    "salah</strong> — bukan gagal dengan tulisan merah, tapi mengembalikan angka yang terlihat "
    "wajar dan keliru.</p>",
    blok("catatan", "Kamu sudah punya refleks untuk ini. Di kertas kerja, angka yang "
                    "<em>terlihat</em> benar tapi tidak bisa kamu telusuri asalnya adalah "
                    "temuan, bukan jawaban. Minggu ini kamu memindahkan refleks itu ke SQL — "
                    "di PostgreSQL, mesin yang dipakai perusahaan tempat kamu melamar."))

langkah("Pasang dua ekstensi di VS Code",
    blok("aksi", "Buka VS Code, tekan <strong>Ctrl+Shift+X</strong>, lalu cari dan pasang "
                 "dua ini — <strong>berurutan</strong>.", "LAKUKAN"),
    tabel(["Ekstensi", "Penerbit", "Gunanya"],
          [["SQLTools", "Matheus Teixeira", "Kerangka: sambungan, editor, tabel hasil"],
           ["SQLTools PostgreSQL/Cockroach Driver", "Matheus Teixeira",
            "Penyetir khusus PostgreSQL — <strong>wajib, dan sering terlupa</strong>"]]),
    blok("hasil", "<p>Ikon basis data (silinder) muncul di batang sisi kiri VS Code.</p>",
         "YANG HARUS TERLIHAT"),
    blok("bahaya", "<strong>Kalau kamu hanya memasang yang pertama</strong>, SQLTools akan "
                   "terpasang tapi tidak menawarkan PostgreSQL waktu kamu membuat sambungan. "
                   "Itu penyebab kebingungan paling umum di langkah berikutnya."))

langkah("Buat sambungan ke server PostgreSQL-mu",
    blok("aksi", "Klik ikon basis data di sisi kiri → <strong>Add New Connection</strong> → "
                 "pilih <strong>PostgreSQL</strong>. Isi seperti tabel ini, lalu "
                 "<strong>Test Connection</strong>.", "LAKUKAN"),
    tabel(["Isian", "Isinya"],
          [["Connection name", "<code>senja</code>"],
           ["Server / Host", "<code>localhost</code>"],
           ["Port", "<code>5432</code>"],
           ["Database", "<code>postgres</code> — untuk sekarang; diganti nanti"],
           ["Username", "<code>postgres</code>"],
           ["Password", "yang kamu buat waktu memasang PostgreSQL"]]),
    blok("hasil", "<p>Muncul tulisan <strong>Successfully connected</strong>. Simpan "
                  "sambungannya.</p>", "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Kalau muncul <code>password authentication failed for user "
                    "\"postgres\"</code>, itu wajar</strong> — hampir semua orang salah ingat "
                    "kata sandi yang dibuat saat memasang. Kata sandinya bisa diatur ulang lewat "
                    "pgAdmin yang ikut terpasang bersama PostgreSQL di Windows."))

langkah("Uji sambungannya dengan satu baris SQL",
    blok("aksi", "Buat berkas baru di VS Code, simpan sebagai <code>uji.sql</code>, ketik "
                 "satu baris ini, lalu jalankan (klik <em>Run on active connection</em> yang "
                 "muncul di atas query, atau tekan <strong>Ctrl+E Ctrl+E</strong>).", "LAKUKAN"),
    kode("SELECT version();"),
    blok("hasil", "<p>Satu baris panjang yang diawali <code>PostgreSQL 16.</code> "
                  "(atau 15, atau 17 — nomor versimu boleh berbeda), lalu keterangan sistem "
                  "operasimu.</p>", "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Kalau versimu bukan 16, itu tidak apa-apa.</strong> Seluruh modul "
                    "ini berjalan di PostgreSQL 12 ke atas. Yang penting <code>SELECT</code>-mu "
                    "sampai ke server dan hasilnya kembali."))

langkah("Buat basis data latihanmu",
    blok("aksi", "Di <code>uji.sql</code>, ganti isinya dengan satu baris ini dan jalankan.",
         "LAKUKAN"),
    kode("CREATE DATABASE senja;"),
    blok("hasil", "<p>Tidak ada tabel hasil — hanya pemberitahuan bahwa perintahnya berhasil.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Perintah yang tidak menampilkan apa-apa itu normal.</strong> "
                    "<code>CREATE</code>, <code>INSERT</code>, dan <code>UPDATE</code> mengubah "
                    "sesuatu; hanya <code>SELECT</code> yang mengembalikan tabel."),
    blok("bahaya", "Kalau muncul <code>database \"senja\" already exists</code>, berarti kamu "
                   "sudah membuatnya. Lanjut saja ke langkah berikutnya."))

langkah("Arahkan sambunganmu ke basis data yang baru",
    blok("aksi", "Kembali ke daftar sambungan → klik kanan <code>senja</code> → "
                 "<strong>Edit Connection</strong> → ubah isian <em>Database</em> dari "
                 "<code>postgres</code> jadi <code>senja</code> → simpan → sambungkan lagi.",
         "LAKUKAN"),
    blok("hasil", "<p>Di panel SQLTools, di bawah sambungan <code>senja</code>, muncul "
                  "<strong>Schemas → public → Tables</strong> — dan isinya masih kosong.</p>",
         "YANG HARUS TERLIHAT"),
    "<p>Kosong itu benar. Kamu baru membuat wadahnya; isinya datang di langkah berikutnya.</p>")

langkah("Muat datanya dari senja.sql",
    blok("aksi", "Di paket zip-mu, buka <code>data-dan-skrip/sql-mahir/senja.sql</code> lewat "
                 "VS Code. Berkas itu berisi tujuh <code>CREATE TABLE</code> dan 1.744 baris "
                 "data. <strong>Jalankan seluruh berkasnya</strong> — di SQLTools: klik kanan "
                 "di dalam editor → <em>Run this file</em>.", "LAKUKAN"),
    blok("hasil", "<p>Sederet pemberitahuan berhasil, tanpa satu pun tulisan merah. Prosesnya "
                  "beberapa detik.</p>", "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Ini persis cara kerja di kantor.</strong> Kamu jarang membuat data "
                    "sendiri; kamu menerima berkas <code>.sql</code> atau hasil ekspor, lalu "
                    "memuatnya ke basis datamu sebelum menganalisis apa pun."))

langkah("Periksa muatannya sebelum melangkah",
    blok("aksi", "Berkas baru, simpan sebagai <code>senja/00-periksa.sql</code>. Jalankan.",
         "LAKUKAN"),
    kode('''SELECT 'pelanggan' AS tabel, count(*) FROM pelanggan
UNION ALL SELECT 'produk',        count(*) FROM produk
UNION ALL SELECT 'pegawai',       count(*) FROM pegawai
UNION ALL SELECT 'pesanan',       count(*) FROM pesanan
UNION ALL SELECT 'item',          count(*) FROM item
UNION ALL SELECT 'kunjungan',     count(*) FROM kunjungan
UNION ALL SELECT 'pesanan_kasir', count(*) FROM pesanan_kasir;'''),
    keluaran(H, "h1_hitung_tabel"),
    blok("bahaya", "<strong>Kalau angkamu berbeda walau satu baris, berhenti di sini.</strong> "
                   "Jalankan ulang <code>senja.sql</code> dari awal. Seluruh angka di tujuh hari "
                   "ini dihitung dari data itu persis — mencocokkan dengan data yang berbeda "
                   "cuma akan membuatmu curiga pada dirimu sendiri tanpa sebab."))

langkah("Cara kerja sehari-hari: satu berkas .sql, banyak query",
    blok("aksi", "Baca sekali, lalu terapkan mulai sekarang.", "LAKUKAN"),
    blok("hasil", "<p>Simpan tiap hari sebagai satu berkas: <code>senja/hari-1.sql</code>, "
                  "<code>senja/hari-2.sql</code>, dan seterusnya. Query dipisahkan titik koma; "
                  "SQLTools menjalankan <strong>query tempat kursormu berada</strong>.</p>",
         "KEBIASAAN YANG DIBANGUN"),
    "<p>Jangan mengetik ulang di kotak sekali pakai. Berkas <code>.sql</code> yang tersimpan "
    "adalah kertas kerjamu: bisa dibuka lagi, bisa dikirim ke orang lain, bisa diperiksa "
    "kembali enam bulan lagi.</p>",
    blok("catatan", "Kalau nanti kamu memakai Git (Modul M11), berkas-berkas ini yang masuk ke "
                    "repositori — dan riwayat perubahannya jadi bukti kerjamu waktu melamar."))

langkah("Lihat tabel pertamamu",
    blok("aksi", "Berkas baru: <code>senja/hari-1.sql</code>. Ketik dan jalankan.", "LAKUKAN"),
    kode("SELECT * FROM produk ORDER BY id;"),
    keluaran(H, "h1_produk"),
    "<p>Perhatikan dua baris terakhir kolom <code>harga_beli</code>: Cheesecake dan Matcha Latte "
    "<strong>kosong</strong>. Di basis datanya itu <code>NULL</code> — harga belinya belum "
    "tercatat.</p>",
    blok("catatan", "Ekstensimu bisa menampilkannya sebagai sel kosong, sebagai tulisan "
                    "<em>NULL</em> yang pudar, atau sebagai <code>[null]</code>. "
                    "<strong>Tampilannya boleh berbeda; nilainya sama.</strong>"))

langkah("Tiga hal yang sering dikira sama",
    blok("aksi", "Baca sekali, hafalkan.", "LAKUKAN"),
    tabel(["Yang kamu lihat", "Artinya"],
          [["<code>0</code>", "nol rupiah — sebuah angka, dan angkanya nol"],
           ["<code>''</code>", "teks kosong — ada isinya, isinya nol huruf"],
           ["<code>NULL</code>", "<strong>tidak diketahui</strong> — belum ada nilainya sama sekali"]]),
    "<p>Kalau kamu pernah melihat sel Excel kosong yang tiba-tiba ikut terhitung sebagai nol di "
    "<code>AVERAGE</code>, kamu sudah pernah kena versi Excel-nya.</p>")

langkah("Tebak dulu, jangan langsung dijalankan",
    blok("aksi", "Jawab di kepalamu: apakah <code>NULL = NULL</code> bernilai benar?", "LAKUKAN"),
    blok("bahaya", "<strong>Tebak dulu sebelum menggulir.</strong> Kalau kamu langsung membaca "
                   "jawabannya, kamu sedang membaca — bukan berlatih. Wawancara tidak "
                   "menyediakan tombol buka kunci."),
    "<p>Sebagian besar orang menjawab “benar”. Itu jawaban yang wajar, dan itu salah — jadi "
    "kalau itu tebakanmu, kamu sedang berada di tempat yang tepat.</p>")

langkah("Tiga nilai kebenaran, bukan dua",
    blok("aksi", "Sekarang jalankan.", "LAKUKAN"),
    kode('''SELECT NULL = NULL  AS "NULL=NULL",
       NULL <> NULL AS "NULL<>NULL",
       NULL IS NULL AS "NULL IS NULL",
       1 = 1        AS benar,
       1 = 2        AS salah;'''),
    keluaran(H, "h1_tiga_nilai"),
    "<p>Di Python sebuah perbandingan menghasilkan <code>True</code> atau <code>False</code>. "
    "Di SQL ada <strong>tiga</strong>: benar, salah, dan <strong>tidak diketahui</strong> "
    "(<code>NULL</code>).</p>",
    blok("hasil", "<p>Kalau umur dua orang sama-sama <strong>tidak diketahui</strong>, apakah "
                  "umur mereka sama? Kamu tidak tahu. Jawabannya bukan ya, bukan tidak — "
                  "<em>tidak diketahui</em>.</p>", "TERJEMAHANNYA"),
    blok("catatan", "<code>NULL IS NULL</code> tetap bernilai <em>true</em>. "
                    "<code>IS NULL</code> tidak bertanya “apakah nilainya sama”, ia bertanya "
                    "“apakah nilainya belum ada”. Itu pertanyaan yang selalu bisa dijawab."))

langkah("Layar merah pertamamu minggu ini — dan itu disengaja",
    blok("aksi", "Salah ketik nama kolomnya, dengan sengaja. Jalankan.", "LAKUKAN"),
    kode("SELECT nama FROM pelanggan WHERE kotta IS NULL;"),
    keluaran(H, "h1_merah_kolom"),
    blok("catatan", "<strong>Layar merah itu kabar baik.</strong> PostgreSQL memberitahumu tiga "
                    "hal sekaligus: apa yang salah, <em>di kolom keberapa</em> (tanda "
                    "<code>^</code> menunjuk tepat ke situ), dan tebakan perbaikannya di baris "
                    "<code>HINT</code>. SQLite tidak sebaik itu."),
    "<p>Ingat rasanya. Besok kamu akan melihat kesalahan yang <em>tidak</em> merah, dan itu "
    "jenis yang mahal.</p>")

HARI1 = {
  "n": "HARI 1", "tab": "1",
  "judul": "Sambungkan VS Code ke PostgreSQL, lalu temui NULL",
  "waktu": "± 55 menit",
  "tujuan": "punya basis data <code>senja</code> di PostgreSQL yang angkanya sama persis dengan "
            "halaman ini, dijalankan dari VS Code, dan bisa menyebut ketiga nilai kebenaran SQL.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> VS Code yang tersambung ke PostgreSQL, tujuh "
           "tabel yang kamu muat sendiri, satu tulisan merah yang kamu picu sendiri, dan satu "
           "kalimat: <code>NULL</code> berarti <em>tidak diketahui</em>, bukan kosong dan bukan "
           "nol.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 1 dari 8.</strong> Tutup halaman "
           "ini dan jawab dengan suara: <em>berapa nilai kebenaran yang ada di SQL, dan apa "
           "hasil <code>NULL = NULL</code>?</em></p>"
           "<details><summary>Kunci</summary><p>Tiga: benar, salah, dan tidak diketahui. "
           "<code>NULL = NULL</code> menghasilkan <code>NULL</code> (tidak diketahui) — bukan "
           "benar, bukan salah.</p></details>",
}
