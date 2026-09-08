# -*- coding: utf-8 -*-
"""Hari 1 — apa yang sebenarnya dikerjakan OVER."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buka kembali basis datanya",
    blok("aksi", "Colab baru. Kalau <code>senja.db</code> dari Level 1 masih ada, cukup "
                 "sambungkan lagi.", "LAKUKAN"),
    kode('''import sqlite3, pandas as pd
con = sqlite3.connect("senja.db")
def q(sql): return pd.read_sql(sql, con)
q("SELECT COUNT(*) AS pesanan FROM pesanan")'''),
    blok("hasil", "<pre><code>   pesanan\n0      400</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau yang muncul <code>no such table: pesanan</code>, itu wajar</strong> "
                    "— sesi Colab-mu sudah berakhir dan berkasnya ikut hilang. Jalankan ulang "
                    "tujuh sel pembuat <code>senja.db</code> dari Level 1 Hari 1, sekali "
                    "berurutan, lalu kembali ke sini."))

langkah("GROUP BY meringkas, dan itu memang gunanya",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT cabang, SUM(i.jumlah*i.harga_saat_itu) AS nilai_cabang
     FROM pesanan o JOIN item i ON i.pesanan_id = o.id
     WHERE o.status='selesai' GROUP BY cabang ORDER BY cabang""")'''),
    blok("hasil", "<pre><code>    cabang  nilai_cabang\n0     Dago      12665000\n"
                  "1   Kemang      11669000\n2  Seturan      11405000</code></pre>",
         "HARUS MUNCUL"),
    "<p>Tiga baris, dari 788 baris item. Rinciannya hilang — dan untuk pertanyaan “berapa total "
    "tiap cabang”, itu justru yang kamu mau.</p>")

langkah("Pertanyaan yang GROUP BY tidak bisa jawab",
    blok("aksi", "Baca sekali. Jangan ketik apa-apa dulu.", "LAKUKAN"),
    blok("hasil", "<p><em>“Tiap baris item itu berapa persen dari total cabangnya?”</em></p>",
         "PERTANYAANNYA"),
    "<p>Untuk menjawabnya kamu butuh <strong>baris aslinya dan totalnya berdampingan</strong>. "
    "GROUP BY sudah membuang baris aslinya sebelum kamu sempat memakainya.</p>")

langkah("Window function menghitung tanpa membuang satu baris pun",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT o.id, o.cabang,
       i.jumlah*i.harga_saat_itu AS nilai_baris,
       SUM(i.jumlah*i.harga_saat_itu) OVER (PARTITION BY o.cabang) AS nilai_cabang,
       ROUND(i.jumlah*i.harga_saat_itu * 100.0 /
             SUM(i.jumlah*i.harga_saat_itu) OVER (PARTITION BY o.cabang), 3) AS persen
     FROM pesanan o JOIN item i ON i.pesanan_id = o.id
     WHERE o.status='selesai' ORDER BY o.cabang, o.id LIMIT 6""")'''),
    blok("hasil", "<pre><code>   id cabang  nilai_baris  nilai_cabang  persen\n"
                  "0   1   Dago        22000      12665000   0.174\n"
                  "1   1   Dago        88000      12665000   0.695\n"
                  "2   1   Dago       104000      12665000   0.821\n"
                  "3   3   Dago        66000      12665000   0.521\n"
                  "4  10   Dago        45000      12665000   0.355\n"
                  "5  10   Dago        50000      12665000   0.395</code></pre>", "HARUS MUNCUL"),
    "<p>Barisnya utuh, dan totalnya ikut menempel di sebelahnya.</p>")

langkah("Buktinya ada di kolom keempat",
    blok("aksi", "Bandingkan <code>nilai_cabang</code> di atas dengan hasil GROUP BY di "
                 "langkah 2.", "LAKUKAN"),
    blok("hasil", "<p><strong>12.665.000</strong> berulang di tiap baris — angka yang sama "
                  "persis dengan hasil GROUP BY tadi.</p>", "YANG HARUS TERLIHAT"),
    "<p>Itu bukti bahwa keduanya menghitung hal yang sama. Bedanya cuma window function "
    "<strong>menempelkannya ke tiap baris</strong>, bukan menggantikan barisnya.</p>")

langkah("Empat kata yang memberitahumu jawabannya window function",
    blok("aksi", "Salin ke catatanmu, lalu ucapkan kalimat pertamanya dengan suara keras.",
         "LAKUKAN"),
    blok("hasil", "<p>GROUP BY menjawab <em>“berapa totalnya”</em>. Window function menjawab "
                  "<em>“berapa bagian baris ini dari totalnya”</em>.</p>", "SATU KALIMAT"),
    tabel(["Kalau pertanyaannya mengandung…", "Alatnya"],
          [["“dibanding”, “berapa persen dari”", "window function"],
           ["“peringkat ke berapa”, “tiga teratas per…”", "window function"],
           ["“dibanding bulan sebelumnya”, “selisih dari yang lalu”", "window function"],
           ["“berjalan”, “kumulatif”, “rata-rata bergerak”", "window function"]]),
    "<p>Empat kata itu — <strong>dibanding, peringkat, sebelumnya, berjalan</strong> — hampir "
    "selalu berarti kamu tidak boleh membuang barisnya.</p>")

langkah("Layar merah pertamamu minggu ini — dan itu disengaja",
    blok("aksi", "Sel baru. Coba saring pakai window function.", "LAKUKAN"),
    kode('''q("""SELECT cabang FROM pesanan
     WHERE ROW_NUMBER() OVER (ORDER BY id) = 1""")'''),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': misuse of window "
                  "function ROW_NUMBER()</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Kamu sudah punya penjelasannya dari Level 1 Hari 6: <code>WHERE</code> berjalan "
    "<strong>sebelum</strong> baris-barisnya lengkap dikumpulkan, jadi tidak ada “urutan” yang "
    "bisa dinomori.</p>")

langkah("Di mana window function berjalan di dalam urutan itu",
    blok("aksi", "Baca sekali, lalu lanjut.", "LAKUKAN"),
    kode('''FROM → WHERE → GROUP BY → HAVING → WINDOW → SELECT → ORDER BY → LIMIT
                                    ^^^^^^
                       di sini, hampir paling akhir''', salin=False),
    blok("hasil", "<p>Window function dihitung <strong>setelah</strong> <code>WHERE</code>, "
                  "<code>GROUP BY</code>, dan <code>HAVING</code> selesai.</p>", "AKIBATNYA"),
    "<p>Jadi kamu tidak bisa menyaring dengan hasil window function di query yang sama. "
    "Obatnya selalu satu: <strong>bungkus dengan CTE, lalu saring di luarnya</strong> — pola "
    "yang kamu pakai berkali-kali di Level 3.</p>")

langkah("Tiga bagian di dalam OVER",
    blok("aksi", "Salin tabel ini. Kamu akan kembali ke sini sepanjang minggu.", "LAKUKAN"),
    tabel(["Bagian", "Artinya", "Kalau kamu hilangkan"],
          [["<code>PARTITION BY</code>", "Bagi jadi kelompok, hitung ulang tiap kelompok",
            "Seluruh tabel jadi satu kelompok"],
           ["<code>ORDER BY</code>", "Urutkan di dalam kelompok",
            "Tidak ada urutan — dan frame jadi seluruh kelompok"],
           ["<code>ROWS</code>/<code>RANGE</code> (frame)", "Baris mana saja yang ikut dihitung",
            "Bawaannya berubah tergantung ada <code>ORDER BY</code> atau tidak"]]),
    "<p>Baris ketiga itu isi seluruh Hari 2, dan <strong>hampir tidak pernah diajarkan</strong>. "
    "Modul M6 tidak pernah menyebutnya sama sekali.</p>")

langkah("Buktikan baris pertama tabel itu",
    blok("aksi", "Sel baru. Hilangkan <code>PARTITION BY</code>-nya.", "LAKUKAN"),
    kode('''q("""SELECT o.cabang, i.jumlah*i.harga_saat_itu AS nilai_baris,
       SUM(i.jumlah*i.harga_saat_itu) OVER () AS semua_cabang
     FROM pesanan o JOIN item i ON i.pesanan_id = o.id
     WHERE o.status='selesai' ORDER BY o.cabang, o.id LIMIT 3""")'''),
    blok("hasil", "<pre><code>  cabang  nilai_baris  semua_cabang\n"
                  "0   Dago        22000      35739000\n"
                  "1   Dago        88000      35739000\n"
                  "2   Dago       104000      35739000</code></pre>", "HARUS MUNCUL"),
    "<p>35.739.000 — total seluruh cabang, angka yang sama dengan yang kamu hitung di Level 1 "
    "Hari 4 dan Hari 7. <code>OVER ()</code> yang kosong berarti “satu kelompok berisi "
    "semuanya”.</p>")

langkah("Sekarang buktikan baris kedua, dan bersiaplah terkejut",
    blok("aksi", "Sel baru. Dua kolom, bedanya cuma dua kata.", "LAKUKAN"),
    kode('''q("""
WITH b AS (SELECT substr(o.tanggal,1,7) AS bulan, SUM(i.jumlah*i.harga_saat_itu) AS nilai
           FROM pesanan o JOIN item i ON i.pesanan_id=o.id
           WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  SUM(nilai) OVER ()                  AS tanpa_order_by,
  SUM(nilai) OVER (ORDER BY bulan)    AS pakai_order_by
FROM b ORDER BY bulan""")'''),
    blok("hasil", "<pre><code>     bulan    nilai  tanpa_order_by  pakai_order_by\n"
                  "0  2024-01  5968000        35739000         5968000\n"
                  "1  2024-02  6351000        35739000        12319000\n"
                  "2  2024-03  5574000        35739000        17893000\n"
                  "3  2024-04  5754000        35739000        23647000\n"
                  "4  2024-05  6272000        35739000        29919000\n"
                  "5  2024-06  5820000        35739000        35739000</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "Kolom ketiga memberi <strong>total</strong>. Kolom keempat memberi "
                   "<strong>running total</strong>. Yang kamu tambahkan cuma dua kata: "
                   "<code>ORDER BY bulan</code>."))

langkah("Dua kata itu diam-diam memasang frame",
    blok("aksi", "Baca sekali, pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Menambahkan <code>ORDER BY</code> ke dalam <code>OVER</code> tidak cuma "
                  "mengurutkan. Ia <strong>mengubah frame</strong> dari “seluruh kelompok” "
                  "menjadi “dari awal sampai baris ini”.</p>", "YANG SEBENARNYA TERJADI"),
    "<p>Itu sebabnya <code>SUM(...) OVER (PARTITION BY x)</code> memberi total, sedangkan "
    "<code>SUM(...) OVER (PARTITION BY x ORDER BY y)</code> memberi running total — perubahan "
    "besar dari menambahkan dua kata yang kelihatannya cuma soal urutan.</p>",
    blok("catatan", "Kalau kamu pernah bingung kenapa angka kumulatifmu tiba-tiba jadi total, "
                    "atau sebaliknya, <strong>ini penyebabnya</strong>. Besok kamu akan melihat "
                    "sisi yang lebih halus lagi dari frame yang sama."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis query yang menampilkan, untuk <strong>Januari 2024</strong>: nilai "
                 "penjualan tiap cabang, dan berapa persen tiap cabang dari total Januari. "
                 "Pakai window function, bukan dua query.", "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>q(\"\"\"\n"
    "WITH b AS (SELECT o.cabang, substr(o.tanggal,1,7) AS bulan,\n"
    "                  SUM(i.jumlah*i.harga_saat_itu) AS nilai\n"
    "           FROM pesanan o JOIN item i ON i.pesanan_id=o.id\n"
    "           WHERE o.status='selesai' GROUP BY 1,2)\n"
    "SELECT cabang, bulan, nilai,\n"
    "  ROUND(nilai*100.0/SUM(nilai) OVER (PARTITION BY bulan),1) AS persen_bulan\n"
    "FROM b WHERE bulan='2024-01' ORDER BY cabang\"\"\")</code></pre></div>"
    "<pre><code>    cabang    bulan    nilai  persen_bulan\n"
    "0     Dago  2024-01  2834000          47.5\n"
    "1   Kemang  2024-01  1255000          21.0\n"
    "2  Seturan  2024-01  1879000          31.5</code></pre>"
    "<p>Pemeriksaanmu: 47,5 + 21,0 + 31,5 = <strong>100,0</strong>. Kalau jumlahnya bukan 100, "
    "partisimu salah — kemungkinan besar kamu memakai <code>PARTITION BY cabang</code> padahal "
    "yang dibagi adalah bulannya.</p>"
    "<p>Perhatikan juga <code>WHERE bulan='2024-01'</code> berada <strong>di luar</strong> CTE. "
    "Kalau penyaring itu kamu taruh di dalam, hasilnya tetap sama di sini — tapi begitu kamu "
    "menyaring <em>setelah</em> window function menghitung, urutannya jadi penting. Itu bahan "
    "Level 3.</p></details>")

HARI1 = {
  "n": "HARI 1", "tab": "1",
  "judul": "Apa yang sebenarnya dikerjakan OVER",
  "waktu": "± 50 menit",
  "tujuan": "menjelaskan beda window function dan <code>GROUP BY</code> dalam satu kalimat, dan "
            "tahu kapan hanya window function yang bisa menjawab.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> GROUP BY meringkas dan membuang baris; window "
           "function menghitung sambil menyimpan semua baris · <code>PARTITION BY</code> = "
           "kelompok, <code>ORDER BY</code> = urutan <em>dan</em> diam-diam mengubah frame · "
           "window function berjalan setelah <code>WHERE</code>, jadi tidak bisa dipakai di "
           "sana.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 1 dari 8.</strong> Jawab dengan "
           "suara, satu kalimat: <em>apa beda <code>GROUP BY</code> dan window function?</em></p>"
           "<details><summary>Kunci</summary><p><code>GROUP BY</code> meringkas banyak baris "
           "jadi satu; window function menghitung hal yang sama tanpa membuang baris.</p></details>",
}
