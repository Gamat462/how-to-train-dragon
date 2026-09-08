# Tugas 02 — JOIN, Window Function, dan Laba
**Modul:** SQL & pandas, Minggu 3–4 · **Perkiraan waktu:** 8–10 jam
**Berkas keluaran:** `02_sql_lanjutan.sql`

## Konteks
Pemilik ingin tahu bukan cuma omzet, tapi **laba** — dan omzet tidak ada gunanya
kalau produk yang laku ternyata modalnya mahal. Data laba hanya bisa didapat
dengan menggabungkan tiga tabel.

## Yang harus dikerjakan
14 query. Minimal 5 memakai JOIN tiga tabel, minimal 4 memakai window function,
minimal 2 memakai CTE.

### Pertanyaan
1. Laba per produk sepanjang 2025. Urut dari laba terbesar.
2. Bandingkan peringkat produk berdasarkan **omzet** vs berdasarkan **laba**.
   Produk mana yang peringkatnya paling jauh berbeda? Kenapa?
3. Margin (%) per kategori produk.
4. Produk terlaris (per porsi) di tiap cabang — hanya tampilkan peringkat 1.
5. Tiga produk dengan laba tertinggi di **tiap** kota (window + PARTITION BY).
6. Omzet bulanan dengan kolom tambahan: omzet bulan sebelumnya, dan pertumbuhan
   persennya (LAG).
7. Omzet kumulatif berjalan sepanjang 2025 (SUM OVER).
8. Untuk tiap cabang: omzetnya, rata-rata omzet semua cabang, dan selisihnya.
9. Produk yang belum pernah terjual sama sekali di cabang tertentu
   (petunjuk: butuh LEFT JOIN atau anti-join).
10. Rata-rata jumlah item per transaksi, per saluran.
11. Kontribusi tiap produk terhadap total laba, dalam persen, urut menurun.
    Berapa produk yang menyumbang 80% laba pertama?
12. Untuk tiap cabang, bulan terbaiknya sepanjang sejarah.
13. Bandingkan perilaku member vs non-member: rata-rata nilai transaksi,
    rata-rata jumlah item, dan komposisi salurannya.
14. Produk yang penjualannya turun paling tajam dari 2025 ke semester 1 2026
    (perhatikan: 2026 hanya 6 bulan — jangan bandingkan angka mentah).

## Syarat
- Pertanyaan 14 wajib menangani perbedaan panjang periode. Membandingkan
  6 bulan dengan 12 bulan secara langsung adalah kesalahan yang gagal otomatis.
- Sertakan satu query pemeriksaan di akhir yang membuktikan JOIN-mu tidak
  menggandakan baris (bandingkan `SUM(total)` sebelum dan sesudah JOIN).

## Kesalahan yang akan diperiksa
- INNER JOIN ke `pelanggan` sehingga 62,8% transaksi hilang tanpa disadari
- JOIN ke `transaksi_item` lalu menjumlahkan `transaksi.total` — ini menggandakan
  nilai sebanyak jumlah item. **Ini kesalahan paling sering dan paling mahal.**
- Memakai `DISTINCT` untuk menambal masalah di atas alih-alih memperbaiki JOIN-nya
