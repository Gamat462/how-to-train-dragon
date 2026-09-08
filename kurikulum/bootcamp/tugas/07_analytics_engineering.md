# Tugas 07 — Analytics Engineering
**Waktu:** 20–25 jam · **Keluaran:** repositori dbt + GitHub Actions

## Bagian A — Optimasi query
1. Muat data ke SQLite/Postgres **tanpa index**. Ukur waktu 5 query berat.
2. Jalankan `EXPLAIN`. Catat mana yang Seq Scan.
3. Jalankan `sql/04_index.sql`. Ukur ulang. Buat tabel sebelum-sesudah.
4. Tulis satu query yang tetap lambat walau sudah ada index, dan jelaskan kenapa.

## Bagian B — Proyek dbt
Tiga lapis: staging (bersihkan) → intermediate (gabung, hitung laba) → mart.
Minimal 6 model, semua punya deskripsi.

**Test wajib (minimal 10):**
- `unique` + `not_null` pada semua kunci utama
- `relationships` dari `transaksi.cabang_id` ke `cabang`
- `accepted_values` pada `saluran` dan `metode_bayar`
- **Satu test rekonsiliasi buatan sendiri:** `SUM(transaksi_item.nilai)` per transaksi
  harus sama dengan `transaksi.subtotal`. Ini test paling berharga di seluruh proyek.

## Bagian C — Otomasi
GitHub Actions yang menjalankan `dbt build` terjadwal. Lencana status di README.

## Syarat
- `dbt build` hijau dari nol di folder baru hasil clone
- Tangkapan layar lineage graph di README
- Tidak ada kredensial di repositori (periksa seluruh riwayat, bukan hanya kondisi terakhir)
