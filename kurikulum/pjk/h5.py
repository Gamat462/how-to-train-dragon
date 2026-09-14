# -*- coding: utf-8 -*-
"""Hari 5 — yang belum kamu punya, dan cara bicara soal itu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Kejujuran dulu: apa yang genuinely belum ada",
    blok("aksi", "Baca sekali. Tidak ada yang perlu ditutupi.", "LAKUKAN"),
    blok("hasil", "<p>Tiga hal: <strong>Polars</strong> (bahasa berbeda, bukan skill baru) · "
                  "<strong>Docker/Kubernetes/Airflow/Azure</strong> (infrastruktur, belum "
                  "disentuh sama sekali di rute ini) · <strong>LLM API/agentic workflow</strong> "
                  "(nama baru, tapi bukan pengalaman baru — tunggu langkah 6).</p>",
         "TIGA CELAH SUNGGUHAN"),
    "<p>Ketiganya berlabel <strong>\"advantageous\"</strong> di lowongan, bukan wajib. Lowongan "
    "ini sendiri bilang: <em>\"You do not need to arrive as a Tax or AI specialist.\"</em></p>")

langkah("Polars: sintaksnya beda, gagasannya sama",
    blok("aksi", "Bandingkan dua cara menghitung rata-rata penghasilan per jenis wajib pajak.",
         "LAKUKAN"),
    kode('# pandas (yang sudah kamu kuasai dari M3)\n'
         'df.groupby("jenis")["penghasilan_tahunan"].mean()\n\n'
         '# polars\n'
         'pf.group_by("jenis").agg(pl.col("penghasilan_tahunan").mean())'),
    blok("hasil", "<p>Keduanya menghasilkan angka yang sama: perorangan Rp 2.011.250.000, "
                  "umkm Rp 513.333.333.</p>", "SUDAH DIVERIFIKASI"),
    "<p><code>groupby</code> jadi <code>group_by</code>, <code>[\"kolom\"]</code> jadi "
    "<code>pl.col(\"kolom\")</code>. Kamu sudah tahu <strong>gagasan</strong> "
    "(kelompokkan, lalu hitung) — Polars cuma menaruh gagasan yang sama dalam sintaks "
    "berbeda, dan lebih cepat untuk data besar karena ditulis di Rust.</p>",
    blok("catatan", "<strong>Jangan panik kalau syntax-nya asing waktu wawancara.</strong> "
                    "Jawaban yang jujur dan kuat: \"Saya belum pakai Polars, tapi API-nya mirip "
                    "pandas dan saya terbiasa pindah antar-library data — SQL ke pandas sudah "
                    "saya lakukan berkali-kali.\""))

langkah("Docker, Kubernetes, Airflow, Azure — secukupnya untuk tidak buta istilah",
    blok("aksi", "Salin tabel ini. Ini bukan untuk dikuasai — untuk <strong>tidak diam</strong> "
                 "kalau disebut di wawancara.", "LAKUKAN"),
    tabel(["Istilah", "Satu kalimat artinya"],
          [["Docker", "Membungkus kode + semua yang dibutuhkannya jadi satu paket yang "
            "jalan sama persis di komputer siapa pun"],
           ["Kubernetes", "Mengatur banyak paket Docker itu berjalan otomatis, termasuk "
            "menghidupkan ulang yang mati"],
           ["Airflow", "Penjadwal — menjalankan urutan tugas data (\"jam 2 pagi, ambil data, "
            "lalu hitung, lalu kirim\") dan memberitahu kalau ada yang gagal"],
           ["Azure", "Layanan komputer dan penyimpanan yang disewa, bukan dibeli — tempat "
            "Docker/Kubernetes/Airflow tadi biasanya dijalankan"]]),
    "<p>Empat kalimat ini cukup untuk mengikuti percakapan, mengajukan pertanyaan yang masuk "
    "akal, dan jujur bilang \"saya belum pernah pakai tangan sendiri\" tanpa terdengar "
    "buta.</p>")

langkah("Yang keempat: kamu sudah membangunnya, cuma belum menyadarinya",
    blok("aksi", "Baca pelan-pelan. Ini bagian paling penting hari ini.", "LAKUKAN"),
    blok("hasil", "<p>Lowongan minta <em>\"AI-assisted engineering tools\"</em> dan "
                  "<em>\"evaluation harnesses\"</em>. Seluruh rute belajar yang sedang kamu "
                  "jalani — termasuk lima hari modul ini — dibangun memakai <strong>Claude "
                  "Code, dengan skrip yang menjalankan tiap query ke basis data sungguhan, "
                  "menyimpan hasilnya, lalu mengukur apakah tulisannya memenuhi standar "
                  "sebelum diterbitkan.</strong></p>", "TEMUAN"),
    "<p>Itu bukan analogi longgar. <code>mat/_sql.py</code> yang menjalankan query dan "
    "menangkap hasil/error-nya adalah <strong>alat</strong>. <code>hasil.json</code> yang "
    "menyimpan tiap keluaran terverifikasi adalah <strong>golden dataset</strong>. "
    "<code>ukur.py</code> yang mencetak seberapa jauh sebuah modul dari standar adalah "
    "<strong>evaluation harness</strong> — persis kata yang dipakai lowongan.</p>")

langkah("Kalimat wawancara untuk temuan ini",
    blok("aksi", "Baca sekali, ucapkan dengan suara.", "LAKUKAN"),
    blok("hasil", "<p>\"Saya sudah punya pengalaman bekerja dengan tooling berbasis AI — "
                  "saya membangun kurikulum belajar saya sendiri memakai Claude Code, dengan "
                  "pipeline yang menjalankan tiap contoh kode ke basis data sungguhan, "
                  "menyimpan hasilnya sebagai golden dataset, dan skrip pengukur otomatis "
                  "yang memvalidasi konten sebelum diterbitkan. Itu bukan proyek besar, tapi "
                  "itu evaluation harness sungguhan yang saya rancang dan pakai sendiri.\"</p>",
         "KALIMAT WAWANCARA"),
    blok("catatan", "Ini <strong>satu-satunya</strong> jawaban di modul ini yang tidak bisa "
                    "ditiru pelamar lain dengan cara yang sama. Kebanyakan orang belajar "
                    "\"pakai AI\" berarti menyalin jawaban ChatGPT. Kamu membangun sistem yang "
                    "memverifikasi jawabannya sendiri."))

langkah("Susun CV-mu: empat draf jadi satu bagian pengalaman",
    blok("aksi", "Salin susunan ini ke CV-mu, di bawah bagian proyek/portofolio.", "LAKUKAN"),
    blok("hasil", "<p><strong>Proyek: Simulasi Aturan Perpajakan Bertingkat (Python, SQL, "
                  "PostgreSQL)</strong></p>"
                  "<ul style=\"margin:8px 0 0;padding-left:20px;font-size:0.93rem\">"
                  "<li>Merancang skema aturan pajak berjenjang dan tarif final dengan logika "
                  "precedence tiga-tingkat (klasifikasi → syarat batas → aturan default)</li>"
                  "<li>Menemukan dan memperbaiki kesalahan kalkulasi yang menyebabkan selisih "
                  "43% dan 9,3x dari pendekatan naif, dibuktikan lewat query SQL</li>"
                  "<li>Membangun suite regresi (pytest) dengan golden dataset terverifikasi, "
                  "divalidasi dengan menyuntik kesalahan yang disengaja</li>"
                  "<li>Menguji dan menangani kesalahan data ERP umum (duplikasi kunci, format "
                  "angka lokal) di PostgreSQL</li></ul>",
         "CV — BAGIAN PROYEK"),
    "<p>Empat baris, empat angka atau bukti konkret, nol klaim kosong. Ini yang membedakan CV "
    "yang bertahan waktu ditanya lebih dalam dari CV yang cuma daftar kata kunci.</p>")

langkah("Lima pertanyaan yang kemungkinan besar ditanyakan, dan jawabanmu",
    blok("aksi", "Baca semuanya sekali, lalu latihan menjawab dengan suara — bukan dalam "
                 "hati.", "LAKUKAN"),
    tabel(["Kemungkinan pertanyaan", "Jawabanmu, singkat"],
          [["\"Ceritakan pengalamanmu dengan aturan bisnis yang kompleks.\"",
            "Kisah UMKM: label bisa basi, aturan khusus menang <em>dengan syarat</em>, "
            "selisihnya 9,3x kalau diabaikan"],
           ["\"Bagaimana kamu memastikan kode-mu benar sebelum dikirim?\"",
            "Golden dataset + pytest, dan kamu <em>membuktikan</em> tesnya bisa gagal dengan "
            "sengaja merusaknya"],
           ["\"Kamu belum punya pengalaman Tax — kenapa kami harus mempertimbangkanmu?\"",
            "Kamu <em>punya</em> — dari KAP, di sisi audit. Sekarang kamu bisa menulis "
            "temuan itu sebagai kode yang bisa diuji ulang, bukan cuma sampling manual"],
           ["\"Ceritakan soal pengalaman AI-mu.\"",
            "Kurikulum ini sendiri: pipeline verifikasi otomatis, golden dataset, evaluation "
            "harness — dibangun dan dipakai sendiri"],
           ["\"Bagaimana kalau kami butuh Docker/Airflow?\"",
            "Jujur: belum pernah pakai tangan sendiri, tapi paham konsepnya dan terbiasa "
            "belajar tool baru — bukti: SQLite ke PostgreSQL, minggu lalu"]]),
    blok("bahaya", "<strong>Jangan menghafal kalimat ini kata per kata.</strong> Kalau "
                   "terdengar seperti dibaca dari kertas, itu justru mengurangi kepercayaan. "
                   "Pahami intinya, lalu ucapkan dengan kata-katamu sendiri."))

langkah("Sebelum melamar: jalankan sekali lagi seluruh lima hari ini",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    "<p>Buka kembali <code>senja/pjk-hari-2.sql</code> sampai <code>pjk-hari-4.sql</code>, "
    "jalankan ulang semuanya dari awal sampai akhir tanpa membuka kunci jawaban. Kalau kamu "
    "bisa menjalankannya lancar dan menjelaskan tiap angka <strong>tanpa membaca "
    "catatan</strong>, kamu siap.</p>",
    blok("catatan", "Ini persis latihan yang kamu lakukan sebelum ujian sertifikasi CPA/CA — "
                    "kamu sudah tahu cara belajar seperti ini bekerja. Bedanya sekarang "
                    "materinya SQL dan Python, bukan PSAK."))

langkah("Satu kalimat penutup, untuk ditulis tangan",
    blok("aksi", "Tulis di buku fisikmu, seperti biasa.", "LAKUKAN"),
    blok("hasil", "<p>Delapan dari sepuluh syarat wajib lowongan ini sudah tertutup sebelum "
                  "modul ini dimulai. Tiga celah yang tersisa bukan celah kemampuan — celah "
                  "kosakata. Dan satu hal yang kamu kira kelemahan (bukan spesialis pajak, "
                  "bukan spesialis AI) justru kalimat yang ditulis lowongan ini sendiri "
                  "sebagai syarat cukup.</p>", "TULIS INI"),
    "<p>Modul ini selesai. Lamarannya bukan pekerjaanmu selanjutnya — <strong>kirim "
    "lamarannya</strong> adalah.</p>")

HARI5 = {
  "n": "HARI 5", "tab": "5",
  "judul": "Yang belum kamu punya, dan cara bicara soal itu",
  "waktu": "± 45 menit",
  "tujuan": "mengenali tiga celah sungguhan tanpa melebih-lebihkannya, menemukan bahwa proses "
            "membangun kurikulum ini sendiri adalah pengalaman AI-assisted tooling, dan "
            "menyusun CV serta jawaban wawancara siap pakai untuk lowongan ini.",
  "langkah": L,
  "tutup_judul": "Bekal Pajak & ERP selesai",
  "tutup": "<p>Lima hari ini tidak mengajarkan SQL atau Python dari nol — semuanya sudah kamu "
           "kuasai. Yang dilakukannya adalah <strong>menerjemahkan</strong>: precedence dan "
           "exception jadi kaskade tarif pajak yang bisa salah 43% tanpa error, golden "
           "dataset jadi pytest yang kamu buktikan sendiri bisa gagal, dan pengalaman KAP-mu "
           "jadi kalimat yang persis dipakai lowongan Deloitte ini.</p>"
           "<p style=\"margin-top:8px\">Draf CV dan jawaban wawancara dari lima hari ini sudah "
           "siap disalin. Yang tersisa cuma satu langkah, dan tidak ada modul yang bisa "
           "mengerjakannya untukmu: <strong>tekan kirim.</strong></p>",
}
