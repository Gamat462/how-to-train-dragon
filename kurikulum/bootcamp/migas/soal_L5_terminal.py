import sqlite3, pandas as pd, numpy as np
from scipy.optimize import curve_fit
con=sqlite3.connect("migas.db")
prod=pd.read_sql("SELECT * FROM produksi_harian",con,parse_dates=["tanggal"])
sumur=pd.read_sql("SELECT * FROM sumur",con,parse_dates=["tanggal_onstream"])
wo=pd.read_sql("SELECT * FROM workover",con,parse_dates=["tanggal_mulai"]); con.close()

def arps(t,qi,D,b): return qi/np.power(1+b*D*t,1/b)

D_TERMINAL, Q_LIMIT, BUFFER, MIN_BLN = 0.08, 15.0, 270, 14

def proyeksi(qi,D,b,n=1200):
    """Hiperbolik lalu BERALIH ke eksponensial saat laju decline sesaat < D_TERMINAL."""
    t=np.arange(n)/12.0
    D_sesaat=D/(1+b*D*t)                       # laju decline sesaat Arps
    sw=np.argmax(D_sesaat<D_TERMINAL) if (D_sesaat<D_TERMINAL).any() else None
    q=arps(t,qi,D,b)
    if sw is not None and sw>0:
        q_sw=q[sw]; t_sw=t[sw]
        q[sw:]=q_sw*np.exp(-D_TERMINAL*(t[sw:]-t_sw))
    q=q[q>Q_LIMIT]
    return q, (sw if sw is not None else -1)

rows=[]
for w,g in prod[prod.berproduksi==1].groupby("sumur_id"):
    g=g.sort_values("tanggal"); wl=wo[wo.sumur_id==w].tanggal_mulai
    mulai=g.tanggal.min()
    if len(wl): mulai=max(mulai, wl.max()+pd.Timedelta(days=BUFFER))
    m=g[g.tanggal>=mulai].set_index("tanggal").oil_bopd.resample("MS").mean().dropna()
    if len(m)<MIN_BLN: continue
    t,q=np.arange(len(m))/12.0,m.values
    try:
        popt,_=curve_fit(arps,t,q,p0=[q[0],.3,.5],
            bounds=([q[0]*.5,.05,.05],[q[0]*1.8,1.5,1.0]),maxfev=20000)   # b DIBATASI <= 1.0
    except Exception: continue
    qi,D,b=popt; r2=1-((q-arps(t,*popt))**2).sum()/max(((q-q.mean())**2).sum(),1e-9)
    if r2<0.5: continue
    qf,sw=proyeksi(qi,D,b)
    qf=qf[len(m):] if len(qf)>len(m) else np.array([])
    rows.append((w,round(qi,1),round(D,3),round(b,3),round(r2,3),len(m),
                 round(g.oil_bopd.sum(),0),round(qf.sum()*30.44,0),len(qf),sw))
d=pd.DataFrame(rows,columns=["sumur_id","qi_fit","D_fit","b_fit","r2","bulan_dipakai",
      "kumulatif_bbl","sisa_cadangan_bbl","umur_sisa_bulan","bulan_switch"])
d=d.merge(sumur[["sumur_id","lapangan_id","decline_D_tahunan","qi_oil_bopd"]],on="sumur_id")
d["eur_bbl"]=d.kumulatif_bbl+d.sisa_cadangan_bbl

print("="*74); print("L5.1 FINAL — DCA + b<=1.0 + terminal exponential decline 8%/thn")
print(f"sumur lolos       : {len(d)} | R2 rata2 {d.r2.mean():.3f} (min {d.r2.min():.3f})")
print(f"mentok 1200 bln   : {(d.umur_sisa_bulan>=1150).sum()} sumur")
print(f"umur sisa: median {d.umur_sisa_bulan.median():.0f} bln, maks {d.umur_sisa_bulan.max()} bln")
print(f"b_fit mentok di 1.0: {(d.b_fit>=0.999).sum()} sumur")
print(f"\nEUR total       : {d.eur_bbl.sum():,.0f} bbl")
print(f"Sisa cadangan   : {d.sisa_cadangan_bbl.sum():,.0f} bbl")
print(f"Pengurasan      : {d.kumulatif_bbl.sum()/d.eur_bbl.sum()*100:.1f}%")
print("\nBANDINGKAN dgn versi tanpa terminal decline (sisa 21.562.234 bbl):")
print(f"  selisih: {21562234-d.sisa_cadangan_bbl.sum():,.0f} bbl "
      f"({(21562234-d.sisa_cadangan_bbl.sum())/21562234*100:.1f}% lebih rendah)")
print("\n5 sisa cadangan terbesar:")
print(d.nlargest(5,"sisa_cadangan_bbl")[["sumur_id","lapangan_id","qi_fit","D_fit","b_fit",
      "r2","sisa_cadangan_bbl","umur_sisa_bulan","bulan_switch"]].to_string(index=False))
print("\nper lapangan:")
print(d.groupby("lapangan_id").agg(n=("sumur_id","size"),r2=("r2","mean"),
      sisa_bbl=("sisa_cadangan_bbl","sum"),umur_med=("umur_sisa_bulan","median")).round(2).to_string())
d.to_csv("data/jawaban_L5_dca.csv",index=False)
