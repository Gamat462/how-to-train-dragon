"""
Generator dataset Bootcamp Data Analyst — Kedai Kopi Senja
Semua data dibuat dengan seed tetap, jadi hasilnya identik tiap kali dijalankan.
"""
import numpy as np, pandas as pd, os

OUT = "/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad/bootcamp/data"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)

# ---------------------------------------------------------------- 1. PRODUK
produk = pd.DataFrame([
    ("P01","Kopi Susu Gula Aren","Minuman Kopi",22000, 9000,"2024-01-01"),
    ("P02","Americano","Minuman Kopi",18000, 6000,"2024-01-01"),
    ("P03","Cappuccino","Minuman Kopi",25000,10000,"2024-01-01"),
    ("P04","Latte","Minuman Kopi",25000,10500,"2024-01-01"),
    ("P05","Espresso","Minuman Kopi",15000, 5000,"2024-01-01"),
    ("P06","Matcha Latte","Minuman Non-Kopi",28000,13000,"2024-06-01"),
    ("P07","Cokelat Panas","Minuman Non-Kopi",24000,10000,"2024-01-01"),
    ("P08","Teh Tarik","Minuman Non-Kopi",18000, 6500,"2025-01-15"),
    ("P09","Roti Bakar Cokelat","Makanan",15000, 7000,"2024-01-01"),
    ("P10","Croissant Butter","Makanan",20000,11000,"2024-01-01"),
    ("P11","Nasi Goreng Senja","Makanan",35000,17000,"2024-09-01"),
    ("P12","Pisang Goreng","Makanan",14000, 5500,"2024-01-01"),
    ("P13","Donat Gula","Makanan",12000, 5000,"2025-03-01"),
    ("P14","Kopi Susu Botol 1L","Merchandise",65000,28000,"2025-06-01"),
    ("P15","Tumbler Senja","Merchandise",95000,52000,"2025-06-01"),
], columns=["produk_id","nama_produk","kategori","harga","biaya_modal","tanggal_rilis"])
produk.to_csv(f"{OUT}/produk.csv", index=False)

# ---------------------------------------------------------------- 2. CABANG
cabang = pd.DataFrame([
    ("C01","Senja Menteng","Jakarta","DKI Jakarta","2024-01-01","Rina Kusuma",45),
    ("C02","Senja Kemang","Jakarta","DKI Jakarta","2024-03-15","Bayu Pratama",38),
    ("C03","Senja Dago","Bandung","Jawa Barat","2024-07-01","Dimas Anggara",52),
    ("C04","Senja Darmo","Surabaya","Jawa Timur","2025-02-01","Ayu Lestari",40),
    ("C05","Senja Seturan","Yogyakarta","DI Yogyakarta","2025-08-01","Galih Saputra",35),
    ("C06","Senja Renon","Denpasar","Bali","2026-01-15","Kadek Ari",30),
], columns=["cabang_id","nama_cabang","kota","provinsi","tanggal_buka","manajer","kapasitas_kursi"])
cabang.to_csv(f"{OUT}/cabang.csv", index=False)

# ---------------------------------------------------------------- 3. KALENDER
tgl = pd.date_range("2024-01-01","2026-06-30",freq="D")
libur = {  # hari libur nasional utama (disederhanakan)
 "2024-01-01","2024-02-08","2024-03-11","2024-03-29","2024-04-10","2024-04-11",
 "2024-05-01","2024-05-09","2024-06-17","2024-08-17","2024-12-25",
 "2025-01-01","2025-01-29","2025-03-29","2025-03-31","2025-04-01","2025-05-01",
 "2025-05-29","2025-06-06","2025-08-17","2025-12-25",
 "2026-01-01","2026-02-17","2026-03-19","2026-03-21","2026-03-22","2026-05-01",
 "2026-05-14","2026-05-27","2026-06-01"}
kalender = pd.DataFrame({"tanggal": tgl})
kalender["tahun"] = kalender.tanggal.dt.year
kalender["bulan"] = kalender.tanggal.dt.month
kalender["nama_bulan"] = kalender.tanggal.dt.strftime("%B")
kalender["minggu_ke"] = kalender.tanggal.dt.isocalendar().week.astype(int)
kalender["hari"] = kalender.tanggal.dt.dayofweek.map(
    {0:"Senin",1:"Selasa",2:"Rabu",3:"Kamis",4:"Jumat",5:"Sabtu",6:"Minggu"})
kalender["akhir_pekan"] = kalender.tanggal.dt.dayofweek.isin([5,6])
kalender["hari_libur"] = kalender.tanggal.dt.strftime("%Y-%m-%d").isin(libur)
kalender["kuartal"] = "Q" + kalender.tanggal.dt.quarter.astype(str)
kalender.to_csv(f"{OUT}/kalender.csv", index=False)

# ---------------------------------------------------------------- 4. PELANGGAN
N_PEL = 6200
kota_bobot = {"Jakarta":.42,"Bandung":.20,"Surabaya":.16,"Yogyakarta":.13,"Denpasar":.09}
daftar_awal = pd.Timestamp("2025-01-01")
hari_daftar = rng.integers(0, 540, N_PEL)
kanal = rng.choice(["organik","iklan_meta","iklan_google","referral","gojek_grab"],
                   N_PEL, p=[.30,.24,.16,.14,.16])
pelanggan = pd.DataFrame({
    "pelanggan_id": [f"U{i:05d}" for i in range(1, N_PEL+1)],
    "tanggal_daftar": daftar_awal + pd.to_timedelta(hari_daftar, unit="D"),
    "kota": rng.choice(list(kota_bobot), N_PEL, p=list(kota_bobot.values())),
    "kanal_akuisisi": kanal,
    "tahun_lahir": rng.integers(1975, 2007, N_PEL),
    "jenis_kelamin": rng.choice(["P","L"], N_PEL, p=[.56,.44]),
    "member_premium": rng.random(N_PEL) < 0.18,
})
pelanggan["tanggal_daftar"] = pelanggan.tanggal_daftar.dt.date
pelanggan.to_csv(f"{OUT}/pelanggan.csv", index=False)

print("produk", produk.shape, "| cabang", cabang.shape,
      "| kalender", kalender.shape, "| pelanggan", pelanggan.shape)
