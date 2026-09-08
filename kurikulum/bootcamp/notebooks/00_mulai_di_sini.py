# ============================================================
# Bootcamp Data Analyst — Sel pertama untuk SEMUA notebook
# Salin sel ini di paling atas tiap notebook barumu.
# ============================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", 40)
pd.set_option("display.width", 160)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (9, 4.5)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

DATA = "data"          # ubah kalau letak foldermu berbeda

def muat_semua():
    """Memuat seluruh tabel Kedai Kopi Senja sekaligus."""
    t  = pd.read_csv(f"{DATA}/transaksi.csv", parse_dates=["tanggal"])
    it = pd.read_csv(f"{DATA}/transaksi_item.csv")
    pr = pd.read_csv(f"{DATA}/produk.csv", parse_dates=["tanggal_rilis"])
    cb = pd.read_csv(f"{DATA}/cabang.csv", parse_dates=["tanggal_buka"])
    pl = pd.read_csv(f"{DATA}/pelanggan.csv", parse_dates=["tanggal_daftar"])
    kl = pd.read_csv(f"{DATA}/kalender.csv", parse_dates=["tanggal"])
    return t, it, pr, cb, pl, kl

def periksa(df, nama="data"):
    """Pemeriksaan awal yang harus dijalankan pada SETIAP data baru."""
    print(f"=== {nama} ===")
    print(f"bentuk   : {df.shape}")
    print(f"duplikat : {df.duplicated().sum()}")
    kosong = df.isna().sum()
    kosong = kosong[kosong > 0]
    print(f"kosong   : {dict(kosong) if len(kosong) else 'tidak ada'}")
    print(f"tipe     : {dict(df.dtypes.astype(str))}")
    return df.head()

# --- Uji cepat: jalankan ini dulu sebelum apa pun ---
if __name__ == "__main__":
    t, it, pr, cb, pl, kl = muat_semua()
    periksa(t, "transaksi")
    assert len(t) == 151088, f"jumlah transaksi salah: {len(t)}"
    assert int(t.total.sum()) == 8567304450, f"total omzet salah: {t.total.sum()}"
    print("\nSemua pemeriksaan lolos. Data siap dipakai.")
