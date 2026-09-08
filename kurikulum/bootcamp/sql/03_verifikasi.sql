-- ============================================================
-- Jalankan ini setelah memuat data. Kalau ada angka yang tidak
-- cocok, ada yang salah pada proses muat — perbaiki dulu sebelum
-- mengerjakan tugas apa pun.
-- ============================================================

SELECT 'produk'         AS tabel, COUNT(*) AS baris, 15     AS seharusnya FROM produk
UNION ALL SELECT 'cabang',         COUNT(*), 6      FROM cabang
UNION ALL SELECT 'pelanggan',      COUNT(*), 6200   FROM pelanggan
UNION ALL SELECT 'kalender',       COUNT(*), 912    FROM kalender
UNION ALL SELECT 'transaksi',      COUNT(*), 151088 FROM transaksi
UNION ALL SELECT 'transaksi_item', COUNT(*), 278303 FROM transaksi_item;

-- Total omzet seharusnya 8.567.304.450
SELECT SUM(total) AS total_omzet FROM transaksi;

-- Tanggal seharusnya 2024-01-01 s/d 2026-06-30
SELECT MIN(tanggal) AS mulai, MAX(tanggal) AS selesai FROM transaksi;

-- Uji keutuhan: tiap transaksi harus punya minimal satu item
SELECT COUNT(*) AS transaksi_tanpa_item
FROM transaksi t
LEFT JOIN transaksi_item i ON t.transaksi_id = i.transaksi_id
WHERE i.transaksi_id IS NULL;      -- seharusnya 0

-- Uji rekonsiliasi: subtotal harus sama dengan jumlah nilai item
SELECT COUNT(*) AS subtotal_tidak_cocok
FROM (
    SELECT t.transaksi_id, t.subtotal, SUM(i.nilai) AS jumlah_item
    FROM transaksi t
    JOIN transaksi_item i ON t.transaksi_id = i.transaksi_id
    GROUP BY t.transaksi_id, t.subtotal
) x
WHERE subtotal <> jumlah_item;     -- seharusnya 0
