"""Hitung mundur tenggat beasiswa dan kapan tiap fase kurikulum selesai (Jalur S2, Hari 5-6).

Modul menulis "tinggal 29 hari" pada 7 September 2026. Besok angka itu salah.
Skrip ini menghitungnya ulang dari tanggal hari ini, jadi tidak pernah basi.

    python hitung_tenggat.py                 # mulai belajar hari ini
    python hitung_tenggat.py 2026-09-08      # mulai belajar pada tanggal itu
"""
import sys
from datetime import date, timedelta

# Ritme kurikulum: 2 hari materi per hari kerja, 5 hari seminggu = 10 per minggu.
PER_MINGGU = 10

# Jumlah hari materi kumulatif tiap fase (dihitung dari _urutan.py, bukan diketik).
FASE = [("Fase 1-5 (teknis)", 217), ("Fase 1-6", 254), ("Fase 1-7 (penuh)", 282)]

# Tenggat beasiswa. Perbarui kalau panitianya mengumumkan tanggal baru.
# (nama, tenggat, catatan, apakah butuh portofolio kurikulum selesai)
TENGGAT = [
    ("Chevening 2027/28",     date(2026, 10, 6), "6 Okt 2026, 11:00 UTC",        False),
    ("LPDP Tahap 1 2027",     date(2027, 2, 23), "perkiraan, pola 2026",         True),
    ("Australia Awards 2028", date(2027, 4, 30), "jendela 1 Feb - 30 Apr 2027",  True),
]

def selesai(mulai, hari_materi):
    """Bulatkan ke minggu penuh, seperti rencana di MULAI-DI-SINI."""
    minggu = -(-hari_materi // PER_MINGGU)          # pembulatan ke atas
    return mulai + timedelta(weeks=minggu), minggu

def main():
    hari_ini = date.today()
    mulai = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else hari_ini
    print("hari ini      :", hari_ini)
    print("mulai belajar :", mulai, "\n")

    print("TENGGAT")
    for nama, tgl, cat, _ in TENGGAT:
        sisa = (tgl - hari_ini).days
        status = f"{sisa:>4} hari lagi" if sisa >= 0 else f"LEWAT {-sisa} hari"
        print(f"  {nama:24} {tgl}  {status:18} ({cat})")

    print("\nKAPAN FASE SELESAI")
    for nama, hari in FASE:
        tgl, minggu = selesai(mulai, hari)
        print(f"  {nama:20} {hari:>4} hari materi = {minggu:>2} minggu -> {tgl}")

    print("\nMUAT ATAU TIDAK")
    pakai = [x for x in TENGGAT if x[3]]
    print("  (Chevening tidak masuk tabel ini: ia tidak menunggu portofoliomu selesai)")
    print(f"  {'berhenti di':20}" + "".join(f"{n[:20]:>22}" for n, _, _, _ in pakai))
    for nama, hari in FASE:
        tgl, _ = selesai(mulai, hari)
        sel = []
        for _, t, _, _ in pakai:
            d = (t - tgl).days
            sel.append(f"muat, sisa {d} hr" if d >= 0 else f"TERLAMBAT {-d} hr")
        print(f"  {nama:20}" + "".join(f"{s:>22}" for s in sel))

if __name__ == "__main__":
    main()
