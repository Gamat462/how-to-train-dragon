# -*- coding: utf-8 -*-
"""Semua SQL yang muncul di modul SQL Mahir L2 — PostgreSQL 16."""
KUERI = {

# ---------------- Hari 1: apa yang dikerjakan OVER ----------------
"h1_sambung": "SELECT count(*) AS pesanan FROM pesanan",
"h1_group_by": """
SELECT cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai_cabang
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai' GROUP BY cabang ORDER BY cabang""",
"h1_window": """
SELECT o.id, o.cabang,
       i.jumlah * i.harga_saat_itu AS nilai_baris,
       sum(i.jumlah * i.harga_saat_itu) OVER (PARTITION BY o.cabang) AS nilai_cabang,
       round(i.jumlah * i.harga_saat_itu * 100.0 /
             sum(i.jumlah * i.harga_saat_itu) OVER (PARTITION BY o.cabang), 3) AS persen
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai' ORDER BY o.cabang, o.id LIMIT 6""",
"h1_merah_window_where": """
SELECT cabang FROM pesanan WHERE row_number() OVER (ORDER BY id) = 1""",
"h1_merah_window_group": """
SELECT cabang, count(*) FROM pesanan GROUP BY cabang HAVING row_number() OVER () = 1""",
"h1_over_kosong": """
SELECT o.cabang, i.jumlah * i.harga_saat_itu AS nilai_baris,
       sum(i.jumlah * i.harga_saat_itu) OVER () AS semua_cabang
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai' ORDER BY o.cabang, o.id LIMIT 3""",
"h1_order_by_diam": """
WITH b AS (SELECT to_char(o.tanggal,'YYYY-MM') AS bulan,
                  sum(i.jumlah * i.harga_saat_itu) AS nilai
           FROM pesanan o JOIN item i ON i.pesanan_id = o.id
           WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
       sum(nilai) OVER ()               AS tanpa_order_by,
       sum(nilai) OVER (ORDER BY bulan) AS pakai_order_by
FROM b ORDER BY bulan""",
"h1_kunci": """
WITH b AS (SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
                  sum(i.jumlah * i.harga_saat_itu) AS nilai
           FROM pesanan o JOIN item i ON i.pesanan_id = o.id
           WHERE o.status='selesai' GROUP BY 1,2)
SELECT cabang, bulan, nilai,
       round(nilai * 100.0 / sum(nilai) OVER (PARTITION BY bulan), 1) AS persen_bulan
FROM b WHERE bulan = '2024-01' ORDER BY cabang""",

# ---------------- Hari 2: ROWS lawan RANGE ----------------
"h2_kecil": """
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai,
  sum(nilai) OVER (ORDER BY nilai
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS pakai_rows,
  sum(nilai) OVER (ORDER BY nilai
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS pakai_range
FROM t ORDER BY nilai, nama""",
"h2_tanpa_frame": """
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai, sum(nilai) OVER (ORDER BY nilai) AS tanpa_frame
FROM t ORDER BY nilai, nama""",
"h2_groups": """
WITH t(nama, nilai) AS (VALUES ('a',10),('b',20),('c',20),('d',30))
SELECT nama, nilai,
  sum(nilai) OVER (ORDER BY nilai GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS pakai_groups
FROM t ORDER BY nilai, nama""",
"h2_sungguhan": """
WITH harian AS (
  SELECT o.tanggal, o.cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-05'
  GROUP BY o.tanggal, o.cabang)
SELECT tanggal, cabang, nilai,
  sum(nilai) OVER (ORDER BY tanggal
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_rows,
  sum(nilai) OVER (ORDER BY tanggal
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_range
FROM harian ORDER BY tanggal, cabang""",
"h2_rata_bergerak": """
WITH harian AS (
  SELECT o.tanggal, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.tanggal <= DATE '2024-01-12'
  GROUP BY o.tanggal)
SELECT tanggal, nilai,
  round(avg(nilai) OVER (ORDER BY tanggal
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW))                   AS rata2_7_baris,
  round(avg(nilai) OVER (ORDER BY tanggal
        RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW))  AS rata2_7_hari
FROM harian ORDER BY tanggal""",
"h2_hari_hilang": """
SELECT d::date AS tanggal
FROM generate_series(DATE '2024-01-01', DATE '2024-01-12', INTERVAL '1 day') AS d
WHERE NOT EXISTS (SELECT 1 FROM pesanan o
                  WHERE o.tanggal = d::date AND o.status='selesai')""",
"h2_merah_frame_terbalik": """
WITH t(n) AS (VALUES (10),(20))
SELECT sum(n) OVER (ORDER BY n ROWS BETWEEN CURRENT ROW AND UNBOUNDED PRECEDING) FROM t""",
"h2_merah_range_tanpa_order": """
WITH t(n) AS (VALUES (10),(20))
SELECT sum(n) OVER (RANGE BETWEEN 1 PRECEDING AND CURRENT ROW) FROM t""",
"h2_kunci": """
WITH harian AS (
  SELECT o.tanggal, o.cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-05'
  GROUP BY o.tanggal, o.cabang)
SELECT tanggal, cabang, nilai,
  sum(nilai) OVER (PARTITION BY cabang ORDER BY tanggal
       ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_rows,
  sum(nilai) OVER (PARTITION BY cabang ORDER BY tanggal
       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kum_range
FROM harian ORDER BY cabang, tanggal""",

# ---------------- Hari 3: LAG, LEAD, LAST_VALUE ----------------
"h3_lag_lead": """
WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  lag(nilai)  OVER (ORDER BY bulan) AS bulan_lalu,
  lead(nilai) OVER (ORDER BY bulan) AS bulan_depan,
  round((nilai - lag(nilai) OVER (ORDER BY bulan)) * 100.0
        / lag(nilai) OVER (ORDER BY bulan), 1) AS tumbuh_persen
FROM b ORDER BY bulan""",
"h3_window_clause": """
WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  lag(nilai) OVER w AS bulan_lalu,
  round((nilai - lag(nilai) OVER w) * 100.0 / lag(nilai) OVER w, 1) AS tumbuh_persen
FROM b
WINDOW w AS (ORDER BY bulan)
ORDER BY bulan""",
"h3_lag_default": """
WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan, nilai,
  lag(nilai, 1)    OVER (ORDER BY bulan) AS satu_bulan_lalu,
  lag(nilai, 2)    OVER (ORDER BY bulan) AS dua_bulan_lalu,
  lag(nilai, 1, 0) OVER (ORDER BY bulan) AS dengan_bawaan_nol
FROM b ORDER BY bulan LIMIT 4""",
"h3_coalesce_teks": """
WITH b AS (
  SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY 1)
SELECT bulan,
  COALESCE(round((nilai - lag(nilai) OVER w) * 100.0 / lag(nilai) OVER w, 1)::text,
           'tidak ada pembanding') AS tumbuh
FROM b WINDOW w AS (ORDER BY bulan) ORDER BY bulan LIMIT 3""",
"h3_merah_lag_tanpa_over": """
SELECT bulan, lag(nilai) FROM
 (SELECT to_char(tanggal,'YYYY-MM') AS bulan, count(*) AS nilai FROM pesanan GROUP BY 1) x""",
"h3_last_value": """
SELECT nama, harga,
  first_value(harga) OVER (ORDER BY harga) AS first_v,
  last_value(harga)  OVER (ORDER BY harga) AS last_v_tanpa_frame,
  last_value(harga)  OVER (ORDER BY harga
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_v_dengan_frame
FROM produk ORDER BY harga""",
"h3_first_value_dibalik": """
SELECT nama, harga, first_value(harga) OVER (ORDER BY harga DESC) AS termahal
FROM produk ORDER BY harga LIMIT 3""",
"h3_nth_value": """
SELECT nama, harga,
  nth_value(nama, 2) OVER (ORDER BY harga DESC
      ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS termahal_kedua
FROM produk ORDER BY harga DESC LIMIT 3""",
"h3_kunci": """
SELECT nama, kategori, harga,
  first_value(nama) OVER (PARTITION BY kategori ORDER BY harga)      AS termurah,
  first_value(nama) OVER (PARTITION BY kategori ORDER BY harga DESC) AS termahal
FROM produk ORDER BY kategori, harga""",

# ---------------- Hari 4: peringkat, kuartil, persentil, median ----------------
"h4_tiga_peringkat": """
WITH t(nama, nilai) AS (VALUES ('a',30),('b',20),('c',20),('d',10))
SELECT nama, nilai,
  row_number() OVER (ORDER BY nilai DESC) AS row_number,
  rank()       OVER (ORDER BY nilai DESC) AS rank,
  dense_rank() OVER (ORDER BY nilai DESC) AS dense_rank
FROM t ORDER BY nilai DESC, nama""",
"h4_ntile": """
WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id)
SELECT p.nama, b.belanja,
  ntile(4)      OVER (ORDER BY b.belanja DESC)      AS kuartil,
  rank()        OVER (ORDER BY b.belanja DESC)      AS peringkat,
  round(percent_rank() OVER (ORDER BY b.belanja)::numeric, 2) AS persentil
FROM b JOIN pelanggan p ON p.id = b.pelanggan_id
ORDER BY b.belanja DESC""",
"h4_anggota_kuartil": """
WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id),
k AS (SELECT ntile(4) OVER (ORDER BY belanja DESC) AS kuartil FROM b)
SELECT kuartil, count(*) AS anggota FROM k GROUP BY kuartil ORDER BY kuartil""",
"h4_median": """
WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id)
SELECT round(avg(belanja))                                            AS rata_rata,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY belanja)           AS median,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY belanja)           AS median_baris_nyata,
       percentile_cont(0.9) WITHIN GROUP (ORDER BY belanja)           AS persentil_90
FROM b""",
"h4_merah_median": """
SELECT median(harga) FROM produk""",
"h4_case_when": """
WITH b AS (
  SELECT o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.pelanggan_id)
SELECT CASE WHEN belanja >= 2000000 THEN 'di atas 2 juta'
            ELSE 'di bawah 2 juta' END AS kelompok, count(*) AS orang
FROM b GROUP BY 1 ORDER BY 1""",
"h4_merah_ntile": "SELECT ntile() OVER (ORDER BY harga) FROM produk",
"h4_dedup": """
SELECT * FROM (
  SELECT o.pelanggan_id, o.id, o.tanggal,
         row_number() OVER (PARTITION BY o.pelanggan_id
                            ORDER BY o.tanggal DESC, o.id DESC) AS n
  FROM pesanan o WHERE o.pelanggan_id IS NOT NULL) x
WHERE n = 1 ORDER BY pelanggan_id LIMIT 5""",
"h4_kunci": """
WITH b AS (
  SELECT o.cabang, o.pelanggan_id, sum(i.jumlah * i.harga_saat_itu) AS belanja
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' AND o.pelanggan_id IS NOT NULL
  GROUP BY o.cabang, o.pelanggan_id)
SELECT cabang, nama, belanja, peringkat FROM (
  SELECT b.cabang, p.nama, b.belanja,
         dense_rank() OVER (PARTITION BY b.cabang ORDER BY b.belanja DESC) AS peringkat
  FROM b JOIN pelanggan p ON p.id = b.pelanggan_id) x
WHERE peringkat <= 2 ORDER BY cabang, peringkat""",

# ---------------- Hari 5: recursive CTE ----------------
"h5_pohon": """
WITH RECURSIVE pohon AS (
  SELECT id, nama, jabatan, id_atasan, 1 AS tingkat, nama AS jalur
  FROM pegawai WHERE id_atasan IS NULL
  UNION ALL
  SELECT p.id, p.nama, p.jabatan, p.id_atasan,
         t.tingkat + 1, t.jalur || ' > ' || p.nama
  FROM pegawai p JOIN pohon t ON p.id_atasan = t.id)
SELECT tingkat, nama, jabatan, jalur FROM pohon ORDER BY jalur""",
"h5_merah_tanpa_recursive": """
WITH pohon AS (
  SELECT id, nama FROM pegawai WHERE id_atasan IS NULL
  UNION ALL
  SELECT p.id, p.nama FROM pegawai p JOIN pohon t ON p.id_atasan = t.id)
SELECT * FROM pohon""",
"h5_bawahan": """
WITH RECURSIVE bawahan AS (
  SELECT id, nama, 0 AS jarak FROM pegawai WHERE id = 2
  UNION ALL
  SELECT p.id, p.nama, b.jarak + 1
  FROM pegawai p JOIN bawahan b ON p.id_atasan = b.id)
SELECT nama, jarak FROM bawahan WHERE jarak > 0 ORDER BY jarak, nama""",
"h5_batas": """
WITH RECURSIVE pohon AS (
  SELECT id, nama, 1 AS tingkat FROM pegawai WHERE id_atasan IS NULL
  UNION ALL
  SELECT p.id, p.nama, t.tingkat + 1
  FROM pegawai p JOIN pohon t ON p.id_atasan = t.id
  WHERE t.tingkat < 10)
SELECT max(tingkat) AS tingkat_terdalam, count(*) AS baris FROM pohon""",
"h5_cycle": """
WITH RECURSIVE lingkar(a, b) AS (VALUES (1,2),(2,3),(3,1)),
jalan AS (
  SELECT a, b FROM lingkar WHERE a = 1
  UNION ALL
  SELECT l.a, l.b FROM lingkar l JOIN jalan j ON l.a = j.b)
CYCLE a SET terulang USING jejak
SELECT a, b, terulang FROM jalan""",
"h5_rantai": """
WITH RECURSIVE rantai AS (
  SELECT id, nama, 0 AS jarak FROM pelanggan WHERE id = 1
  UNION ALL
  SELECT p.id, p.nama, r.jarak + 1
  FROM pelanggan p JOIN rantai r ON p.id_perujuk = r.id
  WHERE r.jarak < 10)
SELECT nama, jarak FROM rantai WHERE jarak > 0 ORDER BY jarak, nama""",
"h5_kunci": """
WITH RECURSIVE rantai AS (
  SELECT id, nama, 0 AS jarak, nama AS jalur FROM pelanggan WHERE id_perujuk IS NULL
  UNION ALL
  SELECT p.id, p.nama, r.jarak + 1, r.jalur || ' > ' || p.nama
  FROM pelanggan p JOIN rantai r ON p.id_perujuk = r.id
  WHERE r.jarak < 10)
SELECT jarak, count(*) AS orang FROM rantai GROUP BY jarak ORDER BY jarak""",

# ---------------- Hari 6: kerangka waktu + LATERAL ----------------
"h6_kerangka_2d": """
SELECT d::date AS tanggal, c.cabang,
       COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
FROM generate_series(DATE '2024-01-01', DATE '2024-01-03', INTERVAL '1 day') AS d
CROSS JOIN (SELECT DISTINCT cabang FROM pesanan) c
LEFT JOIN pesanan o ON o.tanggal = d::date AND o.cabang = c.cabang AND o.status='selesai'
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY d, c.cabang ORDER BY d, c.cabang""",
"h6_kumulatif_per_cabang": """
WITH lengkap AS (
  SELECT d::date AS tanggal, c.cabang,
         COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
  FROM generate_series(DATE '2024-01-01', DATE '2024-01-05', INTERVAL '1 day') AS d
  CROSS JOIN (SELECT DISTINCT cabang FROM pesanan) c
  LEFT JOIN pesanan o ON o.tanggal = d::date AND o.cabang = c.cabang AND o.status='selesai'
  LEFT JOIN item i ON i.pesanan_id = o.id
  GROUP BY d, c.cabang)
SELECT tanggal, cabang, nilai,
       sum(nilai) OVER (PARTITION BY cabang ORDER BY tanggal
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
FROM lengkap ORDER BY cabang, tanggal LIMIT 10""",
"h6_lateral": """
SELECT c.cabang, t.nama, t.terjual
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN LATERAL (
  SELECT p.nama, sum(i.jumlah) AS terjual
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  JOIN produk p ON p.id = i.produk_id
  WHERE o.cabang = c.cabang AND o.status = 'selesai'
  GROUP BY p.nama ORDER BY sum(i.jumlah) DESC, p.nama LIMIT 2) t
ORDER BY c.cabang, t.terjual DESC""",
"h6_lateral_vs_window": """
SELECT cabang, nama, terjual FROM (
  SELECT o.cabang, p.nama, sum(i.jumlah) AS terjual,
         row_number() OVER (PARTITION BY o.cabang
                            ORDER BY sum(i.jumlah) DESC, p.nama) AS n
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  JOIN produk p ON p.id = i.produk_id
  WHERE o.status = 'selesai'
  GROUP BY o.cabang, p.nama) x
WHERE n <= 2 ORDER BY cabang, terjual DESC""",
"h6_merah_lateral": """
SELECT c.cabang, t.nama
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN (
  SELECT p.nama FROM produk p WHERE p.id = length(c.cabang) LIMIT 1) t""",
"h6_gap_hari": """
WITH hari AS (
  SELECT DISTINCT tanggal FROM pesanan WHERE status='selesai'
    AND tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-31')
SELECT tanggal, lead(tanggal) OVER (ORDER BY tanggal) AS berikutnya,
       lead(tanggal) OVER (ORDER BY tanggal) - tanggal AS jeda_hari
FROM hari
ORDER BY jeda_hari DESC NULLS LAST, tanggal
LIMIT 5""",
"h6_kunci": """
WITH lengkap AS (
  SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
  FROM generate_series(DATE '2024-01-01', DATE '2024-01-31', INTERVAL '1 day') AS d
  LEFT JOIN pesanan o ON o.tanggal = d::date AND o.status='selesai'
  LEFT JOIN item i ON i.pesanan_id = o.id
  GROUP BY d)
SELECT count(*) AS hari_kalender,
       count(*) FILTER (WHERE nilai = 0) AS hari_tanpa_transaksi,
       round(avg(nilai))                          AS rata2_semua_hari,
       round(avg(nilai) FILTER (WHERE nilai > 0)) AS rata2_hari_jualan
FROM lengkap""",

# ---------------- Hari 7: ulangan + terapan ----------------
"h7_terapan_benar": """
WITH bulanan AS (
  SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
         sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.cabang, 2)
SELECT cabang, bulan, nilai,
  lag(nilai) OVER w AS bulan_lalu,
  round((nilai - lag(nilai) OVER w) * 100.0 / lag(nilai) OVER w, 1) AS tumbuh,
  sum(nilai) OVER (PARTITION BY cabang ORDER BY bulan
       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
FROM bulanan
WINDOW w AS (PARTITION BY cabang ORDER BY bulan)
ORDER BY cabang, bulan LIMIT 6""",
"h7_terapan_lupa_partition": """
WITH bulanan AS (
  SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
         sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.cabang, 2)
SELECT cabang, bulan, nilai,
  lag(nilai) OVER (ORDER BY cabang, bulan) AS bulan_lalu,
  sum(nilai) OVER (ORDER BY cabang, bulan
       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS kumulatif
FROM bulanan ORDER BY cabang, bulan LIMIT 8""",
"h7_periksa": """
WITH bulanan AS (
  SELECT o.cabang, to_char(o.tanggal,'YYYY-MM') AS bulan,
         sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status='selesai' GROUP BY o.cabang, 2)
SELECT cabang, sum(nilai) AS total_cabang FROM bulanan GROUP BY cabang ORDER BY cabang""",

# ---------------- langkah pemanasan: lihat bahannya dulu ----------------
"h1_lihat_bulan": """
SELECT to_char(tanggal,'YYYY-MM') AS bulan, count(*) AS pesanan
FROM pesanan WHERE status='selesai' GROUP BY 1 ORDER BY 1""",
"h2_cek_seri": """
SELECT tanggal, count(*) AS baris
FROM (SELECT DISTINCT tanggal, cabang FROM pesanan
      WHERE status='selesai' AND tanggal <= DATE '2024-01-05') x
GROUP BY tanggal HAVING count(*) > 1 ORDER BY tanggal""",
"h3_produk_urut": "SELECT nama, harga FROM produk ORDER BY harga",
"h4_jumlah_pelanggan": """
SELECT count(DISTINCT pelanggan_id) AS pelanggan_pernah_belanja
FROM pesanan WHERE status='selesai' AND pelanggan_id IS NOT NULL""",
"h5_pegawai": "SELECT id, nama, id_atasan FROM pegawai ORDER BY id",
"h6_cabang": "SELECT DISTINCT cabang FROM pesanan ORDER BY 1",
"h6_hari_jualan": """
SELECT count(DISTINCT tanggal) AS hari_ada_jualan
FROM pesanan WHERE status='selesai' AND tanggal <= DATE '2024-01-31'""",
"h7_jumlah_baris": """
SELECT count(*) AS baris FROM (
  SELECT cabang, to_char(tanggal,'YYYY-MM') FROM pesanan
  WHERE status='selesai' GROUP BY 1,2) x""",

# ---------------- isi CTE, dilihat sendiri sebelum dipakai ----------------
"h1_cte_bulanan": """
SELECT to_char(o.tanggal,'YYYY-MM') AS bulan, sum(i.jumlah * i.harga_saat_itu) AS nilai
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status='selesai' GROUP BY 1 ORDER BY 1""",
"h2_cte_harian": """
SELECT o.tanggal, o.cabang, sum(i.jumlah * i.harga_saat_itu) AS nilai
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-05'
GROUP BY o.tanggal, o.cabang ORDER BY o.tanggal, o.cabang""",
"h4_cte_belanja": """
SELECT p.nama, sum(i.jumlah * i.harga_saat_itu) AS belanja
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
JOIN pelanggan p ON p.id = o.pelanggan_id
WHERE o.status='selesai' GROUP BY p.nama ORDER BY belanja DESC LIMIT 5""",
"h6_cte_lengkap": """
SELECT count(*) AS baris_kerangka
FROM generate_series(DATE '2024-01-01', DATE '2024-01-05', INTERVAL '1 day') AS d
CROSS JOIN (SELECT DISTINCT cabang FROM pesanan) c""",
"h3_termahal": "SELECT max(harga) AS termahal, min(harga) AS termurah FROM produk",
"h5_akar": "SELECT count(*) AS tanpa_atasan FROM pegawai WHERE id_atasan IS NULL",
"h6_rentang": "SELECT min(tanggal) AS awal, max(tanggal) AS akhir FROM pesanan",
"h7_selesai": "SELECT count(*) AS pesanan_selesai FROM pesanan WHERE status = 'selesai'",
"h4_pesanan_per_orang": """
SELECT round(avg(n), 1) AS rata2_pesanan_per_pelanggan FROM (
  SELECT pelanggan_id, count(*) AS n FROM pesanan
  WHERE status='selesai' AND pelanggan_id IS NOT NULL GROUP BY 1) x""",
"h1_item_semua": "SELECT sum(jumlah * harga_saat_itu) AS semua_item FROM item",
"h4_ntile_kecil": "SELECT nama, harga, ntile(3) OVER (ORDER BY harga) AS kelompok FROM produk",
"h5_siapa": "SELECT id, nama, jabatan FROM pegawai WHERE id = 2",
"h7_to_char": "SELECT to_char(DATE '2024-03-05', 'YYYY-MM') AS bulan",
}
