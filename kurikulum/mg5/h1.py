# -*- coding: utf-8 -*-
"""Hari 29 — Tahap A: fit yang jalan mulus dan salah total.
Semua angka HARUS MUNCUL diperoleh dengan menjalankan kode sungguhan (Python 3.11,
scipy 1.17) terhadap migas.db — database yang sama sejak Migas L1."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Rumus yang menggerakkan seluruh minggu ini",
    blok("aksi", "Buka Google Colab (seperti minggu-minggu sebelumnya), unggah "
                 "<code>migas.db</code>, siapkan sel kosong.", "LAKUKAN"),
    kode("q(t) = qi / (1 + b·D·t)^(1/b)", salin=False),
    "<p>Sumur minyak makin lama makin sedikit produksinya, dan pola turunnya cukup "
    "teratur untuk dirumuskan. Rumus ini namanya <strong>persamaan Arps</strong>, "
    "dipakai industri sejak 1945. <code>qi</code> laju awal, <code>D</code> laju "
    "penurunan tahunan, <code>b</code> bentuk lengkungan (0 = eksponensial, 1 = "
    "harmonik).</p>",
    blok("catatan", "Kalau kamu tahu qi, D, b sebuah sumur, kamu bisa memproyeksikan "
                    "produksinya bertahun-tahun dan mendapat angka <strong>cadangan</strong> "
                    "— barel yang masih bisa diambil. Angka itu masuk ke laporan keuangan "
                    "dan penilaian aset saat akuisisi. Kamu pernah menandatangani opini "
                    "atas angka seperti ini tanpa pernah menelusuri sendiri caranya "
                    "dihitung — hari ini kamu yang menghitungnya."))

langkah("Muat datanya, dan tulis fungsi Arps-nya",
    blok("aksi", "Jalankan ini dulu — cuma memuat, belum menghitung apa pun.", "LAKUKAN"),
    kode("""import sqlite3, pandas as pd, numpy as np
from scipy.optimize import curve_fit

con = sqlite3.connect("migas.db")
prod = pd.read_sql("SELECT * FROM produksi_harian", con, parse_dates=["tanggal"])
sumur = pd.read_sql("SELECT * FROM sumur", con)"""),
    kode("""def arps(t, qi, D, b):
    return qi / np.power(1 + b*D*t, 1/b)""", salin=False),
    "<p>Fungsi ini persis rumus di atas, ditulis ulang jadi Python. <code>t</code> "
    "waktu dalam tahun; ketiga parameter lainnya nanti dicari oleh <code>curve_fit</code>, "
    "bukan kamu tebak sendiri.</p>",
    blok("aksi", "Uji dulu fungsinya sebelum dipakai — di t=0, hasilnya harus persis "
                 "qi, tidak kurang tidak lebih.", "LAKUKAN"),
    kode('arps(np.array([0.0]), 500.0, 0.3, 0.5)'),
    blok("hasil", "<p><code>array([500.])</code></p>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Itu normal kamu lakukan tiap kali menulis fungsi baru,</strong> "
                    "dan tidak berlebihan — satu baris, beberapa detik, dan kamu "
                    "langsung tahu fondasinya benar sebelum membangun 60 baris di "
                    "atasnya."))

langkah("Coba dulu pada SATU sumur, sebelum jadi satu batch",
    blok("aksi", "Jangan langsung loop ke 64 sumur. Pilih satu dulu, biar kamu lihat "
                 "sendiri apa yang terjadi di setiap baris.", "LAKUKAN"),
    kode("""W = "CDN-020"
g = prod[(prod.sumur_id == W) & (prod.berproduksi == 1)].sort_values("tanggal")
m = g.set_index("tanggal").oil_bopd.resample("MS").mean().dropna()
t, q = np.arange(len(m)) / 12.0, m.values

popt, _ = curve_fit(arps, t, q, p0=[q[0], 0.3, 0.5],
                    bounds=([q[0]*0.4, 0.01, 0.0], [q[0]*2.5, 2.0, 1.5]), maxfev=8000)
print("qi, D, b =", popt.round(3))"""),
    blok("hasil", "<p><code>qi, D, b = [52.389  0.17   0.426]</code></p>", "HARUS MUNCUL"),
    "<p><code>resample(\"MS\")</code> merata-ratakan data harian ke bulanan supaya derau "
    "harian tidak menyetir fit. <code>bounds</code> memagari pencarian: qi masuk akal "
    "secara fisik, D antara 1%–200%/tahun, b antara 0 dan 1,5.</p>")

langkah("Coba sumur berikutnya — dan lihat layar merahmu yang pertama",
    blok("aksi", "Ganti <code>W</code> jadi sumur berikutnya secara urutan ID, tanpa "
                 "berpikir dulu. Ini yang biasanya orang lakukan.", "LAKUKAN"),
    kode('W = "CDN-002"', salin=False),
    blok("hasil", "<div class=\"kode\"><pre><code>Traceback (most recent call last):\n"
                  "  File \"&lt;stdin&gt;\", line 1, in &lt;module&gt;\n"
                  "IndexError: index 0 is out of bounds for axis 0 with size 0</code></pre></div>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("catatan", "<strong>Itu wajar, dan bukan salahmu.</strong> Baris <code>q[0]</code> "
                    "di <code>p0</code> mengandaikan sumurnya punya produksi. CDN-002 "
                    "ternyata sumur <strong>injeksi</strong> (Injector) — dipakai memompa "
                    "air ke reservoir, bukan mengangkat minyak. Baris <code>berproduksi==1</code> "
                    "benar menyaringnya jadi kosong; masalahnya kode belum tahu harus "
                    "berhenti sebelum memanggil <code>q[0]</code> pada larik kosong."))

langkah("Perbaiki dengan satu baris, sebelum loop ke semuanya",
    "<p>Perbaikannya bukan “tangkap errornya lalu lupakan” — itu menyembunyikan masalah, "
    "bukan menyelesaikannya. Perbaikannya: jangan pernah ikutkan sumur non-Producer "
    "sejak awal.</p>",
    kode('prod2 = prod.merge(sumur[["sumur_id","tipe_sumur"]], on="sumur_id")\n'
         'prod2 = prod2[prod2.tipe_sumur == "Producer"]', salin=True),
    blok("bahaya", "<strong>Camkan urutan kejadiannya.</strong> Kode yang salah tadi juga "
                   "tidak error untuk 58 dari 59 sumur producer — ia hanya meledak pada "
                   "satu sumur spesifik. Kalau kamu memulai loop langsung dari semua 64 "
                   "sumur tanpa mencoba satu-satu dulu, error ini akan muncul di tengah "
                   "loop dan menghentikan semuanya. Mencoba satu sumur dulu bukan buang "
                   "waktu; itu yang membuatmu menemukan bug ini di baris ke-2, bukan di "
                   "baris ke-200."))

langkah("Sekarang jalankan ke seluruh sumur producer — bagian pertama",
    blok("aksi", "Bungkus langkah 3 jadi loop, dengan dua penjagaan tambahan: sumur "
                 "dengan riwayat kurang dari 400 hari dilewati (terlalu baru untuk "
                 "dipercaya), dan segmen bulanan kurang dari 18 bulan juga dilewati.",
         "LAKUKAN"),
    kode("""hasil = []
for w, g in prod2.groupby("sumur_id"):
    g = g[g.berproduksi == 1].sort_values("tanggal")
    if len(g) < 400: continue
    m = g.set_index("tanggal").oil_bopd.resample("MS").mean().dropna()
    if len(m) < 18: continue
    t, q = np.arange(len(m)) / 12.0, m.values
    try:
        popt, _ = curve_fit(arps, t, q, p0=[q[0], 0.3, 0.5],
                            bounds=([q[0]*0.4,0.01,0.0], [q[0]*2.5,2.0,1.5]), maxfev=8000)
    except Exception:
        continue"""),
    "<p>Sampai sini baru penyaringan dan pemasangan kurva. Kalau fit-nya gagal "
    "konvergen, sumurnya dilewati — bukan dipaksakan.</p>")

langkah("Bagian kedua: rekam hasilnya, lalu proyeksikan 30 tahun ke depan",
    kode("""    qi, D, b = popt
    pred = arps(t, *popt)
    r2 = 1 - ((q-pred)**2).sum() / ((q-q.mean())**2).sum()
    tf = np.arange(len(m), len(m)+360) / 12.0          # 360 bln = 30 thn pagu sementara
    qf = arps(tf, *popt); qf = qf[qf > 15]              # 15 bopd batas ekonomis sementara
    hasil.append((w, round(qi,1), round(D,3), round(b,3), round(r2,3),
                  round(g.oil_bopd.sum(),0), round(qf.sum()*30.44,0)))"""),
    "<p>Pagu 30 tahun dan batas 15 bopd itu dua angka sementara yang akan kamu "
    "pertanyakan sendiri di Hari 32 dan 33.</p>")

langkah("Kumpulkan hasilnya jadi satu tabel, dan lihat ringkasannya",
    kode("""dca = pd.DataFrame(hasil, columns=["sumur_id","qi_fit","D_fit","b_fit","r2",
                   "kumulatif_bbl","sisa_cadangan_bbl"])
dca["eur_bbl"] = dca.kumulatif_bbl + dca.sisa_cadangan_bbl
print(f"berhasil fit: {len(dca)} sumur | R2 rata-rata {dca.r2.mean():.3f} | R2 min {dca.r2.min():.3f}")
print(f"Sisa cadangan: {dca.sisa_cadangan_bbl.sum():,.0f} bbl | EUR: {dca.eur_bbl.sum():,.0f} bbl")"""),
    blok("hasil", "<p><strong>berhasil fit: 59 sumur · R² rata-rata 0,701 · R² minimum "
                  "−0,047</strong></p><p style=\"margin-top:8px\">Sisa cadangan "
                  "<strong>50.544.537 bbl</strong> · EUR total <strong>70.623.671 bbl</strong> "
                  "· Pengurasan <strong>28,4%</strong></p>", "HARUS MUNCUL"),
    "<p>Tidak ada error. Tidak ada peringatan. Angka 50,5 juta barel siap ditempel ke "
    "slide. <strong>Kalau angkamu persis sama sampai digit terakhir,</strong> itu memang "
    "seharusnya begitu — datanya deterministik, dari <code>migas.db</code> yang sama.</p>")

langkah("Lihat lima sumur cadangan terbesarnya",
    kode('print(dca.nlargest(5,"sisa_cadangan_bbl")[["sumur_id","qi_fit","D_fit","b_fit","r2","sisa_cadangan_bbl"]])'),
    blok("hasil", tabel(["sumur", "qi_fit", "D_fit", "b_fit", "r2", "sisa cadangan (bbl)"],
          [["CDN-060", "536,9", "0,010", "0,0", "0,002", "4.910.439"],
           ["CDN-063", "898,0", "0,062", "0,0", "0,144", "3.590.578"],
           ["CDN-028", "321,9", "0,010", "1,5", "<strong>−0,047</strong>", "3.042.763"],
           ["CDN-061", "475,6", "0,034", "0,0", "0,077", "2.917.057"],
           ["CDN-064", "703,7", "0,314", "1,5", "0,928", "1.930.071"]]), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Empat dari lima sumur penyumbang cadangan terbesar punya R² "
                   "di bawah 0,15.</strong> CDN-028 malah <strong>negatif</strong> — "
                   "menebak garis datar rata-rata saja lebih akurat daripada kurva yang "
                   "barusan kamu pasang. Dan justru sumur-sumur inilah yang menyumbang "
                   "mayoritas angka cadangannya."))

langkah("Kenapa fit yang buruk justru menghasilkan cadangan besar?",
    kode("print('korelasi R2 vs cadangan:', dca.r2.corr(dca.sisa_cadangan_bbl).round(3))"),
    blok("hasil", "<p><code>korelasi R2 vs cadangan: −0.424</code></p>", "HARUS MUNCUL"),
    "<p>Korelasinya negatif: makin buruk fit-nya, makin besar cadangan yang "
    "dijanjikannya. Empat belas sumur ber-R² di bawah 0,5 menyumbang "
    "<strong>21.002.225 bbl — 41,6% dari seluruh angka cadangan.</strong></p>",
    blok("catatan", "Kalau kurva tidak bisa mengikuti data, <code>curve_fit</code> mencari "
                    "jalan tengah — biasanya menekan D ke batas bawah atau menaikkan b ke "
                    "batas atas. Keduanya menghasilkan kurva nyaris datar, dan kurva datar "
                    "diproyeksikan 30 tahun menghasilkan cadangan sangat besar. Cek sendiri: "
                    "<code>(dca.D_fit<=0.0101).sum()</code> memberi <strong>4</strong>, dan "
                    "parameter b menempel batas pada <strong>39 dari 59 sumur</strong>."))

langkah("Aturan yang perlu kamu bawa seumur karier",
    blok("catatan", "<strong>Kode yang berjalan tanpa eror tidak memberitahumu apa pun "
                    "tentang benar atau salahnya.</strong>", None),
    "<p>Ini berlaku jauh di luar DCA — regresi yang tidak konvergen, join yang "
    "menggandakan baris, rata-rata yang menyembunyikan sebaran. Tiga pertanyaan wajib "
    "untuk setiap model: seberapa cocok <em>yang terburuk</em> (bukan rata-rata saja)? "
    "Apakah parameternya menempel di batas? Apakah hasilnya masuk akal secara fisik?</p>",
    "<p>Besok kamu cari tahu <em>kenapa</em> fit-nya gagal — dengan melihat datanya, "
    "bukan mengganti-ganti modelnya.</p>")

HARI1 = {
  "n": "MIGAS HARI 29",
  "tab": "29",
  "judul": "Tahap A: fit yang jalan mulus dan salah total",
  "waktu": "± 90 menit",
  "tujuan": "memasang kurva Arps pada data produksi, dan mengenali kapan sebuah fit "
            "yang “berhasil” sebenarnya tidak boleh dipercaya.",
  "langkah": L,
  "tutup_judul": "Hari 29 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu fungsi Arps, satu error nyata yang "
           "kamu perbaiki sendiri (IndexError pada sumur injeksi), dan satu angka "
           "cadangan yang kelihatan rapi tapi separuhnya ditopang fit yang buruk.</p>"
           "<p style=\"margin-top:8px\">Besok: berhenti menebak model, dan mulai "
           "melihat data mentahnya.</p>",
}
