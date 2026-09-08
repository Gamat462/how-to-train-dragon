-- ============================================================
-- JANGAN jalankan ini di awal.
-- File ini dipakai di Modul Analytics Engineering, setelah kamu
-- mengukur sendiri kecepatan query TANPA index lebih dulu.
-- ============================================================
CREATE INDEX idx_trx_tanggal   ON transaksi(tanggal);
CREATE INDEX idx_trx_cabang    ON transaksi(cabang_id);
CREATE INDEX idx_trx_pelanggan ON transaksi(pelanggan_id);
CREATE INDEX idx_item_trx      ON transaksi_item(transaksi_id);
CREATE INDEX idx_item_produk   ON transaksi_item(produk_id);
