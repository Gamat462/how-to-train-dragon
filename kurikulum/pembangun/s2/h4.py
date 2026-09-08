# -*- coding: utf-8 -*-
"""Hari 4 — pintu masuk untuk ijazah akuntansi."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Baca satu syarat masuk, kata per kata",
    blok("aksi", "Baca kutipan ini pelan-pelan, lalu cari nama jurusanmu di dalamnya.", "LAKUKAN"),
    kode("""Edinburgh MSc Data Science, syarat masuk:
  - Gelar UK 2:1 dalam informatics, artificial intelligence,
    cognitive science, computer science, econometrics,
    electrical engineering, linguistics, mathematics,
    philosophy, physics, psychology, atau disiplin kuantitatif lain
  - Pengalaman pemrograman setara satu mata kuliah pengantar
  - 60 kredit SCQF / 30 ECTS matematika yang mencakup
    KALKULUS, ALJABAR LINEAR, dan MATEMATIKA DISKRIT""", salin=False),
    blok("hasil", "<p><strong>Akuntansi tidak ada dalam daftar itu.</strong></p>", "YANG KAMU TEMUKAN"),
    blok("bahaya", "<strong>Kamu bukan kandidat yang lemah untuk Edinburgh — kamu <em>tidak "
                   "memenuhi syarat</em>.</strong> Itu keputusan administratif yang tidak bisa "
                   "dibantah dengan portofolio sebagus apa pun."))

langkah("Hitung syarat 60 kredit matematikanya",
    blok("aksi", "Ubah “60 kredit SCQF / 30 ECTS” jadi satuan yang kamu pahami.", "LAKUKAN"),
    tabel(["Satuan", "Nilai", "Setara"],
          [["60 kredit SCQF", "= 30 ECTS", "± 4 mata kuliah matematika tingkat sarjana"],
           ["Bekalmu (pindaian Hari 2)", "kalkulus 3 modul · aljabar linear 5 modul", "MAT L2 dan L4 — bukan mata kuliah bertranskrip"]]),
    blok("bahaya", "<strong>Inilah selisih yang harus kamu pegang sepanjang hari ini:</strong> "
                   "MAT L1–L4 membuatmu <em>mampu mengikuti</em> kuliahnya. Yang memenuhi "
                   "<em>syarat administratif</em> hanyalah mata kuliah yang punya transkrip. "
                   "Dua hal berbeda — jangan mencampurnya."),
    blok("catatan", "<strong>Manchester</strong> (MSc Data Science, Business and Management) juga "
                    "menyebut “gelar dalam bidang kuantitatif atau komputasi” dan mensyaratkan "
                    "<strong>IELTS 7.0 tanpa komponen di bawah 6.5</strong> — salah satu syarat "
                    "bahasa tertinggi dalam daftar ini."))

langkah("Sekarang pintu yang justru terbuka",
    blok("aksi", "Baca kolom tengah. Cari yang menyebut akuntansi secara eksplisit.", "LAKUKAN"),
    tabel(["Program", "Posisi ijazah akuntansimu", "Catatan penting"],
          [["<strong>LSE</strong> — MSc Accounting and Data Analytics", "ini justru <em>bidang aslimu</em>",
            "10 bulan. AC415 wajib. <strong>GMAT atau GRE wajib untuk semua pelamar tanpa gelar sarjana UK.</strong>"],
           ["<strong>Bristol</strong> — MSc Data Science for Business", "diterima secara eksplisit",
            "Bristol memasukkan <strong>Accounting and Finance sebagai bidang kuantitatif</strong> yang memenuhi syarat"],
           ["<strong>Georgia Tech</strong> — OMS Analytics", "diterima meski bekal matematika kurang",
            "<strong>tanpa syarat GRE/GMAT.</strong> Pelamar yang bekal matematikanya belum cukup tetap bisa diterima"],
           ["<strong>Exeter</strong> — MSc Data Science", "dirancang untuk latar non-komputasi",
            "program <em>conversion</em>: materinya memang disusun untuk pendatang dari luar bidang"]]),
    blok("hasil", "<p><strong>LSE MSc Accounting and Data Analytics.</strong> Nama programnya "
                  "harfiah menggabungkan dua hal yang kamu punya. Di program ini, latar KAP-mu "
                  "bukan hambatan yang harus dijelaskan — itu <em>syarat masuknya</em>.</p>",
         "TEMUAN PALING BERGUNA HARI INI"))

langkah("Buat tabel daftarmu, lima kolom",
    blok("aksi", "Buat berkas <code>kampus.md</code> berisi kerangka ini, empat baris kosong.", "LAKUKAN"),
    kode("""| program | syarat matematika | GMAT/GRE | IELTS | tenggat |
|---------|-------------------|----------|-------|---------|
| 1.      |                   |          |       |         |
| 2.      |                   |          |       |         |
| 3.      |                   |          |       |         |
| 4.      |                   |          |       |         |"""),
    "<p>Tiga realistis, satu aspirasi. <strong>Sumbernya harus halaman resmi kampus</strong> — "
    "bukan agen pendidikan, dan bukan modul ini.</p>")

langkah("Isi tabelnya dari sumber primer, satu kampus dulu",
    blok("aksi", "Buka halaman <em>entry requirements</em> resmi satu kampus. Salin syaratnya "
                 "apa adanya ke tabelmu, termasuk angkanya.", "LAKUKAN"),
    blok("hasil", "<p>Satu baris terisi penuh, dengan tautan sumbernya di bawah tabel.</p>",
         "YANG HARUS ADA"),
    blok("bahaya", "<strong>Kenapa saya menyuruhmu mengecek ulang semua angka saya.</strong> "
                   "Riset modul ini dilakukan lewat hasil pencarian, karena akses langsung ke "
                   "situs kampus diblokir dari lingkungan kerja saya. Uang kuliah berubah tiap "
                   "tahun, dan beberapa sumber saling bertentangan — untuk Edinburgh saja saya "
                   "menemukan tiga angka berbeda (£38.500, £40.900, dan £45.410). Saya memakai "
                   "yang terendah."),
    "<p>Perlakukan seluruh modul ini seperti kertas kerja audit: <strong>berguna sebagai peta, "
    "wajib diuji ke sumber primer sebelum dipakai mengambil keputusan.</strong></p>")

langkah("Periksa daftarmu dengan satu pertanyaan",
    blok("aksi", "Setelah empat baris terisi, jawab satu pertanyaan untuk tiap baris.", "LAKUKAN"),
    tabel(["Pertanyaan", "Kalau jawabannya ya", "Kalau tidak"],
          [["Apakah syarat matematikanya bisa saya penuhi <strong>hari ini</strong>?",
            "kampus ini realistis", "ia butuh 6–12 bulan tambahan sebelum kamu bahkan mendaftar"],
           ["Apakah GMAT/GRE diwajibkan?", "tambah 2–3 bulan persiapan dan biaya tes", "satu hambatan hilang"],
           ["Apakah IELTS-nya di atas 6,5?", "targetmu naik, jadwalkan tes lebih awal", "6,0–6,5 cukup"]]),
    blok("catatan", "<strong>Kalau tiga dari empat barismu butuh 6–12 bulan tambahan,</strong> "
                    "daftarmu terlalu ambisius untuk siklus ini. Ganti satu dengan yang menerimamu "
                    "apa adanya — supaya kamu punya sesuatu untuk dikirim tahun ini."))

langkah("Kalau kamu tetap mengincar kampus yang mensyaratkan matematika",
    blok("aksi", "Baca tiga jalan ini, lalu tulis tanggal mulai yang realistis untuk masing-masing.", "LAKUKAN"),
    """<ol>
          <li><strong>Ambil kalkulus dan aljabar linear daring yang bersertifikat kredit</strong> —
          bukan sekadar sertifikat penyelesaian. Yang dihitung panitia adalah kredit yang bisa
          ditranskripkan.</li>
          <li><strong>Ambil GRE dan kejar nilai Quantitative yang tinggi.</strong> Untuk pelamar
          yang latar belakangnya diragukan, nilai GRE Quant sering dipakai sebagai bukti pengganti
          — LSE menyatakan ini secara eksplisit.</li>
          <li><strong>Pilih program <em>conversion</em></strong> seperti Exeter, yang memang
          menargetkan pendatang dari luar bidang komputasi.</li>
        </ol>""",
    blok("bahaya", "<strong>Jujur soal biayanya:</strong> ketiga jalan ini menambah 6–12 bulan "
                   "<em>sebelum kamu bahkan mendaftar</em>, dan menggeser mulai kuliah paling "
                   "cepat ke 2028. Bandingkan dengan LSE atau Bristol yang menerimamu apa adanya "
                   "sekarang."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Sebutkan dua kampus yang akan menolakmu otomatis dan dua "
                 "yang menerimamu apa adanya — beserta alasannya.", "LAKUKAN"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>Menolak otomatis:</strong> Edinburgh (akuntansi tidak ada di daftar
            jurusan, plus 60 kredit matematika) dan Manchester (bidang kuantitatif/komputasi,
            IELTS 7.0).</p>
            <p><strong>Menerima apa adanya:</strong> LSE (akuntansi justru syaratnya, tapi wajib
            GMAT/GRE) · Bristol (Accounting and Finance dihitung kuantitatif) · Georgia Tech
            (tanpa GRE, menerima bekal matematika yang kurang) · Exeter (program conversion).</p>
          </div>
        </details>""")

HARI4 = {
  "n": "HARI 4",
  "tab": "4",
  "judul": "Pintu mana yang terkunci untuk ijazah akuntansi, dan mana yang terbuka lebar",
  "waktu": "± 2,5 jam",
  "tujuan": "mengetahui — sebelum membayar biaya pendaftaran apa pun — kampus mana yang menolak "
            "lamaranmu secara otomatis, dan menyusun daftar empat kampus dari sumber primer, "
            "bukan dari modul ini.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p>Empat kampus menerimamu apa adanya; setidaknya dua akan menolakmu otomatis. Itu "
           "daftar pendek yang jauh lebih berguna daripada peringkat QS.</p>"
           "<p style=\"margin-top:8px\">Dan satu selisih yang harus kamu pegang: <strong>mampu "
           "mengikuti kuliahnya</strong> tidak sama dengan <strong>memenuhi syarat "
           "administratifnya</strong>. Besok: uangnya — siapa yang mau membayari, dan kapan "
           "tenggatnya.</p>",
}
