"""Titik masuk baris perintah untuk alat laporan."""
import argparse
import logging
import sys
import time
from pathlib import Path

import pandas as pd

from laporan.hitung import omzet_per_cabang

TIPE = {"id": "int32", "cabang": "category", "pelanggan_id": "int32",
        "produk": "category", "jumlah": "int8", "nilai": "int32"}

log = logging.getLogger("laporan")


def atur_log(rinci: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if rinci else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def argumen(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Ringkas omzet per cabang dari berkas CSV.")
    p.add_argument("--berkas", type=Path, required=True, help="CSV sumber")
    p.add_argument("--keluar", type=Path, help="CSV hasil (kalau kosong: cetak ke layar)")
    p.add_argument("--cabang", help="saring satu cabang saja")
    p.add_argument("--rinci", action="store_true", help="tampilkan log tingkat DEBUG")
    return p.parse_args(argv)


def main(argv=None) -> int:
    a = argumen(argv)
    atur_log(a.rinci)
    mulai = time.perf_counter()

    if not a.berkas.exists():
        log.error("berkas tidak ditemukan: %s", a.berkas)
        return 2                       # kode keluar bukan-nol = gagal

    log.info("membaca %s", a.berkas)
    df = pd.read_csv(a.berkas, dtype=TIPE, parse_dates=["tanggal"])
    log.debug("terbaca %s baris, memori %.1f MB",
              f"{len(df):,}", df.memory_usage(deep=True).sum() / 1e6)

    if a.cabang:
        sebelum = len(df)
        df = df[df["cabang"] == a.cabang]
        log.info("saring cabang=%s: %s -> %s baris", a.cabang, f"{sebelum:,}", f"{len(df):,}")
        if df.empty:
            log.warning("tidak ada baris untuk cabang %r — hasilnya akan kosong", a.cabang)

    hasil = omzet_per_cabang(df)
    if a.keluar:
        hasil.to_csv(a.keluar, index=False)
        log.info("ditulis ke %s", a.keluar)
    else:
        print(hasil.to_string(index=False))

    log.info("selesai dalam %.2f detik", time.perf_counter() - mulai)
    return 0


if __name__ == "__main__":
    sys.exit(main())
