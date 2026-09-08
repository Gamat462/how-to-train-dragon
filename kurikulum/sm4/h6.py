# -*- coding: utf-8 -*-
"""Hari 6 — transaksi, dan satu setelan bawaan yang mengizinkan data rusak masuk."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bikin dua akun kas",
    blok("aksi", "Sesi Python baru. Ini bekerja di salinan <code>tx.db</code>, "
                 "<code>senja.db</code>-mu aman.", "LAKUKAN"),
    kode("""import sqlite3, shutil
shutil.copy("senja.db", "tx.db")
con = sqlite3.connect("tx.db", isolation_level=None)
con.executescript(\"\"\"
CREATE TABLE kas (akun TEXT PRIMARY KEY,
                  saldo INTEGER NOT NULL CHECK (saldo >= 0));
INSERT INTO kas VALUES ('Kas Besar', 5000000), ('Kas Kecil', 300000);
\"\"\")"""),
    blok("hasil", "<p>Tidak ada yang tercetak. Itu memang benar.</p>", "HARUS MUNCUL"),
    "<p><code>CHECK (saldo &gt;= 0)</code> artinya: saldo kas tidak boleh minus. "
    "<code>isolation_level=None</code> artinya: <em>jangan urus transaksi untukku, aku yang "
    "pegang kendali</em> — hari ini kamu yang pegang.</p>")

langkah("Catat saldo awalnya",
    blok("aksi", "Bikin fungsi <code>saldo</code>, lalu cetak totalnya.", "LAKUKAN"),
    kode("""def saldo():
    return dict(con.execute("SELECT akun, saldo FROM kas").fetchall())

print("saldo:", saldo())
print("total:", sum(saldo().values()))"""),
    blok("hasil", "<pre><code>saldo: {'Kas Besar': 5000000, 'Kas Kecil': 300000}\n"
                  "total: 5300000</code></pre>", "HARUS MUNCUL"),
    "<p><strong>5.300.000.</strong> Ingat angka ini. Empat langkah lagi ia akan berubah tanpa "
    "ada yang mencuri apa pun.</p>")

langkah("Perintah pertama: keluarkan Rp 400.000 dari Kas Besar",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""con.execute("UPDATE kas SET saldo = saldo - 400000 WHERE akun = 'Kas Besar'")
print("saldo:", saldo())"""),
    blok("hasil", "<pre><code>saldo: {'Kas Besar': 4600000, 'Kas Kecil': 300000}</code></pre>",
         "HARUS MUNCUL"),
    "<p>Berhasil. Uangnya sudah keluar dari Kas Besar dan <strong>belum masuk ke mana pun</strong>.</p>")

langkah("Perintah kedua: keluarkan Rp 900.000 dari Kas Kecil",
    blok("aksi", "Kas Kecil cuma punya 300.000, jadi ini akan ditolak. Jalankan.", "LAKUKAN"),
    kode("""try:
    con.execute("UPDATE kas SET saldo = saldo - 900000 WHERE akun = 'Kas Kecil'")
except sqlite3.IntegrityError as e:
    print("error:", e)"""),
    blok("hasil", "<pre><code>error: CHECK constraint failed: saldo &gt;= 0</code></pre>",
         "HARUS MUNCUL"),
    "<p>Ditolak, seperti seharusnya. Basis datanya melakukan tugasnya dengan benar.</p>")

langkah("Sekarang hitung totalnya",
    blok("aksi", "Ini langkah yang penting. Jalankan, lalu bandingkan dengan langkah 2.", "LAKUKAN"),
    kode("""print("saldo:", saldo())
print("total:", sum(saldo().values()))"""),
    blok("hasil", "<pre><code>saldo: {'Kas Besar': 4600000, 'Kas Kecil': 300000}\n"
                  "total: 4900000</code></pre>", "HARUS MUNCUL"),
    "<p><strong>5.300.000 → 4.900.000.</strong> Rp 400.000 hilang dari muka bumi. Tidak dicuri, "
    "tidak salah hitung — perintah pertama berhasil, perintah kedua ditolak, "
    "dan <strong>tidak ada yang membatalkan yang pertama</strong>.</p>",
    blok("bahaya", "<strong>Bentuk kesalahan yang tidak akan ketahuan dari laporan.</strong> "
                   "Tidak ada baris merah, tidak ada pesan gagal di dasbor — cuma angka yang "
                   "sedikit kurang benar, dan program yang <em>terlihat</em> jalan lancar. "
                   "Di skrip harian yang kamu pasang untuk klien (Minggu 11), ia akan mengulang "
                   "kesalahannya tiap hari sampai ada yang mencoba merekonsiliasi."))

langkah("Kamu sudah paham prinsipnya sejak sebelum tahu istilahnya",
    blok("aksi", "Baca satu kalimat ini, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p><strong>Debit dan kredit dicatat bersama-sama, atau tidak sama sekali.</strong> "
                  "Setengah jurnal bukan jurnal yang setengah benar — ia jurnal yang salah.</p>",
         "YANG SUDAH KAMU TAHU"),
    "<p>SQL punya nama untuk aturan itu: <strong>transaksi</strong>. Tiga baris perintah "
    "berikutnya adalah seluruh isinya.</p>")

langkah("Ulangi kejadian yang sama, dibungkus transaksi",
    blok("aksi", "Kembalikan saldonya dulu, lalu jalankan tiga <code>UPDATE</code> yang sama "
                 "persis — dengan tiga baris tambahan.", "LAKUKAN"),
    kode("""con.execute("UPDATE kas SET saldo = 5000000 WHERE akun = 'Kas Besar'")
try:
    con.execute("BEGIN")                                     # <-- satu baris ini
    con.execute("UPDATE kas SET saldo = saldo - 400000 WHERE akun = 'Kas Besar'")
    con.execute("UPDATE kas SET saldo = saldo - 900000 WHERE akun = 'Kas Kecil'")
    con.execute("COMMIT")                                    # <-- dan satu ini
except sqlite3.IntegrityError as e:
    con.execute("ROLLBACK")                                  # <-- dan penyelamatnya
    print("error:", e, "-> ROLLBACK")
print("total:", sum(saldo().values()))"""),
    blok("hasil", "<pre><code>error: CHECK constraint failed: saldo &gt;= 0 -&gt; ROLLBACK\n"
                  "total: 5300000</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Error yang sama persis. Totalnya tetap 5.300.000.</strong> "
    "<code>ROLLBACK</code> membatalkan juga <code>UPDATE</code> pertama yang sudah terlanjur "
    "berhasil, seolah-olah tidak pernah terjadi.</p>")

langkah("Tiga kata, satu janji",
    blok("aksi", "Baca sekali. Ini yang harus keluar dari mulutmu di wawancara.", "LAKUKAN"),
    tabel(["Kata", "Janjinya"],
          [["<code>BEGIN</code>", "mulai sekarang, semua yang kulakukan menggantung dulu"],
           ["<code>COMMIT</code>", "semuanya berhasil — tuliskan permanen"],
           ["<code>ROLLBACK</code>", "ada yang gagal — kembalikan seperti sebelum <code>BEGIN</code>"]]),
    "<p>Tidak ada keadaan setengah jalan yang bisa dilihat orang lain, dan tidak ada keadaan "
    "setengah jalan yang tertinggal <strong>kalau listrik mati di tengahnya</strong>.</p>")

langkah("Pola yang benar, dan satu baris yang sering dilupakan",
    blok("aksi", "Salin pola ini ke catatanmu. Ia menempel langsung ke <code>try</code>/"
                 "<code>except</code> dari <em>Bekal Kirim Hasil</em>.", "LAKUKAN"),
    kode("""try:
    con.execute("BEGIN")
    ...                      # kerjanya di sini
    con.execute("COMMIT")
except Exception:
    con.execute("ROLLBACK")
    raise                    # <-- jangan pernah dihapus""", salin=False),
    blok("bahaya", "<code>ROLLBACK</code> menyelamatkan <strong>datanya</strong>; "
                   "<code>raise</code> yang menyelamatkan <strong>kamu</strong>. Tanpa "
                   "<code>raise</code>, skripmu tetap melapor “selesai” padahal tidak ada yang "
                   "tersimpan — dan kamu baru tahu berbulan-bulan kemudian."),
    "<p><strong>Kapan ini perlu:</strong> setiap kali satu kejadian bisnis butuh "
    "<em>lebih dari satu perintah</em> — mencatat pembayaran (tulis ke tabel pembayaran "
    "<em>dan</em> ubah status pesanan), memuat ulang data bulanan (hapus bulan lama "
    "<em>lalu</em> masukkan yang baru). Kalau cuma satu perintah, SQLite sudah membungkusnya "
    "sendiri.</p>")

langkah("Sekarang bagian yang membuat orang terkejut",
    blok("aksi", "Salinan baru. Cetak satu setelan.", "LAKUKAN"),
    kode("""shutil.copy("senja.db", "fk.db")
c = sqlite3.connect("fk.db")
print("foreign_keys bawaan:", c.execute("PRAGMA foreign_keys").fetchone()[0])"""),
    blok("hasil", "<pre><code>foreign_keys bawaan: 0</code></pre>", "HARUS MUNCUL"),
    "<p>Nol berarti <strong>mati</strong>. Simpan keheranan itu sampai langkah 12.</p>")

langkah("Bikin dua tabel yang jelas-jelas bertaut",
    blok("aksi", "Perhatikan baris <code>REFERENCES induk(id)</code> — ditulis dengan jelas.", "LAKUKAN"),
    kode("""c.executescript(\"\"\"
CREATE TABLE induk (id INTEGER PRIMARY KEY, nama TEXT);
CREATE TABLE anak  (id INTEGER PRIMARY KEY,
                    induk_id INTEGER REFERENCES induk(id),
                    catatan TEXT);
INSERT INTO induk VALUES (1, 'Sari');
\"\"\")
print("induk:", c.execute("SELECT * FROM induk").fetchall())"""),
    blok("hasil", "<pre><code>induk: [(1, 'Sari')]</code></pre>", "HARUS MUNCUL"),
    "<p>Satu induk, nomor 1. Tabel <code>anak</code> hanya boleh menunjuk induk yang ada.</p>")

langkah("Coba masukkan baris yatim",
    blok("aksi", "Induk nomor 777 tidak pernah ada. Jalankan.", "LAKUKAN"),
    kode("""c.execute("INSERT INTO anak VALUES (99, 777, 'induk 777 tidak ada')")
c.commit()
print("tersimpan:", c.execute("SELECT * FROM anak").fetchall())"""),
    blok("hasil", "<pre><code>tersimpan: [(99, 777, 'induk 777 tidak ada')]</code></pre>",
         "HARUS MUNCUL"),
    "<p><strong>Diterima.</strong> Kamu menuliskan <code>REFERENCES induk(id)</code> dengan jelas, "
    "SQLite membacanya dengan jelas, dan tetap menyimpan baris yang menunjuk induk yang tidak ada. "
    "<em>Aturannya tercatat tapi tidak ditegakkan.</em></p>")

langkah("Nyalakan, lalu coba lagi",
    blok("aksi", "Satu baris PRAGMA, lalu ulangi dengan induk 888 yang juga tidak ada.", "LAKUKAN"),
    kode("""c.execute("PRAGMA foreign_keys = ON")
print("sesudah ON:", c.execute("PRAGMA foreign_keys").fetchone()[0])
try:
    c.execute("INSERT INTO anak VALUES (100, 888, 'induk 888 tidak ada')")
except sqlite3.IntegrityError as e:
    print("ditolak:", e)"""),
    blok("hasil", "<pre><code>sesudah ON: 1\nditolak: FOREIGN KEY constraint failed</code></pre>",
         "HARUS MUNCUL"),
    "<p>Sekarang ditolak. Aturan yang sama, tabel yang sama — bedanya cuma satu baris PRAGMA.</p>")

langkah("Periksa yang sudah terlanjur masuk",
    blok("aksi", "Menyalakan aturan tidak membersihkan pelanggaran lama. Buktikan.", "LAKUKAN"),
    kode("""print(c.execute("PRAGMA foreign_key_check").fetchall())"""),
    blok("hasil", "<pre><code>[('anak', 99, 'induk', 0)]</code></pre>", "HARUS MUNCUL"),
    "<p>Baris nomor 99 masih di sana. <strong>Menyalakan aturan cuma menghentikan yang baru.</strong></p>",
    blok("catatan", "<strong>Dua kebiasaan baru, mulai hari ini.</strong> "
                    "(1) Setelan ini <em>tidak</em> tersimpan di dalam berkasnya — ia harus "
                    "dinyalakan ulang <strong>di tiap koneksi baru</strong>, jadi tulis "
                    "<code>con.execute(\"PRAGMA foreign_keys = ON\")</code> tepat setelah "
                    "<code>connect</code>. "
                    "(2) Ketika menerima basis data dari orang lain, jalankan "
                    "<code>PRAGMA foreign_key_check</code> sekali <em>sebelum</em> mempercayai "
                    "apa pun di dalamnya."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab empat pertanyaan di kertas.", "LAKUKAN"),
    kode("""1. Tiga kata yang menjamin "semua atau tidak sama sekali"?
2. Satu baris yang wajib ikut di blok except selain ROLLBACK?
3. Berapa nilai bawaan PRAGMA foreign_keys di SQLite?
4. Perintah untuk memeriksa baris yatim yang sudah terlanjur masuk?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>BEGIN</code>, <code>COMMIT</code>, <code>ROLLBACK</code>. "
    "2. <code>raise</code>. "
    "3. <strong>0</strong> — mati, dan harus dinyalakan di tiap koneksi baru. "
    "4. <code>PRAGMA foreign_key_check</code>.</p></details>",
    blok("catatan", "<strong>Bagus untuk wawancara:</strong> bukan sekadar tahu apa itu foreign "
                    "key, tapi tahu bahwa <em>ada</em>-nya aturan dan <em>ditegakkan</em>-nya "
                    "aturan adalah dua hal berbeda. SQLite mematikannya demi kompatibilitas "
                    "dengan basis data lama yang sudah terlanjur punya baris yatim; PostgreSQL "
                    "menegakkannya sejak awal tanpa perlu diminta."))

HARI6 = {
  "n": "HARI 6",
  "tab": "6",
  "judul": "Transaksi: Rp 400.000 yang menguap di antara dua baris perintah",
  "waktu": "± 65 menit",
  "tujuan": "memakai <code>BEGIN</code>/<code>COMMIT</code>/<code>ROLLBACK</code> dengan sadar, "
            "dan menemukan sendiri satu setelan bawaan SQLite yang diam-diam mengizinkan data "
            "rusak masuk ke basis datamu.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu kejadian yang kamu saksikan sendiri "
           "(Rp 400.000 menguap), tiga kata yang mencegahnya, dan satu baris PRAGMA yang mulai "
           "sekarang ikut di tiap <code>connect</code> yang kamu tulis.</p>"
           "<p style=\"margin-top:8px\">Hari ini bukan soal kecepatan sama sekali. Ia soal "
           "<strong>angka yang bisa dipercaya</strong> — dan itu bagian pekerjaanmu yang paling "
           "dekat dengan enam tahun terakhirmu.</p>"
           "<p style=\"margin-top:8px\">Besok, hari terakhir: memilih antara <code>VIEW</code> dan "
           "tabel ringkasan, dan satu berkas uji mutu yang berteriak <em>sebelum</em> angkanya "
           "sampai ke klien.</p>",
}
