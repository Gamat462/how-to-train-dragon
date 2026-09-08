import pandas as pd, numpy as np
pd.set_option("display.width", 220)
BERKAS = "Rekap SPP Yayasan Bina Cendekia.xlsx"
BULAN = ["Jul","Agu","Sep","Okt","Nov","Des","Jan","Feb","Mar","Apr","Mei","Jun"]

df = pd.read_excel(BERKAS, skiprows=2)
print("bentuk mentah:", df.shape)
print(df.head(3).to_string())

tu = df[df["Nama Siswa"].astype(str).str.startswith("TOTAL DITERIMA", na=False)]
VERSI_TU = int(tu["Jun"].iloc[0])
print("\nangka yang dilaporkan TU:", f"{VERSI_TU:,}".replace(",","."))

d = df[df["NIS"].notna()].copy()
print("siswa:", len(d))

print("\n=== isi sel bulan itu apa saja? ===")
semua = pd.concat([d[b] for b in BULAN])
jenis = semua.map(lambda x: "kosong" if pd.isna(x) else ("angka" if isinstance(x,(int,float,np.integer)) else f"teks: {x}"))
print(jenis.value_counts().to_string())

# --- ubah dari MELEBAR jadi MEMANJANG ---
panjang = d.melt(id_vars=["NIS","Nama Siswa","Kelas","SPP/Bulan","Keterangan"],
                 value_vars=BULAN, var_name="bulan", value_name="isi")
panjang["urut"] = panjang["bulan"].map({b:i for i,b in enumerate(BULAN)})
print("\nbentuk memanjang:", panjang.shape, f"({len(d)} siswa x {len(BULAN)} bulan)")

TEKS_LUNAS  = {"LUNAS","lunas","Lunas"}
TEKS_BELUM  = {"blm","BELUM","nunggak","x"}
TEKS_KELUAR = {"-"}

def tafsir(row):
    v = row["isi"]
    if pd.isna(v):                      return pd.Series(["belum bayar", 0, 1])
    if isinstance(v, (int, float, np.integer)):
        return pd.Series(["bayar", int(v), 1])
    s = str(v).strip()
    if s in TEKS_LUNAS:                 return pd.Series(["bayar", int(row["SPP/Bulan"]), 1])
    if s in TEKS_KELUAR:                return pd.Series(["tidak wajib", 0, 0])
    if s in TEKS_BELUM:                 return pd.Series(["belum bayar", 0, 1])
    return pd.Series(["tak dikenali", 0, 1])

panjang[["status","dibayar","wajib"]] = panjang.apply(tafsir, axis=1)
print("\n=== hasil penafsiran tiap sel ===")
print(panjang["status"].value_counts().to_string())
assert (panjang["status"] == "tak dikenali").sum() == 0

panjang["tagihan"] = panjang["wajib"] * panjang["SPP/Bulan"]
panjang["kurang"]  = panjang["tagihan"] - panjang["dibayar"]

print("\n=== PEMERIKSAAN ===")
diterima = int(panjang["dibayar"].sum())
tagihan  = int(panjang["tagihan"].sum())
print("total tagihan       :", f"{tagihan:,}".replace(",","."))
print("total diterima      :", f"{diterima:,}".replace(",","."))
print("tunggakan sebenarnya:", f"{tagihan-diterima:,}".replace(",","."))
print("versi TU            :", f"{VERSI_TU:,}".replace(",","."))
print("SELISIH             :", f"{diterima-VERSI_TU:,}".replace(",","."),
      f'<- dari {(panjang["isi"].isin(TEKS_LUNAS)).sum()} sel bertuliskan "LUNAS"')

print("\n=== HASIL: tunggakan per kelas ===")
print(panjang.groupby("Kelas").agg(siswa=("NIS","nunique"), tagihan=("tagihan","sum"),
      diterima=("dibayar","sum"), tunggakan=("kurang","sum"))
      .assign(persen=lambda x: (x.tunggakan/x.tagihan*100).round(1)).to_string())

print("\n=== HASIL: 8 siswa dengan tunggakan terbesar ===")
per = (panjang.groupby(["NIS","Nama Siswa","Kelas"])
       .agg(bulan_wajib=("wajib","sum"), tunggakan=("kurang","sum"),
            bulan_nunggak=("status", lambda s: (s=="belum bayar").sum()))
       .reset_index().sort_values("tunggakan", ascending=False))
print(per.head(8).to_string(index=False))

print("\n=== HASIL: siswa pindah (bulan wajibnya < 12) ===")
pindah = per[per["bulan_wajib"] < 12]
print(len(pindah), "siswa | tunggakan mereka:",
      f'{int(pindah["tunggakan"].sum()):,}'.replace(",","."))
print(pindah[["NIS","Nama Siswa","Kelas","bulan_wajib","tunggakan"]].to_string(index=False))
