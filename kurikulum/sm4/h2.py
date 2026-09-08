# -*- coding: utf-8 -*-
"""Hari 2 — dua cara paling umum membunuh index yang sudah ada."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Siapkan index tanggal",
    blok("aksi", "Lanjutkan di sesi Python yang sama dengan Hari 1 — <code>ukur</code> dan "
                 "<code>rencana</code> masih hidup. Kalau sudah kamu tutup, jalankan ulang "
                 "langkah 2, 4, dan 5 Hari 1 dulu.", "LAKUKAN"),
    kode("""t = time.perf_counter()
con.execute("CREATE INDEX idx_tgl ON transaksi(tanggal)")
con.commit()
print(f"membuat index: {time.perf_counter()-t:.2f} detik")"""),
    blok("hasil", "<pre><code>membuat index: 0.42 detik</code></pre>", "HARUS MUNCUL"),
    "<p>Sekarang kolom <code>tanggal</code> punya index. Hari ini kamu akan membuatnya "
    "tidak berguna — dengan sengaja.</p>")

langkah("Tanyakan “berapa transaksi Januari 2024?” dengan cara yang biasa",
    blok("aksi", "Cara ini yang paling sering ditulis orang. Jalankan.", "LAKUKAN"),
    kode("""A = "SELECT COUNT(*) FROM transaksi WHERE substr(tanggal,1,7) = '2024-01'"
ms, h = ukur(A)
print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(A)"""),
    blok("hasil", "<pre><code>52.6 ms   hasil = 33993\n"
                  "    SCAN transaksi USING COVERING INDEX idx_tgl</code></pre>", "HARUS MUNCUL"),
    "<p>Index-nya <em>disebut</em> di rencana, tapi kata di depannya <strong>SCAN</strong>. "
    "Index-nya ada; index-nya tidak menolong.</p>")

langkah("Tanyakan hal yang sama, bentuk lain",
    blok("aksi", "Jangan ubah pertanyaannya. Ubah cara menuliskannya.", "LAKUKAN"),
    kode("""B = "SELECT COUNT(*) FROM transaksi WHERE tanggal >= '2024-01-01' AND tanggal < '2024-02-01'"
ms, h = ukur(B)
print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(B)"""),
    blok("hasil", "<pre><code>1.1 ms   hasil = 33993\n"
                  "    SEARCH transaksi USING COVERING INDEX idx_tgl (tanggal&gt;? AND tanggal&lt;?)</code></pre>",
         "HARUS MUNCUL"),
    "<p><strong>33993 dan 33993.</strong> Jawaban dua query itu identik. Yang satu 52,6 ms, "
    "yang satu 1,1 ms — <strong>sekitar 47 kali</strong>, hanya karena cara menulisnya.</p>")

langkah("Kenapa bentuk pertama membunuh index-nya",
    blok("aksi", "Tidak ada yang dijalankan di langkah ini. Baca dua kalimat, lalu lanjut.", "LAKUKAN"),
    "<p>Index <code>idx_tgl</code> menyimpan nilai <code>tanggal</code> dalam keadaan "
    "<strong>terurut</strong>. SQLite bisa melompat ke <code>2024-01-01</code> lalu berhenti "
    "begitu lewat <code>2024-02-01</code>.</p>"
    "<p>Begitu kamu tulis <code>substr(tanggal,1,7)</code>, yang dicari bukan lagi nilai yang "
    "tersimpan — melainkan <em>hasil olahan</em> dari nilai itu, dan tidak ada daftar terurut "
    "untuk hasil olahan. Satu-satunya cara tahu: hitung <code>substr()</code> untuk "
    "<strong>ke-800.000 baris</strong>.</p>",
    blok("catatan", "<strong>Berlaku di semua basis data, bukan cuma SQLite.</strong> "
                    "<code>UPPER()</code>, <code>DATE()</code>, <code>strftime()</code>, "
                    "<code>CAST()</code>, bahkan <code>kolom * 1</code> — semua membunuh index "
                    "kolom itu. Obatnya selalu sama: <strong>pindahkan olahannya ke sisi kanan</strong>."))

langkah("Satu kebiasaan tanda baca yang menyelamatkanmu nanti",
    blok("aksi", "Perhatikan batas atas di query <code>B</code> tadi. Ia ditulis "
                 "<code>&lt; '2024-02-01'</code>, bukan <code>&lt;= '2024-01-31'</code>.", "LAKUKAN"),
    kode("""-- AMAN     : selalu benar, jam ada atau tidak
WHERE tanggal >= '2024-01-01' AND tanggal < '2024-02-01'
-- BERBAHAYA: diam-diam membuang tanggal 31 kalau kolomnya menyimpan jam
WHERE tanggal >= '2024-01-01' AND tanggal <= '2024-01-31'""", salin=False),
    "<p>Untuk teks tanggal polos keduanya sama. Tapi begitu kolomnya menyimpan jam juga "
    "(<code>2024-01-31 14:05</code>), yang kedua membuang seluruh transaksi tanggal 31 "
    "setelah tengah malam.</p>",
    blok("bahaya", "Ini jenis kesalahan yang <strong>tidak pernah memunculkan error</strong>. "
                   "Angkanya cuma sedikit kurang, dan laporannya tetap terlihat wajar. "
                   "Pakai <em>lebih-kecil-dari hari pertama bulan berikutnya</em> sebagai "
                   "kebiasaan, dan ini tidak akan terjadi padamu."))

langkah("Bentuk kedua: mulai dari yang berhasil",
    blok("aksi", "Bikin index untuk <code>cabang</code>, lalu ukur cara yang paling lugas.", "LAKUKAN"),
    kode("""con.execute("CREATE INDEX idx_cab ON transaksi(cabang)"); con.commit()
s = "SELECT COUNT(*) FROM transaksi WHERE cabang = 'Kemang'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>5.3 ms   hasil = 160457\n"
                  "    SEARCH transaksi USING COVERING INDEX idx_cab (cabang=?)</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>SEARCH</code>. Ingat angka <strong>160457</strong> — tiga langkah berikutnya "
    "harus mengeluarkan angka yang sama.</p>")

langkah("Sekarang tanya hal yang sama pakai LIKE",
    blok("aksi", "Awalan katanya jelas: <code>'Kem%'</code>. Menurutmu index-nya terpakai?", "LAKUKAN"),
    kode("""s = "SELECT COUNT(*) FROM transaksi WHERE cabang LIKE 'Kem%'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>37.5 ms   hasil = 160457\n"
                  "    SCAN transaksi USING COVERING INDEX idx_cab</code></pre>", "HARUS MUNCUL"),
    "<p>Jawabannya sama, waktunya <strong>tujuh kali lebih lama</strong>, dan rencananya "
    "<code>SCAN</code>. Secara teori awalannya jelas dan index-nya bisa dipakai. "
    "Hasil pengukurannya bilang tidak.</p>")

langkah("Kenapa 'Kem%' pun ditolak",
    blok("aksi", "Baca ini sekali, lalu lanjut ke langkah berikutnya.", "LAKUKAN"),
    "<p>Secara bawaan <code>LIKE</code> di SQLite <strong>tidak peduli huruf besar-kecil</strong> "
    "untuk huruf ASCII — <code>'kem%'</code> juga cocok dengan <code>Kemang</code>. Sementara "
    "index <code>idx_cab</code> dibangun dengan urutan yang <strong>peduli</strong> huruf "
    "besar-kecil. Dua aturan itu tidak cocok, jadi SQLite memilih aman: baca semua.</p>",
    "<details><summary>Kalau kamu ingin index-nya tetap dipakai</summary>"
    "<p>Ada dua caranya, dan dua-duanya harus diputuskan sebelum tabelnya diisi: "
    "kolomnya dibuat dengan <code>COLLATE NOCASE</code>, atau kamu menyalakan "
    "<code>PRAGMA case_sensitive_like = ON</code>. Barulah <code>LIKE 'Kem%'</code> "
    "bisa jadi <code>SEARCH</code>. Untuk pekerjaan sehari-hari, menulis ulangnya jadi "
    "rentang (langkah 10) lebih aman daripada mengubah setelan basis data.</p></details>",
    blok("catatan", "<strong>Yang dibawa pulang bukan PRAGMA-nya.</strong> Yang dibawa pulang: "
                    "<em>jangan pernah menebak apakah index-mu terpakai.</em> Baris "
                    "<code>rencana(sql)</code> itu murah dan tidak pernah bohong. Menulis "
                    "asumsi “ini pasti pakai index” di laporan tanpa mengeceknya adalah "
                    "menaruh nama baikmu di atas tebakan."))

langkah("Yang memang mustahil dipercepat",
    blok("aksi", "Sekarang tanpa awalan yang diketahui.", "LAKUKAN"),
    kode("""s = "SELECT COUNT(*) FROM transaksi WHERE cabang LIKE '%mang'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>42.0 ms   hasil = 160457\n"
                  "    SCAN transaksi USING COVERING INDEX idx_cab</code></pre>", "HARUS MUNCUL"),
    "<p>Yang ini <strong>tidak ada obatnya</strong>, dan bukan salah SQLite. Kalau awal katanya "
    "tidak diketahui, tidak ada daftar terurut yang bisa menolong — sama seperti mencari "
    "semua nama yang <em>berakhiran</em> “anto” di buku telepon.</p>")

langkah("Penyelamatnya: tulis “diawali Kem” sebagai rentang",
    blok("aksi", "Trik yang sama seperti tanggal di langkah 3.", "LAKUKAN"),
    kode("""s = "SELECT COUNT(*) FROM transaksi WHERE cabang >= 'Kem' AND cabang < 'Ken'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>5.3 ms   hasil = 160457\n"
                  "    SEARCH transaksi USING COVERING INDEX idx_cab (cabang&gt;? AND cabang&lt;?)</code></pre>",
         "HARUS MUNCUL"),
    tabel(["Cara menanyakan", "Waktu di mesinku", "Rencananya"],
          [["<code>cabang = 'Kemang'</code>", "5,3 ms", "SEARCH"],
           ["<code>LIKE 'Kem%'</code>", "37,5 ms", "SCAN"],
           ["<code>LIKE '%mang'</code>", "42,0 ms", "SCAN"],
           ["<code>&gt;= 'Kem' AND &lt; 'Ken'</code>", "5,3 ms", "SEARCH"]]),
    "<p>Empat cara menanyakan hal yang sama, empat kali jawaban <strong>160457</strong>, "
    "dan delapan kali selisih waktu.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Tulis di kertas, tanpa melihat.", "LAKUKAN"),
    kode("""1. Dua bentuk WHERE yang membuat index berhenti berguna?
2. Bentuk pengganti untuk "bulan Januari 2024"?
3. Bentuk pengganti untuk "cabang diawali Kem"?
4. Satu baris yang membuktikan tebakanmu benar atau salah?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Fungsi yang menempel di kolom (<code>substr(tanggal,…)</code>), dan "
    "<code>LIKE</code>. "
    "2. <code>tanggal &gt;= '2024-01-01' AND tanggal &lt; '2024-02-01'</code>. "
    "3. <code>cabang &gt;= 'Kem' AND cabang &lt; 'Ken'</code>. "
    "4. <code>rencana(sql)</code> — dan lihat kata pertamanya.</p></details>",
    blok("catatan", "Jawaban 2 dan 3 bentuknya sama: <strong>rentang</strong>. "
                    "Satu prinsip, dua penampilan."))

HARI2 = {
  "n": "HARI 2",
  "tab": "2",
  "judul": "Cara paling umum membunuh index yang sudah kamu punya",
  "waktu": "± 55 menit",
  "tujuan": "mengenali kapan sebuah <code>WHERE</code> membuat index-nya tidak terpakai, dan "
            "menulis ulang query itu jadi bentuk yang <strong>hasilnya identik tapi puluhan kali "
            "lebih cepat</strong>.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu aturan yang berlaku di semua basis data — "
           "<em>jangan bungkus kolom yang di-index dengan apa pun</em> — dan satu bentuk "
           "pengganti yang selalu bisa dipakai: <strong>rentang</strong>.</p>"
           "<p style=\"margin-top:8px\">Dan satu kebiasaan: kamu sudah dua hari tidak pernah "
           "menyimpulkan apa pun tanpa menjalankan <code>rencana()</code> dulu.</p>"
           "<p style=\"margin-top:8px\">Besok: index atas dua kolom, dan kenapa urutan kolomnya "
           "bukan selera.</p>",
}
