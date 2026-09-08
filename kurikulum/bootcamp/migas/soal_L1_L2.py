import sqlite3, pandas as pd
con = sqlite3.connect("migas.db")
def run(q, n=6):
    return pd.read_sql(q, con).head(n)

S = {}

# ================= LEVEL 1 — FONDASI =================
S["L1.1"] = ("Berapa total produksi minyak (bbl) sepanjang 2025?", """
SELECT ROUND(SUM(oil_bopd),0) AS total_oil_bbl
FROM produksi_harian WHERE tanggal LIKE '2025%';""")

S["L1.2"] = ("Ada berapa sumur produser dan berapa injektor?", """
SELECT tipe_sumur, COUNT(*) AS jumlah FROM sumur GROUP BY tipe_sumur;""")

S["L1.3"] = ("Produksi minyak per lapangan sepanjang 2025, urut terbesar.", """
SELECT s.lapangan_id, ROUND(SUM(p.oil_bopd),0) AS oil_bbl
FROM produksi_harian p JOIN sumur s ON p.sumur_id = s.sumur_id
WHERE p.tanggal LIKE '2025%' GROUP BY s.lapangan_id ORDER BY oil_bbl DESC;""")

S["L1.4"] = ("Lima sumur dengan produksi minyak kumulatif terbesar.", """
SELECT sumur_id, ROUND(SUM(oil_bopd),0) AS kumulatif_bbl
FROM produksi_harian GROUP BY sumur_id ORDER BY kumulatif_bbl DESC LIMIT 5;""")

S["L1.5"] = ("Berapa hari-sumur yang tidak berproduksi sama sekali?", """
SELECT COUNT(*) AS hari_mati FROM produksi_harian WHERE berproduksi = 0;""")

S["L1.6"] = ("Berapa jumlah insiden HSE per jenis, urut terbanyak?", """
SELECT jenis_insiden, COUNT(*) AS jumlah FROM hse_insiden
GROUP BY jenis_insiden ORDER BY jumlah DESC;""")

S["L1.7"] = ("Rata-rata ICP per tahun.", """
SELECT SUBSTR(periode,1,4) AS tahun, ROUND(AVG(icp_usd_bbl),2) AS icp_rata2
FROM harga_icp GROUP BY tahun ORDER BY tahun;""")

S["L1.8"] = ("Total biaya per jenis (OPEX vs CAPEX).", """
SELECT jenis, ROUND(SUM(nilai_usd),0) AS total_usd FROM biaya_operasi
GROUP BY jenis;""")

S["L1.9"] = ("Metode angkat apa yang paling banyak dipakai?", """
SELECT metode_angkat, COUNT(*) AS jumlah_sumur FROM sumur
GROUP BY metode_angkat ORDER BY jumlah_sumur DESC;""")

S["L1.10"] = ("Berapa total volume dan nilai lifting untuk tujuan Ekspor?", """
SELECT tujuan, COUNT(*) AS kargo, ROUND(SUM(volume_bbl),0) AS volume,
       ROUND(SUM(nilai_usd),0) AS nilai_usd
FROM lifting GROUP BY tujuan;""")

S["L1.11"] = ("Penyebab downtime paling sering, dan total hari yang hilang.", """
SELECT penyebab, COUNT(*) AS kejadian, SUM(durasi_hari) AS total_hari
FROM downtime GROUP BY penyebab ORDER BY total_hari DESC;""")

S["L1.12"] = ("Berapa workover dilakukan per jenis, dan berapa total biayanya?", """
SELECT jenis_pekerjaan, COUNT(*) AS jumlah, ROUND(SUM(biaya_usd),0) AS total_usd
FROM workover GROUP BY jenis_pekerjaan ORDER BY total_usd DESC;""")

# ================= LEVEL 2 — MENENGAH =================
S["L2.1"] = ("Produksi minyak per lapangan per tahun, DENGAN nama lapangan.", """
SELECT l.nama_lapangan, SUBSTR(p.tanggal,1,4) AS tahun,
       ROUND(SUM(p.oil_bopd),0) AS oil_bbl
FROM produksi_harian p
JOIN sumur s   ON p.sumur_id = s.sumur_id
JOIN lapangan l ON s.lapangan_id = l.lapangan_id
GROUP BY l.nama_lapangan, tahun ORDER BY l.nama_lapangan, tahun;""")

S["L2.2"] = ("Watercut rata-rata per lapangan per tahun. Lapangan mana paling 'basah'?", """
SELECT s.lapangan_id, SUBSTR(p.tanggal,1,4) AS tahun,
       ROUND(AVG(p.watercut)*100,1) AS watercut_persen
FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
GROUP BY s.lapangan_id, tahun ORDER BY s.lapangan_id, tahun;""")

S["L2.3"] = ("Uptime (%) per lapangan sepanjang 2025.", """
SELECT s.lapangan_id,
       ROUND(AVG(p.berproduksi)*100,2) AS uptime_persen,
       COUNT(*) AS hari_sumur
FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
WHERE p.tanggal LIKE '2025%'
GROUP BY s.lapangan_id ORDER BY uptime_persen;""")

S["L2.4"] = ("Lifting cost per bbl per lapangan 2025 (OPEX saja).", """
WITH o AS (SELECT lapangan_id, SUM(nilai_usd) AS opex FROM biaya_operasi
           WHERE jenis='OPEX' AND periode LIKE '2025%' GROUP BY lapangan_id),
     v AS (SELECT s.lapangan_id, SUM(p.oil_bopd) AS vol
           FROM produksi_harian p JOIN sumur s ON p.sumur_id=s.sumur_id
           WHERE p.tanggal LIKE '2025%' GROUP BY s.lapangan_id)
SELECT o.lapangan_id, ROUND(o.opex,0) AS opex_usd, ROUND(v.vol,0) AS vol_bbl,
       ROUND(o.opex/v.vol,2) AS lifting_cost_per_bbl
FROM o JOIN v ON o.lapangan_id=v.lapangan_id ORDER BY lifting_cost_per_bbl DESC;""")

S["L2.5"] = ("Sumur yang watercut-nya sudah melewati 90% di data terakhir.", """
WITH akhir AS (SELECT sumur_id, MAX(tanggal) AS t FROM produksi_harian GROUP BY sumur_id)
SELECT p.sumur_id, p.tanggal, ROUND(p.watercut*100,1) AS wc_persen,
       ROUND(p.oil_bopd,1) AS oil_bopd
FROM produksi_harian p JOIN akhir a ON p.sumur_id=a.sumur_id AND p.tanggal=a.t
WHERE p.watercut > 0.90 ORDER BY p.watercut DESC;""")

S["L2.6"] = ("Lapangan mana yang insiden HSE beratnya paling banyak?", """
SELECT h.lapangan_id, l.nama_lapangan,
       SUM(CASE WHEN h.tingkat_keparahan='Berat' THEN 1 ELSE 0 END) AS berat,
       COUNT(*) AS total_insiden
FROM hse_insiden h JOIN lapangan l ON h.lapangan_id=l.lapangan_id
GROUP BY h.lapangan_id, l.nama_lapangan ORDER BY berat DESC;""")

S["L2.7"] = ("Produksi bulanan 2026 beserta ICP dan perkiraan gross revenue.", """
SELECT SUBSTR(p.tanggal,1,7) AS periode,
       ROUND(SUM(p.oil_bopd),0) AS vol_bbl,
       h.icp_usd_bbl,
       ROUND(SUM(p.oil_bopd)*h.icp_usd_bbl,0) AS gross_usd
FROM produksi_harian p JOIN harga_icp h ON SUBSTR(p.tanggal,1,7)=h.periode
WHERE p.tanggal LIKE '2026%'
GROUP BY periode, h.icp_usd_bbl ORDER BY periode;""")

S["L2.8"] = ("Sumur yang PERNAH di-workover vs yang belum, beserta produksi rata-ratanya.", """
SELECT CASE WHEN w.sumur_id IS NULL THEN 'Belum pernah' ELSE 'Pernah' END AS status,
       COUNT(DISTINCT p.sumur_id) AS jumlah_sumur,
       ROUND(AVG(p.oil_bopd),1) AS rata2_bopd
FROM produksi_harian p
LEFT JOIN (SELECT DISTINCT sumur_id FROM workover) w ON p.sumur_id=w.sumur_id
GROUP BY status;""")

S["L2.9"] = ("Sumur produser yang TIDAK pernah punya catatan downtime.", """
SELECT s.sumur_id, s.lapangan_id, s.metode_angkat
FROM sumur s
LEFT JOIN (SELECT DISTINCT sumur_id FROM downtime) d ON s.sumur_id=d.sumur_id
WHERE s.tipe_sumur='Producer' AND d.sumur_id IS NULL
ORDER BY s.sumur_id;""")

S["L2.10"] = ("Bandingkan volume lifting vs volume produksi per tahun. Cocok?", """
WITH prod AS (SELECT SUBSTR(tanggal,1,4) AS th, SUM(oil_bopd) AS produksi
              FROM produksi_harian GROUP BY th),
     lift AS (SELECT SUBSTR(periode,1,4) AS th, SUM(volume_bbl) AS lifting
              FROM lifting GROUP BY th)
SELECT p.th, ROUND(p.produksi,0) AS produksi_bbl, ROUND(l.lifting,0) AS lifting_bbl,
       ROUND(l.lifting-p.produksi,0) AS selisih,
       ROUND((l.lifting-p.produksi)/p.produksi*100,2) AS selisih_persen
FROM prod p JOIN lift l ON p.th=l.th ORDER BY p.th;""")

S["L2.11"] = ("Rata-rata biaya workover per jenis, dan rata-rata kenaikan produksinya.", """
SELECT jenis_pekerjaan, COUNT(*) AS n,
       ROUND(AVG(biaya_usd),0) AS biaya_rata2,
       ROUND(AVG(faktor_kenaikan),3) AS kenaikan_rata2,
       ROUND(AVG(biaya_usd)/AVG(faktor_kenaikan-1),0) AS biaya_per_unit_kenaikan
FROM workover GROUP BY jenis_pekerjaan ORDER BY biaya_per_unit_kenaikan;""")

S["L2.12"] = ("Berapa hari kerja hilang akibat LTI, per tahun?", """
SELECT SUBSTR(periode,1,4) AS tahun,
       SUM(CASE WHEN jenis_insiden='Lost Time Injury' THEN 1 ELSE 0 END) AS jumlah_lti,
       SUM(hari_kerja_hilang) AS hari_hilang
FROM hse_insiden GROUP BY tahun ORDER BY tahun;""")

# ---- jalankan semua ----
for k in sorted(S, key=lambda x:(x.split('.')[0], int(x.split('.')[1]))):
    judul, q = S[k]
    print(f"\n{'='*70}\n{k} — {judul}")
    try:
        print(run(q).to_string(index=False))
    except Exception as e:
        print("ERROR:", e)
con.close()
