# Jalur Spesialisasi: Analitik Data Migas

## Kenapa jalur ini

Kombinasi **audit/keuangan + migas + analitik data** langka dan mahal. Di Indonesia
pemberi kerjanya: Pertamina Hulu Energi, Medco, PetroChina, Premier Oil, SKK Migas,
dan KAP yang mengaudit cost recovery PSC. Di Australia: sektor LNG (Woodside,
Santos) sangat besar. Di Singapura: pusat perdagangan minyak dunia.

Latar belakang auditmu bukan penghambat di sini — ini justru keunggulan. Sebagian
besar pekerjaan analis migas hulu adalah **rekonsiliasi, alokasi biaya, dan
verifikasi volume**. Itu pekerjaan audit dengan data yang jauh lebih besar.

## Blok Cendana — perusahaan tempat kamu bekerja

PSC fiktif dengan skema cost recovery. 4 lapangan, 64 sumur, data harian
Januari 2023 – Juni 2026.

| Lapangan | Tipe | Onstream | Sumur | Ciri |
|---|---|---|---|---|
| F01 Cendana Utara | Onshore | 1998 | 22 | Tua, watercut tinggi (82% di 2026) |
| F02 Cendana Selatan | Onshore | 2005 | 18 | Menengah |
| F03 Meranti | Offshore | 2012 | 14 | Karbonat, produktif |
| F04 Gaharu | Offshore | 2019 | 10 | Termuda, decline tercepat |

**Angka kunci yang harus kamu ketahui di luar kepala** (dipakai untuk memeriksa
apakah analisismu masuk akal):

- Total produksi 2023–Jun 2026: **20.079.135 bbl**
- Produksi 2025: **5.641.070 bbl**
- Lifting cost: **$14,35/bbl**
- Government take: **70,5%** dari gross revenue
- Uptime: **98,1%**
- Watercut naik 29% (2023) → 70% (2026)

Kalau hasil hitunganmu jauh dari angka-angka ini, ada yang salah — periksa dulu
sebelum lanjut.

## Fisika yang perlu kamu pahami secukupnya

Kamu tidak perlu jadi petroleum engineer. Empat hal ini cukup:

1. **Produksi selalu menurun.** Sumur minyak mengikuti kurva decline. Persamaan
   Arps: `q(t) = qi / (1 + b·D·t)^(1/b)`. Kalau `b=0` jadi eksponensial murni.
2. **Watercut naik seiring waktu.** Reservoir makin lama makin banyak
   mengeluarkan air. Di atas ~95% sumur biasanya tidak ekonomis lagi.
3. **Workover menaikkan produksi sementara,** lalu meluruh kembali. Ini
   menghancurkan kurva decline — dan itu jebakan utama di Level 5.
4. **Downtime mengurangi produksi tanpa mengubah kemampuan sumur.** Bedakan
   "sumur lemah" dari "sumur mati sementara".

## Istilah yang akan sering muncul

| Istilah | Arti |
|---|---|
| **bopd / bwpd** | barrel oil (water) per day |
| **mscfd** | thousand standard cubic feet per day (gas) |
| **Watercut** | proporsi air dalam cairan yang keluar |
| **GOR** | Gas Oil Ratio, scf gas per bbl minyak |
| **Uptime** | % waktu sumur benar-benar berproduksi |
| **Lifting cost** | biaya operasi per barel yang diangkat |
| **ICP** | Indonesian Crude Price, acuan harga bulanan |
| **Lifting** | pengangkatan/penjualan kargo minyak |
| **EUR** | Estimated Ultimate Recovery, total yang bisa diambil seumur sumur |
| **DCA** | Decline Curve Analysis |
| **PSC** | Production Sharing Contract |
| **FTP** | First Tranche Petroleum, potongan di awal sebelum cost recovery |
| **Cost recovery** | pengembalian biaya kontraktor dari hasil produksi |
| **ETS** | Equity To Be Split, sisa yang dibagi pemerintah–kontraktor |
| **DMO** | Domestic Market Obligation, kewajiban jual domestik di bawah harga |
| **Government take** | total bagian negara (FTP + ETS + pajak) |
| **LTI** | Lost Time Injury, kecelakaan yang menyebabkan hari kerja hilang |
