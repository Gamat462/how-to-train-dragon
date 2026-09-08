# -*- coding: utf-8 -*-
"""Hari 4 — memilih tipe data sendiri saat membaca berkas."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Siapkan berkas besarnya",
    blok("aksi", "Kita pakai <code>besar.db</code> dari SQL Mahir L4 (800.000 baris). Salin ke "
                 "<code>proyek/</code>. Kalau belum punya, jalankan ulang <code>besar.py</code> "
                 "dari modul itu.", "LAKUKAN"),
    kode('''import sqlite3, pandas as pd, os
con = sqlite3.connect("besar.db")
pd.read_sql("SELECT * FROM transaksi", con).to_csv("transaksi.csv", index=False)
print(f"{os.path.getsize('transaksi.csv')/1e6:.1f} MB")'''),
    blok("hasil", "<pre><code>39.6 MB</code></pre>", "HARUS MUNCUL"),
    "<p>39,6 MB <strong>di disk</strong>. Ingat angka itu — langkah berikutnya menunjukkan berapa "
    "besar ia jadi di dalam memori.</p>")

langkah("Baca apa adanya, lalu ukur",
    blok("aksi", "Jangan beri petunjuk apa pun ke pandas. Biarkan ia menebak sendiri.", "LAKUKAN"),
    kode('''d1 = pd.read_csv("transaksi.csv")
m1 = d1.memory_usage(deep=True).sum() / 1e6
print(f"apa adanya : {m1:8.1f} MB")'''),
    blok("hasil", "<pre><code>apa adanya :     65.4 MB</code></pre>", "HARUS MUNCUL"),
    "<p>39,6 MB di disk jadi <strong>65,4 MB di memori</strong>. Berkas apa pun selalu membengkak "
    "saat dibaca — pertanyaannya cuma seberapa.</p>",
    blok("bahaya", "<strong>Angkamu bisa jauh lebih besar.</strong> Di pandas 2 baris ini "
                   "menghasilkan sekitar <strong>183 MB</strong> untuk berkas yang sama, karena "
                   "kolom teks disimpan sebagai <code>object</code>. Cek versimu dengan "
                   "<code>pd.__version__</code>."))

langkah("Lihat tebakannya",
    blok("aksi", "Sebelum mengubah apa pun, lihat apa yang ditebak pandas.", "LAKUKAN"),
    kode("print(d1.dtypes.to_string())"),
    blok("hasil", "<pre><code>id              int64\ntanggal           str\ncabang            str\n"
                  "pelanggan_id    int64\nproduk            str\njumlah          int64\n"
                  "nilai           int64</code></pre>", "HARUS MUNCUL"),
    "<p>Semua bilangan jadi <code>int64</code> — delapan bita per angka, apa pun isinya. "
    "Dan <code>tanggal</code> cuma teks: kamu <strong>tidak bisa</strong> memakai "
    "<code>.dt.month</code> atau membandingkan tanggal di kolom ini.</p>")

langkah("Sekarang beri tahu pandas apa yang kamu tahu",
    blok("aksi", "Kamu tahu isi datanya; pandas tidak. Katakan.", "LAKUKAN"),
    kode('''d2 = pd.read_csv("transaksi.csv",
                 dtype={"id":"int32", "cabang":"category", "pelanggan_id":"int32",
                        "produk":"category", "jumlah":"int8", "nilai":"int32"},
                 parse_dates=["tanggal"])
m2 = d2.memory_usage(deep=True).sum() / 1e6
print(f"dipilih    : {m2:8.1f} MB   -> {m1/m2:.1f}x lebih kecil, hemat {m1-m2:.0f} MB")'''),
    blok("hasil", "<pre><code>dipilih    :     18.4 MB   -> 3.6x lebih kecil, hemat 47 MB</code></pre>",
         "HARUS MUNCUL"),
    "<p>65,4 → <strong>18,4 MB</strong>. Berkasnya sendiri 39,6 MB di disk; sekarang isinya muat "
    "di memori dengan setengah dari itu.</p>")

langkah("Pastikan tidak ada angka yang berubah",
    blok("aksi", "Ini langkah yang tidak boleh dilewati.", "LAKUKAN"),
    kode('print("hasil sama?", d1["nilai"].sum() == d2["nilai"].sum())'),
    blok("hasil", "<pre><code>hasil sama? True</code></pre>", "HARUS MUNCUL"),
    "<p>Menghemat memori <strong>tidak boleh mengubah jawabannya</strong> — sama seperti menulis "
    "ulang query demi kecepatan di SQL Mahir L4. Cara memastikannya juga sama: bandingkan.</p>")

langkah("Kenapa tiap penggantian itu aman",
    blok("aksi", "Baca tabel ini sambil melihat baris <code>dtype=</code> yang kamu tulis.", "LAKUKAN"),
    tabel(["Bawaan", "Diganti jadi", "Kenapa aman"],
          [["<code>int64</code> untuk <code>jumlah</code>", "<code>int8</code>",
            "Isinya cuma 1–4. <code>int8</code> menampung −128 sampai 127. Delapan kali lebih kecil."],
           ["<code>int64</code> untuk <code>nilai</code>, <code>id</code>", "<code>int32</code>",
            "Menampung sampai 2,1 miliar. Cukup untuk rupiah per transaksi."],
           ["teks untuk <code>cabang</code>, <code>produk</code>", "<code>category</code>",
            "<strong>Penghemat terbesarnya.</strong> Hanya 5 dan 7 nilai unik di 800.000 baris — "
            "pandas menyimpan daftar pendeknya sekali, lalu 800.000 nomor kecil."],
           ["teks untuk <code>tanggal</code>", "<code>datetime64</code>",
            "Bukan cuma hemat — tanpa ini kamu tidak bisa memakai <code>.dt.month</code>."]]))

langkah("Buktikan sendiri kenapa category yang paling hemat",
    blok("aksi", "Hitung berapa nilai unik di dua kolom itu.", "LAKUKAN"),
    kode('''print("cabang :", d1["cabang"].nunique(), "nilai unik di", f"{len(d1):,}", "baris")
print("produk :", d1["produk"].nunique(), "nilai unik")'''),
    blok("hasil", "<pre><code>cabang : 5 nilai unik di 800,000 baris\nproduk : 7 nilai unik</code></pre>",
         "HARUS MUNCUL"),
    "<p>Lima kata disimpan 800.000 kali, atau lima kata disimpan sekali plus 800.000 nomor. "
    "<code>category</code> memilih yang kedua.</p>",
    blok("catatan", "<strong>Aturannya:</strong> pakai <code>category</code> kalau jumlah nilai "
                    "uniknya <em>jauh</em> lebih kecil daripada jumlah barisnya. Untuk kolom yang "
                    "hampir semua isinya berbeda — nama pelanggan, nomor faktur — "
                    "<code>category</code> justru <strong>memperbesar</strong> pemakaian memori."))

langkah("Batas yang harus kamu tahu sebelum memakai int32 untuk uang",
    blok("aksi", "Jalankan ini sekali. Pelan-pelan.", "LAKUKAN"),
    kode('''import numpy as np
print(np.iinfo("int32").max)
print(np.int32(2147483647) + np.int32(1))'''),
    blok("hasil", "<pre><code>2147483647\n-2147483648</code></pre>",
         "HARUS MUNCUL (mungkin dengan peringatan overflow)"),
    blok("bahaya", "<strong>Angkanya berputar jadi negatif, tanpa error.</strong> "
                   "<code>int32</code> cukup untuk nilai <em>per transaksi</em>, tapi "
                   "<strong>tidak</strong> untuk total kumulatif atau nilai kontrak besar. "
                   "Untuk kolom yang mungkin melewati 2 miliar, tetap <code>int64</code>."),
    "<p>Ini persis jenis kesalahan diam-diam yang kamu latih untuk dicurigai sejak Level 1: "
    "angkanya salah, dan tidak ada yang berteriak.</p>")

langkah("Kapan ini benar-benar menyelamatkanmu",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Colab gratis memberi sekitar <strong>12 GB RAM</strong>. Berkas 400 MB "
                  "yang membengkak jadi 1,8 GB masih muat — tapi begitu kamu meng-"
                  "<code>merge</code> dua tabel seperti itu, salinan sementaranya bisa "
                  "menghabiskan semuanya dan <strong>sesimu mati tanpa penjelasan</strong>.</p>",
         "KENAPA INI PENTING"),
    "<p>Memilih tipe di baris <code>read_csv</code> adalah pencegahan termurah yang ada: "
    "empat baris, sekali tulis.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Dua argumen read_csv yang dipakai hari ini?
2. Kapan "category" menghemat, dan kapan justru memperbesar?
3. Batas int32, dan apa yang terjadi kalau dilewati?
4. Satu langkah yang tidak boleh dilewati setelah mengubah dtype?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>dtype={...}</code> dan <code>parse_dates=[...]</code>. "
    "2. Menghemat kalau nilai uniknya jauh lebih sedikit daripada barisnya; memperbesar kalau "
    "hampir semua isinya berbeda. "
    "3. 2.147.483.647 — dilewati berarti <strong>berputar jadi negatif tanpa error</strong>. "
    "4. Bandingkan hasilnya dengan versi sebelumnya.</p></details>")

HARI4 = {
  "n": "HARI 4",
  "tab": "4",
  "judul": "65 MB jadi 18 MB, hasilnya sama persis",
  "waktu": "± 55 menit",
  "tujuan": "memilih tipe data sendiri saat membaca berkas, dan mengecilkan pemakaian memori "
            "tiga setengah kali <strong>tanpa mengubah satu pun angka hasil</strong>.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> empat baris <code>dtype=</code> yang memangkas "
           "65,4 MB jadi 18,4 MB, dan satu batas angka (2.147.483.647) yang kalau dilewati "
           "merusak datamu tanpa berbunyi.</p>"
           "<p style=\"margin-top:8px\">Besok soal kecepatan — dan satu kata yang sering "
           "diajarkan sebagai “cara benar”, padahal justru yang paling lambat.</p>",
}
