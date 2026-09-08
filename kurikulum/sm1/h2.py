# -*- coding: utf-8 -*-
"""Hari 2 — tiga tempat NULL diam-diam mengubah hitunganmu."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Sambungkan ulang kalau Colab-mu sudah mati",
    blok("aksi", "Kalau sesi Colab kemarin masih hidup, lewati langkah ini. Kalau sudah mati, "
                 "jalankan.", "LAKUKAN"),
    kode('''import sqlite3, pandas as pd
con = sqlite3.connect("senja.db")
def q(sql): return pd.read_sql(sql, con)
q("SELECT COUNT(*) AS pesanan FROM pesanan")'''),
    blok("hasil", "<pre><code>   pesanan\n0      400</code></pre>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Kalau yang muncul <code>no such table: pesanan</code>, itu wajar</strong> "
                    "— Colab menghapus berkasnya kalau sesinya lama menganggur. Jalankan ulang "
                    "tujuh sel Hari 1, sekali berurutan, lalu kembali ke sini."))

langkah("Kesalahan yang tidak akan pernah memberimu tulisan merah",
    blok("aksi", "Sel baru. Kamu ingin daftar pelanggan yang kotanya belum tercatat. Ini cara "
                 "yang paling wajar ditulis orang.", "LAKUKAN"),
    kode('q("SELECT nama, kota FROM pelanggan WHERE kota = NULL")'),
    blok("hasil", "<pre><code>Empty DataFrame\nColumns: [nama, kota]\nIndex: []</code></pre>",
         "HARUS MUNCUL"),
    "<p>Kosong. Layarmu bersih — tidak ada tulisan merah, tidak ada peringatan. Kesimpulan yang wajar: "
    "<strong>“semua pelanggan sudah tercatat kotanya.”</strong></p>")

langkah("Sekarang tanya hal yang sama dengan cara yang benar",
    blok("aksi", "Sel baru. Ganti <code>= NULL</code> jadi <code>IS NULL</code>.", "LAKUKAN"),
    kode('q("SELECT nama, kota FROM pelanggan WHERE kota IS NULL")'),
    blok("hasil", "<pre><code>    nama  kota\n0   Rina  None\n1   Bayu  None\n2   Sari  None\n"
                  "3  Dimas  None\n4  Wawan  None\n5  Bagus  None</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Nol lawan enam.</strong> Kamu menanyakan hal yang sama dua kali dan mendapat dua "
    "jawaban. Dan yang salah adalah yang <em>tidak</em> merah.</p>")

langkah("Kenapa yang pertama kosong",
    blok("aksi", "Baca, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p><code>kota = NULL</code> bernilai <em>tidak diketahui</em> untuk setiap "
                  "baris — termasuk untuk baris yang kotanya memang <code>NULL</code>. Dan "
                  "<code>WHERE</code> hanya meloloskan baris yang syaratnya bernilai "
                  "<strong>benar</strong>.</p>", "SATU ATURAN YANG MENJELASKAN SEMUANYA"),
    blok("bahaya", "Satu-satunya cara memeriksa <code>NULL</code> adalah <code>IS NULL</code> "
                   "dan <code>IS NOT NULL</code>. <strong>Tidak pernah dengan <code>=</code> "
                   "atau <code>&lt;&gt;</code>.</strong>"))

langkah("Tebak dulu: berapa pelanggan yang kotanya bukan Jakarta?",
    blok("aksi", "Dari 20 pelanggan, enam kotanya belum tercatat. Tebak angkanya di kepalamu, "
                 "baru jalankan.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS bukan_jakarta FROM pelanggan
     WHERE kota <> 'Jakarta'""")'''),
    blok("hasil", "<pre><code>   bukan_jakarta\n0              8</code></pre>", "HARUS MUNCUL"),
    "<p>Delapan. Padahal hanya 6 pelanggan yang kotanya Jakarta — jadi seharusnya ada 14 yang "
    "bukan. Ke mana enam sisanya, dan apakah tebakanmu tadi mendekati?</p>")

langkah("Yang hilang adalah yang tidak diketahui",
    blok("aksi", "Sel baru. Tambahkan satu syarat.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS bukan_jakarta_lengkap FROM pelanggan
     WHERE kota <> 'Jakarta' OR kota IS NULL""")'''),
    blok("hasil", "<pre><code>   bukan_jakarta_lengkap\n0                     14</code></pre>",
         "HARUS MUNCUL"),
    "<p>Enam pelanggan yang kotanya <code>NULL</code> <strong>secara logika bisnis jelas bukan "
    "Jakarta</strong> — tapi <code>kota &lt;&gt; 'Jakarta'</code> membuang mereka.</p>",
    blok("catatan", "Kamu yang memutuskan mana yang benar untuk laporanmu: 8 (“yang terbukti "
                    "bukan Jakarta”) atau 14 (“yang tidak terbukti Jakarta”). Dua-duanya sah. "
                    "Yang tidak sah adalah <strong>tidak tahu mana yang sedang kamu pakai</strong>."))

langkah("Pemeriksaan kelengkapan yang paling murah yang kamu punya",
    blok("aksi", "Sel baru. Tiga cara menghitung, berdampingan.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*)             AS semua,
       COUNT(kota)          AS kota_terisi,
       COUNT(DISTINCT kota) AS kota_unik
     FROM pelanggan""")'''),
    blok("hasil", "<pre><code>   semua  kota_terisi  kota_unik\n0     20           14          3</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>COUNT(*)</code> menghitung <strong>baris</strong>. <code>COUNT(kota)</code> "
    "menghitung <strong>nilai yang bukan NULL</strong>. Selisihnya, 6, adalah jumlah yang belum "
    "lengkap — dan itu angka yang kamu dapat gratis, dalam satu query.</p>")

langkah("Jadikan ini kebiasaan sebelum menganalisis apa pun",
    blok("aksi", "Baca sekali. Ini yang paling sering kamu pakai di pekerjaan nyata.", "LAKUKAN"),
    blok("hasil", "<p>Jalankan <code>COUNT(*)</code> dan <code>COUNT(kolom)</code> berdampingan "
                  "untuk <strong>tiap kolom penting</strong> sebelum menghitung apa pun "
                  "darinya.</p>", "REFLEKS PERTAMA"),
    "<p>Kalau selisihnya besar, setiap rata-rata dan setiap pengelompokan yang memakai kolom itu "
    "berdiri di atas data yang tidak lengkap — <strong>dan tidak ada yang akan "
    "memberitahumu</strong>.</p>",
    blok("catatan", "Ini prosedur kelengkapan di kertas kerja audit, ditulis dalam SQL. Bedanya "
                    "cuma satu: di sini tidak ada partner yang menegur kalau kamu melewatinya."))

langkah("Rata-rata yang berbeda 40% dari data yang sama persis",
    blok("aksi", "Dua dari tujuh produk belum ada harga belinya. Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*)                              AS produk,
       COUNT(harga_beli)                     AS ada_harga_beli,
       ROUND(AVG(harga_beli),1)              AS avg_abaikan_null,
       ROUND(SUM(harga_beli)*1.0/COUNT(*),1) AS avg_anggap_nol
     FROM produk""")'''),
    blok("hasil", "<pre><code>   produk  ada_harga_beli  avg_abaikan_null  avg_anggap_nol\n"
                  "0       7               5            6200.0          4428.6</code></pre>",
         "HARUS MUNCUL"),
    "<p>6.200 lawan 4.428,6. Selisihnya 40%, dan kamu mendapatkannya dari tabel yang sama persis.</p>")

langkah("Mana yang benar — dan kenapa pertanyaan itu keliru",
    blok("aksi", "Baca tabelnya, lalu lanjut.", "LAKUKAN"),
    tabel(["Rumus", "Kalimat yang sebenarnya kamu ucapkan"],
          [["<code>AVG(harga_beli)</code> = 6.200",
            "“Rata-rata harga beli produk <strong>yang datanya sudah lengkap</strong>.”"],
           ["<code>SUM/COUNT(*)</code> = 4.428,6",
            "“Rata-rata harga beli <strong>seluruh produk</strong>, menganggap yang belum "
            "tercatat bernilai nol rupiah.”"]]),
    "<p>Tidak ada yang salah dari keduanya. Yang salah adalah tidak tahu mana yang sedang kamu "
    "pakai. <code>AVG</code> selalu memberimu yang pertama, diam-diam, tanpa pernah "
    "menyebutkannya.</p>")

langkah("Kalimat yang harus ikut ke dalam laporanmu",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("bahaya", "Kalau kamu melaporkan “rata-rata harga beli kami Rp 6.200” tanpa menyebut "
                   "bahwa dua produk belum tercatat, kamu memberi pernyataan yang "
                   "<strong>lebih pasti daripada yang didukung datanya</strong>."),
    "<p>Kamu sudah terlatih menghindari itu bertahun-tahun. Di SQL jebakannya cuma lebih "
    "tersembunyi, karena tidak ada kolom “catatan” yang otomatis muncul di sebelah angkanya.</p>")

langkah("NULL menular ke seluruh perhitungan",
    blok("aksi", "Sel baru. Hitung margin tiap produk.", "LAKUKAN"),
    kode('q("SELECT nama, harga - harga_beli AS margin FROM produk ORDER BY id")'),
    blok("hasil", "<pre><code>           nama   margin\n0     Kopi Susu  15000.0\n1     Americano  13000.0\n"
                  "2     Teh Manis   8000.0\n3    Roti Bakar   9000.0\n4     Croissant  14000.0\n"
                  "5    Cheesecake      NaN\n6  Matcha Latte      NaN</code></pre>", "HARUS MUNCUL"),
    "<p><code>30000 - NULL</code> bukan 30.000. Hasilnya <code>NULL</code>. Angka apa pun "
    "dikurangi “tidak diketahui” tetap tidak diketahui — <strong>dan itu memang jawaban yang "
    "paling jujur</strong>.</p>")

langkah("COALESCE: menampilkan yang kosong, bukan menyembunyikannya",
    blok("aksi", "Sel baru.", "LAKUKAN"),
    kode('''q("""SELECT nama, COALESCE(kota, 'BELUM TERCATAT') AS kota_tampil
     FROM pelanggan WHERE kota IS NULL""")'''),
    blok("hasil", "<pre><code>    nama     kota_tampil\n0   Rina  BELUM TERCATAT\n"
                  "1   Bayu  BELUM TERCATAT\n2   Sari  BELUM TERCATAT\n3  Dimas  BELUM TERCATAT\n"
                  "4  Wawan  BELUM TERCATAT\n5  Bagus  BELUM TERCATAT</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "<code>COALESCE(harga_beli, 0)</code> terlihat rapi dan "
                   "<strong>berbahaya</strong>: ia mengubah “tidak diketahui” jadi “nol rupiah”, "
                   "lalu angka itu ikut ke rata-rata seolah-olah fakta. Pakai COALESCE untuk "
                   "<em>label yang dilihat mata</em>, hampir tidak pernah untuk angka yang "
                   "dihitung."))

langkah("Urutan pun ikut terpengaruh",
    blok("aksi", "Sel baru. Urutkan dari harga beli termurah.", "LAKUKAN"),
    kode('q("SELECT nama, harga_beli FROM produk ORDER BY harga_beli LIMIT 4")'),
    blok("hasil", "<pre><code>           nama  harga_beli\n0    Cheesecake         NaN\n"
                  "1  Matcha Latte         NaN\n2     Teh Manis      2000.0\n"
                  "3     Americano      5000.0</code></pre>", "HARUS MUNCUL"),
    "<p>Dua produk yang harga belinya <strong>tidak diketahui</strong> menempati dua tempat teratas di layarmu — "
    "daftar “termurah”. Kalau kamu mengambil <code>LIMIT 3</code> untuk laporan “tiga "
    "produk paling murah”, dua dari tiga isinya karangan.</p>",
    blok("catatan", "SQLite dan PostgreSQL menaruh <code>NULL</code> di tempat berbeda saat "
                    "mengurutkan. Kalau urutan itu penting, tulis eksplisit: "
                    "<code>ORDER BY harga_beli IS NULL, harga_beli</code>."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis query yang menampilkan nama produk yang <code>harga_beli</code>-nya "
                 "belum terisi. Lalu jawab dengan suara: kalau kamu diminta menghitung margin "
                 "per produk, dua produk itu harus muncul sebagai margin nol, margin 100%, atau "
                 "tidak muncul sama sekali?", "KERJAKAN, ± 8 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>q(\"SELECT nama, harga, harga_beli FROM produk "
    "WHERE harga_beli IS NULL\")</code></pre></div>"
    "<pre><code>           nama  harga harga_beli\n0    Cheesecake  30000       None\n"
    "1  Matcha Latte  26000       None</code></pre>"
    "<p><strong>Tidak muncul sama sekali</strong> — dan disebutkan terpisah sebagai “2 produk "
    "belum bisa dihitung marginnya karena harga beli belum tercatat”. Margin nol itu bohong "
    "(seolah dijual rugi total), margin 100% juga bohong (seolah gratis). Yang benar adalah "
    "mengakui bahwa jawabannya belum ada, lalu memberitahu siapa yang harus melengkapi "
    "datanya.</p></details>")

HARI2 = {
  "n": "HARI 2", "tab": "2",
  "judul": "Tiga tempat NULL diam-diam mengubah hitunganmu",
  "waktu": "± 50 menit",
  "tujuan": "menyebut tiga tempat <code>NULL</code> mengubah hasil tanpa memberi peringatan, dan "
            "memakai <code>COUNT(*)</code> lawan <code>COUNT(kolom)</code> sebagai pemeriksaan "
            "kelengkapan.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>= NULL</code> selalu kosong · "
           "<code>&lt;&gt;</code> membuang yang <code>NULL</code> · <code>AVG</code> mengabaikan "
           "<code>NULL</code>, tidak menganggapnya nol · aritmetika apa pun dengan "
           "<code>NULL</code> menghasilkan <code>NULL</code> · dan <code>ORDER BY</code> pun ikut "
           "terpengaruh.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 2 dari 8.</strong> Jawab dengan "
           "suara: <em>kenapa <code>WHERE kota &lt;&gt; 'Jakarta'</code> tidak mengembalikan "
           "pelanggan yang kotanya <code>NULL</code>?</em></p>"
           "<details><summary>Kunci</summary><p>Karena <code>NULL &lt;&gt; 'Jakarta'</code> "
           "bernilai <em>tidak diketahui</em>, dan <code>WHERE</code> hanya meloloskan baris "
           "yang syaratnya bernilai benar.</p></details>",
}
