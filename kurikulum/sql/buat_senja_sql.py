# -*- coding: utf-8 -*-
"""Membuat sql/senja.sql (PostgreSQL) dari senja.db yang dibangun gen_final.py.

Datanya sengaja dipertahankan sama persis dengan versi SQLite, supaya seluruh
angka di modul SQL Mahir L1-L5 tetap cocok setelah pindah mesin.

    python3 gen_final.py          # membuat senja.db (SQLite)
    python3 buat_senja_sql.py     # membuat senja.sql (PostgreSQL)
"""
import sqlite3, pathlib

SKEMA = """-- senja.sql — basis data latihan jalur SQL Mahir (PostgreSQL 12+)
-- Jalankan sekali di database kosong bernama senja.
DROP TABLE IF EXISTS item, pesanan, kunjungan, pesanan_kasir, pelanggan, produk, pegawai;

CREATE TABLE pelanggan (
  id             integer PRIMARY KEY,
  nama           text,
  kota           text,
  tanggal_daftar date,
  id_perujuk     integer
);
CREATE TABLE produk (
  id         integer PRIMARY KEY,
  nama       text,
  kategori   text,
  harga      integer,
  harga_beli integer
);
CREATE TABLE pegawai (
  id        integer PRIMARY KEY,
  nama      text,
  jabatan   text,
  cabang    text,
  id_atasan integer,
  gaji      integer
);
CREATE TABLE pesanan (
  id           integer PRIMARY KEY,
  pelanggan_id integer,
  tanggal      date,
  cabang       text,
  kanal        text,
  status       text
);
CREATE TABLE item (
  id             integer PRIMARY KEY,
  pesanan_id     integer,
  produk_id      integer,
  jumlah         integer,
  harga_saat_itu integer
);
CREATE TABLE kunjungan (
  id           integer PRIMARY KEY,
  pelanggan_id integer,
  waktu        timestamp
);
CREATE TABLE pesanan_kasir (
  id      integer PRIMARY KEY,
  tanggal date,
  cabang  text,
  nilai   integer
);
"""

def lit(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"

def main():
    di_sini = pathlib.Path(__file__).parent
    con = sqlite3.connect(di_sini / "senja.db")
    out = [SKEMA]
    for t in ["pelanggan", "produk", "pegawai", "pesanan", "item", "kunjungan", "pesanan_kasir"]:
        kol = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
        baris = con.execute(f"SELECT * FROM {t} ORDER BY id").fetchall()
        out.append(f"\n-- {t}: {len(baris)} baris")
        out.append(f"INSERT INTO {t} ({', '.join(kol)}) VALUES")
        out.append(",\n".join("  (" + ", ".join(lit(v) for v in r) + ")" for r in baris) + ";")
    (di_sini / "senja.sql").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("ditulis: senja.sql")

if __name__ == "__main__":
    main()
