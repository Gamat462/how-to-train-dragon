"""
Memberi siklus hidup nyata pada pelanggan, lalu menugaskan ulang pelanggan_id
ke transaksi. Tanpa ini, analisis retensi tidak mungkin dilakukan.
"""
import numpy as np, pandas as pd
from collections import defaultdict
OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/data"
rng = np.random.default_rng(313)

trx = pd.read_csv(f"{OUT}/transaksi.csv", parse_dates=["tanggal"])
pel = pd.read_csv(f"{OUT}/pelanggan.csv", parse_dates=["tanggal_daftar"])
cab = pd.read_csv(f"{OUT}/cabang.csv")
kota_cabang = dict(zip(cab.cabang_id, cab.kota))

# ---- 1. tetapkan tipe pelanggan & bulan-bulan aktifnya ----
AKHIR = pd.Period("2026-06", freq="M")
aktif_di = defaultdict(list)          # (kota, Period) -> [pelanggan_id]
tipe_map = {}

for pid, tgl_daftar, kota, kanal in zip(
        pel.pelanggan_id, pel.tanggal_daftar, pel.kota, pel.kanal_akuisisi):
    # kanal referral menghasilkan pelanggan yang lebih setia — pola nyata
    p_setia = {"referral":0.34,"organik":0.26,"gojek_grab":0.18,
               "iklan_meta":0.15,"iklan_google":0.15}[kanal]
    setia = rng.random() < p_setia
    tipe_map[pid] = "setia" if setia else "biasa"
    p_bertahan = 0.88 if setia else 0.45
    p_aktivasi = 0.82 if setia else 0.68      # tidak semua langsung belanja

    m = pd.Period(tgl_daftar, freq="M")
    if rng.random() > p_aktivasi:             # tidak pernah aktif sama sekali
        continue
    while m <= AKHIR:
        aktif_di[(kota, m)].append(pid)
        if rng.random() > p_bertahan:
            break
        m += 1

pel["tipe_pelanggan"] = pel.pelanggan_id.map(tipe_map)
pel.to_csv(f"{OUT}/pelanggan.csv", index=False)

# ---- 2. tugaskan ulang pelanggan_id ke transaksi ----
trx["kota"] = trx.cabang_id.map(kota_cabang)
trx["periode"] = trx.tanggal.dt.to_period("M")
butuh = trx.pelanggan_id.notna().values      # pertahankan pola mana yang member
baru = np.full(len(trx), None, dtype=object)

for (kota, per), idx in trx.groupby(["kota","periode"]).groups.items():
    kandidat = aktif_di.get((kota, per), [])
    if not kandidat:
        continue
    idx = np.asarray(idx)
    idx = idx[butuh[idx]]
    if len(idx) == 0:
        continue
    baru[idx] = rng.choice(kandidat, size=len(idx), replace=True)

trx["pelanggan_id"] = baru
trx = trx.drop(columns=["kota","periode"])
trx.to_csv(f"{OUT}/transaksi.csv", index=False)

era = trx[trx.tanggal >= "2025-01-01"]
print(f"transaksi 2025+ dengan member: {era.pelanggan_id.notna().mean()*100:.1f}%")
print(f"pelanggan unik yang pernah transaksi: {trx.pelanggan_id.nunique():,} dari {len(pel):,}")

# ---- 3. bangun ulang tabel kohor & verifikasi ----
m = trx[trx.pelanggan_id.notna()].merge(
        pel[["pelanggan_id","tanggal_daftar"]], on="pelanggan_id")
m["bulan_daftar"] = m.tanggal_daftar.dt.to_period("M")
m["bulan_ke"] = (m.tanggal.dt.to_period("M") - m.bulan_daftar).apply(lambda x: x.n)
m = m[m.bulan_ke >= 0]

kohor = (m.groupby(["pelanggan_id","bulan_daftar","bulan_ke"])
           .agg(transaksi=("transaksi_id","count"), nilai=("total","sum"))
           .reset_index())
kohor["bulan_daftar"] = kohor.bulan_daftar.astype(str)
kohor.to_csv(f"{OUT}/keanggotaan_bulanan.csv", index=False)

# penyebut yang BENAR: jumlah pendaftar per bulan dari tabel pelanggan
ukuran = pel.groupby(pel.tanggal_daftar.dt.to_period("M").astype(str)).pelanggan_id.nunique()
piv = kohor.groupby(["bulan_daftar","bulan_ke"]).pelanggan_id.nunique().unstack()
ret = (piv.div(ukuran, axis=0)*100).round(1)

print(f"\nkeanggotaan_bulanan: {kohor.shape}")
print("\nMATRIKS RETENSI (% dari pendaftar bulan itu):")
print(ret.iloc[:8, :9].to_string())
print("\nrata-rata retensi bulan 0-8:")
print(ret.mean().head(9).round(1).to_string())
