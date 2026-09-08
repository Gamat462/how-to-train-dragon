# -*- coding: utf-8 -*-
"""Hari 1 — pasang senja.db satu sel demi satu sel, lalu temui NULL."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Apa yang sebenarnya kamu tutup minggu ini",
    blok("aksi", "Baca sekali, lalu lanjut. Tidak ada yang perlu diketik.", "LAKUKAN"),
    "<p>M1, M2, dan M6 sudah membawamu dari nol sampai bisa menulis query bertingkat. Yang "
    "belum pernah disinggung justru hal-hal yang membuat query-mu <strong>diam-diam "
    "salah</strong> — bukan gagal dengan tulisan merah, tapi mengembalikan angka yang "
    "terlihat wajar dan keliru.</p>",
    blok("catatan", "Kamu sudah punya refleks untuk ini. Di kertas kerja, angka yang "
                    "<em>terlihat</em> benar tapi tidak bisa kamu telusuri asalnya adalah "
                    "temuan, bukan jawaban. Minggu ini kamu memindahkan refleks itu ke SQL."))

langkah("Buka Colab baru, dan sambungkan",
    blok("aksi", "Colab baru, sel pertama. Jalankan.", "LAKUKAN"),
    kode('''import sqlite3, random
from datetime import date, timedelta
rng = random.Random(11)
con = sqlite3.connect("senja.db")'''),
    blok("hasil", "<p>Tidak ada apa-apa yang muncul di layarmu. Selnya selesai, dan tidak ada tulisan merah.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Sel yang diam itu normal.</strong> Python hanya menampilkan sesuatu "
                    "kalau kamu memintanya. Empat baris ini cuma menyiapkan alat."),
    "<p><code>random.Random(11)</code> mengunci angka acaknya. Itu sebabnya angka di halaman ini "
    "akan sama persis dengan angka di layarmu — asal tujuh sel berikutnya kamu jalankan "
    "<strong>sekali, berurutan</strong>.</p>")

langkah("Sel 2 — tujuh tabel",
    blok("aksi", "Sel baru. Ini kerangka basis datanya: nama tabel, nama kolom, tipe.", "LAKUKAN"),
    kode('''con.executescript("""
DROP TABLE IF EXISTS pelanggan; DROP TABLE IF EXISTS produk; DROP TABLE IF EXISTS pesanan;
DROP TABLE IF EXISTS item; DROP TABLE IF EXISTS pegawai; DROP TABLE IF EXISTS kunjungan;
DROP TABLE IF EXISTS pesanan_kasir;
CREATE TABLE pelanggan (id INTEGER PRIMARY KEY, nama TEXT, kota TEXT, tanggal_daftar TEXT, id_perujuk INTEGER);
CREATE TABLE produk    (id INTEGER PRIMARY KEY, nama TEXT, kategori TEXT, harga INTEGER, harga_beli INTEGER);
CREATE TABLE pesanan   (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, tanggal TEXT, cabang TEXT, kanal TEXT, status TEXT);
CREATE TABLE item      (id INTEGER PRIMARY KEY, pesanan_id INTEGER, produk_id INTEGER, jumlah INTEGER, harga_saat_itu INTEGER);
CREATE TABLE pegawai   (id INTEGER PRIMARY KEY, nama TEXT, jabatan TEXT, cabang TEXT, id_atasan INTEGER, gaji INTEGER);
CREATE TABLE kunjungan (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, waktu TEXT);
CREATE TABLE pesanan_kasir (id INTEGER PRIMARY KEY, tanggal TEXT, cabang TEXT, nilai INTEGER);
""")
print("Tujuh tabel dibuat.")'''),
    blok("hasil", "<pre><code>Tujuh tabel dibuat.</code></pre>", "HARUS MUNCUL"),
    "<p><code>DROP TABLE IF EXISTS</code> di depan membuat sel ini <strong>aman dijalankan "
    "ulang</strong>. Kalau nanti kamu bingung dan ingin mulai bersih, jalankan lagi dari sel 1.</p>")

langkah("Sel 3 — produk dan pelanggan",
    blok("aksi", "Sel baru. Isi dua tabel sekaligus.", "LAKUKAN"),
    kode('''produk = [(1,"Kopi Susu","Minuman",22000,7000),(2,"Americano","Minuman",18000,5000),
          (3,"Teh Manis","Minuman",10000,2000),(4,"Roti Bakar","Makanan",15000,6000),
          (5,"Croissant","Makanan",25000,11000),(6,"Cheesecake","Makanan",30000,None),
          (7,"Matcha Latte","Minuman",26000,None)]
con.executemany("INSERT INTO produk VALUES (?,?,?,?,?)", produk)
kota = ["Jakarta","Bandung","Yogyakarta",None]
nama = ["Rina","Bayu","Sari","Dimas","Putri","Agus","Maya","Fajar","Intan","Yoga",
        "Nadia","Reza","Lita","Hendra","Tari","Wawan","Sinta","Bagus","Vira","Andi"]
con.executemany("INSERT INTO pelanggan VALUES (?,?,?,?,?)", [
    (i, n, kota[rng.randrange(4)], (date(2023,1,1)+timedelta(days=rng.randrange(500))).isoformat(),
     (rng.choice([None,None,rng.randint(1,max(1,i-1))]) if i>1 else None)) for i,n in enumerate(nama,1)])
print("produk:", con.execute("SELECT COUNT(*) FROM produk").fetchone()[0],
      "| pelanggan:", con.execute("SELECT COUNT(*) FROM pelanggan").fetchone()[0])'''),
    blok("hasil", "<pre><code>produk: 7 | pelanggan: 20</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "Perhatikan dua <code>None</code> di daftar produk, dan satu <code>None</code> "
                    "di daftar kota. Itu bukan salah ketik — <strong>itu bahan pelajaran hari "
                    "ini</strong>, ditanam dengan sengaja."))

langkah("Sel 4 — pegawai",
    blok("aksi", "Sel baru. Sepuluh orang, lengkap dengan siapa atasan siapa.", "LAKUKAN"),
    kode('''con.executemany("INSERT INTO pegawai VALUES (?,?,?,?,?,?)", [
    (1,"Pak Hardi","Pemilik",None,None,25000000),(2,"Bu Rina","Manajer Area","Jakarta",1,14000000),
    (3,"Sinta","Kepala Cabang","Kemang",2,9000000),(4,"Bagus","Kepala Cabang","Dago",2,8500000),
    (5,"Vira","Kepala Cabang","Seturan",2,8500000),(6,"Andi","Barista","Kemang",3,4500000),
    (7,"Tari","Barista","Kemang",3,4500000),(8,"Wawan","Barista","Dago",4,4200000),
    (9,"Yoga","Kasir","Seturan",5,4000000),(10,"Lita","Kasir","Kemang",3,4000000)])
print("pegawai:", con.execute("SELECT COUNT(*) FROM pegawai").fetchone()[0])'''),
    blok("hasil", "<pre><code>pegawai: 10</code></pre>", "HARUS MUNCUL"),
    "<p>Kolom kelima yang kamu lihat adalah <code>id_atasan</code>, dan isinya menunjuk ke <code>id</code> di "
    "tabel yang sama. Pak Hardi tidak punya atasan, jadi <code>None</code>. Tabel ini yang "
    "kamu pakai di Hari 5.</p>")

langkah("Sel 5 — 400 pesanan dan isinya",
    blok("aksi", "Sel baru. Ini yang paling lama jalannya — beberapa detik.", "LAKUKAN"),
    kode('''cab=["Kemang","Dago","Seturan"]; kan=["Dine-in","Take-away","Ojol"]; pid=iid=1
for _ in range(400):
    p = rng.choice([None]+list(range(1,18))*2)
    con.execute("INSERT INTO pesanan VALUES (?,?,?,?,?,?)", (pid, p,
        (date(2024,1,1)+timedelta(days=rng.randrange(182))).isoformat(),
        rng.choice(cab), rng.choice(kan), rng.choices(["selesai","batal"],weights=[92,8])[0]))
    for _ in range(rng.randint(1,3)):
        pr = rng.randrange(1,8)
        con.execute("INSERT INTO item VALUES (?,?,?,?,?)",
                    (iid,pid,pr,rng.randint(1,4),produk[pr-1][3])); iid+=1
    pid+=1
print("pesanan:", con.execute("SELECT COUNT(*) FROM pesanan").fetchone()[0],
      "| item:", con.execute("SELECT COUNT(*) FROM item").fetchone()[0])'''),
    blok("hasil", "<pre><code>pesanan: 400 | item: 788</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "Baris ketiga menyelipkan <code>None</code> ke dalam daftar pilihan "
                    "<code>pelanggan_id</code>. Artinya sebagian pesanan datang dari tamu yang "
                    "tidak punya akun. Itu wajar di kedai kopi — dan itu yang meledak di Hari 3."))

langkah("Sel 6 — kunjungan",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''kid=1
for p in range(1,21):
    t = date(2024,3,1)
    for _ in range(rng.randint(3,12)):
        t += timedelta(days=rng.choice([0,0,1,1,2,5,9,20]))
        con.execute("INSERT INTO kunjungan VALUES (?,?,?)",
                    (kid,p,t.isoformat()+f" {rng.randrange(8,21):02d}:{rng.randrange(60):02d}")); kid+=1
print("kunjungan:", con.execute("SELECT COUNT(*) FROM kunjungan").fetchone()[0])'''),
    blok("hasil", "<pre><code>kunjungan: 158</code></pre>", "HARUS MUNCUL"),
    "<p>Satu pelanggan bisa berkunjung belasan kali. Tabel inilah yang di Hari 4 akan kamu pakai untuk "
    "melihat omzetmu melipat jadi tujuh kali lipat, kalau kamu menggabungnya sembarangan.</p>")

langkah("Sel 7 — ekspor kasir",
    blok("aksi", "Sel terakhir untuk membangun. Jalankan.", "LAKUKAN"),
    kode('''nilai = dict(con.execute("""SELECT o.id, SUM(i.jumlah*i.harga_saat_itu) FROM pesanan o
    JOIN item i ON i.pesanan_id=o.id WHERE o.status='selesai' GROUP BY o.id""").fetchall())
info = {r[0]:(r[1],r[2]) for r in con.execute("SELECT id,tanggal,cabang FROM pesanan")}
for oid,v in nilai.items():
    if oid in (7,88,251): continue
    con.execute("INSERT INTO pesanan_kasir VALUES (?,?,?,?)",
                (oid,info[oid][0],info[oid][1],v+{12:50000,199:-25000}.get(oid,0)))
for e,v in [(9001,120000),(9002,75000)]:
    con.execute("INSERT INTO pesanan_kasir VALUES (?,?,?,?)", (e,"2024-04-15","Kemang",v))
con.commit()
print("pesanan_kasir:", con.execute("SELECT COUNT(*) FROM pesanan_kasir").fetchone()[0])'''),
    blok("hasil", "<pre><code>pesanan_kasir: 361</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "Sel ini sengaja membuat ekspor kasir <strong>tidak cocok</strong> dengan "
                    "pembukuan: tiga pesanan tidak ikut terekspor, dua transaksi muncul hanya di "
                    "kasir, dan dua nilai dibuat berbeda. Kamu merekonsiliasi kelimanya di Hari 7."))

langkah("Hitung ulang semuanya sebelum melangkah",
    blok("aksi", "Sel baru. Ini pemeriksaan, bukan pembuatan.", "LAKUKAN"),
    kode('''for t in ["pelanggan","produk","pesanan","item","pegawai","kunjungan","pesanan_kasir"]:
    print(f"{t:<14}", con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "baris")'''),
    blok("hasil", "<pre><code>pelanggan      20 baris\n"
                  "produk         7 baris\n"
                  "pesanan        400 baris\n"
                  "item           788 baris\n"
                  "pegawai        10 baris\n"
                  "kunjungan      158 baris\n"
                  "pesanan_kasir  361 baris</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Kalau angkamu berbeda walau satu baris, berhenti di sini.</strong> "
                   "Jalankan ulang dari sel 1 sampai sel 7, sekali masing-masing, berurutan. "
                   "Seluruh angka di tujuh hari ini dihitung dari basis data itu persis — dan "
                   "mencocokkan dengan basis data yang berbeda cuma akan membuatmu curiga pada "
                   "dirimu sendiri tanpa sebab."))

langkah("Satu alat kecil supaya hasilnya enak dibaca",
    blok("aksi", "Sel baru. Kamu memakai <code>q()</code> ini sepanjang minggu.", "LAKUKAN"),
    kode('''import pandas as pd
def q(sql):
    return pd.read_sql(sql, con)
q("SELECT * FROM produk")'''),
    blok("hasil", "<pre><code>   id          nama kategori  harga  harga_beli\n"
                  "0   1     Kopi Susu  Minuman  22000      7000.0\n"
                  "1   2     Americano  Minuman  18000      5000.0\n"
                  "2   3     Teh Manis  Minuman  10000      2000.0\n"
                  "3   4    Roti Bakar  Makanan  15000      6000.0\n"
                  "4   5     Croissant  Makanan  25000     11000.0\n"
                  "5   6    Cheesecake  Makanan  30000         NaN\n"
                  "6   7  Matcha Latte  Minuman  26000         NaN</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "Colab menampilkan hasil <code>q(...)</code> sebagai tabel rapi berlatar "
                    "putih, bukan teks polos seperti di atas. <strong>Yang perlu kamu cocokkan "
                    "angkanya, bukan spasi dan garisnya.</strong>"))

langkah("Dua sel kosong yang bukan nol",
    blok("aksi", "Lihat lagi dua baris terakhir tabel di atas. Baca kolom "
                 "<code>harga_beli</code>.", "LAKUKAN"),
    "<p>Cheesecake dan Matcha Latte menampilkan <code>NaN</code>. Di basis datanya itu "
    "<code>NULL</code> — harga belinya <strong>belum tercatat</strong>.</p>",
    blok("hasil", "<p>Tiga hal yang sering dikira sama, padahal berbeda: <code>0</code> "
                  "(nol rupiah), <code>''</code> (teks kosong), dan <code>NULL</code> "
                  "(<strong>tidak diketahui</strong>).</p>", "BEDAKAN BERTIGA"),
    "<p>Kalau kamu pernah melihat sel Excel kosong yang tiba-tiba ikut terhitung sebagai nol di "
    "<code>AVERAGE</code>, kamu sudah pernah kena versi Excel-nya.</p>")

langkah("Tebak dulu, jangan langsung dijalankan",
    blok("aksi", "Jawab di kepalamu: apakah <code>NULL = NULL</code> bernilai benar?",
         "LAKUKAN"),
    blok("bahaya", "<strong>Tebak dulu sebelum menggulir.</strong> Kalau kamu langsung membaca "
                   "jawabannya, kamu sedang membaca — bukan berlatih. Wawancara tidak "
                   "menyediakan tombol buka kunci."),
    "<p>Sebagian besar orang menjawab “benar”. Itu jawaban yang wajar, dan itu salah — jadi kalau "
    "itu tebakanmu, kamu sedang berada di tempat yang tepat.</p>")

langkah("Tiga nilai kebenaran, bukan dua",
    blok("aksi", "Sel baru. Sekarang jalankan.", "LAKUKAN"),
    kode('''q("""SELECT NULL = NULL    AS "NULL=NULL",
       NULL <> NULL   AS "NULL<>NULL",
       NULL IS NULL   AS "NULL IS NULL",
       1 = 1          AS benar,
       1 = 2          AS salah""")'''),
    blok("hasil", "<pre><code>  NULL=NULL NULL&lt;&gt;NULL  NULL IS NULL  benar  salah\n"
                  "0      None       None             1      1      0</code></pre>",
         "HARUS MUNCUL"),
    "<p>Di Python, yang sudah kamu pelajari, sebuah perbandingan menghasilkan <code>True</code> atau <code>False</code>. "
    "Di SQL ada <strong>tiga</strong>: benar (1), salah (0), dan <strong>tidak diketahui</strong> "
    "(<code>None</code>).</p>")

langkah("Kenapa aturannya begitu",
    blok("aksi", "Baca kalimat ini pelan-pelan, sekali.", "LAKUKAN"),
    blok("hasil", "<p>Kalau umur dua orang sama-sama <strong>tidak diketahui</strong>, apakah "
                  "umur mereka sama? Kamu tidak tahu. Jawabannya bukan ya, bukan tidak — "
                  "<em>tidak diketahui</em>.</p>", "TERJEMAHANNYA"),
    "<p>Begitu kamu berhenti membaca <code>NULL</code> sebagai “kosong” dan mulai membacanya "
    "sebagai “tidak diketahui”, seluruh aturan yang tadinya terasa rewel jadi masuk akal "
    "sendiri.</p>",
    blok("catatan", "<code>NULL IS NULL</code> tetap bernilai 1. <code>IS NULL</code> tidak "
                    "bertanya “apakah nilainya sama”, ia bertanya “apakah nilainya belum ada”. "
                    "Itu pertanyaan yang selalu bisa dijawab."))

langkah("Layar merah pertamamu minggu ini — dan itu disengaja",
    blok("aksi", "Sel baru. Salah ketik nama kolomnya, dengan sengaja.", "LAKUKAN"),
    kode('q("SELECT nama FROM pelanggan WHERE kotta IS NULL")'),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql 'SELECT nama FROM "
                  "pelanggan WHERE kotta IS NULL': no such column: kotta</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("catatan", "<strong>Layar merah itu kabar baik.</strong> SQL memberitahumu persis di "
                    "mana salahnya: <code>no such column: kotta</code>. Baris terakhir pesan "
                    "error selalu yang paling berguna — <strong>baca dari bawah</strong>."),
    "<p>Ingat rasanya. Besok kamu akan melihat kesalahan yang <em>tidak</em> merah, dan itu "
    "jenis yang mahal.</p>")

HARI1 = {
  "n": "HARI 1", "tab": "1",
  "judul": "Pasang basis datanya, lalu temui NULL",
  "waktu": "± 50 menit",
  "tujuan": "punya <code>senja.db</code> yang angkanya sama persis dengan halaman ini, dan bisa "
            "menyebut ketiga nilai kebenaran SQL.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> tujuh tabel yang kamu bangun sendiri satu per "
           "satu, satu tulisan merah yang kamu picu sendiri, dan satu kalimat: "
           "<code>NULL</code> berarti <em>tidak diketahui</em>, bukan kosong dan bukan nol.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 1 dari 8.</strong> Tutup halaman "
           "ini dan jawab dengan suara: <em>berapa nilai kebenaran yang ada di SQL, dan apa "
           "hasil <code>NULL = NULL</code>?</em></p>"
           "<details><summary>Kunci</summary><p>Tiga: benar, salah, dan tidak diketahui. "
           "<code>NULL = NULL</code> menghasilkan <code>NULL</code> (tidak diketahui) — bukan "
           "benar, bukan salah.</p></details>",
}
