# Tugas 08 — Product Analytics
**Waktu:** 12–15 jam · **Keluaran:** `08_kesehatan_bisnis.ipynb`
**Data:** `keanggotaan_bulanan.csv` + `pelanggan.csv` + `transaksi.csv`

## Yang harus dikerjakan
1. **Matriks kohor retensi.** ⚠️ Penyebutnya adalah jumlah **pendaftar** dari tabel
   `pelanggan`, bukan jumlah yang bertransaksi di bulan 0. Kalau kamu salah pilih
   penyebut, retensimu bisa melebihi 100% — dan itu mustahil.
2. **Activation rate.** Berapa persen pendaftar yang pernah bertransaksi sama sekali?
   Kenapa angkanya jauh di bawah 100%?
3. Peta panas retensi dengan skala warna tetap (`vmin`/`vmax`)
4. Kurva retensi rata-rata. Di bulan ke berapa melandai?
5. **Segmentasi:** temukan sendiri kelompok pelanggan dengan retensi sangat berbeda.
   Baru **setelah** itu, bandingkan dengan kolom `tipe_pelanggan`. Seberapa dekat tebakanmu?
6. Retensi per `kanal_akuisisi`. Kanal mana yang menghasilkan pelanggan terbaik?
7. LTV kotor dan bersih (margin dari `produk.biaya_modal`)
8. Tabel LTV/CAC untuk beberapa skenario CAC + waktu balik modal
9. Peramalan 28 hari `omzet_harian.csv` dengan **4 metode pembanding** + tabel MAPE
10. Enam bagian laporan: keadaan, retensi, segmentasi, ekonomi unit, ramalan, rekomendasi

## Yang gagal otomatis
- Retensi di atas 100% (salah penyebut)
- Melaporkan LTV kotor sebagai LTV
- Ramalan tanpa pembanding metode sederhana
- Rekomendasi belanja iklan tanpa menghitung LTV/CAC
