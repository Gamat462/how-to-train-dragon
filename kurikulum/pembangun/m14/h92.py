# -*- coding: utf-8 -*-
"""Hari 92 — memilih dan merencanakan capstone."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buat berkas rencananya lebih dulu, sebelum berpikir",
    blok("aksi", "Buat folder <code>capstone/</code> dan satu berkas kosong di dalamnya. "
                 "Rencana yang cuma di kepala tidak pernah selesai.", "LAKUKAN"),
    kode("mkdir -p capstone && cd capstone\ntouch RENCANA.md"),
    blok("hasil", "<p>Satu berkas kosong bernama <code>RENCANA.md</code>. Sisa hari ini kamu "
                  "mengisinya, dan di akhir kamu memeriksanya dengan perintah.</p>", "HARUS MUNCUL"))

langkah("Daftar proyek yang sudah kamu punya",
    blok("aksi", "Tulis di <code>RENCANA.md</code> daftar proyek Minggu 6–13 milikmu, satu baris "
                 "per proyek, dengan format: nama · data apa · berapa baris.", "LAKUKAN"),
    kode("## Kandidat\n- Dashboard kedai kopi · transaksi POS · 151.088 baris\n- Pipeline dbt HDB · data.gov.sg · 240.000 baris\n- Model churn · data langganan · 8.000 baris"),
    "<p>Capstone bukan proyek baru dari nol. Ia salah satu proyek yang sudah ada, "
    "<strong>diperdalam sampai selesai betul</strong>. Membuat yang baru dari nol adalah cara "
    "tercepat untuk punya dua belas proyek setengah jadi.</p>")

langkah("Coret yang tidak lolos syarat pertama: datanya harus berantakan",
    blok("aksi", "Untuk tiap kandidat, jawab satu pertanyaan: <em>apakah ada bagian membersihkan "
                 "data yang sungguhan?</em> Coret yang jawabannya tidak.", "LAKUKAN"),
    blok("bahaya", "<strong>Dataset kompetisi yang sudah bersih adalah jebakan.</strong> Titanic, "
                   "Iris, dan sejenisnya menunjukkan kamu bisa menjalankan kode — bukan bahwa kamu "
                   "bisa bekerja. Bagian yang paling dinilai perekrut justru bagian yang paling "
                   "tidak menyenangkan: apa yang rusak di data itu dan apa keputusanmu."),
    "<p>Kalau semua kandidatmu bersih, ambil satu dan <strong>rusakkan sumbernya</strong> — pakai "
    "data mentah aslinya, bukan versi yang sudah kamu bersihkan minggu lalu.</p>")

langkah("Syarat kedua: judulnya harus bisa berbentuk temuan",
    blok("aksi", "Untuk tiap kandidat yang tersisa, coba tulis satu judul yang berisi "
                 "<strong>angka</strong>. Kalau kamu tidak bisa, proyeknya belum cukup dalam.", "LAKUKAN"),
    tabel(["Judul lemah", "Judul yang lolos"],
          [["Analisis Data HDB", "Lokasi menentukan 61% harga HDB — dan menurun sejak 2020"],
           ["Dashboard Penjualan Kedai Kopi", "Retensi bulan pertama 42%, tapi kohor Desember cuma 13%"],
           ["Prediksi Churn Pelanggan", "Tiga sinyal memprediksi 71% pelanggan yang berhenti"]]),
    "<p>Perhatikan yang berubah: kolom kiri menyebut <em>apa yang kamu kerjakan</em>, kolom kanan "
    "menyebut <em>apa yang kamu temukan</em>. Yang kedua tidak bisa ditulis kalau analisisnya "
    "belum selesai — itulah gunanya syarat ini.</p>")

langkah("Syarat ketiga: relevan dengan pasar tujuanmu",
    blok("aksi", "Tulis di <code>RENCANA.md</code>: negara tujuanmu, dan sumber data terbuka "
                 "negara itu yang bisa kamu pakai.", "LAKUKAN"),
    tabel(["Tujuan", "Sumber", "Contoh dataset"],
          [["Singapura", "<code>data.gov.sg</code>", "Resale Flat Prices — ratusan ribu baris, ada dimensi waktu dan lokasi"],
           ["Singapura", "LTA DataMall", "data transportasi, diperbarui berkala"],
           ["Australia", "<code>data.gov.au</code> / ABS", "sensus, ekonomi, kesehatan"]]),
    blok("catatan", "<strong>Kenapa ini bukan sekadar gaya-gayaan:</strong> perekrut di Singapura "
                    "mengenali \"Resale Flat Prices\" tanpa perlu kamu jelaskan. Itu memotong "
                    "separuh usaha menjelaskan proyekmu, dan sisa waktunya bisa dipakai membahas "
                    "temuanmu."))

langkah("Tulis enam bagian susunannya",
    blok("aksi", "Salin kerangka ini ke <code>RENCANA.md</code>, lalu isi tiap baris dengan satu "
                 "kalimat konkret.", "LAKUKAN"),
    kode("""## Susunan
1. Pertanyaan bisnis  :
2. Data & pembersihan :
3. Pipeline           :
4. Analisis berlapis  :
5. Hasil yang diklik  :
6. Temuan & batasan   :"""),
    tabel(["Bagian", "Yang harus ada", "Kenapa"],
          [["1", "satu kalimat, berbentuk pertanyaan", "kalau butuh dua kalimat, pertanyaanmu belum tajam"],
           ["2", "dari mana, berapa baris, apa yang rusak, keputusanmu", "bagian yang paling sering dilewati orang lain"],
           ["3", "dbt + penjadwalan kalau relevan", "membedakan analis dari orang yang menjalankan notebook"],
           ["4", "deskriptif → perbandingan → model/uji", "menunjukkan kedalaman, bukan sekadar grafik"],
           ["5", "tautan hidup, bukan tangkapan layar", "perekrut mengklik tautan, jarang menjalankan notebook"],
           ["6", "lima temuan berangka, tiga rekomendasi, satu batasan", "batasan adalah bagian yang paling membedakan"]]))

langkah("Tulis bagian batasan sekarang, bukan nanti",
    blok("aksi", "Tulis satu paragraf batasan di <code>RENCANA.md</code> — sekarang, sebelum "
                 "analisisnya dikerjakan.", "LAKUKAN"),
    kode("""## Batasan
Analisis ini korelasional, bukan sebab-akibat: tidak ada eksperimen, dan
faktor yang tidak saya ukur bisa menjelaskan sebagian pola yang saya temukan.""", salin=False),
    blok("catatan", "<strong>Ini senjata rahasianya.</strong> Hampir tidak ada pelamar junior yang "
                    "menuliskannya. Menuliskannya di awal juga menjaga analisismu jujur — kamu "
                    "sudah menyatakan apa yang tidak bisa kamu buktikan sebelum tergoda "
                    "membuktikannya."),
    "<p>Ini kelanjutan langsung dari Minggu 5 Hari 32: korelasi bukan sebab-akibat. Bedanya, di "
    "sini kamu menuliskannya di tempat yang dibaca orang.</p>")

langkah("Periksa rencanamu dengan perintah, bukan perasaan",
    blok("aksi", "Dua baris. Yang pertama menghitung apakah keenam bagian ada, yang kedua mencari "
                 "bagian yang masih kosong.", "LAKUKAN"),
    kode('grep -cE "^[1-6]\\. " RENCANA.md\ngrep -n ":$" RENCANA.md'),
    blok("hasil", kode("6", salin=False), "HARUS MUNCUL"),
    "<p>Angka <strong>6</strong>, lalu <strong>tidak ada apa-apa lagi</strong>. Perintah kedua "
    "mencari baris yang berakhir dengan titik dua — artinya bagian yang kamu salin tapi belum "
    "kamu isi.</p>",
    "<p>Kalau rencanamu belum lengkap, yang muncul seperti ini — dan tiap baris menyebut nomor "
    "barisnya:</p>",
    blok("hasil", kode("""3:2. Data & pembersihan :
4:3. Pipeline           :
6:5. Hasil yang diklik  :""", salin=False), "KALAU BELUM SELESAI"),
    blok("catatan", "<strong>Beri dirimu 3–5 hari kerja untuk capstone-nya,</strong> dicicil di sela "
                    "Hari 93–98. Hari-hari berikutnya sengaja tidak menuntut capstone selesai — "
                    "yang dituntut cuma rencananya ada."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Sebutkan tiga syarat proyek capstone dan enam bagian "
                 "susunannya, dengan suara keras.", "LAKUKAN"),
    """<details>
          <summary>Kunci</summary>
          <div class="isi">
            <p><strong>Tiga syarat:</strong> data nyata dan berantakan · pertanyaan bisnis yang
            bisa dijadikan judul berangka · relevan dengan pasar tujuan.</p>
            <p><strong>Enam bagian:</strong> pertanyaan bisnis · data &amp; pembersihan ·
            pipeline · analisis berlapis · hasil yang bisa diklik · temuan &amp; batasan.</p>
          </div>
        </details>""")

HARI92 = {
  "n": "HARI 92",
  "tab": "92",
  "judul": "Memilih capstone: satu proyek dalam mengalahkan lima yang dangkal",
  "waktu": "± 60 menit perencanaan (+ 3–5 hari kerja dicicil)",
  "tujuan": "punya berkas rencana konkret untuk satu proyek yang cukup dalam untuk dibicarakan "
            "30 menit di wawancara, dan cukup jelas untuk dimengerti dalam 30 detik oleh perekrut.",
  "langkah": L,
  "tutup_judul": "Hari 92 selesai. Berhenti di sini — mulai kerjakan capstone-mu di sela hari berikutnya.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> tiga syarat (data berantakan · judul berangka · "
           "relevan pasar tujuan) · enam bagian susunan · bagian batasan ditulis di awal, bukan "
           "di akhir.</p>",
}
