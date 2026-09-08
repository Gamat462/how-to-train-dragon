# Bootcamp Data Analyst — Paket Lengkap

Kurikulum belajar mandiri 12 bulan, plus jalur spesialisasi migas.
Semua data, tugas, rubrik, dan kunci jawaban ada di dalam paket ini.

## Mulai dari mana

```
1. Baca  KAMUS_DATA.md            — kenali datanya dulu
2. Baca  tugas/00_RUBRIK.md       — pahami cara menilai diri sendiri
3. Salin PROGRESS.md              — ini catatan kemajuanmu
4. Jalankan notebooks/00_mulai_di_sini.py  — pastikan data terbaca
5. Mulai tugas/01_sql_dasar.md
```

## Isi paket

```
bootcamp/
├── README.md                  ← kamu di sini
├── KAMUS_DATA.md              ← penjelasan tiap kolom + jebakan yang disengaja
├── SYARAT_KELULUSAN.md        ← definisi "siap melamar"
├── PROGRESS.md                ← catatan kemajuan, isi sendiri
│
├── data/                      ← 11 berkas CSV, ±17 MB
│   ├── transaksi.csv                (151.088 baris)
│   ├── transaksi_item.csv           (278.303 baris)
│   ├── pelanggan.csv                (6.200)
│   ├── produk.csv · cabang.csv · kalender.csv
│   ├── transaksi_kotor.csv          (2.650, sengaja berantakan)
│   ├── abtest_checkout.csv          (8.000)
│   ├── keanggotaan_bulanan.csv      (10.200)
│   ├── churn_features.csv           (5.000)
│   └── omzet_harian.csv             (912)
│
├── sql/                       ← skema, pemuatan, verifikasi, index
├── notebooks/00_mulai_di_sini.py
├── tugas/                     ← 8 tugas + rubrik
│
└── migas/                     ← JALUR SPESIALISASI
    ├── 00_PANDUAN_MIGAS.md
    ├── 01_BANK_SOAL.md        ← 45 soal, 5 tingkat kesulitan
    ├── 02_KUNCI_JAWABAN.md    ← semua angka sudah diverifikasi
    ├── 03_JADWAL_PENGULANGAN.md  ← spaced repetition 12 minggu
    ├── 04_KAMUS_DATA_MIGAS.md
    └── data/                  ← 10 berkas, 70.602 baris produksi harian
```

## Dua jalur

**Jalur inti** (`tugas/`) — SQL, pandas, statistik, visualisasi, analytics
engineering, product analytics. Cocok untuk posisi analis umum.

**Jalur migas** (`migas/`) — analitik hulu migas: kurva decline, rekonsiliasi
volume, alokasi biaya, ekonomi PSC. Cocok kalau kamu berlatar audit/keuangan dan
mengincar Pertamina, Medco, SKK Migas, KAP yang mengaudit cost recovery, atau
sektor LNG Australia.

Boleh dikerjakan paralel. Jalur migas mengandaikan Level SQL dasar sudah lewat.

## Yang perlu dipasang

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn jupyter
# untuk modul lanjutan:
pip install plotly streamlit dbt-postgres sqlalchemy
```

Semua bisa dikerjakan gratis: Google Colab (Python), sqliteonline.com (SQL),
Tableau Public, Streamlit Community Cloud, GitHub.

## Angka pemeriksaan

Kalau hasil hitunganmu berbeda dari ini, ada langkah yang salah:

| Data | Angka |
|---|---|
| Transaksi | 151.088 baris |
| Total omzet | Rp 8.567.304.450 |
| Rentang tanggal | 2024-01-01 s/d 2026-06-30 |
| Transaksi tanpa member | 62,8% |
| Produksi migas total | 20.079.135 bbl |
| Lifting cost | $14,35/bbl |
| Government take | 70,5% |

## Jujur soal keterbatasan

Data ini **dibuat oleh program**. Polanya sengaja dirancang supaya bisa ditemukan.
Data nyata jauh lebih berisik, sering tidak berpola, dan penuh kolom yang tidak
terisi berbulan-bulan.

Karena itu **syarat kelulusan mewajibkan satu proyek dengan data terbuka nyata**.
Tanpa itu, kamu belum benar-benar siap.

Paket ini juga **bukan sertifikat**. Jangan tulis "lulusan bootcamp" di CV.
Tulis proyeknya — itu yang dibaca perekrut.
