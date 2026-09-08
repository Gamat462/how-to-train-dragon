# -*- coding: utf-8 -*-
"""Hari 5 — self join: satu tabel yang menunjuk dirinya sendiri."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Kolom yang menunjuk ke tabelnya sendiri",
    blok("aksi", "Sel baru. Lihat lima pelanggan pertama.", "LAKUKAN"),
    kode('q("SELECT id, nama, id_perujuk FROM pelanggan LIMIT 5")'),
    blok("hasil", "<pre><code>   id   nama id_perujuk\n0   1   Rina       None\n"
                  "1   2   Bayu       None\n2   3   Sari       None\n3   4  Dimas       None\n"
                  "4   5  Putri       None</code></pre>", "HARUS MUNCUL"),
    "<p><code>id_perujuk</code> berisi <code>id</code> dari tabel yang sama — siapa yang mengajak "
    "pelanggan ini datang. Lima orang pertama yang kamu lihat datang sendiri, jadi kolomnya "
    "<code>NULL</code>.</p>")

langkah("Layar merah kalau kamu lupa memberi nama",
    blok("aksi", "Sel baru. Gabungkan tabel itu dengan dirinya sendiri, tanpa alias.", "LAKUKAN"),
    kode('''q("""SELECT nama FROM pelanggan
     JOIN pelanggan ON pelanggan.id_perujuk = pelanggan.id""")'''),
    blok("hasil", "<pre><code>DatabaseError: Execution failed on sql '...': ambiguous column "
                  "name: nama</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Ada dua tabel bernama <code>pelanggan</code> di query yang kamu tulis, dan keduanya punya "
    "kolom <code>nama</code>. SQL tidak tahu sisi mana yang kamu maksud, dan ia menolak "
    "menebak.</p>",
    blok("catatan", "<strong>Alias bukan hiasan di sini.</strong> Di self join, alias adalah "
                    "satu-satunya hal yang membuat query-mu punya arti."))

langkah("Beri dua nama berbeda, dan query-nya jadi masuk akal",
    blok("aksi", "Sel baru. <code>p</code> untuk pelanggannya, <code>r</code> untuk perujuknya.",
         "LAKUKAN"),
    kode('''q("""SELECT p.nama AS pelanggan, r.nama AS perujuk
     FROM pelanggan p
     JOIN pelanggan r ON p.id_perujuk = r.id
     ORDER BY p.nama""")'''),
    blok("hasil", "<pre><code>  pelanggan perujuk\n0      Agus    Rina\n1    Hendra    Bayu\n"
                  "2     Intan   Dimas\n3      Lita   Dimas\n4      Vira    Maya\n"
                  "5     Wawan    Rina</code></pre>", "HARUS MUNCUL"),
    "<p><code>p</code> dan <code>r</code> adalah tabel yang sama, kamu baca dua kali dengan dua "
    "peran berbeda. Itu seluruh isi gagasan “self join”, dan kamu baru saja memakainya.</p>")

langkah("Enam baris dari dua puluh pelanggan",
    blok("aksi", "Sel baru. Hitung penyebutnya.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS semua_pelanggan,
       COUNT(id_perujuk) AS punya_perujuk
     FROM pelanggan""")'''),
    blok("hasil", "<pre><code>   semua_pelanggan  punya_perujuk\n0               20              6</code></pre>",
         "HARUS MUNCUL"),
    blok("bahaya", "Query di langkah 3 adalah <code>INNER JOIN</code>, jadi 14 pelanggan yang "
                   "<code>id_perujuk</code>-nya <code>NULL</code> <strong>hilang seluruhnya</strong>. "
                   "Kalau pertanyaannya “berapa persen pelanggan datang dari rujukan?”, "
                   "penyebutnya harus <strong>20</strong>, bukan 6 — jawabannya 30%, bukan 100%."))

langkah("Pola yang sama untuk hierarki, tapi dengan LEFT",
    blok("aksi", "Sel baru. Pegawai dan atasannya.", "LAKUKAN"),
    kode('''q("""SELECT b.nama, b.jabatan, a.nama AS atasan
     FROM pegawai b
     LEFT JOIN pegawai a ON b.id_atasan = a.id
     ORDER BY b.id""")'''),
    blok("hasil", "<pre><code>        nama        jabatan     atasan\n"
                  "0  Pak Hardi        Pemilik        NaN\n"
                  "1    Bu Rina   Manajer Area  Pak Hardi\n"
                  "2      Sinta  Kepala Cabang    Bu Rina\n"
                  "3      Bagus  Kepala Cabang    Bu Rina\n"
                  "4       Vira  Kepala Cabang    Bu Rina\n"
                  "5       Andi        Barista      Sinta\n"
                  "6       Tari        Barista      Sinta\n"
                  "7      Wawan        Barista      Bagus\n"
                  "8       Yoga          Kasir       Vira\n"
                  "9       Lita          Kasir      Sinta</code></pre>", "HARUS MUNCUL"),
    "<p>Sepuluh baris, semua pegawai muncul di layarmu. Pak Hardi atasannya <code>NaN</code> — "
    "dia pemiliknya, jadi memang tidak ada yang di atasnya.</p>")

langkah("Buktikan apa yang hilang kalau kamu pakai INNER",
    blok("aksi", "Sel baru. Hapus kata <code>LEFT</code>, lalu hitung barisnya.", "LAKUKAN"),
    kode('''q("""SELECT COUNT(*) AS baris FROM pegawai b
     JOIN pegawai a ON b.id_atasan = a.id""")'''),
    blok("hasil", "<pre><code>   baris\n0      9</code></pre>", "HARUS MUNCUL"),
    "<p>Sembilan, bukan sepuluh. <strong>Pemiliknya hilang dari daftar pegawai</strong> — dan "
    "kalau kamu tidak menghitung barisnya, tidak ada yang akan menyadarinya.</p>",
    blok("catatan", "Aturannya sederhana: pakai <code>LEFT</code> kalau baris tanpa pasangan "
                    "harus tetap muncul. Di daftar pegawai, orang yang tidak punya atasan tetap "
                    "pegawai."))

langkah("Batas alat ini, supaya kamu tahu kapan ia kurang",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Satu self join membaca <strong>satu tingkat</strong> ke atas. Untuk "
                  "“siapa saja yang berada di bawah Bu Rina, sampai berapa pun tingkatnya”, satu "
                  "self join tidak cukup.</p>", "YANG TIDAK BISA DILAKUKANNYA"),
    "<p>Yang dibutuhkan adalah <em>recursive CTE</em>, dan itu dibahas tuntas di Level 2. "
    "Mengenali batas alatmu sekarang lebih berguna daripada memaksakan alat yang salah "
    "nanti.</p>")

langkah("Nama yang sama di dua tabel bukan berarti orang yang sama",
    blok("aksi", "Sel baru. Gabungkan pelanggan dan pegawai lewat nama.", "LAKUKAN"),
    kode('''q("""SELECT pl.nama, pg.jabatan
     FROM pelanggan pl JOIN pegawai pg ON pl.nama = pg.nama""")'''),
    blok("hasil", "<pre><code>    nama        jabatan\n0   Yoga          Kasir\n1   Lita          Kasir\n"
                  "2   Tari        Barista\n3  Wawan        Barista\n4  Sinta  Kepala Cabang\n"
                  "5  Bagus  Kepala Cabang\n6   Vira  Kepala Cabang\n"
                  "7   Andi        Barista</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "Delapan baris yang terlihat bermakna dan <strong>sepenuhnya karangan</strong>. "
                   "Tabel <code>pelanggan</code> dan <code>pegawai</code> tidak punya kaitan apa "
                   "pun di basis data ini; namanya kebetulan diambil dari daftar yang sama."))

langkah("Nama bukan kunci",
    blok("aksi", "Baca sekali, lalu ucapkan dengan suara keras.", "LAKUKAN"),
    blok("hasil", "<p>Menggabungkan tabel lewat nama orang, nama perusahaan, atau nama produk "
                  "adalah <strong>salah satu sumber kesalahan paling umum di pekerjaan "
                  "nyata</strong>.</p>", "KALIMAT YANG DINILAI DI WAWANCARA"),
    "<p>Apalagi di Indonesia, di mana satu orang bisa punya satu kata nama saja dan ribuan orang "
    "punya nama yang sama. Gabungkan lewat <code>id</code>. Kalau tidak ada id bersama, "
    "<strong>itu temuan yang harus dilaporkan, bukan masalah yang diakali</strong>.</p>",
    blok("catatan", "Kamu sudah pernah menuliskan kalimat itu di kertas kerja: “data tidak dapat "
                    "ditelusuri karena tidak tersedia pengenal unik.” Kalimatnya sama, medianya "
                    "saja yang berbeda."))

langkah("Self join juga membandingkan periode",
    blok("aksi", "Sel baru. Bulan ini dibandingkan bulan lalu, di cabang Kemang.", "LAKUKAN"),
    kode('''q("""
WITH bulanan AS (
  SELECT cabang, substr(tanggal,1,7) AS bulan, COUNT(*) AS pesanan
  FROM pesanan WHERE status='selesai' GROUP BY cabang, bulan)
SELECT i.bulan, i.pesanan, l.pesanan AS bulan_lalu,
       i.pesanan - l.pesanan AS selisih
FROM bulanan i
LEFT JOIN bulanan l ON l.cabang = i.cabang
     AND l.bulan = strftime('%Y-%m', i.bulan || '-01', '-1 month')
WHERE i.cabang='Kemang' ORDER BY i.bulan
""")'''),
    blok("hasil", "<pre><code>     bulan  pesanan  bulan_lalu  selisih\n"
                  "0  2024-01       14         NaN      NaN\n"
                  "1  2024-02       20        14.0      6.0\n"
                  "2  2024-03       24        20.0      4.0\n"
                  "3  2024-04       16        24.0     -8.0\n"
                  "4  2024-05       28        16.0     12.0\n"
                  "5  2024-06       18        28.0    -10.0</code></pre>", "HARUS MUNCUL"),
    "<p>Tabel yang sama, kamu baca dua kali: sekali sebagai “bulan ini”, sekali sebagai “bulan "
    "lalu”. Polanya sama persis dengan perujuk tadi.</p>")

langkah("Baca baris pertamanya, jangan lewati",
    blok("aksi", "Lihat baris <code>2024-01</code> di atas.", "LAKUKAN"),
    blok("hasil", "<p><code>bulan_lalu</code> dan <code>selisih</code>-nya <code>NaN</code>. "
                  "<strong>Itu benar</strong> — Desember 2023 tidak ada di data, jadi selisihnya "
                  "memang tidak diketahui.</p>", "YANG HARUS TERLIHAT"),
    "<p>Kalau kamu menaruh <code>COALESCE(selisih, 0)</code> di situ supaya “rapi”, kamu baru "
    "saja melaporkan bahwa Januari <em>tidak berubah</em> dari bulan sebelumnya — padahal kamu "
    "tidak tahu.</p>",
    blok("catatan", "Level 2 memperkenalkan <code>LAG()</code>, yang mengerjakan hal yang sama "
                    "dengan satu baris. Tapi self join tetap perlu kamu kuasai: ia satu-satunya "
                    "cara kalau syarat pasangannya lebih rumit daripada “baris sebelumnya”."))

langkah("Kerjakan sendiri",
    blok("aksi", "Tulis query yang menjawab: <strong>siapa yang paling banyak merujuk "
                 "pelanggan lain, dan berapa orang?</strong> Urutkan dari yang terbanyak.",
         "KERJAKAN, ± 10 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>q(\"\"\"SELECT r.nama AS perujuk, COUNT(*) AS jumlah_dirujuk\n"
    "     FROM pelanggan p JOIN pelanggan r ON p.id_perujuk = r.id\n"
    "     GROUP BY r.nama ORDER BY jumlah_dirujuk DESC, r.nama\"\"\")</code></pre></div>"
    "<pre><code>  perujuk  jumlah_dirujuk\n0   Dimas               2\n1    Rina               2\n"
    "2    Bayu               1\n3    Maya               1</code></pre>"
    "<p>Empat orang merujuk, total enam rujukan — cocok dengan angka <code>punya_perujuk</code> "
    "di langkah 4. Itu pemeriksaanmu.</p>"
    "<p>Perhatikan <code>ORDER BY jumlah_dirujuk DESC, r.nama</code>: kunci kedua itu bukan "
    "hiasan. Dimas dan Rina sama-sama 2, dan tanpa kunci kedua urutannya bisa berubah tiap kali "
    "query dijalankan. Laporan yang urutannya berubah sendiri akan membuat orang meragukan "
    "seluruh isinya.</p></details>")

HARI5 = {
  "n": "HARI 5", "tab": "5",
  "judul": "Self join: satu tabel yang menunjuk dirinya sendiri",
  "waktu": "± 55 menit",
  "tujuan": "menggabungkan sebuah tabel dengan dirinya sendiri untuk membaca hubungan antar "
            "barisnya — perujuk, atasan, dan perbandingan antar periode.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> self join = tabel yang sama, dua alias berbeda · "
           "pakai <code>LEFT</code> kalau baris tanpa pasangan harus tetap muncul · satu self "
           "join membaca satu tingkat saja · dan jangan pernah menggabungkan tabel lewat nama "
           "orang.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 5 dari 8.</strong> Jawab dengan "
           "suara: <em>kenapa CTE lebih mudah dibaca daripada subquery bersarang?</em> "
           "(ulangan dari M6)</p>"
           "<details><summary>Kunci</summary><p>CTE dibaca dari atas ke bawah seperti resep, dan "
           "tiap langkahnya punya nama yang bisa kamu sebut. Subquery bersarang dibaca dari "
           "dalam ke luar, dan bagian-bagiannya tidak punya nama.</p></details>",
}
