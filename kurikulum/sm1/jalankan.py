# -*- coding: utf-8 -*-
"""Jalankan semua SQL modul L1 ke PostgreSQL, simpan hasilnya ke hasil.json."""
import sys, pathlib
AKAR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR/"mat")); sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _sql import jalankan
from kueri import KUERI
h = jalankan(KUERI, pathlib.Path(__file__).parent / "hasil.json")
galat = [k for k, v in h.items() if "galat" in v]
print(f"{len(h)} query dijalankan, {len(galat)} menghasilkan error:")
for k in galat:
    print("  ", k, "->", h[k]["galat"].splitlines()[0])
