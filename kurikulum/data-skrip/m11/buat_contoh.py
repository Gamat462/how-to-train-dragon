"""Membuat data-contoh/penjualan.csv untuk Minggu 11 (Hari 73-74).
Angka acaknya berkunci tetap, jadi hasilmu sama persis dengan yang tertulis di modul:
400 baris, omzet Rp 224.907.000."""
import random, csv, os
from datetime import date, timedelta

rng = random.Random(11)
PRODUK = ["Semen 40kg", "Cat 5kg", "Pasir m3", "Keramik dus", "Pipa 4 inci"]
HARGA = {"Semen 40kg": 62000, "Cat 5kg": 185000, "Pasir m3": 320000,
         "Keramik dus": 145000, "Pipa 4 inci": 78000}

baris = []
for i in range(400):
    d = date(2024, 1, 1) + timedelta(days=rng.randrange(182))
    p = PRODUK[rng.randrange(5)]
    q = rng.choice([1, 1, 2, 3, 5, 10])
    baris.append([d.isoformat(), f"NT{i+1:04d}", p, q, HARGA[p], q * HARGA[p]])
baris.sort()

os.makedirs("data-contoh", exist_ok=True)
with open("data-contoh/penjualan.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["tanggal", "nota", "produk", "qty", "harga", "jumlah"])
    w.writerows(baris)

print("baris ditulis:", len(baris))
print("omzet total  : Rp", f"{sum(b[5] for b in baris):,}".replace(",", "."))
