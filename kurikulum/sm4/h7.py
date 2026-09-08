# -*- coding: utf-8 -*-
"""Hari 7 — view, snapshot, dan berkas uji mutu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bikin sebuah VIEW",
    blok("aksi", "Sesi Python baru, salinan <code>vw.db</code>.", "LAKUKAN"),
    kode("""import sqlite3, time, shutil
shutil.copy("besar.db", "vw.db")
c = sqlite3.connect("vw.db")
c.execute(\"\"\"CREATE VIEW ringkas AS
SELECT cabang, substr(tanggal,1,7) AS bulan,
       COUNT(*) AS transaksi, SUM(nilai) AS omzet
FROM transaksi GROUP BY cabang, substr(tanggal,1,7)\"\"\")"""),
    blok("hasil", "<p>Tidak ada yang tercetak.</p>", "HARUS MUNCUL"),
    "<p>Sebuah <code>VIEW</code> adalah <strong>query yang diberi nama</strong>. "
    "Ia tidak menyimpan data apa pun — tiap kali kamu menyebutnya, query di baliknya "
    "dijalankan lagi dari awal.</p>")

langkah("Ukur berapa lama membacanya",
    blok("aksi", "Bikin fungsi ukur lagi (sesi ini baru), lalu panggil.", "LAKUKAN"),
    kode("""def ukur(sql, n=5):
    w = []
    for _ in range(n):
        t = time.perf_counter(); r = c.execute(sql).fetchall(); w.append(time.perf_counter()-t)
    return min(w)*1000, r

mv, rv = ukur("SELECT * FROM ringkas WHERE cabang='Kemang' ORDER BY bulan")
print(f"VIEW  : {mv:8.1f} ms   {len(rv)} baris")"""),
    blok("hasil", "<pre><code>VIEW  :    319.8 ms   24 baris</code></pre>", "HARUS MUNCUL"),
    "<p>24 baris hasil, 320 milidetik. View yang baru kamu bikin harus meringkas ulang 800.000 "
    "baris <strong>tiap kali kamu memanggilnya</strong>.</p>")

langkah("Bikin tabel ringkasan dari view yang sama",
    blok("aksi", "Satu perintah, dan catat berapa lama sekali-buatnya.", "LAKUKAN"),
    kode("""t = time.perf_counter()
c.execute("CREATE TABLE ringkas_snapshot AS SELECT * FROM ringkas"); c.commit()
print(f"sekali buat: {time.perf_counter()-t:.2f} detik")"""),
    blok("hasil", "<pre><code>sekali buat: 1.72 detik</code></pre>", "HARUS MUNCUL"),
    "<p>Sekarang hasil ringkasannya tersimpan sebagai tabel biasa — 24 baris, sudah jadi.</p>")

langkah("Ukur tabel itu, dan pastikan isinya sama",
    blok("aksi", "Query yang sama persis, cuma nama tabelnya beda.", "LAKUKAN"),
    kode("""mt, rt = ukur("SELECT * FROM ringkas_snapshot WHERE cabang='Kemang' ORDER BY bulan", n=9)
print(f"TABEL : {mt:8.3f} ms   {len(rt)} baris")
print("isi sama?", rv == rt)"""),
    blok("hasil", "<pre><code>TABEL :    0.033 ms   24 baris\nisi sama? True</code></pre>",
         "HARUS MUNCUL"),
    "<p>319,8 ms lawan 0,033 ms — sekitar <strong>sepuluh ribu kali</strong>, dan "
    "<code>isi sama? True</code> membuktikan kamu tidak kehilangan apa pun. Masuk akal: yang satu "
    "meringkas 800.000 baris tiap kali, yang satu membaca 24 baris yang sudah jadi.</p>")

langkah("Sekarang harganya",
    blok("aksi", "Masukkan satu transaksi baru senilai Rp 22.000, lalu tanya kedua-duanya.", "LAKUKAN"),
    kode("""c.execute("INSERT INTO transaksi VALUES (9000001,'2024-06-01','Kemang',7,'Kopi Susu',1,22000)")
c.commit()
v = c.execute("SELECT omzet FROM ringkas          WHERE cabang='Kemang' AND bulan='2024-06'").fetchone()[0]
s = c.execute("SELECT omzet FROM ringkas_snapshot WHERE cabang='Kemang' AND bulan='2024-06'").fetchone()[0]
print(f"view    : {v}\\nsnapshot: {s}\\nselisih : {v-s}")"""),
    blok("hasil", "<pre><code>view    : 338587000\nsnapshot: 338565000\nselisih : 22000</code></pre>",
         "HARUS MUNCUL"),
    "<p>View langsung tahu. Snapshot tidak, <strong>dan tidak akan pernah tahu</strong> sampai "
    "ada yang membangunnya ulang.</p>")

langkah("Seluruh pertukarannya, dalam satu tabel",
    blok("aksi", "Baca sekali. Kamu barusan mengukur ketiga baris pertamanya sendiri.", "LAKUKAN"),
    tabel(["", "VIEW", "Tabel snapshot"],
          [["Kecepatan baca", "selambat query aslinya (319,8 ms)", "secepat tabel kecil (0,033 ms)"],
           ["Kesegaran", "selalu terbaru", "sesegar terakhir kali dibangun"],
           ["Ruang berkas", "nol", "sebesar hasilnya"],
           ["Pakai untuk", "menyembunyikan query rumit; data yang harus akurat detik ini",
            "dasbor, laporan bulanan, apa pun yang dibaca berkali-kali dari data yang sudah "
            "tidak berubah"]]),
    "<p><strong>Kecepatan ditukar dengan kesegaran.</strong> Tidak ada pilihan yang benar untuk "
    "semua kasus — yang ada cuma pilihan yang kamu ambil dengan sadar.</p>")

langkah("Satu istilah, dan satu aturan yang menyelamatkan reputasi",
    blok("aksi", "Baca dua paragraf ini, lalu lanjut ke bagian uji mutu.", "LAKUKAN"),
    "<p>Tabel snapshot yang dibangun ulang otomatis oleh basis datanya sendiri punya nama: "
    "<strong>materialized view</strong>. PostgreSQL punya, BigQuery punya, <strong>SQLite "
    "tidak</strong>. Di SQLite kamu membangunnya sendiri: <code>DROP TABLE</code> lalu "
    "<code>CREATE TABLE … AS SELECT * FROM view</code>, dijalankan terjadwal — persis pola "
    "skrip harian di Minggu 11. Alatnya sudah kamu punya; yang baru cuma namanya.</p>",
    blok("bahaya", "<strong>Tabel snapshot apa pun harus membawa kapan ia dibangun.</strong> "
                   "Tambahkan kolom <code>dibangun_pada</code>, dan cetak tanggal itu di kaki "
                   "tiap laporan. Klien yang melihat “data per 3 September 08:00” tahu persis "
                   "apa yang ia baca. Klien yang melihat angka tanpa keterangan waktu akan "
                   "menganggapnya angka hari ini — dan ketika ternyata bukan, yang disalahkan "
                   "adalah kamu."))

langkah("Jalankan berkas uji mutu",
    blok("aksi", "Ambil <code>uji_mutu.py</code> dari paket zip "
                 "(<code>data-dan-skrip/sql-mahir/</code>), taruh di sebelah "
                 "<code>senja.db</code>, lalu jalankan.", "LAKUKAN"),
    kode("python uji_mutu.py"),
    blok("hasil", "<pre><code>utang  Pesanan tanpa pelanggan: 12 baris (sesuai batas 12)\n"
                  "utang  Produk tanpa harga beli: 2 baris (sesuai batas 2)\n"
                  "utang  Pelanggan tanpa kota: 6 baris (sesuai batas 6)\n"
                  "bersih Item menunjuk pesanan hantu\n"
                  "bersih Jumlah atau harga tidak masuk akal\n"
                  "GAGAL  Pesanan selesai yang hilang dari kasir: 3 baris (batas 0)\n"
                  "          (7,)\n          (88,)\n          (251,)\n"
                  "GAGAL  Struk kasir tanpa pesanan: 2 baris (batas 0)\n"
                  "          (9001,)\n          (9002,)\n"
                  "GAGAL  Nilai pesanan beda antara sistem dan kasir: 2 baris (batas 0)\n"
                  "          (12, 50000)\n          (199, -25000)\n\n"
                  "5 lolos, 3 gagal</code></pre>", "HARUS MUNCUL"),
    "<p>Isinya <strong>sekumpulan query yang seharusnya tidak mengembalikan baris apa pun</strong>. "
    "Kalau salah satu mengembalikan baris, ada yang rusak.</p>")

langkah("Jalankan dari folder yang salah, dengan sengaja",
    blok("aksi", "Buat satu folder kosong, masuk ke dalamnya, lalu panggil skripnya "
                 "dari sana.", "LAKUKAN"),
    kode("mkdir coba\ncd coba\npython ../uji_mutu.py"),
    blok("bahaya", "<pre><code>sqlite3.OperationalError: no such table: pesanan</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Perhatikan pesannya: bukan “berkas tidak ditemukan”. SQLite justru <strong>membuat "
    "<code>senja.db</code> baru yang kosong</strong> di folder itu, lalu bingung karena "
    "tabelnya tidak ada.</p>",
    blok("bahaya", "<strong>Ini jebakan yang mahal.</strong> Skrip yang dijalankan dari folder "
                   "salah tidak pernah berteriak “salah folder” — ia diam-diam bekerja di basis "
                   "data kosong. Kalau yang kamu jalankan skrip <em>penulis</em>, bukan pemeriksa, "
                   "hasilnya masuk ke berkas yang salah dan tidak ada yang tahu."),
    blok("catatan", "<strong>Kalau punyamu justru berhasil</strong>, kamu masih di folder yang "
                    "benar. Bereskan: <code>cd ..</code> lalu hapus folder <code>coba</code> "
                    "beserta <code>senja.db</code> kosong di dalamnya."))

langkah("Periksa kode keluarnya",
    blok("aksi", "Langsung setelah perintah tadi, di terminal yang sama.", "LAKUKAN"),
    kode("""echo $?          # Linux / Mac
echo %ERRORLEVEL%   # Windows"""),
    blok("hasil", "<pre><code>1</code></pre>", "HARUS MUNCUL"),
    "<p>Angka 1 berarti gagal. Ini yang membuat skrip terjadwal di Minggu 11 ikut berhenti dan "
    "memberitahumu — <strong>bukan cuma mencetak sesuatu yang tidak ada yang membaca</strong>.</p>")

langkah("Baca tiga kelompok keluarannya",
    blok("aksi", "Lihat lagi keluaran langkah 8. Ada tiga kata di kolom kiri.", "LAKUKAN"),
    tabel(["Kata", "Artinya", "Yang kamu lakukan"],
          [["<code>bersih</code>", "tidak ada masalah — dan kamu sekarang <em>tahu</em>, "
            "bukan berasumsi", "tidak ada"],
           ["<code>utang</code>", "masalah yang sudah kamu ketahui dan sepakati dengan klien",
            "tidak ada, selama angkanya tidak naik"],
           ["<code>GAGAL</code>", "sesuatu yang belum kamu ketahui", "tanyakan ke klien hari ini juga"]]),
    "<p>Tiga <code>GAGAL</code> di atas adalah tiga kalimat yang bisa kamu kirim apa adanya: "
    "tiga pesanan selesai yang tidak ada struknya, dua struk yang tidak ada pesanannya, dan dua "
    "pesanan yang nilainya beda Rp 50.000 dan Rp 25.000 antara dua sistem.</p>")

langkah("Kenapa ada kolom “batas”",
    blok("aksi", "Buka <code>uji_mutu.py</code> dan cari kata <code>batas</code>.", "LAKUKAN"),
    kode("""dict(nama="Pesanan tanpa pelanggan", batas=12,
     sql="SELECT id FROM pesanan WHERE pelanggan_id IS NULL")""", salin=False),
    "<p>Batas = <strong>berapa banyak baris bermasalah yang masih boleh ada</strong>. "
    "<code>0</code> berarti harus bersih. Di atas nol berarti utang yang sudah disepakati — "
    "angkanya dipatok, dan <strong>kalau besok jadi 13, statusnya berubah jadi GAGAL</strong>.</p>",
    blok("catatan", "<strong>Kolom ini yang membedakan pemeriksaan yang dipakai orang dari yang "
                    "diabaikan orang.</strong> Pemeriksaan yang menyala merah tiap hari karena "
                    "masalah lama akan berhenti dibaca dalam seminggu. Dengan batas, merah selalu "
                    "berarti <em>sesuatu berubah hari ini</em>."))

langkah("Kesalahan yang hampir kubuat — jalankan versi pertamaku",
    blok("aksi", "Versi pertama pemeriksaan rekonsiliasi kutulis lebih sederhana, tanpa syarat "
                 "<code>status = 'selesai'</code>. Jalankan di <code>senja.db</code> "
                 "<strong>sebelum</strong> membaca langkah berikutnya.", "LAKUKAN"),
    kode("""s = sqlite3.connect("senja.db")
r = s.execute(\"\"\"SELECT 'hanya di pesanan' AS sisi, id FROM pesanan
WHERE id NOT IN (SELECT id FROM pesanan_kasir)
UNION ALL
SELECT 'hanya di kasir', id FROM pesanan_kasir
WHERE id NOT IN (SELECT id FROM pesanan)\"\"\").fetchall()
print(len(r), "baris bermasalah")"""),
    blok("hasil", "<pre><code>43 baris bermasalah</code></pre>", "HARUS MUNCUL"),
    "<p>43. Terlihat lebih menyeluruh daripada versi yang cuma menemukan 5. "
    "<strong>Menurutmu berapa yang benar-benar masalah?</strong></p>")

langkah("Pecah menurut statusnya",
    blok("aksi", "Satu query yang mengubah seluruh kesimpulan.", "LAKUKAN"),
    kode("""print(s.execute(\"\"\"SELECT status, COUNT(*) FROM pesanan
WHERE id NOT IN (SELECT id FROM pesanan_kasir) GROUP BY status\"\"\").fetchall())"""),
    blok("hasil", "<pre><code>[('batal', 38), ('selesai', 3)]</code></pre>", "HARUS MUNCUL"),
    "<p><strong>38 kebisingan, 3 masalah sungguhan.</strong> Pesanan batal memang "
    "<em>seharusnya</em> tidak punya struk kasir. Itu bukan kerusakan; itu cara kerja bisnisnya.</p>",
    blok("bahaya", "Pemeriksaan yang membangunkanmu <strong>43 kali untuk 3 hal yang benar</strong> "
                   "akan kamu matikan dalam dua minggu — dan hari kamu mematikannya adalah hari "
                   "ketiga masalah itu jadi tak terlihat selamanya."))

langkah("Dari mana syarat itu datang",
    blok("aksi", "Baca satu kalimat ini. Ini bagian yang paling penting di seluruh Level 4.", "LAKUKAN"),
    blok("hasil", "<p>Syarat <code>status = 'selesai'</code> tidak datang dari SQL, dan tidak "
                  "datang dari datanya. Ia datang dari <strong>memahami bahwa pesanan batal tidak "
                  "menghasilkan struk</strong>.</p>", "YANG HARUS KAMU BAWA"),
    "<p><strong>Pemeriksaan mutu yang bagus selalu berisi satu potong pengetahuan bisnis</strong> — "
    "dan itulah bagian yang tidak bisa disalin dari internet, dan bagian yang kamu sudah punya "
    "dari enam tahun terakhirmu.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Lima pertanyaan, di kertas.", "LAKUKAN"),
    kode("""1. VIEW menyimpan datanya atau tidak?
2. Satu kolom yang wajib ada di tiap tabel snapshot?
3. Berkas uji mutu isinya query yang seharusnya mengembalikan apa?
4. Fungsi kolom "batas"?
5. Kenapa 43 baris temuan lebih buruk daripada 3?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Tidak — ia query yang diberi nama, dijalankan ulang tiap kali disebut. "
    "2. <code>dibangun_pada</code>, dan tanggalnya dicetak di kaki laporan. "
    "3. <strong>Nol baris.</strong> Ada baris berarti ada yang rusak. "
    "4. Memisahkan utang yang sudah disepakati dari kejadian baru, supaya merah selalu berarti "
    "sesuatu berubah hari ini. "
    "5. Karena 38 di antaranya bukan masalah, dan pemeriksaan yang berisik akan dimatikan orang.</p></details>")

HARI7 = {
  "n": "HARI 7",
  "tab": "7",
  "judul": "View, snapshot, dan menguji SQL sebelum klien yang mengujinya",
  "waktu": "± 70 menit",
  "tujuan": "memilih antara <code>VIEW</code> dan tabel ringkasan dengan alasan yang bisa kamu "
            "ucapkan, dan punya satu berkas uji mutu yang berteriak <strong>sebelum</strong> "
            "angkanya sampai ke klien.",
  "langkah": L,
  "tutup_judul": "SQL Mahir Level 4 selesai",
  "tutup": "<p>Sekarang kamu bisa menjawab tiga pertanyaan yang membedakan analis dari orang yang "
           "bisa menulis <code>SELECT</code>: <strong>kenapa query ini lambat</strong> (baca "
           "rencananya, jangan menebak), <strong>apa yang terjadi kalau gagal di tengah</strong> "
           "(bungkus dengan transaksi), dan <strong>bagaimana aku tahu angkanya benar</strong> "
           "(jalankan berkas uji mutu sebelum mengirim, bukan sesudah ditanya).</p>"
           "<p style=\"margin-top:8px\">Dan satu kebiasaan yang lebih penting daripada seluruh isi "
           "halaman ini: <strong>tiap angka di sini kamu ukur sendiri.</strong> Tidak ada satu pun "
           "yang kamu terima karena ada yang bilang begitu. Itu cara kerja yang akan membuatmu "
           "dipercaya, jauh setelah angka-angka spesifiknya kamu lupakan.</p>"
           "<p style=\"margin-top:8px\"><strong>Berikutnya di Level 5</strong>, yang terakhir: "
           "ujian dan wawancara — soal SQL <em>live coding</em> yang benar-benar diberikan, cara "
           "menjelaskan jawabanmu sambil menulisnya, membaca soal yang sengaja ambigu, dan satu "
           "latihan penutup yang menggabungkan kelima level.</p>",
}
