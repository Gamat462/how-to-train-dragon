# -*- coding: utf-8 -*-
"""Hari 2 — silabus kampus, dan peta lubang yang dipindai sendiri."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Baca lima mata kuliah wajib NUS",
    blok("aksi", "Baca tabelnya sekali, lalu tutup halaman dan sebutkan kembali berapa mata "
                 "kuliah wajibnya dan berapa unit totalnya.", "LAKUKAN"),
    tabel(["Kode", "Nama mata kuliah", "Unit"],
          [["<code>DSA5101</code>", "Introduction to Big Data for Industry", "4"],
           ["<code>DSA5103</code>", "Optimization Algorithms for Data Modelling", "4"],
           ["<code>DSA5104</code>", "Principles of Data Management and Retrieval", "4"],
           ["<code>DSA5105</code>", "Principles of Machine Learning", "4"],
           ["<code>DSA5106</code>", "Deep Learning: Foundations and Techniques", "4"]],
          kelas_n=(2,)),
    "<p>Lima inti wajib (20 unit) ditambah lima pilihan (20 unit). Struktur untuk angkatan "
    "masuk AY2025 dan AY2026.</p>",
    blok("catatan", "<strong>Perhatikan DSA5103.</strong> “Optimization Algorithms” bukan mata "
                    "kuliah pemrograman — itu matematika: fungsi konveks, gradien, pengali "
                    "Lagrange. Kalau kalkulus multivariabelmu belum kuat, ini mata kuliah yang "
                    "akan menghabisimu di semester pertama."))

langkah("Baca enam mata kuliah wajib Melbourne, lalu hitung satu hal",
    blok("aksi", "Baca tabelnya, lalu hitung: dari enam mata kuliah ini, berapa yang bertumpu "
                 "pada <strong>statistika matematis</strong> dan berapa yang mengajarkan "
                 "<strong>alat</strong>?", "LAKUKAN"),
    tabel(["Kode", "Nama mata kuliah", "Rumpun"],
          [["<code>MAST90138</code>", "Multivariate Statistics for Data Science", "Statistika"],
           ["<code>MAST90139</code>", "Statistical Modelling for Data Science", "Statistika"],
           ["<code>MAST90083</code>", "Computational Statistics &amp; Data Science", "Statistika"],
           ["<code>COMP90024</code>", "Cluster and Cloud Computing", "Ilmu komputer"],
           ["<code>COMP90050</code>", "Advanced Database Systems", "Ilmu komputer"],
           ["<code>COMP90051</code>", "Statistical Machine Learning", "Ilmu komputer"]]),
    blok("hasil", "<p><strong>Empat dari enam</strong> bertumpu pada statistika matematis. "
                  "<strong>Nol</strong> yang mengajarkan alat — tidak ada mata kuliah bernama "
                  "“Tableau” atau “Power BI”.</p>", "JAWABANNYA"),
    "<p>S2 Data Science yang baik <em>tidak</em> mengajarkan yang sudah kamu pelajari di 50 modul. "
    "Ia mengajarkan lapisan di bawahnya.</p>")

langkah("Lima kampus lain, dan satu pola yang menentukan Hari 3",
    blok("aksi", "Baca kolom “Bentuk”. Hitung berapa yang daring.", "LAKUKAN"),
    tabel(["Kampus &amp; program", "Bentuk", "Isi wajib yang tercatat"],
          [["<strong>UC Berkeley</strong> — MIDS", "Daring, ± 2 th, 27 unit",
            "DATASCI W201 · W203 Statistics for Data Science · W205 Data Engineering · W207 Applied ML · W210 Capstone"],
           ["<strong>CMU Heinz</strong> — jalur BIDA", "Daring, ± 12 mata kuliah, 2–3 th",
            "Database Management · Data Warehousing · Data Mining · Exploring and Visualizing Data · Privacy in the Digital Age · Advanced Business Analytics"],
           ["<strong>Georgia Tech</strong> — OMS Analytics", "Daring, 36 kredit, 24–36 bln",
            "ISYE 6501 Analytics Modeling (R) · CSE 6040 Computing for Data Analysis (Python) · 6748 Practicum"],
           ["<strong>UCL</strong> — Data Science MSc", "Tatap muka, 12 bln",
            "STAT0032 Introduction to Statistical Data Science + maks. dua modul ilmu komputer + proyek riset"],
           ["<strong>Imperial</strong> — MSc Statistics (DS &amp; ML)", "Tatap muka, 12 bln",
            "Fondasi statistika di term 1, lalu satu dari lima aliran"]]),
    blok("hasil", "<p><strong>Tiga dari lima daring.</strong> Georgia Tech, Berkeley, dan CMU "
                  "tidak mengharuskanmu pindah negara.</p>", "YANG HARUS KAMU HITUNG"),
    blok("catatan", "<strong>Simpan angka itu untuk besok.</strong> Biaya hidup di luar negeri — "
                    "bukan uang kuliah — yang sering jadi bagian terbesar tagihannya. Program "
                    "daring memotongnya jadi nol."))

langkah("Ambil pemindainya, jangan percaya peta buatan saya",
    blok("aksi", "Dari paket zip, salin <code>data-dan-skrip/jalur-s2/pindai_topik.py</code> ke "
                 "folder paket — sejajar dengan folder <code>kurikulum/</code>. Lalu jalankan.", "LAKUKAN"),
    kode("python pindai_topik.py"),
    blok("hasil", kode("memindai 58 modul di kurikulum/  (ambang: disebut >= 3 kali)", salin=False),
         "HARUS MUNCUL (baris pertama)"),
    "<p>Skrip ini membaca <strong>teks seluruh modulmu</strong> dan menghitung berapa modul yang "
    "benar-benar membahas tiap topik penyusun silabus di atas. Bukan ingatan saya — hitungan.</p>",
    blok("catatan", "<strong>Kalau muncul “tidak ada berkas .html”:</strong> kamu menjalankannya "
                    "dari folder yang salah. Skripnya harus berada di sebelah folder "
                    "<code>kurikulum/</code>, bukan di dalamnya."))

langkah("Baca hasil pindaiannya",
    blok("hasil", kode("""topik dalam silabus S2           modul   modul yang paling membahasnya
pandas / pembersihan data           21   022-M03-python-pandas.html
SQL join & agregasi                 28   911-referensi-sql-pandas.html
Git & rekayasa perangkat lunak      21   045-M11-git-otomasi-streamlit.html
rekayasa data / pipeline            12   044-M10-dbt.html
desain & indeks basis data          12   073-sql-mahir-L4.html
visualisasi                         11   041-M08-visualisasi-bi.html
big data / Spark / cloud            11   043-M09-sql-data-besar.html
A/B test                             9   912-referensi-statistik-abtest.html
window function                      9   072-sql-mahir-L3.html
machine learning                     7   085-jalur-s2-luar-negeri.html
regresi                              7   091-mat-L2-aljabar-linear.html
aljabar linear / matriks             5   091-mat-L2-aljabar-linear.html
optimisasi                           5   092-mat-L3-optimisasi.html
kalkulus / turunan                   3   093-mat-L4-deep-learning.html
probabilitas formal                  3   090-mat-L1-probabilitas.html
deep learning                        3   093-mat-L4-deep-learning.html
statistik inferensial                2   023-M04-statistik-abtest.html
etika & privasi data                 1   042-bekal-rahasia-klien.html""", salin=False),
         "HARUS MUNCUL"),
    blok("catatan", "<strong>Angkamu boleh sedikit berbeda</strong> kalau kurikulummu sudah "
                    "bertambah modul. Yang harus sama: urutannya, dan dua baris paling bawah."))

langkah("Lihat apa yang berubah sejak modul ini pertama ditulis",
    blok("aksi", "Bandingkan hasil pindaianmu dengan angka lama di bawah ini.", "LAKUKAN"),
    tabel(["Topik", "Saat modul ini ditulis pertama kali", "Sekarang", "Yang menutupnya"],
          [["probabilitas formal", "<strong>0</strong>", "3", "MAT L1"],
           ["aljabar linear / matriks", "<strong>0</strong>", "5", "MAT L2"],
           ["optimisasi", "<strong>0</strong>", "5", "MAT L3"],
           ["deep learning", "<strong>0</strong>", "3", "MAT L4"]]),
    blok("hasil", "<p><strong>Empat lubang terbesar sudah ditutup</strong> — MAT L1 sampai L4 "
                  "dibuat setelah modul ini pertama ditulis, justru karena pindaian ini "
                  "menemukannya.</p>", "YANG BERUBAH"),
    "<p>Inilah gunanya menghitung dan bukan mengingat. Peta yang diketik tangan akan basi diam-diam; "
    "peta yang dihitung ulang tidak bisa.</p>")

langkah("Sekarang lubang yang sebenarnya",
    blok("aksi", "Lihat dua baris paling bawah hasil pindaianmu.", "LAKUKAN"),
    blok("bahaya", "<strong>etika &amp; privasi data: 1 modul. statistik inferensial: 2 modul.</strong> "
                   "Dua-duanya ada di silabus wajib: <em>Privacy in the Digital Age</em> (CMU) dan "
                   "<em>MAST90139 Statistical Modelling</em> (Melbourne). Ini daftar belanja "
                   "belajarmu yang sekarang, menggantikan daftar lama."),
    tabel(["Lubang", "Menutup mata kuliah", "Bisa ditutup dengan"],
          [["etika &amp; privasi data", "Privacy in the Digital Age (CMU)",
            "Bekal Rahasia Klien sudah menutup sisi praktiknya; sisi regulasinya (GDPR, UU PDP) belum"],
           ["statistik inferensial", "MAST90139 (Melbourne) · W203 (Berkeley)",
            "M4 Statistik &amp; A/B test menutup dasarnya; uji hipotesis formal belum"]]),
    blok("catatan", "<strong>Perhatikan bahwa keduanya bukan matematika berat.</strong> Berbeda "
                    "dengan empat lubang lama, dua ini bisa ditutup dengan membaca dan latihan "
                    "beberapa minggu, bukan modul 7 hari."))

langkah("Salin dua baris itu ke catatanmu",
    blok("aksi", "Tulis dua lubang itu di catatan, dengan tanggal pindaianmu.", "LAKUKAN"),
    "<p>Di Hari 4 kamu akan melihat bahwa beberapa kampus mengubah daftar ini dari “sebaiknya” "
    "menjadi <strong>syarat masuk tertulis</strong> — dan di situ selisih antara “sudah bisa” "
    "dan “punya transkripnya” jadi menentukan.</p>",
    blok("bahaya", "<strong>Ini kalimat terpenting di seluruh modul.</strong> 50 modulmu dirancang "
                   "membuatmu <em>bisa dipekerjakan</em>. Modul-modul itu tidak dirancang membuatmu "
                   "<em>bisa diterima kuliah S2</em>. Itu dua target berbeda — dan MAT L1–L4 ada "
                   "justru karena selisih itu ditemukan di sini."))

HARI2 = {
  "n": "HARI 2",
  "tab": "2",
  "judul": "Silabusnya, dan pindaian yang menghitung lubangmu sendiri",
  "waktu": "± 2,5 jam",
  "tujuan": "melihat mata kuliah wajib tujuh kampus, lalu menjalankan satu skrip yang memindai "
            "seluruh modulmu dan memberitahu topik mana yang benar-benar tipis — hitungan, "
            "bukan ingatan.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> hasil pindaian bertanggal, dan dua lubang yang "
           "masih nyata (etika/privasi dan statistik inferensial). Empat lubang lama sudah "
           "ditutup MAT L1–L4.</p>"
           "<p style=\"margin-top:8px\">Besok: harganya. Kamu akan menghitungnya sendiri dengan "
           "kalkulator yang bisa kamu ubah asumsinya — bukan membaca tabel saya.</p>",
}
