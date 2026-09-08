import numpy as np, pandas as pd
OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/data"
rng = np.random.default_rng(999)

trx  = pd.read_csv(f"{OUT}/transaksi.csv", parse_dates=["tanggal"])
item = pd.read_csv(f"{OUT}/transaksi_item.csv")
pel  = pd.read_csv(f"{OUT}/pelanggan.csv", parse_dates=["tanggal_daftar"])

print("=== cek keterkaitan member (era aplikasi 2025+) ===")
era = trx[trx.tanggal >= "2025-01-01"]
print(f"  transaksi 2025+: {len(era):,} | ada pelanggan_id: {era.pelanggan_id.notna().mean()*100:.1f}%")

# ---------------------------------------------------------- A. DATA KOTOR
print("\n=== A. transaksi_kotor.csv ===")
src = trx[trx.tanggal.between("2026-01-01","2026-03-31")].sample(2500, random_state=7).copy()
src = src.merge(pd.read_csv(f"{OUT}/cabang.csv")[["cabang_id","kota"]], on="cabang_id", how="left")
k = src[["transaksi_id","tanggal","cabang_id","kota","saluran","metode_bayar","total"]].copy()
k["tanggal"] = k.tanggal.dt.strftime("%Y-%m-%d")
# kolom dibuat bertipe object supaya bisa menampung kekacauan seperti data nyata
for c in ["kota","saluran","metode_bayar","total"]:
    k[c] = k[c].astype(object)

idx = k.index.to_numpy()
def pick(n): return rng.choice(idx, n, replace=False)

# 1. format tanggal campur aduk
for i in pick(300):
    k.loc[i,"tanggal"] = pd.Timestamp(k.loc[i,"tanggal"]).strftime("%d/%m/%Y")
for i in pick(150):
    k.loc[i,"tanggal"] = pd.Timestamp(k.loc[i,"tanggal"]).strftime("%d-%b-%Y")
# 2. huruf besar-kecil & spasi berantakan
for i in pick(260): k.loc[i,"kota"] = str(k.loc[i,"kota"]).upper()
for i in pick(180): k.loc[i,"kota"] = " " + str(k.loc[i,"kota"]) + "  "
for i in pick(120): k.loc[i,"kota"] = str(k.loc[i,"kota"]).lower()
# 3. singkatan tidak konsisten
for i in pick(90):  k.loc[i,"kota"] = "JKT"
for i in pick(60):  k.loc[i,"saluran"] = "dine in"
for i in pick(60):  k.loc[i,"saluran"] = "DINE-IN"
for i in pick(45):  k.loc[i,"metode_bayar"] = "qris"
# 4. nilai kosong
for i in pick(140): k.loc[i,"total"] = np.nan
for i in pick(80):  k.loc[i,"kota"] = ""
for i in pick(50):  k.loc[i,"metode_bayar"] = "-"
# 5. total sebagai teks berformat rupiah
for i in pick(200):
    v = k.loc[i,"total"]
    if pd.notna(v): k.loc[i,"total"] = f"Rp {int(v):,}".replace(",",".")
# 6. angka negatif & nol yang mustahil
for i in pick(35): k.loc[i,"total"] = -abs(float(pd.to_numeric(k.loc[i,"total"], errors="coerce") if pd.notna(pd.to_numeric(k.loc[i,"total"], errors="coerce")) else 50000))
for i in pick(25): k.loc[i,"total"] = 0
# 7. baris duplikat penuh
dup = k.loc[pick(120)].copy()
k = pd.concat([k, dup], ignore_index=True)
# 8. baris kosong melompong
kosong = pd.DataFrame([[np.nan]*len(k.columns)]*30, columns=k.columns)
k = pd.concat([k, kosong], ignore_index=True)
k = k.sample(frac=1, random_state=11).reset_index(drop=True)
k.to_csv(f"{OUT}/transaksi_kotor.csv", index=False)
print(f"  {k.shape} | duplikat: {k.duplicated().sum()} | kosong total: {k.total.isna().sum()}")

# ---------------------------------------------------------- B. OMZET HARIAN
print("\n=== B. omzet_harian.csv (diturunkan dari transaksi) ===")
harian = (trx.groupby("tanggal")
            .agg(jumlah_transaksi=("transaksi_id","count"),
                 omzet=("total","sum"),
                 diskon=("diskon","sum"))
            .reset_index())
kal = pd.read_csv(f"{OUT}/kalender.csv", parse_dates=["tanggal"])
harian = harian.merge(kal[["tanggal","hari","akhir_pekan","hari_libur"]], on="tanggal")
harian.to_csv(f"{OUT}/omzet_harian.csv", index=False)
print(f"  {harian.shape}")
print("  rata-rata omzet per hari dalam seminggu:")
for h, v in harian.groupby("hari").omzet.mean().reindex(
        ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]).items():
    print(f"    {h:8s} Rp {v:>12,.0f}  ({v/harian.omzet.mean()*100-100:+5.1f}%)")

# ---------------------------------------------------------- C. KOHOR
print("\n=== C. keanggotaan_bulanan.csv (kohor nyata dari transaksi) ===")
m = trx[trx.pelanggan_id.notna()].merge(pel[["pelanggan_id","tanggal_daftar"]], on="pelanggan_id")
m["bulan_transaksi"] = m.tanggal.dt.to_period("M")
m["bulan_daftar"]    = m.tanggal_daftar.dt.to_period("M")
m["bulan_ke"] = (m.bulan_transaksi - m.bulan_daftar).apply(lambda x: x.n)
m = m[m.bulan_ke >= 0]
kohor = (m.groupby(["pelanggan_id","bulan_daftar","bulan_ke"])
           .agg(transaksi=("transaksi_id","count"), nilai=("total","sum"))
           .reset_index())
kohor["bulan_daftar"] = kohor.bulan_daftar.astype(str)
kohor.to_csv(f"{OUT}/keanggotaan_bulanan.csv", index=False)
uk  = kohor[kohor.bulan_ke==0].groupby("bulan_daftar").pelanggan_id.nunique()
piv = kohor.groupby(["bulan_daftar","bulan_ke"]).pelanggan_id.nunique().unstack()
ret = (piv.div(uk, axis=0)*100).round(1)
print(f"  {kohor.shape}")
print("  retensi rata-rata bulan 0-6:")
print("   ", ret.mean().head(7).round(1).to_dict())

# ---------------------------------------------------------- D. A/B TEST
print("\n=== D. abtest_checkout.csv ===")
r2 = np.random.default_rng(42); N = 4000
def grup(nm, p, mn):
    c = r2.random(N) < p
    v = np.where(c, r2.normal(mn, 25000, N).round(-2), 0).clip(0, None)
    return pd.DataFrame({"user_id":[f"A{i:05d}" for i in range(N)] if nm=="kontrol"
                                    else [f"B{i:05d}" for i in range(N)],
                         "grup":nm, "konversi":c.astype(int), "nilai_pesanan":v})
ab = pd.concat([grup("kontrol",0.110,85000), grup("perlakuan",0.132,80000)], ignore_index=True)
ab.to_csv(f"{OUT}/abtest_checkout.csv", index=False)
print("  ", ab.groupby("grup").konversi.agg(['count','sum','mean']).round(5).to_dict('index'))

# ---------------------------------------------------------- E. CHURN
print("\n=== E. churn_features.csv ===")
r3 = np.random.default_rng(21); M = 5000
trx30 = r3.poisson(3.2, M); recency = r3.integers(1,60,M)
nilai = r3.normal(78000,25000,M).clip(15000); promo = r3.random(M)<0.38
kanal = r3.choice(["organik","iklan","referral"],M,p=[.45,.40,.15]); ragam = r3.integers(1,6,M)
logit = (-0.55 -0.42*trx30 +0.055*recency -0.30*ragam
         +0.55*(kanal=="iklan") -0.45*(kanal=="referral")
         +0.25*promo -0.0000035*(nilai-78000))
churn = (r3.random(M) < 1/(1+np.exp(-logit))).astype(int)
ch = pd.DataFrame({"pelanggan_id":[f"C{i:05d}" for i in range(M)],
    "trx_30d":trx30,"hari_sejak_transaksi_terakhir":recency,
    "nilai_rata2":nilai.round(-2),"pakai_promo":promo.astype(int),
    "kanal":kanal,"jumlah_produk_beda":ragam,"churn":churn})
ch.to_csv(f"{OUT}/churn_features.csv", index=False)
print(f"  {ch.shape} | churn rate {ch.churn.mean()*100:.1f}%")
print("  churn per kanal:", ch.groupby('kanal').churn.mean().round(3).to_dict())
