# -*- coding: utf-8 -*-
"""Hari 77 — proyek portofolio #9 bagian 2, dan penutup Minggu 11."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Sambungkan dashboard ke mart, bukan ke CSV",
    blok("aksi", "Salin <code>app.py</code> dari Hari 74. Ganti bagian pemuat datanya jadi query ke "
                 "mart dbt-mu.", "LAKUKAN"),
    kode('''@st.cache_data(ttl=3600)
def muat():
    return pd.read_gbq("SELECT * FROM `proyekmu.marts.penjualan_bulanan`")'''),
    blok("hasil", "<p>Dashboard yang sama persis seperti Hari 74, tapi angkanya datang dari gudang "
                  "data yang diperbarui sendiri tiap pagi.</p>", "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong><code>ttl=3600</code> itu tambahan penting.</strong> Tanpa itu, "
                    "cache-nya tidak pernah kedaluwarsa dan dashboard-mu menampilkan angka kemarin "
                    "selamanya — meskipun pipeline-mu sudah memperbaruinya. Satu jam adalah "
                    "kompromi yang wajar untuk data harian."))

langkah("Terbitkan, lalu buka dari HP",
    blok("aksi", "Terbitkan ke Streamlit Community Cloud (pola Hari 74). Lalu ambil HP-mu, matikan "
                 "wifi, dan buka tautannya lewat data seluler.", "LAKUKAN"),
    blok("hasil", "<p>Dashboard terbuka dan bisa dipakai di layar kecil.</p>", "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Mematikan wifi itu bukan lelucon.</strong> Itu cara tercepat memastikan "
                    "kamu tidak sedang melihat versi yang jalan di komputermu sendiri. Dan perekrut "
                    "yang membuka tautanmu <em>akan</em> membukanya dari HP."))

langkah("Tulis README yang menjual",
    blok("aksi", "Susun README-mu dengan enam bagian ini, urutannya persis seperti ini.", "LAKUKAN"),
    tabel(["Urutan", "Bagian", "Kenapa di posisi itu"],
          [["1", "Lencana status", "bukti pertama yang terlihat tanpa membaca"],
           ["2", "Satu kalimat: sistem ini melakukan apa", "pembaca memutuskan lanjut atau tidak di sini"],
           ["3", "Tautan hidup ke dashboard", "sebelum ada alasan untuk berhenti membaca"],
           ["4", "Diagram alur empat kotak", "arsitektur dalam satu pandangan"],
           ["5", "Tangkapan layar lineage graph dbt", "bukti transformasinya berlapis, bukan satu query"],
           ["6", "Keputusan desain — 3–4 kalimat", "bagian yang membedakanmu dari pelamar lain"]]),
    blok("bahaya", "<strong>Tautan hidup harus di paruh atas.</strong> Orang yang membuka repositorimu "
                   "memberimu sekitar dua puluh detik. Kalau tautan dashboard-nya ada di bawah "
                   "setelah lima paragraf instalasi, ia tidak akan pernah diklik."))

langkah("Tulis bagian yang paling jarang ada di portofolio orang",
    blok("aksi", "Tulis bagian <strong>Keputusan desain</strong>. Tiga sampai empat kalimat, "
                 "menjawab \"kenapa begini\" bukan \"apa ini\".", "LAKUKAN"),
    """<p>Contoh bentuk yang baik — tirulah polanya, bukan isinya:</p>""",
    kode("""## Keputusan desain

Dua mart, bukan satu: satu menjawab pertanyaan waktu (omzet per bulan),
satu menjawab pertanyaan produk. Menggabungkannya memaksa dashboard
mengagregasi ulang tiap kali filter diganti.

Jadwal harian, bukan tiap jam: datanya sendiri hanya diperbarui harian,
jadi menjalankan lebih sering hanya membakar kuota tanpa menambah apa pun.

Retur dihitung sebagai nilai negatif, bukan dibuang, supaya omzet bersih
di dashboard bisa dicocokkan langsung ke total di sistem sumber.""", salin=False),
    "<p><strong>Perhatikan bahwa tiap kalimat menyebut alternatif yang tidak dipilih.</strong> "
    "Itu yang membedakan \"saya membuat dua mart\" dari \"saya memutuskan dua mart\". Yang pertama "
    "laporan pekerjaan; yang kedua bukti cara berpikir.</p>")

langkah("Periksa dengan daftar tutup",
    blok("aksi", "Enam baris. Centang satu per satu, dan jangan mencentang yang belum kamu "
                 "buktikan sendiri.", "LAKUKAN"),
    """<ol>
          <li><code>dbt build</code> hijau dari clone bersih di folder baru</li>
          <li>Minimal 10 test, termasuk satu rekonsiliasi mart lawan angka kontrol sumber</li>
          <li>GitHub Actions berjalan terjadwal, lencana hijau di README</li>
          <li>Dashboard hidup, dibuka dari HP dengan wifi mati</li>
          <li>Tidak ada satu pun kredensial di repositori — <strong>periksa seluruh riwayat</strong>,
          bukan hanya kondisi terakhir</li>
          <li>Kamu bisa menjelaskan tiap keputusan desain selama 5 menit tanpa membuka kode</li>
        </ol>""",
    "<p>Untuk baris kelima, jangan mengandalkan ingatan:</p>",
    kode('git log -p --all | grep -iE "password|api_key|secret|BEGIN PRIVATE KEY"'),
    blok("hasil", "<p>Tidak ada satu baris pun keluaran. Kalau ada, kunci itu harus diganti "
                  "hari ini juga — bukan dihapus.</p>", "HARUS MUNCUL"))

langkah("Latih menjelaskannya dalam 90 detik",
    blok("aksi", "Nyalakan perekam suara di HP-mu. Jawab pertanyaan ini dengan suara keras, "
                 "sekali jalan, tanpa berhenti. Lalu dengarkan rekamannya.", "LAKUKAN"),
    blok("catatan", "<em>\"Ceritakan satu proyek yang paling kamu banggakan.\"</em>"),
    tabel(["Detik", "Isi", "Contoh pembuka"],
          [["0–15", "konteks: data apa, pertanyaan apa", "\"Data harga rumah second Singapura, ratusan ribu baris…\""],
           ["15–45", "arsitektur empat lapis", "\"Sumbernya masuk BigQuery, dbt menyusunnya tiga lapis…\""],
           ["45–70", "<strong>satu</strong> keputusan teknis yang kamu timbang", "\"Saya sempat menggabungkan jadi satu mart, tapi…\""],
           ["70–90", "hasil dan apa yang berjalan sendiri", "\"Sekarang ia memperbarui dirinya tiap pagi, tautannya…\""]]),
    blok("bahaya", "<strong>Dengarkan rekamanmu sendiri. Ini bagian yang tidak enak dan paling "
                   "berguna.</strong> Yang biasanya terdengar: terlalu lama di bagian konteks, "
                   "dan bagian keputusan teknis dilewati sama sekali — padahal itu satu-satunya "
                   "bagian yang tidak bisa ditiru pelamar lain."))

langkah("Ulangi sampai tidak perlu catatan",
    blok("aksi", "Rekam ulang dua kali lagi, tanpa membaca tabel di atas.", "LAKUKAN"),
    "<p>Target: rekaman ketiga terdengar seperti bercerita, bukan menghafal. Kalau masih terdengar "
    "seperti membaca daftar, biasanya penyebabnya bukan kurang latihan — tapi kamu belum benar-benar "
    "memutuskan keputusan teknis mana yang mau kamu ceritakan.</p>",
    blok("catatan", "<strong>Pilih satu, bukan tiga.</strong> Satu keputusan yang kamu ceritakan "
                    "lengkap dengan alternatif yang kamu tolak jauh lebih kuat daripada tiga "
                    "keputusan yang disebut sambil lalu."))

HARI77 = {
  "n": "HARI 77",
  "tab": "77",
  "judul": "Proyek #9 bagian 2: dashboard publik dan cara menceritakannya",
  "waktu": "± 65 menit",
  "tujuan": "menyelesaikan proyek kesembilan — pipeline sampai dashboard, semuanya berjalan sendiri — "
            "dan bisa menjelaskannya dalam 90 detik tanpa membuka kode.",
  "langkah": L,
  "tutup_judul": "Sebelas minggu selesai — dari satu query ke satu sistem",
  "tutup": "<p>Sembilan proyek publik di GitHub-mu, termasuk satu sistem menyeluruh yang berjalan "
           "tanpa kamu sentuh. Kombinasi SQL + Python + statistik + visualisasi + "
           "<em>analytics engineering</em> ini menutup hampir seluruh syarat teknis posisi "
           "<em>data analyst</em> di Singapura dan Australia — termasuk beberapa yang biasanya baru "
           "dikuasai di posisi <em>analytics engineer</em>.</p>"
           "<p style=\"margin-top:10px\"><strong>Yang membuat proyek ini bernilai:</strong> hampir "
           "semua pelamar posisi analis punya notebook berisi analisis. Sangat sedikit yang bisa "
           "menunjukkan data yang bertransformasi sendiri, menguji dirinya sendiri, dan menyajikan "
           "hasilnya lewat tautan yang hidup saat itu juga.</p>"
           "<p style=\"margin-top:10px\">Minggu depan: <em>Product &amp; Business Analytics</em> — "
           "cohort, retensi, LTV/CAC, dan peramalan. Bagian di mana kamu berhenti jadi orang yang "
           "menjalankan query, dan mulai jadi orang yang menjawab pertanyaan bisnis.</p>",
}
