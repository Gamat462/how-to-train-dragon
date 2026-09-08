import pandas as pd, re
pd.set_option("display.width", 220)
BERKAS = "RAB vs Realisasi CV Karya Mandiri.xlsx"

print("=== sheet apa saja yang ada ===")
print(pd.ExcelFile(BERKAS).sheet_names)

rab  = pd.read_excel(BERKAS, sheet_name="RAB", skiprows=2)
real = pd.read_excel(BERKAS, sheet_name="Realisasi")
print("\nRAB:", rab.shape, "| Realisasi:", real.shape)

print("\n=== kolom Biaya: campur teks dan angka ===")
print(real["Biaya"].head(6).to_string())
print("tipe kolom Biaya:", real["Biaya"].dtype)
teks  = real["Biaya"].map(lambda x: isinstance(x, str)).sum()
print(f"baris berupa TEKS: {teks} | berupa ANGKA: {len(real)-teks}")
print("kalau langsung .sum():", real["Biaya"].sum() if real["Biaya"].dtype != object else "GAGAL / hasil aneh")

def ke_angka(x):
    if pd.isna(x): return 0
    if isinstance(x, (int, float)): return int(x)
    t = re.sub(r"[^0-9\-]", "", str(x))
    return int(t) if t not in ("", "-") else 0
real["biaya"] = real["Biaya"].map(ke_angka)
print("sesudah dibersihkan, total:", f'{real["biaya"].sum():,}'.replace(",","."))

print("\n=== nama proyek di dua sheet TIDAK SAMA ===")
print("di RAB      :", sorted(rab["Nama Proyek"].tolist()))
print("\ndi Realisasi:", sorted(real["Proyek"].unique().tolist()))

print("\n=== kalau nekat merge langsung ===")
coba = rab.merge(real, left_on="Nama Proyek", right_on="Proyek", how="inner")
print("baris hasil merge:", len(coba), " <-- tidak ada satu pun yang cocok")

# --- tabel pemetaan dibuat MANUAL, karena ini keputusan manusia ---
PETA = {
 "RUKO DEPOK - 2024":             "Pembangunan Ruko Depok 2 Lantai",
 "PEK. TAMBAH KURANG RUKO DEPOK": "Pembangunan Ruko Depok 2 Lantai",   # pekerjaan tambah masuk ke proyek induk
 "renovasi kantor sinarmas":      "Renovasi Kantor PT Sinar Mas",
 "GUDANG CIBITUNG":               "Gudang Logistik Cibitung",
 "Rmh Bpk Handoko":               "Rumah Tinggal Bpk. Handoko",
 "PAGAR TAMAN GRIYA":             "Pagar & Taman Perumahan Griya",
 "MASJID AL IKHLAS TAHAP II":     "Masjid Al-Ikhlas Tahap 2",
 "KIOS PASAR BEKASI":             "Kios Pasar Modern Bekasi",
}
belum = set(real["Proyek"].unique()) - set(PETA)
assert not belum, f"belum dipetakan: {belum}"
real["proyek_baku"] = real["Proyek"].map(PETA)

rekap = (real.groupby("proyek_baku")["biaya"].sum().rename("realisasi").reset_index()
         .merge(rab, left_on="proyek_baku", right_on="Nama Proyek", how="outer"))
rekap["selisih"]    = rekap["Total RAB"] - rekap["realisasi"]
rekap["serapan_%"]  = (rekap["realisasi"] / rekap["Total RAB"] * 100).round(1)
rekap["laba"]       = rekap["Nilai Kontrak"] - rekap["realisasi"]
rekap["margin_%"]   = (rekap["laba"] / rekap["Nilai Kontrak"] * 100).round(1)
rekap["target_%"]   = (rekap["Target Margin"] * 100).round(1)

print("\n=== HASIL: RAB lawan realisasi ===")
print(rekap[["proyek_baku","Nilai Kontrak","Total RAB","realisasi","serapan_%","laba","margin_%","target_%"]]
      .sort_values("margin_%").to_string(index=False))

print("\n=== proyek yang RAB-nya jebol ===")
j = rekap[rekap["selisih"] < 0]
print(j[["proyek_baku","Total RAB","realisasi","selisih"]].to_string(index=False))

print("\n=== total ===")
print("nilai kontrak :", f'{rekap["Nilai Kontrak"].sum():,.0f}'.replace(",","."))
print("total RAB     :", f'{rekap["Total RAB"].sum():,.0f}'.replace(",","."))
print("realisasi     :", f'{rekap["realisasi"].sum():,.0f}'.replace(",","."))
print("laba kotor    :", f'{rekap["laba"].sum():,.0f}'.replace(",","."))
print("margin rata2  :", round(rekap["laba"].sum()/rekap["Nilai Kontrak"].sum()*100,1), "%")
print("tie-out ke sheet Realisasi:", int(rekap["realisasi"].sum()) - int(real["biaya"].sum()))
