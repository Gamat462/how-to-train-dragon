# -*- coding: utf-8 -*-
"""Hari 5 — recursive CTE: hierarki, rantai, dan lingkaran."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Kenapa self join tidak cukup",
    blok("aksi", "Berkas <code>senja/l2-hari-5.sql</code>. Baca sekali dulu.", "LAKUKAN"),
    "<p>Di Level 1 Hari 5 kamu membaca pegawai dan atasannya dengan self join. Itu bekerja untuk "
    "<strong>satu tingkat</strong>. Untuk “siapa saja di bawah Bu Rina, berapa pun dalamnya”, "
    "kamu harus menambah JOIN untuk tiap tingkat — dan kamu tidak tahu ada berapa tingkat "
    "sampai kamu melihat datanya.</p>",
    blok("bahaya", "Kalau besok ada tingkat baru, query-mu <strong>diam-diam melewatkannya</strong>. "
                   "Tidak ada error, cuma orang yang hilang dari daftar."))

langkah("Lihat tabelnya apa adanya dulu",
    blok("aksi", "Sepuluh baris. Baca kolom ketiga.", "LAKUKAN"),
    kode("SELECT id, nama, id_atasan FROM pegawai ORDER BY id;"),
    keluaran(H, "h5_pegawai"),
    "<p>Kolom <code>id_atasan</code> menunjuk ke <code>id</code> di tabel yang sama. Bentuk yang "
    "sama persis kamu temui di bagan akun: akun 1101 anaknya 1101-01, dan kamu tidak pernah "
    "tahu ada berapa tingkat sampai kamu menelusurinya.</p>")

langkah("Berapa titik awal yang kamu punya",
    blok("aksi", "Satu baris. Ini menentukan dari mana penelusuranmu mulai.", "LAKUKAN"),
    kode("SELECT count(*) AS tanpa_atasan FROM pegawai WHERE id_atasan IS NULL;"),
    keluaran(H, "h5_akar"),
    "<p>Satu orang — Pak Hardi. Jadi pohonmu punya <strong>satu akar</strong>.</p>",
    blok("catatan", "Kalau angka ini <strong>nol</strong>, semua orang punya atasan dan itu "
                    "berarti datamu melingkar. Kalau <strong>lebih dari satu</strong>, kamu "
                    "punya beberapa pohon terpisah — bukan kesalahan, tapi harus kamu sebut di "
                    "laporan. Dua pemeriksaan sepuluh detik yang menghemat sejam kebingungan."))

langkah("Query yang memanggil dirinya sendiri",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH RECURSIVE pohon AS (
  -- 1. titik awal: yang tidak punya atasan
  SELECT id, nama, jabatan, id_atasan, 1 AS tingkat, nama AS jalur
  FROM pegawai WHERE id_atasan IS NULL
  UNION ALL
  -- 2. langkah berulang: ambil bawahan dari yang sudah ketemu
  SELECT p.id, p.nama, p.jabatan, p.id_atasan,
         t.tingkat + 1, t.jalur || ' > ' || p.nama
  FROM pegawai p JOIN pohon t ON p.id_atasan = t.id)
SELECT tingkat, nama, jabatan, jalur FROM pohon ORDER BY jalur;'''),
    keluaran(H, "h5_pohon"),
    "<p>Seluruh struktur organisasi, empat tingkat, dari satu query yang kamu tulis — dan "
    "query-nya <strong>tidak berubah</strong> kalau besok ada tingkat kelima. Kalau hasilmu "
    "lebih sedikit dari sepuluh baris, itu wajar cuma kalau ada pegawai yang "
    "<code>id_atasan</code>-nya menunjuk ke id yang tidak ada.</p>")

langkah("Tiga bagian yang harus ada, selalu",
    blok("aksi", "Salin ke catatanmu.", "LAKUKAN"),
    tabel(["Bagian", "Isinya", "Kalau salah"],
          [["1. Titik awal", "Baris yang bisa ditemukan tanpa mengulang — di sini: pegawai "
            "tanpa atasan", "Pohonnya kosong, atau mulai dari tempat yang keliru"],
           ["2. <code>UNION ALL</code>", "Penyambung antara titik awal dan langkah berulang",
            "<code>UNION</code> membuang baris yang kebetulan identik — cabang pohonmu terpotong"],
           ["3. Langkah berulang", "Bagian yang menyebut nama CTE-nya sendiri "
            "(<code>pohon</code>)", "Bukan recursive CTE lagi, cuma UNION biasa"]]),
    "<p>Kolom <code>tingkat</code> dan <code>jalur</code> tidak wajib, tapi hampir selalu "
    "berguna: <code>tingkat</code> memberi kedalaman, <code>jalur</code> memberi urutan tampil "
    "yang rapi lewat <code>ORDER BY jalur</code>.</p>")

langkah("Layar merah kalau kata RECURSIVE-nya hilang",
    blok("aksi", "Hapus kata <code>RECURSIVE</code>, jalankan.", "LAKUKAN"),
    kode('''WITH pohon AS (
  SELECT id, nama FROM pegawai WHERE id_atasan IS NULL
  UNION ALL
  SELECT p.id, p.nama FROM pegawai p JOIN pohon t ON p.id_atasan = t.id)
SELECT * FROM pohon;'''),
    keluaran(H, "h5_merah_tanpa_recursive"),
    "<p>Tanpa kata itu, PostgreSQL tidak mengizinkan CTE menyebut namanya sendiri — jadi "
    "<code>pohon</code> di baris keempat dianggap tabel yang tidak ada.</p>",
    blok("catatan", "<strong>SQLite menerima query ini tanpa kata <code>RECURSIVE</code>.</strong> "
                    "Kalau kamu pernah menulisnya begitu dan berhasil, itu kelonggaran SQLite. "
                    "PostgreSQL mewajibkannya — dan begitu juga standar SQL."))

langkah("Siapa yang akan kamu telusuri",
    blok("aksi", "Satu baris. Pastikan kamu menelusuri orang yang benar.", "LAKUKAN"),
    kode("SELECT id, nama, jabatan FROM pegawai WHERE id = 2;"),
    keluaran(H, "h5_siapa"),
    "<p>Bu Rina, Manajer Area. <strong>Selalu buktikan id yang kamu tulis di query menunjuk ke "
    "orang yang kamu maksud</strong> — menaruh angka 2 begitu saja di dalam query adalah cara "
    "paling mudah membuat laporan yang rapi tentang orang yang salah.</p>")

langkah("Mulai dari tengah, bukan dari puncak",
    blok("aksi", "Pertanyaan yang lebih sering muncul: “semua yang berada di bawah orang ini”. "
                 "Cukup ganti titik awalnya.", "LAKUKAN"),
    kode('''WITH RECURSIVE bawahan AS (
  SELECT id, nama, 0 AS jarak FROM pegawai WHERE id = 2      -- Bu Rina
  UNION ALL
  SELECT p.id, p.nama, b.jarak + 1
  FROM pegawai p JOIN bawahan b ON p.id_atasan = b.id)
SELECT nama, jarak FROM bawahan WHERE jarak > 0 ORDER BY jarak, nama;'''),
    keluaran(H, "h5_bawahan"),
    "<p>Delapan orang di bawah Bu Rina: tiga kepala cabang langsung, dan lima staf di bawah "
    "mereka. <code>WHERE jarak &gt; 0</code> membuang Bu Rina sendiri dari daftar.</p>")

langkah("Bahaya yang tidak akan diberitahu siapa pun: data yang melingkar",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("bahaya", "Andai A atasannya B <em>dan</em> B atasannya A, recursive CTE berputar "
                   "<strong>selamanya</strong> sampai memori habis. Query-mu tidak error — ia "
                   "menggantung."),
    "<p>Di data pegawai sungguhan hal itu terjadi lebih sering daripada dugaanmu, biasanya "
    "akibat salah input saat seseorang pindah jabatan.</p>")

langkah("Pengaman pertama, yang murah: batasi kedalamannya",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH RECURSIVE pohon AS (
  SELECT id, nama, 1 AS tingkat FROM pegawai WHERE id_atasan IS NULL
  UNION ALL
  SELECT p.id, p.nama, t.tingkat + 1
  FROM pegawai p JOIN pohon t ON p.id_atasan = t.id
  WHERE t.tingkat < 10)
SELECT max(tingkat) AS tingkat_terdalam, count(*) AS baris FROM pohon;'''),
    keluaran(H, "h5_batas"),
    "<p>Empat tingkat, sepuluh baris — jauh dari batas 10. <strong>Kalau hasilmu menyentuh "
    "tingkat 10, itu bukan hierarki yang dalam; itu lingkaran yang harus kamu laporkan</strong> "
    "— temuan, bukan bug yang kamu diamkan.</p>")

langkah("Pengaman kedua, yang tepat: klausa CYCLE",
    blok("aksi", "PostgreSQL 14 ke atas bisa mendeteksi lingkarannya sendiri. Ini contoh dengan "
                 "data yang sengaja melingkar: 1→2, 2→3, 3→1.", "LAKUKAN"),
    kode('''WITH RECURSIVE lingkar(a, b) AS (VALUES (1,2),(2,3),(3,1)),
jalan AS (
  SELECT a, b FROM lingkar WHERE a = 1
  UNION ALL
  SELECT l.a, l.b FROM lingkar l JOIN jalan j ON l.a = j.b)
CYCLE a SET terulang USING jejak
SELECT a, b, terulang FROM jalan;'''),
    keluaran(H, "h5_cycle"),
    "<p>Empat baris, lalu <strong>berhenti sendiri</strong>. Baris terakhir ditandai "
    "<code>terulang = true</code>: PostgreSQL mengenali bahwa <code>a = 1</code> sudah pernah "
    "dilewati, lalu menghentikan cabang itu.</p>",
    blok("catatan", "Bacanya: <code>CYCLE a SET terulang USING jejak</code> = “awasi kolom "
                    "<code>a</code>; kalau nilainya terulang, isi kolom <code>terulang</code> "
                    "dengan true, dan simpan riwayatnya di kolom <code>jejak</code>”. Tanpa "
                    "klausa ini, query di atas tidak akan pernah berhenti."))

langkah("Mana yang kamu pakai di pekerjaan nyata",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    tabel(["Cara", "Kelebihan", "Kekurangan"],
          [["<code>WHERE tingkat &lt; 10</code>", "Berjalan di semua mesin, mudah dijelaskan",
            "Kamu tidak tahu apakah 10 itu batas wajar atau lingkaran"],
           ["<code>CYCLE</code>", "Menandai <em>baris mana</em> yang melingkar, berhenti tepat "
            "waktu", "PostgreSQL 14 ke atas saja"]]),
    "<p>Pakai keduanya. Batas kedalaman adalah jaring pengaman; <code>CYCLE</code> adalah "
    "diagnosisnya — <strong>ia memberitahumu id mana yang salah input</strong>, dan itu yang "
    "bisa kamu laporkan.</p>")

langkah("Pola yang sama, di luar organisasi",
    blok("aksi", "Rantai rujukan pelanggan. Jalankan.", "LAKUKAN"),
    kode('''WITH RECURSIVE rantai AS (
  SELECT id, nama, 0 AS jarak FROM pelanggan WHERE id = 1     -- Rina
  UNION ALL
  SELECT p.id, p.nama, r.jarak + 1
  FROM pelanggan p JOIN rantai r ON p.id_perujuk = r.id
  WHERE r.jarak < 10)
SELECT nama, jarak FROM rantai WHERE jarak > 0 ORDER BY jarak, nama;'''),
    keluaran(H, "h5_rantai"),
    "<p>Hanya dua, dan keduanya jarak 1 — Agus dan Wawan tidak merujuk siapa pun lagi, jadi "
    "rantainya berhenti di situ.</p>",
    blok("catatan", "Bentuknya <strong>selalu sama</strong>: satu tabel yang menunjuk dirinya "
                    "sendiri. Kategori produk yang bersarang, komponen di dalam komponen, "
                    "balasan di dalam balasan komentar, akun di dalam akun di bagan akun — "
                    "semuanya recursive CTE."))

langkah("Kerjakan sendiri",
    blok("aksi", "Bukan lagi satu orang: tampilkan <strong>berapa pelanggan yang berada di tiap "
                 "jarak rujukan</strong>, dihitung dari semua orang yang datang sendiri "
                 "(<code>id_perujuk IS NULL</code>). Pakai batas kedalaman.",
         "KERJAKAN, ± 15 MENIT"),
    "<details><summary>Kunci jawaban</summary>"
    "<div class=\"kode\"><pre><code>WITH RECURSIVE rantai AS (\n"
    "  SELECT id, nama, 0 AS jarak, nama AS jalur FROM pelanggan WHERE id_perujuk IS NULL\n"
    "  UNION ALL\n"
    "  SELECT p.id, p.nama, r.jarak + 1, r.jalur || ' &gt; ' || p.nama\n"
    "  FROM pelanggan p JOIN rantai r ON p.id_perujuk = r.id\n"
    "  WHERE r.jarak &lt; 10)\n"
    "SELECT jarak, count(*) AS orang FROM rantai GROUP BY jarak ORDER BY jarak;</code></pre></div>"
    + keluaran(H, "h5_kunci", tag="HASILNYA") +
    "<p><strong>Pemeriksaanmu:</strong> jumlah seluruh kolom <code>orang</code> harus 20 — "
    "seluruh pelanggan, tidak lebih dan tidak kurang. Kalau lebih dari 20, ada yang terhitung "
    "dua kali dan kamu punya lingkaran. Kalau kurang, ada yang <code>id_perujuk</code>-nya "
    "menunjuk ke id yang tidak ada.</p>"
    "<p>Perhatikan bahwa titik awalnya sekarang <em>banyak baris</em> sekaligus, bukan satu. "
    "Recursive CTE tidak keberatan — ia menelusuri semua cabang serentak.</p></details>")

HARI5 = {
  "n": "HARI 5", "tab": "5",
  "judul": "Recursive CTE: hierarki, rantai, dan lingkaran",
  "waktu": "± 60 menit",
  "tujuan": "menulis query yang memanggil dirinya sendiri untuk menelusuri hubungan bertingkat, "
            "dan memasang dua pengaman supaya data yang melingkar tidak menggantung query-mu.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> recursive CTE = titik awal + <code>UNION ALL</code> "
           "+ langkah yang menyebut namanya sendiri · kata <code>RECURSIVE</code> wajib di "
           "PostgreSQL · bawa kolom tingkat/jarak dan jalur · pasang batas kedalaman, dan pakai "
           "<code>CYCLE</code> untuk tahu <em>baris mana</em> yang melingkar.</p>"
           "<p style=\"margin-top:8px\"><strong>Soal ingatan 5 dari 8.</strong> Jawab dengan "
           "suara: <em>tiga bagian wajib sebuah recursive CTE, dan satu pengaman yang harus "
           "selalu ada.</em></p>"
           "<details><summary>Kunci</summary><p>Titik awal, <code>UNION ALL</code> (bukan "
           "<code>UNION</code>), dan langkah berulang yang menyebut nama CTE-nya sendiri. "
           "Pengamannya: batas kedalaman (<code>WHERE tingkat &lt; 10</code>) supaya data yang "
           "melingkar tidak membuat query berputar selamanya — atau klausa <code>CYCLE</code>, "
           "yang sekaligus menunjukkan baris mana penyebabnya.</p></details>",
}
