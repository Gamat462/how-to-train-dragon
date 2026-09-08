import pandas as pd, re
from datetime import date
pd.set_option("display.width", 230)
TGL = pd.Timestamp("2024-06-30")

pi = pd.read_excel("Daftar Piutang PT Anugerah Jaya.xlsx", skiprows=2)
rk = pd.read_csv("Rekening Koran Juni 2024.csv", sep=";", dtype=str)
print("faktur:", pi.shape, "| rekening koran:", rk.shape)

def ke_angka(x):
    if pd.isna(x) or str(x).strip() == "": return 0
    t = re.sub(r"[^0-9]", "", str(x))
    return int(t) if t else 0

rk["kredit"] = rk["Kredit"].map(ke_angka)
rk["debet"]  = rk["Debet"].map(ke_angka)
rk["tanggal"] = pd.to_datetime(rk["Tanggal"], format="%d/%m/%Y")
pi["tanggal"] = pd.to_datetime(pi["Tgl Faktur"], format="%d/%m/%Y")
pi["jatuh_tempo"] = pd.to_datetime(pi["Jatuh Tempo"], format="%d/%m/%Y")

print("\n=== 1. mana yang uang MASUK ===")
masuk = rk[rk["kredit"] > 0].copy()
print("baris kredit:", len(masuk), "| nilai:", f'{masuk["kredit"].sum():,}'.replace(",","."))

print("\n=== 2. cocokkan keterangan bank ke pelanggan ===")
# kunci pencarian dibuat MANUAL: ini pekerjaan manusia, bukan tebakan mesin
PETA = {
 "SUMBERMAKMUR":     "PT Sumber Makmur Sentosa",
 "SUMBER MAKMUR":    "PT Sumber Makmur Sentosa",
 "BERKAH JAYA":      "CV Berkah Jaya Abadi",
 "CV BERKAH":        "CV Berkah Jaya Abadi",
 "TOKO BAHAGIA":     "Toko Bahagia",
 "SINAR TERANG":     "UD Sinar Terang",
 "SINARTERANG":      "UD Sinar Terang",
 "MITRA NIAGA":      "PT Mitra Niaga Utama",
 "TOKO SEJAHTERA":   "Toko Sejahtera",
 "TK SEJAHTERA":     "Toko Sejahtera",
 "ANUGERAH PANGAN":  "CV Anugerah Pangan",
 "GLOBAL DISTRIBUSI":"PT Global Distribusi",
 "GLOBAL DIST":      "PT Global Distribusi",
}
def cocokkan(ket):
    k = str(ket).upper()
    for kunci, nama in PETA.items():
        if kunci in k: return nama
    return None
masuk["pelanggan"] = masuk["Keterangan"].map(cocokkan)

cocok = masuk[masuk["pelanggan"].notna()]
tidak = masuk[masuk["pelanggan"].isna()]
print("kredit tercocokkan  :", len(cocok), "|", f'{cocok["kredit"].sum():,}'.replace(",","."))
print("kredit TIDAK cocok  :", len(tidak), "|", f'{tidak["kredit"].sum():,}'.replace(",","."))
print("\nyang tidak cocok — harus ditanyakan ke klien:")
print(tidak[["Tanggal","Keterangan","kredit"]].to_string(index=False))

print("\n=== 3. saldo piutang per pelanggan ===")
f = pi.groupby("Pelanggan")["Nilai Faktur"].agg(["count","sum"]).rename(
    columns={"count":"faktur","sum":"nilai_faktur"})
b = cocok.groupby("pelanggan")["kredit"].sum().rename("dibayar")
s = f.join(b).fillna(0)
s["saldo"] = s["nilai_faktur"] - s["dibayar"]
s["tertagih_%"] = (s["dibayar"]/s["nilai_faktur"]*100).round(1)
print(s.sort_values("saldo", ascending=False).to_string())
print("\nTOTAL saldo piutang:", f'{s["saldo"].sum():,.0f}'.replace(",","."))

print("\n=== 4. umur piutang (aging) berbasis faktur tertua ===")
# pembayaran diterapkan FIFO: faktur paling tua dilunasi lebih dulu
pi = pi.sort_values(["Pelanggan","tanggal"]).reset_index(drop=True)
bayar_sisa = b.to_dict()
sisa_faktur = []
for _, row in pi.iterrows():
    p = row["Pelanggan"]; n = row["Nilai Faktur"]
    pakai = min(bayar_sisa.get(p, 0), n)
    bayar_sisa[p] = bayar_sisa.get(p, 0) - pakai
    sisa_faktur.append(n - pakai)
pi["sisa"] = sisa_faktur
pi["umur"] = (TGL - pi["jatuh_tempo"]).dt.days

def ember(h):
    if h <= 0:  return "1. Belum jatuh tempo"
    if h <= 30: return "2. 1-30 hari"
    if h <= 60: return "3. 31-60 hari"
    if h <= 90: return "4. 61-90 hari"
    return "5. > 90 hari"
pi["kelompok"] = pi["umur"].map(ember)
ag = pi[pi["sisa"] > 0].groupby("kelompok").agg(faktur=("sisa","size"), nilai=("sisa","sum"))
ag["persen"] = (ag["nilai"]/ag["nilai"].sum()*100).round(1)
print(ag.to_string())
print("\ntotal aging:", f'{ag["nilai"].sum():,.0f}'.replace(",","."),
      "| cocok dengan saldo?", int(ag["nilai"].sum()) == int(s["saldo"].sum()))

print("\n=== 5. piutang macet (>90 hari) per pelanggan ===")
macet = pi[(pi["sisa"] > 0) & (pi["umur"] > 90)]
print(macet.groupby("Pelanggan")["sisa"].agg(["size","sum"]).to_string())
print("total macet:", f'{macet["sisa"].sum():,.0f}'.replace(",","."),
      f'({macet["sisa"].sum()/s["saldo"].sum()*100:.1f}% dari saldo)')
