# -*- coding: utf-8 -*-
"""Hari 96 — LinkedIn."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Cari dirimu sendiri seperti perekrut mencarimu",
    blok("aksi", "Buka LinkedIn di jendela penyamaran. Di kotak pencarian ketik "
                 "<code>data analyst</code> dan saring lokasi ke kota tujuanmu. "
                 "Lihat bentuk hasilnya.", "LAKUKAN"),
    blok("hasil", "<p>Tiap hasil cuma menampilkan tiga hal: <strong>foto, nama, dan "
                  "headline</strong>. Jabatan sekarang, pengalaman, dan About tidak terlihat "
                  "sama sekali sampai kartunya diklik.</p>", "YANG HARUS TERLIHAT"),
    "<p>Itu sebabnya headline adalah satu-satunya bagian profil yang menentukan apakah kamu "
    "diklik. Sisa profilmu baru berguna <em>setelah</em> headline-nya bekerja.</p>")

langkah("Tulis headline dengan empat bagian",
    blok("aksi", "Klik pensil di bagian atas profilmu → kolom <strong>Headline</strong>. "
                 "Ganti isinya mengikuti pola ini.", "LAKUKAN"),
    kode("Ex-auditor turned Data Analyst | SQL · Python · dbt | Built a daily HDB price pipeline | Open to roles in Singapore", salin=False),
    tabel(["Bagian", "Isi", "Kenapa"],
          [["1", "jabatan yang kamu tuju", "kata yang diketik perekrut di kotak pencarian"],
           ["2", "tiga alat, bukan sepuluh", "sepuluh alat terbaca sebagai daftar hafalan"],
           ["3", "satu bukti konkret", "bagian yang hampir tidak pernah ada di headline orang lain"],
           ["4", "lokasi yang kamu tuju", "banyak perekrut menyaring lokasi lebih dulu"]]),
    blok("catatan", "<strong>Batas headline LinkedIn 220 karakter.</strong> Contoh di atas "
                    "115 karakter — masih separuh jatah. Yang lebih penting: bagian awalnya yang "
                    "terbaca di hasil pencarian, jadi taruh jabatan di paling depan."))

langkah("Periksa panjangnya sebelum menyimpan",
    blok("aksi", "Tempel headline-mu ke dalam perintah ini dan jalankan, sebelum "
                 "menyimpannya di LinkedIn.", "LAKUKAN"),
    kode('''python3 -c "h='Ex-auditor turned Data Analyst | SQL · Python · dbt | Built a daily HDB price pipeline | Open to roles in Singapore'; print(len(h), 'karakter')"'''),
    blok("hasil", kode("115 karakter", salin=False), "HARUS MUNCUL"),
    "<p>Di bawah 220 aman. Di atas itu LinkedIn memotongnya tanpa memberitahu, dan yang terpotong "
    "adalah bagian akhir — yaitu lokasi tujuanmu.</p>")

langkah("Setel lokasi",
    blok("aksi", "Klik pensil profil → gulung ke <strong>Location</strong>.", "LAKUKAN"),
    blok("bahaya", "<strong>Ini keputusan, bukan pengaturan.</strong> Menyetel lokasi ke kota "
                   "tujuan membuatmu muncul di pencarian perekrut di sana — tapi kalau kamu belum "
                   "punya izin kerja, itu harus dijelaskan, bukan disembunyikan."),
    "<p>Jalan tengah yang jujur: setel lokasi ke kota tujuan, dan tulis satu kalimat di About: "
    "<em>\"Currently in Jakarta, relocating to Singapore and open to sponsorship discussions.\"</em> "
    "Perekrut yang tidak bisa mensponsori akan berhenti di situ — dan itu menghemat waktu "
    "kalian berdua.</p>")

langkah("Tulis About dalam tiga paragraf",
    blok("aksi", "Klik <strong>Add profile section → About</strong>. Tiga paragraf, orang pertama, "
                 "bukan daftar kata kunci.", "LAKUKAN"),
    tabel(["Paragraf", "Isi", "Panjang"],
          [["1", "apa yang kamu kerjakan sekarang dan dari mana kamu datang", "2–3 kalimat"],
           ["2", "bukti terbaikmu — satu proyek, dengan angka", "2–3 kalimat"],
           ["3", "apa yang kamu cari, dan status relokasi", "1–2 kalimat"]]),
    blok("catatan", "<strong>Orang pertama, bukan orang ketiga.</strong> \"Saya membangun...\" "
                    "bukan \"Budi adalah seorang analis yang...\". Menulis tentang diri sendiri "
                    "sebagai orang ketiga terbaca janggal di LinkedIn dan hanya lazim di biografi "
                    "pembicara konferensi."))

langkah("Isi Featured — bagian yang paling sering diklik",
    blok("aksi", "<strong>Add profile section → Recommended → Add featured</strong>. Tambahkan "
                 "tautan dashboard capstone-mu dan satu repositori.", "LAKUKAN"),
    blok("hasil", "<p>Kotak besar bergambar muncul tepat di bawah About, dengan gambar pratinjau "
                  "dari halaman yang kamu tautkan.</p>", "YANG HARUS TERLIHAT"),
    "<p>Ini satu-satunya bagian profil LinkedIn yang punya <strong>gambar besar</strong>, dan "
    "gambar mengalahkan teks. Kalau cuma satu bagian yang sempat kamu isi hari ini, isi ini.</p>",
    blok("catatan", "<strong>Kalau gambar pratinjaunya tidak muncul,</strong> halaman yang kamu "
                    "tautkan tidak punya gambar pembuka. Untuk repositori GitHub, unggah "
                    "tangkapan layar dashboard sebagai gambar sosial repo di "
                    "Settings → Social preview."))

langkah("Unggah satu tulisan pendek",
    blok("aksi", "Buat satu unggahan tentang capstone-mu. Empat kalimat, bukan lebih.", "LAKUKAN"),
    kode("""Baru selesai menganalisis 240.000 transaksi rumah HDB Singapura 2017-2024.

Temuan yang paling mengejutkan saya: jarak ke MRT menjelaskan 61% ragam
harga sebelum 2020, tapi cuma 44% sesudahnya.

Yang paling sulit ternyata bukan analisisnya, tapi menyadari bahwa nama
estate ditulis tiga versi berbeda dan diam-diam terhitung tiga wilayah.

Dashboard-nya di sini: [tautan]""", salin=False),
    "<p>Polanya: <strong>apa yang dikerjakan → satu temuan berangka → satu hal yang sulit → "
    "tautan.</strong> Bagian ketiga yang membuatnya terbaca seperti orang, bukan seperti "
    "pengumuman.</p>",
    blok("catatan", "<strong>Satu unggahan tentang pekerjaanmu sendiri lebih berguna daripada "
                    "dua puluh kali membagikan artikel orang lain.</strong> Perekrut yang membuka "
                    "tab Aktivitasmu mencari bukti kamu mengerjakan sesuatu, bukan bukti kamu "
                    "membaca sesuatu."))

langkah("Uji profilmu pada manusia",
    blok("aksi", "Kirim tautan profilmu ke satu orang. Minta ia membacanya 60 detik, lalu tutup "
                 "dan sebutkan apa yang ia ingat.", "LAKUKAN"),
    tabel(["Yang ia sebut", "Artinya"],
          [["satu temuan berangka dari proyekmu", "profilmu bekerja"],
           ["daftar alat yang kamu kuasai", "headline-mu terlalu penuh alat, kurang bukti"],
           ["pekerjaan lamamu", "About-mu masih bercerita mundur, bukan maju"],
           ["\"kayaknya kamu cari kerja\"", "cukup, tapi belum ada alasan untuk menghubungimu"]]),
    "<p>Ini uji yang sama dengan README Hari 93, dan alasannya sama: kamu sudah terlalu terbiasa "
    "dengan tulisanmu sendiri untuk bisa menilainya.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Sebutkan empat bagian headline dan tiga paragraf About, "
                 "dengan suara keras.", "LAKUKAN"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>Headline:</strong> jabatan yang dituju · tiga alat · satu bukti konkret ·
            lokasi tujuan. Maksimal 220 karakter, bagian terpenting di depan.</p>
            <p><strong>About:</strong> (1) apa yang kamu kerjakan dan dari mana kamu datang,
            (2) bukti terbaik dengan angka, (3) apa yang kamu cari dan status relokasi.
            Orang pertama.</p>
          </div>
        </details>""")

HARI96 = {
  "n": "HARI 96",
  "tab": "96",
  "judul": "LinkedIn: yang menentukan cuma headline, sisanya menyusul",
  "waktu": "± 50 menit",
  "tujuan": "profil yang muncul di pencarian perekrut, dan meyakinkan begitu dibuka — diuji "
            "pada orang sungguhan, bukan diperkirakan sendiri.",
  "langkah": L,
  "tutup_judul": "Hari 96 selesai.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> hasil pencarian cuma menampilkan foto, nama, "
           "headline · headline = jabatan + 3 alat + 1 bukti + lokasi (≤220 karakter) · About "
           "3 paragraf orang pertama · Featured punya gambar besar, isi itu dulu · unggahan "
           "tentang pekerjaanmu &gt; membagikan artikel orang.</p>",
}
