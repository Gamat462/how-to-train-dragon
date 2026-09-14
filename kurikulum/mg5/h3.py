# -*- coding: utf-8 -*-
"""Hari 31 — Tahap C: segmen bersih, dan keberanian membuang 33 dari 59 sumur."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Terjemahkan rancangan kemarin jadi kode: potong segmennya",
    blok("aksi", "Tiga perubahan dari tahap A: potong data ke segmen bersih, tolak "
                 "segmen terlalu pendek, dan tolak fit yang R²-nya rendah.", "LAKUKAN"),
    kode("""BUFFER  = 270   # hari sesudah workover terakhir yang dibuang
MIN_BLN = 14    # panjang minimum segmen bersih

hasil, ditolak = [], []
for w, g in prod2.groupby("sumur_id"):
    g  = g[g.berproduksi==1].sort_values("tanggal")
    wl = wo[wo.sumur_id == w].tanggal_mulai
    mulai_bersih = g.tanggal.min()
    if len(wl):
        mulai_bersih = max(mulai_bersih, wl.max() + pd.Timedelta(days=BUFFER))
    seg = g[g.tanggal >= mulai_bersih]
    m = seg.set_index("tanggal").oil_bopd.resample("MS").mean().dropna()
    if len(m) < MIN_BLN:
        ditolak.append((w, len(m), "segmen bersih terlalu pendek")); continue"""),
    "<p>Sampai sini baru penyaringan panjang segmen. Fit dan kendali mutu R² menyusul "
    "di langkah berikutnya — dipisah supaya kamu bisa membaca tiap bagian sendiri.</p>")

langkah("Lanjutkan: fit, lalu tolak yang cocoknya buruk",
    kode("""    t, q = np.arange(len(m))/12.0, m.values
    try:
        popt, _ = curve_fit(arps, t, q, p0=[q[0],0.3,0.5],
                            bounds=([q[0]*0.5,0.05,0.05],[q[0]*1.8,1.5,1.2]), maxfev=20000)
    except Exception:
        ditolak.append((w, len(m), "fit gagal")); continue
    qi, D, b = popt
    r2 = 1 - ((q-arps(t,*popt))**2).sum() / max(((q-q.mean())**2).sum(), 1e-9)
    if r2 < 0.5:                                       # KENDALI MUTU
        ditolak.append((w, len(m), f"R2 rendah {r2:.2f}")); continue
    tf = np.arange(len(m), len(m)+480)/12.0
    qf = arps(tf, *popt); qf = qf[qf > 15]
    hasil.append((w, round(qi,1), round(D,3), round(b,3), round(r2,3), len(m),
                  round(g.oil_bopd.sum(),0), round(qf.sum()*30.44,0), len(qf)))"""),
    blok("catatan", "<strong>R² &lt; 0,5 ditolak, bukan diterima dengan catatan.</strong> "
                    "Ambang ini kamu pilih sendiri, sama seperti BUFFER dan MIN_BLN — dan "
                    "kamu akan mengujinya juga."))

langkah("Rangkum, lalu lihat hasilnya",
    kode("""dca = pd.DataFrame(hasil, columns=["sumur_id","qi_fit","D_fit","b_fit","r2",
                   "bulan_dipakai","kumulatif_bbl","sisa_cadangan_bbl","umur_sisa_bulan"])
dca["eur_bbl"] = dca.kumulatif_bbl + dca.sisa_cadangan_bbl
print(f"lolos {len(dca)} | ditolak {len(ditolak)} | R2 rata-rata {dca.r2.mean():.3f} (min {dca.r2.min():.3f})")
print(f"Sisa cadangan: {dca.sisa_cadangan_bbl.sum():,.0f} bbl | EUR: {dca.eur_bbl.sum():,.0f} bbl")"""),
    blok("hasil", "<p><strong>lolos 26 sumur · ditolak 33 · R² rata-rata 0,995 "
                  "(minimum 0,976)</strong></p><p style=\"margin-top:8px\">Sisa cadangan "
                  "<strong>21.562.234 bbl</strong> · EUR total <strong>31.347.381 bbl</strong> "
                  "· Pengurasan <strong>31,2%</strong></p>", "HARUS MUNCUL"))

langkah("Bandingkan tahap A dan tahap C",
    tabel(["", "Tahap A (naif)", "Tahap C (segmen bersih)"],
          [["Sumur dipakai", "59", "26"],
           ["R² rata-rata", "0,701", "<strong>0,995</strong>"],
           ["R² minimum", "<strong>−0,047</strong>", "0,976"],
           ["Sisa cadangan", "<strong>50.544.537 bbl</strong>", "<strong>21.562.234 bbl</strong>"]]),
    "<p>Cadangannya <strong>turun 57%</strong>. Pada netback kontraktor sekitar "
    "$19,79/bbl, selisih 29 juta barel itu setara lebih dari <strong>$570 juta</strong> "
    "nilai yang tidak pernah ada.</p>",
    blok("catatan", "<strong>Perhatikan arahnya:</strong> analisis yang lebih benar "
                    "menghasilkan angka yang lebih kecil. Ini hampir selalu terjadi, dan "
                    "analis sering dapat tekanan halus untuk tidak terlalu teliti — versi "
                    "teliti selalu terdengar lebih mengecewakan di ruang rapat. Bertahan "
                    "pada angka yang benar ketika angka yang salah lebih disukai: itu yang "
                    "membedakan analis yang dipercaya."))

langkah("Cara melaporkan bahwa kamu membuang 56% sampelmu",
    kode('print(Counter(x[2].split(" R2")[0] for x in ditolak))'),
    blok("hasil", "<p><code>{'segmen bersih terlalu pendek': 33}</code> — seluruh "
                  "penolakan dari satu sebab yang sama, tak satu pun karena R² rendah.</p>",
         "HARUS MUNCUL"),
    "<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0\">"
    "<div class=\"bahaya\" style=\"margin:0\"><strong>Salah:</strong> “Cadangan blok "
    "diperkirakan 21,6 juta barel.” — pembaca menyangka ini seluruh blok.</div>"
    "<div class=\"catatan\" style=\"margin:0\"><strong>Benar:</strong> “Sisa "
    "cadangan 26 sumur yang memenuhi syarat: 21,6 juta barel. 33 sumur tak dapat "
    "dinilai karena segmen bersihnya lebih pendek dari 14 bulan — angka ini bersifat "
    "<em>batas bawah</em>.”</div></div>")

langkah("Uji sensitivitas: seberapa jauh jawabanmu bergantung pada pilihanmu?",
    "<p>270 hari dan 14 bulan kamu pilih sendiri, tidak ada hukum fisika di baliknya. "
    "Bungkus kode di atas jadi fungsi <code>run(BUFFER, MIN_BLN)</code>, lalu panggil "
    "untuk enam kombinasi.</p>",
    kode('for buf, mb in [(180,14),(270,14),(365,14),(270,12),(270,18),(270,24)]:\n'
         '    print(buf, mb, run(buf, mb))'),
    tabel(["buffer", "min bulan", "lolos", "sisa cadangan (bbl)", "R² rata2"],
          [["180", "14", "28", "22.941.752", "0,994"],
           ["<strong>270</strong>", "<strong>14</strong>", "<strong>26</strong>", "<strong>21.562.232</strong>", "0,995"],
           ["365", "14", "26", "20.101.273", "0,994"],
           ["270", "12", "27", "22.236.946", "0,995"],
           ["270", "18", "25", "21.246.379", "0,996"],
           ["270", "24", "21", "15.489.111", "0,996"]]),
    "<p>Rentangnya <strong>15,5 sampai 22,9 juta barel</strong> — selisih 48% dari angka "
    "terendah, hanya karena dua angka yang kamu pilih sendiri.</p>",
    blok("catatan", "<strong>Ini bukan kabar buruk; ini hasil.</strong> R² tetap di "
                    "0,994–0,996 di semua kombinasi — kualitas fit tidak bisa dipakai "
                    "memilih di antaranya, semuanya sama-sama cocok tapi jawabannya "
                    "berbeda. Model yang cocok tidak sama dengan model yang benar. "
                    "<strong>Kalau angkamu sedikit beda dari tabel ini,</strong> cek "
                    "urutan kombinasi <code>run()</code>-mu — hasilnya sensitif terhadap "
                    "urutan pemrosesan kalau ada bug penyaringan yang tidak stabil."))

langkah("Satu masalah yang belum selesai",
    "<p>Lihat lagi keluaran tahap C: <strong>umur sisa mentok 480 bulan: 12 sumur.</strong> "
    "Empat ratus delapan puluh bulan = 40 tahun, pagu yang kita pasang sendiri. Dua "
    "belas dari 26 sumur mencapainya — modelnya <em>belum juga</em> sampai batas "
    "ekonomis 15 bopd setelah 40 tahun.</p>",
    blok("bahaya", "<strong>Cadangan 12 sumur itu bukan hasil model — ia hasil dari di "
                   "mana kita kebetulan berhenti.</strong> Naikkan pagunya, angkanya "
                   "naik. Turunkan, angkanya turun. Angka yang mengikuti pilihan "
                   "sewenang-wenang bukan estimasi, melainkan artefak."),
    "<p>Besok kamu cari tahu kenapa kurvanya tidak pernah berakhir — dan kenapa itu "
    "bukan cacat kode, melainkan sifat matematis Arps yang sudah diketahui sejak "
    "lama.</p>")

HARI3 = {
  "n": "MIGAS HARI 31",
  "tab": "31",
  "judul": "Tahap C: segmen bersih — dan keberanian membuang 33 dari 59 sumur",
  "waktu": "± 90 menit",
  "tujuan": "menerapkan kendali mutu pada sebuah model, melaporkan apa yang kamu buang "
            "dengan jujur, dan menguji seberapa banyak kesimpulanmu bergantung pada "
            "pilihan yang kamu buat sendiri.",
  "langkah": L,
  "tutup_judul": "Hari 31 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> angka cadangan turun 57% begitu kamu "
           "membuang data terkontaminasi, dan kamu tahu persis rentang ketidakpastiannya "
           "(15,5–22,9 juta bbl) karena kamu mengujinya sendiri.</p>",
}
