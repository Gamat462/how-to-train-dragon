# -*- coding: utf-8 -*-
"""Hari 93 — README yang dibaca sampai habis. Keluaran periksa_readme.py diperoleh
dengan menjalankannya sungguhan pada dua berkas contoh."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Ambil pemeriksanya dulu",
    blok("aksi", "Dari paket zip, salin <code>data-dan-skrip/minggu-14/periksa_readme.py</code> "
                 "ke folder <code>capstone/</code>-mu. Jalankan tanpa argumen dulu.", "LAKUKAN"),
    kode("python periksa_readme.py"),
    blok("hasil", kode("pakai: python periksa_readme.py README.md", salin=False), "HARUS MUNCUL"),
    "<p>Skrip ini memeriksa sepuluh hal yang <strong>bisa dihitung</strong> — bukan selera. "
    "Sisa hari ini kamu menulis README sampai kesepuluhnya lolos.</p>")

langkah("Tulis README seburuk mungkin dulu, lalu ukur",
    blok("aksi", "Buat <code>README.md</code> berisi persis tiga baris ini. Ini bentuk README "
                 "yang paling sering dikirim pelamar.", "LAKUKAN"),
    kode("""# Analisis Data HDB

Proyek ini menganalisis data harga rumah di Singapura menggunakan Python,
pandas, dan matplotlib."""),
    blok("aksi", "Lalu jalankan pemeriksanya.", "LAKUKAN"),
    kode("python periksa_readme.py README.md"),
    blok("hasil", kode("""[OK ] ada judul H1             # Analisis Data HDB
[CEK] judul memuat angka       judul temuan biasanya berangka, mis. '61% harga ditentukan lokasi'
[CEK] judul bukan 'analisis X' judul yang dimulai 'Analisis ...' adalah nama dataset, bukan temuan
[CEK] tautan hidup             0 tautan http ditemukan
[CEK] tautan di paruh atas     tautan dashboard harus terlihat tanpa menggulung layar
[CEK] gambar                   0 gambar ditemukan
[CEK] temuan berangka          0 poin berangka (target 3)
[CEK] bagian Data              menjelaskan sumber, jumlah baris, apa yang rusak
[CEK] bagian Batasan           bagian yang hampir tidak pernah ditulis pelamar lain
[CEK] cara menjalankan         perintah yang benar-benar berhasil dijalankan orang lain

lolos 1 dari 10 pemeriksaan""", salin=False), "HARUS MUNCUL"),
    "<p><strong>1 dari 10.</strong> Dan README ini bukan karangan — ini bentuk yang benar-benar "
    "dikirim orang, termasuk orang yang analisisnya bagus.</p>")

langkah("Ganti judulnya jadi temuan",
    blok("aksi", "Ubah baris pertama <code>README.md</code>-mu jadi kalimat yang memuat angka, "
                 "lalu jalankan pemeriksanya lagi.", "LAKUKAN"),
    kode("# Lokasi menentukan 61% harga HDB — dan pengaruhnya menurun sejak 2020"),
    blok("hasil", kode("""[OK ] judul memuat angka       judul temuan biasanya berangka, mis. '61% harga ditentukan lokasi'
[OK ] judul bukan 'analisis X' judul yang dimulai 'Analisis ...' adalah nama dataset, bukan temuan""",
         salin=False), "HARUS MUNCUL"),
    "<p>Perhatikan apa yang berubah dari kedua judul itu. Yang lama menyebut <em>apa yang kamu "
    "kerjakan</em>. Yang baru menyebut <em>apa yang kamu temukan</em> — dan angka membuatnya bisa "
    "dipercaya.</p>",
    blok("catatan", "<strong>Judul yang dimulai dengan \"Analisis\" hampir selalu lemah,</strong> "
                    "karena semua orang menganalisis; yang membedakan adalah hasilnya. Pemeriksa "
                    "ini menolaknya secara otomatis."))

langkah("Taruh tautan hidup di paruh atas",
    blok("aksi", "Tambahkan dua baris ini tepat di bawah paragraf pembuka — bukan di bawah "
                 "halaman.", "LAKUKAN"),
    kode("**[Lihat dashboard →](https://contoh.streamlit.app)** · **[Baca notebook →](https://github.com/contoh/hdb)**\n\n![Tangkapan layar dashboard](gambar/dashboard.png)"),
    blok("hasil", kode("""[OK ] tautan hidup             2 tautan http ditemukan
[OK ] tautan di paruh atas     tautan dashboard harus terlihat tanpa menggulung layar
[OK ] gambar                   1 gambar ditemukan""", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Pemeriksa ini menuntut tautannya ada di 12 baris pertama.</strong> "
                   "Bukan tanpa alasan: perekrut memberimu 30–60 detik. Kalau tautan dashboard "
                   "berada di bawah lima paragraf instalasi, ia tidak akan pernah diklik."))

langkah("Tulis tiga temuan berangka",
    blok("aksi", "Tambahkan bagian <code>## Temuan</code> berisi tiga poin bernomor, "
                 "<strong>masing-masing memuat angka</strong>.", "LAKUKAN"),
    kode("""## Temuan

1. **Jarak ke MRT menjelaskan 61% ragam harga** pada 2017–2019, turun jadi 44% pada 2021–2024.
2. **Flat 4-kamar naik 38%** sepanjang periode, dibanding 22% untuk 3-kamar.
3. **Sisa sewa di bawah 60 tahun memotong harga rata-rata 18%**, makin tajam sejak 2021."""),
    blok("hasil", kode("[OK ] temuan berangka          3 poin berangka (target 3)", salin=False),
         "HARUS MUNCUL"),
    "<p>Pola tiap poin sama: <strong>angka + arah + periode</strong>. Poin tanpa angka bukan "
    "temuan, itu kesan.</p>")

langkah("Tulis bagian Data — yang paling sering dilewati",
    blok("aksi", "Tambahkan <code>## Data</code>: dari mana, berapa baris, rentang waktu, "
                 "<strong>apa yang rusak dan apa keputusanmu</strong>.", "LAKUKAN"),
    kode("""## Data

Sumber: data.gov.sg "Resale Flat Prices", 240.118 baris, Januari 2017 – Juni 2024.
Masalah yang ditemukan: nama estate ditulis tiga versi berbeda (ANG MO KIO,
Ang Mo Kio, AMK); 1.204 baris tanpa sisa masa sewa, dibuang setelah dicek
tidak terkonsentrasi di satu tahun."""),
    blok("hasil", kode("[OK ] bagian Data              menjelaskan sumber, jumlah baris, apa yang rusak",
                       salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalimat terakhir itu yang paling bernilai:</strong> \"dibuang setelah "
                    "dicek tidak terkonsentrasi di satu tahun\". Itu bukan pembersihan data, itu "
                    "<em>pertimbangan</em> — dan pertimbangan yang ditulis adalah satu-satunya "
                    "bukti bahwa kamu memikirkannya."))

langkah("Tulis cara menjalankan yang benar-benar berhasil",
    blok("aksi", "Tambahkan <code>## Menjalankan sendiri</code> dengan tiga baris perintah. Lalu "
                 "— dan ini bagian yang wajib — <strong>jalankan sendiri di folder kosong</strong>.", "LAKUKAN"),
    kode("""## Menjalankan sendiri

```
git clone https://github.com/[username]/[repo].git && cd [repo]
pip install -r requirements.txt
streamlit run app.py
```"""),
    blok("bahaya", "<strong>Perintah yang tidak pernah kamu uji dari folder kosong hampir selalu "
                   "salah.</strong> Yang paling sering: berkas yang lupa di-commit karena kena "
                   "<code>.gitignore</code>, dan pustaka yang terpasang di komputermu berbulan-bulan "
                   "lalu tapi tidak ada di <code>requirements.txt</code>. Perekrut yang mencobanya "
                   "dan gagal tidak akan mengirim pesan bertanya."))

langkah("Tulis batasan, lalu lolos sepuluh dari sepuluh",
    blok("aksi", "Tambahkan <code>## Batasan</code>, lalu jalankan pemeriksanya untuk terakhir "
                 "kali.", "LAKUKAN"),
    kode("""## Batasan

Analisis ini korelasional, bukan sebab-akibat: tidak ada eksperimen, dan faktor
yang tidak saya ukur (misalnya mutu sekolah di sekitar) bisa menjelaskan
sebagian pola yang saya temukan."""),
    blok("hasil", kode("""[OK ] ada judul H1             # Lokasi menentukan 61% harga HDB — dan pengaruhnya menurun 
[OK ] judul memuat angka       judul temuan biasanya berangka, mis. '61% harga ditentukan lokasi'
[OK ] judul bukan 'analisis X' judul yang dimulai 'Analisis ...' adalah nama dataset, bukan temuan
[OK ] tautan hidup             2 tautan http ditemukan
[OK ] tautan di paruh atas     tautan dashboard harus terlihat tanpa menggulung layar
[OK ] gambar                   1 gambar ditemukan
[OK ] temuan berangka          3 poin berangka (target 3)
[OK ] bagian Data              menjelaskan sumber, jumlah baris, apa yang rusak
[OK ] bagian Batasan           bagian yang hampir tidak pernah ditulis pelamar lain
[OK ] cara menjalankan         perintah yang benar-benar berhasil dijalankan orang lain

lolos 10 dari 10 pemeriksaan""", salin=False), "HARUS MUNCUL"),
    "<p>Dari <strong>1 dari 10</strong> jadi <strong>10 dari 10</strong>, dan kamu bisa melihat "
    "tiap langkah yang membuatnya berubah.</p>")

langkah("Uji yang tidak bisa dilakukan skrip",
    blok("aksi", "Minta seseorang yang <strong>bukan orang data</strong> membaca README-mu selama "
                 "60 detik. Lalu tutup layarnya dan tanya: apa isinya?", "LAKUKAN"),
    blok("bahaya", "<strong>Kalau dia tidak bisa menyebutkan satu temuan pun, README-mu belum "
                   "selesai</strong> — meski lolos 10 dari 10. Skrip cuma bisa memeriksa apakah "
                   "bagiannya ada; ia tidak bisa memeriksa apakah kalimatmu bisa dimengerti."),
    "<p>Dua pemeriksaan ini saling melengkapi, dan keduanya perlu. Skripnya menangkap yang "
    "terlewat; manusianya menangkap yang tidak terbaca.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Sebutkan urutan enam bagian README dan alasan tiap bagian "
                 "ada di posisi itu.", "LAKUKAN"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p>Judul temuan berangka → paragraf pertanyaan bisnis → tautan hidup → gambar →
            Temuan → Data → Cara kerja → Menjalankan sendiri → Batasan.</p>
            <p>Alasannya satu: <strong>urutannya mengikuti perhatian pembaca yang menurun</strong>.
            Yang paling meyakinkan ditaruh di tempat yang pasti terbaca; yang butuh niat
            (cara instalasi) ditaruh di bawah.</p>
          </div>
        </details>""")

HARI93 = {
  "n": "HARI 93",
  "tab": "93",
  "judul": "README yang dinilai 60 detik — dan skrip yang mengukurnya",
  "waktu": "± 55 menit",
  "tujuan": "menulis README yang lolos sepuluh pemeriksaan terukur, lalu mengujinya pada orang "
            "yang belum pernah mendengar namamu.",
  "langkah": L,
  "tutup_judul": "Hari 93 selesai.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> judul = temuan berangka, bukan nama dataset · "
           "tautan hidup di 12 baris pertama · bagian Data menyebut apa yang rusak dan keputusanmu · "
           "Batasan selalu ada · uji dengan orang non-data, 60 detik.</p>"
           "<p style=\"margin-top:8px\">Simpan <code>periksa_readme.py</code>. Jalankan lagi tiap "
           "kali kamu menyelesaikan proyek baru — sepuluh detik, dan menangkap hal yang kamu "
           "lupakan setiap kali.</p>",
}
