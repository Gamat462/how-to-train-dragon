# -*- coding: utf-8 -*-
"""Hari 6 — soal yang sengaja ambigu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Satu kalimat, dan tulis jawabanmu sebelum membaca apa pun",
    blok("aksi", "Pertanyaannya: <strong>“Berapa pelanggan aktif kita?”</strong> "
                 "Tulis satu query dan satu angka di kertas. Sekarang.", "LAKUKAN"),
    kode("-- jawabanmu, satu query, satu angka:", salin=False),
    blok("bahaya", "<strong>Jangan gulung ke bawah sebelum kertasmu terisi.</strong> Seluruh "
                   "pelajaran hari ini bergantung pada kamu sudah memilih satu jawaban."))

langkah("Kenapa hari ini pakai besar.db, bukan senja.db",
    blok("aksi", "Sambungkan ke <code>besar.db</code> dari Level 4.", "LAKUKAN"),
    kode('''import sqlite3
c = sqlite3.connect("besar.db")
print(c.execute("SELECT COUNT(*), COUNT(DISTINCT pelanggan_id) FROM transaksi").fetchone())'''),
    blok("hasil", "<pre><code>(800000, 50000)</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Baris ini butuh beberapa detik dan layarmu diam.</strong> Itu wajar "
                    "— <code>COUNT(DISTINCT)</code> pada 800.000 baris memang harus membaca "
                    "semuanya. Jangan kamu hentikan."),
    "<p>800.000 transaksi, 50.000 pelanggan, dua tahun. Di <code>senja.db</code> yang cuma 20 "
    "pelanggan semua bacaan memberi angka yang sama, dan <strong>kamu tidak akan melihat "
    "masalahnya.</strong></p>")

langkah("Bacaan 1 — pernah bertransaksi sama sekali",
    blok("aksi", "Simpan patokan tanggalnya dulu, lalu hitung yang paling longgar.", "LAKUKAN"),
    kode('akhir = "(SELECT MAX(tanggal) FROM transaksi)"\n'
         'print(c.execute("SELECT COUNT(DISTINCT pelanggan_id) FROM transaksi").fetchone()[0])'),
    blok("hasil", "<pre><code>50000</code></pre>", "HARUS MUNCUL"),
    "<p>Lima puluh ribu. Kalau jawabanmu di kertas tadi angka ini, kamu memilih bacaan yang "
    "<strong>paling longgar</strong> — dan tidak menyebutnya.</p>")

langkah("Bacaan 2 dan 3 — beri batas waktu",
    blok("aksi", "Sekarang batasi. Jalankan dua-duanya.", "LAKUKAN"),
    kode('for hari in [365, 90]:\n'
         '    sql = f"""SELECT COUNT(DISTINCT pelanggan_id) FROM transaksi\n'
         '              WHERE tanggal >= date({akhir},\'-{hari} day\')"""\n'
         '    print(f"  {hari:>3} hari terakhir: {c.execute(sql).fetchone()[0]:>7,}")'),
    blok("hasil", "<pre><code>  365 hari terakhir:  49,983\n   90 hari terakhir:  43,263</code></pre>",
         "HARUS MUNCUL"),
    "<p>Setahun hampir tidak mengubah apa pun (49.983). Tiga bulan mulai menggigit: "
    "<strong>43.263</strong>.</p>")

langkah("Bacaan 4 — persempit jadi sebulan",
    blok("aksi", "Satu angka lagi, dan di sinilah kejutannya.", "LAKUKAN"),
    kode('sql = f"""SELECT COUNT(DISTINCT pelanggan_id) FROM transaksi\n'
         '          WHERE tanggal >= date({akhir},\'-30 day\')"""\n'
         'print(f"{c.execute(sql).fetchone()[0]:,}")'),
    blok("hasil", "<pre><code>24,768</code></pre>", "HARUS MUNCUL"),
    "<p><strong>24.768 lawan 50.000</strong> — separuhnya, dari kalimat yang sama persis. "
    "Dan kita belum menyentuh arti “aktif” yang lebih ketat.</p>")

langkah("Bacaan 5 — aktif berarti berulang, bukan sekadar pernah",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('sql = f"""SELECT COUNT(*) FROM (SELECT pelanggan_id FROM transaksi\n'
         '          WHERE tanggal >= date({akhir},\'-90 day\')\n'
         '          GROUP BY pelanggan_id HAVING COUNT(*) >= 2)"""\n'
         'print(f"{c.execute(sql).fetchone()[0]:,}")'),
    blok("hasil", "<pre><code>29,616</code></pre>", "HARUS MUNCUL"),
    "<p>Dari 43.263 yang pernah bertransaksi dalam 90 hari, cuma <strong>29.616</strong> yang "
    "melakukannya lebih dari sekali.</p>")

langkah("Bacaan 6 — dan yang paling ketat",
    blok("aksi", "Terakhir. Dua bulan <em>berbeda</em>, bukan dua transaksi.", "LAKUKAN"),
    kode('sql = f"""SELECT COUNT(*) FROM (SELECT pelanggan_id FROM transaksi\n'
         '          WHERE tanggal >= date({akhir},\'-90 day\')\n'
         '          GROUP BY pelanggan_id\n'
         '          HAVING COUNT(DISTINCT substr(tanggal,1,7)) >= 2)"""\n'
         'print(f"{c.execute(sql).fetchone()[0]:,}")'),
    blok("hasil", "<pre><code>24,007</code></pre>", "HARUS MUNCUL"),
    "<p>Sekarang lihat angkamu di kertas tadi. <strong>Dari 24.007 sampai 50.000</strong> — "
    "angka tertinggi lebih dari <strong>dua kali lipat</strong> angka terendah.</p>",
    blok("catatan", "<strong>Kalau angkamu meleset beberapa puluh</strong> dari kotak-kotak di "
                    "atas, cek dulu <code>besar.db</code>-mu dibuat dengan "
                    "<code>Random(7)</code>. Kalau meleset ribuan, ada yang salah ketik di "
                    "batas harinya."))

langkah("Salah tulis format tanggal, dan kehilangan seluruh jawabanmu",
    blok("aksi", "Tulis tanggalnya gaya Indonesia — 31-12-2024. Jalankan dua-duanya.", "LAKUKAN"),
    kode('''for fmt in ["'31-12-2024'", "'2024-12-31'"]:
    d = c.execute(f"SELECT date({fmt},'-90 day')").fetchone()[0]
    n = c.execute(f"""SELECT COUNT(DISTINCT pelanggan_id) FROM transaksi
                      WHERE tanggal >= date({fmt},'-90 day')""").fetchone()[0]
    print(f"  date({fmt:14}) = {str(d):12} -> aktif: {n:,}")'''),
    blok("bahaya", "<pre><code>  date('31-12-2024'  ) = None         -&gt; aktif: 0\n"
                   "  date('2024-12-31'  ) = 2024-10-02   -&gt; aktif: 43,113</code></pre>",
         "HARUS MUNCUL — DAN TIDAK ADA TULISAN MERAH SAMA SEKALI"),
    blok("bahaya", "<strong>Nol pelanggan aktif, tanpa satu pun error.</strong> "
                   "<code>date()</code> menolak format yang tidak dikenalnya dengan mengembalikan "
                   "<code>NULL</code> — lalu <code>tanggal &gt;= NULL</code> tidak pernah benar "
                   "untuk baris mana pun, persis seperti <code>NOT IN</code> di Hari 1."),
    "<p>SQL cuma mengenal <strong>tahun-bulan-hari</strong>. Kalau angka “aktif”-mu tiba-tiba "
    "nol, ini tersangka pertama — <em>sebelum</em> kamu menyimpulkan pelangganmu kabur semua.</p>")

langkah("Enam-enamnya benar. Itu bagian yang harus kamu terima.",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Keenamnya adalah bacaan yang masuk akal dari kalimat yang sama persis. "
                  "<strong>Tidak ada yang salah di antara keenamnya.</strong></p>",
         "YANG HARUS KAMU TERIMA"),
    "<p>Kalau klien memakai angka ini untuk menghitung biaya per pelanggan aktif, memilih "
    "50.000 atau 24.007 <strong>mengubah hasilnya dua kali lipat</strong>. Kalau untuk target "
    "pertumbuhan, bedanya adalah selisih antara “kita baik-baik saja” dan “separuh pelanggan "
    "kita menghilang”.</p>")

langkah("Jadi apa kesalahannya",
    blok("aksi", "Baca, lalu tulis kalimat ini di catatanmu.", "LAKUKAN"),
    blok("hasil", "<p><strong>Kesalahannya bukan memilih yang salah — itu tidak ada. "
                  "Kesalahannya adalah memilih diam-diam.</strong></p>", "INTINYA"),
    "<p>Mengetik satu query, mengirim satu angka, dan tidak pernah menyebut bahwa ada lima "
    "angka lain yang sama benarnya. Enam bulan kemudian ada orang lain yang menghitung ulang "
    "dengan definisi berbeda, angkanya tidak cocok, dan <strong>yang dipertanyakan adalah "
    "kompetensimu — bukan definisinya</strong>.</p>")

langkah("Tiga pertanyaan yang menutup hampir semua ambiguitas",
    blok("aksi", "Hafalkan bentuknya, bukan kata-katanya.", "LAKUKAN"),
    tabel(["Pertanyaan", "Contoh kalimatnya", "Yang diselamatkan"],
          [["Batas waktunya sampai mana?",
            "“Aktif ini dalam berapa lama terakhir — 30 hari, 90 hari, atau seumur hidup?”",
            "Selisih 24.768 lawan 50.000"],
           ["Yang gagal ikut atau tidak?",
            "“Pesanan yang dibatalkan dihitung atau dibuang?”",
            "38 dari 400 pesanan — hampir 10%"],
           ["Yang kosong diapakan?",
            "“Ada 12 pesanan tanpa <code>pelanggan_id</code>. Dibuang, atau dihitung sebagai "
            "pelanggan tak dikenal?”", "Jebakan <code>NOT IN</code> di Hari 1"]]),
    "<p>Ketiganya kamu sudah temui sendiri minggu ini. Sekarang mereka jadi pertanyaan yang "
    "kamu <strong>ajukan</strong>, bukan jebakan yang menimpamu.</p>")

langkah("Kalau tidak ada yang bisa ditanya",
    blok("aksi", "Baca — ini yang terjadi di kebanyakan wawancara.", "LAKUKAN"),
    blok("hasil", "<p>Pewawancara bilang “terserah kamu”, atau klien sedang tidak bisa "
                  "dihubungi. <strong>Jangan berhenti. Pilih satu, tulis alasannya, "
                  "lanjutkan.</strong></p>", "YANG KAMU LAKUKAN"),
    kode("""Aktif = pernah bertransaksi dalam 90 hari terakhir (43.263 pelanggan).
Kalau definisinya berbeda, angka ini berubah — dengan 30 hari jadi 24.768.""", salin=False),
    "<p>Dua kalimat. Itu sudah cukup, dan itu yang membedakanmu dari kandidat yang mengirim "
    "satu angka telanjang.</p>")

langkah("Namanya catatan asumsi, dan tempatnya di atas",
    blok("aksi", "Baca, lalu buka satu laporan lamamu dan cek apakah ada bagian ini.", "LAKUKAN"),
    blok("hasil", "<p>Dua sampai empat baris di <strong>bagian atas</strong> tiap laporan — "
                  "bukan di catatan kaki: <em>apa yang dihitung, apa yang dibuang, dan tanggal "
                  "datanya.</em></p>", "CATATAN ASUMSI"),
    "<p>Klien yang membacanya akan mengoreksimu di hari pertama kalau ada yang keliru. "
    "<strong>Koreksi di hari pertama itu murah. Koreksi di bulan keenam yang mahal.</strong></p>",
    blok("catatan", "Kamu sudah menulis yang seperti ini selama bertahun-tahun — namanya "
                    "<em>basis penyajian</em> dan <em>catatan atas laporan keuangan</em>. "
                    "Bentuknya berbeda, gunanya persis sama."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Berapa angka terendah dan tertinggi dari "pelanggan aktif", dan berapa lipatnya?
2. Berapa dari enam bacaan itu yang salah?
3. Apa kesalahan yang sesungguhnya?
4. Tiga pertanyaan yang menutup hampir semua ambiguitas?
5. Apa yang kamu lakukan kalau tidak ada yang bisa ditanya?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. 24.007 sampai 50.000 — lebih dari <strong>dua kali lipat</strong>. "
    "2. <strong>Nol.</strong> Keenamnya benar. "
    "3. Memilih diam-diam, tanpa menyebut bahwa ada bacaan lain. "
    "4. Batas waktu · yang gagal ikut atau tidak · yang kosong diapakan. "
    "5. Pilih satu, tulis alasannya dalam dua kalimat, lanjutkan.</p></details>")

HARI6 = {
  "n": "HARI 6", "tab": "6",
  "judul": "Soal yang sengaja ambigu, dan kenapa menjawabnya langsung itu kesalahan",
  "waktu": "± 60 menit",
  "tujuan": "mengenali pertanyaan yang punya lebih dari satu jawaban benar, dan "
            "<strong>membuktikan dengan angka</strong> bahwa bedanya dua kali lipat.",
  "langkah": L,
  "tutup_judul": "Hari 6 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> enam angka dari satu kalimat, tiga pertanyaan "
           "yang bisa kamu ajukan di detik pertama, dan satu kebiasaan menulis yang sebenarnya "
           "sudah kamu kuasai di pekerjaan lamamu.</p>"
           "<p style=\"margin-top:8px\">Besok ujian akhirnya: satu kalimat permintaan klien, dua "
           "jam, dan jawaban yang benar dimulai dengan <strong>menolak menjawabnya</strong>.</p>",
}
