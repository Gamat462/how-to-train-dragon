import numpy as np, pandas as pd
OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/migas/data"
rng = np.random.default_rng(3131)

prod = pd.read_csv(f"{OUT}/produksi_harian.csv", parse_dates=["tanggal"])
sumur = pd.read_csv(f"{OUT}/sumur.csv")
prod = prod.merge(sumur[["sumur_id","lapangan_id"]], on="sumur_id")
prod["periode"] = prod.tanggal.dt.to_period("M")
bulan = sorted(prod.periode.unique())

# ------------------------------------------------- 1. HARGA ICP (USD/bbl)
harga = []
p = 78.0
for m in bulan:
    p = float(np.clip(p + rng.normal(0.4, 4.6), 52, 118))
    icp = round(p, 2)
    harga.append((str(m), icp, round(icp*rng.uniform(0.965,0.995),2),
                  round(float(np.clip(icp*0.118 + rng.normal(0,0.35), 5.5, 14)),2)))
icp = pd.DataFrame(harga, columns=["periode","icp_usd_bbl","realisasi_usd_bbl","harga_gas_usd_mmbtu"])
icp.to_csv(f"{OUT}/harga_icp.csv", index=False)

# ------------------------------------------------- 2. BIAYA OPERASI
kategori = [("Well Services","OPEX"),("Facility O&M","OPEX"),("Chemicals","OPEX"),
            ("Power & Fuel","OPEX"),("Transportation","OPEX"),("Manpower","OPEX"),
            ("HSE & Environment","OPEX"),("G&A Allocation","OPEX"),
            ("Drilling","CAPEX"),("Facility Upgrade","CAPEX"),("Workover","OPEX")]
biaya_rows = []
prod_bln = prod.groupby(["periode","lapangan_id"]).oil_bopd.sum().reset_index()
for r in prod_bln.itertuples():
    skala = r.oil_bopd / 1000.0
    for kat, jenis in kategori:
        # dikalibrasi supaya lifting cost mendekati $13-15/bbl, kisaran nyata Indonesia
        dasar = {"Well Services":1.55,"Facility O&M":1.85,"Chemicals":1.00,
                 "Power & Fuel":2.55,"Transportation":1.25,"Manpower":2.80,
                 "HSE & Environment":0.70,"G&A Allocation":1.40,
                 "Drilling":0.0,"Facility Upgrade":0.0,"Workover":0.82}[kat]
        nilai = dasar*skala*rng.uniform(0.8,1.25)*1000
        if jenis == "CAPEX":
            nilai = rng.choice([0,0,0,1], p=[.62,.16,.10,.12]) * rng.uniform(300_000, 4_800_000)
        if nilai <= 0: continue
        biaya_rows.append((str(r.periode), r.lapangan_id, kat, jenis, round(float(nilai),2)))
biaya = pd.DataFrame(biaya_rows, columns=["periode","lapangan_id","kategori_biaya","jenis","nilai_usd"])
biaya.to_csv(f"{OUT}/biaya_operasi.csv", index=False)

# ------------------------------------------------- 3. LIFTING (kargo)
lift_rows, lid = [], 0
for m in bulan:
    vol_bulan = prod[prod.periode==m].oil_bopd.sum()
    sisa = vol_bulan * rng.uniform(0.93, 1.03)      # lifting != produksi (ada stok)
    n = int(rng.integers(2,5))
    for i in range(n):
        lid += 1
        v = sisa/n * rng.uniform(0.82,1.18)
        tgl = pd.Period(m).to_timestamp() + pd.Timedelta(days=int(rng.integers(2,27)))
        h = float(icp[icp.periode==str(m)].realisasi_usd_bbl.iloc[0])
        lift_rows.append((f"LFT-{lid:04d}", tgl.date(), str(m),
                          rng.choice(["Pertamina","Trafigura","Vitol","PetroChina","ExxonMobil"],
                                     p=[.42,.16,.14,.16,.12]),
                          round(float(v),1), h, round(float(v*h),2),
                          rng.choice(["Domestik","Ekspor"], p=[.68,.32])))
lifting = pd.DataFrame(lift_rows, columns=[
    "lifting_id","tanggal","periode","pembeli","volume_bbl","harga_usd_bbl","nilai_usd","tujuan"])
lifting.to_csv(f"{OUT}/lifting.csv", index=False)

# ------------------------------------------------- 4. PSC COST RECOVERY
# Skema PSC cost recovery Indonesia (disederhanakan tapi strukturnya benar)
FTP_RATE, FTP_SHARE_GOV = 0.20, 0.60      # FTP 20%, dibagi 60:40
SPLIT_GOV_OIL = 0.85                       # bagi hasil sebelum pajak
DMO_RATE, DMO_PRICE_FRAC = 0.25, 0.25      # 25% jatah kontraktor, harga 25% ICP
TAX_RATE = 0.44
CAP_RECOVERY = 0.80                        # batas cost recovery thd gross revenue

psc_rows = []
unrecovered = 0.0
for m in bulan:
    mm = str(m)
    vol = float(prod[prod.periode==m].oil_bopd.sum())
    h   = float(icp[icp.periode==mm].icp_usd_bbl.iloc[0])
    gross = vol * h
    b = biaya[biaya.periode==mm]
    opex   = float(b[b.jenis=="OPEX"].nilai_usd.sum())
    capex  = float(b[b.jenis=="CAPEX"].nilai_usd.sum())
    depre  = capex/60.0                      # disusutkan 5 tahun garis lurus (disederhanakan)
    biaya_recoverable = opex + depre + unrecovered

    ftp = gross * FTP_RATE
    ftp_gov, ftp_con = ftp*FTP_SHARE_GOV, ftp*(1-FTP_SHARE_GOV)

    tersedia = max(gross - ftp, 0)
    cap = gross * CAP_RECOVERY
    cost_recovery = min(biaya_recoverable, tersedia, cap)
    unrecovered = max(biaya_recoverable - cost_recovery, 0)

    ets = max(tersedia - cost_recovery, 0)
    ets_gov, ets_con = ets*SPLIT_GOV_OIL, ets*(1-SPLIT_GOV_OIL)

    con_vol_share = (ets_con + ftp_con) / h if h else 0
    dmo_vol = con_vol_share * DMO_RATE
    dmo_loss = dmo_vol * h * (1 - DMO_PRICE_FRAC)

    con_before_tax = ftp_con + ets_con + cost_recovery - dmo_loss
    taxable = ftp_con + ets_con - dmo_loss
    tax = max(taxable, 0) * TAX_RATE
    con_after_tax = con_before_tax - tax
    gov_take = ftp_gov + ets_gov + tax + dmo_loss

    psc_rows.append((mm, round(vol,1), h, round(gross,2), round(opex,2), round(capex,2),
                     round(depre,2), round(biaya_recoverable,2), round(cost_recovery,2),
                     round(unrecovered,2), round(ftp_gov,2), round(ftp_con,2),
                     round(ets_gov,2), round(ets_con,2), round(dmo_vol,1), round(dmo_loss,2),
                     round(tax,2), round(con_after_tax,2), round(gov_take,2)))

psc = pd.DataFrame(psc_rows, columns=[
    "periode","volume_bbl","icp_usd_bbl","gross_revenue_usd","opex_usd","capex_usd",
    "depresiasi_usd","biaya_recoverable_usd","cost_recovery_usd","unrecovered_carry_usd",
    "ftp_pemerintah_usd","ftp_kontraktor_usd","ets_pemerintah_usd","ets_kontraktor_usd",
    "dmo_volume_bbl","dmo_loss_usd","pajak_usd","kontraktor_net_usd","government_take_usd"])
psc.to_csv(f"{OUT}/psc_bulanan.csv", index=False)

# ------------------------------------------------- 5. HSE
hse_rows = []
for m in bulan:
    for _ in range(rng.poisson(1.9)):
        jenis = rng.choice(["Near Miss","First Aid","Medical Treatment",
                            "Lost Time Injury","Spill","Fire"],
                           p=[.42,.22,.14,.07,.11,.04])
        hse_rows.append((str(m),
            (pd.Period(m).to_timestamp()+pd.Timedelta(days=int(rng.integers(0,27)))).date(),
            rng.choice(["F01","F02","F03","F04"]), jenis,
            rng.choice(["Ringan","Sedang","Berat"], p=[.66,.27,.07]),
            rng.choice(["Kontraktor","Karyawan"], p=[.71,.29]),
            int(rng.integers(0,26)) if jenis=="Lost Time Injury" else 0))
hse = pd.DataFrame(hse_rows, columns=[
    "periode","tanggal","lapangan_id","jenis_insiden","tingkat_keparahan",
    "status_pekerja","hari_kerja_hilang"])
hse.to_csv(f"{OUT}/hse_insiden.csv", index=False)

print("harga_icp     :", icp.shape, f"| rentang ICP ${icp.icp_usd_bbl.min():.2f}–${icp.icp_usd_bbl.max():.2f}")
print("biaya_operasi :", biaya.shape, f"| total ${biaya.nilai_usd.sum():,.0f}")
print("lifting       :", lifting.shape, f"| total ${lifting.nilai_usd.sum():,.0f}")
print("psc_bulanan   :", psc.shape)
print("hse_insiden   :", hse.shape)
print(f"\nlifting cost/bbl rata-rata: ${biaya[biaya.jenis=='OPEX'].nilai_usd.sum()/prod.oil_bopd.sum():.2f}")
print(f"government take rata-rata : {psc.government_take_usd.sum()/psc.gross_revenue_usd.sum()*100:.1f}%")
print(f"cost recovery tertahan    : ${psc.unrecovered_carry_usd.iloc[-1]:,.0f}")
print("\ncontoh 3 baris PSC:")
print(psc[["periode","gross_revenue_usd","cost_recovery_usd","government_take_usd","kontraktor_net_usd"]].head(3).to_string(index=False))
