# -*- coding: utf-8 -*-
"""Hari 98 — latihan lisan, capstone, dan penutup Minggu 14."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Kosongkan query.sql, lalu kerjakan Soal 1 dari ingatan",
    blok("aksi", "Hapus seluruh isi <code>query.sql</code>. Tutup halaman Hari 97. Nyalakan "
                 "perekam suara di HP-mu. Kerjakan Soal 1 sambil mengucapkan tiap langkahnya.", "LAKUKAN"),
    kode('echo "" > query.sql'),
    blok("hasil", kode("""┌────────┐
│ hilang │
│ int64  │
├────────┤
│     24 │
└────────┘""", salin=False), "HARUS MUNCUL"),
    "<p>Angkanya harus <strong>24</strong>. Kalau beda, querymu beda — dan itu justru yang mau "
    "kamu temukan hari ini, bukan besok di depan pewawancara.</p>",
    blok("catatan", "<strong>Perekamnya bukan hiasan.</strong> Yang mau kamu dengar bukan "
                    "jawabannya, tapi berapa lama kamu diam. Diam panjang di tengah pengerjaan "
                    "adalah hal yang paling sering membuat kandidat kalah, dan kamu tidak bisa "
                    "menyadarinya tanpa mendengar rekamanmu sendiri."))

langkah("Kerjakan Soal 2, 3, dan 4 dari ingatan",
    blok("aksi", "Satu per satu, masih dengan suara keras. Catat soal mana yang butuh lebih dari "
                 "sepuluh menit.", "LAKUKAN"),
    tabel(["Soal", "Angka yang harus keluar", "Kalau salah, ulangi bagian"],
          [["2", "12 baris, 3 per kota", "ROW_NUMBER + PARTITION BY, saring di CTE kedua"],
           ["3", "retensi 28,0 / 42,3 / 13,0 / 39,1 / 47,8", "LEFT JOIN, bukan INNER"],
           ["4", "346 baris, 240 ada isinya, 106 NULL", "LAG menghasilkan NULL di baris pertama tiap partisi"]]),
    blok("catatan", "<strong>Kalau satu soal butuh lebih dari sepuluh menit, itu bukan soal yang "
                    "kamu kuasai</strong> — itu soal yang kamu ingat pernah lihat. Bedanya besar, "
                    "dan cuma ketahuan lewat latihan seperti ini."))

langkah("Dengarkan rekamanmu",
    blok("aksi", "Putar rekamannya. Hitung tiga hal sambil mendengar.", "LAKUKAN"),
    tabel(["Yang dihitung", "Target", "Kalau meleset"],
          [["berapa detik diam terpanjang", "di bawah 15 detik", "biasakan mengucapkan \"saya sedang memikirkan...\" alih-alih diam"],
           ["apakah kamu mengulang soalnya di awal", "selalu", "ini langkah yang paling murah dan paling sering dilewati"],
           ["apakah kamu menyebut satu kasus khusus", "minimal satu per soal", "NULL, nilai seri, atau pembagian nol"]]),
    "<p>Mendengar rekaman diri sendiri tidak enak. Itu justru tandanya berguna — kamu sedang "
    "mendengar apa yang didengar pewawancara.</p>")

langkah("Kerjakan sepuluh soal baru di luar",
    blok("aksi", "Buka StrataScratch atau DataLemur. Pilih sepuluh soal tingkat "
                 "<em>medium</em>. Untuk tiap soal, jalankan lima langkah Hari 97.", "LAKUKAN"),
    blok("catatan", "<strong>Sepuluh soal medium jauh lebih berguna daripada empat puluh soal "
                    "easy.</strong> Soal <em>easy</em> menguji apakah kamu hafal sintaks; soal "
                    "<em>medium</em> menguji apakah kamu bisa memecah masalah — dan itu yang "
                    "diuji di wawancara."),
    "<p>Catat pola mana yang masih terasa asing. Daftar itu — bukan jumlah soal yang selesai — "
    "yang jadi bahan review sebelum wawancara sungguhan.</p>")

langkah("Kembali ke capstone dan jalankan ketiga pemeriksa",
    blok("aksi", "Buka folder capstone-mu. Jalankan tiga hal yang sudah kamu punya.", "LAKUKAN"),
    kode('grep -n ":$" RENCANA.md\npython periksa_readme.py README.md\npython periksa_cv.py cv.txt'),
    blok("hasil", kode("""lolos 10 dari 10 pemeriksaan
lolos 7 dari 7 pemeriksaan""", salin=False), "HARUS MUNCUL"),
    "<p>Perintah pertama tidak boleh mengeluarkan apa pun. Dua berikutnya harus lolos penuh. "
    "Tiga perintah, dua puluh detik, dan kamu tahu persis di mana kamu berdiri.</p>")

langkah("Uji capstone-mu dari folder kosong",
    blok("aksi", "Ini pemeriksaan yang tidak bisa diwakili skrip. Clone repositorimu sendiri ke "
                 "folder baru dan jalankan dari nol.", "LAKUKAN"),
    kode("cd /tmp\ngit clone https://github.com/[username]/[repo].git uji-bersih\ncd uji-bersih\npip install -r requirements.txt"),
    blok("bahaya", "<strong>Kalau gagal di sini, portofoliomu gagal di tangan perekrut</strong> — "
                   "dan mereka tidak akan mengirim pesan bertanya. Dua penyebab yang hampir selalu "
                   "muncul: berkas yang lupa di-commit karena kena <code>.gitignore</code>, dan "
                   "pustaka yang terpasang di komputermu berbulan-bulan lalu tapi tidak ada di "
                   "<code>requirements.txt</code>."),
    "<p>Lalu buka tautan dashboard-mu dari HP dengan wifi dimatikan. Kalau tidak terbuka, ia "
    "sedang berjalan di komputermu, bukan di internet.</p>")

langkah("Periksa tidak ada kredensial di seluruh riwayat",
    blok("aksi", "Satu perintah, di dalam folder capstone-mu.", "LAKUKAN"),
    kode('git log -p --all | grep -iE "password|api_key|secret|BEGIN PRIVATE KEY"'),
    blok("hasil", "<p>Tidak ada satu baris pun keluaran.</p>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Kalau ada keluaran, kunci itu harus diganti hari ini juga</strong> — "
                   "bukan dihapus. Riwayat git menyimpan semua versi lama, dan repositori yang "
                   "pernah publik harus dianggap sudah terbaca. Ini pelajaran Minggu 11 Hari 72, "
                   "dan di sinilah ia diperiksa."))

langkah("Checklist Minggu 14",
    blok("aksi", "Centang satu per satu. Jangan mencentang yang belum kamu buktikan.", "LAKUKAN"),
    """<ol>
          <li>Capstone selesai, dashboard hidup, dibuka dari HP dengan wifi mati</li>
          <li>README lolos 10 dari 10, dan lolos uji 60 detik pada orang non-data</li>
          <li>4 repositori tersemat, tiap satu punya deskripsi berisi temuan</li>
          <li>README profil GitHub terisi, tiga proyek dengan temuannya</li>
          <li>CV lolos 8 dari 8, termasuk kecocokan kata kunci dengan iklan sungguhan</li>
          <li>LinkedIn: headline ≤220 karakter, About 3 paragraf, Featured terisi</li>
          <li>14 soal SQL dikerjakan (4 Hari 97 + 10 Hari 98), semuanya sambil bersuara</li>
          <li>Tidak ada kredensial di seluruh riwayat git capstone</li>
        </ol>""",
    blok("catatan", "<strong>Kalau ada satu yang belum tercentang, tulis tanggalnya.</strong> "
                    "Minggu depan adalah minggu terakhir dan isinya wawancara — bukan waktu yang "
                    "baik untuk menemukan bahwa dashboard-mu sudah mati."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup semuanya. Jawab dengan suara keras: sebutkan empat pola SQL Hari 97 "
                 "beserta jebakan masing-masing.", "LAKUKAN"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>Anti-join</strong> — LEFT JOIN + <code>IS NULL</code>. Jebakan:
            <code>NOT IN</code> dengan NULL di dalamnya memberi hasil kosong tanpa peringatan.</p>
            <p><strong>Peringkat per kelompok</strong> — <code>ROW_NUMBER() OVER (PARTITION BY
            ...)</code>. Jebakan: <code>WHERE rn &lt;= 3</code> tidak bisa di query yang sama,
            harus CTE kedua.</p>
            <p><strong>Retensi kohor</strong> — LEFT JOIN wajib. Jebakan: INNER JOIN membuat
            setiap kohor terlihat 100%.</p>
            <p><strong>Jeda antar kejadian</strong> — <code>LAG</code> dengan
            <code>PARTITION BY</code>. Jebakan: baris pertama tiap partisi selalu NULL.</p>
          </div>
        </details>""")

HARI98 = {
  "n": "HARI 98",
  "tab": "98",
  "judul": "Latihan lisan, dan menutup capstone dengan pemeriksaan",
  "waktu": "± 75 menit",
  "tujuan": "mengerjakan keempat soal SQL dari ingatan sambil bersuara, dan menutup capstone "
            "dengan pemeriksaan yang bisa dijalankan, bukan perasaan sudah selesai.",
  "langkah": L,
  "tutup_judul": "Empat belas minggu selesai — portofolio, CV, dan profil siap dipamerkan",
  "tutup": "<p>Capstone-mu, profil GitHub, CV, dan LinkedIn sekarang saling terhubung dan "
           "konsisten: judul yang sama, temuan yang sama, angka yang sama. Dan empat pola SQL "
           "yang paling sering diuji sudah kamu kerjakan pada data sungguhan, bukan kamu baca.</p>"
           "<p style=\"margin-top:10px\"><strong>Tiga skrip yang kamu punya sekarang</strong> — "
           "<code>periksa_readme.py</code>, <code>periksa_cv.py</code>, dan "
           "<code>jalankan.py</code> dengan basis data latihannya — jangan dihapus. Ketiganya "
           "dipakai lagi setiap kali kamu menyelesaikan proyek baru atau menyiapkan wawancara.</p>"
           "<p style=\"margin-top:10px\">Minggu depan, dan terakhir: wawancara studi kasus, "
           "wawancara perilaku, strategi melamar ke Singapura dan Australia, serta visa, gaji, "
           "dan negosiasi tawaran — sampai ke garis akhir dua belas bulan ini.</p>",
}
