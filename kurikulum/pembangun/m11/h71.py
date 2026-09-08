# -*- coding: utf-8 -*-
"""Hari 71 — alur git, ditulis ulang mengikuti _pola.md.
Semua keluaran di kotak HARUS MUNCUL diperoleh dengan menjalankan perintahnya
sungguhan (git 2.43.0) di folder lab-git."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buat folder latihan dan nyalakan git di dalamnya",
    blok("aksi", "Buka Terminal (Mac: Terminal · Windows: Git Bash). Ketik empat baris ini "
                 "satu per satu, tekan Enter tiap baris.", "LAKUKAN"),
    kode("mkdir latihan-git\ncd latihan-git\ngit init -b main"),
    blok("hasil", kode("Initialized empty Git repository in /home/kamu/latihan-git/.git/", salin=False),
         "HARUS MUNCUL"),
    "<p>Satu folder tersembunyi bernama <code>.git</code> baru saja dibuat di situ. "
    "Seluruh riwayat proyek nanti tinggal di dalam folder itu — bukan di cloud, bukan di GitHub.</p>",
    blok("catatan", "<strong>Kalau muncul <code>git: command not found</code>:</strong> git belum "
                    "terpasang. Mac: ketik <code>xcode-select --install</code>. Windows: pasang "
                    "Git for Windows dari <code>git-scm.com</code>, lalu buka Git Bash, bukan CMD."))

langkah("Beri tahu git kamu siapa",
    blok("aksi", "Ganti nama dan email di bawah dengan milikmu, lalu jalankan.", "LAKUKAN"),
    kode('git config user.name "Nama Kamu"\ngit config user.email "email@kamu.com"'),
    blok("hasil", "<p>Tidak ada apa-apa yang muncul. Kursor langsung kembali ke baris baru.</p>",
         "HARUS MUNCUL"),
    blok("catatan", "<strong>Tidak ada keluaran itu benar.</strong> Sebagian besar perintah git "
                    "yang berhasil memang diam. Yang berisik justru yang gagal. Kalau kamu menunggu "
                    "ucapan selamat dari git, kamu akan menunggu selamanya."))

langkah("Buat berkas pertama, lalu tanya git apa yang ia lihat",
    blok("aksi", "Dua baris. Yang pertama membuat berkas <code>README.md</code>, "
                 "yang kedua bertanya ke git.", "LAKUKAN"),
    kode('echo "# Analisis Penjualan Toko" > README.md\ngit status'),
    blok("hasil", kode("""On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md

nothing added to commit but untracked files present (use "git add" to track)""", salin=False), "HARUS MUNCUL"),
    "<p><strong>Untracked</strong> artinya git melihat berkas itu ada, tapi belum mau mengurusnya. "
    "Git tidak pernah menyimpan apa pun tanpa kamu suruh — itu fitur, bukan kelalaian.</p>")

langkah("Simpan versi pertama",
    blok("aksi", "Dua langkah, dan ini pasangan yang akan kamu ketik ribuan kali seumur hidup.", "LAKUKAN"),
    kode('git add README.md\ngit commit -m "Commit pertama: README proyek"'),
    blok("hasil", kode("""[main (root-commit) 282f1a3] Commit pertama: README proyek
 1 file changed, 1 insertion(+)
 create mode 100644 README.md""", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Tujuh huruf-angka itu punyamu pasti beda.</strong> <code>282f1a3</code> "
                    "adalah sidik jari commit — dihitung dari isi, waktu, dan namamu. Tidak ada dua "
                    "orang di dunia yang mendapat angka sama. Yang harus sama denganku cuma "
                    "<code>1 file changed, 1 insertion(+)</code>."),
    "<p><code>git add</code> memilih apa yang mau disimpan. <code>git commit</code> menyimpannya "
    "sungguhan, dengan catatan kenapa. Dua perintah, bukan satu, dan sebentar lagi kamu tahu kenapa "
    "pemisahan itu berharga.</p>")

langkah("Buat cabang sebelum mengubah apa pun",
    blok("aksi", "Satu baris.", "LAKUKAN"),
    kode("git switch -c catatan-metodologi"),
    blok("hasil", kode("Switched to a new branch 'catatan-metodologi'", salin=False), "HARUS MUNCUL"),
    "<p>Cabang (<em>branch</em>) adalah salinan pekerjaan yang bisa kamu rusak tanpa merusak "
    "<code>main</code>. Di portofolio pribadi ini terasa berlebihan. Di tim, mengubah "
    "<code>main</code> langsung adalah pelanggaran yang membuat orang menegurmu di hari pertama.</p>",
    blok("catatan", "<strong>Kalau git-mu tua dan menolak <code>switch</code>:</strong> pakai "
                    "<code>git checkout -b catatan-metodologi</code>. Sama persis hasilnya. "
                    "<code>switch</code> baru ada sejak git 2.23 (2019) dan lebih sulit disalahketik."))

langkah("Ubah berkasnya, lalu lihat bedanya baris demi baris",
    blok("aksi", "Tambahkan tiga baris ke README, lalu minta git menunjukkan perubahannya.", "LAKUKAN"),
    kode('printf "\\n## Metodologi\\n\\nRetur dihitung negatif, bukan dibuang.\\n" >> README.md\ngit diff'),
    blok("hasil", kode("""diff --git a/README.md b/README.md
index 440f372..2dffde4 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,5 @@
 # Analisis Penjualan Toko
+
+## Metodologi
+
+Retur dihitung negatif, bukan dibuang.""", salin=False), "HARUS MUNCUL"),
    "<p>Baris berawalan <code>+</code> ditambahkan; kalau ada <code>-</code> berarti dihapus. "
    "Inilah yang dibaca orang saat mereview pekerjaanmu — dan inilah yang harus kamu baca sendiri "
    "sebelum menyerahkannya.</p>",
    blok("catatan", "<strong>Kalau layarnya berhenti dan ada tanda <code>:</code> di bawah:</strong> "
                    "git sedang menahan tampilan supaya bisa digulung. Tekan <kbd>q</kbd> untuk keluar. "
                    "Ini yang paling sering membuat pemula mengira terminalnya menggantung."))

langkah("Perhatikan kolom yang bergeser satu spasi",
    blok("aksi", "Jalankan <code>git status -s</code> — versi ringkasnya. Lalu <code>git add</code>, "
                 "lalu jalankan lagi. Perhatikan baik-baik posisi hurufnya.", "LAKUKAN"),
    kode("git status -s\ngit add README.md\ngit status -s"),
    blok("hasil", kode(""" M README.md
M  README.md""", salin=False), "HARUS MUNCUL"),
    "<p>Dua baris itu <strong>tidak sama</strong>. Yang pertama: spasi dulu, baru <code>M</code>. "
    "Yang kedua: <code>M</code> dulu, baru spasi. Kalau di layarmu terlihat mirip, hitung spasinya.</p>",
    "<p><strong>Kolom kiri = sudah dipilih untuk disimpan. Kolom kanan = berubah tapi belum dipilih.</strong> "
    "Satu spasi geser, dua arti berbeda. Sekali kamu melihatnya, kamu tidak bisa tidak melihatnya lagi.</p>",
    """<details>
          <summary>Kenapa git repot memisahkan "dipilih" dan "berubah"?</summary>
          <div class="isi">
            <p>Karena kamu sering mengubah lima berkas sekaligus, tapi cuma tiga di antaranya
            yang layak disimpan bersama sebagai satu perubahan yang masuk akal. Yang dua lagi
            — misalnya berkas berisi kata sandi percobaan — tidak boleh ikut.</p>
            <p>Coba sendiri: jalankan <code>git diff</code> sekarang, sesudah <code>git add</code>.
            Hasilnya <strong>kosong</strong>. Bukan karena perubahanmu hilang, tapi karena
            <code>git diff</code> hanya menunjukkan yang <em>belum</em> dipilih. Untuk melihat
            yang sudah dipilih, pakai <code>git diff --staged</code>. Ini jebakan yang membuat
            orang panik dan mengetik ulang pekerjaannya.</p>
          </div>
        </details>""")

langkah("Tulis pesan commit yang masih berguna enam bulan lagi",
    blok("aksi", "Perintah ini punya dua <code>-m</code>. Yang pertama judul, yang kedua alasan. "
                 "Salin apa adanya.", "LAKUKAN"),
    kode('git commit -m "Jelaskan perlakuan retur di README" \\\n  -m "Pembaca perlu tahu retur dihitung negatif, bukan dibuang."'),
    blok("hasil", kode("""[catatan-metodologi 1b1d321] Jelaskan perlakuan retur di README
 1 file changed, 4 insertions(+)""", salin=False), "HARUS MUNCUL"),
    "<p>Judul menjawab <em>apa</em>. Badan menjawab <em>kenapa</em>. Kode sudah memberitahu apa yang "
    "berubah — yang tidak bisa dibaca dari kode adalah alasannya.</p>",
    tabel(["Pesan yang buruk", "Pesan yang berguna", "Kenapa"],
          [["<code>update</code>", "<code>Perbaiki JOIN ganda di mart harian</code>",
            "Enam bulan lagi kamu perlu tahu apa yang berubah"],
           ["<code>fix bug</code>", "<code>Ganti inner join jadi left join supaya produk tanpa penjualan tetap muncul</code>",
            "Menjelaskan keputusan, bukan cuma tindakan"],
           ["<code>asdfgh</code>", "<code>Tambah test rekonsiliasi omzet mart vs sumber</code>",
            "Riwayat commit adalah dokumentasi yang tidak pernah basi"]]))

langkah("Lihat riwayatnya, lalu kembali ke main",
    blok("aksi", "Tiga baris.", "LAKUKAN"),
    kode("git log --oneline\ngit switch main\ncat README.md"),
    blok("hasil", kode("""1b1d321 Jelaskan perlakuan retur di README
282f1a3 Commit pertama: README proyek
Switched to branch 'main'
# Analisis Penjualan Toko""", salin=False), "HARUS MUNCUL"),
    "<p><strong>Bagian Metodologi hilang dari README.</strong> Itu bukan kerusakan — itu inti "
    "cabang. Perubahanmu masih utuh di cabang <code>catatan-metodologi</code>; "
    "<code>main</code> memang belum tahu apa-apa soal itu.</p>",
    blok("bahaya", "<strong>Jangan panik di titik ini.</strong> Berkas yang “hilang” saat berpindah "
                   "cabang adalah pemandangan normal yang paling sering membuat pemula mengira "
                   "pekerjaannya lenyap. Ketik <code>git switch catatan-metodologi</code> dan "
                   "isinya kembali. Tidak ada yang hilang selama sudah di-<em>commit</em>."))

langkah("Gabungkan, lalu bersihkan",
    blok("aksi", "Dari <code>main</code>, jalankan dua baris ini.", "LAKUKAN"),
    kode("git merge catatan-metodologi\ngit branch -d catatan-metodologi"),
    blok("hasil", kode("""Updating 282f1a3..1b1d321
Fast-forward
 README.md | 4 ++++
 1 file changed, 4 insertions(+)
Deleted branch catatan-metodologi (was 1b1d321).""", salin=False), "HARUS MUNCUL"),
    "<p><em>Fast-forward</em> artinya <code>main</code> tidak berubah sejak cabang dibuat, jadi git "
    "cukup memajukan penunjuknya — tidak ada yang perlu didamaikan.</p>",
    blok("catatan", "<strong>Di tim, langkah ini tidak kamu lakukan sendiri.</strong> Kamu "
                    "<code>git push</code>, membuka <em>pull request</em> di GitHub, dan orang lain "
                    "yang menekan tombol gabung setelah membaca diff-mu. Perintahnya sama; yang "
                    "berbeda cuma siapa yang menekannya."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Buka folder baru, dan kerjakan seluruh alur tadi dari nol "
                 "tanpa melihat: init → config → berkas → add → commit → cabang → ubah → diff → "
                 "commit → main → merge → hapus cabang.", "LAKUKAN"),
    "<p>Kalau macet di satu perintah, jangan buka halaman ini — ketik <code>git status</code> dulu. "
    "Sembilan dari sepuluh kali, git sendiri yang memberitahu perintah berikutnya di dalam tanda "
    "kurung. Membaca keluaran git adalah keterampilan yang lebih berharga daripada menghafal "
    "perintahnya.</p>",
    blok("catatan", "<strong>Kalau perlu tiga kali percobaan, itu wajar.</strong> Yang tidak wajar "
                    "adalah menyalin ulang dari halaman ini dan merasa sudah bisa."))

HARI71 = {
  "n": "HARI 71",
  "tab": "71",
  "judul": "Git yang benar-benar kamu ketik, bukan yang kamu baca",
  "waktu": "± 60 menit",
  "tujuan": "menjalankan satu perubahan lewat alur git lengkap — cabang, diff, commit, gabung — "
            "dan tahu membedakan berkas yang <em>dipilih</em> dari yang cuma <em>berubah</em>.",
  "langkah": L,
  "tutup_judul": "Hari 71 selesai. Berhenti di sini.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> "
           "<code>switch -c</code> → ubah → <code>diff</code> → <code>add</code> → "
           "<code>commit -m</code> → <code>switch main</code> → <code>merge</code> → "
           "<code>branch -d</code>.</p>"
           "<p style=\"margin-top:8px\">Dan satu kebiasaan: ketik <code>git status</code> "
           "sebelum dan sesudah setiap perintah, sampai kamu bisa menebak keluarannya "
           "sebelum menekan Enter.</p>",
}
