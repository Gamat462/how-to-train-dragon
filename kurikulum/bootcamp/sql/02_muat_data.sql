-- ============================================================
-- Memuat data. Pilih salah satu cara sesuai alat yang kamu pakai.
-- ============================================================

-- CARA 1 — sqliteonline.com (paling mudah, tanpa instalasi)
-- Tidak perlu file ini. Pakai tombol "Import" di panel kiri,
-- unggah tiap CSV satu per satu. Pastikan skema sudah dibuat lebih dulu.

-- CARA 2 — SQLite di komputer sendiri
-- Jalankan di terminal, bukan di dalam psql:
--   sqlite3 kedai.db
--   .mode csv
--   .import --skip 1 data/produk.csv produk
--   .import --skip 1 data/cabang.csv cabang
--   .import --skip 1 data/pelanggan.csv pelanggan
--   .import --skip 1 data/kalender.csv kalender
--   .import --skip 1 data/transaksi.csv transaksi
--   .import --skip 1 data/transaksi_item.csv transaksi_item

-- CARA 3 — PostgreSQL
\copy produk         FROM 'data/produk.csv'         WITH (FORMAT csv, HEADER true);
\copy cabang         FROM 'data/cabang.csv'         WITH (FORMAT csv, HEADER true);
\copy pelanggan      FROM 'data/pelanggan.csv'      WITH (FORMAT csv, HEADER true);
\copy kalender       FROM 'data/kalender.csv'       WITH (FORMAT csv, HEADER true);
\copy transaksi      FROM 'data/transaksi.csv'      WITH (FORMAT csv, HEADER true);
\copy transaksi_item FROM 'data/transaksi_item.csv' WITH (FORMAT csv, HEADER true);
