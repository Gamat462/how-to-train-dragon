"""Agregasi laporan. Tidak mencetak apa pun — hanya mengembalikan nilai."""
import pandas as pd


def omzet_per_cabang(df: pd.DataFrame) -> pd.DataFrame:
    """Ringkas omzet dan jumlah transaksi per cabang, terbesar dulu."""
    return (df.groupby("cabang", observed=True)
              .agg(transaksi=("nilai", "size"), omzet=("nilai", "sum"))
              .sort_values("omzet", ascending=False)
              .reset_index())
