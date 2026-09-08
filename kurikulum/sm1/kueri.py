# -*- coding: utf-8 -*-
"""Semua SQL yang muncul di modul SQL Mahir L1 — PostgreSQL 16.

Dijalankan oleh jalankan.py; hasilnya disimpan di hasil.json dan itulah yang
ditulis ke kotak HARUS MUNCUL. Tidak ada keluaran yang diketik tangan.
"""
KUERI = {

# ---------------- Hari 1: pasang, sambung, kenali ----------------
"h1_versi": "SELECT version()",
"h1_hitung_tabel": """
SELECT 'pelanggan' AS tabel, count(*) FROM pelanggan
UNION ALL SELECT 'produk',        count(*) FROM produk
UNION ALL SELECT 'pegawai',       count(*) FROM pegawai
UNION ALL SELECT 'pesanan',       count(*) FROM pesanan
UNION ALL SELECT 'item',          count(*) FROM item
UNION ALL SELECT 'kunjungan',     count(*) FROM kunjungan
UNION ALL SELECT 'pesanan_kasir', count(*) FROM pesanan_kasir""",
"h1_produk": "SELECT * FROM produk ORDER BY id",
"h1_merah_kolom": "SELECT nama FROM pelanggan WHERE kotta IS NULL",
"h1_tiga_nilai": """
SELECT NULL = NULL  AS "NULL=NULL",
       NULL <> NULL AS "NULL<>NULL",
       NULL IS NULL AS "NULL IS NULL",
       1 = 1        AS benar,
       1 = 2        AS salah""",
"h1_tipe_kolom": """
SELECT column_name AS kolom, data_type AS tipe, is_nullable AS boleh_null
FROM information_schema.columns
WHERE table_name = 'produk' ORDER BY ordinal_position""",

# ---------------- Hari 2: NULL ----------------
"h2_sama_null": "SELECT nama, kota FROM pelanggan WHERE kota = NULL",
"h2_is_null":   "SELECT nama, kota FROM pelanggan WHERE kota IS NULL",
"h2_bukan_jkt": "SELECT count(*) AS bukan_jakarta FROM pelanggan WHERE kota <> 'Jakarta'",
"h2_bukan_jkt_lengkap": """
SELECT count(*) AS bukan_jakarta_lengkap FROM pelanggan
WHERE kota <> 'Jakarta' OR kota IS NULL""",
"h2_count": """
SELECT count(*) AS semua, count(kota) AS kota_terisi,
       count(DISTINCT kota) AS kota_unik
FROM pelanggan""",
"h2_avg": """
SELECT count(*) AS produk, count(harga_beli) AS ada_harga_beli,
       round(avg(harga_beli), 1)                     AS avg_abaikan_null,
       round(sum(harga_beli)::numeric / count(*), 1) AS avg_anggap_nol
FROM produk""",
"h2_margin": "SELECT nama, harga - harga_beli AS margin FROM produk ORDER BY id",
"h2_coalesce": """
SELECT nama, COALESCE(kota, 'BELUM TERCATAT') AS kota_tampil
FROM pelanggan WHERE kota IS NULL""",
"h2_urut_null": "SELECT nama, harga_beli FROM produk ORDER BY harga_beli LIMIT 4",
"h2_urut_null_first": """
SELECT nama, harga_beli FROM produk ORDER BY harga_beli NULLS FIRST LIMIT 4""",
"h2_kunci": "SELECT nama, harga, harga_beli FROM produk WHERE harga_beli IS NULL",

# ---------------- Hari 3: NOT IN ----------------
"h3_not_in": "SELECT nama FROM pelanggan WHERE id NOT IN (SELECT pelanggan_id FROM pesanan)",
"h3_not_exists": """
SELECT nama FROM pelanggan p
WHERE NOT EXISTS (SELECT 1 FROM pesanan o WHERE o.pelanggan_id = p.id)
ORDER BY nama""",
"h3_left_join": """
SELECT count(*) AS jumlah FROM pelanggan p
LEFT JOIN pesanan o ON o.pelanggan_id = p.id
WHERE o.id IS NULL""",
"h3_not_in_saring": """
SELECT count(*) AS jumlah FROM pelanggan
WHERE id NOT IN (SELECT pelanggan_id FROM pesanan WHERE pelanggan_id IS NOT NULL)""",
"h3_empat_cara": """
SELECT 'NOT IN' AS cara,
       (SELECT count(*) FROM pelanggan
        WHERE id NOT IN (SELECT pelanggan_id FROM pesanan)) AS hasil
UNION ALL SELECT 'NOT EXISTS',
       (SELECT count(*) FROM pelanggan p
        WHERE NOT EXISTS (SELECT 1 FROM pesanan o WHERE o.pelanggan_id = p.id))
UNION ALL SELECT 'LEFT JOIN IS NULL',
       (SELECT count(*) FROM pelanggan p
        LEFT JOIN pesanan o ON o.pelanggan_id = p.id WHERE o.id IS NULL)
UNION ALL SELECT 'NOT IN + saring NULL',
       (SELECT count(*) FROM pelanggan
        WHERE id NOT IN (SELECT pelanggan_id FROM pesanan WHERE pelanggan_id IS NOT NULL))""",
"h3_tanpa_pid": "SELECT count(*) AS tanpa_pelanggan_id FROM pesanan WHERE pelanggan_id IS NULL",
"h3_kecil": """
SELECT 5 NOT IN (1,2,3)    AS "5 NOT IN (1,2,3)",
       5 NOT IN (1,2,NULL) AS "5 NOT IN (1,2,NULL)" """,
"h3_positif": """
SELECT 5 IN (1,2,NULL) AS "5 IN (1,2,NULL)",
       1 IN (1,2,NULL) AS "1 IN (1,2,NULL)" """,
"h3_merah_dua_kolom": """
SELECT nama FROM pelanggan WHERE id NOT IN (SELECT pelanggan_id, id FROM pesanan)""",
"h3_kunci": """
SELECT nama FROM produk pr
WHERE NOT EXISTS (SELECT 1 FROM item i WHERE i.produk_id = pr.id)""",
"h3_kunci_cek": "SELECT count(*) AS item_tanpa_produk FROM item WHERE produk_id IS NULL",

# ---------------- Hari 4: JOIN ----------------
"h4_merah_ambigu": "SELECT id FROM pelanggan p JOIN pesanan o ON o.pelanggan_id = p.id",
"h4_inner": "SELECT count(*) AS baris FROM pelanggan p JOIN pesanan o ON o.pelanggan_id = p.id",
"h4_left":  "SELECT count(*) AS baris FROM pelanggan p LEFT JOIN pesanan o ON o.pelanggan_id = p.id",
"h4_right": "SELECT count(*) AS baris FROM pelanggan p RIGHT JOIN pesanan o ON o.pelanggan_id = p.id",
"h4_full":  "SELECT count(*) AS baris FROM pelanggan p FULL OUTER JOIN pesanan o ON o.pelanggan_id = p.id",
"h4_cross": "SELECT count(*) AS baris FROM pelanggan CROSS JOIN produk",
"h4_omzet": """
SELECT sum(i.jumlah * i.harga_saat_itu) AS omzet
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai'""",
"h4_omzet_lipat": """
SELECT sum(i.jumlah * i.harga_saat_itu) AS omzet
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
JOIN kunjungan k ON k.pelanggan_id = o.pelanggan_id
WHERE o.status = 'selesai'""",
"h4_baris_lipat": """
SELECT count(*) AS baris
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
JOIN kunjungan k ON k.pelanggan_id = o.pelanggan_id
WHERE o.status = 'selesai'""",
"h4_tanpa_kerangka": """
SELECT count(*) AS baris FROM (
  SELECT o.cabang, i.produk_id
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-14'
  GROUP BY o.cabang, i.produk_id) x""",
"h4_kerangka_nol": """
WITH laku AS (
  SELECT o.cabang, i.produk_id, count(*) AS n
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-14'
  GROUP BY o.cabang, i.produk_id)
SELECT c.cabang, p.nama, COALESCE(l.n, 0) AS terjual
FROM (SELECT DISTINCT cabang FROM pesanan) c
CROSS JOIN produk p
LEFT JOIN laku l ON l.cabang = c.cabang AND l.produk_id = p.id
WHERE COALESCE(l.n, 0) = 0""",

# ---------------- Hari 5: self join ----------------
"h5_kolom": "SELECT id, nama, id_perujuk FROM pelanggan ORDER BY id LIMIT 5",
"h5_merah_alias": """
SELECT nama FROM pelanggan JOIN pelanggan ON pelanggan.id_perujuk = pelanggan.id""",
"h5_perujuk": """
SELECT p.nama AS pelanggan, r.nama AS perujuk
FROM pelanggan p JOIN pelanggan r ON p.id_perujuk = r.id
ORDER BY p.nama""",
"h5_penyebut": """
SELECT count(*) AS semua_pelanggan, count(id_perujuk) AS punya_perujuk FROM pelanggan""",
"h5_hierarki": """
SELECT b.nama, b.jabatan, a.nama AS atasan
FROM pegawai b LEFT JOIN pegawai a ON b.id_atasan = a.id
ORDER BY b.id""",
"h5_inner": "SELECT count(*) AS baris FROM pegawai b JOIN pegawai a ON b.id_atasan = a.id",
"h5_nama_bukan_kunci": """
SELECT pl.nama, pg.jabatan
FROM pelanggan pl JOIN pegawai pg ON pl.nama = pg.nama""",
"h5_antar_bulan": """
WITH bulanan AS (
  SELECT cabang, to_char(tanggal, 'YYYY-MM') AS bulan, count(*) AS pesanan
  FROM pesanan WHERE status = 'selesai' GROUP BY cabang, 2)
SELECT i.bulan, i.pesanan, l.pesanan AS bulan_lalu,
       i.pesanan - l.pesanan AS selisih
FROM bulanan i
LEFT JOIN bulanan l ON l.cabang = i.cabang
     AND l.bulan = to_char(to_date(i.bulan, 'YYYY-MM') - INTERVAL '1 month', 'YYYY-MM')
WHERE i.cabang = 'Kemang' ORDER BY i.bulan""",
"h5_kunci": """
SELECT r.nama AS perujuk, count(*) AS jumlah_dirujuk
FROM pelanggan p JOIN pelanggan r ON p.id_perujuk = r.id
GROUP BY r.nama ORDER BY jumlah_dirujuk DESC, r.nama""",

# ---------------- Hari 6: WHERE/HAVING/urutan ----------------
"h6_where_having": """
SELECT cabang, count(*) AS pesanan
FROM pesanan
WHERE status = 'selesai'
GROUP BY cabang
HAVING count(*) > 100
ORDER BY pesanan DESC""",
"h6_merah_count_where": "SELECT cabang FROM pesanan WHERE count(*) > 100 GROUP BY cabang",
"h6_alias_order_by": """
SELECT cabang, count(*) AS pesanan FROM pesanan
GROUP BY cabang ORDER BY pesanan DESC""",
"h6_merah_alias_where": "SELECT harga*2 AS dobel FROM produk WHERE dobel > 30000",
"h6_tulis_ulang": "SELECT nama, harga*2 AS dobel FROM produk WHERE harga*2 > 30000 ORDER BY harga",
"h6_cte": """
WITH d AS (SELECT nama, harga*2 AS dobel FROM produk)
SELECT * FROM d WHERE dobel > 30000 ORDER BY dobel""",
"h6_merah_order_union": """
SELECT cabang FROM pesanan
UNION ALL SELECT kanal FROM pesanan
ORDER BY status""",
"h6_filter": """
SELECT cabang,
       count(*)                                 AS semua_pesanan,
       count(*) FILTER (WHERE status='selesai') AS selesai,
       count(*) FILTER (WHERE status='batal')   AS batal
FROM pesanan GROUP BY cabang ORDER BY cabang""",
"h6_persen_batal": """
SELECT cabang,
       round(100.0 * count(*) FILTER (WHERE status='batal') / count(*), 1) AS persen_batal
FROM pesanan GROUP BY cabang ORDER BY persen_batal DESC""",
"h6_case_when": """
SELECT cabang, sum(CASE WHEN status='selesai' THEN 1 ELSE 0 END) AS selesai
FROM pesanan GROUP BY cabang ORDER BY cabang""",
"h6_kunci": """
SELECT kanal, count(*) AS semua,
       count(*) FILTER (WHERE status='batal') AS batal
FROM pesanan GROUP BY kanal HAVING count(*) > 120 ORDER BY kanal""",

# ---------------- Hari 7: himpunan & rekonsiliasi ----------------
"h7_union_buang": """
SELECT 'A' AS x, 10000 AS n
UNION     SELECT 'A', 10000
UNION     SELECT 'B', 20000""",
"h7_union_all": """
SELECT 'A' AS x, 10000 AS n
UNION ALL SELECT 'A', 10000
UNION ALL SELECT 'B', 20000""",
"h7_merah_kolom": "SELECT id, nama FROM produk UNION ALL SELECT id FROM pelanggan",
"h7_hitung_cocok": """
WITH buku AS (
  SELECT o.id, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT 'selesai di pembukuan' AS keterangan, count(*) AS jumlah FROM buku
UNION ALL SELECT 'baris di ekspor kasir', count(*) FROM pesanan_kasir
UNION ALL SELECT 'id cocok',
  (SELECT count(*) FROM buku b JOIN pesanan_kasir k ON k.id = b.id)
UNION ALL SELECT 'hanya di pembukuan',
  (SELECT count(*) FROM (SELECT id FROM buku EXCEPT SELECT id FROM pesanan_kasir) x)
UNION ALL SELECT 'hanya di kasir',
  (SELECT count(*) FROM (SELECT id FROM pesanan_kasir EXCEPT SELECT id FROM buku) y)""",
"h7_intersect": """
SELECT count(*) AS id_di_dua_sisi FROM (
  SELECT id FROM pesanan WHERE status = 'selesai'
  INTERSECT SELECT id FROM pesanan_kasir) x""",
"h7_except": """
SELECT 'hanya pembukuan' AS sisi, id FROM (
  SELECT id FROM pesanan WHERE status='selesai'
  EXCEPT SELECT id FROM pesanan_kasir) a
UNION ALL
SELECT 'hanya kasir', id FROM (
  SELECT id FROM pesanan_kasir
  EXCEPT SELECT id FROM pesanan WHERE status='selesai') b
ORDER BY 1 DESC, 2""",
"h7_nilai_beda": """
WITH buku AS (
  SELECT o.id, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT b.id, b.nilai AS pembukuan, k.nilai AS kasir, k.nilai - b.nilai AS selisih
FROM buku b JOIN pesanan_kasir k ON k.id = b.id
WHERE b.nilai <> k.nilai
ORDER BY abs(k.nilai - b.nilai) DESC""",
"h7_tieout": """
WITH buku AS (
  SELECT o.id, sum(i.jumlah * i.harga_saat_itu) AS nilai
  FROM pesanan o JOIN item i ON i.pesanan_id = o.id
  WHERE o.status = 'selesai' GROUP BY o.id)
SELECT 'Total pembukuan' AS keterangan, (SELECT sum(nilai) FROM buku) AS rupiah
UNION ALL SELECT '(-) hanya di pembukuan',
  -(SELECT COALESCE(sum(nilai),0) FROM buku b
     WHERE NOT EXISTS (SELECT 1 FROM pesanan_kasir k WHERE k.id = b.id))
UNION ALL SELECT '(+) hanya di kasir',
  (SELECT COALESCE(sum(nilai),0) FROM pesanan_kasir k
     WHERE NOT EXISTS (SELECT 1 FROM buku b WHERE b.id = k.id))
UNION ALL SELECT '(+/-) selisih nilai id sama',
  (SELECT COALESCE(sum(k.nilai - b.nilai),0)
     FROM buku b JOIN pesanan_kasir k ON k.id = b.id)
UNION ALL SELECT '= Total kasir', (SELECT sum(nilai) FROM pesanan_kasir)""",
"h7_terapan_salah": """
SELECT o.cabang,
       count(*) FILTER (WHERE o.status='selesai')     AS pesanan_selesai,
       count(*) FILTER (WHERE o.status='batal')       AS pesanan_batal,
       count(DISTINCT o.pelanggan_id)                 AS pelanggan_unik,
       sum(CASE WHEN o.status='selesai'
                THEN i.jumlah * i.harga_saat_itu END) AS nilai_selesai
FROM pesanan o
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY o.cabang ORDER BY o.cabang""",
"h7_terapan_benar": """
WITH nilai_per_pesanan AS (
  SELECT o.id, o.cabang, o.status, o.pelanggan_id,
         (SELECT COALESCE(sum(i.jumlah * i.harga_saat_itu), 0)
          FROM item i WHERE i.pesanan_id = o.id) AS nilai
  FROM pesanan o)
SELECT cabang,
       count(*) FILTER (WHERE status='selesai')   AS pesanan_selesai,
       count(*) FILTER (WHERE status='batal')     AS pesanan_batal,
       count(DISTINCT pelanggan_id)               AS pelanggan_unik,
       sum(nilai) FILTER (WHERE status='selesai') AS nilai_selesai
FROM nilai_per_pesanan
GROUP BY cabang ORDER BY cabang""",

# ---------------- tambahan: kompleksitas khas PostgreSQL ----------------
"h5_distinct_on": """
SELECT DISTINCT ON (pelanggan_id)
       pelanggan_id, id AS pesanan_terakhir, tanggal, cabang
FROM pesanan
WHERE pelanggan_id IS NOT NULL AND status = 'selesai'
ORDER BY pelanggan_id, tanggal DESC, id DESC
LIMIT 6""",
"h5_distinct_on_tanpa_pemecah": """
SELECT count(*) AS pesanan_pada_tanggal_kembar FROM (
  SELECT pelanggan_id, tanggal, count(*) AS n
  FROM pesanan WHERE pelanggan_id IS NOT NULL AND status='selesai'
  GROUP BY pelanggan_id, tanggal HAVING count(*) > 1) x""",
"h6_rollup": """
SELECT COALESCE(cabang, 'SEMUA CABANG') AS cabang,
       COALESCE(kanal,  'semua kanal')  AS kanal,
       count(*) AS pesanan
FROM pesanan WHERE status = 'selesai'
GROUP BY ROLLUP (cabang, kanal)
ORDER BY GROUPING(cabang), cabang, GROUPING(kanal), kanal""",
"h6_grouping_sets": """
SELECT COALESCE(cabang, '(total)') AS cabang,
       COALESCE(kanal,  '(total)') AS kanal,
       count(*) AS pesanan
FROM pesanan WHERE status = 'selesai'
GROUP BY GROUPING SETS ((cabang), (kanal), ())
ORDER BY GROUPING(cabang), GROUPING(kanal), cabang, kanal""",
"h7_gen_series": """
SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
FROM generate_series(DATE '2024-01-01', DATE '2024-01-07', INTERVAL '1 day') AS d
LEFT JOIN pesanan o ON o.tanggal = d::date AND o.status = 'selesai'
LEFT JOIN item i ON i.pesanan_id = o.id
GROUP BY d ORDER BY d""",
"h7_gen_series_rusak": """
SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
FROM generate_series(DATE '2024-01-01', DATE '2024-01-07', INTERVAL '1 day') AS d
LEFT JOIN pesanan o ON o.tanggal = d::date
LEFT JOIN item i ON i.pesanan_id = o.id
WHERE o.status = 'selesai'
GROUP BY d ORDER BY d""",
"h7_tanpa_kerangka_harian": """
SELECT o.tanggal, sum(i.jumlah * i.harga_saat_itu) AS nilai
FROM pesanan o JOIN item i ON i.pesanan_id = o.id
WHERE o.status='selesai' AND o.tanggal BETWEEN DATE '2024-01-01' AND DATE '2024-01-07'
GROUP BY o.tanggal ORDER BY o.tanggal""",
"h7_rata2_dua_cara": """
WITH lengkap AS (
  SELECT d::date AS tanggal, COALESCE(sum(i.jumlah * i.harga_saat_itu), 0) AS nilai
  FROM generate_series(DATE '2024-01-01', DATE '2024-01-07', INTERVAL '1 day') AS d
  LEFT JOIN pesanan o ON o.tanggal = d::date AND o.status = 'selesai'
  LEFT JOIN item i ON i.pesanan_id = o.id
  GROUP BY d)
SELECT round(avg(nilai))                              AS rata2_7_hari_kalender,
       round(avg(nilai) FILTER (WHERE nilai > 0))     AS rata2_hari_ada_transaksi
FROM lengkap""",
}
