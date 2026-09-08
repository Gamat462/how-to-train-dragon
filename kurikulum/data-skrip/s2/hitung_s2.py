"""Kalkulator biaya S2 luar negeri (Jalur S2, Hari 3).

Ubah tiga angka di bagian ANGKAMU, jalankan, dan tabelnya dihitung ulang
dengan asumsimu sendiri. Semua angka sumber tercatat dalam mata uang aslinya,
jadi kamu bisa memeriksa dan membantahnya satu per satu.

    python hitung_s2.py              # semua rute, biaya sendiri
    python hitung_s2.py --beasiswa   # uang kuliah & biaya hidup ditanggung
"""
import sys

# ---------- ANGKAMU: ubah tiga baris ini ----------
GAJI_SEKARANG = 14_000_000      # rupiah/bulan yang hilang selama kuliah penuh waktu
GAJI_PASAR    = 6_000_000       # median gaji data analyst Indonesia, buat pembanding
TAHUN_IMPAS   = 5               # dalam berapa tahun modalnya harus kembali
# --------------------------------------------------

# Kurs jual 6 September 2026 (BCA, BRI, Yahoo Finance). Ganti kalau sudah berubah.
KURS = {"USD": 17_690, "GBP": 24_114, "AUD": 12_538,
        "CHF": 22_489, "EUR": 20_649, "SGD": 14_044}

# (nama, mata uang, uang kuliah total, biaya hidup total, bulan, tetap bekerja?)
# Biaya hidup memakai syarat dana visa resmi — itu BATAS BAWAH yang diizinkan
# pemerintah setempat, bukan perkiraan nyaman.
RUTE = [
    ("Georgia Tech OMSA (daring)",  "USD",  12_000,       0, 30, True),
    ("Jerman negeri (RWTH/TU Berlin)","EUR",  1_438,  23_808, 24, False),
    ("TU Munich (non-UE)",          "EUR",  24_000,  23_808, 24, False),
    ("NUS MSc DSML",                "SGD",  55_590,  27_000, 18, False),
    ("ETH Zurich",                  "CHF",   8_760,  44_400, 24, False),
    ("Edinburgh",                   "GBP",  38_500,  14_052, 12, False),
    ("Imperial College London",     "GBP",  39_900,  18_348, 12, False),
    ("Berkeley MIDS (daring)",      "USD",  82_227,       0, 24, True),
    ("CMU Heinz BIDA (daring)",     "USD",  89_599,       0, 30, True),
    ("University of Melbourne",     "AUD", 119_684,  59_420, 24, False),
]

def jt(x):
    """1234567890 -> '1.234,6' (juta rupiah, gaya Indonesia).
    Titik ribuan dan koma desimal ditukar lewat penanda sementara, karena
    .replace(",", ".") saja akan menghasilkan '1.234.6' yang tidak terbaca."""
    return f"{x/1e6:,.1f}".replace(",", "#").replace(".", ",").replace("#", ".")

def hitung(beasiswa=False):
    baris = []
    for nama, mu, kuliah, hidup, bulan, tetap_kerja in RUTE:
        r = KURS[mu]
        kantong = 0 if beasiswa else (kuliah + hidup) * r
        hilang = 0 if tetap_kerja else bulan * GAJI_SEKARANG
        ekonomi = kantong + hilang
        impas = ekonomi / (TAHUN_IMPAS * 12)
        setara = ekonomi / GAJI_PASAR
        baris.append((nama, bulan, kantong, hilang, ekonomi, impas, setara))
    return sorted(baris, key=lambda b: b[4])

def main():
    beasiswa = "--beasiswa" in sys.argv
    print("uang kuliah & biaya hidup:", "DITANGGUNG BEASISWA" if beasiswa else "biaya sendiri")
    print(f"gaji yang hilang: Rp {jt(GAJI_SEKARANG)} jt/bln · impas dalam {TAHUN_IMPAS} tahun\n")
    print(f"{'rute':32}{'bln':>5}{'kantong':>11}{'gaji hilang':>13}"
          f"{'biaya ekonomi':>15}{'impas/bln':>11}{'= bln gaji':>12}")
    for nama, bulan, kantong, hilang, ekonomi, impas, setara in hitung(beasiswa):
        print(f"{nama:32}{bulan:>5}{jt(kantong):>11}{jt(hilang):>13}"
              f"{jt(ekonomi):>15}{jt(impas):>11}{setara:>12.0f}")

if __name__ == "__main__":
    main()
