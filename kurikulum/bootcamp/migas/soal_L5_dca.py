import sqlite3, pandas as pd, numpy as np
from scipy.optimize import curve_fit
con = sqlite3.connect("migas.db")
prod = pd.read_sql("SELECT * FROM produksi_harian", con, parse_dates=["tanggal"])
sumur= pd.read_sql("SELECT * FROM sumur", con, parse_dates=["tanggal_onstream"])
wo   = pd.read_sql("SELECT * FROM workover", con, parse_dates=["tanggal_mulai"])
con.close()

def arps(t,qi,D,b): return qi/np.power(1+b*D*t, 1/b)

BUFFER = 270      # hari sesudah workover yang dibuang (efeknya masih meluruh)
MIN_BLN = 14      # minimal panjang segmen bersih

hasil, ditolak = [], []
for w, g in prod[prod.berproduksi==1].groupby("sumur_id"):
    g = g.sort_values("tanggal")
    wl = wo[wo.sumur_id==w].tanggal_mulai
    mulai_bersih = g.tanggal.min()
    if len(wl):                                   # ambil SETELAH workover terakhir + buffer
        mulai_bersih = max(mulai_bersih, wl.max()+pd.Timedelta(days=BUFFER))
    seg = g[g.tanggal >= mulai_bersih]
    m = seg.set_index("tanggal").oil_bopd.resample("MS").mean().dropna()
    if len(m) < MIN_BLN:
        ditokan = ditolak.append((w, len(m), "segmen bersih terlalu pendek")); continue
    t, q = np.arange(len(m))/12.0, m.values
    try:
        popt,_ = curve_fit(arps, t, q, p0=[q[0],0.3,0.5],
                           bounds=([q[0]*0.5,0.05,0.05],[q[0]*1.8,1.5,1.2]), maxfev=20000)
    except Exception as e:
        ditolak.append((w,len(m),"fit gagal")); continue
    qi,D,b = popt
    pred = arps(t,*popt)
    r2 = 1-((q-pred)**2).sum()/max(((q-q.mean())**2).sum(),1e-9)
    if r2 < 0.5:
        ditolak.append((w,len(m),f"R2 rendah {r2:.2f}")); continue
    tf = np.arange(len(m), len(m)+480)/12.0
    qf = arps(tf,*popt); qf = qf[qf>15]
    hasil.append((w, round(qi,1),round(D,3),round(b,3),round(r2,3),len(m),
                  round(g.oil_bopd.sum(),0), round(qf.sum()*30.44,0), len(qf)))

dca = pd.DataFrame(hasil, columns=["sumur_id","qi_fit","D_fit","b_fit","r2","bulan_dipakai",
                    "kumulatif_bbl","sisa_cadangan_bbl","umur_sisa_bulan"])
dca = dca.merge(sumur[["sumur_id","lapangan_id","qi_oil_bopd","decline_D_tahunan","arps_b"]],on="sumur_id")
dca["eur_bbl"] = dca.kumulatif_bbl + dca.sisa_cadangan_bbl

print("="*72); print("L5.1 (DIPERBAIKI) — DCA hanya pada segmen bersih pasca-workover")
print(f"lolos kendali mutu : {len(dca)} sumur")
print(f"ditolak            : {len(ditolak)} sumur")
print(f"R2 rata-rata       : {dca.r2.mean():.3f} | minimum {dca.r2.min():.3f}")
print(f"umur sisa mentok 480 bln: {(dca.umur_sisa_bulan>=480).sum()} sumur")
print("\nalasan penolakan:")
for a,c in pd.Series([x[2].split(' R2')[0] for x in ditolak]).value_counts().items():
    print(f"  {a}: {c}")
print("\n5 sisa cadangan terbesar:")
print(dca.nlargest(5,"sisa_cadangan_bbl")[["sumur_id","lapangan_id","qi_fit","D_fit","b_fit",
      "r2","bulan_dipakai","kumulatif_bbl","sisa_cadangan_bbl","umur_sisa_bulan"]].to_string(index=False))
print(f"\nEUR total (sumur lolos)  : {dca.eur_bbl.sum():,.0f} bbl")
print(f"Sisa cadangan            : {dca.sisa_cadangan_bbl.sum():,.0f} bbl")
print(f"Tingkat pengurasan       : {dca.kumulatif_bbl.sum()/dca.eur_bbl.sum()*100:.1f}%")
print("\nUJI KEJUJURAN — fit vs parameter asli yang dipakai membuat data:")
print(f"  korelasi D  : {dca.D_fit.corr(dca.decline_D_tahunan):.3f}")
print(f"  korelasi qi : {dca.qi_fit.corr(dca.qi_oil_bopd):.3f}")
print(f"  median |D_fit - D_asli| : {(dca.D_fit-dca.decline_D_tahunan).abs().median():.3f}")
dca.to_csv("data/jawaban_L5_dca.csv", index=False)
print("\nper lapangan:")
print(dca.groupby("lapangan_id").agg(n=("sumur_id","size"), r2=("r2","mean"),
      sisa_bbl=("sisa_cadangan_bbl","sum")).round(3).to_string())
