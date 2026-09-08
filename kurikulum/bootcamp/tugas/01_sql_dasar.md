# Tugas 01 — SQL Dasar
**Modul:** SQL & pandas, Minggu 1–2 · **Perkiraan waktu:** 6–8 jam
**Berkas keluaran:** `01_sql_dasar.sql`

## Konteks
Manajer operasional Kedai Kopi Senja belum pernah melihat angkanya sendiri.
Dia minta jawaban atas beberapa pertanyaan dasar sebelum rapat bulanan.

## Yang harus dikerjakan
Tulis satu berkas `.sql` berisi 12 query. Format tiap query:

```sql
-- Pertanyaan 1: [tulis ulang pertanyaannya]
SELECT ...;
-- Jawaban: [tulis hasilnya di sini setelah dijalankan]
```

### Pertanyaan
1. Berapa total transaksi sepanjang 2025?
2. Berapa omzet per cabang di 2025, urut dari terbesar?
3. Cabang mana yang rata-rata nilai transaksinya tertinggi? Apakah sama dengan
   cabang beromzet terbesar? Jelaskan bedanya dalam komentar.
4. Berapa transaksi per metode bayar, dan berapa persen masing-masing?
5. Jam berapa paling ramai? Tampilkan 5 jam teratas dengan jumlah transaksinya.
6. Berapa omzet per saluran (Dine-in/Takeaway/Delivery) per tahun?
7. Hari apa dalam seminggu yang paling ramai? (butuh JOIN ke `kalender`)
8. Berapa rata-rata diskon yang diberikan, dan berapa persen transaksi yang
   mendapat diskon?
9. Berapa transaksi yang terjadi di hari libur nasional? Berapa rata-rata
   omzet hari libur dibanding hari biasa?
10. Cabang mana yang paling bergantung pada Delivery? (persentase, bukan jumlah)
11. Berapa transaksi yang tidak punya `pelanggan_id`? Berapa persen? Jelaskan
    dalam komentar kenapa angkanya setinggi itu.
12. Bandingkan omzet Q1 2025 vs Q1 2026. Berapa persen pertumbuhannya?

## Syarat
- Semua query berjalan berurutan dari atas ke bawah tanpa error.
- Setiap query memakai alias kolom yang jelas (`AS omzet`, bukan hasil tanpa nama).
- Tidak ada `SELECT *` kecuali untuk melihat contoh data.
- Pertanyaan 3 dan 11 wajib punya komentar penjelasan, bukan hanya angka.

## Kesalahan yang akan diperiksa
- Menghitung `COUNT(*)` padahal yang diminta `COUNT(DISTINCT ...)`
- Lupa menyaring tahun sehingga jawabannya mencakup seluruh periode
- Pembagian bilangan bulat yang membuat persentase jadi 0 (pakai `100.0`, bukan `100`)
