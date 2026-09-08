# -*- coding: utf-8 -*-
"""Hari 1 — membaca rencana eksekusi, dan satu baris CREATE INDEX."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bikin tabel 800.000 baris",
    blok("aksi", "Ambil <code>besar.py</code> dari paket zip "
                 "(<code>data-dan-skrip/sql-mahir/besar.py</code>), taruh di folder yang sama "
                 "dengan <code>senja.db</code>, lalu jalankan.", "LAKUKAN"),
    kode("python besar.py"),
    blok("hasil", "<pre><code>dibuat dalam 3.6 detik\nbaris: 800000\nukuran berkas: 36.7 MB</code></pre>",
         "HARUS MUNCUL"),
    "<p>Baris <em>“dibuat dalam …”</em> boleh beda; mesinmu bukan mesinku. "
    "Dua baris di bawahnya <strong>tidak boleh beda</strong>.</p>",
    blok("catatan", "<strong>Kenapa bukan <code>senja.db</code>?</strong> Isinya 400 pesanan. "
                    "Query apa pun di atasnya selesai dalam sepersekian milidetik, dengan atau "
                    "tanpa index — jadi kamu tidak akan pernah <em>merasakan</em> bedanya, dan "
                    "semua nasihat kinerja akan terdengar seperti teori."))

langkah("Sambungkan, dan hitung barisnya sendiri",
    blok("aksi", "Buka sesi Python baru (atau satu sel Colab). Semua langkah hari ini "
                 "jalan di sesi yang sama, jadi jangan ditutup.", "LAKUKAN"),
    kode("""import sqlite3, time
con = sqlite3.connect("besar.db")
print(con.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0])"""),
    blok("hasil", "<pre><code>800000</code></pre>", "HARUS MUNCUL"),
    "<p>Kamu tidak percaya keluaran <code>besar.py</code> begitu saja — kamu menghitung ulang "
    "dari sisi lain. Kebiasaan ini yang membedakan orang yang datanya bisa dipercaya.</p>")

langkah("Ukur satu query, pakai jam",
    blok("aksi", "Tempel dan jalankan. <code>perf_counter</code> itu stopwatch bawaan Python.", "LAKUKAN"),
    kode("""Q = "SELECT COUNT(*) FROM transaksi WHERE pelanggan_id = 12345"
t = time.perf_counter()
h = con.execute(Q).fetchall()
print(f"{(time.perf_counter()-t)*1000:.1f} ms   hasil = {h[0][0]}")"""),
    blok("hasil", "<pre><code>39.3 ms   hasil = 15</code></pre>", "HARUS MUNCUL"),
    "<p>Angka milidetiknya <strong>akan beda di mesinmu</strong> — 20, 80, terserah. "
    "<code>hasil = 15</code> harus sama.</p>")

langkah("Jangan percaya satu kali ukur — ambil yang tercepat dari tujuh",
    blok("aksi", "Bikin fungsi <code>ukur</code>, lalu panggil untuk <code>Q</code> yang sama.", "LAKUKAN"),
    kode("""def ukur(sql, n=7):
    w = []
    for _ in range(n):
        t = time.perf_counter(); h = con.execute(sql).fetchall()
        w.append(time.perf_counter() - t)
    return min(w) * 1000, h

ms, h = ukur(Q)
print(f"{ms:.1f} ms   hasil = {h[0][0]}")"""),
    blok("hasil", "<pre><code>39.0 ms   hasil = 15</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Yang tercepat, bukan rata-rata.</strong> Yang lambat biasanya bukan salah "
    "query-nya — mesinmu sedang mengurus hal lain. Yang tercepat mendekati biaya query-nya "
    "yang sebenarnya.</p>",
    blok("catatan", "Fungsi <code>ukur</code> ini dipakai sampai Hari 4. Simpan selnya."))

langkah("Minta SQLite menjelaskan rencananya",
    blok("aksi", "Sekarang tanya <em>bagaimana</em> ia mencarinya, bukan berapa lama.", "LAKUKAN"),
    kode("""def rencana(sql):
    for b in con.execute("EXPLAIN QUERY PLAN " + sql):
        print("   ", b[3])

rencana(Q)"""),
    blok("hasil", "<pre><code>    SCAN transaksi</code></pre>", "HARUS MUNCUL"),
    "<p><strong>SCAN</strong> = SQLite membaca <em>semua</em> 800.000 baris satu per satu, "
    "lalu membuang yang tidak cocok. Itu sebabnya 39 milidetik.</p>")

langkah("Kata ketiga yang akan sering kamu lihat",
    blok("aksi", "Jalankan rencana untuk satu query pengelompokan.", "LAKUKAN"),
    kode('rencana("SELECT produk, COUNT(*) FROM transaksi GROUP BY produk")'),
    blok("hasil", "<pre><code>    SCAN transaksi\n    USE TEMP B-TREE FOR GROUP BY</code></pre>",
         "HARUS MUNCUL"),
    tabel(["Kata di rencana", "Artinya", "Rasanya"],
          [["<code>SCAN t</code>", "membaca semua baris tabel <code>t</code>",
            "2× data = 2× lama"],
           ["<code>SEARCH t USING INDEX …</code>", "melompat langsung ke baris yang dicari",
            "hampir tidak peduli tabelnya sebesar apa"],
           ["<code>USE TEMP B-TREE FOR …</code>", "bikin tabel bantu sementara untuk mengurutkan "
            "atau mengelompokkan", "bukan bencana, tapi ada kerja yang mungkin bisa dihemat"]]),
    "<p>Tiga kata ini yang kamu baca seumur hidup. Sisa modul ini cuma memindahkan "
    "<code>SCAN</code> jadi <code>SEARCH</code>.</p>",
    blok("catatan", "<strong>Ini pendalaman dari Minggu 9.</strong> Di M9 kamu memakai "
                    "<code>EXPLAIN QUERY PLAN</code> sekali, untuk melihat bahwa query-mu jalan. "
                    "Di sini kamu memakainya untuk <em>memutuskan</em> — dan mulai Hari 4, "
                    "untuk memutuskan kapan undangan membuat index harus kamu <em>tolak</em>."))

langkah("Satu baris perintah",
    blok("aksi", "Buat index untuk kolom yang barusan di-<code>SCAN</code>.", "LAKUKAN"),
    kode("""t = time.perf_counter()
con.execute("CREATE INDEX idx_pel ON transaksi(pelanggan_id)")
con.commit()
print(f"membuat index: {time.perf_counter()-t:.2f} detik")"""),
    blok("hasil", "<pre><code>membuat index: 0.35 detik</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Yang normal tapi bikin panik:</strong> tidak ada yang tercetak "
                   "selama 1–5 detik, dan berkas <code>besar.db</code> membesar. Dua-duanya benar."))

langkah("Ukur lagi query yang sama persis",
    blok("aksi", "Jangan ubah apa pun di <code>Q</code>. Ukur ulang, 50 kali.", "LAKUKAN"),
    kode("""ms2, h = ukur(Q, n=50)
print(f"{ms2:.3f} ms   hasil = {h[0][0]}")"""),
    blok("hasil", "<pre><code>0.006 ms   hasil = 15</code></pre>", "HARUS MUNCUL"),
    "<p>39,0 ms → 0,006 ms. Di mesinku <strong>6.513 kali lebih cepat</strong>, dan jawabannya "
    "sama persis: 15. Modalnya satu baris perintah dan 0,35 detik, sekali seumur hidup tabel itu.</p>",
    blok("catatan", "Kelipatanmu tidak akan 6.513. Yang penting: <strong>ribuan kali</strong>, "
                    "bukan puluhan persen."))

langkah("Lihat kenapa jadi cepat",
    blok("aksi", "Minta rencananya lagi.", "LAKUKAN"),
    kode("rencana(Q)"),
    blok("hasil", "<pre><code>    SEARCH transaksi USING COVERING INDEX idx_pel (pelanggan_id=?)</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>SCAN</code> berubah jadi <code>SEARCH</code>. Kamu tidak menebaknya — "
    "kamu membacanya.</p>")

langkah("Satu kata yang bisa hilang: COVERING",
    blok("aksi", "Query yang sama, tapi minta kolom lain.", "LAKUKAN"),
    kode("""Q2 = "SELECT SUM(nilai) FROM transaksi WHERE pelanggan_id = 12345"
m, h = ukur(Q2, n=50)
print(f"{m:.3f} ms   hasil = {h[0][0]}")
rencana(Q2)"""),
    blok("hasil", "<pre><code>0.009 ms   hasil = 745000\n"
                  "    SEARCH transaksi USING INDEX idx_pel (pelanggan_id=?)</code></pre>",
         "HARUS MUNCUL"),
    "<p>Kata <strong>COVERING</strong> hilang. Artinya: tadi semua yang dibutuhkan query sudah "
    "ada di dalam index; sekarang <code>nilai</code> tidak ada di sana, jadi SQLite bolak-balik "
    "ke tabelnya. Masih <code>SEARCH</code>, masih cepat — sedikit lebih mahal.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Di kertas, tulis jawaban tiga pertanyaan ini "
                 "<strong>tanpa melihat</strong>.", "LAKUKAN"),
    kode("""1. Perintah apa yang menunjukkan cara SQLite mencari baris?
2. Dua kata yang membedakan "membaca semua" dari "melompat langsung"?
3. Satu baris perintah yang mengubah yang pertama jadi yang kedua?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>EXPLAIN QUERY PLAN &lt;query&gt;</code>. "
    "2. <code>SCAN</code> dan <code>SEARCH</code>. "
    "3. <code>CREATE INDEX nama ON tabel(kolom)</code>.</p></details>",
    blok("catatan", "<strong>Memanggil dari ingatan mengikat; membaca ulang tidak.</strong> "
                    "Kalau ada yang tidak keluar, buka lagi langkahnya — lalu tutup dan tulis lagi."))

HARI1 = {
  "n": "HARI 1",
  "tab": "1",
  "judul": "800.000 baris, supaya lambat itu terasa",
  "waktu": "± 60 menit",
  "tujuan": "membaca <code>EXPLAIN QUERY PLAN</code>, membedakan <code>SCAN</code> dari "
            "<code>SEARCH</code>, dan membuktikan sendiri bahwa satu baris <code>CREATE INDEX</code> "
            "mengubah query 39 milidetik jadi 0,006 milidetik.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu tabel 800.000 baris, dua fungsi "
           "(<code>ukur</code> dan <code>rencana</code>), dan satu pengukuran yang kamu lakukan "
           "sendiri — bukan klaim yang kamu baca.</p>"
           "<p style=\"margin-top:8px\">Kalimat untuk wawancara: <em>“Index itu daftar isi buku. "
           "Tanpa daftar isi, mencari satu bab berarti membalik semua halaman — itu SCAN. "
           "Dengan daftar isi, kamu langsung buka halaman 214 — itu SEARCH.”</em> "
           "Di Hari 4 kamu akan mengukur berapa harga “halaman daftar isi” itu.</p>"
           "<p style=\"margin-top:8px\">Besok: cara paling umum membunuh index yang sudah kamu "
           "punya — dan kamu akan melakukannya sendiri dulu supaya tahu rasanya.</p>",
}
