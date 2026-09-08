# -*- coding: utf-8 -*-
"""Hari 6 — berkas yang lebih besar daripada memorimu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Alat ukur baru: puncak memori, bukan cuma waktu",
    blok("aksi", "Sesi Python baru. <code>tracemalloc</code> itu bawaan Python, tidak perlu "
                 "dipasang.", "LAKUKAN"),
    kode('''import pandas as pd, time, tracemalloc
BERKAS = "transaksi.csv"

def puncak(f):
    """Jalankan f, kembalikan (detik, puncak MB, hasil)."""
    tracemalloc.start()
    t = time.perf_counter(); hasil = f(); dt = time.perf_counter() - t
    _, puncak_b = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return dt, puncak_b/1e6, hasil'''),
    blok("hasil", "<p>Tidak ada yang tercetak.</p>", "HARUS MUNCUL"),
    "<p>Sampai kemarin kamu mengukur <strong>waktu</strong>. Hari ini yang menentukan adalah "
    "<strong>memori tertinggi yang sempat dipakai</strong> — karena itu yang membunuh sesimu.</p>")

langkah("Cara pertama: muat semuanya",
    blok("aksi", "Tugasnya: omzet per cabang. Cara yang selama ini kamu pakai.", "LAKUKAN"),
    kode('''def sekaligus():
    return pd.read_csv(BERKAS).groupby("cabang")["nilai"].sum().sort_index()

t1, m1, h1 = puncak(sekaligus)
print(f"muat sekaligus   : {t1:5.2f} detik | puncak memori {m1:7.1f} MB")'''),
    blok("hasil", "<pre><code>muat sekaligus   :  0.86 detik | puncak memori    78.9 MB</code></pre>",
         "HARUS MUNCUL"),
    "<p>78,9 MB untuk menjawab pertanyaan yang hasilnya <strong>lima angka</strong>. "
    "Seluruh tujuh kolom dimuat, padahal yang dipakai cuma dua.</p>")

langkah("Cara kedua: baca sepotong-sepotong",
    blok("aksi", "Perhatikan tiga hal baru: <code>usecols</code>, <code>dtype</code>, dan "
                 "<code>chunksize</code>.", "LAKUKAN"),
    kode('''def bertahap(chunk=100_000):
    total = {}
    for bagian in pd.read_csv(BERKAS, usecols=["cabang","nilai"],
                              dtype={"cabang":"category","nilai":"int32"},
                              chunksize=chunk):
        for k, v in bagian.groupby("cabang", observed=True)["nilai"].sum().items():
            total[k] = total.get(k, 0) + v
    return pd.Series(total).sort_index()'''),
    blok("hasil", "<p>Belum dijalankan — langkah berikutnya.</p>", "HARUS MUNCUL"),
    "<p><code>chunksize=100_000</code> mengubah <code>read_csv</code> dari “kembalikan satu "
    "DataFrame” jadi “kembalikan potongan satu per satu”. Delapan potongan untuk 800.000 baris.</p>")

langkah("Ukur, dan bandingkan hasilnya",
    blok("aksi", "Jalankan, lalu pastikan jawabannya identik.", "LAKUKAN"),
    kode('''t2, m2, h2 = puncak(bertahap)
print(f"bertahap (chunk) : {t2:5.2f} detik | puncak memori {m2:7.1f} MB  <- {m1/m2:.0f}x lebih hemat")
print("hasil sama?", (h1.values == h2.values).all())'''),
    blok("hasil", "<pre><code>bertahap (chunk) :  0.29 detik | puncak memori     2.9 MB  <- 27x lebih hemat\n"
                  "hasil sama? True</code></pre>", "HARUS MUNCUL"),
    "<p><strong>78,9 MB jadi 2,9 MB, dan waktunya justru tiga kali lebih cepat.</strong> "
    "Pertukaran yang hampir gratis.</p>",
    blok("catatan", "Yang membuatnya <em>juga</em> lebih cepat bukan <code>chunksize</code>, tapi "
                    "<code>usecols</code>: lima kolom yang tidak dipakai tidak pernah dibaca "
                    "sama sekali."))

langkah("Pola chunksize selalu tiga langkah",
    blok("aksi", "Lihat lagi fungsi <code>bertahap</code> dan cari ketiganya.", "LAKUKAN"),
    kode("""total = {}                      # 1. wadah kosong DI LUAR perulangan
for bagian in ...chunksize=...: # 2. untuk tiap potongan, hitung ringkasannya
    total[k] = total.get(k,0)+v # 3. gabungkan ke wadah""", salin=False),
    blok("bahaya", "<strong>Yang tidak boleh:</strong> menumpuk potongannya dalam sebuah list "
                   "lalu <code>pd.concat</code> di akhir. Itu memuat semuanya juga — cuma dengan "
                   "cara yang lebih berbelit dan lebih boros."))

langkah("Yang tidak bisa dikerjakan bertahap",
    blok("aksi", "Baca sekali. Ini batasnya.", "LAKUKAN"),
    blok("hasil", "<p>Apa pun yang butuh <strong>melihat seluruh data sekaligus</strong>: median, "
                  "urutan global, deduplikasi menyeluruh, atau <code>merge</code> besar.</p>",
         "TIDAK BISA DI-CHUNK"),
    "<p>Untuk itu jawabannya bukan chunk, tapi <strong>serahkan ke basis data</strong>: muat ke "
    "DuckDB atau SQLite, lalu kerjakan dengan SQL. Itu sebabnya SQL Produksi datang sebelum "
    "modul ini.</p>",
    blok("catatan", "Jumlah dan hitungan bisa digabung dari potongan; <strong>median tidak "
                    "bisa</strong>. Median dari dua potongan bukan rata-rata dari dua median."))

langkah("Cara ketiga: generator",
    blok("aksi", "Perhatikan satu kata: <code>yield</code>.", "LAKUKAN"),
    kode('''import csv

def baris_besar(path, ambang):
    """Keluarkan baris satu per satu; jangan pernah simpan semuanya."""
    with open(path, newline="") as f:
        for baris in csv.DictReader(f):
            if int(baris["nilai"]) > ambang:
                yield baris'''),
    blok("hasil", "<p>Belum ada keluaran.</p>", "HARUS MUNCUL"),
    "<p><code>yield</code>-lah yang membuatnya generator: fungsi ini <strong>berhenti</strong> di "
    "situ, menyerahkan satu baris, lalu melanjutkan dari titik yang sama saat diminta lagi. "
    "Ia tidak pernah memegang lebih dari satu baris.</p>")

langkah("Ukur harganya",
    blok("aksi", "Jalankan. Yang ini lambat — biarkan.", "LAKUKAN"),
    kode('''def hitung_generator():
    n = jml = 0
    for b in baris_besar(BERKAS, 100_000):
        n += 1; jml += int(b["nilai"])
    return n, jml

t3, m3, h3 = puncak(hitung_generator)
print(f"generator : {t3:5.2f} detik | puncak memori {m3:7.1f} MB")
print(f"  transaksi > 100.000: {h3[0]:,} baris, nilai {h3[1]:,}")'''),
    blok("hasil", "<pre><code>generator :  7.05 detik | puncak memori     0.0 MB\n"
                  "  transaksi &gt; 100,000: 57,459 baris, nilai 6,433,560,000</code></pre>",
         "HARUS MUNCUL"),
    "<p><strong>Puncak memori 0,0 MB — dan 7,05 detik, delapan kali lebih lambat</strong> "
    "daripada muat sekaligus. Itu harganya, dan halaman ini tidak menyembunyikannya.</p>")

langkah("Tiga cara, satu tabel",
    blok("aksi", "Ketiga barisnya kamu ukur sendiri hari ini.", "LAKUKAN"),
    tabel(["Cara", "Waktu", "Puncak memori", "Pakai kalau"],
          [["Muat sekaligus", "0,86 dtk", "78,9 MB",
            "Datanya muat. <strong>Ini bawaan yang benar</strong> — jangan merumitkan tanpa sebab."],
           ["<code>chunksize</code>", "0,29 dtk", "2,9 MB",
            "Tidak muat, tapi tugasnya bisa diringkas bertahap. <strong>Pilihan pertama saat "
            "mentok.</strong>"],
           ["Generator", "7,05 dtk", "~0 MB",
            "Sangat besar, dan tugasnya sebaris-sebaris: menyaring, mengubah bentuk, menulis ulang."]]),
    "<p>Baris pertama yang paling sering benar. <strong>Jangan pakai chunk untuk berkas 5 MB.</strong></p>")

langkah("Kenapa generator tetap layak dipelajari meski paling lambat",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Ia satu-satunya yang <strong>tidak peduli seberapa besar berkasnya</strong> "
                  "— 40 MB atau 40 GB, pemakaian memorinya sama.</p>", "ALASANNYA"),
    "<p>Dan <code>yield</code> muncul di banyak tempat lain: membaca log, memanggil API "
    "berhalaman, memproses berkas satu per satu dari folder. Tapi untuk pekerjaan analis "
    "sehari-hari, <strong><code>chunksize</code> hampir selalu jawaban yang benar</strong>.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Tiga langkah pola chunksize?
2. Satu argumen read_csv yang membuat chunk JUGA lebih cepat, bukan cuma hemat?
3. Satu perhitungan yang tidak bisa dikerjakan bertahap, dan jalan keluarnya?
4. Kata apa yang membuat sebuah fungsi jadi generator?
5. Cara mana yang harus jadi pilihan pertamamu?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Wadah kosong di luar perulangan → ringkas tiap potongan → gabungkan ke wadah. "
    "2. <code>usecols</code>. "
    "3. Median (juga urutan global, deduplikasi, merge besar) — jalan keluarnya "
    "<strong>serahkan ke basis data</strong>. "
    "4. <code>yield</code>. "
    "5. <strong>Muat sekaligus</strong>, selama datanya muat.</p></details>")

HARI6 = {
  "n": "HARI 6",
  "tab": "6",
  "judul": "Berkas yang lebih besar daripada memorimu",
  "waktu": "± 65 menit",
  "tujuan": "memproses berkas yang tidak muat di RAM, dan tahu <strong>harga</strong> yang harus "
            "dibayar untuk tiap caranya.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu tabel tiga baris yang seluruh angkanya kamu "
           "ukur sendiri, dan satu alat ukur baru (<code>tracemalloc</code>) yang menjawab "
           "pertanyaan yang selama ini tidak bisa kamu jawab: <em>berapa memori yang sebenarnya "
           "dipakai kodeku?</em></p>"
           "<p style=\"margin-top:8px\">Besok hari terakhir: mengubah semua ini jadi "
           "<strong>satu perintah</strong> yang bisa dipasang di jadwal dan dipercaya berjalan "
           "tanpa kamu tonton.</p>",
}
