import numpy as np, pandas as pd
OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/data"
rng = np.random.default_rng(777)

produk    = pd.read_csv(f"{OUT}/produk.csv")
cabang    = pd.read_csv(f"{OUT}/cabang.csv")
kalender  = pd.read_csv(f"{OUT}/kalender.csv", parse_dates=["tanggal"])
pelanggan = pd.read_csv(f"{OUT}/pelanggan.csv", parse_dates=["tanggal_daftar"])

cabang["tanggal_buka"]  = pd.to_datetime(cabang.tanggal_buka)
produk["tanggal_rilis"] = pd.to_datetime(produk.tanggal_rilis)

efek_hari  = {"Senin":.86,"Selasa":.84,"Rabu":.92,"Kamis":1.00,
              "Jumat":1.12,"Sabtu":1.24,"Minggu":1.14}
pel_sorted = pelanggan.sort_values("tanggal_daftar")
pel_by_kota = {k: (g.pelanggan_id.values, g.tanggal_daftar.values)
               for k, g in pel_sorted.groupby("kota")}
daftar_map  = dict(zip(pelanggan.pelanggan_id, pelanggan.tanggal_daftar))
prem_map    = dict(zip(pelanggan.pelanggan_id, pelanggan.member_premium))

trx_rows, item_rows = [], []
tid = 0
for _, hari in kalender.iterrows():
    t = hari.tanggal
    buka = cabang[cabang.tanggal_buka <= t]
    if buka.empty: continue
    tersedia = produk[produk.tanggal_rilis <= t]
    # pertumbuhan bisnis dari waktu ke waktu
    umur = (t - pd.Timestamp("2024-01-01")).days
    tren = 1 + 0.0011 * umur
    for _, cab in buka.iterrows():
        dasar = cab.kapasitas_kursi * 0.62
        n = rng.poisson(max(dasar * tren * efek_hari[hari.hari]
                            * (1.28 if hari.hari_libur else 1.0)
                            * rng.normal(1, 0.09), 3))
        ids, tgls = pel_by_kota.get(cab.kota, (np.array([]), np.array([])))
        n_eligible = int(np.searchsorted(tgls, np.datetime64(t), side="right")) if len(ids) else 0
        for _ in range(int(n)):
            tid += 1
            trx_id = f"T{tid:07d}"
            # 46% transaksi dikaitkan ke member yang sudah mendaftar
            pid = None
            if n_eligible > 0 and rng.random() < 0.46:
                pid = ids[rng.integers(0, n_eligible)]
            saluran = rng.choice(["Dine-in","Takeaway","Delivery"],
                                 p=[.44,.34,.22] if t >= pd.Timestamp("2025-01-01") else [.55,.40,.05])
            bayar = rng.choice(["QRIS","Kartu Debit","Tunai","E-Wallet"], p=[.38,.19,.21,.22])
            jam = int(np.clip(rng.normal(13.5, 3.4), 7, 21))
            n_item = rng.choice([1,2,3,4], p=[.44,.34,.16,.06])
            bobot = np.where(tersedia.kategori.str.startswith("Minuman"), 3.0, 1.0)
            bobot = bobot / bobot.sum()
            pilihan = rng.choice(tersedia.produk_id.values, size=n_item, replace=False, p=bobot)
            subtotal = 0
            for pr in pilihan:
                row = tersedia[tersedia.produk_id == pr].iloc[0]
                qty = int(rng.choice([1,2,3], p=[.76,.19,.05]))
                nilai = int(row.harga * qty)
                subtotal += nilai
                item_rows.append((trx_id, pr, qty, int(row.harga), nilai))
            diskon = 0
            if pid is not None and prem_map[pid] and rng.random() < 0.42:
                diskon = int(subtotal * 0.10)
            elif rng.random() < 0.08:
                diskon = int(subtotal * 0.05)
            trx_rows.append((trx_id, t.date(), jam, cab.cabang_id, pid, saluran,
                             bayar, subtotal, diskon, subtotal - diskon))

trx = pd.DataFrame(trx_rows, columns=[
    "transaksi_id","tanggal","jam","cabang_id","pelanggan_id","saluran",
    "metode_bayar","subtotal","diskon","total"])
item = pd.DataFrame(item_rows, columns=[
    "transaksi_id","produk_id","jumlah","harga_satuan","nilai"])

trx.to_csv(f"{OUT}/transaksi.csv", index=False)
item.to_csv(f"{OUT}/transaksi_item.csv", index=False)

print("transaksi     :", trx.shape)
print("transaksi_item:", item.shape)
print("rentang       :", trx.tanggal.min(), "s/d", trx.tanggal.max())
print("total omzet   : Rp {:,}".format(trx.total.sum()))
print("\nomzet per tahun:")
print(pd.to_datetime(trx.tanggal).dt.year.groupby(pd.to_datetime(trx.tanggal).dt.year).size().to_string())
print("\ntransaksi per cabang:"); print(trx.cabang_id.value_counts().sort_index().to_string())
print("\n% transaksi tanpa pelanggan_id: {:.1f}%".format(trx.pelanggan_id.isna().mean()*100))
print("ukuran file (MB): trx {:.1f}, item {:.1f}".format(
    trx.memory_usage(deep=True).sum()/1e6, item.memory_usage(deep=True).sum()/1e6))
