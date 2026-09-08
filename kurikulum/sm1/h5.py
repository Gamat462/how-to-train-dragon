# -*- coding: utf-8 -*-
"""Hari 5 — self join, dan DISTINCT ON milik PostgreSQL."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Kolom yang menunjuk ke tabelnya sendiri",
    blok("aksi", "Berkas <code>senja/hari-5.sql</code>. Lihat lima pelanggan pertama.",
         "LAKUKAN"),
    kode("SELECT id, nama, id_perujuk FROM pelanggan ORDER BY id LIMIT 5;"),
    keluaran(H, "h5_kolom"),
    "<p><code>id_perujuk</code> berisi <code>id</code> dari tabel yang sama — siapa yang mengajak "
    "pelanggan ini datang. Lima orang pertama yang kamu lihat datang sendiri, jadi kolomnya "
    "<code>NULL</code>.</p>")

langkah("Layar merah kalau kamu lupa memberi nama",
    blok("aksi", "Gabungkan tabel itu dengan dirinya sendiri, tanpa alias.", "LAKUKAN"),
    kode("SELECT nama FROM pelanggan\nJOIN pelanggan ON pelanggan.id_perujuk = pelanggan.id;"),
    keluaran(H, "h5_merah_alias"),
    "<p>PostgreSQL menolak sebelum sempat bingung soal kolom: <strong>satu nama tabel tidak "
    "boleh muncul dua kali</strong> dalam satu <code>FROM</code>.</p>",
    blok("catatan", "<strong>Alias bukan hiasan di sini.</strong> Di self join, alias adalah "
                    "satu-satunya hal yang membuat query-mu punya arti."))

langkah("Beri dua nama berbeda, dan query-nya jadi masuk akal",
    blok("aksi", "<code>p</code> untuk pelanggannya, <code>r</code> untuk perujuknya.",
         "LAKUKAN"),
    kode('''SELECT p.nama AS pelanggan, r.nama AS perujuk
FROM pelanggan p JOIN pelanggan r ON p.id_perujuk = r.id
ORDER BY p.nama;'''),
    keluaran(H, "h5_perujuk"),
    "<p><code>p</code> dan <code>r</code> adalah tabel yang sama, kamu baca dua kali dengan dua "
    "peran berbeda. Itu seluruh isi gagasan “self join”, dan kamu baru saja memakainya.</p>")

langkah("Enam baris dari dua puluh pelanggan",
    blok("aksi", "Hitung penyebutnya.", "LAKUKAN"),
    kode("SELECT count(*) AS semua_pelanggan, count(id_perujuk) AS punya_perujuk\nFROM pelanggan;"),
    keluaran(H, "h5_penyebut"),
    blok("bahaya", "Query di langkah 3 adalah <code>INNER JOIN</code>, jadi 14 pelanggan yang "
                   "<code>id_perujuk</code>-nya <code>NULL</code> <strong>hilang "
                   "seluruhnya</strong>. Kalau pertanyaannya “berapa persen pelanggan datang "
                   "dari rujukan?”, penyebutnya harus <strong>20</strong>, bukan 6 — jawabannya "
                   "30%, bukan 100%."))

langkah("Pola yang sama untuk hierarki, tapi dengan LEFT",
    blok("aksi", "Pegawai dan atasannya.", "LAKUKAN"),
    kode('''SELECT b.nama, b.jabatan, a.nama AS atasan
FROM pegawai b LEFT JOIN pegawai a ON b.id_atasan = a.id
ORDER BY b.id;'''),
    keluaran(H, "h5_hierarki"),
    "<p>Sepuluh baris, semua pegawai muncul di layarmu. Pak Hardi atasannya <code>NULL</code> — "
    "dia pemiliknya, jadi memang tidak ada yang di atasnya.</p>")

langkah("Buktikan apa yang hilang kalau kamu pakai INNER",
    blok("aksi", "Hapus kata <code>LEFT</code>, lalu hitung barisnya.", "LAKUKAN"),
    kode("SELECT count(*) AS baris FROM pegawai b\nJOIN pegawai a ON b.id_atasan = a.id;"),
    keluaran(H, "h5_inner"),
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
    blok("aksi", "Gabungkan pelanggan dan pegawai lewat nama.", "LAKUKAN"),
    kode('''SELECT pl.nama, pg.jabatan
FROM pelanggan pl JOIN pegawai pg ON pl.nama = pg.nama;'''),
    keluaran(H, "h5_nama_bukan_kunci"),
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
    blok("aksi", "Bulan ini dibandingkan bulan lalu, di cabang Kemang.", "LAKUKAN"),
    kode('''WITH bulanan AS (
  SELECT cabang, to_char(tanggal, 'YYYY-MM') AS bulan, count(*) AS pesanan
  FROM pesanan WHERE status = 'selesai' GROUP BY cabang, 2)
SELECT i.bulan, i.pesanan, l.pesanan AS bulan_lalu,
       i.pesanan - l.pesanan AS selisih
FROM bulanan i
LEFT JOIN bulanan l ON l.cabang = i.cabang
     AND l.bulan = to_char(to_date(i.bulan,'YYYY-MM') - INTERVAL '1 month','YYYY-MM')
WHERE i.cabang = 'Kemang' ORDER BY i.bulan;'''),
    keluaran(H, "h5_antar_bulan"),
    "<p>Tabel yang sama, kamu baca dua kali: sekali sebagai “bulan ini”, sekali sebagai “bulan "
    "lalu”. Polanya sama persis dengan perujuk tadi.</p>",
    blok("catatan", "<code>to_char</code>, <code>to_date</code>, dan <code>INTERVAL</code> adalah "
                    "cara PostgreSQL bekerja dengan tanggal. SQLite memakai "
                    "<code>strftime</code> dan <code>date(d,'-1 month')</code> — nama yang "
                    "berbeda untuk gagasan yang sama, dan salah satu hal pertama yang harus kamu "
                    "cari waktu pindah mesin."))

langkah("Baca baris pertamanya, jangan lewati",
    blok("aksi", "Lihat baris <code>2024-01</code> di atas.", "LAKUKAN"),
    blok("hasil", "<p><code>bulan_lalu</code> dan <code>selisih</code>-nya <code>NULL</code>. "
                  "<strong>Itu benar</strong> — Desember 2023 tidak ada di data, jadi selisihnya "
                  "memang tidak diketahui.</p>", "YANG HARUS TERLIHAT"),
    "<p>Kalau kamu menaruh <code>COALESCE(selisih, 0)</code> di situ supaya “rapi”, kamu baru "
    "saja melaporkan bahwa Januari <em>tidak berubah</em> dari bulan sebelumnya — padahal kamu "
    "tidak tahu.</p>",
    blok("catatan", "Level 2 memperkenalkan <code>LAG()</code>, yang mengerjakan hal yang sama "
                    "dengan satu baris. Tapi self join tetap perlu kamu kuasai: ia satu-satunya "
                    "cara kalau syarat pasangannya lebih rumit daripada “baris sebelumnya”."))

langkah("Satu alat PostgreSQL yang tidak ada di SQLite: DISTINCT ON",
    blok("aksi", "“Ambil pesanan terakhir tiap pelanggan” — soal yang muncul di hampir setiap "
                 "wawancara. Di PostgreSQL ada jalan pintas.", "LAKUKAN"),
    kode('''SELECT DISTINCT ON (pelanggan_id)
       pelanggan_id, id AS pesanan_terakhir, tanggal, cabang
FROM pesanan
WHERE pelanggan_id IS NOT NULL AND status = 'selesai'
ORDER BY pelanggan_id, tanggal DESC, id DESC
LIMIT 6;'''),
    keluaran(H, "h5_distinct_on"),
    "<p><code>DISTINCT ON (pelanggan_id)</code> berarti “satu baris saja per "
    "<code>pelanggan_id</code>” — dan baris <strong>mana</strong> yang diambil ditentukan oleh "
    "<code>ORDER BY</code>-nya.</p>")

langkah("Aturan wajib DISTINCT ON, dan kenapa itu bukan formalitas",
    blok("aksi", "Baca, lalu jalankan pemeriksaannya.", "LAKUKAN"),
    blok("hasil", "<p><code>ORDER BY</code> <strong>harus</strong> dimulai dengan kolom yang "
                  "sama seperti di <code>DISTINCT ON</code>. Sisanya menentukan siapa yang "
                  "menang.</p>", "SATU ATURAN"),
    kode('''SELECT count(*) AS pesanan_pada_tanggal_kembar FROM (
  SELECT pelanggan_id, tanggal, count(*) AS n
  FROM pesanan WHERE pelanggan_id IS NOT NULL AND status='selesai'
  GROUP BY pelanggan_id, tanggal HAVING count(*) > 1) x;'''),
    keluaran(H, "h5_distinct_on_tanpa_pemecah"),
    blok("bahaya", "Ada <strong>19</strong> pasangan pelanggan–tanggal yang punya lebih dari satu "
                   "pesanan. Kalau <code>ORDER BY</code>-mu berhenti di <code>tanggal DESC</code> "
                   "saja, siapa yang menang di 19 kasus itu <strong>ditentukan mesin, dan bisa "
                   "berubah antar-jalankan</strong>. Karena itu ada <code>, id DESC</code> di "
                   "belakangnya: pemecah seri, supaya hasilmu bisa direproduksi besok."))

HARI5 = {
  "n": "HARI 5", "tab": "5",
  "judul": "Self join, dan satu jalan pintas milik PostgreSQL",
  "waktu": "± 55 menit",
  "tujuan": "menggabungkan sebuah tabel dengan dirinya sendiri untuk membaca hubungan antar "
            "barisnya, dan memakai <code>DISTINCT ON</code> untuk mengambil satu baris per "
            "kelompok.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> self join = tabel yang sama, dua alias berbeda · "
           "pakai <code>LEFT</code> kalau baris tanpa pasangan harus tetap muncul · satu self "
           "join membaca satu tingkat saja · jangan pernah menggabungkan tabel lewat nama orang · "
           "dan <code>DISTINCT ON</code> selalu butuh pemecah seri di <code>ORDER BY</code>-nya.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 5 dari 8.</strong> Jawab dengan "
           "suara: <em>kenapa CTE lebih mudah dibaca daripada subquery bersarang?</em> "
           "(ulangan dari M6)</p>"
           "<details><summary>Kunci</summary><p>CTE dibaca dari atas ke bawah seperti resep, dan "
           "tiap langkahnya punya nama yang bisa kamu sebut. Subquery bersarang dibaca dari "
           "dalam ke luar, dan bagian-bagiannya tidak punya nama.</p></details>",
}
