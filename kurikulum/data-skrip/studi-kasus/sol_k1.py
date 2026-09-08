import pandas as pd, re
pd.set_option("display.width", 200)
BERKAS = "Laporan Penjualan Toko Sumber Rejeki.xlsx"

def ke_angka(s):
    if pd.isna(s): return pd.NA
    t = re.sub(r"[^0-9\-]", "", str(s))
    return int(t) if t not in ("", "-") else pd.NA

raw = pd.read_excel(BERKAS, skiprows=5, dtype=str)
raw = raw.drop(columns=[c for c in raw.columns if str(c).startswith("Unnamed")])

# 1. angka kontrol dari baris subtotal, DIAMBIL SEBELUM dibuang
sub = raw[raw["Nama Barang"].astype(str).str.startswith("TOTAL BULAN", na=False)]
KONTROL = int(sub["Jumlah"].map(ke_angka).sum())

# 2. baris transaksi = baris yang kolom No-nya benar-benar angka
d = raw[raw["No"].fillna("").str.fullmatch(r"\d+")].copy()

# 3. angka
for asal, baru in [("Qty","qty"), ("Harga Satuan","harga"), ("Jumlah","jumlah")]:
    d[baru] = d[asal].map(ke_angka).astype("Int64")

# 4. tanggal tiga format sekaligus
d["tanggal"] = pd.to_datetime(d["Tanggal"], format="mixed", dayfirst=True, errors="coerce")

# 5. nama pelanggan — perhatikan urutannya
d["pelanggan"] = (d["Pelanggan"]
    .str.strip().str.replace(r"\s+", " ", regex=True)      # sebelum astype(str)!
    .str.title()
    .str.replace(r"^(Cv|Pt|Ud|Cv\.|Pt\.)\s+", lambda m: m.group(1).upper().rstrip(".") + " ", regex=True)
    .replace({"-": pd.NA})
    .fillna("Tanpa Nama"))

# 6. kode barang
d["kode"] = d["Kode Barang"].str.upper().str.replace(r"[\s\-]", "", regex=True)
d["retur"] = d["qty"] < 0

print("=== PEMERIKSAAN ===")
print("baris transaksi     :", len(d))
print("tanggal gagal dibaca:", int(d["tanggal"].isna().sum()))
print("nilai kosong        :", int(d[["qty","harga","jumlah"]].isna().sum().sum()))
hasil = int(d["jumlah"].sum())
print("total bersih        :", f"{hasil:,}".replace(",","."))
print("angka kontrol       :", f"{KONTROL:,}".replace(",","."))
print("selisih             :", hasil - KONTROL)
print("cek harga x qty     :", int((d["qty"]*d["harga"] != d["jumlah"]).sum()), "baris tidak konsisten")

print("\n=== HASIL 1: omzet per bulan ===")
d["bulan"] = d["tanggal"].dt.strftime("%Y-%m")
print(d.groupby("bulan").agg(transaksi=("jumlah","size"), omzet=("jumlah","sum")).to_string())

print("\n=== HASIL 2: lima barang teratas ===")
print(d.groupby("kode").agg(unit=("qty","sum"), omzet=("jumlah","sum"))
        .sort_values("omzet", ascending=False).head(5).to_string())

print("\n=== HASIL 3: pelanggan teratas ===")
print(d.groupby("pelanggan").agg(nota=("jumlah","size"), omzet=("jumlah","sum"))
        .sort_values("omzet", ascending=False).head(6).to_string())

print("\n=== HASIL 4: retur ===")
r = d[d["retur"]]
print("jumlah retur:", len(r), "| nilai:", f'{int(r["jumlah"].sum()):,}'.replace(",","."),
      "| persen dari omzet kotor:",
      round(abs(r["jumlah"].sum()) / d.loc[~d["retur"],"jumlah"].sum() * 100, 2), "%")

print("\n=== dampak pembersihan ===")
print("pelanggan unik sebelum:", d["Pelanggan"].nunique(), "-> sesudah:", d["pelanggan"].nunique())
print("kode barang   sebelum:", d["Kode Barang"].nunique(), "-> sesudah:", d["kode"].nunique())
