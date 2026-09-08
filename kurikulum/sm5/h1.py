# -*- coding: utf-8 -*-
"""Hari 1 — kerangka empat langkah, dan jebakan NOT IN."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Hafalkan empat langkah ini sebelum menyentuh keyboard",
    blok("aksi", "Salin tabel ini ke catatanmu. Kamu akan memakainya di tiap soal "
                 "sepanjang minggu ini.", "LAKUKAN"),
    tabel(["Langkah", "Yang kamu ucapkan"],
          [["1. Ulangi soalnya", "“Jadi yang dicari … per … untuk periode …, betul?”"],
           ["2. Sebut asumsimu", "“Aku hitung hanya pesanan selesai, dan buang yang "
            "<code>pelanggan_id</code>-nya kosong. Kalau kamu mau yang lain, bilang.”"],
           ["3. Tulis dari <code>FROM</code>, bukan dari <code>SELECT</code>",
            "“Tabel mana dulu … disambung ke apa … disaring apa … baru dikelompokkan.”"],
           ["4. Periksa jawabanmu", "“Ada 400 pesanan, hasilnya 362 — sisanya batal. Masuk akal.”"]]),
    "<p>Pewawancara SQL yang bagus tidak memeriksa hafalanmu. Ia memeriksa "
    "<strong>apakah kamu berpikir sebelum mengetik</strong>.</p>")

langkah("Langkah 4 adalah keunggulanmu, dan kamu belum menyadarinya",
    blok("aksi", "Baca sekali, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p>Kamu sudah bertahun-tahun terbiasa bertanya <em>“ini balance "
                  "tidak?”</em> sebelum menyerahkan apa pun. <strong>Kebanyakan kandidat data "
                  "analyst tidak punya refleks itu</strong> — mereka menjalankan query, melihat "
                  "ada angka keluar, lalu menyerahkannya.</p>", "YANG KAMU BAWA DARI KAP"),
    "<p>Ucapkan pemeriksaanmu <strong>dengan suara keras</strong> di wawancara. Itu bukan "
    "basa-basi; itu barang daganganmu, dan kamu satu-satunya kandidat yang punya stoknya.</p>")

langkah("Soal yang paling sering dipakai memisahkan kandidat",
    blok("aksi", "Pertanyaannya sederhana: <strong>berapa pelanggan yang belum pernah "
                 "memesan sama sekali?</strong> Tulis query-mu di kertas <em>sebelum</em> "
                 "menjalankan apa pun.", "LAKUKAN"),
    kode("""-- tulis jawabanmu di sini dulu, jangan dijalankan
SELECT ... FROM pelanggan WHERE ...""", salin=False),
    blok("bahaya", "<strong>Jangan lompat ke langkah berikutnya sebelum kamu menulis sesuatu.</strong> "
                   "Kalau kamu membaca jawabannya dulu, kamu sedang membaca — bukan berlatih. "
                   "Wawancara tidak menyediakan tombol buka kunci."))

langkah("Jalankan versi yang paling wajar ditulis orang",
    blok("aksi", "Sambungkan ke <code>senja.db</code>, lalu jalankan.", "LAKUKAN"),
    kode('''import sqlite3
con = sqlite3.connect("senja.db")
a = "SELECT COUNT(*) FROM pelanggan WHERE id NOT IN (SELECT pelanggan_id FROM pesanan)"
print("NOT IN     :", con.execute(a).fetchone()[0])'''),
    blok("hasil", "<pre><code>NOT IN     : 0</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Nol.</strong> Kalau jawabanmu tadi juga <code>NOT IN</code>, kamu baru saja "
    "menulis kalimat “semua pelanggan kita aktif” ke dalam laporan — dengan percaya diri "
    "penuh.</p>")

langkah("Sekarang tanya hal yang sama dengan cara lain",
    blok("aksi", "Query berbeda, pertanyaan identik.", "LAKUKAN"),
    kode('''b = """SELECT COUNT(*) FROM pelanggan pl
       WHERE NOT EXISTS (SELECT 1 FROM pesanan p WHERE p.pelanggan_id = pl.id)"""
print("NOT EXISTS :", con.execute(b).fetchone()[0])'''),
    blok("hasil", "<pre><code>NOT EXISTS : 3</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Nol lawan tiga.</strong> Dan yang berbahaya: nol <em>bukan</em> pesan error. "
    "Nol adalah jawaban yang enak dibaca.</p>")

langkah("Cari penyebabnya sendiri, jangan percaya penjelasanku dulu",
    blok("aksi", "Satu query. Tebak dulu angkanya sebelum menjalankan.", "LAKUKAN"),
    kode('print(con.execute("SELECT COUNT(*) FROM pesanan WHERE pelanggan_id IS NULL").fetchone()[0])'),
    blok("hasil", "<pre><code>12</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau angkamu bukan 12</strong>, <code>senja.db</code>-mu bukan yang "
                    "dibuat <code>gen_final.py</code>. Bikin ulang dulu — seluruh angka minggu "
                    "ini bergantung padanya, dan mencocokkan dengan basis data yang berbeda cuma "
                    "akan membuatmu curiga pada dirimu sendiri tanpa sebab."),
    "<p>Dua belas baris <code>pesanan.pelanggan_id</code> berisi <code>NULL</code>. Itulah "
    "seluruh sebabnya, dan sekarang kamu menemukannya sendiri.</p>")

langkah("Kenapa satu NULL merusak seluruh NOT IN",
    blok("aksi", "Baca dua kalimat ini pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Ketika SQL memeriksa <code>18 NOT IN (5, 9, NULL, …)</code>, ia harus "
                  "memutuskan apakah 18 berbeda dari <code>NULL</code> — dan jawabannya bukan "
                  "“ya”, bukan “tidak”, tapi <strong>tidak diketahui</strong>.</p>",
         "LOGIKA TIGA NILAI"),
    "<p>Satu <code>NULL</code> saja di dalam daftar membuat seluruh <code>NOT IN</code> "
    "<strong>tidak pernah bisa bernilai benar, untuk baris mana pun</strong>. Hasilnya nol "
    "baris, selamanya.</p>")

langkah("Tambalan yang masih boleh dipakai — dan kenapa kamu sebaiknya tidak",
    blok("aksi", "Versi ketiga: <code>NOT IN</code> yang disembuhkan.", "LAKUKAN"),
    kode('''c = """SELECT COUNT(*) FROM pelanggan
       WHERE id NOT IN (SELECT pelanggan_id FROM pesanan
                        WHERE pelanggan_id IS NOT NULL)"""
print("NOT IN + IS NOT NULL :", con.execute(c).fetchone()[0])'''),
    blok("hasil", "<pre><code>NOT IN + IS NOT NULL : 3</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Benar, tapi menuntutmu mengingat.</strong> Kamu harus menambahkan "
                    "<code>IS NOT NULL</code> itu tiap kali, seumur hidup, di tiap "
                    "<code>NOT IN</code> yang kamu tulis. <code>NOT EXISTS</code> tidak menuntutmu "
                    "mengingat apa pun — dan biasanya juga lebih cepat."),
    "<p>Aturan yang layak kamu hafalkan mati-matian: <strong>jangan pakai <code>NOT IN</code> "
    "pada subquery, titik.</strong></p>")

langkah("Kesalahan sepupunya, yang juga diam",
    blok("aksi", "Jalankan dua baris ini. Salah satunya salah, dan tidak ada yang "
                 "memberitahumu.", "LAKUKAN"),
    kode('''print("= NULL  :", con.execute("SELECT COUNT(*) FROM pesanan WHERE pelanggan_id = NULL").fetchone()[0])
print("IS NULL :", con.execute("SELECT COUNT(*) FROM pesanan WHERE pelanggan_id IS NULL").fetchone()[0])'''),
    blok("hasil", "<pre><code>= NULL  : 0\nIS NULL : 12</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Tidak ada error, tidak ada peringatan.</strong> <code>= NULL</code> "
                   "adalah SQL yang sah, dan ia selalu memberi nol baris. Kalau kamu memakainya "
                   "untuk menghitung data yang hilang, laporanmu akan berkata “tidak ada yang "
                   "hilang” selamanya."),
    "<p>Kamu menulis <code>IS NULL</code>, bukan <code>= NULL</code> — karena "
    "<code>NULL</code> bukan sebuah nilai yang bisa disamakan dengan apa pun.</p>")

langkah("Satu salah ketik lagi, yang ini justru berteriak",
    blok("aksi", "Tambahkan satu kolom di dalam subquery-nya — dengan sengaja.", "LAKUKAN"),
    kode('''con.execute("""SELECT COUNT(*) FROM pelanggan
   WHERE id NOT IN (SELECT pelanggan_id, id FROM pesanan)""").fetchall()'''),
    blok("bahaya", "<pre><code>OperationalError: sub-select returns 2 columns - expected 1</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Pesannya menyebut <strong>angkanya</strong>: dapat 2 kolom, harusnya 1. Kamu tidak perlu "
    "menebak apa pun — subquery di dalam <code>IN</code> selalu harus mengembalikan tepat satu "
    "kolom.</p>",
    blok("catatan", "<strong>Bandingkan dengan tiga langkah sebelumnya.</strong> Salah ketik "
                    "yang ini berteriak dalam sepersekian detik. Yang <code>NULL</code> tadi "
                    "diam selama enam bulan. Yang berteriak bukan yang harus kamu takuti."))

langkah("Sekarang tulis kalimat yang akan kamu ucapkan di wawancara",
    blok("aksi", "Ucapkan keras-keras, sungguhan bersuara, lalu tulis di catatanmu.", "LAKUKAN"),
    blok("hasil", "<p>“Aku pakai <code>NOT EXISTS</code>, bukan <code>NOT IN</code>, karena kalau "
                  "kolom di subquery-nya ada <code>NULL</code>, <code>NOT IN</code> akan "
                  "mengembalikan nol baris <strong>tanpa error</strong>.”</p>",
         "YANG KAMU UCAPKAN"),
    "<p>Kalimat itu memberi tahu pewawancara bahwa <strong>kamu pernah tertipu olehnya dan "
    "sudah tidak akan lagi</strong> — dan itu jauh lebih meyakinkan daripada jawaban yang "
    "kebetulan benar.</p>",
    blok("catatan", "<strong>Kalau kamu gugup dan lupa kalimatnya</strong>, cukup bilang “aku "
                    "hindari <code>NOT IN</code> karena masalah <code>NULL</code>”. Itu sudah "
                    "menempatkanmu di atas mayoritas kandidat."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas, tanpa melihat.", "LAKUKAN"),
    kode("""1. Empat langkah sebelum mengetik?
2. Berapa jawaban NOT IN tadi, dan berapa yang benar?
3. Kenapa satu NULL merusak seluruh NOT IN?
4. Apa yang kamu tulis sebagai ganti "= NULL"?
5. Dari empat langkah tadi, mana yang jadi keunggulanmu?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Ulangi soal → sebut asumsi → tulis dari <code>FROM</code> → periksa hasilnya. "
    "2. <code>NOT IN</code> memberi <strong>0</strong>; yang benar <strong>3</strong>. "
    "3. Perbandingan dengan <code>NULL</code> bernilai <em>tidak diketahui</em>, jadi "
    "kondisinya tidak pernah benar untuk baris mana pun. "
    "4. <code>IS NULL</code>. "
    "5. Langkah 4 — memeriksa, karena kamu sudah melakukannya bertahun-tahun.</p></details>")

HARI1 = {
  "n": "HARI 1", "tab": "1",
  "judul": "Yang sebenarnya diuji, dan jebakan yang menjatuhkan paling banyak orang",
  "waktu": "± 55 menit",
  "tujuan": "memakai satu kerangka empat langkah untuk soal SQL apa pun, dan tidak akan pernah "
            "lagi tertipu oleh <code>NOT IN</code>.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> empat langkah yang bisa kamu ucapkan, dua "
           "kesalahan yang diam (<code>NOT IN</code> dan <code>= NULL</code>) yang kamu buktikan "
           "sendiri, dan satu kalimat wawancara yang sudah kamu latih bersuara.</p>"
           "<p style=\"margin-top:8px\">Besok kamu mulai mengetik di bawah pengatur waktu — "
           "lima soal, sepuluh menit masing-masing.</p>",
}
