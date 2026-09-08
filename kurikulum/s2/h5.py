# -*- coding: utf-8 -*-
"""Hari 5 — beasiswa, dengan hitungan mundur yang dihitung ulang sendiri."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Jalankan hitungan mundurnya dari hari ini, bukan dari hari saya",
    blok("aksi", "Salin <code>data-dan-skrip/jalur-s2/hitung_tenggat.py</code> dari paket zip, "
                 "lalu jalankan tanpa argumen.", "LAKUKAN"),
    kode("python hitung_tenggat.py"),
    blok("hasil", kode("""TENGGAT
  Chevening 2027/28        2026-10-06    29 hari lagi     (6 Okt 2026, 11:00 UTC)
  LPDP Tahap 1 2027        2027-02-23   169 hari lagi     (perkiraan, pola 2026)
  Australia Awards 2028    2027-04-30   235 hari lagi     (jendela 1 Feb - 30 Apr 2027)""",
         salin=False), "HARUS MUNCUL (kalau hari ini 7 Sep 2026)"),
    blok("catatan", "<strong>Angkamu pasti berbeda dari saya</strong>, dan itu memang tujuannya. "
                    "Modul yang menuliskan “tinggal 29 hari” jadi salah keesokan harinya. Skrip "
                    "ini menghitungnya ulang tiap kali dijalankan."))

langkah("Baca baris paling atas dua kali",
    blok("aksi", "Lihat sisa hari untuk Chevening di layarmu.", "LAKUKAN"),
    blok("bahaya", "<strong>Chevening mensyaratkan minimum dua tahun pengalaman kerja "
                   "(setara 2.800 jam) — dan kamu sudah melewatinya bertahun-tahun lalu di KAP.</strong> "
                   "Ini bukan tenggat yang “sebaiknya dipertimbangkan”. Ini pintu yang sedang "
                   "terbuka dan akan tertutup selama setahun penuh."),
    "<p>Kalau angkanya sudah negatif di layarmu, jendela itu sudah lewat — dan yang berlaku adalah "
    "siklus berikutnya. Perbarui tanggalnya di dalam skrip, jangan menebak.</p>")

langkah("Bandingkan syarat ketiganya berdampingan",
    blok("aksi", "Cari satu baris yang kamu belum penuhi.", "LAKUKAN"),
    tabel(["Syarat", "LPDP (reguler LN)", "Chevening", "Australia Awards"],
          [["Usia maksimum S2", "35 th per 31 Des 2026", "tidak ada", "tidak ada"],
           ["IPK minimum", "2,50", "—", "—"],
           ["Pengalaman kerja", "—", "<strong>2 th / 2.800 jam</strong>", "—"],
           ["Bahasa Inggris", "IELTS 6,5 · TOEFL iBT 80 · PTE 58", "syarat kampusnya", "<strong>IELTS 6,0</strong>"],
           ["Masa berlaku sertifikat", "maks. 2 tahun", "—", "berlaku 1 Jan 2027, tes setelah 1 Jan 2025"],
           ["Ikatan setelah lulus", "wajib pulang", "<strong>pulang min. 2 tahun</strong>", "wajib pulang"],
           ["Kewajiban lain", "—", "—", "<strong>pelatihan EAP penuh waktu</strong> Sen–Jum 08.00–16.00 sebelum berangkat"]]),
    blok("hasil", "<p>Baris <strong>Bahasa Inggris</strong>. Kamu belum punya IELTS, dan ketiga "
                  "jalur membutuhkannya.</p>", "BARIS YANG BELUM KAMU PENUHI"))

langkah("Hitung usiamu per 31 Desember 2026",
    blok("aksi", "Satu baris di terminal. Ganti tanggal lahirnya dengan milikmu.", "LAKUKAN"),
    kode('''python3 -c "from datetime import date; l=date(1996,5,20); b=date(2026,12,31); print(b.year-l.year-((b.month,b.day)<(l.month,l.day)), 'tahun')"'''),
    blok("hasil", kode("30 tahun", salin=False), "HARUS MUNCUL (untuk contoh 20 Mei 1996)"),
    tabel(["Usiamu per 31 Des 2026", "Artinya untuk LPDP"],
          [["di bawah 33", "jendelamu masih 3+ siklus. Tidak perlu terburu-buru."],
           ["33–34", "tersisa 1–2 siklus. LPDP naik prioritas."],
           ["35 ke atas", "jalur S2 reguler LPDP tertutup. Chevening dan AAS tidak punya batas usia."]]),
    blok("catatan", "<strong>Batas 35 tahun dihitung per 31 Desember tahun pendaftaran</strong>, "
                    "bukan per tanggal kamu mendaftar. Selisihnya bisa satu siklus penuh."))

langkah("Pilih target IELTS yang paling murah dikejar",
    blok("aksi", "Lihat tiga angka ini dan pilih satu sebagai targetmu.", "LAKUKAN"),
    tabel(["Target", "Untuk", "Catatan"],
          [["<strong>6,0</strong>", "Australia Awards", "paling ringan; targetkan ini dulu"],
           ["<strong>6,5</strong>", "LPDP", "target realistis kedua"],
           ["<strong>7,0</strong> tanpa komponen &lt; 6,5", "Manchester", "paling berat; hanya kalau kampus itu memang tujuanmu"]]),
    "<p>Ambil satu tes, bukan tiga. Skor 7,0 memenuhi semuanya sekaligus — tapi mengejar 7,0 "
    "menunda tesmu berbulan-bulan. <strong>Skor 6,5 membuka LPDP dan AAS sekaligus</strong>, "
    "dan itu titik yang paling masuk akal.</p>",
    blok("bahaya", "<strong>Pesan jadwal tesnya minggu ini juga.</strong> Kursi IELTS sering penuh "
                   "3–6 minggu di muka. Ini satu-satunya langkah di seluruh modul yang gagal "
                   "hanya karena ditunda seminggu."))

langkah("Lihat isi LPDP, dan apa yang baru dihapus",
    blok("aksi", "Baca tabelnya, lalu perhatikan baris terakhir.", "LAKUKAN"),
    tabel(["Komponen", "Besaran"],
          [["Dana hidup bulanan", "menyesuaikan standar biaya hidup negara tujuan"],
           ["Dana kedatangan", "<strong>200% dari dana hidup bulanan</strong>"],
           ["Tunjangan buku", "maks. Rp 10 juta/tahun"],
           ["Asuransi kesehatan", "maks. Rp 29 juta/tahun"],
           ["Tunjangan keluarga", "25% dari dana hidup, maks. 2 orang"],
           ["<em>Dihapus mulai 2026</em>", "<em>biaya laptop · visa keluarga · publikasi jurnal</em>"]]),
    blok("catatan", "<strong>Hubungkan dengan Hari 3.</strong> Kalau uang kuliah dan biaya hidup "
                    "ditanggung, yang tersisa cuma gaji yang tidak kamu terima — dan syarat "
                    "impasmu turun dari Rp 26,2 juta jadi Rp 2,8 juta per bulan."))

langkah("Cocokkan daftar kampusmu dengan daftar LPDP",
    blok("aksi", "Unduh buku “Daftar Perguruan Tinggi Tujuan” LPDP terbaru dari "
                 "<code>lpdp.kemenkeu.go.id</code>. Cocokkan dengan empat kampus dari Hari 4.", "LAKUKAN"),
    blok("bahaya", "<strong>Perubahan LPDP 2026 yang paling berdampak:</strong> daftar Perguruan "
                   "Tinggi Utama Dunia yang diprioritaskan <strong>dipangkas dari 30 menjadi 17 "
                   "kampus</strong>, seiring pengetatan fokus ke bidang STEM dan industri "
                   "strategis. Kampus yang tidak ada di daftar akan menggugurkan berkasmu, "
                   "sebagus apa pun esaimu."),
    blok("hasil", "<p>Empat baris di <code>kampus.md</code>-mu, masing-masing bertanda "
                  "<strong>ada</strong> atau <strong>tidak ada</strong> di daftar LPDP.</p>",
         "YANG HARUS ADA SETELAH LANGKAH INI"),
    "<p>Kalau LSE atau Bristol tidak ada di daftar untuk bidangmu, itu mengubah rencanamu "
    "<strong>hari ini juga</strong> — bukan nanti setelah esaimu selesai.</p>")

langkah("Satu perubahan aturan visa yang memangkas nilai gelar Inggris",
    blok("aksi", "Baca, lalu hubungkan dengan satu angka yang sudah kamu punya.", "LAKUKAN"),
    blok("hasil", "<p>Mahasiswa yang <strong>menyelesaikan studi setelah 1 Januari 2027</strong> "
                  "mendapat <strong>18 bulan</strong> izin kerja pascastudi (Graduate Route), "
                  "bukan 2 tahun lagi. Yang menentukan adalah <em>tanggal kamu mengajukan</em>, "
                  "bukan tanggal kuliahmu dimulai. Lulusan S3 tetap 3 tahun.</p>", "ATURAN BARU"),
    blok("bahaya", "<strong>Riset LPEM FEB UI atas Sakernas BPS Agustus 2025 mencatat rata-rata "
                   "pencarian kerja di Indonesia 19,8 bulan.</strong> Kalau di Inggris pun butuh "
                   "waktu sebanding, izin 18 bulan itu <em>lebih pendek daripada rata-rata lama "
                   "orang mendapatkan pekerjaan</em>. Rencana “kuliah di Inggris lalu kerja di "
                   "sana untuk balik modal” baru saja kehilangan enam bulan dari margin yang "
                   "sudah tipis."))

langkah("Pasang pengingat, bukan niat",
    blok("aksi", "Buka kalender di HP-mu. Pasang tiga pengingat, masing-masing dua minggu "
                 "<em>sebelum</em> tenggatnya.", "LAKUKAN"),
    tabel(["Pengingat", "Kapan"],
          [["Chevening — kirim, jangan tunggu hari terakhir", "22 September 2026"],
           ["LPDP — cek pengumuman jadwal Tahap 1", "1 Januari 2027"],
           ["Australia Awards — jendela buka", "25 Januari 2027"]]),
    blok("catatan", "<strong>Jangan mengirim di hari terakhir.</strong> Server Chevening kelebihan "
                    "beban tiap tahun menjelang tenggat, dan tidak ada perpanjangan untuk itu."))

HARI5 = {
  "n": "HARI 5",
  "tab": "5",
  "judul": "Beasiswa: syaratnya, isinya, dan hitungan mundur yang tidak pernah basi",
  "waktu": "± 2,5 jam",
  "tujuan": "Hari 3 membuktikan seluruh keputusan ini bergantung pada beasiswa. Hari ini kamu "
            "menghitung sendiri sisa waktunya, mengukur usiamu terhadap batas LPDP, dan memilih "
            "target IELTS.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> Chevening tidak punya batas usia dan syarat "
           "terberatnya sudah kamu penuhi · batas usia LPDP dihitung per 31 Desember · IELTS 6,5 "
           "membuka dua jalur sekaligus · daftar kampus LPDP dipangkas jadi 17 · Graduate Route "
           "Inggris turun jadi 18 bulan.</p>"
           "<p style=\"margin-top:8px\">Besok kita ubah semua ini menjadi kalender — dengan "
           "tanggal yang dihitung skrip, bukan niat.</p>",
}
