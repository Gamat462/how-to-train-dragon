# -*- coding: utf-8 -*-
"""Hari 3 — jebakan NOT IN (PostgreSQL)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Tulis jawabanmu dulu, di kertas",
    blok("aksi", "Pertanyaan bisnisnya wajar: <strong>pelanggan mana yang belum pernah memesan "
                 "sama sekali?</strong> Daftar itu dipakai untuk kirim promo. Tulis query-mu di "
                 "kertas sebelum menjalankan apa pun.", "KERJAKAN, ± 3 MENIT"),
    kode("-- tulis jawabanmu di sini dulu, jangan dijalankan\nSELECT ... FROM pelanggan WHERE ...",
         salin=False),
    blok("bahaya", "<strong>Jangan lanjut sebelum kamu menulis sesuatu.</strong> Kalau kamu "
                   "membaca jawabannya dulu, kamu sedang membaca — bukan berlatih."))

langkah("Jalankan versi yang paling wajar ditulis orang",
    blok("aksi", "Berkas <code>senja/hari-3.sql</code>. Jalankan.", "LAKUKAN"),
    kode("SELECT nama FROM pelanggan\nWHERE id NOT IN (SELECT pelanggan_id FROM pesanan);"),
    keluaran(H, "h3_not_in"),
    "<p>Kosong. Query-mu jalan, layarmu bersih, hasilnya masuk akal: “semua pelanggan sudah "
    "pernah memesan, tidak ada yang perlu dikirimi promo.”</p>")

langkah("Berhenti sebentar sebelum menggulir",
    blok("aksi", "Kalau ini hasil di layarmu di hari kerja pertamamu, apa yang kamu lakukan?",
         "JAWAB DALAM HATI"),
    blok("hasil", "<p>Hampir semua orang menjawab: <em>“saya laporkan bahwa tidak ada pelanggan "
                  "pasif.”</em> Dan hasil itu <strong>salah</strong>.</p>", "JAWABAN JUJURNYA"),
    blok("catatan", "Kalau tadi kamu juga menulis <code>NOT IN</code> di kertas, "
                    "<strong>itu wajar</strong> — itu jawaban yang diberikan hampir semua orang, "
                    "termasuk yang sudah dua tahun bekerja. Bedanya sekarang kamu akan tahu."))

langkah("Tanya hal yang sama dengan cara kedua",
    blok("aksi", "Query berbeda, pertanyaan identik.", "LAKUKAN"),
    kode('''SELECT nama FROM pelanggan p
WHERE NOT EXISTS (SELECT 1 FROM pesanan o WHERE o.pelanggan_id = p.id)
ORDER BY nama;'''),
    keluaran(H, "h3_not_exists"),
    "<p>Andi, Bagus, dan Vira nyata-nyata belum pernah memesan. Query pertama tidak menemukan "
    "mereka — <strong>dan tidak memberitahu siapa pun</strong>.</p>")

langkah("Cara ketiga, supaya kamu tidak percaya padaku begitu saja",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''SELECT count(*) AS jumlah FROM pelanggan p
LEFT JOIN pesanan o ON o.pelanggan_id = p.id
WHERE o.id IS NULL;'''),
    keluaran(H, "h3_left_join"),
    "<p>Tiga lagi. Kamu memakai dua cara berbeda dan sampai ke satu angka — itu cara kamu tahu "
    "angkanya benar, bukan karena aku yang bilang.</p>")

langkah("Cara keempat: NOT IN yang disaring dulu",
    blok("aksi", "<code>NOT IN</code> yang sama, ditambah satu penyaring.", "LAKUKAN"),
    kode('''SELECT count(*) AS jumlah FROM pelanggan
WHERE id NOT IN (SELECT pelanggan_id FROM pesanan
                 WHERE pelanggan_id IS NOT NULL);'''),
    keluaran(H, "h3_not_in_saring"),
    "<p>Tiga. Jadi yang bermasalah bukan <code>NOT IN</code> itu sendiri — yang bermasalah ada "
    "di <strong>apa yang masuk ke dalam daftarnya</strong>.</p>")

langkah("Empat cara berdampingan",
    blok("aksi", "Satu query, empat jawaban.", "LAKUKAN"),
    kode('''SELECT 'NOT IN' AS cara,
       (SELECT count(*) FROM pelanggan
        WHERE id NOT IN (SELECT pelanggan_id FROM pesanan)) AS hasil
UNION ALL SELECT 'NOT EXISTS',
       (SELECT count(*) FROM pelanggan p
        WHERE NOT EXISTS (SELECT 1 FROM pesanan o WHERE o.pelanggan_id = p.id))
UNION ALL SELECT 'LEFT JOIN IS NULL',
       (SELECT count(*) FROM pelanggan p
        LEFT JOIN pesanan o ON o.pelanggan_id = p.id WHERE o.id IS NULL)
UNION ALL SELECT 'NOT IN + saring NULL',
       (SELECT count(*) FROM pelanggan
        WHERE id NOT IN (SELECT pelanggan_id FROM pesanan
                         WHERE pelanggan_id IS NOT NULL));'''),
    keluaran(H, "h3_empat_cara"),
    "<p>Tiga cara menjawab 3. Satu cara menjawab 0. Padahal kamu menanyakan hal yang sama kepada "
    "keempatnya.</p>")

langkah("Cari penyebabnya sendiri",
    blok("aksi", "Tebak angkanya dulu sebelum menjalankan.", "LAKUKAN"),
    kode("SELECT count(*) AS tanpa_pelanggan_id FROM pesanan WHERE pelanggan_id IS NULL;"),
    keluaran(H, "h3_tanpa_pid"),
    "<p>Dua belas pesanan datang dari tamu yang tidak punya akun, jadi "
    "<code>pelanggan_id</code>-nya <code>NULL</code>. Itulah seluruh sebabnya — dan kamu "
    "menemukannya sendiri, bukan dari penjelasanku.</p>")

langkah("Kenapa satu NULL merusak seluruh daftar",
    blok("aksi", "Baca penjabaran ini pelan-pelan.", "LAKUKAN"),
    kode('''id NOT IN (3, 7, NULL)

sama artinya dengan

id <> 3  AND  id <> 7  AND  id <> NULL''', salin=False),
    blok("hasil", "<p>Bagian terakhir, <code>id &lt;&gt; NULL</code>, <strong>selalu</strong> "
                  "bernilai <em>tidak diketahui</em>. Dan <em>benar</em> AND <em>tidak "
                  "diketahui</em> hasilnya <em>tidak diketahui</em>.</p>", "LOGIKA TIGA NILAI"),
    "<p>Jadi seluruh syaratnya tidak pernah bisa bernilai benar, untuk baris mana pun. "
    "<code>WHERE</code> membuang semuanya.</p>")

langkah("Buktikan di ukuran sekecil mungkin",
    blok("aksi", "Tanpa tabel, tanpa data — cuma angka.", "LAKUKAN"),
    kode('''SELECT 5 NOT IN (1,2,3)    AS "5 NOT IN (1,2,3)",
       5 NOT IN (1,2,NULL) AS "5 NOT IN (1,2,NULL)";'''),
    keluaran(H, "h3_kecil"),
    "<p>Lima jelas bukan 1 dan bukan 2. Tapi begitu kamu menyelipkan satu <code>NULL</code> ke "
    "daftarnya, jawabannya berubah dari <strong>true</strong> jadi <strong>tidak "
    "diketahui</strong>.</p>")

langkah("Bentuk positifnya tidak rusak",
    blok("aksi", "Sekarang tanpa <code>NOT</code>.", "LAKUKAN"),
    kode('''SELECT 5 IN (1,2,NULL) AS "5 IN (1,2,NULL)",
       1 IN (1,2,NULL) AS "1 IN (1,2,NULL)";'''),
    keluaran(H, "h3_positif"),
    "<p><code>1 IN (1,2,NULL)</code> tetap <strong>true</strong>: cukup satu bagian bernilai "
    "benar, karena <code>OR</code> tidak menuntut semuanya. Yang rusak hanya bentuk negatifnya, "
    "karena <code>AND</code> menuntut <em>semua</em> bagian bernilai benar.</p>")

langkah("Satu layar merah supaya kamu kenal bentuknya",
    blok("aksi", "Kesalahan ini sering terjadi saat kamu buru-buru menyalin subquery.",
         "LAKUKAN"),
    kode("SELECT nama FROM pelanggan\nWHERE id NOT IN (SELECT pelanggan_id, id FROM pesanan);"),
    keluaran(H, "h3_merah_dua_kolom"),
    blok("catatan", "<strong>Layar merah ini justru menolongmu.</strong> Bandingkan dengan "
                    "langkah 2: di sana SQL diam saja dan memberimu jawaban salah. Di sini ia "
                    "berteriak dan kamu memperbaikinya dalam sepuluh detik. Yang berbahaya "
                    "selalu yang diam."))

langkah("Aturan yang kamu pakai seterusnya",
    blok("aksi", "Salin tabel ini ke catatanmu.", "LAKUKAN"),
    tabel(["Bentuk", "Aman?", "Pakai kalau"],
          [["<code>NOT EXISTS (...)</code>", "Selalu aman",
            "Bawaan. Tidak peduli ada <code>NULL</code> atau tidak."],
           ["<code>LEFT JOIN ... WHERE x IS NULL</code>", "Aman",
            "Kalau kamu juga butuh kolom dari tabel kanan"],
           ["<code>NOT IN (SELECT ... WHERE kol IS NOT NULL)</code>", "Aman, tapi rapuh",
            "Hindari — orang berikutnya akan menghapus penyaringnya"],
           ["<code>NOT IN (SELECT ...)</code>", "Berbahaya",
            "Jangan, kecuali kolomnya dijamin <code>NOT NULL</code> di skema"]]),
    "<p>Jadikan <code>NOT EXISTS</code> refleks. Ia sedikit lebih panjang ditulis, tidak pernah "
    "salah, dan di PostgreSQL perencananya menghasilkan rencana yang sama baiknya.</p>")

langkah("Kenapa ini ditanyakan di hampir setiap wawancara",
    blok("aksi", "Baca sekali, lalu ucapkan jawabannya dengan suara keras.", "LAKUKAN"),
    blok("hasil", "<p>Yang berbahaya bukan salahnya. Yang berbahaya adalah "
                  "<strong>hasil kosong hampir tidak pernah dicurigai</strong> — “tidak ada "
                  "pelanggan yang belum memesan” terdengar seperti kabar baik, bukan seperti "
                  "bug.</p>", "KALIMAT YANG DINILAI"),
    "<p>Dan kolom yang hari ini tidak punya <code>NULL</code> bisa mulai punya "
    "<code>NULL</code> bulan depan tanpa ada yang memberitahumu. Query yang dulu benar jadi "
    "salah dengan sendirinya.</p>",
    blok("catatan", "Kalau kamu bisa menjelaskan <em>kenapa</em> hasilnya nol — bukan sekadar "
                    "“pakai NOT EXISTS saja” — kamu terdengar seperti orang yang pernah kena, "
                    "bukan yang pernah membaca."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis query yang menjawab: <strong>produk mana yang belum pernah dipesan sama "
                 "sekali?</strong> Pakai <code>NOT EXISTS</code>. Lalu coba versi "
                 "<code>NOT IN</code>-nya dan jelaskan kenapa kali ini hasilnya sama.",
         "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>SELECT nama FROM produk pr\n"
    "WHERE NOT EXISTS (SELECT 1 FROM item i WHERE i.produk_id = pr.id);</code></pre></div>"
    + keluaran(H, "h3_kunci", tag="HASILNYA") +
    "<p>Kosong — dan <strong>kali ini kosongnya benar</strong>: ketujuh produk memang pernah "
    "terjual. Versi <code>NOT IN</code>-nya memberi jawaban yang sama karena "
    "<code>item.produk_id</code> tidak pernah <code>NULL</code>. Buktikan sendiri:</p>"
    "<div class=\"kode\"><pre><code>SELECT count(*) AS item_tanpa_produk FROM item\n"
    "WHERE produk_id IS NULL;</code></pre></div>"
    + keluaran(H, "h3_kunci_cek", tag="HASILNYA") +
    "<p>Di sinilah letak jebakannya: <code>NOT IN</code> berfungsi normal sampai suatu hari ada "
    "<code>NULL</code> yang masuk. Query yang kelihatan benar hari ini bisa berubah jadi salah "
    "tanpa kamu menyentuhnya.</p></details>")

HARI3 = {
  "n": "HARI 3", "tab": "3",
  "judul": "Jebakan NOT IN — jawaban nol padahal jawabannya tiga",
  "waktu": "± 55 menit",
  "tujuan": "menulis pertanyaan “siapa yang tidak pernah…” dengan cara yang tidak bisa salah, dan "
            "menjelaskan kenapa cara yang paling wajar justru berbahaya.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>NOT IN</code> yang daftarnya mengandung "
           "<code>NULL</code> selalu mengembalikan nol baris — bukan “sebagian salah”, kosong "
           "seluruhnya, setiap kali · <code>IN</code> biasa tidak bermasalah · "
           "<code>NOT EXISTS</code> jadi bawaanmu selamanya.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 3 dari 8.</strong> Jawab dengan "
           "suara: <em>sebuah query <code>NOT IN (SELECT ...)</code> mengembalikan nol baris. "
           "Apa yang pertama kali kamu curigai?</em></p>"
           "<details><summary>Kunci</summary><p>Ada <code>NULL</code> di dalam daftar "
           "subquery-nya. Satu saja sudah membuat seluruh hasilnya kosong. Ganti ke "
           "<code>NOT EXISTS</code>, lalu hitung ulang.</p></details>",
}
