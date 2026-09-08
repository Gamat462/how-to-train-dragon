# -*- coding: utf-8 -*-
"""Hari 94 — merapikan profil GitHub. Keluaran git dijalankan sungguhan (git 2.43.0)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Lihat profilmu seperti orang asing melihatnya",
    blok("aksi", "Buka <code>github.com/[username-mu]</code> di jendela penyamaran "
                 "(<em>incognito</em>), supaya kamu melihatnya sebagai orang yang belum login. "
                 "Beri dirimu 30 detik, lalu tutup.", "LAKUKAN"),
    blok("hasil", "<p>Tuliskan apa yang kamu ingat. Biasanya: deretan nama repositori tanpa "
                  "keterangan, sebagian bernama <code>latihan-1</code> atau <code>tugas-sql</code>, "
                  "dan tidak ada satu kalimat pun yang menyebutkan siapa kamu.</p>",
         "YANG HARUS TERLIHAT"),
    "<p>Itulah yang dilihat perekrut. Sisa hari ini memperbaiki tepat itu — bukan kodemu, yang "
    "jarang dibaca.</p>")

langkah("Sematkan empat repositori, dan sembunyikan sisanya",
    blok("aksi", "Di halaman profilmu, klik <strong>Customize your pins</strong>. Pilih tepat "
                 "empat.", "LAKUKAN"),
    tabel(["Slot", "Isi", "Kenapa"],
          [["1", "capstone (Hari 92–93)", "proyek terdalammu, dibaca pertama"],
           ["2", "satu proyek SQL/pipeline murni", "membuktikan kemampuan teknis inti"],
           ["3", "satu dashboard dengan tautan hidup", "satu-satunya yang bisa diklik dan langsung terlihat"],
           ["4", "satu proyek beda jenis (ML/statistik)", "menunjukkan keluasan"]]),
    blok("bahaya", "<strong>Repositori latihan setengah jadi merugikanmu, bukan menambah.</strong> "
                   "Jadikan privat atau arsipkan. Sepuluh repo bagus di antara empat puluh repo "
                   "kosong terlihat seperti empat puluh repo kosong."))

langkah("Isi deskripsi dan topik tiap repo yang disematkan",
    blok("aksi", "Buka tiap repo tersemat → klik ikon gerigi di kanan atas → isi "
                 "<strong>Description</strong> dan <strong>Topics</strong>.", "LAKUKAN"),
    tabel(["Kolom", "Isi yang benar", "Contoh"],
          [["Description", "kalimat temuan, sama dengan judul README-mu",
            "Lokasi menentukan 61% harga HDB, dan menurun sejak 2020"],
           ["Topics", "tag alat, huruf kecil, dipisah spasi",
            "<code>sql python dbt bigquery streamlit</code>"]]),
    "<p>Tanpa deskripsi, kartu repo di halaman profilmu tampil kosong — meski isinya bagus. "
    "Topics juga membuat repomu muncul di pencarian GitHub berdasarkan alat.</p>")

langkah("Buat README profil",
    blok("aksi", "Buat repositori baru dengan nama <strong>persis sama</strong> dengan username "
                 "GitHub-mu, centang <em>Add a README file</em>.", "LAKUKAN"),
    kode("username: budiwijaya  ->  nama repo: budiwijaya"),
    blok("hasil", "<p>GitHub menampilkan kotak biru bertuliskan <em>\"You found a secret! "
                  "budiwijaya/budiwijaya is a special repository...\"</em> — itu tanda namanya "
                  "sudah tepat. Isi README-nya otomatis muncul di paling atas halaman profilmu.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Kalau kotak birunya tidak muncul,</strong> nama repomu tidak sama "
                    "persis dengan username — periksa huruf besar-kecil dan tanda hubung."))

langkah("Isi README profil dengan tiga hal saja",
    blok("aksi", "Ganti seluruh isi README profil dengan ini, sesuaikan.", "LAKUKAN"),
    kode("""### Budi Wijaya

Mantan auditor KAP, sekarang data analyst. SQL · Python · dbt · Tableau.
Sedang mencari posisi analis di Singapura.

- **[Harga HDB Singapura](https://github.com/budiwijaya/hdb)** — lokasi menentukan 61% harga, dan menurun sejak 2020
- **[Retensi kedai kopi](https://github.com/budiwijaya/kopi)** — retensi bulan-1 42%, kohor Desember cuma 13%
- **[Prediksi churn](https://github.com/budiwijaya/churn)** — tiga sinyal memprediksi 71% pelanggan yang berhenti

budi.wijaya@email.com · [LinkedIn](https://linkedin.com/in/budiwijaya)"""),
    "<p>Tiga hal: <strong>siapa kamu, apa yang kamu cari, tiga proyek terbaik dengan temuannya.</strong> "
    "Tidak ada ikon animasi, tidak ada grafik statistik GitHub, tidak ada daftar bahasa pemrograman "
    "berbentuk lencana warna-warni.</p>",
    blok("catatan", "<strong>Kenapa tanpa hiasan:</strong> lencana dan animasi memenuhi layar "
                    "pertama, dan mendorong turun satu-satunya bagian yang berguna — tautan ke "
                    "proyekmu beserta temuannya."))

langkah("Periksa riwayat commit capstone-mu",
    blok("aksi", "Buka folder capstone-mu di terminal. Dua perintah.", "LAKUKAN"),
    kode('git rev-list --count HEAD\ngit log --pretty="%h %s" --shortstat'),
    blok("hasil", kode("""1
d6e65dd upload project
 9 files changed, 9 insertions(+)""", salin=False), "KALAU RIWAYATMU BURUK"),
    "<p><strong>Satu commit berisi seluruh proyek.</strong> Itu bukan riwayat kerja, itu unggahan. "
    "Perekrut yang membuka tab <em>Commits</em> melihat satu baris bertuliskan "
    "<code>upload project</code>, dan tidak ada yang bisa disimpulkan darinya.</p>",
    blok("hasil", kode("""4
73f04d3 Tambah bagian batasan ke README
 1 file changed, 6 insertions(+)
cfbede8 Samakan tiga versi penulisan nama estate
 2 files changed, 4 insertions(+)
02ee8aa Muat data mentah dari CSV
 1 file changed, 1 insertion(+)
7da015c Kerangka proyek dan README awal
 1 file changed, 1 insertion(+)""", salin=False), "YANG SEHARUSNYA"),
    blok("catatan", "<strong>Tujuh huruf-angka di kiri pasti beda di layarmu</strong> — itu sidik "
                    "jari commit, dihitung dari isi, waktu, dan namamu. Yang penting bentuknya: "
                    "beberapa commit, masing-masing menyentuh sedikit berkas, dengan pesan yang "
                    "menyebutkan satu perubahan."),
    "<p>Riwayat yang bertahap menunjukkan <strong>urutan berpikirmu</strong>. Itu satu-satunya "
    "bagian portofolio yang tidak bisa dipalsukan belakangan.</p>")

langkah("Kalau capstone-mu belum selesai, ini justru kesempatan",
    blok("aksi", "Capstone-mu memang belum selesai (Hari 92 memberi 3–5 hari). Sisa pekerjaannya "
                 "kerjakan dengan alur git Minggu 11 Hari 71: satu cabang per perubahan, pesan "
                 "commit yang menjelaskan <em>kenapa</em>.", "LAKUKAN"),
    kode('git switch -c bersihkan-nama-estate\n# kerjakan\ngit commit -m "Samakan tiga versi penulisan nama estate" \\\n  -m "ANG MO KIO / Ang Mo Kio / AMK sebelumnya terhitung tiga wilayah berbeda."'),
    blok("catatan", "<strong>Jangan memalsukan riwayat.</strong> Memecah satu commit besar jadi "
                    "sepuluh commit palsu bertanggal sama akan terlihat, dan itu jauh lebih buruk "
                    "daripada satu commit jujur. Yang bisa kamu perbaiki adalah pekerjaan yang "
                    "<em>belum</em> kamu commit."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Buka profil GitHub-mu di jendela penyamaran lagi, 30 detik, "
                 "lalu tutup dan tulis apa yang kamu ingat.", "LAKUKAN"),
    "<p>Bandingkan dengan catatan yang kamu tulis di langkah 1. Kalau sekarang kamu bisa menyebut "
    "<strong>satu temuan berangka</strong> dari salah satu proyekmu, halamannya sudah bekerja.</p>",
    blok("catatan", "<strong>Kalau yang kamu ingat masih nama repositori, bukan temuan,</strong> "
                    "berarti deskripsi repomu masih menyebut alat, bukan hasil. Ganti."))

HARI94 = {
  "n": "HARI 94",
  "tab": "94",
  "judul": "Profil GitHub yang bisa dinilai dalam sekali pandang",
  "waktu": "± 50 menit",
  "tujuan": "profil yang menyebutkan temuan, bukan tumpukan repo latihan — dan riwayat commit "
            "yang terlihat seperti pekerjaan, bukan unggahan.",
  "langkah": L,
  "tutup_judul": "Hari 94 selesai.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> 4 repo tersemat, sisanya privat/arsip · "
           "deskripsi repo = kalimat temuan, bukan nama alat · README profil di repo bernama sama "
           "dengan username · commit bertahap, tidak dipalsukan.</p>",
}
