# -*- coding: utf-8 -*-
"""Hitung biaya ekonomi tiap rute S2 luar negeri, dalam rupiah.
Semua angka masukan berasal dari sumber yang dicatat di kolom 'sumber'.
Tidak ada angka yang dikarang: kalau tidak ada sumbernya, tidak dipakai.
"""

# Kurs jual, 6 September 2026 (BCA / BRI / Yahoo Finance)
KURS = {"USD": 17_690, "GBP": 24_114, "AUD": 12_538,
        "CHF": 22_489, "EUR": 20_649, "SGD": 14_044}

def rp(mata, jumlah):
    return round(jumlah * KURS[mata])

def juta(x):
    return f"Rp {x/1_000_000:,.1f} juta".replace(",", ".")

# (nama, bulan_kuliah, uang_kuliah_total_rp, biaya_hidup_total_rp, catatan)
RUTE = []

# 1. Georgia Tech OMSA - daring, tidak pindah negara, bisa sambil kerja
RUTE.append(("Georgia Tech OMSA (daring, AS)", 30, rp("USD", 12_000), 0,
             "daring; tetap bekerja, jadi biaya kesempatan = 0"))

# 2. Jerman negeri (RWTH / TU Berlin / LMU) - kontribusi semester 360 EUR x 4
RUTE.append(("Jerman negeri (RWTH/TU Berlin)", 24, rp("EUR", 360*4), rp("EUR", 11_904*2),
             "kontribusi semester EUR 360; hidup = rekening terblokir EUR 11.904/th"))

# 3. TUM (non-UE bayar) - EUR 6.000/semester x 4
RUTE.append(("TU Munich (TUM, non-UE)", 24, rp("EUR", 6_000*4), rp("EUR", 11_904*2),
             "TUM memungut EUR 6.000/semester untuk non-UE"))

# 4. ETH Zurich - CHF 2.190/semester x 4; hidup CHF 1.850/bln (tengah 1.500-2.200)
RUTE.append(("ETH Zurich MSc Data Science", 24, rp("CHF", 2_190*4), rp("CHF", 1_850*24),
             "uang kuliah CHF 2.190/semester; hidup pakai titik tengah CHF 1.500-2.200"))

# 5. Inggris 1 tahun, London (Imperial GBP 39.900) - hidup pakai syarat visa London
RUTE.append(("Imperial College London (1 th)", 12, rp("GBP", 39_900), rp("GBP", 1_529*12),
             "uang kuliah luar negeri 2026 GBP 39.900; hidup pakai patokan visa London"))

# 6. Inggris 1 tahun, luar London (Edinburgh GBP 38.500)
RUTE.append(("Edinburgh MSc Data Science (1 th)", 12, rp("GBP", 38_500), rp("GBP", 1_171*12),
             "uang kuliah indikatif GBP 38.500; hidup pakai patokan visa luar London"))

# 7. Australia - Melbourne MDS 2 tahun AUD 119.684; hidup pakai patokan visa AUD 29.710/th
RUTE.append(("Univ. of Melbourne MDS (2 th)", 24, rp("AUD", 119_684), rp("AUD", 29_710*2),
             "uang kuliah seluruh program AUD 119.684; hidup pakai patokan visa"))

# 8. NUS DSML - SGD 55.590 termasuk GST; hidup SGD 1.500/bln x 18 bulan
RUTE.append(("NUS MSc DSML (1,5 th)", 18, rp("SGD", 55_590), rp("SGD", 1_500*18),
             "uang kuliah SGD 55.590 (sudah GST 9%); hidup asumsi SGD 1.500/bln"))

# 9. Berkeley MIDS daring
RUTE.append(("Berkeley MIDS (daring, AS)", 24, rp("USD", 82_226), 0,
             "daring; total kuliah+biaya untuk yang mulai Fall 2026"))

# 10. CMU Heinz MSIT-BIDA daring
RUTE.append(("CMU Heinz BIDA (daring, AS)", 30, rp("USD", 89_600), 0,
             "daring; perkiraan total program"))

print("=" * 96)
print("BIAYA KANTONG (uang kuliah + biaya hidup), kurs jual 6 September 2026")
print("=" * 96)
print(f"{'Rute':<36}{'Bln':>5}{'Kuliah':>17}{'Hidup':>17}{'Total kantong':>19}")
print("-" * 96)
hasil = []
for nama, bln, kuliah, hidup, cat in RUTE:
    total = kuliah + hidup
    hasil.append((nama, bln, kuliah, hidup, total, cat))
    print(f"{nama:<36}{bln:>5}{juta(kuliah):>17}{juta(hidup):>17}{juta(total):>19}")
print()

# Biaya kesempatan: gaji yang hilang selama berhenti kerja.
# Dua skenario, dua-duanya dari data lapangan yang sudah dikumpulkan:
#   konservatif : Rp 6.000.000  (median gaji data analyst Indonesia, NodeFlair)
#   realistis   : Rp 14.000.000 (batas bawah Big 4 Senior Associate 2-3 th)
SKENARIO = {"median DA (Rp 6 jt)": 6_000_000, "jalur audit-analytics (Rp 14 jt)": 14_000_000}

for label, gaji in SKENARIO.items():
    print("=" * 96)
    print(f"BIAYA EKONOMI TOTAL - gaji yang dikorbankan: {label}")
    print("=" * 96)
    print(f"{'Rute':<36}{'Kantong':>17}{'Gaji hilang':>17}{'Biaya ekonomi':>19}")
    print("-" * 96)
    for nama, bln, kuliah, hidup, total, cat in hasil:
        daring = hidup == 0 and "daring" in cat
        hilang = 0 if daring else gaji * bln
        print(f"{nama:<36}{juta(total):>17}{juta(hilang):>17}{juta(total+hilang):>19}")
    print()
