-- ============================================================
-- Bootcamp Data Analyst — Kedai Kopi Senja
-- Skema database. Jalankan ini SEBELUM memuat data.
--
-- SQLite  : buka sqliteonline.com, tempel seluruh isi file ini, Run.
-- Postgres: psql -d kedai -f 01_buat_skema.sql
-- ============================================================

DROP TABLE IF EXISTS transaksi_item;
DROP TABLE IF EXISTS transaksi;
DROP TABLE IF EXISTS pelanggan;
DROP TABLE IF EXISTS produk;
DROP TABLE IF EXISTS cabang;
DROP TABLE IF EXISTS kalender;

CREATE TABLE produk (
    produk_id       TEXT PRIMARY KEY,
    nama_produk     TEXT NOT NULL,
    kategori        TEXT NOT NULL,
    harga           INTEGER NOT NULL,
    biaya_modal     INTEGER NOT NULL,
    tanggal_rilis   DATE NOT NULL
);

CREATE TABLE cabang (
    cabang_id       TEXT PRIMARY KEY,
    nama_cabang     TEXT NOT NULL,
    kota            TEXT NOT NULL,
    provinsi        TEXT NOT NULL,
    tanggal_buka    DATE NOT NULL,
    manajer         TEXT,
    kapasitas_kursi INTEGER
);

CREATE TABLE pelanggan (
    pelanggan_id    TEXT PRIMARY KEY,
    tanggal_daftar  DATE NOT NULL,
    kota            TEXT,
    kanal_akuisisi  TEXT,
    tahun_lahir     INTEGER,
    jenis_kelamin   TEXT,
    member_premium  BOOLEAN,
    tipe_pelanggan  TEXT
);

CREATE TABLE kalender (
    tanggal      DATE PRIMARY KEY,
    tahun        INTEGER,
    bulan        INTEGER,
    nama_bulan   TEXT,
    minggu_ke    INTEGER,
    hari         TEXT,
    akhir_pekan  BOOLEAN,
    hari_libur   BOOLEAN,
    kuartal      TEXT
);

CREATE TABLE transaksi (
    transaksi_id  TEXT PRIMARY KEY,
    tanggal       DATE NOT NULL,
    jam           INTEGER,
    cabang_id     TEXT REFERENCES cabang(cabang_id),
    pelanggan_id  TEXT REFERENCES pelanggan(pelanggan_id),   -- NULL = non-member
    saluran       TEXT,
    metode_bayar  TEXT,
    subtotal      INTEGER,
    diskon        INTEGER,
    total         INTEGER
);

CREATE TABLE transaksi_item (
    transaksi_id  TEXT REFERENCES transaksi(transaksi_id),
    produk_id     TEXT REFERENCES produk(produk_id),
    jumlah        INTEGER,
    harga_satuan  INTEGER,
    nilai         INTEGER
);

-- Index dibuat SETELAH data dimuat (lihat 03_index.sql).
-- Ini disengaja: kamu akan mengukur sendiri pengaruhnya di Modul Analytics Engineering.
