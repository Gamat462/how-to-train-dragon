"""Fungsi pembersihan yang bisa diuji satu per satu."""
import re
import pandas as pd


def ke_angka(nilai: object) -> int | None:
    """Ubah teks berformat Indonesia jadi bilangan bulat.

    >>> ke_angka("3.200.000")
    3200000
    >>> ke_angka("Rp 91.190.000")
    91190000
    >>> ke_angka(None) is None
    True
    """
    if nilai is None or (isinstance(nilai, float) and pd.isna(nilai)):
        return None
    if isinstance(nilai, (int,)):
        return int(nilai)
    asli = str(nilai).strip()
    negatif = asli.startswith("(") and asli.endswith(")")
    teks = re.sub(r"[^0-9\-]", "", asli)
    if teks in ("", "-"):
        return None
    return -int(teks) if negatif else int(teks)


def rapikan_nama(s: pd.Series) -> pd.Series:
    """Samakan penulisan nama: spasi ganda, huruf besar-kecil, badan usaha."""
    return (s.str.strip()
             .str.replace(r"\s+", " ", regex=True)
             .str.title()
             .str.replace(r"^(Cv|Pt|Ud)(\.?)\s+",
                          lambda m: m.group(1).upper() + m.group(2) + " ", regex=True))


def buang_baris_bukan_data(df: pd.DataFrame, kolom_no: str = "No") -> pd.DataFrame:
    """Sisakan hanya baris yang kolom nomornya benar-benar angka."""
    return df[df[kolom_no].fillna("").astype(str).str.fullmatch(r"\d+")].copy()
