"""
Dataset Migas — Blok Cendana (fiktif, PSC Indonesia)
Kurva decline memakai persamaan Arps yang sesungguhnya, bukan angka acak.
"""
import numpy as np, pandas as pd, os
OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/migas/data"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(1911)

MULAI, AKHIR = pd.Timestamp("2023-01-01"), pd.Timestamp("2026-06-30")
tgl_range = pd.date_range(MULAI, AKHIR, freq="D")

# ---------------------------------------------------------------- LAPANGAN
lapangan = pd.DataFrame([
    ("F01","Cendana Utara","Onshore","Jawa Barat",1998,"Sandstone"),
    ("F02","Cendana Selatan","Onshore","Jawa Barat",2005,"Sandstone"),
    ("F03","Meranti","Offshore Shallow","Laut Jawa",2012,"Carbonate"),
    ("F04","Gaharu","Offshore Shallow","Laut Jawa",2019,"Carbonate"),
], columns=["lapangan_id","nama_lapangan","tipe","wilayah","tahun_onstream","reservoir"])
lapangan.to_csv(f"{OUT}/lapangan.csv", index=False)

# ---------------------------------------------------------------- SUMUR
sumur_rows = []
konf = {  # lapangan: (jumlah sumur, qi_oil rentang, D tahunan, b, GOR, watercut awal)
 "F01": (22, (120, 480), 0.28, 0.45, (450, 900),  (0.18,0.55)),
 "F02": (18, (90, 380),  0.24, 0.55, (380, 750),  (0.10,0.40)),
 "F03": (14, (400,1500), 0.34, 0.70, (900,2200),  (0.02,0.15)),
 "F04": (10, (600,2100), 0.42, 0.85, (1400,3500), (0.01,0.08)),
}
wid = 0
for lap,(n, qi_r, D, b, gor_r, wc_r) in konf.items():
    for i in range(n):
        wid += 1
        tipe = rng.choice(["Producer","Producer","Producer","Injector"], p=[.34,.33,.25,.08])
        # sumur mulai berproduksi tersebar sepanjang waktu
        onstream = MULAI - pd.Timedelta(days=int(rng.integers(0, 2600)))
        if rng.random() < 0.18:   # sebagian sumur baru dibor dalam periode data
            onstream = MULAI + pd.Timedelta(days=int(rng.integers(30, 900)))
        sumur_rows.append((
            f"CDN-{wid:03d}", lap, tipe,
            onstream.date(),
            round(float(rng.uniform(*qi_r)),1),                 # qi_oil bopd
            round(float(D * rng.uniform(0.75,1.3)),4),          # D per tahun
            round(float(b * rng.uniform(0.8,1.2)),3),           # b Arps
            int(rng.uniform(*gor_r)),                            # GOR scf/bbl
            round(float(rng.uniform(*wc_r)),3),                  # watercut awal
            round(float(rng.uniform(0.00018, 0.00075)),6),       # kenaikan watercut/hari
            int(rng.uniform(1100, 3200)),                        # kedalaman m
            rng.choice(["ESP","Gas Lift","Natural Flow","Sucker Rod"], p=[.44,.26,.14,.16]),
        ))
sumur = pd.DataFrame(sumur_rows, columns=[
    "sumur_id","lapangan_id","tipe_sumur","tanggal_onstream","qi_oil_bopd",
    "decline_D_tahunan","arps_b","gor_scf_bbl","watercut_awal",
    "kenaikan_watercut_harian","kedalaman_m","metode_angkat"])
sumur.to_csv(f"{OUT}/sumur.csv", index=False)
print("lapangan", lapangan.shape, "| sumur", sumur.shape)
print(sumur.groupby(["lapangan_id","tipe_sumur"]).size().to_string())
