# -*- coding: utf-8 -*-
"""Hari 7 — ulangan dari ingatan dan satu soal terapan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

def soal(n, tanya, jawab):
    langkah(f"Soal {n} dari 8",
        blok("aksi", f"<strong>{tanya}</strong> Jawab dengan suara keras, jangan dalam hati. "
                     "Baru buka kuncinya.", "JAWAB DULU"),
        f"<details><summary>Kunci soal {n}</summary><p>{jawab}</p></details>")

langkah("Aturan main hari ini",
    blok("aksi", "Tutup semua berkas <code>.sql</code>-mu. Tidak ada materi baru hari ini.",
         "LAKUKAN"),
    blok("hasil", "<p>Delapan soal, dijawab <strong>dengan suara</strong>. Lalu satu soal "
                  "terapan yang dikerjakan di VS Code, di bawah pengatur waktu.</p>",
         "YANG TERJADI HARI INI"),
    blok("bahaya", "<strong>Menjawab dalam hati tidak sama dengan menjawab.</strong> Di "
                   "wawancara kamu harus mengeluarkannya sebagai kalimat, sambil orang lain "
                   "menatapmu. Latih bagian itu, bukan cuma bagian tahunya."))

soal(1, "Satu kalimat: apa beda <code>GROUP BY</code> dan window function?",
     "<code>GROUP BY</code> meringkas banyak baris jadi satu; window function menghitung hal "
     "yang sama <strong>tanpa membuang baris</strong>.")

soal(2, "Apa yang berubah kalau kamu menambahkan <code>ORDER BY</code> ke dalam "
        "<code>OVER (PARTITION BY x)</code>?",
     "Selain mengurutkan, ia diam-diam memasang frame “dari awal kelompok sampai baris ini” — "
     "jadi <strong>total berubah menjadi running total</strong>.")

soal(3, "Frame apa yang jadi bawaan kalau ada <code>ORDER BY</code> tapi frame-nya tidak ditulis?",
     "<code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code> — bukan <code>ROWS</code>. "
     "Bedanya baru terasa kalau ada nilai seri di kolom <code>ORDER BY</code>-nya.")

soal(4, "Running total per tanggal, tiap tanggal punya 3 baris cabang. <code>ROWS</code> atau "
        "<code>RANGE</code>, dan kenapa?",
     "<code>RANGE</code>. Ketiga baris satu tanggal mendapat angka yang sama, yaitu kumulatif "
     "sampai <em>akhir</em> tanggal itu. <code>ROWS</code> memberi tiga angka berbeda yang "
     "bergantung pada urutan cabang — angka yang tidak menjawab pertanyaan siapa pun, dan bisa "
     "berubah kalau urutannya berubah.")

soal(5, "Kenapa <code>last_value(x) OVER (ORDER BY x)</code> tidak memberi nilai terakhir? "
        "Sebutkan dua cara memperbaikinya.",
     "Karena frame bawaannya berakhir di baris yang sedang dihitung, jadi “nilai terakhir dalam "
     "frame” adalah baris itu sendiri. Perbaikan: tulis "
     "<code>ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING</code>, atau balik "
     "urutannya dan pakai <code>first_value</code>.")

soal(6, "Nilai 30, 20, 20, 10. Berapa nomor untuk baris terakhir menurut <code>row_number</code>, "
        "<code>rank</code>, dan <code>dense_rank</code>?",
     "<code>row_number</code> = 4, <code>rank</code> = 4 (melompat, karena dua baris berbagi "
     "peringkat 2), <code>dense_rank</code> = 3.")

soal(7, "Tiga bagian wajib sebuah recursive CTE, dan dua pengaman terhadap data yang melingkar.",
     "Titik awal, <code>UNION ALL</code> (bukan <code>UNION</code>), dan langkah berulang yang "
     "menyebut nama CTE-nya sendiri. Pengamannya: batas kedalaman "
     "(<code>WHERE tingkat &lt; 10</code>), dan klausa <code>CYCLE</code> yang sekaligus "
     "menunjukkan baris mana penyebabnya.")

soal(8, "Kamu butuh dua baris teratas per kelompok. Sebutkan tiga cara, dan kapan masing-masing "
        "lebih baik.",
     "<code>row_number()</code> disaring di luar — berjalan di semua mesin, pilihan bawaan. "
     "<code>CROSS JOIN LATERAL … LIMIT 2</code> — lebih baik kalau kelompoknya sedikit dan tiap "
     "kelompok datanya banyak. <code>DISTINCT ON</code> — kalau cuma butuh <em>satu</em> baris "
     "per kelompok, dan kamu tidak perlu memindahkan query-nya ke mesin lain.")

langkah("Cara membaca hasilmu",
    blok("aksi", "Hitung berapa yang bisa kamu jawab tanpa membuka kunci.", "LAKUKAN"),
    tabel(["Skormu", "Artinya", "Langkah berikutnya"],
          [["8 dari 8", "Siap ke Level 3", "Lanjut, dan kerjakan soal terapan di bawah"],
           ["6–7", "Cukup", "Ulangi hari yang jawabannya meleset, lalu lanjut"],
           ["≤ 5", "Belum", "Ulangi Hari 2 dan 3 dari awal — di situ hampir semua orang jatuh"]]),
    blok("catatan", "<strong>Kalau banyak yang belum tercentang, itu bukan tanda kamu tidak "
                    "bisa.</strong> Soal 3, 5, dan 8 adalah yang paling sering muncul di "
                    "wawancara SQL untuk posisi menengah — bukan karena sulit, tapi karena "
                    "hampir tidak ada yang mempelajarinya sampai pernah tertipu sekali."))

langkah("Soal terapan",
    blok("aksi", "Buat satu query yang menampilkan, untuk <strong>tiap cabang tiap bulan</strong>: "
                 "nilai penjualan bulan itu, nilai bulan sebelumnya <em>di cabang yang sama</em>, "
                 "pertumbuhan persennya, dan nilai kumulatif sejak Januari. Bulan Januari harus "
                 "jelas terlihat tidak punya pembanding.", "KERJAKAN, ± 25 MENIT"),
    blok("bahaya", "Jangan buka dua langkah berikutnya sebelum kamu punya jawaban yang jalan. "
                   "Kalau macet, lihat lagi klausa <code>WINDOW</code> di Hari 3."))

langkah("Ramalkan dulu berapa baris jawabannya",
    blok("aksi", "Sebelum menulis query-nya, jawab: berapa baris yang seharusnya keluar?",
         "LAKUKAN"),
    kode("""SELECT count(*) AS baris FROM (
  SELECT cabang, to_char(tanggal,'YYYY-MM') FROM pesanan
  WHERE status='selesai' GROUP BY 1,2) x;"""),
    keluaran(H, "h7_jumlah_baris"),
    "<p>Delapan belas: 3 cabang × 6 bulan. <strong>Kalau jawabanmu nanti bukan 18 baris, kamu "
    "sudah tahu ada yang salah sebelum melihat satu angka rupiah pun</strong> — persis "
    "pemeriksaan yang kamu lakukan sebelum menyerahkan kertas kerja.</p>")

langkah("Pastikan kamu tahu apa yang dikerjakan to_char",
    blok("aksi", "Satu baris, tanpa tabel.", "LAKUKAN"),
    kode("SELECT to_char(DATE '2024-03-05', 'YYYY-MM') AS bulan;"),
    keluaran(H, "h7_to_char"),
    "<p><code>2024-03</code>. Formatnya kamu tulis sendiri, jadi kamu juga bisa meminta "
    "<code>'YYYY'</code> saja, atau <code>'Mon YYYY'</code>. Karena hasilnya teks, "
    "<strong>mengurutkannya sama dengan mengurutkan tanggal</strong> — dan itu hanya benar kalau "
    "kamu memakai format tahun-di-depan seperti ini.</p>")

langkah("Angka pengikat yang harus kamu jaga",
    blok("aksi", "Satu baris. Catat angkanya.", "LAKUKAN"),
    kode("SELECT count(*) AS pesanan_selesai FROM pesanan WHERE status = 'selesai';"),
    keluaran(H, "h7_selesai"),
    "<p>362 — angka yang sama yang kamu dapat di Level 1 waktu merekonsiliasi pembukuan dengan "
    "ekspor kasir. <strong>Setiap laporan yang kamu buat dari tabel ini harus bisa dikembalikan "
    "ke angka itu.</strong> Itu kolom “kontrol” di kertas kerjamu, ditulis dalam SQL.</p>")

langkah("Kesalahan yang paling sering terjadi di soal ini",
    blok("aksi", "Jalankan versi yang lupa <code>PARTITION BY</code>.", "LAKUKAN"),
    kode('''WITH bulanan AS (
  SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
         sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.cabang, 2)
SELECT cabang, bulan, nilai,
  lag(nilai) OVER (ORDER BY cabang, bulan) AS bulan_lalu,
  sum(nilai) OVER (ORDER BY cabang, bulan
       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
FROM bulanan ORDER BY cabang, bulan LIMIT 8;'''),
    keluaran(H, "h7_terapan_lupa_partition"),
    blok("bahaya", "Lihat baris <strong>Kemang 2024-01</strong>: <code>bulan_lalu</code>-nya "
                   "2.582.000 — itu <strong>Juni-nya Dago</strong>. Dan kumulatifnya 13.920.000, "
                   "yang menjumlahkan seluruh Dago ke dalam angka Kemang."),
    "<p>Tidak ada tulisan merah. Query-nya jalan, angkanya keluar, dan seluruh kolom pertumbuhan "
    "Januari tiap cabang <strong>salah</strong>.</p>")

langkah("Versi yang benar",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode('''WITH bulanan AS (
  SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
         sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.cabang, 2)
SELECT cabang, bulan, nilai,
  lag(nilai) OVER w AS bulan_lalu,
  round((nilai - lag(nilai) OVER w) * 100.0 / lag(nilai) OVER w, 1) AS tumbuh,
  sum(nilai) OVER (PARTITION BY cabang ORDER BY bulan
       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
FROM bulanan
WINDOW w AS (PARTITION BY cabang ORDER BY bulan)
ORDER BY cabang, bulan LIMIT 6;'''),
    keluaran(H, "h7_terapan_benar"),
    "<p>(Enam baris pertama dari 18 — tiga cabang × enam bulan, angka yang kamu ramalkan tadi.) "
    "Januari <code>NULL</code>, dan kamu biarkan apa adanya.</p>")

langkah("Tiga hal yang membuat query itu benar",
    blok("aksi", "Baca sekali, lalu cocokkan dengan query-mu sendiri.", "LAKUKAN"),
    tabel(["Bagian", "Kenapa penting"],
          [["<code>PARTITION BY cabang</code>",
            "Membuat <code>lag</code> berhenti di batas cabang, jadi Januari Kemang tidak "
            "mengambil Juni Dago"],
           ["Frame ditulis eksplisit",
            "Di sini <code>RANGE</code> juga benar karena tiap cabang cuma punya satu baris per "
            "bulan — menuliskannya membuat maksudmu tidak perlu ditebak"],
           ["<code>NULL</code> Januari dibiarkan",
            "Bukan “tumbuh 0%”. Tidak ada pembanding, dan itu fakta yang harus terlihat"]]),
    blok("catatan", "Klausa <code>WINDOW w AS (...)</code> menghemat dua salinan definisi "
                    "jendela. Kalau kamu menulisnya tiga kali dan salah mengetik salah satu, "
                    "angkanya berubah tanpa error."))

langkah("Bacalah angkanya, jangan cuma menyerahkannya",
    blok("aksi", "Lihat kolom <code>tumbuh</code> untuk Dago.", "LAKUKAN"),
    blok("hasil", "<p>Maret turun <strong>52,9%</strong>, lalu Juni naik <strong>64,7%</strong>. "
                  "Guncangan sebesar itu di data sekecil ini biasanya <strong>bukan "
                  "tren</strong>.</p>", "YANG DILIHAT MATA"),
    "<p>Yang lebih mungkin: satu bulan punya lebih sedikit hari transaksi. Angka pertumbuhan "
    "bulanan selalu perlu kamu lihat bersama <em>jumlah harinya</em> sebelum kamu ceritakan ke "
    "klien — dan kamu sudah bisa menghitung jumlah hari itu sejak Hari 6. Menyebut “turun 53%” "
    "tanpa menyebut jumlah harinya adalah jenis kesimpulan yang dulu akan ditandai reviewer-mu.</p>")

langkah("Pemeriksaan terakhir",
    blok("aksi", "Jumlahkan kumulatif terakhir tiap cabang, bandingkan dengan total cabangnya.",
         "LAKUKAN"),
    kode('''WITH bulanan AS (
  SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
         sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.cabang, 2)
SELECT cabang, sum(nilai) AS total_cabang FROM bulanan GROUP BY cabang ORDER BY cabang;'''),
    keluaran(H, "h7_periksa"),
    "<p>Kumulatif Dago di baris terakhir tabel sebelumnya = <strong>12.665.000</strong>, sama "
    "persis dengan total Dago di sini — dan sama dengan angka yang kamu hitung di Hari 1. "
    "<strong>Kalau angkanya beda, ada yang salah dengan partisi atau frame-mu.</strong></p>")

HARI7 = {
  "n": "HARI 7", "tab": "7",
  "judul": "Ulangan dari ingatan, dan satu soal terapan",
  "waktu": "± 60 menit",
  "tujuan": "menjawab delapan pertanyaan Level 2 dengan suara, lalu membuktikannya dengan satu "
            "query yang menggabungkan hampir semua yang kamu pelajari minggu ini.",
  "langkah": L,
  "tutup_judul": "SQL Mahir Level 2 selesai",
  "tutup": "<p>Modul M6 memberimu window function sebagai <strong>daftar nama fungsi</strong>. "
           "Tujuh hari ini memberimu <strong>frame</strong> — bagian yang menentukan jawabannya, "
           "dan yang tidak pernah disebut di mana pun sebelumnya.</p>"
           "<p style=\"margin-top:8px\">Dua hal yang paling sering menyelamatkan: menuliskan "
           "frame secara eksplisit walaupun bawaannya sudah benar, dan memastikan "
           "<code>ORDER BY</code> di dalam <code>OVER</code> memecah seri sampai tuntas. "
           "Keduanya mencegah query yang hasilnya berubah-ubah tanpa datanya berubah.</p>"
           "<p style=\"margin-top:8px\"><strong>Yang khas PostgreSQL dan layak kamu sebut di "
           "wawancara:</strong> klausa <code>WINDOW</code> bernama, frame <code>GROUPS</code>, "
           "<code>RANGE</code> dengan <code>INTERVAL</code>, "
           "<code>percentile_cont … WITHIN GROUP</code>, klausa <code>CYCLE</code>, dan "
           "<code>CROSS JOIN LATERAL</code>. Enam hal yang hampir tidak ada di materi latihan "
           "berbasis SQLite.</p>"
           "<p style=\"margin-top:8px\"><strong>Berikutnya di Level 3:</strong> pola yang "
           "benar-benar ditanyakan di wawancara dan dipakai di pekerjaan — deduplikasi, "
           "<em>gaps and islands</em>, sesi pengguna, top-N per kelompok, pivot, dan funnel. "
           "Semuanya dibangun dari yang sudah kamu punya di Level 1 dan 2.</p>",
}
