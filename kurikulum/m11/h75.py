# -*- coding: utf-8 -*-
"""Hari 75 — ulangan dari ingatan. Setiap soal dikerjakan di terminal, bukan dijawab
di kepala; keluarannya diverifikasi dengan menjalankan sungguhan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Aturan mainnya",
    blok("bahaya", "<strong>Tutup catatanmu, tutup empat hari sebelumnya, tutup Google.</strong> "
                   "Enam soal di bawah dikerjakan <em>di terminal</em>, bukan dijawab di kepala. "
                   "Membaca ulang terasa seperti belajar tapi tidak mengikat apa pun; memanggil "
                   "dari ingatan yang mengikat."),
    blok("aksi", "Buat folder kosong bernama <code>ujian-11</code> dan masuk ke dalamnya. "
                 "Semua soal dikerjakan di situ.", "LAKUKAN"),
    kode("mkdir ujian-11 && cd ujian-11"),
    "<p>Kalau satu soal macet lebih dari tiga menit, lewati dan lanjut. Kembali ke Hari 71–74 "
    "untuk bagian yang macet — itu justru informasi paling berguna dari ulangan ini.</p>")

langkah("Soal 1 — repositori siap pakai dalam lima perintah",
    blok("aksi", "Dari folder kosong tadi, buat repositori git yang sudah punya "
                 "<code>.gitignore</code> benar dan satu commit. Jangan melihat contoh.", "LAKUKAN"),
    blok("hasil", kode(""".gitignore
README.md""", salin=False), "HARUS MUNCUL"),
    "<p>Itu keluaran <code>git ls-files</code> setelah commit pertamamu. Kalau ada berkas ketiga "
    "yang tidak kamu sengaja, itu jawaban salah.</p>",
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <div class="kode"><pre><code>git init -b main
printf ".env\\ndata/\\nvenv/\\n__pycache__/\\n" &gt; .gitignore
echo "# Proyek" &gt; README.md
git add .
git commit -m "Kerangka proyek"</code></pre></div>
            <p>Urutannya yang dinilai: <code>.gitignore</code> ada <strong>sebelum</strong>
            commit pertama.</p>
          </div>
        </details>""")

langkah("Soal 2 — buktikan .env benar-benar diabaikan",
    blok("aksi", "Buat berkas <code>.env</code> berisi apa saja. Lalu buktikan dengan "
                 "<strong>dua</strong> perintah berbeda bahwa git mengabaikannya.", "LAKUKAN"),
    blok("hasil", kode(""".gitignore:1:.env	.env""", salin=False), "HARUS MUNCUL"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p>Bukti pertama: <code>git status -s</code> — daftarnya kosong, artinya git tidak
            melihat berkas baru. Bukti kedua, yang lebih kuat karena menyebut alasannya:</p>
            <div class="kode"><pre><code>git check-ignore -v .env</code></pre></div>
            <p>Bukti kedua lebih berharga saat ada yang tidak beres, karena ia menyebutkan
            baris ke berapa di <code>.gitignore</code> yang bekerja.</p>
          </div>
        </details>""")

langkah("Soal 3 — cabang, ubah, gabung, hapus",
    blok("aksi", "Tanpa melihat: buat cabang baru, ubah README, commit di cabang itu, kembali ke "
                 "<code>main</code>, gabungkan, lalu hapus cabangnya.", "LAKUKAN"),
    blok("hasil", kode("""Fast-forward
 README.md | 1 +
Deleted branch coba (was aa38a5a).""", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Nama cabang dan tujuh huruf-angkanya bebas.</strong> Yang harus sama: "
                    "kata <code>Fast-forward</code> dan kalimat <code>Deleted branch</code>."),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <div class="kode"><pre><code>git switch -c coba
echo "baris baru" &gt;&gt; README.md
git commit -am "Tambah baris"
git switch main
git merge coba
git branch -d coba</code></pre></div>
            <p><code>commit -am</code> menggabungkan <code>add</code> dan <code>commit</code> —
            tapi hanya untuk berkas yang <em>sudah</em> dilacak git. Berkas baru tetap butuh
            <code>git add</code> tersendiri.</p>
          </div>
        </details>""")

langkah("Soal 4 — dua soal yang dijawab dengan menulis, bukan mengetik",
    blok("aksi", "Tulis jawabannya di kertas atau catatan, satu-dua kalimat, sebelum membuka kunci.", "LAKUKAN"),
    """<ol>
          <li>Kunci API-mu ter-commit dua minggu lalu, repositorinya publik. Kamu sudah menghapus
          berkasnya dan menambahkannya ke <code>.gitignore</code>. Apakah masalahnya selesai?
          Kalau belum, apa langkah pertamamu?</li>
          <li>Kamu menulis <code>hasil/</code> lalu <code>!hasil/ringkasan.md</code> di
          <code>.gitignore</code>, tapi berkasnya tetap tidak mau masuk git. Kenapa?</li>
        </ol>""",
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>1.</strong> Belum selesai. Riwayat git menyimpan semua versi lama, jadi
            kuncinya masih bisa dibaca siapa pun yang meng-clone. Langkah pertama:
            <strong>cabut kunci itu dan terbitkan yang baru</strong>. Membersihkan riwayat adalah
            langkah kedua, dan untuk repositori yang pernah publik ia tidak menyelamatkan apa pun —
            robot pemindai bekerja dalam hitungan menit.</p>
            <p><strong>2.</strong> Karena git tidak pernah masuk ke folder yang seluruhnya
            diabaikan, sehingga baris pengecualian di dalamnya tidak pernah terbaca. Harus
            <code>hasil/*</code> — dengan tanda bintang.</p>
          </div>
        </details>""")

langkah("Soal 5 — jadwal dan lencana",
    blok("aksi", "Jawab tiga ini tanpa membuka apa pun.", "LAKUKAN"),
    """<ol>
          <li>Tulis baris <code>cron</code> untuk berjalan tiap hari jam 08:00 WIB.</li>
          <li>Apa yang terjadi kalau workflow-mu menjalankan <code>git commit</code> di minggu
          ketika datanya tidak berubah sama sekali — dan bagaimana mencegahnya?</li>
          <li>Kenapa <code>workflow_dispatch</code> hampir selalu ditulis?</li>
        </ol>""",
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>1.</strong> <code>0 1 * * *</code> — WIB = UTC + 7, jadi 08:00 WIB adalah
            01:00 UTC.</p>
            <p><strong>2.</strong> <code>git commit</code> tanpa perubahan mengembalikan kode
            keluar 1, jadi pekerjaannya ditandai <strong>merah</strong> padahal tidak ada yang
            salah. Dicegah dengan
            <code>git diff --staged --quiet || git commit -m "..."</code>.</p>
            <p><strong>3.</strong> Supaya ada tombol <em>Run workflow</em> untuk menguji sekarang
            juga, tanpa menunggu jadwalnya tiba.</p>
          </div>
        </details>""")

langkah("Soal 6 — Streamlit dari ingatan",
    blok("aksi", "Tulis aplikasi Streamlit terpendek yang menampilkan judul, satu filter, dan satu "
                 "angka — dari ingatan, lalu jalankan. Boleh salah; yang dinilai apakah kamu tahu "
                 "bentuknya.", "LAKUKAN"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <div class="kode"><pre><code>import pandas as pd
import streamlit as st

@st.cache_data
def muat():
    return pd.read_csv("data-contoh/penjualan.csv")

df = muat()
st.title("Penjualan")
pilih = st.sidebar.selectbox("Produk", sorted(df["produk"].unique()))
st.metric("Nota", len(df[df["produk"] == pilih]))</code></pre></div>
            <p>Dan satu pertanyaan yang harus kamu bisa jawab: <strong>kenapa
            <code>@st.cache_data</code> ada di situ?</strong> Karena setiap interaksi menjalankan
            ulang seluruh berkas dari baris pertama, termasuk pembacaan datanya.</p>
          </div>
        </details>""")

langkah("Hitung skormu, lalu putuskan",
    blok("aksi", "Beri satu poin per soal yang benar tanpa membuka kunci. Enam soal.", "LAKUKAN"),
    tabel(["Skor", "Artinya", "Lakukan"],
          [["5–6", "Sudah melekat", "Lanjut ke Hari 76"],
           ["3–4", "Bentuknya tahu, detailnya belum", "Ulangi hari yang salahnya, lalu ujian lagi besok"],
           ["0–2", "Masih membaca, belum mengerjakan", "Ulangi Hari 71–74 dengan mengetik ulang semuanya"]]),
    blok("catatan", "<strong>Skor rendah di sini murah; skor rendah saat wawancara mahal.</strong> "
                    "Mengulang dua hari sekarang jauh lebih hemat daripada melanjutkan dengan "
                    "fondasi yang belum menempel."))

HARI75 = {
  "n": "HARI 75",
  "tab": "75",
  "judul": "Ulangan dari ingatan — dikerjakan di terminal, bukan dijawab di kepala",
  "waktu": "± 45 menit",
  "tujuan": "tidak ada materi baru. Enam soal, semuanya dikerjakan tanpa membuka catatan, "
            "sebagian besar dengan mengetik perintah sungguhan.",
  "langkah": L,
  "tutup_judul": "Hari 75 selesai.",
  "tutup": "<p>Kalau lima dari enam benar, lanjut ke proyek besar Hari 76–77. Kalau kurang, "
           "ulangi hari yang salahnya dulu — proyek dua hari ke depan menumpuk semuanya sekaligus, "
           "dan lubang kecil di sini jadi lubang besar di sana.</p>",
}
