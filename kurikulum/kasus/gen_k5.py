"""Kasus 5 — PT Anugerah Jaya (distributor).
Piutang.xlsx : faktur beredar per pelanggan
RekKoran.csv : mutasi bank, keterangan berupa teks bebas seperti aslinya
"""
import random, csv
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font

rng = random.Random(555)
TGL_LAPORAN = date(2024, 6, 30)

PELANGGAN = [
 # (nama resmi,               cara bank menuliskannya)
 ("PT Sumber Makmur Sentosa", ["TRF DR PT SUMBER MAKMUR", "TRANSFER PT SUMBER MAKMUR SENTOSA", "PT SUMBERMAKMUR"]),
 ("CV Berkah Jaya Abadi",     ["KREDIT CV BERKAH JAYA", "TRF CV BERKAH JAYA ABADI", "SETORAN CV BERKAH"]),
 ("Toko Bahagia",             ["SETORAN TUNAI TOKO BAHAGIA", "TRF TOKO BAHAGIA"]),
 ("UD Sinar Terang",          ["TRF DR UD SINAR TERANG", "UD SINARTERANG"]),
 ("PT Mitra Niaga Utama",     ["TRANSFER PT MITRA NIAGA", "TRF PT MITRA NIAGA UTAMA"]),
 ("Toko Sejahtera",           ["SETORAN TOKO SEJAHTERA", "TRF TK SEJAHTERA"]),
 ("CV Anugerah Pangan",       ["TRF CV ANUGERAH PANGAN"]),
 ("PT Global Distribusi",     ["TRANSFER PT GLOBAL DISTRIBUSI", "TRF PT GLOBAL DIST"]),
]

# --- buat faktur ---
faktur = []
no = 0
for nama, _ in PELANGGAN:
    for _ in range(rng.randint(4, 9)):
        no += 1
        tgl = TGL_LAPORAN - timedelta(days=rng.randrange(5, 175))
        nilai = round(rng.randint(8_000_000, 95_000_000), -5)
        faktur.append(dict(no=f"INV/2024/{no:04d}", pelanggan=nama, tanggal=tgl,
                           jatuh_tempo=tgl + timedelta(days=30), nilai=nilai))

wb = Workbook(); ws = wb.active; ws.title = "Piutang"
ws["A1"] = "PT ANUGERAH JAYA - DAFTAR PIUTANG PER 30 JUNI 2024"
ws["A1"].font = Font(bold=True, size=12)
for i,h in enumerate(["No Faktur","Pelanggan","Tgl Faktur","Jatuh Tempo","Nilai Faktur"]):
    c = ws.cell(row=3, column=1+i, value=h); c.font = Font(bold=True)
for r, f in enumerate(faktur, start=4):
    ws.cell(row=r, column=1, value=f["no"])
    ws.cell(row=r, column=2, value=f["pelanggan"])
    ws.cell(row=r, column=3, value=f["tanggal"].strftime("%d/%m/%Y"))
    ws.cell(row=r, column=4, value=f["jatuh_tempo"].strftime("%d/%m/%Y"))
    ws.cell(row=r, column=5, value=f["nilai"])
wb.save("Daftar Piutang PT Anugerah Jaya.xlsx")

# --- buat mutasi bank ---
mutasi = []
terbayar = {}
for f in faktur:
    p = rng.random()
    if p < 0.55:      bayar = f["nilai"]                      # lunas
    elif p < 0.72:    bayar = round(f["nilai"] * rng.choice([0.3,0.5,0.6]), -5)  # sebagian
    else:             bayar = 0                                # belum bayar
    if bayar:
        d = f["jatuh_tempo"] + timedelta(days=rng.randrange(-10, 25))
        if d > TGL_LAPORAN: d = TGL_LAPORAN - timedelta(days=rng.randrange(1,10))
        ket = rng.choice(dict(PELANGGAN)[f["pelanggan"]])
        mutasi.append((d, ket, int(bayar)))
        terbayar[f["pelanggan"]] = terbayar.get(f["pelanggan"], 0) + int(bayar)

# transaksi bank yang BUKAN pelunasan piutang
for _ in range(14):
    d = TGL_LAPORAN - timedelta(days=rng.randrange(1, 180))
    ket, n = rng.choice([
        ("BIAYA ADM BULANAN", -25000),
        ("BUNGA GIRO", rng.randint(15000, 90000)),
        ("PAJAK BUNGA", -rng.randint(3000, 18000)),
        ("TRF KE SUPPLIER PT INDOFOOD", -rng.randint(20_000_000, 60_000_000)),
        ("SETORAN MODAL DIREKTUR", rng.randint(50_000_000, 150_000_000)),
        ("BIAYA TRANSFER RTGS", -6500),
    ])
    mutasi.append((d, ket, n))

# dua setoran dari pihak yang tidak dikenali sama sekali
for _ in range(2):
    d = TGL_LAPORAN - timedelta(days=rng.randrange(1, 90))
    mutasi.append((d, rng.choice(["TRF DR PT MAJU BERSAMA", "SETORAN TUNAI TANPA KETERANGAN"]),
                   rng.randint(5_000_000, 20_000_000)))

mutasi.sort(key=lambda x: x[0])
with open("Rekening Koran Juni 2024.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["Tanggal","Keterangan","Debet","Kredit"])
    for d, ket, n in mutasi:
        deb = f"{-n:,}".replace(",",".") if n < 0 else ""
        kre = f"{n:,}".replace(",",".")  if n > 0 else ""
        w.writerow([d.strftime("%d/%m/%Y"), ket, deb, kre])

total_faktur = sum(f["nilai"] for f in faktur)
total_bayar  = sum(terbayar.values())
print("faktur           :", len(faktur), "| nilai:", f"{total_faktur:,}".replace(",","."))
print("baris rek koran  :", len(mutasi))
print("pelunasan piutang:", f"{total_bayar:,}".replace(",","."))
print("saldo piutang    :", f"{total_faktur-total_bayar:,}".replace(",","."))
