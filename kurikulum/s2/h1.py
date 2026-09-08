# -*- coding: utf-8 -*-
"""Hari 1 — apakah S2 itu gerbangnya."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buka Indeed sebelum membaca apa pun dari saya",
    blok("aksi", "Buka Indeed Indonesia. Cari <code>data analyst</code>, lokasi Jakarta. "
                 "Jangan gulung dulu — ambil sepuluh lowongan pertama apa adanya.", "LAKUKAN"),
    "<p>Sisa hari ini akan menunjukkan angka-angka saya. Tapi angka saya sudah berumur; "
    "pasarmu bergerak. <strong>Kalau hasilmu berbeda, hasilmu yang benar.</strong></p>",
    blok("bahaya", "<strong>Jangan lanjut ke langkah 2 sebelum sepuluh lowongan itu terbuka.</strong> "
                   "Kalau kamu membaca tabel saya lebih dulu, kamu akan menghitung sambil sudah "
                   "tahu jawaban yang saya harapkan. Itu bukan pengukuran lagi."))

langkah("Buat tabel tallynya, tiga kolom",
    blok("aksi", "Di kertas atau berkas teks, buat tiga kolom dan isi satu baris per lowongan.", "LAKUKAN"),
    kode("""no  syarat pendidikan tertulis          S2 wajib?
--  ----------------------------------  ---------
 1
 2
...
10""", salin=False),
    "<p>Kolom tengah diisi <strong>kutipan apa adanya</strong>, bukan ringkasanmu. "
    "\"Bachelor's degree in a quantitative field\" berbeda arti dari \"S1 semua jurusan\", "
    "dan bedanya baru terlihat kalau kamu menyalinnya.</p>")

langkah("Hitung tiga angka dari tabelmu",
    blok("aksi", "Setelah sepuluh baris terisi, hitung.", "LAKUKAN"),
    tabel(["Yang dihitung", "Angkamu"],
          [["Berapa yang menulis <strong>S2 wajib</strong>", "___ dari 10"],
           ["Berapa yang menulis <strong>S2 sebagai nilai tambah</strong>", "___ dari 10"],
           ["Berapa yang memasang filter <strong>STEM / kuantitatif</strong>", "___ dari 10"]]),
    blok("hasil", "<p>Tiga angka di kolom kanan. Tulis tanggalnya juga — angka ini akan kamu "
                  "pakai lagi di Hari 7, dan kamu perlu tahu kapan ia diambil.</p>", "HARUS ADA DI TANGANMU"),
    "<p>Angka ketiga yang paling penting, dan hampir tidak ada yang menghitungnya.</p>")

langkah("Bandingkan dengan tiga lowongan yang saya buka",
    blok("aksi", "Baru sekarang boleh dibaca. Ini kutipan dari Indeed Indonesia, September 2026.", "LAKUKAN"),
    tabel(["Perusahaan", "Posisi", "Syarat pendidikan — apa adanya"],
          [["PT Entrust Digital", "Data Analyst", "“Minimal education <strong>S1</strong>” · “<strong>STEM background</strong>”"],
           ["Moladin", "Data Analyst (3–5 th)", "“<strong>Bachelor's degree</strong> in Business Analytics, Finance, Economics, Statistics, Computer Science, or a matching quantitative field”"],
           ["Thakral One", "Data Science Manager (6+ th)", "“A <strong>Masters or Ph.D. will be an advantage</strong>”"]]),
    blok("hasil", "<p>Bahkan di posisi <em>manajer</em> dengan syarat 6 tahun pengalaman, S2 ditulis "
                  "sebagai <strong>“an advantage”</strong> — keunggulan, bukan syarat. "
                  "<strong>Nol dari tiga mensyaratkan S2.</strong></p>", "YANG TERBACA"),
    blok("catatan", "<strong>Tiga bukan sepuluh.</strong> Sampel saya kecil dan saya tidak "
                    "menyembunyikannya. Angkamu dari sepuluh lowongan lebih kuat daripada angka saya "
                    "dari tiga."))

langkah("Lihat apa yang dikatakan statistik nasional",
    blok("aksi", "Baca satu angka ini pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>BPS, dirilis November 2025: rata-rata upah buruh berpendidikan "
                  "<strong>Diploma IV, S1, S2, dan S3 dikelompokkan dalam satu golongan yang sama: "
                  "Rp 4,77 juta per bulan.</strong></p>", "DATA BPS"),
    "<p>BPS tidak memisahkan S2 dari S1 <em>karena selisihnya tidak cukup besar untuk dipisahkan</em>. "
    "Artinya bukan “S2 tidak berguna”. Artinya: gelar S2 saja, rata-rata, tidak menggeser upahmu.</p>",
    blok("bahaya", "<strong>Jebakan yang paling sering saya lihat.</strong> Orang membandingkan "
                   "“gaji lulusan S2 luar negeri” — yang dilaporkan alumni sukses di LinkedIn — "
                   "dengan “gaji rata-rata S1” yang dihitung BPS dari seluruh populasi. Itu "
                   "membandingkan batas atas melawan rata-rata. Kamu sendiri yang melarang saya "
                   "melakukan itu."))

langkah("Sekarang bagian yang menguntungkan S2",
    blok("aksi", "Lihat lagi baris kedua syarat PT Entrust Digital.", "LAKUKAN"),
    kode("""STEM background (STEM background adalah latar belakang pendidikan
yang berfokus pada bidang Sains (S), Teknologi (T), Engineering
atau Teknik (E), dan Mathematics atau Matematika (M))""", salin=False),
    blok("bahaya", "<strong>Akuntansi bukan STEM.</strong> Lowongan ini bahkan repot menjelaskan "
                   "singkatannya di dalam kurung — artinya mereka serius menyaringnya. Ijazahmu "
                   "gagal di filter ini, dan tidak ada portofolio, sertifikat, atau proyek buta "
                   "yang bisa mengubah tulisan di ijazah S1-mu."),
    blok("hasil", "<p><strong>Inilah nilai asli S2 untukmu.</strong> Bukan “supaya lebih pintar” — "
                  "50 modul sudah mengurus itu. Bukan “supaya gaji naik” — BPS bilang tidak. "
                  "Nilainya sangat spesifik: <strong>S2 Data Science mengubah statusmu dari "
                  "non-STEM menjadi STEM secara permanen di atas kertas.</strong></p>",
         "SATU GERBANG YANG NYATA"))

langkah("Ukur seberapa besar gerbang itu — pakai angkamu sendiri",
    blok("aksi", "Ambil angka ketiga dari langkah 3: berapa dari sepuluh lowongan yang memasang "
                 "filter STEM. Tulis sebagai persen.", "LAKUKAN"),
    tabel(["Angkamu", "Artinya"],
          [["0–1 dari 10", "Gerbangnya sempit. Biayanya besar untuk melewati satu pintu dari sepuluh."],
           ["2–4 dari 10", "Nyata tapi belum menentukan. Cek dulu apakah enam sisanya cukup untukmu."],
           ["5+ dari 10", "Gerbangnya lebar. Ini alasan kuat, dan seluruh sisa modul jadi relevan."]]),
    "<p>Dari tiga lowongan yang saya buka, <strong>satu</strong> memasang filter STEM. Moladin tidak "
    "— mereka menerima Finance dan Economics. Sebelum kamu membayar ratusan juta untuk melewati satu "
    "filter, kamu harus tahu seberapa sering filter itu dipasang.</p>")

langkah("Tulis ulang pertanyaanmu",
    blok("aksi", "Tutup halaman ini. Tulis satu kalimat di catatanmu.", "LAKUKAN"),
    "<p>Kamu masuk hari ini dengan pertanyaan <em>“apakah saya perlu S2?”</em> — pertanyaan yang "
    "tidak bisa dijawab siapa pun. Keluarlah dengan pertanyaan yang bisa dijawab:</p>",
    blok("hasil", "<p><strong>“Berapa persen lowongan yang saya incar memasang filter yang hanya "
                  "bisa saya lewati dengan gelar?”</strong></p>", "PERTANYAAN YANG BENAR"),
    blok("catatan", "<strong>Kalau angkamu masih nol setelah sepuluh lowongan,</strong> buka sepuluh "
                    "lagi minggu depan. Sepuluh terlalu sedikit untuk memutuskan sesuatu senilai "
                    "satu miliar rupiah — dan itu sendiri adalah temuan yang berguna."))

HARI1 = {
  "n": "HARI 1",
  "tab": "1",
  "judul": "Apakah S2 itu gerbangnya? Hitung sendiri, jangan tanya saya",
  "waktu": "± 2 jam",
  "tujuan": "mengganti tebakan “apakah saya perlu S2” dengan tiga angka yang kamu hitung sendiri "
            "dari lowongan sungguhan — termasuk satu filter yang selama ini mungkin luput dan "
            "justru merugikanmu.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> tiga angka dari sepuluh lowongan, bertanggal. "
           "Itu satu-satunya bukti di seluruh modul ini yang berasal dari pasarmu sendiri, bukan "
           "dari rata-rata orang lain.</p>"
           "<p style=\"margin-top:8px\">Besok kita bedah isi kuliahnya — bukan brosurnya, tapi "
           "kode mata kuliah wajibnya, dan berapa banyak yang sudah kamu kuasai.</p>",
}
