# Kunci Jawaban Migas

**Semua angka di bawah ini dihasilkan dengan menjalankan query/kode pada dataset
yang kamu punya.** Kalau hasilmu berbeda, ada langkah yang keliru — bukan
kuncinya yang salah. Selisih pembulatan kecil wajar.

Jangan buka sebelum mencoba minimal 20 menit per soal.

---

## LEVEL 1

| Soal | Jawaban |
|---|---|
| L1.1 | **5.641.070 bbl** |
| L1.2 | Producer **59**, Injector **5** |
| L1.3 | F04 2.422.737 · F03 1.545.966 · F01 927.487 · F02 744.879 |
| L1.4 | CDN-059 (1.506.316) · CDN-057 (1.473.298) · CDN-062 (1.186.553) · CDN-063 (1.007.919) · CDN-049 (863.017) |
| L1.5 | **1.349 hari-sumur** |
| L1.6 | Near Miss 43 · First Aid 20 · Medical Treatment 13 · Spill 8 · LTI 5 · Fire 2 |
| L1.7 | 2023 $67,72 · 2024 $65,64 · 2025 $62,91 · 2026 $69,93 |
| L1.8 | OPEX **$288.049.861** · CAPEX **$100.800.990** |
| L1.9 | ESP 29 · Gas Lift 14 · Sucker Rod 11 · Natural Flow 10 |
| L1.10 | Domestik 78 kargo / 12.788.674 bbl / $823.196.781 · Ekspor 44 kargo / 6.864.737 bbl / $446.298.578 |
| L1.11 | Pump Failure 102 kejadian/225 hari · Power Outage 60/113 · Weather 42/98 · Sand Production 39/89 · Facility Shutdown 48/87 · Flowline Leak 38/78 |
| L1.12 | Acidizing 24/$18,36 jt · ESP Replacement 17/$15,52 jt · Reperforation 17/$14,88 jt · Scale Removal 15/$12,84 jt · Zone Change 6/$5,35 jt |

**Catatan L1.11:** Pump Failure paling sering *dan* paling banyak memakan hari.
Ini petunjuk awal untuk L4.8 — dan memang di sana terbukti paling mahal.

---

## LEVEL 2

**L2.1** Cendana Selatan: 710.540 (2023) → 781.297 (2024) → 744.879 (2025) → 336.751 (Jan–Jun 2026).
Cendana Utara: 798.587 → 901.463 → 927.487 → …
⚠️ **2026 hanya 6 bulan.** Membandingkannya langsung dengan tahun penuh adalah kesalahan.

**L2.2** Watercut naik konsisten di semua lapangan. F01: 46,6% → 61,5% → 72,7% → **81,5%**.
F02: 31,1% → 45,1% → … F01 paling basah. Artinya: biaya angkat air makin besar,
umur ekonomis makin dekat, dan kandidat utama untuk program pengelolaan air.

**L2.3** Uptime 2025: F01 97,93% · F02 97,97% · F04 98,63% · F03 98,97%.
Selisihnya kecil tapi pada volume F04 yang besar, 1% berarti puluhan ribu barel.

**L2.4** **Lifting cost 2025:** F03 $14,69 · F04 $14,65 · F01 $14,29 · F02 $14,18 per bbl.
Cukup seragam. Perhatikan bahwa lapangan offshore tidak otomatis lebih mahal per
barel karena volumenya juga jauh lebih besar.

**L2.5** Banyak sumur F01 sudah mencapai batas 96%: CDN-001 (190,9 bopd),
CDN-005 (45,4), CDN-006 (99,0), CDN-007 (36,1), CDN-008 (111,7), CDN-010 (96,8), dst.

**L2.6** Berat terbanyak: **F03 Meranti (3)** dari 29 insiden · F04 (2) dari 23 ·
F01 (1) dari 16 · F02 (1) dari 23.

**L2.7** 2026-01: 416.170 bbl × $69,42 = $28,89 jt · 2026-02: 366.181 × $63,07 = $23,10 jt · dst.

**L2.8** Pernah workover: rata-rata produksi lebih tinggi. ⚠️ **Ini BUKAN bukti workover
berhasil.** Sumur besar lebih layak di-workover, jadi arah sebabnya bisa terbalik
(*selection bias*). Cara yang benar ada di L4.4: bandingkan sumur yang sama
sebelum vs sesudah.

**L2.9** Sejumlah kecil sumur produser tanpa catatan downtime. Jawaban tergantung
implementasi anti-join-mu; yang dinilai adalah kamu memakai `LEFT JOIN ... IS NULL`
atau `NOT EXISTS`, bukan `NOT IN` (yang berbahaya bila ada NULL).

**L2.10** **Selisih lifting vs produksi ada di kisaran ±3% per tahun.** Ini normal,
bukan kesalahan: ada stok di tangki, ada perbedaan waktu antara produksi dan
pengangkatan kargo, dan ada susut. Yang tidak normal adalah selisih > 5% atau
selisih yang selalu searah — itu tanda masalah pengukuran.

**L2.11** Biaya per unit kenaikan paling murah: Acidizing. ESP Replacement paling mahal
per unit karena biayanya tinggi dan kenaikannya paling kecil.

**L2.12** Jumlah LTI kecil (5 total) — sebaran per tahun bervariasi. Dengan angka
sekecil ini, **jangan menarik tren.** Satu kejadian tambahan mengubah persentase
secara dramatis. Ini pelajaran statistik yang penting.

---

## LEVEL 3

**L3.1** F04 menunjukkan decline paling curam dari semua lapangan (sumur termuda,
`D` tinggi). Pertumbuhan bulanan sering negatif.

**L3.2** Tiga teratas 2025 per lapangan — semua sumur bernomor tinggi (CDN-057
sampai CDN-064) berada di F04/F03, sesuai desain: lapangan baru = sumur produktif.

**L3.3** Kumulatif F01 naik mulus. Gunanya: melihat kapan lapangan mencapai
tonggak produksi tertentu.

**L3.4 (Pareto)** Di F01, sekitar **8–10 sumur dari 20 menyumbang 80% produksi**.
Implikasi manajemen: perhatian dan anggaran perawatan harus mengikuti pola ini,
bukan dibagi rata.

**L3.5** MA-30 perlu karena data harian sangat berisik (derau 5,5% + downtime acak).
Tanpa perataan, kamu akan salah mengira fluktuasi harian sebagai perubahan tren.

**L3.6** Decline paling curam ada di sumur F04. Bandingkan dengan L4.7 — sebagian
adalah decline alami, sebagian anomali. Membedakan keduanya adalah intinya.

**L3.7** Hari produksi terendah tiap bulan biasanya bertepatan dengan downtime
besar. Cocokkan dengan tabel `downtime` untuk membuktikannya.

**L3.8 (jawaban penting)** Pangsa 2023 → 2025:
F04 36,9% → **42,9%** (+6,0) · F01 13,3% → 16,4% (+3,1) · F02 11,8% → 13,2% (+1,4) ·
**F03 38,0% → 27,4% (−10,6)**.
F03 menyusut paling tajam. Penjelasannya: F03 lapangan karbonat yang decline-nya
lebih cepat dari perkiraan, sementara F04 masih dalam fase awal.

---

## LEVEL 4

**L4.1** Selisih **≈ $0,00** (di bawah 1 sen) untuk semua bulan. Tabel PSC memang
konsisten dengan data produksi. Dalam audit sungguhan, temuan "tidak ada selisih"
tetap harus dilaporkan — dan cara kamu membuktikannya yang dinilai.

**L4.2** Selisih **≈ ±0,01 USD** (murni pembulatan) untuk semua 42 bulan.
Identitas `gross = FTP + cost recovery + ETS` terbukti utuh.

**L4.3** Government take **72–73%** saat ICP tinggi ($76,30 → 72,64%), dan turun saat
ICP rendah. Cost recovery bergerak **berlawanan** (19–20% saat harga tinggi, lebih
tinggi saat harga rendah). Sebabnya: biaya nominalnya tetap, jadi saat harga naik
biaya itu jadi porsi yang lebih kecil dan sisanya masuk ETS yang dibagi 85:15.

**L4.4 (jawaban kunci)** Kenaikan produksi 30 hari sesudah vs sebelum:

| Jenis | n | Sebelum | Sesudah | Gain | Biaya rata² |
|---|---:|---:|---:|---:|---:|
| Reperforation | 17 | 346,2 | 461,6 | **+115,4** | $875.289 |
| Scale Removal | 15 | 323,8 | 421,6 | +97,8 | $856.015 |
| Zone Change | 6 | 244,4 | 331,4 | +86,9 | $892.324 |
| Acidizing | 24 | 273,8 | 358,9 | +85,1 | $764.856 |
| ESP Replacement | 17 | 256,5 | 317,8 | +61,3 | $913.189 |

⚠️ Angka "sesudah" ini diukur 30 hari pertama. Efeknya **meluruh** — jadi jangan
mengalikan gain ini dengan 365 untuk menghitung manfaat setahun. Itu kesalahan
yang akan membuat NPV-mu terlalu optimistis.

**L4.5** Payback tercepat: WO-0066 Scale Removal **13 hari** ($280.786, +331,0 bopd,
ICP $64,41). Disusul WO-0073 Reperforation 17 hari, WO-0076 Acidizing 19 hari.
Payback di bawah 60 hari umumnya sangat layak.

**L4.6** Dengan pembagian biaya lapangan secara rata per sumur, **tidak ada sumur
yang merugi** pada harga ~$69. Yang paling tipis: CDN-011 (27,3 bopd, margin
+$10.753/bulan). ⚠️ Kesimpulan ini **sangat bergantung pada cara membagi biaya** —
lihat L5.3.

**L4.7** Anomali terbesar: **CDN-060 (F04)** turun 36,8% sementara rata-rata
lapangannya 21,7% — selisih **15,1 poin persen**. Disusul CDN-013 (F01, −13,6),
CDN-001 (−12,5), CDN-017 (−10,4), CDN-053 (−10,4).
Inilah daftar kandidat intervensi untuk L5.5.

**L4.8 (jawaban kunci)** Nilai produksi hilang:

| Penyebab | Kejadian | Hari | bbl hilang | Nilai USD |
|---|---:|---:|---:|---:|
| Pump Failure | 102 | 225 | 63.343 | **$4.253.473** |
| Power Outage | 60 | 113 | 36.615 | $2.374.051 |
| Facility Shutdown | 48 | 87 | 31.588 | $2.138.411 |
| Weather | 42 | 98 | 26.208 | $1.720.907 |
| Flowline Leak | 38 | 78 | 19.711 | $1.326.094 |
| Sand Production | 39 | 89 | 18.973 | $1.288.621 |

**Total ≈ $13,1 juta.** Pump Failure sendirian $4,25 juta — bandingkan dengan biaya
program perawatan pompa sebelum menyimpulkan apa yang harus dilakukan.

---

## LEVEL 5

### L5.1 — Decline Curve Analysis

**Tahap A (fit mentah):** R² rata-rata hanya **0,701**, minimum **−0,047**.
Beberapa sumur memberi sisa cadangan mustahil (CDN-060: 4,9 juta bbl, umur mentok
360 bulan) karena fit runtuh ke `D = 0,010` (batas bawah) — artinya "hampir tidak
menurun", lalu diekstrapolasi selamanya.

**Tahap B (diagnosis):** penyebabnya **workover**. Kenaikan produksi pasca-workover
membuat kurva terlihat naik-turun, dan Arps tidak bisa mencocokkannya.

**Tahap C (segmen bersih):** buang data sampai **270 hari sesudah workover terakhir**,
minimal **14 bulan** data tersisa, tolak fit dengan R² < 0,5.
Hasil: **26 sumur lolos, 33 ditolak** (semua karena segmen terlalu pendek).
R² rata-rata naik jadi **0,995** (min 0,976). Sisa cadangan **21.562.234 bbl**.

**Tahap D (masalah tersisa):** **12 dari 26 sumur mentok di batas 480 bulan.**
Sebabnya `b` mendekati 1,2. Pada Arps, `b ≥ 1` membuat integral cadangan
**divergen** — secara matematis cadangannya tak terhingga. Ini jebakan nyata yang
menghasilkan laporan cadangan terlalu optimistis di dunia industri.

**Tahap E (praktik industri):** batasi `b ≤ 1,0`, lalu beralih ke eksponensial
saat laju decline sesaat `D/(1+bDt)` turun di bawah **8%/tahun**.

Hasil akhir:
- **26 sumur lolos**, R² rata-rata **0,995** (min 0,973)
- **0 sumur** mentok batas proyeksi
- Umur sisa: median **285 bulan**, maksimum 532 bulan
- **8 sumur** menyentuh batas `b = 1,0` (tanpa batasan akan lebih tinggi)
- **EUR total 27.412.621 bbl** · sisa cadangan **17.627.474 bbl** · pengurasan **35,7%**
- **Selisih dari Tahap C: 3.934.760 bbl lebih rendah (−18,2%)**

Sisa cadangan per lapangan: F03 7.267.911 · F04 6.690.653 · F02 2.211.133 · F01 1.457.777.

**Uji kejujuran model:** korelasi `qi` hasil fit dengan nilai asli **0,867**,
korelasi `D` hanya **0,579**. Artinya model menangkap tingkat produksi awal dengan
baik tapi laju decline hanya sedang. **Sebutkan keterbatasan ini di laporanmu** —
itu yang membedakan analis jujur dari yang menjual angka.

### L5.2 — Batas ekonomis

Biaya operasi per sumur per bulan: F01 $55.227 · F02 $51.791 · F03 $145.551 · F04 $328.570.

Economic limit rate:

| Harga | F01 | F02 | F03 | F04 |
|---|---:|---:|---:|---:|
| $50/bbl | 36,3 | 34,0 | 95,6 | 215,9 bopd |
| $65/bbl | 27,9 | 26,2 | 73,6 | 166,1 bopd |
| $80/bbl | 22,7 | 21,3 | 59,8 | 134,9 bopd |

Pada $65/bbl, **1 sumur dari 59 di bawah batas**: CDN-011 (27,3 bopd vs batas 27,9).

⚠️ Asumsi yang harus kamu nyatakan: biaya lapangan dibagi **rata** per sumur.
Itu hampir pasti salah — sumur besar memakan biaya kimia dan penanganan air lebih
banyak. Dengan pembagian berbasis volume, hasilnya bisa terbalik.

### L5.3 — Alokasi G&A (soal paling mirip pekerjaan audit)

Total G&A 2025 yang dialokasikan: **$8.128.457**.

| Lapangan | Per volume | Per sumur | Per hari aktif | Selisih maks |
|---|---:|---:|---:|---:|
| F01 | 1.336.455 | 2.755.409 | 2.745.716 | 1.418.954 |
| F02 | 1.073.328 | 2.342.098 | 2.334.761 | 1.268.770 |
| F03 | 2.227.649 | 1.791.016 | 1.803.593 | 436.633 |
| F04 | **3.491.025** | **1.239.934** | 1.244.387 | **2.251.091** |

**Selisih terbesar $2.251.091 di F04 — 27,7% dari seluruh G&A.**

Jawaban atas "metode mana yang paling adil": **tidak ada jawaban teknis.**
Per volume menguntungkan lapangan tua bervolume kecil; per sumur menguntungkan
lapangan besar bersumur sedikit. Dalam PSC, pilihan ini menentukan berapa biaya
yang bisa di-*cost recover*, jadi ini **keputusan negosiasi dan kebijakan**, bukan
keputusan statistik. Tugas analis adalah menunjukkan besarnya dampak tiap pilihan,
bukan berpura-pura ada satu jawaban benar.

### L5.4 — Sensitivitas PSC

| Skenario | Gross | Cost recovery | Gov take | Kontraktor | Gov % |
|---|---:|---:|---:|---:|---:|
| −30% | 926.080.723 | 289.729.877 | 556.967.115 | 369.113.609 | **60,1%** |
| −15% | 1.124.526.593 | 289.729.877 | 733.187.047 | 391.339.546 | 65,2% |
| dasar | 1.322.972.462 | 289.729.877 | 909.406.979 | 413.565.483 | 68,7% |
| +15% | 1.521.418.331 | 289.729.877 | 1.085.626.911 | 435.791.421 | 71,4% |
| +30% | 1.719.864.201 | 289.729.877 | 1.261.846.843 | 458.017.358 | **73,4%** |

**Kenapa government take naik saat harga naik:** cost recovery nominalnya tetap
($289,7 jt di semua skenario), karena biaya tidak berubah oleh harga minyak.
Setiap dolar tambahan dari kenaikan harga karena itu hampir seluruhnya masuk ETS,
yang dibagi 85:15 untuk pemerintah.

**Artinya bagi kontraktor saat harga jatuh:** porsinya justru naik secara persentase
(39,9% pada −30%), tapi **nilai absolutnya turun**. Skema ini melindungi kontraktor
dari kehancuran saat harga rendah, dan membatasi keuntungannya saat harga tinggi.
Memahami asimetri ini adalah inti analisis ekonomi PSC.

### L5.5 — Proyek akhir

Tidak ada kunci jawaban. Yang dinilai:

1. Kandidatmu berasal dari bukti (L4.7 + L5.1), bukan dari intuisi
2. Perkiraan kenaikan memakai data workover historis **sejenis** (L4.4), dan
   memperhitungkan bahwa efeknya meluruh
3. Ada tiga skenario harga, bukan satu angka tunggal
4. Risiko dan asumsi ditulis terbuka
5. Memo bisa dipahami manajer tanpa istilah statistik

Kalau memo-mu menyebut "R²" atau "hiperbolik", tulis ulang.
