-- pjk_data.sql — data latihan modul Bekal Pajak & ERP (PostgreSQL 12+)
-- Jalankan di database "senja" yang sama seperti SQL Mahir L1-L2.
-- Angka tarif & batas disederhanakan untuk latihan pola SQL — bukan untuk
-- mengisi SPT sungguhan. Selalu rujuk PMK/UU HPP yang berlaku untuk kerja nyata.

DROP TABLE IF EXISTS pjk_wp, pjk_lapisan;

CREATE TABLE pjk_lapisan (
  urutan      int PRIMARY KEY,
  batas_bawah bigint,
  batas_atas  bigint,   -- NULL = tidak terbatas
  tarif       numeric
);
INSERT INTO pjk_lapisan VALUES
  (1,          0,   60000000, 0.05),
  (2,   60000000,  250000000, 0.15),
  (3,  250000000,  500000000, 0.25),
  (4,  500000000, 5000000000, 0.30),
  (5, 5000000000,       NULL, 0.35);

CREATE TABLE pjk_wp (
  id                   serial PRIMARY KEY,
  nama                 text,
  jenis                text,          -- 'perorangan' atau 'umkm'
  penghasilan_tahunan  bigint,
  omzet_tahunan        bigint         -- dipakai khusus utk cek batas UMKM
);
INSERT INTO pjk_wp (nama, jenis, penghasilan_tahunan, omzet_tahunan) VALUES
  ('Rina',   'perorangan',   45000000, NULL),
  ('Bayu',   'perorangan',  180000000, NULL),
  ('Sari',   'perorangan',  620000000, NULL),
  ('Dimas',  'umkm',        150000000,  900000000),
  ('Putri',  'umkm',        410000000, 3200000000),
  ('Agus',   'umkm',        980000000, 5100000000),  -- omzet lewat batas 4,8 M
  ('Maya',   'perorangan', 7200000000, NULL);
