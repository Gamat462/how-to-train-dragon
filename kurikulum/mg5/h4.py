# -*- coding: utf-8 -*-
"""Hari 32 — Tahap D & E: kurva yang tidak pernah berakhir, dan cara industri mengakhirinya."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Tahap D — buktikan sendiri bahwa proyeksinya tidak konvergen",
    blok("aksi", "Ambil CDN-062, penyumbang cadangan terbesar di tahap C (3.188.119 "
                 "bbl, D 0,253, b 1,200, R² 0,996). Proyeksikan dengan pagu yang "
                 "digandakan terus.", "LAKUKAN"),
    kode("""r = dca[dca.sumur_id == "CDN-062"].iloc[0]
for pagu in [240, 480, 960, 1920, 3840]:
    tf = np.arange(24, 24+pagu) / 12.0
    qf = arps(tf, r.qi_fit, r.D_fit, r.b_fit)
    qf = qf[qf > 15]
    print(f"pagu {pagu:>5} bln -> {qf.sum()*30.44:>12,.0f} bbl")"""),
    blok("hasil", tabel(["pagu", "cadangan"],
          [["240 bln (20 thn)", "2.208.713 bbl"], ["480 bln (40 thn)", "3.188.119 bbl"],
           ["960 bln (80 thn)", "4.365.075 bbl"], ["1.920 bln (160 thn)", "5.735.222 bbl"],
           ["3.840 bln (320 thn)", "7.302.488 bbl"]]), "HARUS MUNCUL"),
    "<p>Setiap kali pagunya digandakan, cadangannya bertambah lagi, dan lajunya tidak "
    "pernah jatuh di bawah 15 bopd. Sumur ini, menurut modelmu, berproduksi "
    "selamanya.</p>")

langkah("Sebelum lanjut: pastikan dulu fungsi arps()-mu aman untuk b = 0",
    blok("aksi", "Ingat CDN-060 dari Hari 29 tahap A? Fit-nya mendarat di "
                 "<code>D_fit = 0,010</code> <strong>dan <code>b_fit = 0,0</code> "
                 "persis</strong>. Coba proyeksikan sumur itu dengan "
                 "<code>arps()</code> yang sudah kamu tulis.", "LAKUKAN"),
    kode('arps(np.array([0.0, 1.0, 2.0]), 536.9, 0.010, 0.0)', salin=True),
    blok("hasil", "<div class=\"kode\"><pre><code>Traceback (most recent call last):\n"
                  "  File \"&lt;stdin&gt;\", line 2, in arps\n"
                  "ZeroDivisionError: float division by zero</code></pre></div>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("catatan", "<strong>Bukan bug acak — ini titik lemah rumusnya sendiri.</strong> "
                    "Pangkat <code>1/b</code> di rumus Arps tidak terdefinisi kalau "
                    "<code>b</code> tepat nol, padahal b = 0 (penurunan eksponensial) "
                    "adalah kasus yang <em>paling umum</em> secara fisik. Untung "
                    "batasnya sudah kamu pasang di <code>curve_fit</code>, jadi "
                    "b tidak pernah persis 0 di tahap C — tapi kamu baru saja lihat "
                    "sendiri apa yang terjadi kalau pagarnya lepas."))

langkah("Kenapa kurvanya divergen — dan ini matematika, bukan bug",
    "<p>Untuk t besar, suku 1 di dalam <code>(1 + b·D·t)</code> jadi tak berarti, "
    "sehingga <code>q(t) ≈ qi · (b·D·t)^(−1/b)</code>. Produksi kumulatif adalah luas "
    "di bawah kurva itu, dan integralnya cuma konvergen kalau <strong>b &lt; 1</strong>.</p>",
    tabel(["kondisi", "artinya"],
          [["b &lt; 1", "kurva cukup curam, luasnya berhingga — cadangan konvergen"],
           ["b = 1 (harmonik)", "tepat di ambang; luasnya tumbuh seperti logaritma, pelan tapi tak pernah berhenti"],
           ["b &gt; 1", "kurva terlalu landai — <strong>cadangan tak berhingga</strong>"]]))

langkah("Periksa berapa banyak sumurmu yang kena",
    kode("""print("b >= 1.0            :", (dca.b_fit >= 1.0).sum())
print("b menempel batas 1.2:", (dca.b_fit >= 1.199).sum())
print("mentok pagu 480 bln :", (dca.umur_sisa_bulan >= 480).sum())
print(pd.crosstab(dca.b_fit >= 1.0, dca.umur_sisa_bulan >= 480))"""),
    blok("hasil", "<p>Dari 26 sumur: <strong>8 punya b ≥ 1,0</strong>, <strong>6</strong> "
                  "di antaranya menempel persis di dinding batas 1,2. Dua belas sumur "
                  "mentok di pagu 480 bulan.</p><p style=\"margin-top:8px\">Tabel "
                  "silangnya: 6 sumur mentok <em>karena</em> b ≥ 1 (divergen), dan 6 "
                  "lagi mentok meski b &lt; 1 — cuma sangat lambat (D kecil, butuh "
                  "ratusan tahun turun ke 15 bopd).</p>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Dua penyakit berbeda, satu gejala sama.</strong> Kalau "
                    "kamu cuma lihat “12 sumur mentok” tanpa memeriksa b-nya, "
                    "kamu akan menyangka satu masalah. Untungnya obatnya sama."))

langkah("Dua koreksi standar industri",
    "<p><strong>Koreksi 1 — batasi b ≤ 1,0.</strong> Nilai b di atas 1 muncul dari fit, "
    "tapi tidak punya penjelasan fisik untuk reservoir minyak konvensional. Ini pilihan "
    "<em>fisika</em>, bukan pilihan statistik.</p>",
    "<p><strong>Koreksi 2 — terminal exponential decline,</strong> yang lebih penting. "
    "Laju penurunan sesaat pada kurva Arps adalah <code>D_sesaat(t) = D / (1 + b·D·t)</code> "
    "— <strong>terus mengecil</strong> seiring waktu. Secara fisik itu tidak terjadi; "
    "sumur tua menurun pada laju yang kurang lebih tetap sampai mati.</p>",
    "<p>Koreksinya: begitu D_sesaat jatuh di bawah <strong>8% per tahun</strong>, "
    "<strong>ganti</strong> kurvanya jadi eksponensial murni pada laju itu. Eksponensial "
    "selalu konvergen.</p>")

langkah("Tulis fungsi koreksinya",
    kode("""D_TERMINAL, Q_LIMIT = 0.08, 15.0

def proyeksi(qi, D, b, n=1200):
    t = np.arange(n) / 12.0
    D_sesaat = D / (1 + b*D*t)
    sw = np.argmax(D_sesaat < D_TERMINAL) if (D_sesaat < D_TERMINAL).any() else None
    q = arps(t, qi, D, b)
    if sw is not None and sw > 0:
        q_sw, t_sw = q[sw], t[sw]
        q[sw:] = q_sw * np.exp(-D_TERMINAL * (t[sw:] - t_sw))   # sambung mulus
    return q[q > Q_LIMIT], (sw if sw is not None else -1)""", salin=False),
    blok("catatan", "Perhatikan baris <code>q[sw:] = q_sw * np.exp(...)</code>. Kurva "
                    "baru dimulai dari nilai <code>q_sw</code> yang sama persis di titik "
                    "peralihan, jadi tidak ada lompatan. Menyambung dua model tanpa "
                    "memastikan keduanya bertemu di titik sambungan adalah salah satu "
                    "kesalahan paling sering dan paling sulit terlihat — hasilnya "
                    "kelihatan wajar di tabel, tapi ada patahan di grafiknya."))

langkah("Jalankan tahap E, dan bandingkan seluruh lima tahap",
    "<p>Ulangi kode tahap C dengan dua perubahan: batas atas b jadi <code>1.0</code> "
    "pada <code>curve_fit</code>, dan ganti proyeksinya dengan <code>proyeksi()</code> "
    "di atas.</p>",
    blok("hasil", "<p><strong>26 sumur lolos · R² rata-rata 0,995 (min 0,973) · mentok "
                  "pagu: 0 sumur</strong></p><p style=\"margin-top:8px\">Umur sisa: "
                  "median <strong>285 bulan</strong> (23,8 tahun), maksimum 532 bulan. "
                  "Delapan sumur ber-b menempel di 1,0.</p><p style=\"margin-top:8px\">"
                  "EUR total <strong>27.412.621 bbl</strong> · Sisa cadangan "
                  "<strong>17.627.474 bbl</strong> · Pengurasan <strong>35,7%</strong></p>",
         "HARUS MUNCUL"),
    tabel(["Tahap", "Yang diperbaiki", "Sumur", "R² min", "Sisa cadangan"],
          [["A — naif", "—", "59", "−0,047", "50.544.537 bbl"],
           ["C — segmen bersih", "buang data terkontaminasi + QC R²", "26", "0,976", "21.562.234 bbl"],
           ["<strong>E — final</strong>", "b ≤ 1,0 + terminal decline 8%/thn", "<strong>26</strong>", "<strong>0,973</strong>", "<strong>17.627.474 bbl</strong>"]]),
    "<p>Dari 50,5 juta barel ke 17,6 juta barel — <strong>angka akhirnya 65% lebih "
    "kecil</strong> daripada yang dihasilkan analisis pertama yang berjalan tanpa eror "
    "sedikit pun.</p>")

langkah("Lima kalimat untuk catatanmu — ini bahan wawancaramu nanti",
    "<ul style=\"font-size:0.93rem;padding-left:20px\">"
    "<li><strong>Tahap A:</strong> kode berjalan mulus bukan berarti hasilnya benar. "
    "Periksa yang terburuk, bukan rata-ratanya.</li>"
    "<li><strong>Tahap B:</strong> ketika model gagal, lihat datanya — jangan ganti "
    "modelnya. Modelnya biasanya benar; datanya yang melanggar asumsi.</li>"
    "<li><strong>Tahap C:</strong> membuang data tak memenuhi syarat adalah kendali "
    "mutu, bukan kecurangan — asal kamu laporkan apa yang dibuang dan mengapa.</li>"
    "<li><strong>Tahap D:</strong> hasil yang berubah mengikuti pilihan sewenang-wenang "
    "bukan estimasi, melainkan artefak.</li>"
    "<li><strong>Tahap E:</strong> ketika matematika dan fisika bertentangan, fisika "
    "yang menang.</li></ul>",
    blok("catatan", "<strong>Ini cerita jauh lebih kuat daripada “aku bikin model "
                    "dan R²-nya 0,995”.</strong> Siapa pun bisa menempelkan "
                    "<code>curve_fit</code> ke data. Yang jarang: orang yang bisa "
                    "menceritakan kenapa jawaban pertamanya salah, bagaimana ia "
                    "mengetahuinya, dan apa yang ia ubah."))

HARI4 = {
  "n": "MIGAS HARI 32",
  "tab": "32",
  "judul": "Tahap D & E: kurva yang tidak pernah berakhir, dan cara industri mengakhirinya",
  "waktu": "± 90 menit",
  "tujuan": "mengenali kapan sebuah model matematis menghasilkan hasil tak berhingga, "
            "dan menerapkan koreksi standar industri untuk mengembalikannya masuk akal "
            "secara fisik.",
  "langkah": L,
  "tutup_judul": "Hari 32 selesai — jalur DCA selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> dari 50,5 juta barel (naif, tanpa eror) "
           "ke 17,6 juta barel (diperiksa, dengan dua koreksi fisika) — dan kamu bisa "
           "menjelaskan tepat kenapa selisihnya sebesar itu. Ini kebiasaan yang sama "
           "seperti audit: angka pertama yang rapi belum tentu angka yang benar.</p>"
           "<p style=\"margin-top:8px\">Besok: dua tempat lain angka bisa dibuat jadi "
           "apa saja tanpa satu pun kode yang salah — batas ekonomis dan alokasi "
           "biaya. Itu wajar terasa mirip pekerjaan lamamu, karena memang begitu.</p>",
}
