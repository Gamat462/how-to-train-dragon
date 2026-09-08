# -*- coding: utf-8 -*-
"""Hari 4 — harga sebuah index, dalam megabita dan detik."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bikin salinan yang boleh kamu rusak",
    blok("aksi", "Hari ini semua bekerja di <code>coba.db</code>, jadi <code>besar.db</code>-mu "
                 "tidak tersentuh. Sesi Python baru boleh.", "LAKUKAN"),
    kode("""import sqlite3, time, os, shutil
shutil.copy("besar.db", "coba.db")
c = sqlite3.connect("coba.db")
c.execute("DROP INDEX IF EXISTS idx_ct")
c.execute("VACUUM")
print(f"tanpa index apa pun : {os.path.getsize('coba.db')/1e6:.1f} MB")"""),
    blok("hasil", "<pre><code>tanpa index apa pun : 36.7 MB</code></pre>", "HARUS MUNCUL"),
    "<p><code>VACUUM</code> merapikan berkasnya supaya ukurannya jujur — tanpa itu, ruang bekas "
    "index yang dihapus masih terhitung.</p>",
    blok("bahaya", "<code>VACUUM</code> menulis ulang seluruh berkas. Lambat 1–5 detik itu wajar, "
                   "dan tidak ada yang tercetak selama itu."))

langkah("Ukur berapa lama menulis 50.000 baris",
    blok("aksi", "Bikin fungsi <code>tulis</code>, lalu panggil sekali.", "LAKUKAN"),
    kode("""def tulis(con, n=50000):
    baris = [(1000000+i, "2024-06-01", "Kemang", 7, "Kopi Susu", 1, 22000)
             for i in range(n)]
    t = time.perf_counter()
    con.executemany("INSERT INTO transaksi VALUES (?,?,?,?,?,?,?)", baris)
    con.commit()
    return time.perf_counter() - t

t_tanpa = tulis(c)
print(f"tanpa index : {t_tanpa:.2f} detik")"""),
    blok("hasil", "<pre><code>tanpa index : 0.06 detik</code></pre>", "HARUS MUNCUL"),
    "<p>Ini angka pembandingnya. Simpan <code>t_tanpa</code> — dipakai lagi di langkah 6.</p>")

langkah("Kembalikan seperti semula",
    blok("aksi", "Hapus 50.000 baris tadi, supaya perbandingan nanti adil.", "LAKUKAN"),
    kode("""c.execute("DELETE FROM transaksi WHERE id >= 1000000"); c.commit()
print("sisa baris:", c.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0])"""),
    blok("hasil", "<pre><code>sisa baris: 800000</code></pre>", "HARUS MUNCUL"),
    "<p>Kalau angkamu bukan 800000, jangan lanjut — ulangi dari langkah 1.</p>")

langkah("Bikin tiga index sekaligus, dan catat waktunya",
    blok("aksi", "Jalankan. Tiga index yang wajar untuk tabel ini.", "LAKUKAN"),
    kode("""for nama, kolom in [("idx_ct","cabang, tanggal"), ("idx_pel","pelanggan_id"),
                    ("idx_prd","produk")]:
    t = time.perf_counter()
    c.execute(f"CREATE INDEX {nama} ON transaksi({kolom})"); c.commit()
    print(f"waktu buat {nama:8s}: {time.perf_counter()-t:.2f} detik")"""),
    blok("hasil", "<pre><code>waktu buat idx_ct  : 0.70 detik\n"
                  "waktu buat idx_pel : 0.35 detik\n"
                  "waktu buat idx_prd : 0.36 detik</code></pre>", "HARUS MUNCUL"),
    "<p>Sekali seumur hidup tabel itu, satu setengah detik total. Murah — sejauh ini.</p>")

langkah("Sekarang lihat harganya di berkas",
    blok("aksi", "Rapikan lagi, lalu ukur ukurannya.", "LAKUKAN"),
    kode("""c.execute("VACUUM")
print(f"dengan 3 index      : {os.path.getsize('coba.db')/1e6:.1f} MB")"""),
    blok("hasil", "<pre><code>dengan 3 index      : 81.7 MB</code></pre>", "HARUS MUNCUL"),
    "<p><strong>36,7 MB → 81,7 MB.</strong> Index-nya sendiri makan <strong>45 MB</strong> — "
    "lebih besar daripada datanya.</p>",
    blok("catatan", "Angka waktu di mesinmu akan beda. <strong>36.7 dan 81.7 tidak boleh beda</strong> "
                    "— itu ukuran berkas, bukan kecepatan."))

langkah("Dan harganya di setiap penulisan",
    blok("aksi", "Tulis 50.000 baris yang sama persis, sekarang dengan tiga index terpasang.", "LAKUKAN"),
    kode("""t_dgn = tulis(c)
print(f"dgn 3 index : {t_dgn:.2f} detik")
print(f"perlambatan : {t_dgn/t_tanpa:.1f}x")"""),
    blok("hasil", "<pre><code>dgn 3 index : 0.17 detik\nperlambatan : 3.0x</code></pre>",
         "HARUS MUNCUL"),
    "<p><strong>Tiga kali lebih lama</strong>, karena tiap baris baru harus disisipkan ke tiga "
    "daftar terurut — bukan cuma ditempel di ujung tabel.</p>")

langkah("Jawab pertanyaan yang tadi tidak bisa kamu jawab",
    blok("aksi", "Baca tabel ini pelan-pelan. Tiap barisnya sekarang punya angka di belakangnya.", "LAKUKAN"),
    tabel(["Bikin index kalau…", "Jangan, kalau…"],
          [["kolomnya sering muncul di <code>WHERE</code>, <code>JOIN … ON</code>, atau "
            "<code>ORDER BY</code>", "kolomnya jarang dipakai menyaring"],
           ["tabelnya besar (puluhan ribu baris ke atas)",
            "tabelnya kecil — di bawah beberapa ribu baris, <code>SCAN</code> sudah cukup cepat"],
           ["nilainya banyak variasinya (<code>pelanggan_id</code>: 50.000 nilai berbeda)",
            "nilainya sedikit variasinya (<code>status</code>: cuma “selesai” dan “batal”) — "
            "melompat ke setengah tabel bukan lompatan"],
           ["datanya lebih sering dibaca daripada ditulis — laporan, dasbor, analisis",
            "datanya masuk terus-menerus dan jarang dibaca — pencatatan mentah"],
           ["kamu sudah <em>melihat</em> <code>SCAN</code> di rencananya",
            "kamu belum mengukur apa pun dan cuma merasa “biar cepat”"]]),
    blok("bahaya", "<strong>Baris terakhir yang paling sering dilanggar</strong>, termasuk oleh "
                   "orang berpengalaman. Membuat index tanpa mengukur dulu adalah menebak — "
                   "dengan biaya 45 MB dan 3× perlambatan tulis."))

langkah("Hafalkan urutannya, bukan aturannya",
    blok("aksi", "Tulis lima langkah ini di tempat yang kamu lihat tiap hari.", "LAKUKAN"),
    kode("""1. query terasa lambat
2. ukur(sql)          -> berapa lama sebenarnya
3. rencana(sql)       -> SCAN-nya di mana
4. CREATE INDEX ...   -> baru sekarang
5. ukur(sql) lagi     -> buktikan bedanya""", salin=False),
    "<p>Langkah 5 yang paling sering dilewati. Kalau kamu melewatinya, kamu tidak tahu index-mu "
    "berguna atau cuma menambah 15 MB.</p>")

langkah("Satu aturan untuk pekerjaan klienmu nanti",
    blok("aksi", "Baca sekali. Ini menempel langsung ke alur <em>Bekal Data Klien</em>.", "LAKUKAN"),
    blok("hasil", "<p>Kalau data klien datang sebagai Excel lalu kamu muat ke SQLite: "
                  "<strong>muat semua barisnya dulu, baru <code>CREATE INDEX</code> di akhir.</strong></p>",
         "URUTAN YANG BENAR"),
    "<p>Alasannya persis dua angka yang barusan kamu ukur: membangun index sekali jadi memakan "
    "<strong>0,35 detik</strong>; membiarkannya terpasang selama pemuatan memperlambat tiap "
    "penulisan <strong>3 kali</strong>.</p>")

langkah("Bereskan, lalu ulangi dari ingatan",
    blok("aksi", "Hapus salinannya, lalu tutup halaman ini dan jawab di kertas.", "LAKUKAN"),
    kode("""c.close(); os.remove("coba.db")

# 1. Dua harga yang dibayar tiap index?
# 2. Kenapa kolom "status" (2 nilai) buruk untuk di-index?
# 3. Kalau memuat 800.000 baris ke tabel baru, index dibuat kapan?"""),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <strong>Ruang</strong> (36,7 → 81,7 MB) dan <strong>kecepatan menulis</strong> (3×). "
    "2. Melompat ke setengah tabel bukan lompatan — SQLite tetap membaca ratusan ribu baris. "
    "3. <strong>Sesudah</strong> semua baris masuk, bukan sebelum.</p></details>")

HARI4 = {
  "n": "HARI 4",
  "tab": "4",
  "judul": "Harga sebuah index, dalam megabita dan detik",
  "waktu": "± 50 menit",
  "tujuan": "menjawab “kenapa tidak semua kolom di-index saja?” dengan <strong>angka yang kamu "
            "ukur sendiri</strong>, bukan dengan perasaan.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> dua angka yang membuat semua nasihat index jadi "
           "masuk akal — <strong>+45 MB</strong> dan <strong>3× lebih lambat menulis</strong> — "
           "dan urutan lima langkah yang membuatmu tidak pernah menebak.</p>"
           "<p style=\"margin-top:8px\">Kalau index selalu menguntungkan, basis data pasti sudah "
           "membuatnya sendiri diam-diam. Ia tidak melakukan itu, dan sekarang kamu tahu sebabnya.</p>"
           "<p style=\"margin-top:8px\">Besok: kelambatan yang <strong>tidak bisa disembuhkan "
           "index apa pun</strong>. Siapkan waktu — satu langkahnya sengaja dibuat menunggu.</p>",
}
