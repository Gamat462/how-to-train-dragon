# -*- coding: utf-8 -*-
"""Hari 74 — Streamlit. Setiap angka di kotak HARUS MUNCUL diambil dari aplikasi
yang benar-benar dijalankan (Streamlit 1.63.0, pandas 3.0.5) dan dibaca dari layar
lewat browser sungguhan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Pasang Streamlit",
    blok("aksi", "Pastikan lingkungan virtualmu aktif — ada tulisan <code>(venv)</code> di depan "
                 "prompt. Lalu satu baris.", "LAKUKAN"),
    kode("pip install streamlit"),
    blok("hasil", kode("Successfully installed altair-6.2.2 ... streamlit-1.63.0", salin=False),
         "HARUS MUNCUL"),
    blok("catatan", "<strong>Pemasangannya lama, 1–3 menit, dan mengunduh belasan pustaka lain.</strong> "
                    "Itu wajar: Streamlit membawa server web sendiri. Nomor versimu boleh lebih baru "
                    "dari <code>1.63.0</code>."))

langkah("Tiga baris pertama",
    blok("aksi", "Buat berkas <code>app.py</code> berisi tepat tiga baris ini.", "LAKUKAN"),
    kode('import streamlit as st\n\nst.title("Penjualan Toko Sumber Rejeki")\nst.write("Halo dari aplikasi pertamaku")'),
    "<p>Lalu jalankan — perhatikan, <strong>bukan</strong> <code>python app.py</code>:</p>",
    kode("streamlit run app.py"),
    blok("hasil", kode("""  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.5:8501""", salin=False), "HARUS MUNCUL"),
    "<p>Browser terbuka sendiri dan menampilkan judul besar <strong>Penjualan Toko Sumber Rejeki</strong> "
    "dengan satu baris teks di bawahnya. Tidak ada satu huruf HTML pun yang kamu tulis.</p>",
    blok("bahaya", "<strong>Kalau kamu menjalankan <code>python app.py</code>,</strong> yang muncul "
                   "adalah peringatan panjang dan halaman kosong. Streamlit bukan skrip biasa — ia "
                   "server, dan harus dijalankan lewat perintah <code>streamlit run</code>."))

langkah("Biarkan terminalnya jalan, dan pahami kenapa",
    blok("aksi", "Jangan tutup terminalnya. Kembali ke editor, ubah <code>st.write</code> jadi "
                 "kalimat lain, simpan, lalu lihat browsernya.", "LAKUKAN"),
    blok("hasil", "<p>Di pojok kanan atas browser muncul tombol <strong>Rerun</strong> / "
                  "<strong>Always rerun</strong>. Klik <em>Always rerun</em> sekali, dan sejak itu "
                  "setiap kali kamu menyimpan berkas, halamannya berubah sendiri.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Terminal yang “menggantung” itu benar.</strong> Server harus terus "
                    "hidup selama aplikasinya dipakai. Untuk menghentikannya nanti: "
                    "<kbd>Ctrl</kbd>+<kbd>C</kbd> di terminal itu."))

langkah("Tampilkan tabelnya",
    blok("aksi", "Ganti isi <code>app.py</code> dengan ini. Simpan, lihat browser.", "LAKUKAN"),
    kode('''import pandas as pd
import streamlit as st

st.title("Penjualan Toko Sumber Rejeki")
df = pd.read_csv("data-contoh/penjualan.csv", parse_dates=["tanggal"])
st.dataframe(df)'''),
    blok("hasil", "<p>Tabel 400 baris yang bisa digulung, diurutkan dengan mengklik judul kolomnya, "
                  "dan dicari isinya. Kolom <code>tanggal</code> tertulis "
                  "<code>2024-01-02 00:00:00</code>.</p>", "YANG HARUS TERLIHAT"),
    "<p><strong>Jam <code>00:00:00</code> itu mengganggu, dan itu salahmu, bukan salah Streamlit.</strong> "
    "<code>parse_dates</code> membuat kolomnya bertipe waktu lengkap; datanya memang tidak punya jam. "
    "Perbaikannya satu baris, dan biarkan dulu — kita kembali ke sini nanti.</p>")

langkah("Tiga angka besar di atas tabel",
    blok("aksi", "Sisipkan blok ini <em>sebelum</em> <code>st.dataframe(df)</code>.", "LAKUKAN"),
    kode('''def rp(x):
    return "Rp " + f"{int(x):,}".replace(",", ".")

k1, k2, k3 = st.columns(3)
k1.metric("Nota", len(df))
k2.metric("Omzet", rp(df["jumlah"].sum()))
k3.metric("Rata-rata per nota", rp(df["jumlah"].mean()))'''),
    blok("hasil", kode("""Nota                Omzet                    Rata-rata per nota
400                 Rp 224.907.000           Rp 562.267""", salin=False), "HARUS MUNCUL"),
    "<p><code>st.columns(3)</code> membagi lebar halaman jadi tiga, dan tiap kolom punya perintah "
    "gambarnya sendiri. Fungsi <code>rp()</code> yang sama dari Hari 73 dipakai lagi di sini — "
    "itulah gunanya menulisnya sebagai fungsi.</p>")

langkah("Pasang satu filter, dan lihat semuanya ikut berubah",
    blok("aksi", "Sisipkan dua baris ini <em>sesudah</em> <code>df = pd.read_csv(...)</code>, lalu "
                 "ganti setiap <code>df</code> di bagian metrik dan tabel menjadi <code>f</code>.", "LAKUKAN"),
    kode('pilih = st.sidebar.selectbox("Produk", ["(semua)"] + sorted(df["produk"].unique()))\nf = df if pilih == "(semua)" else df[df["produk"] == pilih]'),
    blok("aksi", "Simpan. Di panel kiri muncul kotak pilihan. Pilih <strong>Pasir m3</strong>.", "LAKUKAN"),
    blok("hasil", kode("""Nota                Omzet                    Rata-rata per nota
78                  Rp 86.720.000            Rp 1.111.794""", salin=False), "HARUS MUNCUL"),
    "<p><strong>Tiga angka dan seluruh tabel berubah, dan kamu tidak menulis satu baris pun untuk "
    "menghubungkannya.</strong> Inilah satu-satunya hal ajaib di Streamlit, dan langkah berikutnya "
    "menjelaskan bagaimana ia melakukannya.</p>",
    blok("catatan", "<strong>Kalau panel kirinya tidak terlihat:</strong> ada tanda panah kecil di "
                    "pojok kiri atas untuk membukanya. Di layar HP, panel itu memang tertutup "
                    "secara bawaan."))

langkah("Pahami satu-satunya hal yang harus kamu percaya tentang Streamlit",
    blok("aksi", "Baca kalimat ini pelan-pelan, lalu buktikan sendiri di langkah berikutnya.", "LAKUKAN"),
    blok("bahaya", "<strong>Setiap kali kamu menyentuh apa pun di halaman, Streamlit menjalankan "
                   "ulang seluruh <code>app.py</code> dari baris pertama sampai terakhir.</strong> "
                   "Bukan sebagian. Semuanya."),
    "<p>Itu sebabnya filtermu bekerja tanpa kode penghubung: variabel <code>pilih</code> berisi nilai "
    "baru, dan semua baris di bawahnya dihitung ulang dengan nilai itu. Sederhana, dan mahal.</p>",
    "<p>Mahal, karena <code>pd.read_csv</code> juga ikut dijalankan ulang setiap kali. Untuk 400 "
    "baris tidak terasa. Untuk 5 juta baris atau satu query ke gudang data, aplikasimu jadi tidak "
    "bisa dipakai.</p>")

langkah("Buktikan sendiri berapa kali datanya dibaca ulang",
    blok("aksi", "Ganti baris <code>pd.read_csv</code> jadi fungsi berikut, jalankan, lalu "
                 "<strong>ganti pilihan produk tiga kali</strong> sambil melihat terminalmu.", "LAKUKAN"),
    kode('''def muat():
    print(">>> MEMUAT DATA DARI CSV")
    return pd.read_csv("data-contoh/penjualan.csv", parse_dates=["tanggal"])

df = muat()'''),
    blok("hasil", kode(""">>> MEMUAT DATA DARI CSV
>>> MEMUAT DATA DARI CSV
>>> MEMUAT DATA DARI CSV
>>> MEMUAT DATA DARI CSV""", salin=False), "HARUS MUNCUL"),
    "<p><strong>Empat kali:</strong> sekali saat halaman dibuka, lalu sekali untuk tiap kali kamu "
    "mengganti pilihan. Bukan tebakan — hitung sendiri baris di terminalmu.</p>")

langkah("Pasang satu baris yang menghentikannya",
    blok("aksi", "Tambahkan satu baris <code>@st.cache_data</code> tepat di atas "
                 "<code>def muat():</code>. Jalankan ulang dari awal (Ctrl+C lalu "
                 "<code>streamlit run app.py</code>), dan ganti produk tiga kali lagi.", "LAKUKAN"),
    kode('@st.cache_data\ndef muat():\n    print(">>> MEMUAT DATA DARI CSV")\n    return pd.read_csv("data-contoh/penjualan.csv", parse_dates=["tanggal"])'),
    blok("hasil", kode(">>> MEMUAT DATA DARI CSV", salin=False), "HARUS MUNCUL"),
    "<p><strong>Satu baris, bukan empat.</strong> Streamlit menyimpan hasil fungsi itu dan memakainya "
    "kembali. Skripnya tetap dijalankan ulang seluruhnya — yang dilewati cuma isi fungsi yang "
    "ditandai.</p>",
    blok("catatan", "<strong>Kapan hasilnya dihitung ulang:</strong> kalau kode di dalam fungsinya "
                    "berubah, atau kalau argumennya berbeda. Jadi kalau kamu mengubah isi CSV-nya "
                    "tanpa mengubah kodenya, aplikasinya masih menampilkan data lama — tekan tombol "
                    "<em>Clear cache</em> di menu tiga titik pojok kanan atas."))

langkah("Tambahkan grafik",
    blok("aksi", "Sisipkan tiga baris ini sebelum <code>st.dataframe(f)</code>.", "LAKUKAN"),
    kode('''f = f.copy()
f["bulan"] = f["tanggal"].dt.strftime("%Y-%m")
st.bar_chart(f.groupby("bulan")["jumlah"].sum())'''),
    blok("hasil", "<p>Grafik batang enam bulan yang ikut berubah saat filter diganti. Sumbu kirinya "
                  "menampilkan <code>5,000,000</code> sampai <code>45,000,000</code>.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Perhatikan koma di sumbu grafiknya.</strong> Streamlit memformat angka "
                    "dengan gaya Inggris, dan itu tidak mengikuti fungsi <code>rp()</code>-mu. Untuk "
                    "laporan berbahasa Indonesia yang serius, ini harus diatur terpisah — atau "
                    "angkanya dibuat dalam satuan juta supaya tidak membingungkan."),
    """<details>
          <summary>Kenapa <code>f.copy()</code> perlu?</summary>
          <div class="isi">
            <p>Karena <code>f</code> adalah potongan dari <code>df</code>, dan menambahkan kolom
            langsung ke potongan membuat pandas mengeluarkan
            <code>SettingWithCopyWarning</code> — peringatan yang berarti "aku tidak yakin kamu
            sedang mengubah yang mana". <code>.copy()</code> membuat salinan mandiri sehingga
            tidak ada keraguan.</p>
          </div>
        </details>""")

langkah("Terbitkan gratis",
    blok("aksi", "Pastikan <code>app.py</code>, <code>requirements.txt</code>, dan folder "
                 "<code>data-contoh/</code> sudah ter-push ke GitHub. Lalu buka "
                 "<strong>share.streamlit.io</strong>, masuk dengan akun GitHub, klik "
                 "<strong>New app</strong>, pilih repositori dan berkas <code>app.py</code>.", "LAKUKAN"),
    kode("streamlit\npandas"),
    "<p>Isi <code>requirements.txt</code>-mu minimal harus memuat dua baris itu — server "
    "Streamlit Cloud memasang persis apa yang tertulis di sana, dan tidak tahu apa pun tentang "
    "komputermu.</p>",
    blok("hasil", "<p>Dalam 2–5 menit muncul tautan permanen berbentuk "
                  "<code>https://[nama-app].streamlit.app</code> yang bisa dibuka siapa pun, "
                  "termasuk dari HP.</p>", "YANG HARUS TERLIHAT"),
    blok("bahaya", "<strong>Aplikasi ini publik.</strong> Siapa pun yang punya tautannya bisa "
                   "melihat seluruh isi datanya. Yang kamu terbitkan harus data contoh atau data "
                   "terbuka — <em>tidak pernah</em> data klien, sekalipun namanya sudah kamu ganti. "
                   "Ini aturan yang sama dengan Bekal Rahasia Klien, dan di sini pelanggarannya "
                   "permanen: halaman yang pernah publik bisa sudah terindeks mesin pencari."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Buat aplikasi Streamlit baru dari nol, dengan berkas CSV lain "
                 "milikmu, tanpa melihat contoh ini.", "LAKUKAN"),
    """<p>Targetnya: judul, satu filter di panel kiri, dua angka <code>st.metric</code>,
        satu grafik, satu tabel, dan <code>@st.cache_data</code> di fungsi pemuat data.
        Enam hal, dan semuanya sudah kamu ketik hari ini.</p>""",
    """<details>
          <summary>Kalau macet di satu bagian</summary>
          <div class="isi">
            <p>Streamlit punya satu kebiasaan yang menolong: ketik <code>st.write(apa_saja)</code>
            dan ia akan mencari cara menampilkannya — DataFrame jadi tabel, angka jadi teks,
            grafik jadi grafik. Kalau kamu tidak tahu perintah yang tepat,
            <code>st.write</code> hampir selalu jalan.</p>
            <p>Dan pesan error Streamlit muncul <strong>di halaman webnya</strong>, bukan cuma di
            terminal — lengkap dengan nomor baris. Baca yang di browser dulu.</p>
          </div>
        </details>""")

HARI74 = {
  "n": "HARI 74",
  "tab": "74",
  "judul": "Dari notebook jadi aplikasi yang bisa dibuka dari HP",
  "waktu": "± 65 menit",
  "tujuan": "membangun aplikasi web berfilter hanya dengan Python, membuktikan sendiri kenapa "
            "Streamlit menjalankan ulang seluruh skripmu, dan menerbitkannya gratis.",
  "langkah": L,
  "tutup_judul": "Hari 74 selesai. Berhenti di sini.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> <code>streamlit run app.py</code>, bukan "
           "<code>python app.py</code> · setiap interaksi menjalankan ulang seluruh berkas · "
           "<code>@st.cache_data</code> di fungsi pemuat data · yang diterbitkan hanya data contoh.</p>"
           "<p style=\"margin-top:8px\">Empat hari terakhir menghasilkan satu hal yang bisa kamu "
           "kirim lewat WhatsApp: tautan yang hidup, isinya diperbarui sendiri tiap minggu oleh "
           "GitHub Actions.</p>",
}
