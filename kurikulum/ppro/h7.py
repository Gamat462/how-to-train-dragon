# -*- coding: utf-8 -*-
"""Hari 7 — skrip yang bisa dipasang di jadwal."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Tulis fungsi agregasinya",
    blok("aksi", "Simpan sebagai <code>laporan/hitung.py</code>. Perhatikan: ia "
                 "<strong>tidak mencetak apa pun</strong>.", "LAKUKAN"),
    kode('''"""Agregasi laporan. Tidak mencetak apa pun — hanya mengembalikan nilai."""
import pandas as pd


def omzet_per_cabang(df: pd.DataFrame) -> pd.DataFrame:
    """Ringkas omzet dan jumlah transaksi per cabang, terbesar dulu."""
    return (df.groupby("cabang", observed=True)
              .agg(transaksi=("nilai", "size"), omzet=("nilai", "sum"))
              .sort_values("omzet", ascending=False)
              .reset_index())'''),
    blok("hasil", "<p>Tidak ada keluaran.</p>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Fungsi yang menghitung tidak boleh mencetak.</strong> Kalau ia "
                    "mencetak, ia tidak bisa diuji, tidak bisa dipakai ulang, dan keluarannya "
                    "tidak bisa diarahkan ke mana pun. Yang mencetak adalah "
                    "<code>cli.py</code> — satu berkas, satu tugas."))

langkah("Titik masuk, versi paling kecil",
    blok("aksi", "Simpan sebagai <code>laporan/cli.py</code>. Baru satu argumen.", "LAKUKAN"),
    kode('''"""Titik masuk baris perintah untuk alat laporan."""
import argparse
from pathlib import Path


def argumen(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ringkas omzet per cabang dari berkas CSV.")
    p.add_argument("--berkas", type=Path, required=True, help="CSV sumber")
    return p.parse_args(argv)


if __name__ == "__main__":
    print(argumen())'''),
    kode("python -m laporan.cli --berkas transaksi.csv"),
    blok("hasil", "<pre><code>Namespace(berkas=PosixPath('transaksi.csv'))</code></pre>",
         "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau punyamu tertulis <code>WindowsPath</code></strong>, itu normal "
                    "— kamu di Windows, dan isinya sama saja. Yang penting nama berkasnya "
                    "muncul di dalam kurung."),
    "<p>Belum ada yang dihitung — kamu baru membuktikan bahwa argumenmu sampai ke dalam "
    "program.</p>")

langkah("Halaman bantuan yang kamu dapat gratis",
    blok("aksi", "Kamu tidak menulis satu baris pun untuk ini.", "LAKUKAN"),
    kode("python -m laporan.cli --help"),
    blok("hasil", "<pre><code>usage: cli.py [-h] --berkas BERKAS\n\n"
                  "Ringkas omzet per cabang dari berkas CSV.\n\n"
                  "options:\n  -h, --help       show this help message and exit\n"
                  "  --berkas BERKAS  CSV sumber</code></pre>", "HARUS MUNCUL"),
    "<p>argparse menyusunnya sendiri dari <code>description=</code> dan <code>help=</code> yang "
    "kamu tulis. <strong>Enam bulan lagi, waktu kamu lupa cara memakai skripmu sendiri, ini "
    "yang menyelamatkanmu</strong> — dan ini juga yang kamu berikan ke klien, supaya kamu tidak "
    "ditelepon tiap kali dia bingung.</p>")

langkah("Dan penolakan yang kamu dapat gratis juga",
    blok("aksi", "Lupakan argumen wajibnya dengan sengaja.", "LAKUKAN"),
    kode("python -m laporan.cli"),
    blok("hasil", "<pre><code>usage: cli.py [-h] --berkas BERKAS\n"
                  "cli.py: error: the following arguments are required: --berkas</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>required=True</code> yang melakukannya untukmu. Skrip notebook yang biasa kamu "
    "tulis akan jalan setengah jalan lalu gagal dengan pesan yang membingungkan; yang ini "
    "<strong>menolak sebelum mengerjakan apa pun</strong>.</p>")

langkah("Tiga argumen lagi",
    blok("aksi", "Sisipkan tepat sebelum <code>return p.parse_args(argv)</code>.", "LAKUKAN"),
    kode('''    p.add_argument("--keluar", type=Path, help="CSV hasil (kalau kosong: cetak ke layar)")
    p.add_argument("--cabang", help="saring satu cabang saja")
    p.add_argument("--rinci", action="store_true", help="tampilkan log tingkat DEBUG")'''),
    kode("python -m laporan.cli --help"),
    blok("hasil", "<pre><code>usage: cli.py [-h] --berkas BERKAS [--keluar KELUAR] [--cabang CABANG]\n"
                  "              [--rinci]\n...\n"
                  "  --keluar KELUAR  CSV hasil (kalau kosong: cetak ke layar)\n"
                  "  --cabang CABANG  saring satu cabang saja\n"
                  "  --rinci          tampilkan log tingkat DEBUG</code></pre>", "HARUS MUNCUL"),
    "<p>Kurung siku di <code>usage</code> berarti pilihan — kamu boleh tidak menyebutnya. "
    "<code>action=\"store_true\"</code> membuat <code>--rinci</code> jadi saklar: kamu cukup "
    "menyebut namanya, tanpa nilai apa pun di belakangnya.</p>")

langkah("Kenapa print() tidak cukup",
    blok("aksi", "Baca sekali, lalu pasang penggantinya.", "LAKUKAN"),
    blok("hasil", "<p><code>print</code> tidak punya <strong>waktu</strong>, tidak punya "
                  "<strong>tingkat kepentingan</strong>, tidak bisa dimatikan sebagian, dan "
                  "semuanya masuk ke tempat yang sama — sehingga pesan “selesai” dan pesan “ada "
                  "yang salah” terlihat serupa.</p>", "MASALAHNYA"),
    "<p>Ketika skripmu berjalan jam 6 pagi tanpa ditonton siapa pun, <strong>satu-satunya bukti "
    "tentang apa yang terjadi adalah catatannya</strong>.</p>")

langkah("Pasang logging",
    blok("aksi", "Tambahkan <code>import logging</code> di atas, lalu dua potong ini.", "LAKUKAN"),
    kode('''log = logging.getLogger("laporan")


def atur_log(rinci: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if rinci else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )'''),
    blok("aksi", "Lalu ganti blok <code>if __name__</code> di bawah:", "LAKUKAN"),
    kode('''if __name__ == "__main__":
    a = argumen()
    atur_log(a.rinci)
    log.info("membaca %s", a.berkas)
    log.debug("argumen lengkap: %s", a)'''),
    kode("python -m laporan.cli --berkas transaksi.csv"),
    blok("hasil", "<pre><code>04:22:51 INFO    laporan | membaca transaksi.csv</code></pre>",
         "HARUS MUNCUL (jamnya beda)"),
    "<p>Baris <code>DEBUG</code> tidak muncul. Itu benar — ia menunggu <code>--rinci</code>.</p>")

langkah("Nyalakan yang DEBUG",
    blok("aksi", "Perintah yang sama, tambah satu saklar.", "LAKUKAN"),
    kode("python -m laporan.cli --berkas transaksi.csv --rinci"),
    blok("hasil", "<pre><code>04:22:51 INFO    laporan | membaca transaksi.csv\n"
                  "04:22:51 DEBUG   laporan | argumen lengkap: Namespace(berkas=PosixPath('transaksi.csv'), "
                  "keluar=None, cabang=None, rinci=True)</code></pre>", "HARUS MUNCUL"),
    "<p>Tiap catatan punya <strong>waktu</strong>, <strong>tingkat</strong>, dan "
    "<strong>nama sumbernya</strong>. Satu saklar memutuskan seberapa cerewet — tanpa menghapus "
    "satu baris pun dari kodenya.</p>",
    blok("catatan", "Tulis <code>log.info(\"membaca %s\", a.berkas)</code>, bukan "
                    "<code>log.info(f\"membaca {a.berkas}\")</code>. Dengan bentuk pertama, "
                    "teksnya baru dirakit kalau catatannya memang jadi ditampilkan."))

langkah("Ganti blok if __name__ dengan main() yang sungguhan",
    blok("aksi", "Ini inti hari ini. Tambahkan <code>import sys, time</code>, "
                 "<code>import pandas as pd</code>, "
                 "<code>from laporan.hitung import omzet_per_cabang</code>, dan kamus "
                 "<code>TIPE</code> dari Hari 4 di bagian atas berkas.", "LAKUKAN"),
    kode('''def main(argv=None) -> int:
    a = argumen(argv)
    atur_log(a.rinci)
    mulai = time.perf_counter()

    if not a.berkas.exists():
        log.error("berkas tidak ditemukan: %s", a.berkas)
        return 2                       # kode keluar bukan-nol = gagal

    log.info("membaca %s", a.berkas)
    df = pd.read_csv(a.berkas, dtype=TIPE, parse_dates=["tanggal"])
    log.debug("terbaca %s baris, memori %.1f MB",
              f"{len(df):,}", df.memory_usage(deep=True).sum() / 1e6)'''),
    blok("hasil", "<p>Belum bisa dijalankan — <code>main</code> belum selesai. Langkah "
                  "berikutnya melanjutkannya.</p>", "HARUS MUNCUL"),
    "<p><code>return 2</code> itu yang paling penting di potongan ini, dan alasannya di "
    "langkah <em>“Periksa kode keluarnya”</em>.</p>")

langkah("Lanjutkan main(): saringannya",
    blok("aksi", "Sambung persis di bawahnya, indentasi sama.", "LAKUKAN"),
    kode('''    if a.cabang:
        sebelum = len(df)
        df = df[df["cabang"] == a.cabang]
        log.info("saring cabang=%s: %s -> %s baris", a.cabang, f"{sebelum:,}", f"{len(df):,}")
        if df.empty:
            log.warning("tidak ada baris untuk cabang %r — hasilnya akan kosong", a.cabang)'''),
    blok("hasil", "<p>Masih belum bisa dijalankan.</p>", "HARUS MUNCUL"),
    "<p>Baris <code>log.warning</code> itu yang paling penting di seluruh berkas ini, dan "
    "langkah <em>“Gagal dengan benar”</em> menunjukkan kenapa.</p>")

langkah("Selesaikan main(): hitung, keluarkan, lapor",
    blok("aksi", "Sambung lagi di bawahnya.", "LAKUKAN"),
    kode('''    hasil = omzet_per_cabang(df)
    if a.keluar:
        hasil.to_csv(a.keluar, index=False)
        log.info("ditulis ke %s", a.keluar)
    else:
        print(hasil.to_string(index=False))

    log.info("selesai dalam %.2f detik", time.perf_counter() - mulai)
    return 0'''),
    blok("aksi", "Lalu di paling bawah berkas:", "LAKUKAN"),
    kode('''if __name__ == "__main__":
    sys.exit(main())'''),
    blok("hasil", "<p>Berkasnya sekarang sekitar 68 baris. Siap dijalankan.</p>", "HARUS MUNCUL"),
    "<p><code>sys.exit(main())</code> menyerahkan angka yang dikembalikan <code>main</code> "
    "ke sistem operasi. Langkah <em>“Periksa kode keluarnya”</em> membuktikannya.</p>")

langkah("Jalankan seperti alat, bukan seperti notebook",
    blok("aksi", "Dari <code>proyek/</code>.", "LAKUKAN"),
    kode("python -m laporan.cli --berkas transaksi.csv --cabang Dago --rinci"),
    blok("hasil", "<pre><code>04:23:05 INFO    laporan | membaca transaksi.csv\n"
                  "04:23:06 DEBUG   laporan | terbaca 800,000 baris, memori 18.4 MB\n"
                  "04:23:06 INFO    laporan | saring cabang=Dago: 800,000 -&gt; 160,428 baris\n"
                  "cabang  transaksi      omzet\n"
                  "  Dago     160428 8346883000\n"
                  "04:23:06 INFO    laporan | selesai dalam 0.53 detik</code></pre>", "HARUS MUNCUL"),
    "<p>Jamnya akan berbeda; <strong>angkanya tidak boleh</strong>. Perhatikan "
    "<code>memori 18.4 MB</code> — itu pelajaran Hari 4 yang sekarang ikut tercatat tiap kali "
    "skripnya jalan.</p>")

langkah("Gagal dengan benar",
    blok("aksi", "Salah ketik nama cabang, dengan sengaja.", "LAKUKAN"),
    kode("python -m laporan.cli --berkas transaksi.csv --cabang Bogor"),
    blok("hasil", "<pre><code>04:23:17 INFO    laporan | saring cabang=Bogor: 800,000 -&gt; 0 baris\n"
                  "04:23:17 WARNING laporan | tidak ada baris untuk cabang 'Bogor' — hasilnya akan kosong\n"
                  "Empty DataFrame\nColumns: [cabang, transaksi, omzet]\nIndex: []</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "<strong>Ini bukan error, tapi wajib berbunyi.</strong> Ingat pelajaran Bekal "
                   "Data Klien: <code>.sum()</code> pada tabel kosong mengembalikan 0, bukan "
                   "error. Laporan berisi nol yang terkirim tanpa peringatan terlihat seperti "
                   "“penjualan nihil”, bukan seperti “salah ketik nama cabang”. Satu baris "
                   "<code>WARNING</code> memisahkan keduanya."))

langkah("Periksa kode keluarnya",
    blok("aksi", "Inilah yang dibaca cron, GitHub Actions, dan penjadwal mana pun.", "LAKUKAN"),
    kode('''python -m laporan.cli >/dev/null 2>&1;                        echo "lupa argumen wajib -> $?"
python -m laporan.cli --berkas hilang.csv >/dev/null 2>&1;    echo "berkas tidak ada   -> $?"
python -m laporan.cli --berkas transaksi.csv >/dev/null 2>&1; echo "berhasil           -> $?"'''),
    blok("hasil", "<pre><code>lupa argumen wajib -&gt; 2\nberkas tidak ada   -&gt; 2\n"
                  "berhasil           -&gt; 0</code></pre>", "HARUS MUNCUL"),
    "<p><strong>0 berarti berhasil, bukan-nol berarti gagal.</strong> Baku di seluruh dunia "
    "perangkat lunak. Itu sebabnya <code>main()</code> mengembalikan angka dan "
    "<code>sys.exit(main())</code> menyerahkannya ke sistem.</p>",
    blok("catatan", "Skrip yang <em>selalu</em> keluar dengan 0 — misalnya karena error-nya "
                    "ditangkap lalu ditelan — akan dilaporkan “berhasil” oleh penjadwal "
                    "selamanya, meski tidak menghasilkan apa-apa. Ini bersaudara dekat dengan "
                    "pelajaran <code>raise</code> di Bekal Kirim Hasil, dan dengan "
                    "<code>sys.exit(1 if gagal else 0)</code> di SQL Mahir L4."))

langkah("Tulis hasilnya ke berkas",
    blok("aksi", "Sekarang tanpa <code>--cabang</code>, dan dengan <code>--keluar</code>.", "LAKUKAN"),
    kode('''python -m laporan.cli --berkas transaksi.csv --keluar hasil.csv
cat hasil.csv'''),
    blok("hasil", "<pre><code>04:23:19 INFO    laporan | ditulis ke hasil.csv\n"
                  "cabang,transaksi,omzet\nKemang,160457,8373050000\nSeturan2,160087,8360182000\n"
                  "Dago,160428,8346883000\nSeturan,159650,8323688000\n"
                  "Renon,159378,8317611000</code></pre>", "HARUS MUNCUL"),
    "<p>Perhatikan: begitu kamu memberi <code>--keluar</code>, tabelnya <strong>tidak lagi "
    "dicetak ke layar</strong> — cuma satu baris catatan. Itu persis yang kamu mau dari skrip "
    "yang jalan jam 6 pagi tanpa kamu tonton.</p>")

langkah("Kunci lingkungannya",
    blok("aksi", "Satu perintah terakhir.", "LAKUKAN"),
    kode('''pip freeze > requirements.txt
grep -i "pandas\\|pytest" requirements.txt'''),
    blok("hasil", "<pre><code>pandas==3.0.5\npytest==9.1.1</code></pre>",
         "HARUS MUNCUL (versimu boleh beda)"),
    "<p>Di komputer klien atau di server, <code>pip install -r requirements.txt</code> menyusun "
    "ulang lingkungan yang sama.</p>",
    blok("bahaya", "<strong>Ini bukan formalitas, dan kamu sudah membuktikannya sendiri.</strong> "
                   "Di Hari 3 kamu melihat bug “Nan” yang ada di pandas 2 dan hilang di pandas 3 "
                   "— kode yang sama, hasil berbeda, tanpa satu pun error. "
                   "<code>requirements.txt</code> adalah cara termurah menghentikan seluruh kelas "
                   "masalah itu."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Tiga hal yang dimiliki catatan logging dan tidak dimiliki print?
2. Apa arti kode keluar 0, dan apa arti 2?
3. Kenapa laporan kosong wajib memunculkan WARNING?
4. Kenapa fungsi hitung tidak boleh mencetak?
5. Apa yang dilindungi requirements.txt?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Waktu, tingkat kepentingan, dan nama sumbernya. "
    "2. 0 = berhasil, bukan-nol = gagal — itu yang dibaca penjadwal. "
    "3. Karena <code>.sum()</code> pada tabel kosong mengembalikan 0, bukan error, jadi "
    "salah ketik terlihat seperti penjualan nihil. "
    "4. Supaya bisa diuji, dipakai ulang, dan keluarannya bisa diarahkan. "
    "5. Perbedaan versi pustaka yang mengubah hasil <em>tanpa error</em>.</p></details>")

HARI7 = {
  "n": "HARI 7",
  "tab": "7",
  "judul": "Skrip yang bisa dipasang di jadwal",
  "waktu": "± 80 menit",
  "tujuan": "mengubah notebook jadi perintah yang dijalankan dengan argumen, mencatat apa yang "
            "dikerjakannya, dan melapor gagal dengan cara yang <strong>bisa dibaca mesin "
            "penjadwal</strong>.",
  "langkah": L,
  "tutup_judul": "Python Produksi selesai — dan jalur teknismu tuntas",
  "tutup": "<p>Kamu punya satu paket Python sungguhan sekarang: fungsi di berkasnya sendiri, "
           "bertanda tipe, ber-docstring, <strong>diuji 15 kali dalam sepertiga detik</strong>, "
           "dengan titik masuk baris perintah yang punya halaman bantuan, catatan bertingkat, "
           "dan kode keluar yang benar.</p>"
           "<p style=\"margin-top:8px\"><strong>Yang berubah bukan kemampuanmu menulis Python — "
           "tapi apakah kode itu boleh dipercaya berjalan tanpa kamu tonton.</strong> Itu "
           "satu-satunya syarat sebelum kamu menagih klien secara bulanan.</p>"
           "<p style=\"margin-top:8px\"><strong>Enam angka dari modul ini, semuanya hasil "
           "pengukuran:</strong> memori 65,4 → 18,4 MB dengan memilih tipe; <code>.apply</code> → "
           "vektorisasi <strong>248×</strong> di 800.000 baris, tapi cuma <strong>1,2×</strong> "
           "untuk logika bercabang — jadi jangan pukul rata; <code>chunksize</code> memangkas "
           "puncak memori <strong>27×</strong>; generator memakai ~0 MB tapi <strong>8× lebih "
           "lambat</strong>; dan 15 uji berjalan dalam 0,33 detik.</p>"
           "<p style=\"margin-top:8px\"><strong>Satu hal yang belum ditutup, dan saya sebut "
           "supaya kamu tahu.</strong> Seluruh kurikulum ini — termasuk modul ini — tidak pernah "
           "menyuruhmu menunjukkan kode ke <em>manusia lain</em> untuk dikoreksi. Di kantor, "
           "semua kodemu ditinjau orang. Cari satu komunitas data Indonesia, tunjukkan paket "
           "<code>laporan/</code> yang baru kamu buat, dan minta dikritik. Review pertama selalu "
           "terasa seperti serangan pribadi; sesudah yang kelima, ia jadi hal biasa. Lebih baik "
           "pengalaman itu terjadi sebelum hari pertama kerja.</p>",
}
