# -*- coding: utf-8 -*-
"""Hari 6 — kalender, dan bentrokan yang ditemukan skrip."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Jalankan skrip yang sama, dengan tanggal mulai belajarmu",
    blok("aksi", "Beri satu argumen: tanggal kamu mulai (atau sudah mulai) mengerjakan kurikulum.", "LAKUKAN"),
    kode("python hitung_tenggat.py 2026-09-07"),
    blok("hasil", kode("""KAPAN FASE SELESAI
  Fase 1-5 (teknis)     217 hari materi = 22 minggu -> 2027-02-08
  Fase 1-6              254 hari materi = 26 minggu -> 2027-03-08
  Fase 1-7 (penuh)      282 hari materi = 29 minggu -> 2027-03-29""", salin=False),
         "HARUS MUNCUL"),
    "<p>Angka <code>217</code>, <code>254</code>, dan <code>282</code> bukan ketikan — itu jumlah "
    "hari materi tiap fase, dijumlahkan dari daftar modulmu.</p>")

langkah("Pahami ritme yang dipakai perhitungan itu",
    blok("aksi", "Buka <code>hitung_tenggat.py</code> dan cari baris <code>PER_MINGGU</code>.", "LAKUKAN"),
    kode("PER_MINGGU = 10   # 2 hari materi per hari kerja, 5 hari seminggu"),
    "<p>Itu ritme yang dipakai seluruh rute: <strong>dua “hari materi” per satu hari kerja, lima "
    "hari seminggu.</strong> Bukan tiga — modul-modul ini punya ulangan berjarak bawaan, dan "
    "memampatkannya membuat jaraknya ikut memampat.</p>",
    blok("catatan", "<strong>Kalau ritmemu berbeda, ganti angkanya.</strong> Belajar akhir pekan "
                    "juga? <code>PER_MINGGU = 14</code>. Cuma sanggup satu hari materi per hari? "
                    "<code>PER_MINGGU = 5</code>, dan seluruh kalendermu mundur dua kali lipat — "
                    "lebih baik tahu sekarang."))

langkah("Baca tabel “muat atau tidak”",
    blok("aksi", "Lihat bagian paling bawah keluarannya.", "LAKUKAN"),
    blok("hasil", kode("""MUAT ATAU TIDAK
  (Chevening tidak masuk tabel ini: ia tidak menunggu portofoliomu selesai)
  berhenti di              LPDP Tahap 1 2027  Australia Awards 202
  Fase 1-5 (teknis)         muat, sisa 15 hr      muat, sisa 81 hr
  Fase 1-6                   TERLAMBAT 13 hr      muat, sisa 53 hr
  Fase 1-7 (penuh)           TERLAMBAT 34 hr      muat, sisa 32 hr""", salin=False),
         "HARUS MUNCUL"),
    blok("bahaya", "<strong>Inilah bentrokan yang ditemukan skrip ini.</strong> Kalau kamu "
                   "menunggu seluruh rute selesai sebelum mendaftar LPDP, kamu <strong>terlambat "
                   "34 hari</strong>. Kalau berhenti setelah fase 5, kamu <strong>muat dengan "
                   "sisa 15 hari</strong>."))

langkah("Ambil aturannya",
    blok("aksi", "Tulis satu kalimat ini di catatanmu.", "LAKUKAN"),
    blok("hasil", "<p><strong>Kirim berkas LPDP setelah fase 5, bukan setelah seluruh rute.</strong></p>",
         "ATURAN YANG BERLAKU"),
    "<p>Di titik itu portofolio teknismu sudah lengkap: SQL Mahir L1–L5, SQL &amp; Python Produksi, "
    "migas, studi kasus. <strong>Fase 6 dan 7 menambah kemampuan, bukan menambah bukti yang "
    "dibutuhkan panitia.</strong></p>",
    blok("catatan", "<strong>Australia Awards muat di ketiga skenario</strong>, jadi ia bukan yang "
                    "membatasi. Yang membatasi hanya LPDP — dan hanya karena tenggatnya jatuh di "
                    "Februari."))

langkah("Uji sendiri: apa yang terjadi kalau kamu mulai terlambat sebulan",
    blok("aksi", "Jalankan lagi dengan tanggal mulai satu bulan lebih lambat.", "LAKUKAN"),
    kode("python hitung_tenggat.py 2026-10-07"),
    blok("hasil", kode("""  Fase 1-5 (teknis)         TERLAMBAT 15 hr      muat, sisa 51 hr""", salin=False),
         "HARUS MUNCUL (baris fase 1-5)"),
    blok("bahaya", "<strong>Menunda mulai satu bulan menghapus jalur LPDP siklus ini seluruhnya.</strong> "
                   "Bukan karena kamu kurang mampu, tapi karena aritmetika. Ini alasan paling "
                   "konkret untuk mulai minggu ini, dan kamu baru saja membuktikannya sendiri."),
    "<p>Australia Awards masih muat dengan sisa 51 hari — jadi menunda sebulan berarti "
    "<strong>kehilangan satu dari tiga lemparan</strong>, bukan semuanya.</p>")

langkah("Susun kalender lengkapmu",
    blok("aksi", "Salin kerangka ini ke catatanmu dan isi tanggalnya dari keluaran skripmu "
                 "sendiri, bukan dari tabel saya.", "LAKUKAN"),
    tabel(["Kapan", "Yang dikerjakan", "Kenapa saat itu"],
          [["<strong>Minggu ini</strong>", "pesan jadwal IELTS · mulai empat esai Chevening", "kursi IELTS penuh 3–6 minggu di muka"],
           ["<strong>sampai tenggat Chevening</strong>", "selesaikan lamaran: 3 pilihan program UK + 4 esai", "jangan kirim di hari terakhir"],
           ["<strong>sampai fase 5 selesai</strong>", "jalankan fase 1–5", "di titik ini portofoliomu cukup untuk melamar beasiswa"],
           ["<strong>2–3 bulan sebelum LPDP</strong>", "ambil IELTS · GMAT/GRE kalau mengincar LSE", "sertifikatnya harus sudah di tangan saat mendaftar"],
           ["<strong>jendela LPDP</strong>", "daftar LPDP Tahap 1", "setelah fase 5, bukan setelah seluruh rute"],
           ["<strong>setelah berkas terkirim</strong>", "jalankan fase 6 lalu fase 7", "tidak menghalangi apa pun lagi"],
           ["<strong>jendela AAS</strong>", "daftar Australia Awards", "muat di skenario mana pun"],
           ["<strong>sepanjang itu</strong>", "melamar kerja secara paralel", "tidak ada beasiswa yang pasti"]]))

langkah("Pahami kenapa dua jalur ini tidak saling memakan",
    blok("aksi", "Baca diagram ini, lalu jawab: apa isi lamaran beasiswamu?", "LAKUKAN"),
    """        <div class="diagram">
          <div class="kotak"><strong>SEKARANG</strong>58 modul</div>
          <span class="panah">→</span>
          <div class="kotak"><strong>SELESAI FASE 5</strong>portofolio teknis lengkap</div>
          <span class="panah">→</span>
          <div class="kotak"><strong>SELEKSI</strong>bahan esai &amp; wawancara</div>
        </div>""",
    blok("hasil", "<p>Setiap panitia beasiswa menanyakan hal yang sama: <em>kenapa bidang ini, dan "
                  "apa buktinya kamu serius?</em> Pelamar biasa menjawab dengan niat. Kamu bisa "
                  "menjawab dengan <strong>tiga proyek klien yang dikerjakan tanpa kunci jawaban, "
                  "satu nilai ujian berwaktu yang objektif, dan portofolio yang bisa dibuka</strong>.</p>",
         "JAWABANNYA"),
    "<p><strong>Rute itu bukan penunda lamaran beasiswamu — itu isi lamarannya.</strong></p>",
    blok("catatan", "<strong>Dan kalau semua beasiswa gagal</strong>, di titik yang sama kamu tetap "
                    "punya kemampuan kerja yang lengkap, tanpa kehilangan satu rupiah pun. Itu "
                    "properti yang tidak dimiliki rencana mana pun yang bertumpu pada "
                    "diterima-tidaknya kamu di suatu tempat."))

langkah("Lihat empat modul yang menutup lubang matematikanya",
    blok("aksi", "Buka satu di antaranya sebentar, lalu tutup lagi. Kamu cuma perlu tahu "
                 "bentuknya sekarang.", "LAKUKAN"),
    tabel(["Modul", "Menutup mata kuliah wajib", "Hari"],
          [['<a href="https://claude.ai/code/artifact/f6784136-a13e-47e9-9eae-0264bd514182"><strong>MAT L1 — Probabilitas formal</strong></a>',
            "DATASCI W203 (Berkeley) · ISYE 6739 (Georgia Tech)", "7"],
           ['<a href="https://claude.ai/code/artifact/f5079d99-9181-47a2-9ce4-7747feca52a3"><strong>MAT L2 — Aljabar linear</strong></a>',
            "MAST90138 <em>Multivariate Statistics</em> (Melbourne)", "7"],
           ['<a href="https://claude.ai/code/artifact/6dc7de48-3ed0-4126-8455-a2c82e7bad4c"><strong>MAT L3 — Optimisasi</strong></a>',
            "DSA5103 <em>Optimization Algorithms</em> (NUS)", "7"],
           ['<a href="https://claude.ai/code/artifact/bf6f3e02-66dc-40a4-a649-f1c260029d36"><strong>MAT L4 — Deep learning</strong></a>',
            "DSA5106 (NUS) · COMP90051 (Melbourne)", "7"]],
          kelas_n=(2,)),
    "<p>Keempatnya dibuat <em>setelah</em> pindaian Hari 2 menemukan lubangnya — 28 hari materi "
    "yang seluruhnya lahir dari satu skrip yang menghitung, bukan dari dugaan.</p>")

langkah("Putuskan kapan mengerjakan MAT L1–L4",
    blok("aksi", "Pilih satu baris yang menggambarkan tujuanmu.", "LAKUKAN"),
    tabel(["Tujuanmu", "Kapan mengerjakan MAT L1–L4"],
          [["Kerja di analitik audit / risiko di Indonesia",
            "<strong>Jangan sekarang.</strong> Tidak satu pun lowongan di Hari 1 menyebutnya. Waktumu lebih berharga di Pintu B dan Proyek Buta."],
           ["Melamar S2 ke kampus yang mensyaratkan matematika",
            "<strong>Kerjakan, <em>dan</em> ambil kredit resmi.</strong> Empat modul itu membuatmu mampu mengikuti; yang memenuhi syarat administratif tetap mata kuliah bertranskrip."],
           ["Melamar LSE / Bristol / OMSA",
            "<strong>Kerjakan setelah diterima, bukan sebelum melamar.</strong> Ketiganya menerimamu apa adanya. Empat modul itu jadi persiapan 28 hari sebelum kuliah dimulai."]]),
    blok("bahaya", "<strong>Jebakan urutan.</strong> Godaan terbesarnya adalah menghabiskan enam "
                   "bulan menutup lubang matematika “supaya siap”, lalu mendapati kampus tujuanmu "
                   "tidak pernah memintanya — sementara tenggat Chevening sudah lewat. "
                   "<strong>Matematika tidak punya tenggat; beasiswa punya.</strong> Fase 7 "
                   "diletakkan setelah modul ini justru karena itu."))

HARI6 = {
  "n": "HARI 6",
  "tab": "6",
  "judul": "Kalender yang dihitung skrip — dan satu bentrokan yang ketahuan sebelum terjadi",
  "waktu": "± 2 jam",
  "tujuan": "menaruh semua tenggat dan seluruh kurikulummu ke dalam satu kalender yang dihitung, "
            "lalu memeriksa apakah semuanya benar-benar muat. Satu di antaranya ternyata tidak.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> kirim LPDP setelah fase 5 · menunda mulai "
           "sebulan menghapus jalur LPDP siklus ini · Australia Awards muat di skenario mana pun · "
           "matematika tidak punya tenggat, beasiswa punya.</p>"
           "<p style=\"margin-top:8px\">Besok hari terakhir: keputusannya, dan rubrik supaya kamu "
           "bisa mengambilnya sendiri tanpa bertanya kepada saya.</p>",
}
