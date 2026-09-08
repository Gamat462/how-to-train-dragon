# Kamus Data Migas — Blok Cendana

| Berkas | Baris | Isi |
|---|---:|---|
| `produksi_harian.csv` | 70.602 | Produksi harian per sumur |
| `sumur.csv` | 64 | Master sumur + parameter reservoir |
| `lapangan.csv` | 4 | Master lapangan |
| `downtime.csv` | 329 | Kejadian sumur berhenti |
| `workover.csv` | 79 | Intervensi sumur + biaya |
| `biaya_operasi.csv` | 1.552 | OPEX & CAPEX per lapangan per bulan |
| `lifting.csv` | 122 | Kargo minyak yang diangkat/dijual |
| `harga_icp.csv` | 42 | Harga acuan bulanan |
| `psc_bulanan.csv` | 42 | Perhitungan bagi hasil PSC |
| `hse_insiden.csv` | 91 | Insiden keselamatan |

## produksi_harian.csv
| Kolom | Keterangan |
|---|---|
| `sumur_id` | `CDN-001` … `CDN-064` |
| `tanggal` | Harian, 2023-01-01 s/d 2026-06-30 |
| `oil_bopd` | Minyak, barrel per hari |
| `gas_mscfd` | Gas, thousand standard cubic feet per hari |
| `water_bwpd` | Air, barrel per hari |
| `watercut` | Proporsi air (0–0,96) |
| `berproduksi` | 1 = berproduksi, 0 = mati (downtime/workover) |

⚠️ **Sumur injektor tidak ada di tabel ini** — hanya 59 produser dari 64 sumur.
Kalau kamu menghitung "rata-rata produksi per sumur" dengan pembagi 64, hasilnya salah.

## sumur.csv
Berisi parameter reservoir yang **dipakai membuat data**: `qi_oil_bopd`,
`decline_D_tahunan`, `arps_b`, `watercut_awal`, `kenaikan_watercut_harian`.

⚠️ **Jangan pakai kolom-kolom ini sebagai jawaban di L5.1.** Gunanya hanya untuk
memeriksa seberapa dekat hasil fit-mu dengan kebenaran — persis seperti
membandingkan estimasi dengan hasil audit. Di dunia nyata kolom ini tidak ada.

## psc_bulanan.csv
Perhitungan bagi hasil lengkap. Urutan yang benar:

```
gross_revenue = volume × ICP
FTP           = gross × 20%          → 60% pemerintah, 40% kontraktor
tersedia      = gross − FTP
cost_recovery = min(biaya_recoverable, tersedia, gross × 80%)
ETS           = tersedia − cost_recovery   → 85% pemerintah, 15% kontraktor
DMO           = 25% jatah kontraktor, dihargai 25% ICP → selisihnya jadi kerugian
pajak         = 44% × penghasilan kena pajak kontraktor
```

`unrecovered_carry_usd` = biaya yang belum tertutup, dibawa ke bulan berikutnya.
Ini kolom yang paling sering jadi temuan audit di dunia nyata.

## Kalibrasi yang dipakai
- Lifting cost ≈ **$14,35/bbl** (kisaran nyata Indonesia $12–20)
- Government take ≈ **70,5%** (kisaran nyata PSC minyak 65–75%)
- Uptime **98,1%** (kisaran nyata lapangan terkelola baik 95–99%)

## Peringatan jujur
Data ini **dibuat oleh program** dengan persamaan Arps yang benar, tapi tetap
lebih bersih dan lebih teratur daripada data lapangan sungguhan. Data nyata punya
kolom yang tidak terisi selama berbulan-bulan, alokasi produksi yang diperdebatkan
antar mitra, dan meter yang tidak terkalibrasi.

Karena itu, kalau kamu serius mengejar posisi di migas, **cari juga data terbuka
nyata**: publikasi SKK Migas, laporan tahunan Pertamina, data produksi
Norwegian Petroleum Directorate (sangat lengkap dan gratis), atau data terbuka
Texas Railroad Commission.
