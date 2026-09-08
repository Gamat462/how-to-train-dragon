# -*- coding: utf-8 -*-
"""Berapa kenaikan gaji per bulan yang DIBUTUHKAN supaya S2 balik modal?
Ini kebalikan dari cara biasa: bukan mengarang 'gaji naik sekian persen',
tapi menghitung syarat yang harus dipenuhi agar keputusan itu tidak rugi.
"""
KURS = {"USD":17_690,"GBP":24_114,"AUD":12_538,"CHF":22_489,"EUR":20_649,"SGD":14_044}
def rp(m,j): return round(j*KURS[m])
def jt(x): return f"{x/1_000_000:,.1f}".replace(",",".")

RUTE = [
 ("Georgia Tech OMSA (daring)",       30, rp("USD",12_000)+0,                    True),
 ("Jerman negeri (RWTH/TU Berlin)",   24, rp("EUR",360*4)+rp("EUR",11_904*2),    False),
 ("TU Munich (non-UE)",               24, rp("EUR",6_000*4)+rp("EUR",11_904*2),  False),
 ("ETH Zurich",                       24, rp("CHF",2_190*4)+rp("CHF",1_850*24),  False),
 ("Imperial College London",          12, rp("GBP",39_900)+rp("GBP",1_529*12),   False),
 ("Edinburgh",                        12, rp("GBP",38_500)+rp("GBP",1_171*12),   False),
 ("Univ. of Melbourne",               24, rp("AUD",119_684)+rp("AUD",29_710*2),  False),
 ("NUS DSML",                         18, rp("SGD",55_590)+rp("SGD",1_500*18),   False),
 ("Berkeley MIDS (daring)",           24, rp("USD",82_226)+0,                    True),
 ("CMU Heinz BIDA (daring)",          30, rp("USD",89_600)+0,                    True),
]
GAJI_HILANG = 14_000_000   # jalur audit-analytics, batas bawah Big 4 Senior Associate

print("="*104)
print("SYARAT IMPAS  -  kenaikan gaji BERSIH per bulan yang harus terjadi supaya modalnya kembali")
print("(gaji yang dikorbankan selama kuliah: Rp 14 juta/bulan; rute daring dianggap tetap bekerja)")
print("="*104)
print(f"{'Rute':<32}{'Biaya ekonomi':>16}{'impas 5 th':>16}{'impas 10 th':>16}{'setara gaji':>14}")
print("-"*104)
for nama,bln,kantong,daring in RUTE:
    hilang = 0 if daring else GAJI_HILANG*bln
    total  = kantong + hilang
    b5, b10 = total/60, total/120
    bulan_gaji = total/6_000_000     # berapa bulan gaji median DA (Rp 6 jt) yang dibakar
    print(f"{nama:<32}{jt(total):>13} jt{jt(b5):>13} jt{jt(b10):>13} jt{bulan_gaji:>11.0f} bln")

print()
print("="*104)
print("SKENARIO LPDP / CHEVENING / AUSTRALIA AWARDS  -  uang kuliah & hidup ditanggung")
print("(yang tersisa hanyalah gaji yang tidak kamu terima selama kuliah)")
print("="*104)
print(f"{'Rute':<32}{'Bln':>6}{'Biaya ekonomi':>18}{'impas 5 th':>16}{'impas 10 th':>16}")
print("-"*104)
for nama,bln,kantong,daring in RUTE:
    if daring: continue
    total = GAJI_HILANG*bln
    print(f"{nama:<32}{bln:>6}{jt(total):>15} jt{jt(total/60):>13} jt{jt(total/120):>13} jt")

print()
print("="*104)
print("PEMBANDING: rute belajar mandiri 23 minggu yang sudah kamu punya")
print("="*104)
biaya_mandiri = 0
print(f"  Uang kuliah                 : Rp 0")
print(f"  Biaya hidup tambahan        : Rp 0 (belajar dari rumah)")
print(f"  Lama                        : 23 minggu = {23*7/30.44:.1f} bulan")
print(f"  Gaji yang dikorbankan       : Rp 0 kalau belajar sambil kerja/freelance")
print(f"  Syarat impas                : tidak ada - tidak ada modal yang harus kembali")
