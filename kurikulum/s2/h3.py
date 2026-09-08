# -*- coding: utf-8 -*-
"""Hari 3 — harganya, dihitung sendiri dengan kalkulator."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Ambil kalkulatornya dan jalankan apa adanya",
    blok("aksi", "Salin <code>data-dan-skrip/jalur-s2/hitung_s2.py</code> dari paket zip. "
                 "Jalankan tanpa mengubah apa pun dulu.", "LAKUKAN"),
    kode("python hitung_s2.py"),
    blok("hasil", kode("""uang kuliah & biaya hidup: biaya sendiri
gaji yang hilang: Rp 14,0 jt/bln · impas dalam 5 tahun""", salin=False),
         "HARUS MUNCUL (dua baris pertama)"),
    "<p>Dua baris itu adalah <strong>asumsimu</strong>, dan keduanya bisa kamu ganti. "
    "Sisa hari ini menghitung apa yang mengalir dari sana.</p>")

langkah("Periksa dasar perhitungannya sebelum percaya hasilnya",
    blok("aksi", "Buka <code>hitung_s2.py</code> di editor. Baca bagian <code>KURS</code> dan "
                 "<code>RUTE</code> — semua angka sumbernya ada di situ, dalam mata uang aslinya.", "LAKUKAN"),
    tabel(["Yang dipakai", "Nilainya", "Dari mana"],
          [["Kurs jual, 6 Sep 2026", "USD 17.690 · GBP 24.114 · AUD 12.538 · CHF 22.489 · EUR 20.649 · SGD 14.044", "BCA, BRI, Yahoo Finance"],
           ["Biaya hidup Inggris", "£1.529/bln London · £1.171/bln luar London", "syarat dana visa pelajar UK 2026"],
           ["Biaya hidup Australia", "AUD 29.710/tahun", "syarat kapasitas keuangan visa pelajar"],
           ["Biaya hidup Jerman", "€992/bln = €11.904/tahun", "rekening terblokir 2026"],
           ["Biaya hidup Swiss", "CHF 1.850/bln", "titik tengah rentang CHF 1.500–2.200"]]),
    blok("bahaya", "<strong>Kenapa saya memakai syarat visa sebagai biaya hidup.</strong> Karena "
                   "itu angka resmi pemerintah, bukan cerita blog. Sisi buruknya: itu <em>batas "
                   "minimum yang mereka izinkan</em>, jadi biaya hidup sebenarnya biasanya lebih "
                   "tinggi. Semua angka di modul ini adalah <strong>perkiraan bawah</strong>, "
                   "bukan atas. Kamu yang menyuruh saya berhenti memakai batas atas — ini "
                   "kebalikannya, dan itu disengaja."))

langkah("Baca kolom “kantong”: uang yang benar-benar keluar",
    blok("aksi", "Lihat tiga kolom pertama hasilmu.", "LAKUKAN"),
    blok("hasil", kode("""rute                              bln    kantong  gaji hilang  biaya ekonomi
Georgia Tech OMSA (daring)         30      212,3          0,0          212,3
Jerman negeri (RWTH/TU Berlin)     24      521,3        336,0          857,3
TU Munich (non-UE)                 24      987,2        336,0        1.323,2
NUS MSc DSML                       18    1.159,9        252,0        1.411,9
Edinburgh                          12    1.267,2        168,0        1.435,2
Berkeley MIDS (daring)             24    1.454,6          0,0        1.454,6
ETH Zurich                         24    1.195,5        336,0        1.531,5
Imperial College London            12    1.404,6        168,0        1.572,6
CMU Heinz BIDA (daring)            30    1.585,0          0,0        1.585,0
University of Melbourne            24    2.245,6        336,0        2.581,6""", salin=False),
         "HARUS MUNCUL (dalam juta rupiah)"),
    "<p>Selisih antara termurah dan termahal <strong>sepuluh kali lipat</strong> — Rp 212 juta "
    "lawan Rp 2.245 juta — untuk gelar yang di CV sama-sama tertulis “Master”.</p>")

langkah("Temukan satu baris yang paling menyesatkan",
    blok("aksi", "Cari baris ETH Zurich. Pisahkan uang kuliahnya dari biaya hidupnya — buka "
                 "<code>RUTE</code> di editor untuk melihat angka aslinya.", "LAKUKAN"),
    tabel(["ETH Zurich", "Dalam CHF", "Dalam rupiah"],
          [["Uang kuliah, 2 tahun", "CHF 8.760", "197,0 jt"],
           ["Biaya hidup, 24 bulan", "CHF 44.400", "<strong>998,5 jt</strong>"]],
          kelas_n=(1, 2)),
    blok("hasil", "<p><strong>Biaya hidupnya lima kali lipat uang kuliahnya.</strong> “Kuliah "
                  "murah di Eropa” itu benar dan menyesatkan pada saat yang sama.</p>",
         "YANG BARU KAMU HITUNG"),
    blok("catatan", "<strong>Ini pola, bukan kekhususan ETH.</strong> Cek juga Jerman negeri: "
                    "uang kuliah Rp 29,7 juta, biaya hidup Rp 491,6 juta. Enam belas kali lipat. "
                    "Angka yang dipromosikan agen pendidikan hampir selalu yang kiri."))

langkah("Sekarang tambahkan gaji yang tidak kamu terima",
    blok("aksi", "Lihat kolom <code>gaji hilang</code>. Lalu buka editor dan ganti "
                 "<code>GAJI_SEKARANG</code> dengan angka yang realistis untukmu, jalankan lagi.", "LAKUKAN"),
    kode("GAJI_SEKARANG = 14_000_000      # ganti dengan angkamu"),
    "<p>Rp 14 juta/bulan adalah batas bawah Senior Associate Big 4 dengan 2–3 tahun pengalaman — "
    "posisi yang realistis untukmu setelah 50 modul, bukan angka mimpi. <strong>Kalau angkamu "
    "berbeda, ganti dan jalankan lagi.</strong> Itu gunanya berupa skrip, bukan tabel.</p>",
    blok("catatan", "<strong>Perhatikan tiga rute daring punya gaji hilang nol.</strong> Georgia "
                    "Tech, Berkeley, dan CMU tidak menghentikan pekerjaanmu. Kolom itu sendirian "
                    "yang mengubah urutan seluruh tabel."))

langkah("Balik pertanyaannya: berapa kenaikan yang HARUS terjadi",
    blok("aksi", "Lihat kolom <code>impas/bln</code>. Itu bukan ramalan gaji — itu syarat.", "LAKUKAN"),
    blok("hasil", kode("""rute                            biaya ekonomi  impas/bln  = bln gaji
Georgia Tech OMSA (daring)              212,3        3,5          35
Jerman negeri (RWTH/TU Berlin)          857,3       14,3         143
NUS MSc DSML                          1.411,9       23,5         235
Edinburgh                             1.435,2       23,9         239
Berkeley MIDS (daring)                1.454,6       24,2         242
ETH Zurich                            1.531,5       25,5         255
Imperial College London               1.572,6       26,2         262
CMU Heinz BIDA (daring)               1.585,0       26,4         264
University of Melbourne               2.581,6       43,0         430""", salin=False),
         "HARUS MUNCUL"),
    "<p>Bukan “berapa gaji setelah S2?” — itu mengarang. Tapi: <strong>berapa kenaikan gaji per "
    "bulan yang harus benar-benar terjadi, permanen, selama lima tahun, supaya modalnya "
    "kembali.</strong></p>")

langkah("Baca satu baris paling keras",
    blok("aksi", "Lihat baris Melbourne.", "LAKUKAN"),
    blok("bahaya", "<strong>+Rp 43,0 juta per bulan, permanen, selama lima tahun penuh — hanya "
                   "untuk kembali ke titik nol.</strong> Median gaji data analyst Indonesia "
                   "Rp 6 juta: total, bukan kenaikan. Kenaikan sebesar itu bukan “ambisius”; "
                   "itu di luar rentang yang ada datanya."),
    "<p>Kolom terakhir, <code>= bln gaji</code>, membaca hal yang sama dengan cara lain: biaya "
    "ekonominya setara <strong>430 bulan</strong> gaji pasar — 36 tahun.</p>",
    blok("hasil", "<p><strong>S2 luar negeri dengan biaya sendiri tidak masuk akal secara ekonomi "
                  "untukmu, di angka pasar Indonesia mana pun yang punya sumber.</strong> "
                  "Kecuali satu: Georgia Tech OMSA, karena kamu tetap bekerja.</p>",
         "KESIMPULAN SEMENTARA"))

langkah("Sekarang hapus uang kuliahnya",
    blok("aksi", "Jalankan sekali lagi dengan satu tambahan.", "LAKUKAN"),
    kode("python hitung_s2.py --beasiswa"),
    blok("hasil", kode("""rute                            biaya ekonomi  impas/bln  = bln gaji
Georgia Tech OMSA (daring)                0,0        0,0           0
Berkeley MIDS (daring)                    0,0        0,0           0
CMU Heinz BIDA (daring)                   0,0        0,0           0
Edinburgh                               168,0        2,8          28
Imperial College London                 168,0        2,8          28
NUS MSc DSML                            252,0        4,2          42
Jerman negeri (RWTH/TU Berlin)          336,0        5,6          56
University of Melbourne                 336,0        5,6          56""", salin=False),
         "HARUS MUNCUL"),
    blok("hasil", "<p>Rute Inggris satu tahun: dari butuh kenaikan <strong>Rp 26,2 juta/bulan</strong> "
                  "menjadi butuh <strong>Rp 2,8 juta/bulan</strong>. <strong>Turun sembilan kali "
                  "lipat.</strong> Kenaikan Rp 2,8 juta/bulan masuk akal dan ada datanya.</p>",
         "INILAH SELURUH JAWABANNYA"))

langkah("Ubah satu asumsi dan lihat apakah kesimpulannya goyah",
    blok("aksi", "Ini kebiasaan auditor, dan skripnya dibuat justru untuk ini. Ganti satu angka, "
                 "jalankan, lihat apakah kesimpulannya berubah.", "LAKUKAN"),
    tabel(["Ganti", "Jadi", "Yang mau kamu tahu"],
          [["<code>TAHUN_IMPAS</code>", "10", "apakah dengan waktu dua kali lipat, jalur non-beasiswa jadi masuk akal?"],
           ["<code>GAJI_SEKARANG</code>", "8.000.000", "kalau gajimu lebih rendah, apakah biaya ekonominya turun cukup jauh?"],
           ["<code>KURS[\"GBP\"]</code>", "28.000", "seberapa rapuh kesimpulannya terhadap kurs?"]]),
    blok("catatan", "<strong>Yang kamu cari bukan angka barunya, tapi apakah urutannya berubah.</strong> "
                    "Kalau Georgia Tech tetap paling murah di semua percobaan, kesimpulannya kokoh. "
                    "Kalau satu perubahan kecil membalik urutannya, kesimpulannya rapuh dan kamu "
                    "harus mencari angka yang lebih baik dulu."))

langkah("Tulis pertanyaan yang benar",
    blok("aksi", "Tutup halaman ini. Tulis satu kalimat.", "LAKUKAN"),
    blok("hasil", "<p>Pertanyaannya bukan <em>“apakah saya sebaiknya S2 di luar negeri”</em>. "
                  "Pertanyaannya <strong>“apakah saya bisa dapat beasiswa”</strong>.</p>",
         "PERTANYAAN YANG BENAR"),
    "<p>Dengan beasiswa: masuk akal. Tanpa beasiswa: tidak, kecuali OMSA. Sisa modul ini "
    "mengerjakan pertanyaan yang benar itu.</p>")

HARI3 = {
  "n": "HARI 3",
  "tab": "3",
  "judul": "Harganya, dihitung sendiri — dan satu kolom yang membalik semuanya",
  "waktu": "± 2 jam",
  "tujuan": "mengganti “S2 di luar negeri itu mahal” dengan angka yang kamu hitung sendiri, "
            "lalu menghitung hal yang hampir tidak pernah dihitung siapa pun: berapa kenaikan "
            "gaji yang <em>harus</em> terjadi supaya uangnya kembali.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> biaya hidup sering beberapa kali lipat uang "
           "kuliah · gaji yang hilang adalah biaya nyata · syarat impas adalah pertanyaan yang "
           "benar, bukan ramalan gaji · dengan beasiswa syaratnya turun sembilan kali lipat.</p>"
           "<p style=\"margin-top:8px\">Besok: apakah lamaranmu bahkan akan dibaca — karena ada "
           "masalah yang datang lebih dulu daripada uang.</p>",
}
