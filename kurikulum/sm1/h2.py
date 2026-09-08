# -*- coding: utf-8 -*-
"""Hari 2 — tiga tempat NULL diam-diam mengubah hitunganmu (PostgreSQL)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buka berkas baru untuk hari ini",
    blok("aksi", "Di VS Code, buat <code>senja/hari-2.sql</code>. Semua query hari ini masuk "
                 "ke berkas itu, dipisahkan titik koma.", "LAKUKAN"),
    kode("-- Hari 2: NULL\nSELECT count(*) AS pesanan FROM pesanan;"),
    blok("hasil", "<p>Satu baris, satu kolom, isinya <strong>400</strong>.</p>",
         "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Kalau muncul <code>relation \"pesanan\" does not exist</code>, itu "
                    "wajar</strong> — sambunganmu sedang menunjuk ke basis data yang salah. "
                    "Periksa isian <em>Database</em> di sambungan SQLTools-mu: harus "
                    "<code>senja</code>, bukan <code>postgres</code>."))

langkah("Kesalahan yang tidak akan pernah memberimu tulisan merah",
    blok("aksi", "Kamu ingin daftar pelanggan yang kotanya belum tercatat. Ini cara yang "
                 "paling wajar ditulis orang.", "LAKUKAN"),
    kode("SELECT nama, kota FROM pelanggan WHERE kota = NULL;"),
    keluaran(H, "h2_sama_null"),
    "<p>Kosong. Layarmu bersih — tidak ada tulisan merah, tidak ada peringatan. Kesimpulan yang "
    "wajar: <strong>“semua pelanggan sudah tercatat kotanya.”</strong></p>")

langkah("Sekarang tanya hal yang sama dengan cara yang benar",
    blok("aksi", "Ganti <code>= NULL</code> jadi <code>IS NULL</code>.", "LAKUKAN"),
    kode("SELECT nama, kota FROM pelanggan WHERE kota IS NULL;"),
    keluaran(H, "h2_is_null"),
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
    kode("SELECT count(*) AS bukan_jakarta FROM pelanggan WHERE kota <> 'Jakarta';"),
    keluaran(H, "h2_bukan_jkt"),
    "<p>Delapan. Padahal hanya 6 pelanggan yang kotanya Jakarta — jadi seharusnya ada 14 yang "
    "bukan. Ke mana enam sisanya, dan apakah tebakanmu tadi mendekati?</p>")

langkah("Yang hilang adalah yang tidak diketahui",
    blok("aksi", "Tambahkan satu syarat.", "LAKUKAN"),
    kode('''SELECT count(*) AS bukan_jakarta_lengkap FROM pelanggan
WHERE kota <> 'Jakarta' OR kota IS NULL;'''),
    keluaran(H, "h2_bukan_jkt_lengkap"),
    "<p>Enam pelanggan yang kotanya <code>NULL</code> <strong>secara logika bisnis jelas bukan "
    "Jakarta</strong> — tapi <code>kota &lt;&gt; 'Jakarta'</code> membuang mereka.</p>",
    blok("catatan", "Kamu yang memutuskan mana yang benar untuk laporanmu: 8 (“yang terbukti "
                    "bukan Jakarta”) atau 14 (“yang tidak terbukti Jakarta”). Dua-duanya sah. "
                    "Yang tidak sah adalah <strong>tidak tahu mana yang sedang kamu pakai</strong>."))

langkah("Pemeriksaan kelengkapan yang paling murah yang kamu punya",
    blok("aksi", "Tiga cara menghitung, berdampingan.", "LAKUKAN"),
    kode('''SELECT count(*)             AS semua,
       count(kota)          AS kota_terisi,
       count(DISTINCT kota) AS kota_unik
FROM pelanggan;'''),
    keluaran(H, "h2_count"),
    "<p><code>count(*)</code> menghitung <strong>baris</strong>. <code>count(kota)</code> "
    "menghitung <strong>nilai yang bukan NULL</strong>. Selisihnya, 6, adalah jumlah yang belum "
    "lengkap — dan itu angka yang kamu dapat gratis, dalam satu query.</p>")

langkah("Jadikan ini kebiasaan sebelum menganalisis apa pun",
    blok("aksi", "Baca sekali. Ini yang paling sering kamu pakai di pekerjaan nyata.", "LAKUKAN"),
    blok("hasil", "<p>Jalankan <code>count(*)</code> dan <code>count(kolom)</code> berdampingan "
                  "untuk <strong>tiap kolom penting</strong> sebelum menghitung apa pun "
                  "darinya.</p>", "REFLEKS PERTAMA"),
    "<p>Kalau selisihnya besar, setiap rata-rata dan setiap pengelompokan yang memakai kolom itu "
    "berdiri di atas data yang tidak lengkap — <strong>dan tidak ada yang akan "
    "memberitahumu</strong>.</p>",
    blok("catatan", "Ini prosedur kelengkapan di kertas kerja audit, ditulis dalam SQL. Bedanya "
                    "cuma satu: di sini tidak ada partner yang menegur kalau kamu melewatinya."))

langkah("Rata-rata yang berbeda 40% dari data yang sama persis",
    blok("aksi", "Dua dari tujuh produk belum ada harga belinya. Jalankan.", "LAKUKAN"),
    kode('''SELECT count(*)          AS produk,
       count(harga_beli) AS ada_harga_beli,
       round(avg(harga_beli), 1)                     AS avg_abaikan_null,
       round(sum(harga_beli)::numeric / count(*), 1) AS avg_anggap_nol
FROM produk;'''),
    keluaran(H, "h2_avg"),
    "<p>6.200 lawan 4.428,6. Selisihnya 40%, dan kamu mendapatkannya dari tabel yang sama "
    "persis.</p>",
    blok("catatan", "<code>::numeric</code> itu <strong>pemaksaan tipe</strong> khas PostgreSQL. "
                    "Tanpa itu, <code>round(angka_pecahan, 1)</code> ditolak dengan "
                    "<code>function round(double precision, integer) does not exist</code> — "
                    "salah satu error yang paling sering menyambut pendatang dari SQLite."))

langkah("Mana yang benar — dan kenapa pertanyaan itu keliru",
    blok("aksi", "Baca tabelnya, lalu lanjut.", "LAKUKAN"),
    tabel(["Rumus", "Kalimat yang sebenarnya kamu ucapkan"],
          [["<code>avg(harga_beli)</code> = 6.200",
            "“Rata-rata harga beli produk <strong>yang datanya sudah lengkap</strong>.”"],
           ["<code>sum / count(*)</code> = 4.428,6",
            "“Rata-rata harga beli <strong>seluruh produk</strong>, menganggap yang belum "
            "tercatat bernilai nol rupiah.”"]]),
    "<p>Tidak ada yang salah dari keduanya. Yang salah adalah tidak tahu mana yang sedang kamu "
    "pakai. <code>avg</code> selalu memberimu yang pertama, diam-diam, tanpa pernah "
    "menyebutkannya.</p>")

langkah("Kalimat yang harus ikut ke dalam laporanmu",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("bahaya", "Kalau kamu melaporkan “rata-rata harga beli kami Rp 6.200” tanpa menyebut "
                   "bahwa dua produk belum tercatat, kamu memberi pernyataan yang "
                   "<strong>lebih pasti daripada yang didukung datanya</strong>."),
    "<p>Kamu sudah terlatih menghindari itu bertahun-tahun. Di SQL jebakannya cuma lebih "
    "tersembunyi, karena tidak ada kolom “catatan” yang otomatis muncul di sebelah angkanya.</p>")

langkah("NULL menular ke seluruh perhitungan",
    blok("aksi", "Hitung margin tiap produk.", "LAKUKAN"),
    kode("SELECT nama, harga - harga_beli AS margin FROM produk ORDER BY id;"),
    keluaran(H, "h2_margin"),
    "<p><code>30000 - NULL</code> bukan 30.000. Hasilnya <code>NULL</code>. Angka apa pun "
    "dikurangi “tidak diketahui” tetap tidak diketahui — <strong>dan itu memang jawaban yang "
    "paling jujur</strong>.</p>")

langkah("COALESCE: menampilkan yang kosong, bukan menyembunyikannya",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''SELECT nama, COALESCE(kota, 'BELUM TERCATAT') AS kota_tampil
FROM pelanggan WHERE kota IS NULL;'''),
    keluaran(H, "h2_coalesce"),
    blok("bahaya", "<code>COALESCE(harga_beli, 0)</code> terlihat rapi dan "
                   "<strong>berbahaya</strong>: ia mengubah “tidak diketahui” jadi “nol rupiah”, "
                   "lalu angka itu ikut ke rata-rata seolah-olah fakta. Pakai COALESCE untuk "
                   "<em>label yang dilihat mata</em>, hampir tidak pernah untuk angka yang "
                   "dihitung."))

langkah("Urutan pun ikut terpengaruh — dan di sini PostgreSQL berbeda dari SQLite",
    blok("aksi", "Urutkan dari harga beli termurah.", "LAKUKAN"),
    kode("SELECT nama, harga_beli FROM produk ORDER BY harga_beli LIMIT 4;"),
    keluaran(H, "h2_urut_null"),
    "<p>Empat produk termurah, dan kelihatannya benar. Tapi PostgreSQL menaruh "
    "<code>NULL</code> <strong>di paling bawah</strong> saat mengurutkan menaik — jadi dua "
    "produk yang harga belinya tidak diketahui tersembunyi di ujung yang tidak kamu lihat.</p>")

langkah("Buktikan di mana NULL-nya bersembunyi",
    blok("aksi", "Tambahkan dua kata.", "LAKUKAN"),
    kode("SELECT nama, harga_beli FROM produk ORDER BY harga_beli NULLS FIRST LIMIT 4;"),
    keluaran(H, "h2_urut_null_first"),
    blok("bahaya", "Dua produk yang harga belinya <strong>tidak diketahui</strong> sekarang "
                   "menempati dua tempat teratas daftar “termurah”. Kalau kamu mengambil "
                   "<code>LIMIT 3</code> dari query ini untuk laporan “tiga produk paling "
                   "murah”, dua dari tiga isinya karangan."),
    blok("catatan", "<strong>SQLite menaruh <code>NULL</code> di atas, PostgreSQL di bawah.</strong> "
                    "Query yang sama, urutan berbeda. Kalau urutan itu penting bagi laporanmu, "
                    "tulis eksplisit: <code>NULLS FIRST</code> atau <code>NULLS LAST</code> — "
                    "lalu ia benar di mesin mana pun."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis query yang menampilkan nama produk yang <code>harga_beli</code>-nya "
                 "belum terisi. Lalu jawab dengan suara: kalau kamu diminta menghitung margin "
                 "per produk, dua produk itu harus muncul sebagai margin nol, margin 100%, atau "
                 "tidak muncul sama sekali?", "KERJAKAN, ± 8 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>SELECT nama, harga, harga_beli FROM produk\n"
    "WHERE harga_beli IS NULL;</code></pre></div>"
    + keluaran(H, "h2_kunci", tag="HASILNYA") +
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
            "memakai <code>count(*)</code> lawan <code>count(kolom)</code> sebagai pemeriksaan "
            "kelengkapan.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> <code>= NULL</code> selalu kosong · "
           "<code>&lt;&gt;</code> membuang yang <code>NULL</code> · <code>avg</code> mengabaikan "
           "<code>NULL</code>, tidak menganggapnya nol · aritmetika apa pun dengan "
           "<code>NULL</code> menghasilkan <code>NULL</code> · dan <code>ORDER BY</code> menaruh "
           "<code>NULL</code> di bawah — kecuali kamu menulis <code>NULLS FIRST</code>.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 2 dari 8.</strong> Jawab dengan "
           "suara: <em>kenapa <code>WHERE kota &lt;&gt; 'Jakarta'</code> tidak mengembalikan "
           "pelanggan yang kotanya <code>NULL</code>?</em></p>"
           "<details><summary>Kunci</summary><p>Karena <code>NULL &lt;&gt; 'Jakarta'</code> "
           "bernilai <em>tidak diketahui</em>, dan <code>WHERE</code> hanya meloloskan baris "
           "yang syaratnya bernilai benar.</p></details>",
}
