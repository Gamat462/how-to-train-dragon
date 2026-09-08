# -*- coding: utf-8 -*-
"""Hari 95 — CV. Semua keluaran periksa_cv.py diperoleh dengan menjalankannya
sungguhan pada dua CV contoh yang ikut di paket zip."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Lihat CV-mu seperti mesin melihatnya",
    blok("aksi", "Buka PDF CV-mu yang sekarang. Tekan <kbd>Ctrl</kbd>+<kbd>A</kbd> lalu "
                 "<kbd>Ctrl</kbd>+<kbd>C</kbd>. Tempel ke berkas teks kosong, simpan sebagai "
                 "<code>cv.txt</code>.", "LAKUKAN"),
    blok("hasil", "<p>Kalau hasil tempelannya rapi dan urut atas-ke-bawah: bagus. Kalau kalimatnya "
                  "tercampur acak, kolomnya tertukar, atau sebagian tidak ikut sama sekali — "
                  "itu bukan kesalahan salin.</p>", "YANG HARUS TERLIHAT"),
    blok("bahaya", "<strong>Itulah persis yang dibaca sistem penyaring otomatis (ATS).</strong> "
                   "Sebagian besar lamaran di Singapura dan Australia lewat sistem itu sebelum "
                   "dilihat manusia, dan sistem itu membaca teks, bukan tata letak. Teks di dalam "
                   "gambar tidak terbaca sama sekali."),
    "<p>Belum punya CV? Buat <code>cv.txt</code> kosong — hari ini kamu menulisnya dari nol.</p>")

langkah("Ambil pemeriksanya, lalu ukur CV yang buruk",
    blok("aksi", "Salin <code>data-dan-skrip/minggu-14/periksa_cv.py</code> dan "
                 "<code>cv-lemah.txt</code> dari paket zip. Jalankan pada yang lemah dulu.", "LAKUKAN"),
    kode("python periksa_cv.py cv-lemah.txt"),
    blok("hasil", kode("""[OK ] panjang            33 kata (batas wajar satu halaman: 700)
[CEK] bagian baku        tidak ada: experience, education
[CEK] email              kontak email
[CEK] linkedin           tautan LinkedIn
[CEK] github             tautan GitHub
[CEK] poin berangka      0 dari 3 poin memuat angka (target 60%)
[CEK] tanpa kata lemah   ditemukan: responsible for, helped with, worked on

lolos 1 dari 7 pemeriksaan""", salin=False), "HARUS MUNCUL"),
    "<p>Isi <code>cv-lemah.txt</code> cuma sepuluh baris, dan tujuh pemeriksaan menemukan enam "
    "masalah. Buka berkasnya dan baca — kamu akan mengenali bentuknya.</p>")

langkah("Aturan format yang tidak bisa ditawar",
    blok("aksi", "Baca tabel ini sekali, lalu buka CV-mu dan perbaiki yang melanggar.", "LAKUKAN"),
    tabel(["Lakukan", "Hindari", "Alasan"],
          [["Satu kolom, atas ke bawah", "Dua kolom, sidebar", "ATS sering membaca kolom acak, kalimat tercampur"],
           ["Judul baku: Experience, Education, Skills", "Judul kreatif \"My Journey\"", "ATS mencari kata kunci baku"],
           ["Kirim sebagai PDF berbasis teks", "Gambar, ikon, tabel rumit", "teks di dalam gambar tidak terbaca sama sekali"],
           ["Satu halaman", "Dua halaman (untuk &lt;5 tahun pengalaman)", "perekrut memindai 7 detik"],
           ["Salin kata dari iklan lowongan", "Sinonim kreatif", "\"Power BI\" bukan \"Microsoft BI tools\""]]),
    blok("catatan", "<strong>Kenapa pemeriksa tadi menolak \"My Journey\":</strong> ia mencari kata "
                    "<code>experience</code>, <code>education</code>, dan <code>skills</code> di "
                    "mana pun di CV-mu. Sistem ATS sungguhan melakukan hal yang sama, cuma lebih "
                    "banyak variasinya."))

langkah("Rumus tiga bagian untuk tiap poin",
    blok("aksi", "Ambil satu poin di CV-mu yang paling lemah. Tulis ulang dengan rumus: "
                 "<strong>tindakan + cara + hasil berangka</strong>.", "LAKUKAN"),
    tabel(["Lemah", "Kuat"],
          [["Responsible for creating dashboards and reports using Tableau",
            "Built an automated Tableau dashboard replacing 6 hours of manual weekly reporting, now used by 12 people across 3 teams"],
           ["Worked on data cleaning for the finance team",
            "Reconciled general ledgers of up to 2 million rows against trial balances, cutting fieldwork on 3 recurring engagements by 40%"]]),
    "<p>Bagian ketiga — <strong>hasil berangka</strong> — yang paling sering hilang, dan justru "
    "itu satu-satunya bagian yang bisa dipercaya. Dua yang pertama bisa ditulis siapa saja.</p>",
    blok("catatan", "<strong>Angkanya tidak harus mengesankan, cuma harus benar.</strong> "
                    "\"Digunakan 12 orang di 3 tim\" lebih kuat daripada \"meningkatkan efisiensi "
                    "secara signifikan\", meski 12 bukan angka besar."))

langkah("Susunan CV untuk pelamar pindah karier",
    blok("aksi", "Buat kerangka <code>cv.txt</code>-mu dengan urutan ini. Perhatikan posisi "
                 "<em>Projects</em>.", "LAKUKAN"),
    kode("""NAMA LENGKAP
Kota, Negara · email · telepon · linkedin.com/in/... · github.com/...

SUMMARY
SKILLS
PROJECTS
EXPERIENCE
EDUCATION"""),
    blok("bahaya", "<strong>PROJECTS di atas EXPERIENCE</strong> — itu yang membedakan CV pindah "
                   "karier dari CV biasa. Kalau pengalaman kerjamu belum di bidang data, "
                   "menaruhnya lebih dulu berarti tujuh detik pertama perekrut habis membaca "
                   "hal yang tidak relevan."),
    blok("catatan", "<strong>Pengalaman lamamu tetap ditulis, tapi ditulis ulang.</strong> Sebagai "
                    "mantan auditor, \"rekonsiliasi buku besar dua juta baris\" adalah pekerjaan "
                    "data — tulis begitu, jangan tulis \"melaksanakan prosedur audit\"."))

langkah("Isi bagian Projects dengan capstone-mu",
    blok("aksi", "Tulis tiga proyek. Judulnya sama dengan judul README-mu kemarin — temuan "
                 "berangka, bukan nama dataset.", "LAKUKAN"),
    kode("""PROJECTS
Location explains 61% of HDB resale price variance - dashboard | repo
- Built a dbt pipeline over 240,000 Singapore HDB transactions from 2017-2024
- Found that distance to MRT explains 61% of price variance, down from 74% before 2020
- Scheduled daily with GitHub Actions; 12 dbt tests including a reconciliation test"""),
    "<p>Tiga poin, tiga fungsi: <strong>apa yang dibangun</strong> (dan sebesar apa), "
    "<strong>apa yang ditemukan</strong> (berangka), <strong>bagaimana dijalankan</strong> "
    "(yang membuktikan ini bukan notebook sekali jalan).</p>")

langkah("Jalankan pemeriksanya pada CV-mu",
    blok("aksi", "Salin ulang seluruh teks CV barumu ke <code>cv.txt</code>, lalu jalankan.", "LAKUKAN"),
    kode("python periksa_cv.py cv.txt"),
    blok("hasil", kode("""[OK ] panjang            220 kata (batas wajar satu halaman: 700)
[OK ] bagian baku        lengkap
[OK ] email              kontak email
[OK ] linkedin           tautan LinkedIn
[OK ] github             tautan GitHub
[OK ] poin berangka      9 dari 9 poin memuat angka (target 60%)
[OK ] tanpa kata lemah   bersih

lolos 7 dari 7 pemeriksaan""", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Angka \"220 kata\" dan \"9 poin\" akan beda di CV-mu</strong> — itu "
                    "isi CV-mu sendiri. Yang harus sama: semua baris bertanda <code>[OK ]</code>, "
                    "dan baris terakhir menyebut lolos semua. Contoh di atas keluaran dari "
                    "<code>cv-kuat.txt</code> yang ikut di paket zip; buka dan bandingkan dengan "
                    "punyamu."))

langkah("Uji terhadap iklan lowongan sungguhan",
    blok("aksi", "Buka satu iklan lowongan analis di Singapura atau Australia. Salin bagian "
                 "<em>Requirements</em>-nya ke <code>iklan.txt</code>. Lalu jalankan dengan dua "
                 "argumen.", "LAKUKAN"),
    kode("python periksa_cv.py cv.txt iklan.txt"),
    blok("hasil", kode("""[OK ] kata kunci iklan   8 dari 11 kata kunci alat ada di CV | belum ada: etl, looker, warehouse

lolos 8 dari 8 pemeriksaan""", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Tiga kata yang \"belum ada\" itu bukan daftar belanja.</strong> "
                   "Tambahkan hanya yang benar-benar kamu kuasai. Menulis <em>Looker</em> di CV "
                   "karena skrip menyebutnya akan berbalik menyerangmu di menit kelima wawancara — "
                   "dan itu kegagalan yang jauh lebih mahal daripada tidak dipanggil."),
    "<p>Yang boleh langsung ditambahkan: kata yang <strong>sinonim</strong> dengan yang sudah kamu "
    "kuasai. Kalau kamu memakai BigQuery, kata <code>warehouse</code> memang layak ada di CV-mu — "
    "cuma belum tertulis.</p>")

langkah("Ulangi dengan sepuluh iklan",
    blok("aksi", "Kumpulkan sepuluh iklan lowongan, satukan jadi satu berkas, jalankan sekali.", "LAKUKAN"),
    kode("cat iklan-*.txt > semua-iklan.txt\npython periksa_cv.py cv.txt semua-iklan.txt"),
    "<p>Kata yang muncul di banyak iklan sekaligus adalah kata yang <strong>benar-benar dicari "
    "pasar</strong>, bukan yang kamu kira dicari. Kalau ada alat yang muncul terus dan kamu belum "
    "menguasainya, itu daftar belajarmu berikutnya — bukan daftar tulisanmu.</p>",
    blok("catatan", "<strong>Simpan berkas iklan-iklan itu.</strong> Minggu depan, di modul "
                    "wawancara, berkas yang sama dipakai untuk menyiapkan jawaban."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab empat pertanyaan ini dengan suara keras.", "LAKUKAN"),
    """<ol>
          <li>Kenapa CV dua kolom berbahaya, padahal kelihatannya lebih rapi?</li>
          <li>Apa tiga bagian rumus tiap poin, dan bagian mana yang paling sering hilang?</li>
          <li>Kenapa PROJECTS ditaruh di atas EXPERIENCE untuk pelamar pindah karier?</li>
          <li>Kapan kata kunci dari iklan <em>tidak</em> boleh ditambahkan ke CV?</li>
        </ol>""",
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>1.</strong> ATS membaca teksnya, bukan tata letaknya — kolom sering terbaca
            acak sehingga kalimatnya tercampur, dan sebagian bisa hilang sama sekali.</p>
            <p><strong>2.</strong> Tindakan + cara + hasil berangka. Yang paling sering hilang
            adalah hasil berangka, dan itu satu-satunya bagian yang bisa diverifikasi.</p>
            <p><strong>3.</strong> Karena tujuh detik pertama perekrut harus jatuh pada bukti
            kemampuan data, bukan pada pekerjaan lama yang belum relevan.</p>
            <p><strong>4.</strong> Kalau kamu tidak menguasainya. Kata kunci membuatmu lolos
            penyaring lalu gagal di wawancara — hasil akhir yang lebih buruk.</p>
          </div>
        </details>""")

HARI95 = {
  "n": "HARI 95",
  "tab": "95",
  "judul": "CV yang lolos mesin dan meyakinkan manusia — dan skrip yang mengukurnya",
  "waktu": "± 70 menit",
  "tujuan": "CV satu halaman berbahasa Inggris yang lolos delapan pemeriksaan terukur, termasuk "
            "kecocokan kata kunci dengan iklan lowongan sungguhan.",
  "langkah": L,
  "tutup_judul": "Hari 95 selesai.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> satu kolom · PDF berbasis teks · satu halaman · "
           "judul bagian baku · tindakan+cara+hasil berangka di tiap poin · PROJECTS di atas "
           "EXPERIENCE · kata kunci ditambahkan hanya kalau benar dikuasai.</p>"
           "<p style=\"margin-top:8px\">Jalankan <code>periksa_cv.py</code> lagi tiap kali kamu "
           "mengubah CV. Sepuluh detik, dan menangkap hal yang matamu sudah terlalu terbiasa "
           "untuk melihat.</p>",
}
