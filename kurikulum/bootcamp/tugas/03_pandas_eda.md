# Tugas 03 — EDA dengan pandas
**Modul:** SQL & pandas, Minggu 5–6 · **Perkiraan waktu:** 8–10 jam
**Berkas keluaran:** `03_eda_kedai.ipynb`

## Konteks
Kamu baru bergabung sebagai analis. Belum ada yang memberi pertanyaan spesifik —
tugasmu justru menemukan apa yang perlu ditanyakan.

## Yang harus dikerjakan
Notebook EDA lengkap dengan urutan baku:

1. **Muat & periksa** — `shape`, `info()`, `isna().sum()`, `duplicated().sum()`,
   `describe()`. Tulis satu paragraf: apakah data ini sehat?
2. **Kualitas data** — periksa hal-hal ini secara eksplisit:
   - Apakah ada transaksi sebelum cabangnya buka?
   - Apakah ada produk terjual sebelum tanggal rilisnya?
   - Apakah `subtotal - diskon` selalu sama dengan `total`?
   - Apakah ada `pelanggan_id` di transaksi yang tidak ada di tabel pelanggan?
3. **Sebaran tiap kolom penting** — histogram `total`, bar `kategori`, dsb.
4. **Tren waktu** — omzet bulanan, dengan pemisahan per cabang.
5. **Hubungan** — apakah jumlah item berkorelasi dengan nilai transaksi?
   Apakah pola jam berbeda antar saluran?
6. **Lima temuan** — format: apa + angka + artinya buat bisnis.
7. **Tiga pertanyaan lanjutan** yang muncul dari temuanmu, beserta data apa yang
   dibutuhkan untuk menjawabnya.

## Syarat
- Minimal 6 grafik, tiap judul menyatakan **temuan**, bukan nama kolom.
- Semua grafik nilai uang bersumbu mulai dari nol.
- Ada sel Markdown penjelasan di antara sel-sel kode — notebook harus bisa dibaca
  seperti laporan, bukan seperti coretan.
- `Restart and run all` berjalan bersih tanpa error.

## Petunjuk untuk bagian 2
Empat pemeriksaan itu bukan formalitas. Setidaknya satu di antaranya akan
menghasilkan temuan yang mengejutkan. Kalau semuanya bersih, periksa lagi cara
kamu memeriksanya.
