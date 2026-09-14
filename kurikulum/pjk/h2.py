# -*- coding: utf-8 -*-
"""Hari 2 — kalkulasi bertingkat: precedence yang diam-diam salah."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Pertanyaannya sederhana: berapa pajak Bayu?",
    blok("aksi", "Bayu berpenghasilan Rp 180 juta/tahun. Tarif lapisan 2 (Rp 60jt-250jt) "
                 "adalah 15%. Jawab di kepalamu sebelum menjalankan apa pun.", "JAWAB DULU"),
    "<p>Hampir semua orang menjawab <strong>15% × 180 juta = 27 juta</strong>. Itu jawaban "
    "yang wajar — dan itu salah, dengan cara yang tidak akan pernah memberimu tulisan "
    "merah.</p>")

langkah("Jalankan cara yang \"wajar\" itu",
    blok("aksi", "Berkas <code>senja/pjk-hari-2.sql</code>. Jalankan.", "LAKUKAN"),
    kode("SELECT w.nama, w.penghasilan_tahunan, l.tarif,\n"
         "       round(w.penghasilan_tahunan * l.tarif) AS pajak_naif\n"
         "FROM pjk_wp w\n"
         "JOIN pjk_lapisan l\n"
         "  ON w.penghasilan_tahunan >= l.batas_bawah\n"
         " AND (l.batas_atas IS NULL OR w.penghasilan_tahunan < l.batas_atas)\n"
         "WHERE w.jenis = 'perorangan'\n"
         "ORDER BY w.id;"),
    keluaran(H, "h2_naif"),
    "<p>Bayu: 27 juta, persis tebakanmu. Query-nya jalan, tidak ada tulisan merah, hasilnya "
    "kelihatan masuk akal.</p>")

langkah("Kenapa itu tetap salah: pajak berjenjang, bukan satu tarif",
    blok("aksi", "Baca sekali, pelan-pelan.", "LAKUKAN"),
    blok("hasil", "<p>Pajak progresif berarti <strong>tiap rupiah dikenai tarif lapisan "
                  "tempatnya berada</strong> — bukan seluruh penghasilan dikenai tarif "
                  "lapisan tertinggi yang dicapai.</p>", "ATURANNYA"),
    "<p>60 juta pertama Bayu kena 5%, bukan 15%. Hanya rupiah <em>di atas</em> 60 juta yang "
    "kena 15%. Menyamaratakan satu tarif untuk semuanya persis kesalahan yang disebut "
    "lowongan sebagai <em>\"precedence and exceptions\"</em> — lapisan mana yang berlaku "
    "untuk bagian mana.</p>")

langkah("Bongkar per lapisan, untuk kasus yang paling parah",
    blok("aksi", "Sari berpenghasilan Rp 620 juta — melewati empat lapisan. Jalankan.",
         "LAKUKAN"),
    kode("WITH potong AS (\n"
         "  SELECT w.nama, l.urutan, l.batas_bawah, l.batas_atas, l.tarif,\n"
         "         GREATEST(0, LEAST(w.penghasilan_tahunan,\n"
         "                  COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian\n"
         "  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah\n"
         "  WHERE w.nama = 'Sari')\n"
         "SELECT urutan, batas_bawah, batas_atas, tarif, bagian, round(bagian * tarif) AS pajak_lapisan\n"
         "FROM potong ORDER BY urutan;"),
    keluaran(H, "h2_rincian_sari"),
    "<p>Empat baris, empat lapisan, masing-masing dikenai tarifnya sendiri atas "
    "<strong>bagiannya sendiri</strong>. <code>GREATEST</code> dan <code>LEAST</code> "
    "memotong tiap lapisan supaya tidak lebih dari batasnya dan tidak kurang dari nol.</p>")

langkah("Jumlahkan tiap lapisan, untuk semua orang sekaligus",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("WITH potong AS (\n"
         "  SELECT w.id, w.nama, l.tarif,\n"
         "         GREATEST(0, LEAST(w.penghasilan_tahunan,\n"
         "                  COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian\n"
         "  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah\n"
         "  WHERE w.jenis = 'perorangan')\n"
         "SELECT id, nama, round(sum(bagian * tarif)) AS pajak_benar\n"
         "FROM potong GROUP BY id, nama ORDER BY id;"),
    keluaran(H, "h2_benar"),
    "<p>Bayu: <strong>21 juta</strong>, bukan 27 juta. Query pertamamu tadi menagih terlalu "
    "banyak — dan tidak ada satu pun tanda bahwa itu salah selain kamu menghitungnya "
    "ulang.</p>")

langkah("Ukur selisihnya untuk semua orang, dalam satu tabel",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("WITH progresif AS (\n"
         "  SELECT w.id, w.nama,\n"
         "    round(sum(GREATEST(0, LEAST(w.penghasilan_tahunan,\n"
         "      COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) * l.tarif)) AS pajak_benar\n"
         "  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah\n"
         "  WHERE w.jenis = \'perorangan\' GROUP BY w.id, w.nama),\n"
         "naif AS (\n"
         "  SELECT w.id, round(w.penghasilan_tahunan * l.tarif) AS pajak_naif\n"
         "  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan >= l.batas_bawah\n"
         "   AND (l.batas_atas IS NULL OR w.penghasilan_tahunan < l.batas_atas)\n"
         "  WHERE w.jenis = \'perorangan\')\n"
         "SELECT p.nama, n.pajak_naif, p.pajak_benar, n.pajak_naif - p.pajak_benar AS kelebihan_tagih,\n"
         "  round(100.0*(n.pajak_naif-p.pajak_benar)/p.pajak_benar,1) AS persen_lebih\n"
         "FROM progresif p JOIN naif n ON n.id = p.id ORDER BY p.id;"),
    keluaran(H, "h2_selisih"),
    blok("bahaya", "<strong>Sari ditagih 43,1% lebih tinggi</strong> dari yang seharusnya — "
                   "Rp 56 juta kelebihan, dari satu asumsi keliru yang tidak pernah "
                   "menampilkan tulisan merah. Maya, dengan penghasilan Rp 7,2 miliar, "
                   "kelebihan Rp 306 juta."),
    "<p>Ini bukan bug yang eksotis. Ini bug yang <strong>lolos code review</strong> kalau "
    "reviewer-nya cuma memeriksa \"apakah query-nya jalan\", bukan \"apakah angkanya "
    "benar\".</p>")

langkah("Satu lapisan yang diam-diam menghilang",
    blok("aksi", "Coba hitung pajak Maya dengan query naif tadi, tapi kali ini perhatikan "
                 "baik-baik.", "LAKUKAN"),
    kode("SELECT w.nama, w.penghasilan_tahunan, l.tarif\n"
         "FROM pjk_wp w\n"
         "JOIN pjk_lapisan l\n"
         "  ON w.penghasilan_tahunan >= l.batas_bawah\n"
         " AND w.penghasilan_tahunan < l.batas_atas\n"
         "WHERE w.nama = 'Maya';"),
    keluaran(H, "h2_diam_lapisan_teratas"),
    blok("bahaya", "<strong>Kosong.</strong> Bukan error — kosong. Lapisan tertinggi "
                   "<code>batas_atas</code>-nya <code>NULL</code> (\"tidak terbatas\"), dan "
                   "<code>penghasilan &lt; NULL</code> selalu <em>tidak diketahui</em>, "
                   "persis pelajaran SQL Mahir L1 Hari 2. Maya, orang terkaya di tabel ini, "
                   "menghilang total dari laporan."),
    "<p>Inilah kenapa query yang benar di langkah 5 memakai "
    "<code>COALESCE(l.batas_atas, penghasilan)</code> — mengubah \"tidak diketahui\" jadi "
    "\"sebesar penghasilannya sendiri\", supaya lapisan terbuka tidak pernah membuang "
    "siapa pun.</p>")

langkah("Kalimat yang kamu ucapkan di wawancara",
    blok("aksi", "Baca sekali, ucapkan dengan suara.", "LAKUKAN"),
    blok("hasil", "<p>\"Kesalahan precedence yang paling berbahaya bukan yang menghasilkan "
                  "error — justru yang menghasilkan angka yang terlihat masuk akal tapi "
                  "salah. Saya membuktikan sendiri kasus di mana pendekatan naif menagih "
                  "43% lebih tinggi tanpa satu pun tanda kesalahan.\"</p>",
         "KALIMAT WAWANCARA"),
    "<p>Ini menjawab langsung syarat <em>\"strong logical reasoning across calculations, "
    "classifications, precedence and exceptions\"</em> — dengan bukti, bukan janji.</p>")

HARI2 = {
  "n": "HARI 2", "tab": "2",
  "judul": "Kalkulasi bertingkat: precedence yang diam-diam salah",
  "waktu": "± 55 menit",
  "tujuan": "membuktikan sendiri kenapa pajak progresif tidak bisa dihitung dengan satu tarif, "
            "dan mengenali kapan NULL diam-diam membuang baris teratas.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu tarif untuk seluruh penghasilan menagih "
           "sampai 43% lebih tinggi, tanpa error · <code>GREATEST</code>/<code>LEAST</code> "
           "memotong tiap lapisan ke bagiannya sendiri · <code>COALESCE</code> pada lapisan "
           "terbuka (<code>batas_atas IS NULL</code>) mencegah orang terkaya menghilang dari "
           "laporan.</p>"
           "<p style=\"margin-top:8px\">Besok: aturan khusus yang harus <strong>menang</strong> "
           "atas aturan umum — dan kenapa mempercayai klasifikasi apa adanya bisa membuat "
           "kamu salah 9 kali lipat.</p>",
}
