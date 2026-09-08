# -*- coding: utf-8 -*-
"""Hari 7 — keputusan, dengan rubrik yang dijalankan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Lihat pernyataan rubriknya sebelum menjawab",
    blok("aksi", "Salin <code>data-dan-skrip/jalur-s2/skor_rubrik.py</code> dari paket zip. "
                 "Jalankan tanpa membuat berkas jawaban dulu.", "LAKUKAN"),
    kode("python skor_rubrik.py"),
    blok("hasil", kode("""buat dulu jawaban.txt berisi 8 baris Y atau T:

  1. [2 poin] Uang kuliah DAN biaya hidupnya dibayar orang lain (beasiswa penuh)
  2. [1 poin] Usiaku pada 31 Des tahun depan masih di bawah 33
  3. [1 poin] Aku mengincar pekerjaan yang benar-benar memfilter 'STEM background'
  4. [1 poin] Aku ingin bekerja atau menetap di luar negeri, bukan hanya kuliah di sana
  5. [2 poin] Aku menginginkan riset, S3, atau mengajar
  6. [1 poin] Aku sudah punya IELTS/TOEFL yang masih berlaku
  7. [1 poin] Aku sanggup tidak berpenghasilan 12-24 bulan tanpa mengganggu siapa pun
  8. [2 poin] Aku sudah melamar 20+ posisi analitik audit/risiko dan ditolak karena pendidikan""",
         salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Jangan menjawab Y untuk hal yang “bisa diusahakan nanti”.</strong> "
                   "Rubrik ini menilai keadaanmu hari ini. Menjawab Y untuk beasiswa yang belum "
                   "kamu punya membuat seluruh hitungannya tidak berguna."))

langkah("Jawab kedelapannya, satu baris per jawaban",
    blok("aksi", "Buat <code>jawaban.txt</code> berisi delapan baris <code>Y</code> atau "
                 "<code>T</code>. Lalu jalankan lagi.", "LAKUKAN"),
    kode("python skor_rubrik.py"),
    blok("hasil", kode("""  [T] 0/2  Uang kuliah DAN biaya hidupnya dibayar orang lain (beasiswa penuh)
  [Y] 1/1  Usiaku pada 31 Des tahun depan masih di bawah 33
  [T] 0/1  Aku mengincar pekerjaan yang benar-benar memfilter 'STEM background'
  [Y] 1/1  Aku ingin bekerja atau menetap di luar negeri, bukan hanya kuliah di sana
  [T] 0/2  Aku menginginkan riset, S3, atau mengajar
  [T] 0/1  Aku sudah punya IELTS/TOEFL yang masih berlaku
  [Y] 1/1  Aku sanggup tidak berpenghasilan 12-24 bulan tanpa mengganggu siapa pun
  [T] 0/2  Aku sudah melamar 20+ posisi analitik audit/risiko dan ditolak karena pendidikan

skor: 3 dari 11
bacaan: Lamar beasiswanya, jangan biayai sendiri
        Kalau ditolak, tidak ada yang hilang selain waktumu.""", salin=False),
         "CONTOH KELUARAN"),
    blok("catatan", "<strong>Contoh di atas bukan jawabanmu</strong> — itu satu kemungkinan. "
                    "Yang berarti adalah skormu sendiri dan bacaan yang keluar bersamanya."))

langkah("Perhatikan baris nomor 3 dan bandingkan dengan angkamu di Hari 1",
    blok("aksi", "Ambil angka ketiga dari Hari 1: berapa dari sepuluh lowongan yang memasang "
                 "filter STEM. Baru putuskan jawaban baris 3.", "LAKUKAN"),
    tabel(["Angkamu di Hari 1", "Jawaban baris 3"],
          [["0–1 dari 10", "<strong>T</strong> — filternya terlalu jarang untuk jadi alasan"],
           ["2–4 dari 10", "boleh Y, tapi catat bahwa alasannya lemah"],
           ["5+ dari 10", "<strong>Y</strong> — dan ini alasan terkuatmu"]]),
    "<p>Inilah gunanya Hari 1 dikerjakan sebelum Hari 7. Baris ini tidak dijawab dengan perasaan; "
    "ia dijawab dengan angka yang kamu hitung sendiri enam hari lalu.</p>")

langkah("Perhatikan baris nomor 8 dan bobotnya",
    blok("aksi", "Baca baris 8 sekali lagi, lalu hitung berapa lamaran yang sudah kamu kirim.", "LAKUKAN"),
    blok("bahaya", "<strong>Bukti terkuat bahwa kamu butuh gelar adalah penolakan nyata karena "
                   "gelar</strong> — bukan dugaan bahwa kamu akan ditolak. Kalau kamu belum "
                   "melamar, seluruh perhitungan modul ini bertumpu pada rata-rata orang lain, "
                   "bukan pada pasarmu."),
    "<p>Itu sebabnya baris ini berbobot 2 poin, sama dengan beasiswa penuh dan sama dengan jalur "
    "riset. Ia satu-satunya baris yang datanya bisa kamu kumpulkan sendiri dalam sebulan, "
    "tanpa biaya.</p>")

langkah("Baca rekomendasi saya, dan alasan tiap barisnya",
    blok("aksi", "Baca urutannya. Perhatikan bahwa lima dari enam baris tidak berbiaya uang.", "LAKUKAN"),
    tabel(["Urutan", "Lakukan", "Kenapa"],
          [["1", "<strong>Lamar Chevening sebelum tenggatnya</strong>", "biayanya cuma waktumu; syarat terberatnya sudah kamu penuhi"],
           ["2", "<strong>Selesaikan fase 1–5</strong>", "membuatmu bisa dipekerjakan <em>dan</em> mengisi lamaran beasiswamu"],
           ["3", "<strong>Ambil IELTS sebelum jendela LPDP</strong>", "gerbang bersama semua jalur"],
           ["4", "<strong>Lamar LPDP dan Australia Awards</strong>", "tiga lemparan ke tiga sasaran dalam satu siklus"],
           ["5", "<strong>Jangan biayai S2 luar negeri dari kantong sendiri</strong>", "tabel Hari 3: butuh kenaikan Rp 23–43 juta/bulan di pasar yang mediannya Rp 6 juta"],
           ["6", "<strong>Kalau tetap ingin gelar tanpa beasiswa: Georgia Tech OMSA</strong>", "Rp 212 juta, tanpa berhenti bekerja, tanpa GRE — satu-satunya yang lolos uji ekonomi"]]),
    blok("catatan", "<strong>Kamu memintaku memakai skema rata-rata, bukan batas atas.</strong> "
                    "Enam baris ini adalah rekomendasi versi rata-rata, dan itu sebabnya ia "
                    "terdengar hati-hati."))

langkah("Baca juga apa yang tidak akan saya katakan",
    blok("aksi", "Baca sekali, pelan.", "LAKUKAN"),
    blok("bahaya", "<strong>Saya tidak akan bilang “S2 luar negeri akan mengubah hidupmu”.</strong> "
                   "Datanya tidak mendukung itu: BPS meletakkan S1 dan S2 di golongan upah yang "
                   "sama, dan tidak satu pun dari tiga lowongan yang saya buka mensyaratkannya."),
    "<p>Saya juga tidak akan bilang “S2 itu sia-sia” — karena satu filter STEM itu nyata, "
    "kesempatan menetap di luar negeri itu nyata, dan jalur riset memang mensyaratkannya. "
    "<strong>Yang saya tolak adalah menjawab pertanyaanmu dengan perasaan.</strong></p>")

langkah("Tulis keputusanmu, dan beri tanggal",
    blok("aksi", "Buat berkas <code>keputusan-s2.md</code>, salin kerangka ini, isi semuanya.", "LAKUKAN"),
    kode("""KEPUTUSAN S2 - tanggal: ____________
Skor rubrik saya (dari 11)      : ____
Usia saya per 31 Des tahun ini  : ____
IELTS                           : belum / dijadwalkan ____ / skor ____"""),
    "<p>Lalu tiga baris keputusan beasiswanya:</p>",
    kode("""Chevening        : lamar / lewatkan  - alasan: __________
LPDP Tahap 1     : lamar / lewatkan  - alasan: __________
Australia Awards : lamar / lewatkan  - alasan: __________"""),
    "<p>Lalu empat kampus, disalin dari <code>kampus.md</code> Hari 4:</p>",
    kode("""1. ____________  matematika: ____  GMAT/GRE: ____  IELTS: ____
2. ____________  matematika: ____  GMAT/GRE: ____  IELTS: ____
3. ____________  matematika: ____  GMAT/GRE: ____  IELTS: ____
4. ____________  matematika: ____  GMAT/GRE: ____  IELTS: ____"""),
    "<p>Dan dua baris terakhir — yang paling penting:</p>",
    kode("""Kalau semua beasiswa gagal, saya akan: ______________________
Lamaran audit-analytics yang saya kirim  : ____
Ditolak eksplisit karena pendidikan      : ____"""),
    blok("aksi", "Lalu periksa tidak ada yang kosong.", "LAKUKAN"),
    kode('grep -n "____" keputusan-s2.md'),
    blok("hasil", "<p>Tidak ada satu baris pun keluaran.</p>", "HARUS MUNCUL"))

langkah("Pasang satu pengingat untuk membukanya lagi",
    blok("aksi", "Pasang pengingat di kalender: buka <code>keputusan-s2.md</code> pada hari fase 5 "
                 "selesai — tanggalnya sudah dihitung skrip di Hari 6.", "LAKUKAN"),
    blok("catatan", "<strong>Dua baris terakhir kerangka itu inti seluruh modul ini.</strong> Kamu "
                    "sedang mempertimbangkan mengeluarkan lebih dari satu miliar rupiah untuk "
                    "memperbaiki masalah yang belum kamu ukur."),
    "<p>Ukur dulu. <strong>Dua puluh lamaran memakan waktu satu bulan dan tidak berbiaya.</strong> "
    "Kalau tidak satu pun menolakmu karena pendidikan, kamu baru saja menghemat Rp 1,4 miliar dan "
    "dua tahun hidupmu.</p>")

HARI7 = {
  "n": "HARI 7",
  "tab": "7",
  "judul": "Keputusannya, dan rubrik yang kamu jalankan sendiri",
  "waktu": "± 2 jam",
  "tujuan": "menutup enam hari angka menjadi satu keputusan bertanggal yang bisa kamu pertahankan "
            "di depan siapa pun — termasuk di depan dirimu sendiri lima tahun lagi.",
  "langkah": L,
  "tutup_judul": "Jalur S2 Luar Negeri selesai",
  "tutup": "<p>Modul ini tidak menambah satu pun kemampuan teknis. Yang ditambahkannya: "
           "<strong>cara mengambil keputusan mahal dengan cara yang sama seperti kamu mengaudit</strong> "
           "— kumpulkan bukti, sebut sumbernya, hitung sendiri, dan jangan percaya angka yang "
           "tidak bisa kamu telusuri.</p>"
           "<p style=\"margin-top:10px\">Satu hal yang layak kamu bawa dari tujuh hari ini: "
           "<strong>keputusan ini tidak bergantung pada seberapa pintar kamu, tapi pada apakah ada "
           "yang membiayainya.</strong> Dengan beasiswa, syarat impasnya Rp 2,8 juta per bulan. "
           "Tanpa beasiswa, Rp 26,2 juta. Orangnya sama, gelarnya sama, kuliahnya sama. Yang "
           "berbeda cuma siapa yang membayar.</p>"
           "<p style=\"margin-top:10px\"><strong>Empat skrip yang kamu punya sekarang</strong> — "
           "<code>hitung_s2.py</code>, <code>hitung_tenggat.py</code>, <code>pindai_topik.py</code>, "
           "dan <code>skor_rubrik.py</code> — jangan dihapus. Jalankan lagi tiap kali kurs berubah, "
           "tenggat bergeser, atau keadaanmu berubah. Modul ini basi; skripnya tidak.</p>",
}
