import pandas as pd
pd.set_option("display.width", 220)

k = pd.read_excel("Kunjungan Pasien 2024.xlsx")
t = pd.read_csv("Tagihan Klinik 2024.csv", sep=";", decimal=",")

# --- samakan tipe kunci SEBELUM menggabung ---
for df in (k, t):
    df["ID Pasien"] = df["ID Pasien"].astype(int)

print("=== 1. TAGIHAN GANDA ===")
ganda = t[t.duplicated("Kode Kunjungan", keep=False)].sort_values("Kode Kunjungan")
print("baris tagihan terlibat:", len(ganda), "| kunjungan terdampak:", ganda["Kode Kunjungan"].nunique())
print(ganda.head(4)[["No Invoice","Kode Kunjungan","Tanggal","Total"]].to_string(index=False))
nilai_ganda = t[t.duplicated("Kode Kunjungan", keep="first")]["Total"].sum()
print("nilai yang tercatat dua kali:", f"{nilai_ganda:,.0f}".replace(",","."))

t_bersih = t.drop_duplicates("Kode Kunjungan", keep="first")
print("tagihan sesudah dedup:", len(t_bersih))

print("\n=== 2. KUNJUNGAN TANPA TAGIHAN ===")
g = k.merge(t_bersih, on="Kode Kunjungan", how="left", indicator=True, suffixes=("","_tag"))
belum = g[g["_merge"] == "left_only"]
print("kunjungan belum ditagih:", len(belum))
print(belum.groupby("Layanan").size().to_string())

print("\n=== 3. NAMA PASIEN GANDA ===")
print("nama unik mentah :", k["Nama Pasien"].nunique())
print("ID pasien unik   :", k["ID Pasien"].nunique())
per_id = k.groupby("ID Pasien")["Nama Pasien"].nunique()
print("ID dengan >1 ejaan nama:", int((per_id > 1).sum()))
for pid in per_id[per_id > 1].index:
    print(f"  ID {pid}: {sorted(k.loc[k['ID Pasien']==pid,'Nama Pasien'].unique())}")

print("\n=== 4. PENJAMIN ===")
print("nilai mentah:", sorted(k["Penjamin"].unique()))
def rapikan_penjamin(s):
    x = str(s).upper().replace(".", "").replace(" ", "")
    if x.startswith("BPJS"): return "BPJS"
    if x.startswith("UMUM"): return "Umum"
    if x.startswith("ASURANSI"): return "Asuransi"
    return "Lainnya"
g["penjamin"] = g["Penjamin"].map(rapikan_penjamin)
print("sesudah dirapikan:", sorted(g["penjamin"].unique()))

print("\n=== HASIL: pendapatan per penjamin (hanya yang sudah ditagih) ===")
h = g[g["_merge"] == "both"]
print(h.groupby("penjamin").agg(kunjungan=("Total","size"),
                                pendapatan=("Total","sum")).to_string())
print("\ntotal pendapatan bersih:", f'{h["Total"].sum():,.0f}'.replace(",","."))
print("total tagihan mentah   :", f'{t["Total"].sum():,.0f}'.replace(",","."))
print("selisih (tagihan ganda):", f'{t["Total"].sum() - h["Total"].sum():,.0f}'.replace(",","."))

print("\n=== HASIL: potensi pendapatan yang belum ditagih ===")
tarif = {"Pemeriksaan Umum":50000,"Pemeriksaan Gigi":150000,"Cek Laboratorium":275000,
         "Suntik Imunisasi":120000,"Kontrol Kehamilan":180000,"Perawatan Luka":85000}
print("nilai kunjungan tanpa tagihan:",
      f'{belum["Layanan"].map(tarif).sum():,.0f}'.replace(",","."))
