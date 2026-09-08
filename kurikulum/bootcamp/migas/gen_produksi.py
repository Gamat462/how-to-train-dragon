import numpy as np, pandas as pd
OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/migas/data"
rng = np.random.default_rng(2211)

sumur = pd.read_csv(f"{OUT}/sumur.csv", parse_dates=["tanggal_onstream"])
MULAI, AKHIR = pd.Timestamp("2023-01-01"), pd.Timestamp("2026-06-30")
tgl = pd.date_range(MULAI, AKHIR, freq="D")

prod_rows, down_rows, wo_rows = [], [], []
wo_id = 0

for s in sumur.itertuples():
    if s.tipe_sumur == "Injector":
        continue
    hari_aktif = tgl[tgl >= s.tanggal_onstream]
    if len(hari_aktif) == 0:
        continue
    t_thn = (hari_aktif - s.tanggal_onstream).days.values / 365.25

    # --- kurva Arps hiperbolik ---
    b, D = s.arps_b, s.decline_D_tahunan
    q = s.qi_oil_bopd / np.power(1 + b*D*t_thn, 1/b) if b > 0.01 \
        else s.qi_oil_bopd * np.exp(-D*t_thn)

    # --- workover: menaikkan produksi sementara ---
    uplift = np.ones(len(hari_aktif))
    n_wo = rng.poisson(1.4)
    for _ in range(n_wo):
        if len(hari_aktif) < 120: break
        mulai = int(rng.integers(60, len(hari_aktif)-30))
        wo_id += 1
        jenis = rng.choice(["Acidizing","Reperforation","ESP Replacement",
                            "Scale Removal","Zone Change"], p=[.24,.18,.28,.20,.10])
        gain  = float(rng.uniform(1.12, 1.55))
        biaya = int(rng.uniform(180_000, 1_450_000))
        durasi_hari = int(rng.integers(3, 15))
        wo_rows.append((f"WO-{wo_id:04d}", s.sumur_id,
                        hari_aktif[mulai].date(), jenis, durasi_hari, biaya,
                        round(gain,3)))
        # tutup sumur selama pengerjaan, lalu naik dengan peluruhan kembali
        uplift[mulai:mulai+durasi_hari] = 0.0
        sisa = len(hari_aktif) - (mulai+durasi_hari)
        if sisa > 0:
            luruh = np.exp(-np.arange(sisa)/rng.uniform(150, 400))
            uplift[mulai+durasi_hari:] *= (1 + (gain-1)*luruh)

    # --- downtime tak terencana ---
    down = np.ones(len(hari_aktif))
    n_dt = rng.poisson(len(hari_aktif)/210)
    for _ in range(n_dt):
        d0 = int(rng.integers(0, len(hari_aktif)))
        dur = int(rng.choice([1,1,2,2,3,4,6,9], p=[.30,.22,.16,.10,.08,.06,.05,.03]))
        sebab = rng.choice(["Pump Failure","Power Outage","Flowline Leak",
                            "Facility Shutdown","Weather","Sand Production"],
                           p=[.31,.19,.14,.16,.11,.09])
        down[d0:d0+dur] = 0.0
        down_rows.append((s.sumur_id, hari_aktif[min(d0,len(hari_aktif)-1)].date(),
                          dur, sebab,
                          "Terencana" if sebab=="Facility Shutdown" else "Tidak Terencana"))

    wc = np.clip(s.watercut_awal + s.kenaikan_watercut_harian*np.arange(len(hari_aktif)),
                 0, 0.96)
    derau = rng.normal(1, 0.055, len(hari_aktif))
    oil = np.clip(q * uplift * down * derau, 0, None)
    gas = oil * s.gor_scf_bbl / 1000.0 * rng.normal(1, 0.04, len(oil))   # mscf
    air = np.where(oil > 0, oil * wc/(1-wc), 0) * rng.normal(1, 0.06, len(oil))

    for i, d in enumerate(hari_aktif):
        prod_rows.append((s.sumur_id, d.date(), round(float(oil[i]),2),
                          round(float(max(gas[i],0)),2), round(float(max(air[i],0)),2),
                          round(float(wc[i]),4), int(down[i]*uplift[i] > 0)))

prod = pd.DataFrame(prod_rows, columns=[
    "sumur_id","tanggal","oil_bopd","gas_mscfd","water_bwpd","watercut","berproduksi"])
downtime = pd.DataFrame(down_rows, columns=[
    "sumur_id","tanggal_mulai","durasi_hari","penyebab","kategori"])
workover = pd.DataFrame(wo_rows, columns=[
    "workover_id","sumur_id","tanggal_mulai","jenis_pekerjaan","durasi_hari",
    "biaya_usd","faktor_kenaikan"])

prod.to_csv(f"{OUT}/produksi_harian.csv", index=False)
downtime.to_csv(f"{OUT}/downtime.csv", index=False)
workover.to_csv(f"{OUT}/workover.csv", index=False)

print("produksi_harian:", prod.shape)
print("downtime       :", downtime.shape)
print("workover       :", workover.shape)
print(f"\ntotal oil  : {prod.oil_bopd.sum():,.0f} bbl")
print(f"total gas  : {prod.gas_mscfd.sum():,.0f} mscf")
print(f"uptime     : {prod.berproduksi.mean()*100:.1f}%")
p = prod.copy(); p["tanggal"]=pd.to_datetime(p.tanggal)
print("\nproduksi minyak per tahun (bbl):")
print(p.groupby(p.tanggal.dt.year).oil_bopd.sum().round(0).to_string())
print("\nrata-rata watercut per tahun:")
print(p.groupby(p.tanggal.dt.year).watercut.mean().round(3).to_string())
