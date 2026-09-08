# -*- coding: utf-8 -*-
"""Hari 76 — proyek portofolio #9 bagian 1."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Lihat bentuk akhirnya sebelum mulai",
    blok("aksi", "Gambar empat kotak ini di kertas. Sungguh — di kertas, sekarang. Kamu akan "
                 "memakainya lagi besok sebagai diagram di README.", "LAKUKAN"),
    """        <div class="diagram">
          <div class="kotak"><strong>1. SUMBER</strong>CSV mentah</div>
          <span class="panah">→</span>
          <div class="kotak"><strong>2. GUDANG</strong>BigQuery</div>
          <span class="panah">→</span>
          <div class="kotak"><strong>3. TRANSFORMASI</strong>dbt + test</div>
          <span class="panah">→</span>
          <div class="kotak"><strong>4. TAMPILAN</strong>Streamlit</div>
        </div>""",
    "<p>Dan satu panah lagi yang tidak terlihat di gambar: <strong>GitHub Actions</strong> yang "
    "menjalankan kotak 2 dan 3 tiap hari tanpa kamu sentuh.</p>",
    "<p>Semua bagiannya sudah kamu kerjakan terpisah selama tiga minggu terakhir. Dua hari ini "
    "cuma menyambungnya — dan justru sambungannya yang membuat proyek ini bernilai, karena "
    "hampir tidak ada pelamar yang punya.</p>")

langkah("Pilih datanya, dan pilih yang lebih besar dari contoh",
    blok("aksi", "Putuskan sekarang, tulis pilihanmu, lalu unduh datanya.", "LAKUKAN"),
    tabel(["Pilihan", "Kapan dipilih", "Ukuran"],
          [["Data kedai kopi (Minggu 10)", "kamu ingin cepat dan sudah kenal datanya", "151.088 baris"],
           ["<code>data.gov.sg</code> — Resale Flat Prices", "target kerjamu Singapura", "ratusan ribu baris"],
           ["<code>data.gov.au</code> / data ABS", "target kerjamu Australia", "bervariasi"]]),
    blok("catatan", "<strong>Data lokal negara tujuan punya nilai tambah yang nyata.</strong> "
                    "Perekrut di Singapura mengenali \"Resale Flat Prices\" tanpa perlu dijelaskan, "
                    "dan itu memotong separuh usaha menjelaskan proyekmu."),
    blok("bahaya", "<strong>Jangan memakai data klien, sekalipun namanya sudah kamu ganti.</strong> "
                   "Proyek ini akan publik dan permanen. Aturan Bekal Rahasia Klien berlaku penuh "
                   "di sini."))

langkah("Muat ke gudang data",
    blok("aksi", "Ikuti pola Minggu 9: buat dataset baru di BigQuery, unggah CSV-nya sebagai tabel "
                 "mentah. Lalu hitung satu angka kontrol dan simpan.", "LAKUKAN"),
    kode("SELECT COUNT(*) AS baris, SUM(harga) AS total\nFROM `proyekmu.mentah.penjualan`;"),
    blok("hasil", "<p>Dua angka. Tulis keduanya di catatanmu.</p>", "YANG HARUS TERLIHAT"),
    "<p><strong>Dua angka itu yang akan kamu pakai untuk membuktikan bahwa seluruh pipeline-mu "
    "tidak kehilangan apa pun.</strong> Setiap lapisan sesudah ini harus bisa dicocokkan kembali "
    "ke sini. Tanpa angka kontrol, kamu cuma berharap.</p>")

langkah("Bangun tiga lapis dbt",
    blok("aksi", "Ikuti pola Minggu 10. Target minimalnya bukan sekadar meniru latihan minggu lalu.", "LAKUKAN"),
    tabel(["Lapisan", "Jumlah minimal", "Isinya"],
          [["<code>staging/</code>", "1 model per tabel sumber", "ganti nama kolom, betulkan tipe"],
           ["<code>intermediate/</code>", "minimal 2", "gabungan dan perhitungan antara"],
           ["<code>marts/</code>", "minimal 2", "tabel siap pakai untuk dashboard"]]),
    "<p><strong>Minimal 10 test</strong>, dan salah satunya <em>harus</em> test rekonsiliasi: total "
    "di mart dibandingkan dengan angka kontrol yang kamu catat di langkah 3. Semua model punya "
    "<code>description</code>.</p>",
    blok("catatan", "<strong>Kenapa dua mart, bukan satu?</strong> Karena besok kamu harus bisa "
                    "menjelaskan keputusan itu dalam satu kalimat. Jawaban yang bagus terdengar "
                    "seperti: <em>“satu mart menjawab pertanyaan waktu, satu menjawab pertanyaan "
                    "produk; menggabungkannya memaksa dashboard mengagregasi ulang tiap kali.”</em>"))

langkah("Jalankan dari nol untuk membuktikan bukan cuma jalan di komputermu",
    blok("aksi", "Clone repositorimu sendiri ke folder baru yang benar-benar kosong, lalu jalankan.", "LAKUKAN"),
    kode("cd /tmp\ngit clone https://github.com/[username]/[repo].git uji-bersih\ncd uji-bersih\npython3 -m venv venv && source venv/bin/activate\npip install -r requirements.txt\ndbt build"),
    blok("hasil", "<p><code>dbt build</code> selesai hijau, semua model terbangun dan semua test "
                  "lulus — di folder yang tidak pernah kamu sentuh sebelumnya.</p>",
         "YANG HARUS TERLIHAT"),
    blok("bahaya", "<strong>Ini langkah yang paling sering dilewati dan paling sering menjatuhkan.</strong> "
                   "Proyek yang cuma jalan di komputermu akan gagal di depan perekrut yang mencobanya. "
                   "Penyebab paling umum: berkas yang lupa di-commit karena terlanjur masuk "
                   "<code>.gitignore</code>, dan pustaka yang kamu pasang berbulan-bulan lalu tapi "
                   "tidak ada di <code>requirements.txt</code>."))

langkah("Pasang penjadwalan otomatis",
    blok("aksi", "Ikuti pola Hari 73, tapi workflow-nya menjalankan <code>dbt build</code>, bukan "
                 "skrip laporan.", "LAKUKAN"),
    kode('''name: dbt harian

on:
  schedule:
    - cron: "0 21 * * *"
  workflow_dispatch:'''),
    "<p>Bagian <code>jobs:</code>-nya sama persis dengan Hari 73 — checkout, setup-python, "
    "<code>pip install -r requirements.txt</code> — kecuali dua baris terakhir:</p>",
    kode('''      - run: dbt build
        env:
          GOOGLE_APPLICATION_CREDENTIALS_JSON: ${{ secrets.GCP_SA_KEY }}'''),
    "<p><code>0 21 * * *</code> = <strong>04:00 WIB tiap hari</strong> (21:00 UTC + 7 jam, jatuh di "
    "hari berikutnya). Kunci layanan Google disimpan sebagai <em>repository secret</em> bernama "
    "<code>GCP_SA_KEY</code> — tidak pernah di dalam berkas.</p>",
    blok("catatan", "<strong>Jalankan sekali dengan tombol <em>Run workflow</em> sekarang juga.</strong> "
                    "Jangan menunggu jam 4 pagi untuk tahu ada salah ketik di nama secret-mu."))

langkah("Pasang lencananya",
    blok("aksi", "Tambahkan satu baris ini di paling atas README-mu, ganti dua tanda kurung siku "
                 "dengan milikmu.", "LAKUKAN"),
    kode("![status](https://github.com/[username]/[repo]/actions/workflows/dbt.yml/badge.svg)"),
    blok("hasil", "<p>Lencana hijau bertuliskan <strong>passing</strong> di paling atas halaman "
                  "repositorimu.</p>", "YANG HARUS TERLIHAT"),
    "<p>Lencana ini bukan hiasan. Ia bukti visual bahwa pipeline-mu <em>benar-benar berjalan</em> "
    "dan test-nya <em>benar-benar lulus</em> — hari ini, bukan waktu kamu terakhir menyentuhnya. "
    "Perekrut yang tahu artinya akan langsung melihatnya.</p>",
    blok("bahaya", "<strong>Lencana merah lebih buruk daripada tidak ada lencana.</strong> Kalau "
                   "pipeline-mu gagal dan kamu biarkan, kamu sedang memasang bukti permanen bahwa "
                   "kamu tidak memperhatikan pekerjaanmu sendiri. Perbaiki atau lepas lencananya."))

HARI76 = {
  "n": "HARI 76",
  "tab": "76",
  "judul": "Proyek #9 bagian 1: pipeline yang menjalankan dirinya sendiri",
  "waktu": "± 75 menit",
  "tujuan": "menyatukan sepuluh minggu terakhir jadi satu sistem — sumber, gudang, transformasi "
            "bertest, dan jadwal otomatis — dengan angka kontrol yang bisa dicocokkan di tiap lapisan.",
  "langkah": L,
  "tutup_judul": "Hari 76 selesai. Berhenti di sini — lanjutkan besok.",
  "tutup": "<p>Sistemmu sekarang berjalan sendiri sampai lapisan dbt, dan buktinya ada di lencana "
           "hijau di README-mu. Besok: tampilan publik, README yang menjual, dan latihan "
           "menjelaskannya dalam 90 detik.</p>",
}
