# -*- coding: utf-8 -*-
"""Hari 3 — index gabungan dan aturan kolom terkiri."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bersihkan dulu, supaya yang diukur cuma satu hal",
    blok("aksi", "Hapus ketiga index kemarin. Masih di sesi Python yang sama.", "LAKUKAN"),
    kode("""for n in ["idx_pel", "idx_tgl", "idx_cab"]:
    con.execute(f"DROP INDEX IF EXISTS {n}")
con.commit()
print(con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'").fetchone()[0])"""),
    blok("hasil", "<pre><code>0</code></pre>", "HARUS MUNCUL"),
    "<p>Nol index. Kalau punyamu bukan nol, ada yang belum terhapus — dan seluruh pengukuranmu "
    "hari ini akan salah baca. Jangan lanjut sebelum kamu melihat angka nol itu.</p>")

langkah("Bikin satu index atas dua kolom",
    blok("aksi", "Perhatikan urutannya: <code>cabang</code> dulu, <code>tanggal</code> kedua.", "LAKUKAN"),
    kode("""con.execute("CREATE INDEX idx_ct ON transaksi(cabang, tanggal)")
con.commit()"""),
    blok("hasil", "<p>Tidak ada yang tercetak. Itu memang benar.</p>", "HARUS MUNCUL"),
    "<p>Tiga langkah berikutnya menanyakan tiga hal berbeda ke <strong>satu index yang sama ini</strong>. "
    "Nasibnya akan berbeda-beda.</p>")

langkah("Dua error yang akan sering kamu temui saat mengurus index",
    blok("aksi", "Jalankan dua baris ini satu per satu. Dua-duanya akan merah, "
                 "dan dua-duanya berguna.", "LAKUKAN"),
    kode('con.execute("CREATE INDEX idx_ct ON transaksi(cabang, tanggal)")'),
    blok("bahaya", "<pre><code>OperationalError: index idx_ct already exists</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    kode('con.execute("DROP INDEX idx_yang_tidak_ada")'),
    blok("bahaya", "<pre><code>OperationalError: no such index: idx_yang_tidak_ada</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Itu sebabnya langkah 1 menulis <code>DROP INDEX <strong>IF EXISTS</strong></code>. "
    "Tanpa itu, skrip yang kamu jadwalkan berhenti di tengah jalan hanya karena membersihkan "
    "sesuatu yang memang sudah bersih.</p>",
    blok("catatan", "<strong>Kalau punyamu tidak merah</strong> di baris pertama, berarti "
                    "<code>idx_ct</code> belum sempat dibuat — ulangi langkah 2 dulu, lalu "
                    "kembali ke sini."))

langkah("Tanya pakai kolom pertama saja",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("""s = "SELECT COUNT(*) FROM transaksi WHERE cabang = 'Kemang'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>5.7 ms   hasil = 160457\n"
                  "    SEARCH transaksi USING COVERING INDEX idx_ct (cabang=?)</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>SEARCH</code>. Satu index yang kamu buat tadi melayani pertanyaan yang cuma "
    "menyebut <code>cabang</code> — kolom pertamanya.</p>")

langkah("Tanya pakai kedua kolomnya",
    blok("aksi", "Tambah satu syarat.", "LAKUKAN"),
    kode("""s = "SELECT COUNT(*) FROM transaksi WHERE cabang = 'Kemang' AND tanggal >= '2024-01-01'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>2.8 ms   hasil = 80224\n"
                  "    SEARCH transaksi USING COVERING INDEX idx_ct (cabang=? AND tanggal&gt;?)</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>SEARCH</code> dengan <strong>dua syarat sekaligus</strong>, dan justru "
    "<em>lebih cepat</em> daripada langkah sebelumnya — karena barisnya lebih sedikit.</p>")

langkah("Sekarang kolom kedua saja, tanpa yang pertama",
    blok("aksi", "Ini yang penting. Jalankan dan lihat kata pertamanya.", "LAKUKAN"),
    kode("""s = "SELECT COUNT(*) FROM transaksi WHERE tanggal >= '2024-01-01'"
ms, h = ukur(s); print(f"{ms:.1f} ms   hasil = {h[0][0]}")
rencana(s)"""),
    blok("hasil", "<pre><code>35.6 ms   hasil = 400090\n"
                  "    SCAN transaksi USING COVERING INDEX idx_ct</code></pre>", "HARUS MUNCUL"),
    "<p><strong>SCAN.</strong> Index-mu ada, kolomnya ada di dalamnya, dan tetap tidak menolong "
    "sama sekali. Inilah yang tidak akan pernah kamu duga tanpa membaca rencananya.</p>")

langkah("Aturannya, dan gambarannya",
    blok("aksi", "Baca sekali. Ini satu-satunya hal yang harus kamu hafal hari ini.", "LAKUKAN"),
    blok("hasil", "<p><strong>Aturan kolom terkiri.</strong> Index atas <code>(A, B, C)</code> "
                  "bisa dipakai untuk <code>A</code>, untuk <code>A+B</code>, dan untuk "
                  "<code>A+B+C</code> — <strong>tapi tidak untuk <code>B</code> saja, tidak untuk "
                  "<code>C</code> saja, dan tidak untuk <code>B+C</code>.</strong> Kolom paling "
                  "kiri harus selalu ikut disebut di <code>WHERE</code>.</p>", "ATURANNYA"),
    "<p><strong>Buku telepon.</strong> Ia diurutkan menurut <em>nama belakang, lalu nama depan</em> "
    "— persis sebuah index gabungan. Mencari “Wijaya” gampang. “Wijaya, Andi” lebih gampang lagi. "
    "Tapi mencari <em>semua orang bernama depan Andi</em> berarti membaca seluruh buku, karena "
    "Andi tersebar di semua halaman. Itulah <code>SCAN</code> di langkah 5.</p>")

langkah("Latihan: rancang index untuk tiga query nyata",
    blok("aksi", "Ini yang benar-benar ditanyakan di wawancara. "
                 "<strong>Jawab dulu di kepala</strong>, baru buka kuncinya.", "LAKUKAN"),
    kode("""-- Q1  laporan harian satu cabang
SELECT * FROM transaksi WHERE cabang = ? AND tanggal = ?

-- Q2  omzet seluruh cabang untuk satu bulan
SELECT cabang, SUM(nilai) FROM transaksi
WHERE tanggal >= ? AND tanggal < ? GROUP BY cabang

-- Q3  riwayat satu pelanggan, terbaru dulu
SELECT * FROM transaksi WHERE pelanggan_id = ? ORDER BY tanggal DESC""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p><strong>Q1 → <code>(cabang, tanggal)</code>.</strong> Dua-duanya disebut dengan "
    "<code>=</code>, jadi urutannya sebenarnya bebas — kalau ragu, taruh yang "
    "<strong>lebih banyak variasinya</strong> di depan. <code>idx_ct</code> yang sudah kamu punya "
    "sudah pas.</p>"
    "<p><strong>Q2 → <code>(tanggal, cabang)</code>, kebalikan Q1.</strong> Di sini "
    "<code>tanggal</code> yang menyaring, <code>cabang</code> cuma pengelompok. "
    "Langkah 8 mengukurnya.</p>"
    "<p><strong>Q3 → <code>(pelanggan_id, tanggal)</code>.</strong> <code>tanggal</code> masuk "
    "bukan karena ada di <code>WHERE</code>, tapi karena ada di <code>ORDER BY</code>. "
    "Langkah 10 dan 11 membuktikannya.</p></details>",
    blok("catatan", "<strong>Q1 dan Q2 menyebut kolom yang sama persis dan butuh dua index "
                    "yang berbeda.</strong> Itu bagian yang paling sering salah dijawab."))

langkah("Ukur Q2 dengan index yang salah urutan",
    blok("aksi", "Pakai <code>idx_ct</code> yang sudah ada. <code>tanggal</code> ada di posisi "
                 "kedua, dan <code>cabang</code> tidak ada di <code>WHERE</code>.", "LAKUKAN"),
    kode("""Q2 = \"\"\"SELECT cabang, SUM(nilai) FROM transaksi
WHERE tanggal >= '2024-01-01' AND tanggal < '2024-02-01' GROUP BY cabang\"\"\"
ms, h = ukur(Q2); print(f"{ms:.1f} ms   {len(h)} baris")
rencana(Q2)"""),
    blok("hasil", "<pre><code>104.6 ms   5 baris\n"
                  "    SCAN transaksi USING INDEX idx_ct</code></pre>", "HARUS MUNCUL"),
    "<p>Persis kasus <code>SCAN</code> di langkah 5, sekarang di query yang sungguhan.</p>")

langkah("Tambahkan index dengan urutan yang benar",
    blok("aksi", "Jangan hapus <code>idx_ct</code>. Tambahkan yang kedua, lalu ukur query "
                 "yang sama persis.", "LAKUKAN"),
    kode("""con.execute("CREATE INDEX idx_tc ON transaksi(tanggal, cabang)"); con.commit()
ms, h = ukur(Q2); print(f"{ms:.1f} ms   {len(h)} baris")
rencana(Q2)"""),
    blok("hasil", "<pre><code>48.1 ms   5 baris\n"
                  "    SEARCH transaksi USING INDEX idx_tc (tanggal&gt;? AND tanggal&lt;?)\n"
                  "    USE TEMP B-TREE FOR GROUP BY</code></pre>", "HARUS MUNCUL"),
    "<p>104,6 → 48,1 ms. <strong>Dua kali lipat</strong> — bukan enam ribu kali seperti Hari 1, "
    "karena query ini memang harus menyentuh 34 ribu baris apa pun caranya.</p>",
    blok("catatan", "<strong>Index tidak membuat pekerjaan besar jadi kecil.</strong> "
                    "Ia cuma menghapus pekerjaan yang sia-sia. Kalau pekerjaannya memang besar, "
                    "index tidak akan menyulapnya."))

langkah("Q3: lihat biaya pengurutan yang tersembunyi",
    blok("aksi", "Hapus <code>idx_tc</code>, bikin index satu kolom, lalu minta rencananya.", "LAKUKAN"),
    kode("""con.execute("DROP INDEX idx_tc")
Q3 = "SELECT * FROM transaksi WHERE pelanggan_id = 12345 ORDER BY tanggal DESC"
con.execute("CREATE INDEX idx_p1 ON transaksi(pelanggan_id)"); con.commit()
rencana(Q3)"""),
    blok("hasil", "<pre><code>    SEARCH transaksi USING INDEX idx_p1 (pelanggan_id=?)\n"
                  "    USE TEMP B-TREE FOR ORDER BY</code></pre>", "HARUS MUNCUL"),
    "<p>Barisnya ketemu lewat <code>SEARCH</code>, bagus. Tapi ada baris kedua: SQLite masih "
    "harus <strong>mengurutkan hasilnya sendiri</strong>.</p>")

langkah("Hapus biaya itu dengan menambah satu kolom ke index",
    blok("aksi", "Query-nya <strong>tidak diubah sama sekali</strong>. Cuma index-nya.", "LAKUKAN"),
    kode("""con.execute("DROP INDEX idx_p1")
con.execute("CREATE INDEX idx_p2 ON transaksi(pelanggan_id, tanggal)"); con.commit()
rencana(Q3)"""),
    blok("hasil", "<pre><code>    SEARCH transaksi USING INDEX idx_p2 (pelanggan_id=?)</code></pre>",
         "HARUS MUNCUL"),
    "<p>Baris <code>USE TEMP B-TREE FOR ORDER BY</code> <strong>hilang</strong>. Satu langkah "
    "kerja lenyap — bukan karena query-nya diubah, tapi karena datanya sudah tersimpan dalam "
    "urutan yang kebetulan dibutuhkan.</p>")

langkah("Bereskan, lalu ulangi dari ingatan",
    blok("aksi", "Hapus index terakhir supaya Hari 4 mulai dari keadaan yang sama denganku. "
                 "Lalu tutup halaman ini dan jawab di kertas.", "LAKUKAN"),
    kode("""con.execute("DROP INDEX idx_p2"); con.commit()

# 1. Index (A, B, C) bisa dipakai untuk WHERE apa saja?
# 2. Kenapa Q1 dan Q2 butuh index berbeda padahal kolomnya sama?
# 3. Kapan sebuah kolom masuk index bukan karena ada di WHERE?"""),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>A</code>, <code>A+B</code>, <code>A+B+C</code> — kolom terkiri harus selalu ikut. "
    "2. Yang menyaring di Q1 adalah <code>cabang</code>, di Q2 adalah <code>tanggal</code>; "
    "yang menyaring harus di depan. "
    "3. Kalau ia ada di <code>ORDER BY</code> — index menyimpannya sudah terurut.</p></details>")

HARI3 = {
  "n": "HARI 3",
  "tab": "3",
  "judul": "Index gabungan, dan aturan kolom terkiri",
  "waktu": "± 60 menit",
  "tujuan": "merancang index atas dua kolom atau lebih, dan tahu urutan kolomnya <strong>bukan "
            "selera</strong> — urutan yang salah membuat index-nya diam saja ketika paling "
            "dibutuhkan.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu aturan (kolom terkiri), satu gambaran "
           "(buku telepon), dan tiga pengukuran yang membuktikannya — termasuk satu kasus di mana "
           "index yang benar cuma memberi dua kali lipat, bukan ribuan.</p>"
           "<p style=\"margin-top:8px\">Tiga hari terakhir isinya alasan untuk <em>membuat</em> "
           "index. Besok alasan untuk <strong>tidak</strong> — dengan angka, bukan perasaan.</p>",
}
