# -*- coding: utf-8 -*-
"""SQL untuk modul Bekal Pajak & ERP — PostgreSQL 16, database senja.

Tabelnya (pjk_wp, pjk_lapisan) dibuat terpisah dari data kedai kopi, tapi di
database yang sama supaya pembaca tidak perlu membuat sambungan baru.
"""
KUERI = {
"h0_lihat_wp": "SELECT * FROM pjk_wp ORDER BY id",
"h0_lihat_lapisan": "SELECT * FROM pjk_lapisan ORDER BY urutan",

"h2_naif": """
SELECT w.nama, w.penghasilan_tahunan, l.tarif,
       round(w.penghasilan_tahunan * l.tarif) AS pajak_naif
FROM pjk_wp w
JOIN pjk_lapisan l
  ON w.penghasilan_tahunan >= l.batas_bawah
 AND (l.batas_atas IS NULL OR w.penghasilan_tahunan < l.batas_atas)
WHERE w.jenis = 'perorangan'
ORDER BY w.id""",

"h2_rincian_sari": """
WITH potong AS (
  SELECT w.nama, l.urutan, l.batas_bawah, l.batas_atas, l.tarif,
         GREATEST(0, LEAST(w.penghasilan_tahunan,
                  COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian
  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah
  WHERE w.nama = 'Sari')
SELECT urutan, batas_bawah, batas_atas, tarif, bagian, round(bagian * tarif) AS pajak_lapisan
FROM potong ORDER BY urutan""",

"h2_benar": """
WITH potong AS (
  SELECT w.id, w.nama, l.tarif,
         GREATEST(0, LEAST(w.penghasilan_tahunan,
                  COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian
  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah
  WHERE w.jenis = 'perorangan')
SELECT id, nama, round(sum(bagian * tarif)) AS pajak_benar
FROM potong GROUP BY id, nama ORDER BY id""",

"h2_selisih": """
WITH progresif AS (
  SELECT w.id, w.nama,
         round(sum(GREATEST(0, LEAST(w.penghasilan_tahunan,
               COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) * l.tarif)) AS pajak_benar
  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah
  WHERE w.jenis = 'perorangan' GROUP BY w.id, w.nama),
naif AS (
  SELECT w.id, round(w.penghasilan_tahunan * l.tarif) AS pajak_naif
  FROM pjk_wp w JOIN pjk_lapisan l
    ON w.penghasilan_tahunan >= l.batas_bawah
   AND (l.batas_atas IS NULL OR w.penghasilan_tahunan < l.batas_atas)
  WHERE w.jenis = 'perorangan')
SELECT p.nama, n.pajak_naif, p.pajak_benar, n.pajak_naif - p.pajak_benar AS kelebihan_tagih,
       round(100.0 * (n.pajak_naif - p.pajak_benar) / p.pajak_benar, 1) AS persen_lebih
FROM progresif p JOIN naif n ON n.id = p.id ORDER BY p.id""",

"h2_diam_lapisan_teratas": """
SELECT w.nama, w.penghasilan_tahunan, l.tarif
FROM pjk_wp w
JOIN pjk_lapisan l
  ON w.penghasilan_tahunan >= l.batas_bawah
 AND w.penghasilan_tahunan < l.batas_atas
WHERE w.nama = 'Maya'""",

"h3_umkm_naif": """
SELECT nama, omzet_tahunan, round(omzet_tahunan * 0.005) AS pajak_umkm_naif
FROM pjk_wp WHERE jenis = 'umkm' ORDER BY id""",

"h3_agus_progresif": """
WITH potong AS (
  SELECT w.nama, l.tarif,
         GREATEST(0, LEAST(w.penghasilan_tahunan,
                  COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian
  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah
  WHERE w.nama = 'Agus')
SELECT nama, round(sum(bagian * tarif)) AS pajak_benar FROM potong GROUP BY nama""",

"h3_cek_lewat_batas": """
SELECT nama, omzet_tahunan, omzet_tahunan > 4800000000 AS lewat_batas_umkm
FROM pjk_wp WHERE jenis = 'umkm' ORDER BY id""",

"h3_final": """
WITH potong AS (
  SELECT w.id, w.nama, w.jenis, w.omzet_tahunan,
         GREATEST(0, LEAST(w.penghasilan_tahunan,
                  COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian,
         l.tarif
  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah),
progresif AS (
  SELECT id, nama, jenis, omzet_tahunan, round(sum(bagian * tarif)) AS pajak_progresif
  FROM potong GROUP BY id, nama, jenis, omzet_tahunan)
SELECT nama, jenis,
  CASE WHEN jenis = 'umkm' AND omzet_tahunan <= 4800000000
       THEN round(omzet_tahunan * 0.005) ELSE pajak_progresif END AS pajak_final,
  CASE WHEN jenis = 'umkm' AND omzet_tahunan <= 4800000000
       THEN 'umkm final 0,5% omzet' ELSE 'progresif normal' END AS aturan_dipakai
FROM progresif ORDER BY id""",

"h3_diam_tanpa_cek_batas": """
SELECT nama, jenis, omzet_tahunan,
  CASE WHEN jenis = 'umkm' THEN round(omzet_tahunan * 0.005)
       ELSE NULL END AS pajak_umkm_tanpa_cek_batas
FROM pjk_wp WHERE nama = 'Agus'""",

"h1_merah_duplikat": """
INSERT INTO pjk_wp (id, nama, jenis, penghasilan_tahunan)
VALUES (1, 'Rina (kiriman ulang)', 'perorangan', 45000000)""",

"h1_merah_format_erp": """
INSERT INTO pjk_wp (nama, jenis, penghasilan_tahunan)
VALUES ('Tono', 'perorangan', '1.250.000.000')""",
"h1_hitung_jenis": "SELECT jenis, count(*) FROM pjk_wp GROUP BY jenis ORDER BY jenis",
}
