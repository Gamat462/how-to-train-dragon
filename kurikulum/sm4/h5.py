# -*- coding: utf-8 -*-
"""Hari 5 — subquery berkorelasi, dan beban yang tumbuh seperti kuadrat."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bikin tabel 10.000 baris — sengaja kecil",
    blok("aksi", "Sesi Python baru. Skrip ini bikin <code>q2.db</code> sendiri.", "LAKUKAN"),
    kode("""import sqlite3, time, os
if os.path.exists("q2.db"): os.remove("q2.db")
c = sqlite3.connect("q2.db")
c.execute("ATTACH 'besar.db' AS b")
c.execute("CREATE TABLE kecil AS SELECT * FROM b.transaksi WHERE id <= 10000")
c.commit(); c.execute("DETACH b")
print("baris:", c.execute("SELECT COUNT(*) FROM kecil").fetchone()[0])"""),
    blok("hasil", "<pre><code>baris: 10000</code></pre>", "HARUS MUNCUL"),
    "<p>Sepuluh ribu, bukan 800.000. Kamu akan tahu alasannya begitu melihat angka di langkah 3.</p>")

langkah("Tulis dua versi dari satu pertanyaan yang sama",
    blok("aksi", "Pertanyaannya: <em>di tiap cabang, berapa transaksi yang nilainya di atas "
                 "rata-rata cabang itu sendiri?</em> Tempel dua-duanya, jangan dijalankan dulu.", "LAKUKAN"),
    kode("""korelasi = \"\"\"SELECT cabang, COUNT(*) AS di_atas_rata FROM kecil t1
WHERE nilai > (SELECT AVG(nilai) FROM kecil t2 WHERE t2.cabang = t1.cabang)
GROUP BY cabang ORDER BY cabang\"\"\"

cte = \"\"\"WITH rata AS (SELECT cabang, AVG(nilai) AS r FROM kecil GROUP BY cabang)
SELECT t.cabang, COUNT(*) AS di_atas_rata FROM kecil t
JOIN rata ON rata.cabang = t.cabang
WHERE t.nilai > rata.r
GROUP BY t.cabang ORDER BY t.cabang\"\"\""""),
    blok("hasil", "<p>Tidak ada yang tercetak. Dua variabel tersimpan.</p>", "HARUS MUNCUL"),
    "<p>Bedanya cuma di mana rata-ratanya dihitung. Versi pertama menghitungnya "
    "<em>di dalam</em> <code>WHERE</code>; versi kedua menghitungnya sekali di depan.</p>")

langkah("Jalankan yang pertama, dan tunggu",
    blok("aksi", "Jalankan. Lalu duduk dan perhatikan berapa lama.", "LAKUKAN"),
    kode("""t = time.perf_counter(); rk = c.execute(korelasi).fetchall()
print(f"{(time.perf_counter()-t)*1000:.1f} ms")
for x in rk: print("   ", x)"""),
    blok("hasil", "<pre><code>6200.6 ms\n"
                  "    ('Dago', 869)\n    ('Kemang', 879)\n    ('Renon', 877)\n"
                  "    ('Seturan', 933)\n    ('Seturan2', 881)</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Yang normal tapi bikin panik:</strong> 3–15 detik tanpa apa pun di "
                   "layar. Jangan tekan Ctrl-C. Itu memang inti pelajarannya."))

langkah("Tanya kenapa",
    blok("aksi", "Minta rencananya. Cari kata yang belum pernah kamu lihat.", "LAKUKAN"),
    kode("""for p in c.execute("EXPLAIN QUERY PLAN " + korelasi): print("   ", p[3])"""),
    blok("hasil", "<pre><code>    SCAN t1\n    CORRELATED SCALAR SUBQUERY 1\n"
                  "    SCAN t2\n    USE TEMP B-TREE FOR GROUP BY</code></pre>", "HARUS MUNCUL"),
    "<p><strong>CORRELATED</strong> artinya subquery itu menyebut <code>t1.cabang</code> — "
    "sesuatu dari baris yang sedang diproses di luar. Jawabannya beda untuk tiap baris, "
    "jadi SQLite tidak bisa menghitungnya sekali lalu menyimpannya.</p>",
    blok("catatan", "<code>SCAN t2</code> di dalam <code>SCAN t1</code>: menjalankan ulang "
                    "<code>AVG</code> atas 10.000 baris, untuk <strong>tiap satu dari 10.000 "
                    "baris</strong>. Itu 100 juta pembacaan untuk menjawab pertanyaan yang "
                    "sebenarnya cuma butuh <strong>lima</strong> angka."))

langkah("Jalankan yang kedua",
    blok("aksi", "Query yang menjawab pertanyaan yang sama persis.", "LAKUKAN"),
    kode("""w = []
for _ in range(5):
    t = time.perf_counter(); rc = c.execute(cte).fetchall(); w.append(time.perf_counter()-t)
print(f"{min(w)*1000:.1f} ms")
print("sama?", rk == rc)"""),
    blok("hasil", "<pre><code>6.0 ms\nsama? True</code></pre>", "HARUS MUNCUL"),
    "<p><strong>6.200,6 ms lawan 6,0 ms</strong> — sekitar seribu kali. Dan "
    "<code>sama? True</code>: angka hasilnya sepuluh-sepuluhnya identik. "
    "Yang berbeda cuma berapa lama menunggunya.</p>")

langkah("Lihat rencananya juga",
    blok("aksi", "Bandingkan dengan rencana di langkah 4.", "LAKUKAN"),
    kode("""for p in c.execute("EXPLAIN QUERY PLAN " + cte): print("   ", p[3])"""),
    blok("hasil", "<pre><code>    CO-ROUTINE rata\n    SCAN kecil\n"
                  "    USE TEMP B-TREE FOR GROUP BY\n    SCAN t\n"
                  "    SEARCH rata USING AUTOMATIC COVERING INDEX (cabang=?)\n"
                  "    USE TEMP B-TREE FOR GROUP BY</code></pre>", "HARUS MUNCUL"),
    "<p>Rencananya <em>lebih panjang</em>, dan seribu kali lebih cepat. "
    "<strong>Panjang rencana bukan ukuran biaya.</strong> Yang mahal adalah "
    "<code>CORRELATED</code> — pekerjaan yang diulang, bukan pekerjaan yang banyak.</p>")

langkah("Buktikan polanya di lima ukuran tabel",
    blok("aksi", "Skrip ini butuh sekitar <strong>3 menit</strong>. Jalankan, lalu tinggalkan.", "LAKUKAN"),
    kode("""c.execute("ATTACH 'besar.db' AS b")
print(f"{'baris':>8} {'berkorelasi':>14} {'CTE':>10}   kelipatan")
for n in [2500, 5000, 10000, 20000, 40000]:
    c.execute("DROP TABLE IF EXISTS kecil")
    c.execute(f"CREATE TABLE kecil AS SELECT * FROM b.transaksi WHERE id <= {n}")
    c.commit()
    t = time.perf_counter(); rk = c.execute(korelasi).fetchall(); tk = time.perf_counter()-t
    w = []
    for _ in range(5):
        t = time.perf_counter(); rc = c.execute(cte).fetchall(); w.append(time.perf_counter()-t)
    print(f"{n:>8} {tk*1000:>12.1f}ms {min(w)*1000:>8.1f}ms   {tk/min(w):>8.0f}x   sama={rk==rc}")"""),
    blok("hasil", "<pre><code>   baris    berkorelasi        CTE   kelipatan\n"
                  "    2500        382.6ms      1.4ms        273x   sama=True\n"
                  "    5000       1582.8ms      2.7ms        580x   sama=True\n"
                  "   10000       6247.2ms      5.7ms       1095x   sama=True\n"
                  "   20000      25134.3ms     11.4ms       2206x   sama=True\n"
                  "   40000     106286.7ms     24.9ms       4275x   sama=True</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "Baris terakhir sendirian makan <strong>106 detik</strong>. Itu memang "
                   "disengaja — kamu perlu <em>menunggunya</em>, bukan membaca angkanya."))

langkah("Baca kedua kolom itu dari atas ke bawah",
    blok("aksi", "Bandingkan dua deret angka ini. Tidak ada yang dijalankan.", "LAKUKAN"),
    tabel(["Baris jadi 2× lipat", "Berkorelasi", "CTE"],
          [["382 → 1.583", "<strong>4× lipat</strong>", "1,4 → 2,7 = 2× lipat"],
           ["1.583 → 6.247", "<strong>4× lipat</strong>", "2,7 → 5,7 = 2× lipat"],
           ["6.247 → 25.134", "<strong>4× lipat</strong>", "5,7 → 11,4 = 2× lipat"],
           ["25.134 → 106.287", "<strong>4× lipat</strong>", "11,4 → 24,9 = 2× lipat"]]),
    "<p>Dua kali baris → <strong>empat</strong> kali waktu. Itu tanda beban yang naik seperti "
    "kuadrat. Kolom CTE: dua kali baris → dua kali waktu. Lurus.</p>")

langkah("Hitung sendiri kenapa aku tidak menjalankannya di 800.000",
    blok("aksi", "Satu perkalian di kalkulator.", "LAKUKAN"),
    kode("""800000 / 40000        # = 20 kali lipat barisnya
20 * 20               # = 400 kali lipat waktunya (karena kuadrat)
106.3 * 400 / 3600    # jam""", salin=False),
    blok("hasil", "<pre><code>± 11,8 jam</code></pre>", "HITUNGANMU HARUS MENDEKATI"),
    "<p>Itu <strong>perkiraan, bukan pengukuran</strong> — aku tidak menjalankannya sampai "
    "selesai, dan kamu juga sebaiknya tidak.</p>",
    blok("catatan", "<strong>Inilah bentuk kegagalan yang paling berbahaya.</strong> Query ini "
                    "<em>tampak sehat</em> di data contoh 2.500 baris — 0,4 detik, siapa yang "
                    "peduli — lalu menggantung semalaman di data klien yang sebenarnya. "
                    "Dan tidak ada index yang bisa menolongnya."))

langkah("Kenali bentuknya tanpa menjalankan apa pun",
    blok("aksi", "Baca dua query ini dan cari bedanya sendiri sebelum membaca kalimat di bawahnya.", "LAKUKAN"),
    kode("""-- BERKORELASI (mahal): 'p' di dalam kurung datang dari luar kurung
SELECT p.nama,
       (SELECT COUNT(*) FROM pesanan WHERE pelanggan_id = p.id) AS jumlah
FROM pelanggan p

-- TIDAK berkorelasi (murah): isi kurung berdiri sendiri
SELECT nama FROM produk
WHERE harga > (SELECT AVG(harga) FROM produk)""", salin=False),
    blok("hasil", "<p>Tandanya: ada <code>SELECT</code> di dalam kurung, <strong>dan di dalam "
                  "kurung itu disebut nama tabel dari luar</strong>.</p>", "YANG DICARI"),
    "<p>Yang kedua aman — dihitung sekali, hasilnya dipakai berulang. Yang pertama adalah "
    "bentuk yang barusan kamu ukur.</p>")

langkah("Latihan: tulis ulang yang mahal itu",
    blok("aksi", "Ubah query berkorelasi di atas supaya tidak berkorelasi lagi, jalankan di "
                 "<code>senja.db</code>, lalu bandingkan hasilnya. <strong>Baru</strong> buka kuncinya.", "LAKUKAN"),
    "<details><summary>Buka kunci jawaban</summary>"
    + kode("""import sqlite3, pandas as pd
s = sqlite3.connect("senja.db")
baru = \"\"\"SELECT p.nama, COUNT(o.id) AS jumlah_pesanan
FROM pelanggan p
LEFT JOIN pesanan o ON o.pelanggan_id = p.id
GROUP BY p.id, p.nama ORDER BY jumlah_pesanan DESC, p.nama LIMIT 5\"\"\"
print(pd.read_sql(baru, s))""")
    + "</details>",
    blok("hasil", "<pre><code>     nama  jumlah_pesanan\n0    Rina              32\n1    Lita              30\n"
                  "2   Dimas              26\n3  Hendra              26\n4    Bayu              25</code></pre>",
         "HARUS MUNCUL"),
    "<p>Identik dengan versi berkorelasinya. Di <code>senja.db</code> yang cuma 20 pelanggan, "
    "dua-duanya selesai seketika — <strong>dan itu justru masalahnya</strong>.</p>")

langkah("Satu jebakan di jawaban itu: LEFT, bukan JOIN biasa",
    blok("aksi", "Jalankan ini untuk melihat apa yang hilang kalau <code>LEFT</code> dilupakan.", "LAKUKAN"),
    kode("""print(s.execute(\"\"\"SELECT p.id, p.nama FROM pelanggan p
LEFT JOIN pesanan o ON o.pelanggan_id = p.id
WHERE o.id IS NULL ORDER BY p.id\"\"\").fetchall())"""),
    blok("hasil", "<pre><code>[(18, 'Bagus'), (19, 'Vira'), (20, 'Andi')]</code></pre>", "HARUS MUNCUL"),
    "<p>Tiga pelanggan yang belum pernah pesan — yang kamu temukan di Level 1. Versi berkorelasi "
    "memberi mereka angka <strong>0</strong>. <code>JOIN</code> biasa "
    "<strong>menghilangkan mereka dari daftar sama sekali</strong>: 17 baris, bukan 20.</p>",
    blok("bahaya", "<strong>Menulis ulang query demi kecepatan tidak boleh diam-diam mengubah "
                   "jawabannya.</strong> Cara memastikannya cuma satu, dan kamu sudah melakukannya "
                   "di langkah 5: <code>sama? True</code>. Bandingkan hasil kedua versi, selalu."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Hapus <code>q2.db</code>, tutup halaman ini, jawab di kertas.", "LAKUKAN"),
    kode("""c.close(); os.remove("q2.db")

# 1. Kata apa di rencana yang berarti "pekerjaan ini diulang tiap baris"?
# 2. Kalau baris jadi 2x dan waktu jadi 4x, apa artinya?
# 3. Kenapa index tidak menolong kasus ini?
# 4. Satu hal yang wajib dicek setelah menulis ulang query demi kecepatan?"""),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>CORRELATED SCALAR SUBQUERY</code>. "
    "2. Bebannya kuadrat — data 20× lipat berarti waktu ±400× lipat. "
    "3. Index memperbaiki <em>cara mencari baris</em>, bukan <em>berapa kali pekerjaan yang sama "
    "diulang</em>. "
    "4. Bahwa hasilnya masih identik.</p></details>")

HARI5 = {
  "n": "HARI 5",
  "tab": "5",
  "judul": "Lambat karena bentuk query-nya, bukan karena index",
  "waktu": "± 75 menit (satu langkah menunggu 3 menit)",
  "tujuan": "mengenali <strong>subquery berkorelasi</strong> di rencana eksekusi, menulis ulangnya "
            "jadi CTE, dan mengukur sendiri bahwa bebannya tumbuh seperti kuadrat — kelambatan "
            "yang tidak bisa disembuhkan index apa pun.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu kata yang harus kamu cari di tiap rencana "
           "(<code>CORRELATED</code>), satu tanda yang bisa kamu lihat dari teks query-nya saja, "
           "dan satu tabel lima baris yang kamu ukur sendiri selama tiga menit menunggu.</p>"
           "<p style=\"margin-top:8px\">Kebiasaan ini harus kamu bangun <strong>sekarang, di data "
           "kecil, di saat tidak ada bedanya</strong> — karena di saat bedanya terasa, kamu sudah "
           "di depan klien.</p>"
           "<p style=\"margin-top:8px\">Besok berhenti soal kecepatan. Besok soal <strong>Rp 400.000 "
           "yang menguap di antara dua baris perintah</strong> — dan itu bagian yang paling dekat "
           "dengan latar belakangmu.</p>",
}
