# -*- coding: utf-8 -*-
"""Hari 72 — .gitignore, kredensial, dan lingkungan virtual.
Semua keluaran dijalankan sungguhan: git 2.43.0, Python 3.11.15, pandas 3.0.5."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buat dua hal yang tidak boleh masuk git",
    blok("aksi", "Masih di folder <code>latihan-git</code>. Buat satu berkas kata sandi dan satu "
                 "folder data besar, lalu tanya git.", "LAKUKAN"),
    kode('printf "DB_PASSWORD=rahasia123\\n" > .env\nmkdir data\nhead -c 300000 /dev/urandom > data/mentah.csv\ngit status -s'),
    blok("hasil", kode("""?? .env
?? data/""", salin=False), "HARUS MUNCUL"),
    "<p>Dua tanda tanya artinya git belum melacaknya, tapi <strong>siap</strong> melacaknya. "
    "Satu <code>git add .</code> yang terlalu cepat, dan kata sandi klienmu masuk ke internet.</p>")

langkah("Tulis daftar yang harus diabaikan",
    blok("aksi", "Buat berkas bernama <code>.gitignore</code> — pakai titik di depan — berisi empat "
                 "baris ini, lalu tanya git lagi.", "LAKUKAN"),
    kode('printf ".env\\ndata/\\n__pycache__/\\nvenv/\\n" > .gitignore\ngit status -s'),
    blok("hasil", kode("?? .gitignore", salin=False), "HARUS MUNCUL"),
    "<p><code>.env</code> dan <code>data/</code> lenyap dari daftar. Yang tersisa cuma "
    "<code>.gitignore</code> itu sendiri — dan berkas itu memang <em>harus</em> ikut ter-commit, "
    "supaya siapa pun yang meng-<em>clone</em> proyekmu mewarisi aturan yang sama.</p>")

langkah("Buktikan aturan mana yang menangkap berkas mana",
    blok("aksi", "Jangan percaya begitu saja. Tanya git aturan baris ke berapa yang bekerja.", "LAKUKAN"),
    kode("git check-ignore -v .env data/mentah.csv"),
    blok("hasil", kode(""".gitignore:1:.env	.env
.gitignore:2:data/	data/mentah.csv""", salin=False), "HARUS MUNCUL"),
    "<p>Dibaca begini: <em>berkas .gitignore, baris 1, aturan <code>.env</code></em> — itu yang "
    "menangkap <code>.env</code>. Kalau nanti ada berkas yang <em>seharusnya</em> diabaikan tapi "
    "tetap muncul, perintah ini yang memberitahu kenapa.</p>",
    blok("catatan", "<strong>Daftar minimal untuk proyek data:</strong> "
                    "<code>.env</code> · <code>*.key</code> · <code>data/</code> · "
                    "<code>*.xlsx</code> · <code>__pycache__/</code> · "
                    "<code>.ipynb_checkpoints/</code> · <code>venv/</code>. "
                    "Tiga kategori: kredensial, data klien, dan sampah yang bisa dibuat ulang."))

langkah("Sekarang jebakannya: commit dulu, ignore belakangan",
    blok("aksi", "Kita sengaja melakukan kesalahan yang paling sering terjadi. Simpan "
                 "<code>.gitignore</code>, lalu buat kunci API dan commit — <em>sebelum</em> "
                 "sempat memasukkannya ke daftar abaikan.", "LAKUKAN"),
    kode('git add .gitignore && git commit -q -m "Tambah .gitignore"\nprintf "API_KEY=abc123\\n" > kunci.txt\ngit add kunci.txt && git commit -q -m "Simpan kunci API"\necho "kunci.txt" >> .gitignore\ngit status -s'),
    blok("hasil", kode(" M .gitignore", salin=False), "HARUS MUNCUL"),
    "<p><code>kunci.txt</code> <strong>tidak muncul</strong> di daftar — dan itu justru kabar buruk. "
    "Ia tidak muncul bukan karena diabaikan, tapi karena tidak ada yang berubah padanya. "
    "Ia sudah jadi milik git.</p>")

langkah("Tanya git berkas apa saja yang sudah jadi miliknya",
    blok("aksi", "Satu baris.", "LAKUKAN"),
    kode("git ls-files"),
    blok("hasil", kode(""".gitignore
README.md
kunci.txt""", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Inilah aturan yang harus kamu hafal: <code>.gitignore</code> hanya "
                   "berlaku untuk berkas yang belum pernah di-commit.</strong> Begitu sebuah berkas "
                   "masuk, menambahkannya ke <code>.gitignore</code> tidak berpengaruh sama sekali. "
                   "Git akan terus melacaknya, selamanya."))

langkah("Hentikan pelacakannya",
    blok("aksi", "Dua baris. <code>--cached</code> artinya hapus dari git, tapi berkasnya di "
                 "komputermu tetap ada.", "LAKUKAN"),
    kode('git rm --cached kunci.txt\ngit commit -q -am "Berhenti melacak kunci.txt"\ngit ls-files'),
    blok("hasil", kode("""rm 'kunci.txt'
.gitignore
README.md""", salin=False), "HARUS MUNCUL"),
    "<p>Sekarang bersih. Berkasnya masih ada di foldermu, tapi git sudah melepasnya.</p>",
    blok("catatan", "<strong>Tanpa <code>--cached</code>, berkasnya ikut terhapus dari komputermu.</strong> "
                    "<code>git rm kunci.txt</code> menghapus dua-duanya. Satu kata yang lupa diketik, "
                    "dan berkas aslinya hilang."))

langkah("Sekarang periksa apakah kunci itu benar-benar hilang",
    blok("aksi", "Jangan percaya. Cari isinya di seluruh riwayat.", "LAKUKAN"),
    kode('git log -p --all -- kunci.txt | grep "^+API_KEY"'),
    blok("hasil", kode("+API_KEY=abc123", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Kuncinya masih ada.</strong> Kamu sudah menghapus berkasnya, sudah "
                   "commit pembersihannya, sudah menambahkannya ke <code>.gitignore</code> — dan "
                   "isinya tetap bisa dibaca siapa pun yang meng-<em>clone</em> repositorimu. "
                   "Riwayat git menyimpan semua versi lama; itu memang gunanya."),
    "<p><strong>Jadi obatnya bukan teknis, tapi administratif: ganti kuncinya.</strong> Cabut kunci "
    "API itu di dasbor penyedianya, terbitkan yang baru. Membersihkan riwayat git bisa dilakukan "
    "(<code>git filter-repo</code>), tapi kalau repositorimu pernah publik walau lima menit, "
    "anggap kuncinya sudah bocor. Robot pemindai GitHub lebih cepat darimu.</p>",
    """<details>
          <summary>Cara kerja yang membuat ini tidak pernah terjadi</summary>
          <div class="isi">
            <p>Tulis <code>.gitignore</code> sebagai berkas <strong>pertama</strong> di setiap
            proyek baru — sebelum ada satu pun berkas lain, sebelum commit pertama.
            Butuh sepuluh detik, dan menutup seluruh kelas kesalahan ini.</p>
            <p>Dan biasakan mengetik <code>git status</code> lalu membaca daftarnya sebelum
            <code>git add .</code>. Titik di belakang <code>add</code> berarti "semuanya",
            termasuk yang tidak kamu sadari ada.</p>
          </div>
        </details>""")

langkah("Susun folder proyek yang bisa dijalankan orang lain",
    blok("aksi", "Empat folder, tiga berkas kosong.", "LAKUKAN"),
    kode("mkdir -p src hasil data-contoh\ntouch src/muat.py src/olah.py src/laporan.py\nfind . -maxdepth 2 -not -path './.git*' -not -path './venv*' | sort"),
    blok("hasil", kode(""".
./.env
./README.md
./data
./data-contoh
./data/mentah.csv
./hasil
./kunci.txt
./src
./src/laporan.py
./src/muat.py
./src/olah.py""", salin=False), "HARUS MUNCUL"),
    "<p>Perhatikan <code>.env</code>, <code>data/mentah.csv</code>, dan <code>kunci.txt</code> "
    "masih di situ. Diabaikan git bukan berarti terhapus dari komputermu — mereka tetap ada dan "
    "tetap bisa kamu pakai, cuma tidak ikut ke internet.</p>",
    tabel(["Folder", "Isinya", "Masuk git?"],
          [["<code>src/</code>", "kode Python", "ya"],
           ["<code>data/</code>", "data klien asli", "<strong>tidak pernah</strong>"],
           ["<code>data-contoh/</code>", "beberapa baris palsu supaya orang bisa mencoba", "ya"],
           ["<code>hasil/</code>", "keluaran yang dibuat skrip", "boleh, kalau kecil"]],
          kelas_n=()),
    "<p>Folder <code>data-contoh/</code> itu yang membedakan portofolio yang bisa dicoba orang dari "
    "portofolio yang cuma bisa dilihat. Perekrut yang tertarik akan meng-<em>clone</em> repomu; "
    "kalau skripmu langsung gagal karena tidak ada datanya, ketertarikan itu berhenti di situ.</p>")

langkah("Buat lingkungan virtual",
    blok("aksi", "Dua baris. Baris kedua Mac/Linux; kalau kamu di Windows Git Bash pakai "
                 "<code>source venv/Scripts/activate</code>.", "LAKUKAN"),
    kode("python3 -m venv venv\nsource venv/bin/activate\npip list"),
    blok("hasil", kode("""Package    Version
---------- -------
pip        24.0
setuptools 79.0.1""", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau ada tambahan <code>[notice] A new release of pip is "
                    "available</code>:</strong> abaikan. Itu iklan pembaruan pip, bukan kesalahan, "
                    "dan muncul di hampir semua venv baru."),
    "<p><strong>Kosong — dan itu memang tujuannya.</strong> Semua pustaka yang pernah kamu pasang "
    "di komputer ini tidak terlihat dari dalam sini. Kamu mulai dari nol, sama seperti server yang "
    "akan menjalankan kodemu nanti.</p>",
    blok("catatan", "<strong>Nama folder di depan prompt terminalmu berubah jadi "
                    "<code>(venv)</code>.</strong> Itu satu-satunya tanda bahwa lingkungan virtualnya "
                    "aktif. Kalau tanda itu tidak ada, <code>pip install</code>-mu masuk ke Python "
                    "sistem, bukan ke proyek ini."))

langkah("Pasang pandas, lalu bekukan daftarnya",
    blok("aksi", "Dua baris.", "LAKUKAN"),
    kode("pip install pandas\npip freeze > requirements.txt\ncat requirements.txt"),
    blok("hasil", kode("""numpy==2.4.6
pandas==3.0.5
python-dateutil==2.9.0.post0
six==1.17.0""", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Nomor versimu boleh berbeda dariku</strong> — itu versi terbaru saat "
                    "kamu memasangnya. Yang harus sama adalah bentuknya: satu pustaka per baris, "
                    "dengan tanda <code>==</code> dan nomor versi yang tepat."),
    "<p>Kamu memasang <strong>satu</strong> pustaka, tapi daftarnya berisi <strong>empat</strong>. "
    "Tiga sisanya adalah pustaka yang dibutuhkan pandas. Inilah sebabnya <code>requirements.txt</code> "
    "dibuat oleh <code>pip freeze</code>, bukan diketik tangan — kamu tidak tahu apa saja yang "
    "diam-diam ikut terpasang.</p>")

langkah("Simpan, lalu buktikan .env tidak ikut",
    blok("aksi", "Commit semuanya, lalu periksa daftar berkas yang dilacak git.", "LAKUKAN"),
    kode('git add . && git commit -q -m "Struktur proyek, venv, dan requirements"\ngit ls-files'),
    blok("hasil", kode(""".gitignore
README.md
requirements.txt
src/laporan.py
src/muat.py
src/olah.py""", salin=False), "HARUS MUNCUL"),
    "<p><code>.env</code>, folder <code>data/</code>, dan seluruh isi <code>venv/</code> — yang "
    "berisi ribuan berkas — tidak ada satu pun di daftar. Itu bukti bahwa <code>.gitignore</code>-mu "
    "bekerja, dan bukti itu kamu dapat dalam satu perintah.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Buat folder proyek baru dari nol, tanpa melihat halaman ini. Urutannya: "
                 "<code>git init</code> → <strong>.gitignore duluan</strong> → struktur folder → "
                 "venv → <code>pip install</code> → <code>pip freeze</code> → commit pertama.", "LAKUKAN"),
    "<p>Lalu jawab dua pertanyaan tanpa membuka apa pun: <strong>(a)</strong> kenapa "
    "<code>.gitignore</code> harus jadi berkas pertama, dan <strong>(b)</strong> apa yang kamu "
    "lakukan kalau kunci API sudah terlanjur ter-commit dua minggu lalu.</p>",
    """<details>
          <summary>Jawaban</summary>
          <div class="isi">
            <p><strong>(a)</strong> Karena <code>.gitignore</code> tidak berlaku surut. Berkas yang
            sudah pernah ter-commit akan terus dilacak meskipun namanya ditambahkan belakangan.</p>
            <p><strong>(b)</strong> Cabut kunci itu dan terbitkan yang baru. Menghapus berkasnya
            tidak menghapus riwayatnya, dan repositori yang pernah publik harus dianggap sudah
            terbaca. Membersihkan riwayat adalah langkah kedua, bukan pertama.</p>
          </div>
        </details>""")

HARI72 = {
  "n": "HARI 72",
  "tab": "72",
  "judul": "Kredensial yang terlanjur masuk git tidak bisa dihapus",
  "waktu": "± 60 menit",
  "tujuan": "menulis <code>.gitignore</code> yang benar, membuktikan sendiri kenapa ia tidak "
            "menyelamatkan berkas yang terlanjur ter-commit, dan menyusun proyek Python yang bisa "
            "dijalankan ulang orang lain.",
  "langkah": L,
  "tutup_judul": "Hari 72 selesai. Berhenti di sini.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> <code>.gitignore</code> ditulis sebelum commit "
           "pertama · <code>git check-ignore -v</code> untuk membuktikan · <code>git ls-files</code> "
           "untuk melihat apa yang sudah jadi milik git · kunci yang pernah ter-commit "
           "<strong>diganti</strong>, bukan dihapus.</p>",
}
