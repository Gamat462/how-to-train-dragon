# -*- coding: utf-8 -*-
"""Hari 2 — ROWS lawan RANGE: bawaannya bukan yang kamu kira."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Contoh terkecil yang menunjukkan bedanya",
    blok("aksi", "Sel baru. Empat baris, dua di antaranya bernilai kembar.", "LAKUKAN"),
    kode('''q("""
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai,
  SUM(nilai) OVER (ORDER BY nilai
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS pakai_ROWS,
  SUM(nilai) OVER (ORDER BY nilai
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS pakai_RANGE
FROM t ORDER BY nilai, nama""")'''),
    blok("hasil", "<pre><code>  nama  nilai  pakai_ROWS  pakai_RANGE\n0    a     10          10           10\n"
                  "1    b     20          30           50\n2    c     20          50           50\n"
                  "3    d     30          80           80</code></pre>", "HARUS MUNCUL"),
    "<p>Baris <code>b</code> dan <code>c</code> nilainya sama-sama 20. Di situlah kedua kolom "
    "berpisah.</p>")

langkah("Baca dua baris tengahnya",
    blok("aksi", "Lihat lagi baris 1 dan 2 di atas.", "LAKUKAN"),
    tabel(["Cara", "Yang dihitungnya", "Untuk b", "Untuk c"],
          [["<code>ROWS</code>", "baris demi baris", "10+20 = <strong>30</strong>",
            "10+20+20 = <strong>50</strong>"],
           ["<code>RANGE</code>", "berdasarkan <em>nilai</em>; yang seri dilihat sekaligus",
            "<strong>50</strong>", "<strong>50</strong>"]]),
    "<p><code>RANGE</code> memperlakukan seluruh kelompok seri sebagai satu blok. "
    "<code>ROWS</code> tidak peduli nilainya sama atau tidak — ia menghitung cacah baris.</p>")

langkah("Sekarang bagian yang mengejutkan hampir semua orang",
    blok("aksi", "Sel baru. Tulis <strong>tanpa</strong> menyebut frame sama sekali.", "LAKUKAN"),
    kode('''q("""
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai, SUM(nilai) OVER (ORDER BY nilai) AS tanpa_frame
FROM t ORDER BY nilai, nama""")'''),
    blok("hasil", "<pre><code>  nama  nilai  tanpa_frame\n0    a     10           10\n"
                  "1    b     20           50\n2    c     20           50\n"
                  "3    d     30           80</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "10, <strong>50</strong>, 50, 80 — itu kolom <code>pakai_RANGE</code>, bukan "
                   "<code>pakai_ROWS</code>. <strong><code>RANGE</code> adalah bawaannya.</strong> "
                   "Sebagian besar orang mengira sebaliknya, dan tidak pernah memeriksanya."))

langkah("Di data sungguhan, bedanya jadi satu hari penuh",
    blok("aksi", "Sel baru. Contoh tadi terasa buatan; ini tidak.", "LAKUKAN"),
    kode('''q("""
WITH harian AS (
  SELECT o.tanggal, o.cabang, SUM(i.jumlah*i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.tanggal BETWEEN '2024-01-01' AND '2024-01-05'
  GROUP BY o.tanggal, o.cabang)
SELECT tanggal, cabang, nilai,
  SUM(nilai) OVER (ORDER BY tanggal
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_ROWS,
  SUM(nilai) OVER (ORDER BY tanggal
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_RANGE
FROM harian ORDER BY tanggal, cabang""")'''),
    blok("hasil", "<pre><code>      tanggal   cabang   nilai  kum_ROWS  kum_RANGE\n"
                  "0  2024-01-01     Dago  112000    112000     112000\n"
                  "1  2024-01-03     Dago  217000    329000     555000\n"
                  "2  2024-01-03   Kemang  160000    489000     555000\n"
                  "3  2024-01-03  Seturan   66000    555000     555000\n"
                  "4  2024-01-04     Dago  374000    929000    1113000\n"
                  "5  2024-01-04   Kemang   60000    989000    1113000\n"
                  "6  2024-01-04  Seturan  124000   1113000    1113000\n"
                  "7  2024-01-05     Dago  150000   1263000    1263000</code></pre>",
         "HARUS MUNCUL"),
    "<p>Satu tanggal punya tiga baris, karena ada tiga cabang.</p>")

langkah("Tiga angka lawan satu angka",
    blok("aksi", "Lihat tiga baris tanggal 3.", "LAKUKAN"),
    blok("hasil", "<p><code>ROWS</code> memberi <strong>329.000, 489.000, 555.000</strong> — "
                  "tiga angka yang bergantung pada urutan cabang muncul. <code>RANGE</code> "
                  "memberi <strong>555.000</strong> untuk ketiganya.</p>", "YANG HARUS TERLIHAT"),
    "<p>Kalau grafikmu berjudul “penjualan kumulatif per tanggal”, angka untuk tanggal 3 harus "
    "555.000. Angka 329.000 dan 489.000 <strong>tidak menjawab pertanyaan siapa pun</strong> — "
    "mereka “kumulatif sampai sebagian cabang tanggal 3”.</p>")

langkah("Kenapa ROWS di sini bukan cuma salah, tapi tidak stabil",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("bahaya", "Kalau kamu memakai <code>ROWS</code> dan datanya besok datang dengan urutan "
                   "cabang yang berbeda, <strong>angkanya ikut berubah tanpa datanya "
                   "berubah</strong>."),
    "<p>Itu ciri bug yang paling sulit dilacak: laporan yang angkanya bergeser sendiri, tanpa "
    "ada yang mengubah apa pun. Kamu akan menghabiskan sehari mencari perubahan data yang tidak "
    "pernah terjadi.</p>",
    blok("catatan", "Di kertas kerja, angka yang tidak bisa kamu reproduksi minggu depan adalah "
                    "angka yang tidak boleh diserahkan. Aturan itu tidak berubah di SQL."))

langkah("Kapan ROWS justru yang benar",
    blok("aksi", "Baca sekali, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p>Saat frame-nya memang soal <strong>jumlah baris</strong>, bukan soal "
                  "nilai — misalnya rata-rata bergerak tujuh baris terakhir.</p>", "PAKAI ROWS KALAU"),
    "<p>Untuk itu <code>RANGE</code> malah keliru, karena ia menghitung berdasarkan jarak "
    "<em>nilai</em>, bukan cacah baris.</p>")

langkah("Jalankan rata-rata bergerak",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""
WITH harian AS (
  SELECT o.tanggal, SUM(i.jumlah*i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.tanggal)
SELECT tanggal, nilai,
  ROUND(AVG(nilai) OVER (ORDER BY tanggal
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)) AS rata2_7_baris
FROM harian ORDER BY tanggal LIMIT 8""")'''),
    blok("hasil", "<pre><code>      tanggal   nilai  rata2_7_baris\n"
                  "0  2024-01-01  112000       112000.0\n"
                  "1  2024-01-03  443000       277500.0\n"
                  "2  2024-01-04  558000       371000.0\n"
                  "3  2024-01-05  150000       315750.0\n"
                  "4  2024-01-06  422000       337000.0\n"
                  "5  2024-01-08  162000       307833.0\n"
                  "6  2024-01-09  399000       320857.0\n"
                  "7  2024-01-10   18000       307429.0</code></pre>", "HARUS MUNCUL"),
    "<p>Tujuh baris terakhir, digeser satu per satu. Baris pertama cuma punya dirinya sendiri, "
    "jadi rata-ratanya sama dengan nilainya.</p>")

langkah("Perhatikan tanggal yang hilang dari daftar itu",
    blok("aksi", "Baca kolom tanggal di atas dari atas ke bawah.", "LAKUKAN"),
    blok("hasil", "<p>2 Januari dan 7 Januari <strong>tidak ada</strong>. Jadi “rata-rata 7 "
                  "baris terakhir” bukan “rata-rata 7 hari terakhir”.</p>",
         "YANG TIDAK KAMU MINTA"),
    "<p>Yang kamu dapat adalah rata-rata tujuh <em>hari yang ada transaksinya</em> — dan itu "
    "selalu lebih tinggi daripada rata-rata tujuh hari kalender.</p>",
    blok("catatan", "<strong>Ini bukan kesalahan frame-mu; ini kesalahan datanya.</strong> "
                    "Hari 6 memperbaikinya dengan membuat deret tanggal lengkap lebih dulu, "
                    "supaya hari kosong punya baris bernilai nol."))

langkah("Layar merah: frame yang ditulis terbalik",
    blok("aksi", "Sel baru. Tukar urutan batas frame-nya, dengan sengaja.", "LAKUKAN"),
    kode('''q("""
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20))
SELECT SUM(nilai) OVER (ORDER BY nilai
     ROWS BETWEEN CURRENT ROW AND UNBOUNDED PRECEDING) FROM t""")'''),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': near "
                  "\"PRECEDING\": syntax error</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Batas frame selalu ditulis <strong>dari yang lebih awal ke yang lebih akhir</strong>. "
    "<code>UNBOUNDED PRECEDING</code> tidak bisa berada di sisi kanan <code>AND</code>.</p>")

langkah("Layar merah: RANGE dengan angka, tanpa ORDER BY",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20))
SELECT SUM(nilai) OVER (RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) FROM t""")'''),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': RANGE with offset "
                  "PRECEDING/FOLLOWING requires one ORDER BY expression</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("catatan", "<strong>Pesan errornya sedang mengajarimu artinya <code>RANGE</code>.</strong> "
                    "“<code>1 PRECEDING</code>” di <code>RANGE</code> berarti “nilai yang "
                    "selisihnya paling jauh 1” — dan itu mustahil dinilai kalau SQL tidak tahu "
                    "kolom mana yang jadi ukurannya."))

langkah("Aturan yang menutup seluruh hari ini",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    blok("hasil", "<p><strong>Selalu tulis frame-nya secara eksplisit</strong>, walaupun "
                  "bawaannya sudah benar.</p>", "SATU ATURAN"),
    tabel(["Pertanyaanmu", "Frame yang benar"],
          [["Kumulatif per tanggal (satu tanggal banyak baris)",
            "<code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>"],
           ["Rata-rata bergerak N baris",
            "<code>ROWS BETWEEN (N-1) PRECEDING AND CURRENT ROW</code>"],
           ["Total seluruh kelompok (bukan kumulatif)",
            "<code>ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING</code>"]]),
    "<p>Query yang menyebut frame-nya memberitahu pembaca berikutnya bahwa kamu memang "
    "<strong>memilih</strong>, bukan kebetulan mendapat bawaan. Pembaca berikutnya itu sering "
    "kali kamu sendiri, tiga bulan lagi.</p>")

langkah("Kerjakan sendiri",
    blok("aksi", "Ambil query “data sungguhan” di langkah 4. Ubah supaya kumulatifnya dihitung "
                 "<strong>terpisah per cabang</strong>, bukan digabung. Lalu jawab dengan suara: "
                 "setelah diubah begitu, apakah <code>ROWS</code> dan <code>RANGE</code> masih "
                 "berbeda hasilnya?", "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<p>Tambahkan <code>PARTITION BY cabang</code> di kedua <code>OVER</code>-nya:</p>"
    "<div class=\"kode\"><pre><code>SUM(nilai) OVER (PARTITION BY cabang ORDER BY tanggal\n"
    "     RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)</code></pre></div>"
    "<p><strong>Tidak lagi berbeda</strong> — dan itu jawaban yang penting. Setelah dipartisi "
    "per cabang, tiap cabang hanya punya <em>satu</em> baris per tanggal, jadi tidak ada nilai "
    "seri untuk diperlakukan berbeda. <code>ROWS</code> dan <code>RANGE</code> memberi angka "
    "yang sama.</p>"
    "<p>Pelajarannya: bedanya baru muncul kalau ada <strong>seri</strong> di kolom "
    "<code>ORDER BY</code>-mu. Kalau kamu tidak yakin ada seri atau tidak, "
    "<code>SELECT tanggal, COUNT(*) ... GROUP BY tanggal HAVING COUNT(*) &gt; 1</code> "
    "menjawabnya dalam sepuluh detik.</p></details>")

HARI2 = {
  "n": "HARI 2", "tab": "2",
  "judul": "ROWS lawan RANGE: bawaannya bukan yang kamu kira",
  "waktu": "± 55 menit",
  "tujuan": "menjelaskan kenapa running total per tanggal bisa memberi dua jawaban berbeda, dan "
            "memilih yang benar dengan sadar.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>ORDER BY</code> di dalam <code>OVER</code> "
           "diam-diam memasang frame “dari awal sampai baris ini” · bawaannya "
           "<code>RANGE</code>, yang memperlakukan nilai seri sebagai satu blok · "
           "<code>ROWS</code> menghitung baris demi baris dan hasilnya bergantung urutan · dan "
           "tulis frame-nya selalu.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 2 dari 8.</strong> Jawab dengan "
           "suara: <em>frame apa yang jadi bawaan kalau ada <code>ORDER BY</code> tapi "
           "frame-nya tidak ditulis?</em></p>"
           "<details><summary>Kunci</summary><p><code>RANGE BETWEEN UNBOUNDED PRECEDING AND "
           "CURRENT ROW</code> — bukan <code>ROWS</code>.</p></details>",
}
