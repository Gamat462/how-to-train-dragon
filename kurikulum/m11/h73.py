# -*- coding: utf-8 -*-
"""Hari 73 — skrip laporan + GitHub Actions.
Keluaran Python dan git dijalankan sungguhan (Python 3.11.15, pandas 3.0.5, git 2.43.0).
Bagian yang terjadi di layar GitHub ditandai "YANG HARUS TERLIHAT", bukan "HARUS MUNCUL"."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Siapkan data contoh yang ikut masuk repo",
    blok("aksi", "Dari paket zip, salin <code>data-dan-skrip/minggu-11/buat_contoh.py</code> ke "
                 "folder proyekmu. Lalu satu perintah.", "LAKUKAN"),
    kode("python buat_contoh.py"),
    blok("hasil", kode("""baris ditulis: 400
omzet total  : Rp 224.907.000""", salin=False), "HARUS MUNCUL"),
    "<p>Berkas <code>data-contoh/penjualan.csv</code> muncul: 400 baris penjualan enam bulan, "
    "dengan kolom <code>tanggal</code>, <code>nota</code>, <code>produk</code>, <code>qty</code>, "
    "<code>harga</code>, dan <code>jumlah</code>.</p>",
    blok("catatan", "<strong>Angka acaknya berkunci tetap (<code>Random(11)</code> di dalam "
                    "skripnya),</strong> jadi berkasmu isinya sama persis dengan berkasku. Setiap "
                    "angka di sisa hari ini harus cocok denganmu. Kalau tidak cocok, salah satu "
                    "dari kita salah ketik — dan kamu punya datanya untuk membuktikan yang mana."))

langkah("Baca dan hitung satu angka",
    blok("aksi", "Buat berkas <code>laporan.py</code>. Isi empat baris ini dulu — jangan lebih.", "LAKUKAN"),
    kode('''import pandas as pd

df = pd.read_csv("data-contoh/penjualan.csv", parse_dates=["tanggal"])
print(df.shape)
print(df["jumlah"].sum())'''),
    blok("hasil", kode("""(400, 6)
224907000""", salin=False), "HARUS MUNCUL"),
    "<p>400 baris, 6 kolom, omzet Rp 224.907.000. Simpan angka itu — semua yang kamu hitung "
    "sesudah ini harus tetap berjumlah sama.</p>")

langkah("Tambah kolom bulan, lalu kelompokkan",
    blok("aksi", "Tambahkan tiga baris ke <code>laporan.py</code>, jalankan lagi.", "LAKUKAN"),
    kode('''df["bulan"] = df["tanggal"].dt.strftime("%Y-%m")
bulanan = df.groupby("bulan").agg(nota=("nota", "size"), omzet=("jumlah", "sum"))
print(bulanan)'''),
    blok("hasil", kode("""         nota     omzet
bulan                  
2024-01    75  40606000
2024-02    60  27246000
2024-03    61  37041000
2024-04    72  42260000
2024-05    66  34812000
2024-06    66  42942000""", salin=False), "HARUS MUNCUL"),
    "<p><code>.dt.strftime(\"%Y-%m\")</code> memotong tanggal jadi tahun-bulan. Kolom teks itu yang "
    "lalu jadi kunci pengelompokan — dan karena bentuknya <code>2024-01</code>, urutan abjadnya "
    "kebetulan sama dengan urutan waktunya.</p>")

langkah("Pasang satu baris yang membuat skrip ini pantas dijalankan tanpa diawasi",
    blok("aksi", "Tambahkan satu baris <code>assert</code> setelah <code>bulanan</code> dibuat.", "LAKUKAN"),
    kode('assert int(bulanan["omzet"].sum()) == int(df["jumlah"].sum()), "rekap tidak sama dengan sumber"\nprint("rekap cocok dengan sumber")'),
    blok("hasil", kode("rekap cocok dengan sumber", salin=False), "HARUS MUNCUL"),
    "<p>Baris ini membandingkan hasil rekapmu dengan sumbernya. Kalau suatu hari data masuk berubah "
    "bentuk dan rekapmu diam-diam kehilangan baris, skrip ini <strong>berhenti</strong> — bukan "
    "mengirimkan angka yang salah.</p>")

langkah("Lihat wujud kegagalannya sekali, supaya kamu mengenalinya",
    blok("aksi", "Ubah sementara <code>== int(df[\"jumlah\"].sum())</code> jadi "
                 "<code>== int(df[\"jumlah\"].sum()) + 1</code>, jalankan, lalu kembalikan lagi.", "LAKUKAN"),
    kode('assert int(bulanan["omzet"].sum()) == int(df["jumlah"].sum()) + 1, "rekap tidak sama dengan sumber"'),
    blok("hasil", kode("""Traceback (most recent call last):
  File "laporan.py", line 8, in <module>
    assert int(bulanan["omzet"].sum()) == int(df["jumlah"].sum()) + 1, "rekap tidak sama dengan sumber"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: rekap tidak sama dengan sumber""", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Nomor barisnya dan alamat berkasnya pasti beda di layarmu</strong> — "
                    "Python menyebut jalur lengkap foldermu. Yang harus sama adalah baris terakhir: "
                    "<code>AssertionError</code> diikuti pesan yang kamu tulis sendiri."),
    "<p>Skripnya mati dengan kode keluar <strong>1</strong>. Itu angka yang dibaca GitHub Actions "
    "untuk memutuskan lencana merah atau hijau. Inilah yang menghubungkan satu baris "
    "<code>assert</code> di kodemu dengan email peringatan di kotak masukmu.</p>",
    blok("bahaya", "<strong>Jangan lupa mengembalikan <code>+ 1</code>-nya.</strong> "
                   "Jalankan sekali lagi dan pastikan tulisannya kembali "
                   "<code>rekap cocok dengan sumber</code> sebelum lanjut."))

langkah("Tulis hasilnya ke berkas",
    blok("aksi", "Ganti bagian <code>print</code>-mu dengan blok ini. Perhatikan fungsi "
                 "<code>rp()</code> di atas.", "LAKUKAN"),
    kode('''from datetime import datetime, timezone

def rp(x):
    return "Rp " + f"{int(x):,}".replace(",", ".")

waktu = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
with open("hasil/ringkasan.md", "w", encoding="utf-8") as f:
    f.write("# Ringkasan Penjualan\\n\\n")
    f.write(f"Diperbarui otomatis: {waktu}\\n\\n")
    f.write(f"{len(df)} nota, omzet {rp(df['jumlah'].sum())}\\n\\n")
    f.write("## Per bulan\\n\\n```\\n" + bulanan.to_string() + "\\n```\\n")

print("baris dibaca:", len(df))
print("omzet total :", rp(df["jumlah"].sum()))'''),
    blok("hasil", kode("""baris dibaca: 400
omzet total : Rp 224.907.000""", salin=False), "HARUS MUNCUL"),
    """<details>
          <summary>Kenapa pemformatan rupiahnya dibuat fungsi terpisah?</summary>
          <div class="isi">
            <p>Karena versi yang ditulis langsung di tempat menghasilkan bug yang tidak terlihat.
            Coba jalankan dua baris ini dan bandingkan:</p>
            <div class="kode"><pre><code>n = 224907000
print(f"400 nota, omzet Rp {n:,}".replace(",", "."))</code></pre></div>
            <p>Keluarannya <code>400 nota. omzet Rp 224.907.000</code> — koma setelah kata
            <em>nota</em> ikut berubah jadi titik. <code>.replace()</code> tidak tahu mana koma
            pemisah ribuan dan mana koma kalimat; ia mengganti semuanya.</p>
            <p>Dengan <code>rp()</code>, penggantian hanya terjadi di dalam angka. Ini bug nyata
            yang saya buat sendiri saat menulis modul ini, dan baru ketahuan karena keluarannya
            dibaca ulang.</p>
          </div>
        </details>""")

langkah("Izinkan satu berkas hasil masuk git — dan perhatikan bintangnya",
    blok("aksi", "Tambahkan dua baris ini ke <code>.gitignore</code>, lalu buktikan.", "LAKUKAN"),
    kode('printf "hasil/*\\n!hasil/ringkasan.md\\n" >> .gitignore\ngit check-ignore -v hasil/ringkasan.md'),
    blok("hasil", kode(".gitignore:5:!hasil/ringkasan.md	hasil/ringkasan.md", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Harus <code>hasil/*</code>, bukan <code>hasil/</code>.</strong> "
                   "Kalau kamu menulis <code>hasil/</code>, git tidak akan pernah masuk ke dalam "
                   "folder itu, sehingga baris pengecualian <code>!hasil/ringkasan.md</code> di "
                   "bawahnya <em>tidak pernah terbaca</em>. Berkasnya tetap terabaikan, tanpa "
                   "peringatan apa pun. Satu tanda bintang."),
    blok("catatan", "<strong>Nomor barisnya (<code>:5:</code>) boleh beda</strong> — tergantung "
                    "berapa baris yang sudah ada di <code>.gitignore</code>-mu. Yang harus sama "
                    "adalah tanda seru di depan nama berkasnya."))

langkah("Tulis separuh atas berkas jadwal: kapan ia berjalan",
    blok("aksi", "Buat folder dan berkasnya. Namanya harus tepat — dua tingkat folder, dan "
                 "berakhiran <code>.yml</code>.", "LAKUKAN"),
    kode("mkdir -p .github/workflows\ntouch .github/workflows/laporan.yml"),
    "<p>Isi enam baris pertamanya:</p>",
    kode('''name: Laporan mingguan

on:
  schedule:
    - cron: "0 23 * * 0"
  workflow_dispatch:'''),
    "<p>Dua pemicu: <code>schedule</code> menjalankannya sesuai jadwal, "
    "<code>workflow_dispatch</code> memberimu tombol untuk menjalankannya sekarang juga.</p>",
    blok("bahaya", "<strong>Spasi di YAML bukan hiasan.</strong> Kalau nanti GitHub bilang "
                   "<em>“Invalid workflow file”</em>, sembilan dari sepuluh kali penyebabnya "
                   "indentasi. YAML tidak menerima tab — hanya spasi."))

langkah("Tulis separuh bawahnya: apa yang ia kerjakan",
    blok("aksi", "Lanjutkan di berkas yang sama, di bawah baris <code>workflow_dispatch:</code>.", "LAKUKAN"),
    kode('''jobs:
  buat-laporan:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: python laporan.py'''),
    "<p>Baca dari atas: sewa satu komputer Ubuntu → ambil kodemu → pasang Python 3.11 → pasang "
    "pustaka dari <code>requirements.txt</code> → jalankan skripmu. Persis yang kamu lakukan "
    "sendiri di Hari 72, tapi dikerjakan mesin.</p>",
    blok("catatan", "<strong><code>permissions: contents: write</code> itu wajib</strong> untuk "
                    "langkah berikutnya, yang menyimpan hasilnya kembali ke repositori. Tanpa baris "
                    "itu, <code>git push</code> dari dalam Actions ditolak."))

langkah("Tulis langkah terakhir: simpan hasilnya kembali",
    blok("aksi", "Tambahkan blok ini di bawah <code>- run: python laporan.py</code>, dengan "
                 "indentasi yang sama.", "LAKUKAN"),
    kode('''      - name: Simpan hasilnya kembali ke repo
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add hasil/
          git diff --staged --quiet || git commit -m "Laporan otomatis $(date -u +%F)"
          git push'''),
    "<p>Robot Actions harus punya nama dan email seperti manusia — itu syarat git, bukan gaya. "
    "Baris <code>git diff --staged --quiet ||</code> yang paling penting, dan langkah nanti "
    "menjelaskan kenapa.</p>")

langkah("Baca baris jadwalnya, karena jamnya bukan jam Indonesia",
    blok("aksi", "Hitung sendiri: <code>cron: \"0 23 * * 0\"</code> itu jam berapa WIB?", "LAKUKAN"),
    tabel(["Yang kamu inginkan (WIB)", "Yang ditulis di cron (UTC)", "Kolom cron"],
          [["Senin 06:00", "Minggu 23:00", "<code>0 23 * * 0</code>"],
           ["Senin 07:00", "Senin 00:00", "<code>0 0 * * 1</code>"],
           ["Tiap hari 08:00", "Tiap hari 01:00", "<code>0 1 * * *</code>"],
           ["Tiap hari 17:00", "Tiap hari 10:00", "<code>0 10 * * *</code>"]]),
    "<p><strong>WIB = UTC + 7.</strong> Jadi untuk mendapat jam WIB, kurangi 7 dari jam UTC. "
    "Kalau hasilnya negatif, jadwalnya jatuh di <em>hari sebelumnya</em> menurut UTC — itulah "
    "kenapa Senin pagi ditulis sebagai hari Minggu.</p>",
    blok("bahaya", "<strong>Jadwal GitHub Actions tidak tepat waktu.</strong> Ia sering terlambat "
                   "5–30 menit, dan pada jam sibuk bisa lebih. Jangan pakai untuk hal yang "
                   "bergantung pada menit. Untuk laporan mingguan, ini tidak masalah sama sekali."))

langkah("Kirim ke GitHub dan jalankan sekali dengan tangan",
    blok("aksi", "Commit dan push. Lalu di GitHub buka tab <strong>Actions</strong>, pilih "
                 "<em>Laporan mingguan</em> di kiri, klik tombol <strong>Run workflow</strong>.", "LAKUKAN"),
    kode('git add . && git commit -m "Tambah laporan otomatis mingguan"\ngit push -u origin main'),
    blok("hasil", "<p>Di tab Actions muncul satu baris pekerjaan dengan lingkaran kuning berputar, "
                  "lalu berubah jadi <strong>centang hijau</strong> dalam 30–90 detik. Klik "
                  "barisnya untuk melihat catatan tiap langkah — termasuk "
                  "<code>omzet total : Rp 224.907.000</code> yang kamu cetak tadi.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Kalau <code>workflow_dispatch</code> tidak kamu tulis, tombol "
                    "<em>Run workflow</em> tidak muncul</strong> dan kamu harus menunggu sampai hari "
                    "Senin untuk tahu skripmu jalan atau tidak. Selalu pasang baris itu."))

langkah("Pahami baris yang mencegah commit kosong",
    blok("aksi", "Baris ini yang paling sering disalin tanpa dimengerti. Coba sendiri di "
                 "komputermu, dua kali berturut-turut tanpa mengubah apa pun.", "LAKUKAN"),
    kode('git add hasil/\ngit diff --staged --quiet || git commit -m "Laporan otomatis"'),
    blok("hasil", "<p>Kali pertama: sebuah commit dibuat. Kali kedua, tanpa perubahan apa pun: "
                  "tidak terjadi apa-apa, dan tidak ada pesan error.</p>", "HARUS MUNCUL"),
    "<p><code>git diff --staged --quiet</code> berhasil (benar) kalau <strong>tidak ada</strong> "
    "perubahan. Tanda <code>||</code> berarti \"kalau perintah sebelumnya gagal, jalankan yang ini\". "
    "Jadi commit hanya terjadi ketika benar-benar ada yang berubah.</p>",
    blok("catatan", "<strong>Tanpa baris ini, workflow-mu gagal setiap minggu ketika datanya tidak "
                    "berubah</strong> — <code>git commit</code> tanpa perubahan mengembalikan kode "
                    "keluar 1, dan GitHub menandainya merah. Lencana merah yang bukan karena "
                    "kesalahan apa pun adalah cara tercepat membuat orang berhenti mempercayai "
                    "lencananya."))

langkah("Simpan kredensial di tempat yang benar",
    blok("aksi", "Belum dipakai hari ini, tapi wajib kamu tahu sekarang. Di GitHub: "
                 "<strong>Settings → Secrets and variables → Actions → New repository secret</strong>. "
                 "Beri nama <code>DB_PASSWORD</code>.", "LAKUKAN"),
    "<p>Lalu di workflow-mu, tambahkan di bawah langkah yang membutuhkannya:</p>",
    kode('      - run: python laporan.py\n        env:\n          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}'),
    "<p>Di dalam Python, bacanya <code>os.environ[\"DB_PASSWORD\"]</code> — sama persis seperti "
    "membaca dari berkas <code>.env</code> di komputermu. Kodemu tidak perlu tahu bedanya.</p>",
    blok("catatan", "<strong>GitHub menyensor nilai rahasia di catatan Actions secara otomatis.</strong> "
                    "Kalau kamu tidak sengaja mencetaknya, yang muncul <code>***</code>. Jangan "
                    "mengandalkan itu — penyensoran hanya bekerja untuk kecocokan persis, dan gagal "
                    "kalau nilainya sudah kamu potong atau ubah."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab enam pertanyaan ini dengan suara keras, lalu periksa.", "LAKUKAN"),
    """<ol>
          <li>Apa gunanya baris <code>assert</code> di skrip yang berjalan tanpa diawasi?</li>
          <li>Kenapa <code>hasil/</code> di .gitignore membuat <code>!hasil/ringkasan.md</code> tidak berfungsi?</li>
          <li>Jam 8 pagi WIB ditulis bagaimana di cron?</li>
          <li>Kenapa <code>workflow_dispatch</code> hampir selalu perlu ditulis?</li>
          <li>Apa yang terjadi kalau <code>git commit</code> dijalankan tanpa perubahan?</li>
          <li>Di mana kata sandi disimpan supaya bisa dipakai Actions tapi tidak masuk repo?</li>
        </ol>""",
    """<details>
          <summary>Jawaban</summary>
          <div class="isi">
            <p><strong>1.</strong> Menghentikan skrip dengan kode keluar 1 kalau hasilnya tidak
            masuk akal, sehingga Actions menandainya merah — lebih baik daripada mengirim angka
            yang salah tanpa suara.</p>
            <p><strong>2.</strong> Karena git tidak pernah masuk ke folder yang seluruhnya
            diabaikan, jadi baris pengecualian di dalamnya tidak pernah dibaca. Harus
            <code>hasil/*</code>.</p>
            <p><strong>3.</strong> <code>0 1 * * *</code> — 08:00 WIB dikurangi 7 jam = 01:00 UTC.</p>
            <p><strong>4.</strong> Supaya ada tombol <em>Run workflow</em> untuk menguji sekarang,
            tanpa menunggu jadwalnya tiba.</p>
            <p><strong>5.</strong> Ia gagal dengan kode keluar 1, dan Actions menandai
            pekerjaannya merah padahal tidak ada yang salah.</p>
            <p><strong>6.</strong> Repository secrets di Settings, dibaca lewat
            <code>${{ secrets.NAMA }}</code> dan diteruskan sebagai variabel lingkungan.</p>
          </div>
        </details>""")

HARI73 = {
  "n": "HARI 73",
  "tab": "73",
  "judul": "Laporan yang berjalan sendiri tiap Senin pagi",
  "waktu": "± 70 menit",
  "tujuan": "menulis skrip laporan yang memeriksa hasilnya sendiri, lalu menjadwalkannya di "
            "GitHub Actions — gratis, dan terlihat di portofoliomu sebagai lencana hijau.",
  "langkah": L,
  "tutup_judul": "Hari 73 selesai. Berhenti di sini.",
  "tutup": "<p><strong>Tempel di catatanmu:</strong> <code>assert</code> membuat skrip gagal "
           "dengan berisik · <code>hasil/*</code> bukan <code>hasil/</code> · WIB = UTC + 7 · "
           "<code>workflow_dispatch</code> selalu dipasang · "
           "<code>git diff --staged --quiet ||</code> mencegah commit kosong.</p>"
           "<p style=\"margin-top:8px\">Yang kamu punya sekarang: satu repositori yang memperbarui "
           "laporannya sendiri tiap minggu, tanpa kamu sentuh. Itu satu kalimat yang bisa kamu "
           "ucapkan di wawancara, dan tautannya bisa dibuka orang saat itu juga.</p>",
}
