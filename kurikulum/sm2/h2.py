# -*- coding: utf-8 -*-
"""Hari 2 — ROWS, RANGE, GROUPS: frame yang menentukan jawabannya."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Contoh terkecil yang menunjukkan bedanya",
    blok("aksi", "Berkas <code>senja/l2-hari-2.sql</code>. Empat baris, dua di antaranya "
                 "bernilai kembar.", "LAKUKAN"),
    kode('''WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai,
  sum(nilai) OVER (ORDER BY nilai
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS pakai_rows,
  sum(nilai) OVER (ORDER BY nilai
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS pakai_range
FROM t ORDER BY nilai, nama;'''),
    keluaran(H, "h2_kecil"),
    "<p>Baris <code>b</code> dan <code>c</code> nilainya sama-sama 20. Di situlah kedua kolom yang "
    "kamu hitung berpisah — dan kalau kamu tidak tahu bedanya, kamu akan memilih salah satunya "
    "tanpa sadar.</p>")

langkah("Baca dua baris tengahnya",
    blok("aksi", "Lihat lagi baris <code>b</code> dan <code>c</code> di atas.", "LAKUKAN"),
    tabel(["Cara", "Yang dihitungnya", "Untuk b", "Untuk c"],
          [["<code>ROWS</code>", "baris demi baris", "10+20 = <strong>30</strong>",
            "10+20+20 = <strong>50</strong>"],
           ["<code>RANGE</code>", "berdasarkan <em>nilai</em>; yang seri dilihat sekaligus",
            "<strong>50</strong>", "<strong>50</strong>"]]),
    "<p><code>RANGE</code> memperlakukan seluruh kelompok seri sebagai satu blok. "
    "<code>ROWS</code> tidak peduli nilainya sama atau tidak — ia menghitung cacah baris.</p>")

langkah("Sekarang bagian yang mengejutkan hampir semua orang",
    blok("aksi", "Tulis <strong>tanpa</strong> menyebut frame sama sekali.", "LAKUKAN"),
    kode('''WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai, sum(nilai) OVER (ORDER BY nilai) AS tanpa_frame
FROM t ORDER BY nilai, nama;'''),
    keluaran(H, "h2_tanpa_frame"),
    blok("bahaya", "10, <strong>50</strong>, 50, 80 — itu kolom <code>pakai_range</code>, bukan "
                   "<code>pakai_rows</code>. <strong><code>RANGE</code> adalah bawaannya.</strong> "
                   "Sebagian besar orang mengira sebaliknya, dan tidak pernah memeriksanya."))

langkah("Ada frame ketiga yang hampir tidak pernah disebut: GROUPS",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai,
  sum(nilai) OVER (ORDER BY nilai
       GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS pakai_groups
FROM t ORDER BY nilai, nama;'''),
    keluaran(H, "h2_groups"),
    "<p><code>GROUPS</code> menghitung dalam satuan <strong>kelompok nilai seri</strong>. "
    "“1 PRECEDING” berarti satu kelompok ke belakang: untuk <code>d</code> (30), yang ikut "
    "adalah kelompok 20 — yaitu <code>b</code> dan <code>c</code> — jadi 20+20+30 = 70.</p>",
    blok("catatan", "<code>GROUPS</code> ada sejak PostgreSQL 11 dan hampir tidak pernah "
                    "diajarkan. Kamu jarang membutuhkannya, tapi mengenalinya membuat "
                    "<code>ROWS</code> dan <code>RANGE</code> jadi masuk akal: ketiganya "
                    "menjawab pertanyaan “berapa jauh ke belakang”, dengan satuan yang berbeda — "
                    "baris, nilai, dan kelompok."))

langkah("Lihat dulu isi harian yang akan kamu pakai",
    blok("aksi", "Lima hari pertama Januari, dipecah per cabang.", "LAKUKAN"),
    kode("""SELECT o.tanggal, o.cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-05'
GROUP BY o.tanggal, o.cabang ORDER BY o.tanggal, o.cabang;"""),
    keluaran(H, "h2_cte_harian"),
    "<p>Delapan baris untuk lima hari. Perhatikan: <strong>tanggal 3 dan 4 punya tiga baris "
    "masing-masing, tanggal 2 tidak ada sama sekali.</strong> Dua fakta itu yang akan menggigit "
    "kamu di dua langkah berikutnya.</p>")

langkah("Di data sungguhan, bedanya jadi satu hari penuh",
    blok("aksi", "Contoh tadi terasa buatan; ini tidak.", "LAKUKAN"),
    kode('''WITH harian AS (
  SELECT o.tanggal, o.cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-05'
  GROUP BY o.tanggal, o.cabang)
SELECT tanggal, cabang, nilai,
  sum(nilai) OVER (ORDER BY tanggal
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_rows,
  sum(nilai) OVER (ORDER BY tanggal
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_range
FROM harian ORDER BY tanggal, cabang;'''),
    keluaran(H, "h2_sungguhan"),
    "<p>Satu tanggal punya tiga baris di layarmu, karena ada tiga cabang. Itu bentuk yang sama "
    "seperti buku besar: satu tanggal, banyak baris, dan kamu harus memutuskan apakah "
    "menjumlahkannya per baris atau per tanggal.</p>")

langkah("Buktikan bahwa serinya memang ada",
    blok("aksi", "Sebelum menyalahkan frame, periksa dulu apakah ada nilai kembar di kolom "
                 "<code>ORDER BY</code>-mu.", "LAKUKAN"),
    kode("""SELECT tanggal, count(*) AS baris
FROM (SELECT DISTINCT tanggal, cabang FROM pesanan
      WHERE status='selesai' AND tanggal <= DATE '2024-01-05') x
GROUP BY tanggal HAVING count(*) > 1 ORDER BY tanggal;"""),
    keluaran(H, "h2_cek_seri"),
    "<p>Dua tanggal punya tiga baris. <strong>Kalau query ini kosong, <code>ROWS</code> dan "
    "<code>RANGE</code> akan memberimu angka yang sama</strong> dan kamu tidak perlu memilih. "
    "Sepuluh detik untuk tahu apakah kamu sedang berada di wilayah bahaya.</p>")

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

langkah("Kapan ROWS justru yang benar — dan kapan ia menipu",
    blok("aksi", "Rata-rata bergerak tujuh. Dua cara, berdampingan.", "LAKUKAN"),
    kode('''WITH harian AS (
  SELECT o.tanggal, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.tanggal <= DATE '2024-01-12'
  GROUP BY o.tanggal)
SELECT tanggal, nilai,
  round(avg(nilai) OVER (ORDER BY tanggal
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))                  AS rata2_7_baris,
  round(avg(nilai) OVER (ORDER BY tanggal
        RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)) AS rata2_7_hari
FROM harian ORDER BY tanggal;'''),
    keluaran(H, "h2_rata_bergerak"),
    "<p>Lima baris pertama sama. Mulai <strong>8 Januari</strong> keduanya berpisah: 307.833 "
    "lawan 347.000. Kalau kamu terlanjur menyerahkan yang satu dan ditanya soal yang lain, "
    "kamu harus bisa menjelaskan bedanya — bukan mengubahnya diam-diam.</p>")

langkah("Cari sendiri kenapa mereka berpisah",
    blok("aksi", "Tebak dulu, baru jalankan.", "LAKUKAN"),
    kode('''SELECT d::date AS tanggal
FROM generate_series(DATE '2024-01-01', DATE '2024-01-12', INTERVAL '1 day') AS d
WHERE NOT EXISTS (SELECT 1 FROM pesanan o
                  WHERE o.tanggal = d::date AND o.status='selesai');'''),
    keluaran(H, "h2_hari_hilang"),
    blok("hasil", "<p>Dua hari tanpa transaksi. <code>ROWS 6 PRECEDING</code> menghitung "
                  "<strong>tujuh baris</strong> — jadi ia menjangkau sampai sembilan hari ke "
                  "belakang. <code>RANGE INTERVAL '6 days'</code> menghitung <strong>tujuh hari "
                  "kalender</strong>, apa pun jumlah barisnya.</p>", "PENYEBABNYA"),
    "<p>Kalau judul kolommu berbunyi “rata-rata 7 hari”, yang benar adalah "
    "<code>RANGE INTERVAL</code>. Kalau berbunyi “rata-rata 7 transaksi terakhir”, yang benar "
    "<code>ROWS</code>. <strong>Judulnya yang menentukan frame-nya, bukan sebaliknya.</strong>")

langkah("Layar merah: frame yang ditulis terbalik",
    blok("aksi", "Tukar urutan batas frame-nya, dengan sengaja.", "LAKUKAN"),
    kode('''WITH t(n) AS (VALUES (10),(20))
SELECT sum(n) OVER (ORDER BY n
     ROWS BETWEEN CURRENT ROW AND UNBOUNDED PRECEDING) FROM t;'''),
    keluaran(H, "h2_merah_frame_terbalik"),
    "<p>Batas frame selalu ditulis <strong>dari yang lebih awal ke yang lebih akhir</strong>. "
    "<code>UNBOUNDED PRECEDING</code> tidak bisa berada di sisi kanan <code>AND</code>.</p>")

langkah("Layar merah: RANGE dengan angka, tanpa ORDER BY",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH t(n) AS (VALUES (10),(20))
SELECT sum(n) OVER (RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) FROM t;'''),
    keluaran(H, "h2_merah_range_tanpa_order"),
    blok("catatan", "<strong>Pesan errornya sedang mengajarimu artinya <code>RANGE</code>.</strong> "
                    "“<code>1 PRECEDING</code>” di <code>RANGE</code> berarti “nilai yang "
                    "selisihnya paling jauh 1” — dan itu mustahil dinilai kalau PostgreSQL tidak "
                    "tahu kolom mana yang jadi ukurannya. Perhatikan kata "
                    "<em>exactly one</em>: dua kolom pun ditolak."))

langkah("Aturan yang menutup seluruh hari ini",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    blok("hasil", "<p><strong>Selalu tulis frame-nya secara eksplisit</strong>, walaupun "
                  "bawaannya sudah benar.</p>", "SATU ATURAN"),
    tabel(["Pertanyaanmu", "Frame yang benar"],
          [["Kumulatif per tanggal (satu tanggal banyak baris)",
            "<code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>"],
           ["Rata-rata N <em>hari</em> terakhir",
            "<code>RANGE BETWEEN INTERVAL 'N days' PRECEDING AND CURRENT ROW</code>"],
           ["Rata-rata N <em>baris</em> terakhir",
            "<code>ROWS BETWEEN (N-1) PRECEDING AND CURRENT ROW</code>"],
           ["Total seluruh kelompok (bukan kumulatif)",
            "<code>ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING</code>"]]),
    "<p>Query yang menyebut frame-nya memberitahu pembaca berikutnya bahwa kamu memang "
    "<strong>memilih</strong>, bukan kebetulan mendapat bawaan. Pembaca berikutnya itu sering "
    "kali kamu sendiri, tiga bulan lagi.</p>")

langkah("Kerjakan sendiri",
    blok("aksi", "Ambil query “data sungguhan” di langkah 5. Ubah supaya kumulatifnya dihitung "
                 "<strong>terpisah per cabang</strong>. Lalu jawab dengan suara: setelah diubah "
                 "begitu, apakah <code>ROWS</code> dan <code>RANGE</code> masih berbeda "
                 "hasilnya?", "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<p>Tambahkan <code>PARTITION BY cabang</code> di kedua <code>OVER</code>-nya:</p>"
    + keluaran(H, "h2_kunci", tag="HASILNYA") +
    "<p><strong>Tidak lagi berbeda</strong> — dan itu jawaban yang penting. Setelah dipartisi "
    "per cabang, tiap cabang hanya punya <em>satu</em> baris per tanggal, jadi tidak ada nilai "
    "seri untuk diperlakukan berbeda.</p>"
    "<p>Pelajarannya: bedanya baru muncul kalau ada <strong>seri</strong> di kolom "
    "<code>ORDER BY</code>-mu. Kalau kamu tidak yakin ada seri atau tidak, "
    "<code>SELECT tanggal, count(*) … GROUP BY tanggal HAVING count(*) &gt; 1</code> "
    "menjawabnya dalam sepuluh detik.</p></details>")

HARI2 = {
  "n": "HARI 2", "tab": "2",
  "judul": "ROWS, RANGE, GROUPS: bawaannya bukan yang kamu kira",
  "waktu": "± 60 menit",
  "tujuan": "menjelaskan kenapa running total per tanggal bisa memberi dua jawaban berbeda, dan "
            "memilih frame-nya dari judul kolom yang kamu janjikan.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>ORDER BY</code> di dalam <code>OVER</code> "
           "diam-diam memasang frame “dari awal sampai baris ini” · bawaannya "
           "<code>RANGE</code>, yang memperlakukan nilai seri sebagai satu blok · "
           "<code>ROWS</code> menghitung baris, <code>RANGE</code> menghitung nilai, "
           "<code>GROUPS</code> menghitung kelompok seri · dan “7 baris” bukan “7 hari” kalau "
           "ada hari yang bolong.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 2 dari 8.</strong> Jawab dengan "
           "suara: <em>frame apa yang jadi bawaan kalau ada <code>ORDER BY</code> tapi "
           "frame-nya tidak ditulis?</em></p>"
           "<details><summary>Kunci</summary><p><code>RANGE BETWEEN UNBOUNDED PRECEDING AND "
           "CURRENT ROW</code> — bukan <code>ROWS</code>.</p></details>",
}
