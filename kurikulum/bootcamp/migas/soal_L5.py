import sqlite3, pandas as pd, numpy as np
from scipy.optimize import curve_fit
con = sqlite3.connect("migas.db")
prod  = pd.read_sql("SELECT * FROM produksi_harian", con, parse_dates=["tanggal"])
sumur = pd.read_sql("SELECT * FROM sumur", con, parse_dates=["tanggal_onstream"])
icp   = pd.read_sql("SELECT * FROM harga_icp", con)
psc   = pd.read_sql("SELECT * FROM psc_bulanan", con)
biaya = pd.read_sql("SELECT * FROM biaya_operasi", con)

print("="*72); print("L5.1 — FIT KURVA DECLINE ARPS & RAMALKAN EUR")
def arps(t, qi, D, b):
    return np.where(np.abs(b) < 1e-6, qi*np.exp(-D*t), qi/np.power(1+b*D*t, 1/np.maximum(b,1e-6)))

hasil = []
for w, g in prod[prod.berproduksi==1].groupby("sumur_id"):
    g = g.sort_values("tanggal")
    if len(g) < 400: continue
    m = g.set_index("tanggal").oil_bopd.resample("MS").mean().dropna()
    if len(m) < 18: continue
    t = np.arange(len(m))/12.0
    q = m.values
    try:
        popt,_ = curve_fit(arps, t, q, p0=[q[0], 0.3, 0.5],
                           bounds=([q[0]*0.4,0.01,0.0],[q[0]*2.5,2.0,1.5]), maxfev=8000)
    except Exception: continue
    qi,D,b = popt
    pred = arps(t,*popt)
    r2 = 1 - ((q-pred)**2).sum()/((q-q.mean())**2).sum()
    # EUR sampai batas ekonomis 15 bopd, maksimum 30 tahun
    t_fut = np.arange(len(m), len(m)+360)/12.0
    q_fut = arps(t_fut,*popt)
    q_fut = q_fut[q_fut > 15]
    eur_sisa = q_fut.sum()*30.44
    kum = g.oil_bopd.sum()
    hasil.append((w, round(qi,1), round(D,3), round(b,3), round(r2,3),
                  round(kum,0), round(eur_sisa,0), round(kum+eur_sisa,0),
                  len(q_fut)))
dca = pd.DataFrame(hasil, columns=["sumur_id","qi_fit","D_fit","b_fit","r2",
        "kumulatif_bbl","sisa_cadangan_bbl","eur_bbl","umur_sisa_bulan"])
dca = dca.merge(sumur[["sumur_id","lapangan_id","qi_oil_bopd","decline_D_tahunan","arps_b"]], on="sumur_id")
print(f"berhasil fit: {len(dca)} sumur | R2 rata-rata {dca.r2.mean():.3f} | R2 min {dca.r2.min():.3f}")
print("\n5 sumur dengan sisa cadangan terbesar:")
print(dca.nlargest(5,"sisa_cadangan_bbl")[
  ["sumur_id","lapangan_id","qi_fit","D_fit","b_fit","r2","kumulatif_bbl","sisa_cadangan_bbl","umur_sisa_bulan"]].to_string(index=False))
print(f"\nTOTAL EUR seluruh lapangan : {dca.eur_bbl.sum():,.0f} bbl")
print(f"Sudah diproduksi           : {dca.kumulatif_bbl.sum():,.0f} bbl")
print(f"Sisa cadangan              : {dca.sisa_cadangan_bbl.sum():,.0f} bbl")
print(f"Tingkat pengurasan         : {dca.kumulatif_bbl.sum()/dca.eur_bbl.sum()*100:.1f}%")
print("\nseberapa dekat hasil fit dgn parameter asli (uji kejujuran model):")
print(f"  korelasi D  fit vs asli: {dca.D_fit.corr(dca.decline_D_tahunan):.3f}")
print(f"  korelasi qi fit vs asli: {dca.qi_fit.corr(dca.qi_oil_bopd):.3f}")

print("\n"+"="*72); print("L5.2 — BATAS EKONOMIS PER SUMUR (economic limit rate)")
opex25 = biaya[(biaya.jenis=="OPEX") & (biaya.periode.str.startswith("2025"))]
opex_per_lap = opex25.groupby("lapangan_id").nilai_usd.sum()
n_sumur = sumur[sumur.tipe_sumur=="Producer"].groupby("lapangan_id").size()
opex_bln_sumur = (opex_per_lap/12/n_sumur).round(0)
print("biaya operasi per sumur per bulan (USD):"); print(opex_bln_sumur.to_string())
for harga in [50, 65, 80]:
    el = (opex_bln_sumur/(30.44*harga)).round(1)
    print(f"  batas ekonomis @ ${harga}/bbl : " + ", ".join(f"{k}={v} bopd" for k,v in el.items()))

akhir = prod[prod.tanggal>="2026-04-01"].groupby("sumur_id").oil_bopd.mean()
cek = pd.DataFrame({"bopd": akhir}).join(sumur.set_index("sumur_id")[["lapangan_id"]])
cek["batas_65"] = cek.lapangan_id.map(opex_bln_sumur/(30.44*65))
cek["di_bawah_batas"] = cek.bopd < cek.batas_65
print(f"\nsumur di bawah batas ekonomis @ $65/bbl: {cek.di_bawah_batas.sum()} dari {len(cek)}")
if cek.di_bawah_batas.sum():
    print(cek[cek.di_bawah_batas].round(1).to_string())

print("\n"+"="*72); print("L5.3 — ALOKASI BIAYA: tiga metode, hasil berbeda")
vol25 = prod[prod.tanggal.dt.year==2025].merge(sumur[["sumur_id","lapangan_id"]],on="sumur_id")
v = vol25.groupby("lapangan_id").oil_bopd.sum()
n = n_sumur
akt = vol25[vol25.berproduksi==1].groupby("lapangan_id").size()
ga = biaya[(biaya.kategori_biaya=="G&A Allocation")&(biaya.periode.str.startswith("2025"))].nilai_usd.sum()
alok = pd.DataFrame({
    "per_volume":  ga*v/v.sum(),
    "per_sumur":   ga*n/n.sum(),
    "per_hari_aktif": ga*akt/akt.sum()}).round(0)
alok["selisih_maks"] = (alok.max(axis=1)-alok.min(axis=1)).round(0)
print(f"total G&A 2025 yang dialokasikan: ${ga:,.0f}"); print(alok.to_string())
print(f"\nSelisih terbesar: ${alok.selisih_maks.max():,.0f} pada {alok.selisih_maks.idxmax()}"
      f" — {alok.selisih_maks.max()/ga*100:.1f}% dari total G&A")

print("\n"+"="*72); print("L5.4 — SENSITIVITAS PSC TERHADAP HARGA")
base = psc.copy()
def hitung(icp_baru_faktor):
    d = base.copy()
    d["gross"] = d.volume_bbl * d.icp_usd_bbl * icp_baru_faktor
    ftp = d.gross*0.20
    tersedia = d.gross - ftp
    cr = np.minimum(np.minimum(d.biaya_recoverable_usd, tersedia), d.gross*0.80)
    ets = np.maximum(tersedia-cr,0)
    gov = ftp*0.60 + ets*0.85
    kon_pre = ftp*0.40 + ets*0.15
    pajak = np.maximum(kon_pre,0)*0.44
    return pd.Series({"gross":d.gross.sum(), "cost_recovery":cr.sum(),
                      "gov_take":(gov+pajak).sum(),
                      "kontraktor":(kon_pre-pajak+cr).sum()})
print(f"{'skenario':>12} {'gross':>16} {'cost_rec':>15} {'gov_take':>16} {'kontraktor':>15} {'gov%':>7}")
for f,lbl in [(0.7,"-30%"),(0.85,"-15%"),(1.0,"dasar"),(1.15,"+15%"),(1.3,"+30%")]:
    r = hitung(f)
    print(f"{lbl:>12} {r.gross:>16,.0f} {r.cost_recovery:>15,.0f} {r.gov_take:>16,.0f} "
          f"{r.kontraktor:>15,.0f} {r.gov_take/r.gross*100:>6.1f}%")
print("\nCatatan: perhatikan bagaimana porsi pemerintah NAIK saat harga naik.")
print("Itu sifat PSC cost recovery — biaya sudah tetap, jadi tambahan harga")
print("hampir seluruhnya masuk ke ETS yang dibagi 85:15.")

dca.to_csv("data/jawaban_L5_dca.csv", index=False)
con.close()
