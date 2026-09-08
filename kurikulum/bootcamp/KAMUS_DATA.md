# Kamus Data — Kedai Kopi Senja

Semua modul bootcamp memakai data ini. Satu perusahaan, satu konteks, dua belas bulan.

## Cerita perusahaannya

Kedai Kopi Senja mulai dari satu gerai di Menteng, Januari 2024. Sampai Juni 2026
sudah punya 6 cabang di 5 kota. Aplikasi keanggotaan diluncurkan Januari 2025 —
sebelum itu tidak ada data pelanggan sama sekali. Layanan antar mulai serius
sejak 2025.

Tiga fakta itu menjelaskan banyak keanehan yang akan kamu temukan di data,
dan kamu memang diharapkan menemukannya sendiri.

---

## Ringkasan berkas

| Berkas | Baris | Isi |
|---|---:|---|
| `transaksi.csv` | 151.088 | Satu baris = satu struk |
| `transaksi_item.csv` | 278.303 | Satu baris = satu produk dalam struk |
| `pelanggan.csv` | 6.200 | Member aplikasi |
| `produk.csv` | 15 | Daftar produk + biaya modal |
| `cabang.csv` | 6 | Gerai |
| `kalender.csv` | 912 | Dimensi tanggal + hari libur nasional |
| `omzet_harian.csv` | 912 | Ringkasan harian (untuk peramalan) |
| `keanggotaan_bulanan.csv` | 10.200 | Aktivitas member per bulan (untuk kohor) |
| `abtest_checkout.csv` | 8.000 | Hasil eksperimen A/B |
| `churn_features.csv` | 5.000 | Fitur perilaku + label churn |
| `transaksi_kotor.csv` | 2.650 | Versi berantakan, khusus latihan pembersihan |

---

## transaksi.csv

| Kolom | Tipe | Keterangan |
|---|---|---|
| `transaksi_id` | teks | Kunci utama, format `T0000001` |
| `tanggal` | tanggal | 2024-01-01 s/d 2026-06-30 |
| `jam` | bilangan | 7–21, jam transaksi |
| `cabang_id` | teks | Mengacu ke `cabang.cabang_id` |
| `pelanggan_id` | teks | Mengacu ke `pelanggan.pelanggan_id`. **Kosong untuk non-member** |
| `saluran` | teks | Dine-in, Takeaway, Delivery |
| `metode_bayar` | teks | QRIS, Kartu Debit, Tunai, E-Wallet |
| `subtotal` | bilangan | Sebelum diskon, rupiah |
| `diskon` | bilangan | Potongan, rupiah |
| `total` | bilangan | `subtotal - diskon`, yang benar-benar dibayar |

**Yang perlu diwaspadai:** 62,8% transaksi tidak punya `pelanggan_id`. Itu bukan
data rusak — sepanjang 2024 aplikasinya memang belum ada, dan setelah itu banyak
pembeli tidak memakai aplikasi. Kalau kamu memakai INNER JOIN ke `pelanggan`,
kamu diam-diam membuang lebih dari separuh omzet. Ini jebakan yang disengaja.

## transaksi_item.csv

| Kolom | Tipe | Keterangan |
|---|---|---|
| `transaksi_id` | teks | Mengacu ke `transaksi` |
| `produk_id` | teks | Mengacu ke `produk` |
| `jumlah` | bilangan | Porsi |
| `harga_satuan` | bilangan | Harga saat transaksi |
| `nilai` | bilangan | `jumlah × harga_satuan` |

**Rekonsiliasi wajib:** `SUM(nilai)` per transaksi harus sama persis dengan
`transaksi.subtotal`. Kalau JOIN-mu menggandakan baris, uji ini akan gagal —
dan itulah gunanya.

## pelanggan.csv

| Kolom | Keterangan |
|---|---|
| `pelanggan_id` | Kunci utama, `U00001` |
| `tanggal_daftar` | 2025-01-01 s/d 2026-06-24 |
| `kota` | Kota domisili |
| `kanal_akuisisi` | organik, iklan_meta, iklan_google, referral, gojek_grab |
| `tahun_lahir` | 1975–2006 |
| `jenis_kelamin` | P / L |
| `member_premium` | Berbayar atau tidak |
| `tipe_pelanggan` | setia / biasa — **jangan dipakai sebagai fitur model.** Ini label internal untuk memeriksa jawabanmu di modul segmentasi |

**Catatan penting:** hanya 3.973 dari 6.200 member yang pernah bertransaksi.
Sisanya mendaftar lalu tidak pernah membeli. Selisih itu adalah *activation rate*,
dan itu metrik nyata, bukan kesalahan data.

## produk.csv

Berisi `biaya_modal` — kolom yang membuat perhitungan **laba** mungkin dilakukan.
Tanpa JOIN ke tabel ini, kamu hanya bisa menghitung omzet. Perhatikan juga
`tanggal_rilis`: beberapa produk baru ada di tengah periode.

## kalender.csv

Tabel dimensi tanggal, lengkap dengan `hari_libur` (hari libur nasional Indonesia,
disederhanakan). Berguna untuk memisahkan pengaruh hari libur dari tren asli —
sesuatu yang tidak bisa kamu lakukan tanpa tabel ini.

## transaksi_kotor.csv

Sengaja dirusak dengan delapan jenis masalah yang benar-benar terjadi di ekspor
sistem kasir:

1. Tanggal tiga format berbeda (`2026-01-15`, `15/01/2026`, `15-Jan-2026`)
2. Huruf besar-kecil tidak konsisten (`Jakarta`, `JAKARTA`, `jakarta`)
3. Spasi berlebih di awal/akhir teks
4. Singkatan tidak seragam (`JKT` untuk Jakarta, `dine in` vs `DINE-IN`)
5. Nilai kosong pada `total`, `kota`, `metode_bayar`
6. Angka disimpan sebagai teks berformat rupiah (`Rp 61.000`)
7. Nilai mustahil: total negatif dan nol
8. Baris duplikat penuh, dan 30 baris kosong melompong

Jumlah baris bersih yang seharusnya kamu dapat ada di kunci jawaban Tugas 04.

---

## Peringatan yang jujur

Data ini **dibuat oleh program**, bukan data perusahaan sungguhan. Polanya
sengaja dirancang supaya bisa ditemukan: pengaruh akhir pekan, pertumbuhan,
perbedaan kanal akuisisi, penurunan retensi. Data nyata jauh lebih berisik dan
sering tidak punya pola sama sekali.

Karena itu, **kerjakan minimal satu proyek dengan data terbuka sungguhan**
sebelum lulus — data.go.id, data.jakarta.go.id, BPS, atau data.gov.sg kalau
targetmu Singapura. Itu syarat kelulusan, bukan saran.
