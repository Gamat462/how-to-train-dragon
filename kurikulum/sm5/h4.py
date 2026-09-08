# -*- coding: utf-8 -*-
"""Hari 4 — window function: top-N per kelompok dan LAG."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Naik tingkat — dan bacalah ini dulu",
    blok("aksi", "Pengatur waktu 15 menit per soal mulai hari ini.", "LAKUKAN"),
    blok("catatan", "<strong>Tidak apa-apa kalau kamu belum bisa.</strong> Ini tingkat yang "
                    "dipakai untuk posisi data analyst berpengalaman. Tapi cobalah sampai mentok "
                    "sebelum membuka kunci — mentok yang kamu alami sendiri jauh lebih lengket "
                    "di ingatan daripada jawaban yang kamu baca."),
    "<p>Dua soal hari ini, dan satu error yang akan kamu picu sendiri.</p>")

langkah("Soal 6 — kerjakan dulu",
    blok("aksi", "Lima belas menit.", "LAKUKAN"),
    kode("""SOAL 6  Dua produk dengan omzet terbesar DI TIAP CABANG.
        (Hasilnya harus 6 baris: 2 produk x 3 cabang.)""", salin=False),
    blok("catatan", "Kalau kamu terjebak, petunjuknya: kamu butuh <strong>dua tingkat</strong>, "
                    "seperti soal 3."))

langkah("Coba jalan pintas yang terlihat masuk akal",
    blok("aksi", "Sebelum jawaban benarnya: coba saring langsung dengan "
                 "<code>WHERE ROW_NUMBER()</code>. Jalankan.", "LAKUKAN"),
    kode("""con.execute(\"\"\"SELECT cabang FROM pesanan
WHERE ROW_NUMBER() OVER (ORDER BY cabang) <= 2\"\"\").fetchall()"""),
    blok("bahaya", "<pre><code>OperationalError: misuse of window function ROW_NUMBER()</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Sebabnya urutan eksekusi dari Level 1: <strong><code>WHERE</code> dijalankan jauh "
    "sebelum window function dihitung</strong>, jadi di saat <code>WHERE</code> bekerja, nomor "
    "urutnya belum ada.</p>",
    blok("catatan", "<strong>Ini pertanyaan lanjutan yang hampir pasti ditanyakan</strong> "
                    "setelah kamu menjawab soal 6. Sekarang kamu punya jawabannya, dan kamu "
                    "punya pesan errornya."))

langkah("Kunci soal 6, bagian 1 — ringkas dulu",
    blok("aksi", "Jalankan CTE-nya sendirian dulu, supaya kamu lihat isinya.", "LAKUKAN"),
    kode("""SELECT p.cabang, pr.nama AS produk,
       SUM(i.jumlah * i.harga_saat_itu) AS omzet
FROM pesanan p
JOIN item   i  ON i.pesanan_id = p.id
JOIN produk pr ON pr.id = i.produk_id
WHERE p.status = 'selesai'
GROUP BY p.cabang, pr.nama"""),
    blok("hasil", "<pre><code>21 baris — 3 cabang x 7 produk</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau CTE-mu tidak jalan sendirian, itu normal</strong> — "
                    "<code>WITH nama AS (…)</code> memang harus diikuti query yang memakainya. "
                    "Jalankan isi kurungnya saja seperti di atas, tanpa <code>WITH</code>."),
    "<p>Dua puluh satu baris. Belum diperingkat, belum disaring. <strong>Ini bahan mentahnya</strong>, "
    "dan langkah berikutnya cuma memberi nomor lalu memotong.</p>",
    blok("catatan", "<strong>Kalau kamu langsung menulis query utuhnya dan gagal</strong>, "
                    "kembalilah ke sini: jalankan CTE-nya sendiri dulu. Hampir semua kesalahan "
                    "query bertingkat ada di tingkat pertama, bukan di tingkat luarnya."))

langkah("Kunci soal 6 — pola top-N per kelompok",
    blok("aksi", "Perhatikan bentuknya: ringkas → beri nomor → saring.", "LAKUKAN"),
    kode("""WITH omzet AS (
  SELECT p.cabang, pr.nama AS produk,
         SUM(i.jumlah * i.harga_saat_itu) AS omzet
  FROM pesanan p
  JOIN item   i  ON i.pesanan_id = p.id
  JOIN produk pr ON pr.id = i.produk_id
  WHERE p.status = 'selesai'
  GROUP BY p.cabang, pr.nama
),
peringkat AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY cabang ORDER BY omzet DESC) AS urutan
  FROM omzet
)
SELECT cabang, urutan, produk, omzet
FROM peringkat WHERE urutan <= 2 ORDER BY cabang, urutan"""),
    blok("hasil", "<pre><code>    cabang  urutan        produk    omzet\n"
                  "0     Dago       1  Matcha Latte  2574000\n"
                  "1     Dago       2     Croissant  2450000\n"
                  "2   Kemang       1  Matcha Latte  2080000\n"
                  "3   Kemang       2    Roti Bakar  1890000\n"
                  "4  Seturan       1    Cheesecake  2250000\n"
                  "5  Seturan       2  Matcha Latte  1976000</code></pre>", "HARUS MUNCUL"),
    "<p>Bentuknya <strong>selalu sama</strong> untuk soal jenis ini, apa pun datanya. Hafalkan "
    "kerangkanya, bukan query-nya.</p>")

langkah("Pertanyaan lanjutan kedua: kenapa ROW_NUMBER, bukan RANK?",
    blok("aksi", "Siapkan jawabannya sekarang, sebelum ditanya.", "LAKUKAN"),
    tabel(["Fungsi", "Kalau ada seri di peringkat 2", "Jumlah baris per cabang"],
          [["<code>ROW_NUMBER</code>", "salah satu dapat 2, satunya dapat 3", "<strong>tepat 2</strong>"],
           ["<code>RANK</code>", "dua-duanya dapat 2, lalu lompat ke 4", "bisa 3 atau lebih"],
           ["<code>DENSE_RANK</code>", "dua-duanya dapat 2, lalu 3", "bisa 3 atau lebih"]]),
    blok("hasil", "<p>“Aku pakai <code>ROW_NUMBER</code> supaya jumlahnya persis dua; kalau seri "
                  "harus ikut semua, aku ganti <code>RANK</code>.”</p>", "YANG KAMU UCAPKAN"),
    "<p>Mana yang benar tergantung apa yang diminta. <strong>Jawaban terbaik adalah menyebut "
    "bahwa kamu tahu bedanya</strong> — bukan memilih satu dan diam.</p>")

langkah("Soal 7 — kerjakan dulu",
    blok("aksi", "Lima belas menit.", "LAKUKAN"),
    kode("""SOAL 7  Untuk cabang Dago: omzet tiap bulan, omzet bulan sebelumnya,
        selisihnya, dan pertumbuhannya dalam persen.""", salin=False))

langkah("Kunci soal 7",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""WITH bulanan AS (
  SELECT p.cabang, substr(p.tanggal,1,7) AS bulan,
         SUM(i.jumlah * i.harga_saat_itu) AS omzet
  FROM pesanan p JOIN item i ON i.pesanan_id = p.id
  WHERE p.status = 'selesai' GROUP BY p.cabang, bulan
)"""),
    blok("aksi", "Lalu query luarnya, disambung langsung di bawah CTE itu:", "LAKUKAN"),
    kode("""SELECT bulan, omzet,
  LAG(omzet) OVER w AS bulan_lalu,
  omzet - LAG(omzet) OVER w AS selisih,
  ROUND(100.0 * (omzet - LAG(omzet) OVER w) / LAG(omzet) OVER w, 1) AS persen
FROM bulanan WHERE cabang = 'Dago'
WINDOW w AS (PARTITION BY cabang ORDER BY bulan)
ORDER BY bulan"""),
    blok("catatan", "<strong>Klausa <code>WINDOW w AS (…)</code> itu menghemat mengetik</strong> — "
                    "kamu menulis <code>PARTITION BY … ORDER BY …</code> sekali, lalu memakainya "
                    "tiga kali sebagai <code>OVER w</code>. Hasilnya identik dengan menulisnya "
                    "berulang."),
    blok("hasil", "<pre><code>     bulan    omzet  bulan_lalu    selisih  persen\n"
                  "0  2024-01  2834000         NaN        NaN     NaN\n"
                  "1  2024-02  2731000   2834000.0  -103000.0    -3.6\n"
                  "2  2024-03  1286000   2731000.0 -1445000.0   -52.9\n"
                  "3  2024-04  1664000   1286000.0   378000.0    29.4\n"
                  "4  2024-05  1568000   1664000.0   -96000.0    -5.8\n"
                  "5  2024-06  2582000   1568000.0  1014000.0    64.7</code></pre>",
         "HARUS MUNCUL"),
    blok("catatan", "<strong>Baris pertama kosong, dan itu benar.</strong> Januari tidak punya "
                    "bulan sebelumnya. Jangan menutupinya dengan <code>COALESCE(…, 0)</code> — "
                    "menulis “pertumbuhan Januari 0%” adalah berbohong; <code>NULL</code> di sini "
                    "adalah jawaban yang jujur."))

langkah("Hapus satu titik nol, dan lihat persenmu berubah diam-diam",
    blok("aksi", "Ganti <code>100.0</code> jadi <code>100</code>. Jalankan berdampingan.", "LAKUKAN"),
    kode("""SELECT bulan,
  100  *(omzet-LAG(omzet) OVER w)/LAG(omzet) OVER w AS persen_bulat,
  ROUND(100.0*(omzet-LAG(omzet) OVER w)/LAG(omzet) OVER w,1) AS persen_benar
FROM bulanan WHERE cabang='Dago'
WINDOW w AS (PARTITION BY cabang ORDER BY bulan) ORDER BY bulan"""),
    blok("hasil", "<pre><code>     bulan  persen_bulat  persen_benar\n0  2024-01           NaN           NaN\n"
                  "1  2024-02          -3.0          -3.6\n2  2024-03         -52.0         -52.9\n"
                  "3  2024-04          29.0          29.4\n4  2024-05          -5.0          -5.8\n"
                  "5  2024-06          64.0          64.7</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Tidak ada error.</strong> Pembagian dua bilangan bulat di SQLite "
                   "(dan PostgreSQL) menghasilkan bilangan bulat — semua persentasemu dipotong "
                   "diam-diam. <code>100.0</code> yang memaksanya jadi desimal."))

langkah("Baca angkanya seperti analis, bukan seperti mesin",
    blok("aksi", "Lihat lagi kolom persen. Ada dua angka yang tidak wajar.", "LAKUKAN"),
    blok("hasil", "<p>Maret jatuh <strong>52,9%</strong>, lalu Juni melonjak "
                  "<strong>64,7%</strong>.</p>", "YANG HARUS KAMU LIHAT"),
    "<p>Persentase sebesar itu di angka sekecil ini hampir selalu berarti satu dari dua hal: "
    "<strong>ada kejadian nyata</strong> (cabang tutup renovasi, ada pesanan borongan) atau "
    "<strong>ada data yang belum masuk</strong>.</p>",
    blok("hasil", "<p>Jawaban yang benar bukan “Dago tumbuh 64,7%”, tapi <strong>“ada yang perlu "
                  "ditanyakan tentang Maret dan Juni sebelum angka ini dipakai.”</strong></p>",
         "YANG KAMU UCAPKAN"))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Kenapa WHERE ROW_NUMBER() ditolak, dan pesan errornya apa?
2. Pola tiga langkah untuk "top-N per kelompok"?
3. Bedanya ROW_NUMBER, RANK, DENSE_RANK kalau ada seri?
4. Kenapa 100.0 dan bukan 100?
5. Kenapa baris pertama LAG tidak boleh di-COALESCE jadi 0?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>WHERE</code> berjalan sebelum window function dihitung — "
    "<code>misuse of window function ROW_NUMBER()</code>. "
    "2. Ringkas di CTE → beri nomor dengan <code>ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)</code> "
    "→ saring <code>urutan &lt;= N</code> di query luar. "
    "3. <code>ROW_NUMBER</code> selalu unik; <code>RANK</code> memberi angka sama lalu melompat; "
    "<code>DENSE_RANK</code> memberi angka sama tanpa melompat. "
    "4. Pembagian bilangan bulat memotong desimalnya, tanpa error. "
    "5. Karena “tidak diketahui” bukan “nol” — menulisnya nol adalah berbohong.</p></details>")

HARI4 = {
  "n": "HARI 4", "tab": "4",
  "judul": "Window function: peringkat dalam kelompok, dan membandingkan dengan bulan lalu",
  "waktu": "± 85 menit",
  "tujuan": "menyelesaikan soal window function tanpa melihat contoh, dan menyiapkan jawaban "
            "untuk <strong>dua pertanyaan lanjutan</strong> yang hampir pasti menyusul.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu pola yang bentuknya selalu sama (top-N per "
           "kelompok), dua jawaban lanjutan yang sudah siap, dan satu titik nol yang kalau "
           "hilang mengubah semua persentasemu tanpa berbunyi.</p>"
           "<p style=\"margin-top:8px\">Besok dua soal terakhir — termasuk satu yang fungsinya "
           "<strong>tidak ada</strong> di SQLite, dan itu memang bagian dari soalnya.</p>",
}
