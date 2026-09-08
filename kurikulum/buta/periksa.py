"""Pemeriksa STRUKTUR untuk Proyek Buta.

Berkas ini HANYA memastikan datamu termuat lengkap dan benar bentuknya.
Ia TIDAK memberi tahu apa pun tentang temuanmu — itu bagianmu.

    python periksa.py 1     # periksa Proyek 1
    python periksa.py 2
    python periksa.py 3
"""
import sys
import pandas as pd

HARAP = {
    "1": {"berkas": "P1 Koperasi Sejahtera Mandiri.xlsx",
          "sheet": {"Pinjaman": (60, 3), "Angsuran": (496, 0)}},
    "2": {"berkas": "P2 Apotek Sehat Sentosa.xlsx",
          "sheet": {"Stok": (39, 2), "Penjualan": (1141, 0)}},
    "3": {"berkas": ("P3 Penjualan Gerai.csv", "P3 Target Gerai.csv"),
          "baris": (28, 5)},
}


def periksa(n: str) -> bool:
    h = HARAP[n]
    ok = True
    if n == "3":
        jual = pd.read_csv(h["berkas"][0], sep=";")
        target = pd.read_csv(h["berkas"][1], sep=";")
        for nama, df, harap in [("penjualan", jual, h["baris"][0]),
                                ("target", target, h["baris"][1])]:
            status = "OK   " if len(df) == harap else "SALAH"
            if len(df) != harap: ok = False
            print(f"  {status} {nama:10s} {len(df):>5} baris (harus {harap})")
    else:
        for sheet, (harap, lewati) in h["sheet"].items():
            df = pd.read_excel(h["berkas"], sheet_name=sheet, skiprows=lewati)
            df = df.dropna(how="all")
            df = df[df.iloc[:, 0].notna()]
            n_baris = len(df)
            status = "OK   " if n_baris == harap else "SALAH"
            if n_baris != harap: ok = False
            print(f"  {status} sheet {sheet:10s} {n_baris:>5} baris data (harus {harap})")
    return ok


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in HARAP:
        print(__doc__); sys.exit(1)
    n = sys.argv[1]
    print(f"Proyek {n} — pemeriksaan struktur")
    berhasil = periksa(n)
    print("\n" + ("Struktur benar. Angkamu boleh dipakai." if berhasil
                  else "Ada yang belum termuat benar. Perbaiki dulu sebelum menganalisis."))
    print("Catatan: berkas ini TIDAK memeriksa temuanmu. Itu bagianmu.")
    sys.exit(0 if berhasil else 1)
