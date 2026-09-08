# Tugas 05 — Statistik & A/B Testing
**Waktu:** 8–10 jam · **Keluaran:** `05_abtest.ipynb`
**Data:** `abtest_checkout.csv`

Aplikasi Kedai Senja menguji halaman checkout baru. Tim pemasaran sudah bersorak
melihat konversi naik. Tugasmu memastikan sorakan itu beralasan.

## Yang harus dikerjakan
1. Ringkasan konversi kedua grup + selisih absolut dan relatif
2. Uji-z dua proporsi **dihitung manual** (jangan pakai pustaka jadi), lalu
   bandingkan dengan `chi2_contingency`
3. Confidence interval 95% untuk selisih konversi
4. Uji-t Welch untuk nilai pesanan **di antara yang membeli saja**
5. Metrik pendapatan per pengunjung — dan uji apakah selisihnya nyata
6. Hitung power eksperimen ini. Cukup atau tidak?
7. Hitung ukuran sampel yang seharusnya untuk MDE 5%, 10%, 15%, 20%
8. Simulasi peeking: berapa false positive kalau dicek 1×, 5×, 20×?
9. Grafik: batang konversi **dengan error bar**, histogram nilai pesanan bertumpuk
10. Laporan keputusan enam bagian

## Yang gagal otomatis
- Merekomendasikan "luncurkan" hanya karena p < 0,05 pada metrik konversi,
  tanpa memeriksa metrik uang
- Grafik konversi tanpa error bar
- Menulis "ada 96,7% kemungkinan fitur ini lebih baik"

## Petunjuk
Ketiga metrik tidak akan sepakat. Itu disengaja. Keputusan yang benar bukan
"luncurkan" atau "buang".
