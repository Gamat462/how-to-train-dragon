import sqlite3, pandas as pd, numpy as np
con = sqlite3.connect("migas.db")
def run(q,n=8): return pd.read_sql(q,con).head(n)
def show(k,j,q,n=8):
    print(f"\n{'='*72}\n{k} — {j}")
    try: print(run(q,n).to_string(index=False))
    except Exception as e: print("ERROR:",e)

# ================= LEVEL 3 — LANJUTAN (window function, CTE) =================
show("L3.1","Produksi bulanan lapangan + bulan lalu + pertumbuhan % (LAG)","""
WITH b AS (SELECT s.lapangan_id AS lap, SUBSTR(p.tanggal,1,7) AS periode,
                  SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           GROUP BY lap, periode)
SELECT lap, periode, ROUND(vol,0) AS vol_bbl,
       ROUND(LAG(vol) OVER (PARTITION BY lap ORDER BY periode),0) AS bulan_lalu,
       ROUND((vol - LAG(vol) OVER (PARTITION BY lap ORDER BY periode))
             / LAG(vol) OVER (PARTITION BY lap ORDER BY periode)*100,2) AS tumbuh_persen
FROM b WHERE lap='F04' ORDER BY periode;""")

show("L3.2","Peringkat 3 sumur teratas di TIAP lapangan berdasarkan produksi 2025","""
WITH v AS (SELECT s.lapangan_id AS lap, p.sumur_id, SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE p.tanggal LIKE '2025%' GROUP BY lap, p.sumur_id),
     r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY lap ORDER BY vol DESC) AS rn FROM v)
SELECT lap, sumur_id, ROUND(vol,0) AS vol_bbl, rn FROM r WHERE rn<=3
ORDER BY lap, rn;""", 12)

show("L3.3","Produksi kumulatif berjalan per lapangan (SUM OVER)","""
WITH b AS (SELECT s.lapangan_id AS lap, SUBSTR(p.tanggal,1,7) AS periode,
                  SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE s.lapangan_id='F01' GROUP BY lap, periode)
SELECT periode, ROUND(vol,0) AS vol_bulan,
       ROUND(SUM(vol) OVER (ORDER BY periode),0) AS kumulatif
FROM b ORDER BY periode LIMIT 6;""")

show("L3.4","Kontribusi tiap sumur thd total lapangan 2025, + kumulatif % (analisis Pareto)","""
WITH v AS (SELECT s.lapangan_id AS lap, p.sumur_id, SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE p.tanggal LIKE '2025%' AND s.lapangan_id='F01' GROUP BY lap,p.sumur_id)
SELECT sumur_id, ROUND(vol,0) AS vol,
       ROUND(vol*100.0/SUM(vol) OVER (),2) AS persen,
       ROUND(SUM(vol) OVER (ORDER BY vol DESC)*100.0/SUM(vol) OVER (),2) AS kumulatif_persen
FROM v ORDER BY vol DESC;""", 10)

show("L3.5","Moving average 30 hari produksi lapangan F03 (meredam derau harian)","""
WITH h AS (SELECT p.tanggal, SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE s.lapangan_id='F03' GROUP BY p.tanggal)
SELECT tanggal, ROUND(vol,1) AS harian,
       ROUND(AVG(vol) OVER (ORDER BY tanggal ROWS BETWEEN 29 PRECEDING AND CURRENT ROW),1) AS ma30
FROM h ORDER BY tanggal DESC LIMIT 6;""")

show("L3.6","Decline rate tahunan tiap sumur: bandingkan rata-rata bopd 2024 vs 2025","""
WITH a AS (SELECT sumur_id,
             AVG(CASE WHEN tanggal LIKE '2024%' THEN oil_bopd END) AS bopd24,
             AVG(CASE WHEN tanggal LIKE '2025%' THEN oil_bopd END) AS bopd25
           FROM produksi_harian GROUP BY sumur_id)
SELECT sumur_id, ROUND(bopd24,1) AS bopd_2024, ROUND(bopd25,1) AS bopd_2025,
       ROUND((bopd25-bopd24)/bopd24*100,1) AS decline_persen
FROM a WHERE bopd24 IS NOT NULL AND bopd25 IS NOT NULL AND bopd24>0
ORDER BY decline_persen LIMIT 8;""")

show("L3.7","Hari dengan produksi lapangan terendah tiap bulan (kandidat investigasi)","""
WITH h AS (SELECT p.tanggal, SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE s.lapangan_id='F01' GROUP BY p.tanggal),
     r AS (SELECT *, SUBSTR(tanggal,1,7) AS periode,
                  ROW_NUMBER() OVER (PARTITION BY SUBSTR(tanggal,1,7) ORDER BY vol) AS rn
           FROM h)
SELECT periode, tanggal, ROUND(vol,1) AS vol_terendah FROM r WHERE rn=1
ORDER BY periode DESC LIMIT 6;""")

show("L3.8","Perubahan pangsa tiap lapangan thd total produksi, 2023 vs 2025","""
WITH v AS (SELECT s.lapangan_id AS lap, SUBSTR(p.tanggal,1,4) AS th, SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE SUBSTR(p.tanggal,1,4) IN ('2023','2025') GROUP BY lap, th),
     s AS (SELECT lap, th, vol, ROUND(vol*100.0/SUM(vol) OVER (PARTITION BY th),1) AS pangsa
           FROM v)
SELECT lap,
       MAX(CASE WHEN th='2023' THEN pangsa END) AS pangsa_2023,
       MAX(CASE WHEN th='2025' THEN pangsa END) AS pangsa_2025,
       ROUND(MAX(CASE WHEN th='2025' THEN pangsa END)
           - MAX(CASE WHEN th='2023' THEN pangsa END),1) AS perubahan
FROM s GROUP BY lap ORDER BY perubahan DESC;""")

# ================= LEVEL 4 — SULIT =================
show("L4.1","REKONSILIASI: apakah gross revenue PSC cocok dgn volume x ICP? Cari selisih","""
WITH p AS (SELECT SUBSTR(tanggal,1,7) AS periode, SUM(oil_bopd) AS vol
           FROM produksi_harian GROUP BY periode)
SELECT k.periode, ROUND(p.vol,1) AS vol_produksi, ROUND(k.volume_bbl,1) AS vol_psc,
       ROUND(p.vol-k.volume_bbl,2) AS selisih_vol,
       ROUND(k.gross_revenue_usd,0) AS gross_psc,
       ROUND(p.vol*k.icp_usd_bbl,0) AS gross_hitung_ulang,
       ROUND(k.gross_revenue_usd - p.vol*k.icp_usd_bbl,2) AS selisih_usd
FROM psc_bulanan k JOIN p ON k.periode=p.periode
ORDER BY ABS(k.gross_revenue_usd - p.vol*k.icp_usd_bbl) DESC LIMIT 5;""")

show("L4.2","REKONSILIASI PSC: buktikan gross = FTP + cost recovery + ETS (uji keutuhan)","""
SELECT periode,
  ROUND(gross_revenue_usd,0) AS gross,
  ROUND(ftp_pemerintah_usd+ftp_kontraktor_usd,0) AS ftp_total,
  ROUND(cost_recovery_usd,0) AS cost_rec,
  ROUND(ets_pemerintah_usd+ets_kontraktor_usd,0) AS ets_total,
  ROUND(gross_revenue_usd
        - (ftp_pemerintah_usd+ftp_kontraktor_usd)
        - cost_recovery_usd
        - (ets_pemerintah_usd+ets_kontraktor_usd),2) AS selisih
FROM psc_bulanan ORDER BY ABS(selisih) DESC LIMIT 5;""")

show("L4.3","Government take % per bulan + korelasinya dengan harga ICP","""
SELECT periode, icp_usd_bbl,
       ROUND(government_take_usd/gross_revenue_usd*100,2) AS gov_take_persen,
       ROUND(cost_recovery_usd/gross_revenue_usd*100,2) AS cost_rec_persen
FROM psc_bulanan ORDER BY icp_usd_bbl DESC LIMIT 5;""")

show("L4.4","EFEKTIVITAS WORKOVER: produksi 30 hari sebelum vs 30 hari sesudah","""
WITH w AS (SELECT workover_id, sumur_id, tanggal_mulai, durasi_hari, biaya_usd,
                  jenis_pekerjaan FROM workover),
sebelum AS (SELECT w.workover_id, AVG(p.oil_bopd) AS bopd_sebelum
            FROM w JOIN produksi_harian p ON p.sumur_id=w.sumur_id
            WHERE p.tanggal < w.tanggal_mulai
              AND p.tanggal >= DATE(w.tanggal_mulai,'-30 day')
            GROUP BY w.workover_id),
sesudah AS (SELECT w.workover_id, AVG(p.oil_bopd) AS bopd_sesudah
            FROM w JOIN produksi_harian p ON p.sumur_id=w.sumur_id
            WHERE p.tanggal > DATE(w.tanggal_mulai,'+'||w.durasi_hari||' day')
              AND p.tanggal <= DATE(w.tanggal_mulai,'+'||(w.durasi_hari+30)||' day')
            GROUP BY w.workover_id)
SELECT w.jenis_pekerjaan, COUNT(*) AS n,
       ROUND(AVG(s1.bopd_sebelum),1) AS sebelum,
       ROUND(AVG(s2.bopd_sesudah),1) AS sesudah,
       ROUND(AVG(s2.bopd_sesudah-s1.bopd_sebelum),1) AS gain_bopd,
       ROUND(AVG(w.biaya_usd),0) AS biaya_rata2
FROM w JOIN sebelum s1 ON w.workover_id=s1.workover_id
       JOIN sesudah s2 ON w.workover_id=s2.workover_id
GROUP BY w.jenis_pekerjaan ORDER BY gain_bopd DESC;""")

show("L4.5","PAYBACK WORKOVER: berapa hari modal kembali? (pakai ICP saat itu)","""
WITH w AS (SELECT workover_id, sumur_id, tanggal_mulai, durasi_hari, biaya_usd, jenis_pekerjaan FROM workover),
sb AS (SELECT w.workover_id, AVG(p.oil_bopd) AS b0 FROM w
       JOIN produksi_harian p ON p.sumur_id=w.sumur_id
       WHERE p.tanggal<w.tanggal_mulai AND p.tanggal>=DATE(w.tanggal_mulai,'-30 day')
       GROUP BY w.workover_id),
ss AS (SELECT w.workover_id, AVG(p.oil_bopd) AS b1 FROM w
       JOIN produksi_harian p ON p.sumur_id=w.sumur_id
       WHERE p.tanggal>DATE(w.tanggal_mulai,'+'||w.durasi_hari||' day')
         AND p.tanggal<=DATE(w.tanggal_mulai,'+'||(w.durasi_hari+30)||' day')
       GROUP BY w.workover_id)
SELECT w.workover_id, w.jenis_pekerjaan, ROUND(w.biaya_usd,0) AS biaya,
       ROUND(ss.b1-sb.b0,1) AS gain_bopd, h.icp_usd_bbl,
       ROUND(w.biaya_usd/NULLIF((ss.b1-sb.b0)*h.icp_usd_bbl,0),0) AS payback_hari
FROM w JOIN sb ON w.workover_id=sb.workover_id
       JOIN ss ON w.workover_id=ss.workover_id
       JOIN harga_icp h ON SUBSTR(w.tanggal_mulai,1,7)=h.periode
WHERE ss.b1>sb.b0
ORDER BY payback_hari LIMIT 8;""")

show("L4.6","BATAS EKONOMIS: sumur yang pendapatannya < biaya operasi per sumur","""
WITH akhir AS (SELECT sumur_id, AVG(oil_bopd) AS bopd FROM produksi_harian
               WHERE tanggal >= '2026-04-01' GROUP BY sumur_id),
opex AS (SELECT SUM(nilai_usd)/COUNT(DISTINCT lapangan_id) AS dummy FROM biaya_operasi),
biaya_sumur AS (
  SELECT b.lapangan_id, SUM(b.nilai_usd)/3.0 AS opex_bulanan
  FROM biaya_operasi b WHERE b.jenis='OPEX' AND b.periode>='2026-04' GROUP BY b.lapangan_id),
n AS (SELECT lapangan_id, COUNT(*) AS n_sumur FROM sumur WHERE tipe_sumur='Producer' GROUP BY lapangan_id)
SELECT a.sumur_id, s.lapangan_id, ROUND(a.bopd,1) AS bopd,
       ROUND(a.bopd*30*69.0,0) AS pendapatan_bulanan_usd,
       ROUND(bs.opex_bulanan/n.n_sumur,0) AS biaya_per_sumur_usd,
       ROUND(a.bopd*30*69.0 - bs.opex_bulanan/n.n_sumur,0) AS margin_usd
FROM akhir a JOIN sumur s ON a.sumur_id=s.sumur_id
  JOIN biaya_sumur bs ON s.lapangan_id=bs.lapangan_id
  JOIN n ON s.lapangan_id=n.lapangan_id
ORDER BY margin_usd LIMIT 8;""")

show("L4.7","ANOMALI: sumur yang produksinya turun jauh lebih cepat dari rekan selapangan","""
WITH d AS (SELECT p.sumur_id, s.lapangan_id,
             AVG(CASE WHEN p.tanggal LIKE '2025%' THEN p.oil_bopd END) AS b25,
             AVG(CASE WHEN p.tanggal LIKE '2026%' THEN p.oil_bopd END) AS b26
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           GROUP BY p.sumur_id, s.lapangan_id),
r AS (SELECT *, (b26-b25)/b25*100 AS decl FROM d WHERE b25>10),
m AS (SELECT lapangan_id, AVG(decl) AS decl_lap FROM r GROUP BY lapangan_id)
SELECT r.sumur_id, r.lapangan_id, ROUND(r.b25,1) AS bopd_2025,
       ROUND(r.b26,1) AS bopd_2026, ROUND(r.decl,1) AS decline_sumur,
       ROUND(m.decl_lap,1) AS decline_lapangan,
       ROUND(r.decl-m.decl_lap,1) AS selisih
FROM r JOIN m ON r.lapangan_id=m.lapangan_id
ORDER BY selisih LIMIT 6;""")

show("L4.8","DAMPAK DOWNTIME: perkiraan bbl hilang, dinilai dgn ICP saat itu","""
WITH normal AS (SELECT p.sumur_id, AVG(p.oil_bopd) AS bopd_normal
                FROM produksi_harian p WHERE p.berproduksi=1 GROUP BY p.sumur_id)
SELECT d.penyebab, COUNT(*) AS kejadian, SUM(d.durasi_hari) AS hari,
       ROUND(SUM(d.durasi_hari*n.bopd_normal),0) AS bbl_hilang,
       ROUND(SUM(d.durasi_hari*n.bopd_normal*h.icp_usd_bbl),0) AS nilai_usd
FROM downtime d JOIN normal n ON d.sumur_id=n.sumur_id
  JOIN harga_icp h ON SUBSTR(d.tanggal_mulai,1,7)=h.periode
GROUP BY d.penyebab ORDER BY nilai_usd DESC;""")
con.close()
