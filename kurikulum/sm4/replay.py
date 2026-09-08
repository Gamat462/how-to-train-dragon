# Memutar ulang SELURUH modul SQL Mahir L4, urut, di besar.db yang baru dibuat.
# Semua keluaran di sini yang dipakai menulis modulnya. Tidak ada angka lain.
import sqlite3, time, os, shutil, subprocess, sys

def P(t): print(f"\n########## {t}")

P("H1.1  python besar.py")
print(subprocess.run([sys.executable,"besar.py"],capture_output=True,text=True).stdout.strip())

con = sqlite3.connect("besar.db")
def rencana(sql):
    for b in con.execute("EXPLAIN QUERY PLAN " + sql): print("   ", b[3])

P("H1.2  sambungkan & hitung")
print(con.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0])

P("H1.3  ukur sekali dengan perf_counter")
Q = "SELECT COUNT(*) FROM transaksi WHERE pelanggan_id = 12345"
t = time.perf_counter(); h = con.execute(Q).fetchall()
print(f"{(time.perf_counter()-t)*1000:.1f} ms   hasil = {h[0][0]}")

P("H1.4  fungsi ukur()")
def ukur(sql, n=7):
    w = []
    for _ in range(n):
        t = time.perf_counter(); h = con.execute(sql).fetchall()
        w.append(time.perf_counter() - t)
    return min(w) * 1000, h
ms, h = ukur(Q); print(f"{ms:.1f} ms   hasil = {h[0][0]}")

P("H1.5  rencananya")
rencana(Q)

P("H1.6  rencana query pengelompokan")
rencana("SELECT produk, COUNT(*) FROM transaksi GROUP BY produk")

P("H1.7  CREATE INDEX")
t = time.perf_counter()
con.execute("CREATE INDEX idx_pel ON transaksi(pelanggan_id)"); con.commit()
print(f"membuat index: {time.perf_counter()-t:.2f} detik")

P("H1.8  ukur ulang")
ms2, h = ukur(Q, n=50); print(f"{ms2:.3f} ms   hasil = {h[0][0]}")
print(f"(kelipatan {ms/ms2:.0f}x)")

P("H1.9  rencana sesudah index")
rencana(Q)

P("H1.10 minta kolom lain")
Q2 = "SELECT SUM(nilai) FROM transaksi WHERE pelanggan_id = 12345"
m, h = ukur(Q2, n=50); print(f"{m:.3f} ms   hasil = {h[0][0]}"); rencana(Q2)

# ---------------- HARI 2 ----------------
P("H2.1  index tanggal")
t = time.perf_counter()
con.execute("CREATE INDEX idx_tgl ON transaksi(tanggal)"); con.commit()
print(f"membuat index: {time.perf_counter()-t:.2f} detik")

P("H2.2  fungsi menempel di kolom")
A = "SELECT COUNT(*) FROM transaksi WHERE substr(tanggal,1,7) = '2024-01'"
mA, h = ukur(A); print(f"{mA:.1f} ms   hasil = {h[0][0]}"); rencana(A)

P("H2.3  rentang tanggal")
B = "SELECT COUNT(*) FROM transaksi WHERE tanggal >= '2024-01-01' AND tanggal < '2024-02-01'"
mB, h = ukur(B); print(f"{mB:.1f} ms   hasil = {h[0][0]}"); rencana(B)
print(f"(kelipatan {mA/mB:.0f}x)")

P("H2.4  index cabang + sama dengan")
con.execute("CREATE INDEX idx_cab ON transaksi(cabang)"); con.commit()
s = "SELECT COUNT(*) FROM transaksi WHERE cabang = 'Kemang'"
m1, h = ukur(s); print(f"{m1:.1f} ms   hasil = {h[0][0]}"); rencana(s)

P("H2.5  LIKE 'Kem%'")
s = "SELECT COUNT(*) FROM transaksi WHERE cabang LIKE 'Kem%'"
m2, h = ukur(s); print(f"{m2:.1f} ms   hasil = {h[0][0]}"); rencana(s)

P("H2.6  LIKE '%mang'")
s = "SELECT COUNT(*) FROM transaksi WHERE cabang LIKE '%mang'"
m3, h = ukur(s); print(f"{m3:.1f} ms   hasil = {h[0][0]}"); rencana(s)

P("H2.7  rentang teks")
s = "SELECT COUNT(*) FROM transaksi WHERE cabang >= 'Kem' AND cabang < 'Ken'"
m4, h = ukur(s); print(f"{m4:.1f} ms   hasil = {h[0][0]}"); rencana(s)
print(f"(empat cara: {m1:.1f} / {m2:.1f} / {m3:.1f} / {m4:.1f} ms)")

# ---------------- HARI 3 ----------------
P("H3.1  hapus index kemarin")
for n in ["idx_pel","idx_tgl","idx_cab"]: con.execute(f"DROP INDEX IF EXISTS {n}")
con.commit()
print("index tersisa:", con.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'").fetchone()[0])

P("H3.2  index gabungan (cabang, tanggal)")
con.execute("CREATE INDEX idx_ct ON transaksi(cabang, tanggal)"); con.commit()
print("idx_ct dibuat")

P("H3.3  kolom ke-1 saja")
s = "SELECT COUNT(*) FROM transaksi WHERE cabang = 'Kemang'"
m, h = ukur(s); print(f"{m:.1f} ms   hasil = {h[0][0]}"); rencana(s)

P("H3.4  kolom ke-1 lalu ke-2")
s = "SELECT COUNT(*) FROM transaksi WHERE cabang = 'Kemang' AND tanggal >= '2024-01-01'"
m, h = ukur(s); print(f"{m:.1f} ms   hasil = {h[0][0]}"); rencana(s)

P("H3.5  kolom ke-2 saja")
s = "SELECT COUNT(*) FROM transaksi WHERE tanggal >= '2024-01-01'"
m, h = ukur(s); print(f"{m:.1f} ms   hasil = {h[0][0]}"); rencana(s)

P("H3.6  Q2 dengan idx_ct saja")
Q2 = """SELECT cabang, SUM(nilai) FROM transaksi
WHERE tanggal >= '2024-01-01' AND tanggal < '2024-02-01' GROUP BY cabang"""
ma, h = ukur(Q2); print(f"{ma:.1f} ms   {len(h)} baris"); rencana(Q2)

P("H3.7  Q2 sesudah idx_tc")
con.execute("CREATE INDEX idx_tc ON transaksi(tanggal, cabang)"); con.commit()
mb, h = ukur(Q2); print(f"{mb:.1f} ms   {len(h)} baris"); rencana(Q2)
print(f"(kelipatan {ma/mb:.1f}x)")

P("H3.8  ORDER BY dengan idx(pelanggan_id)")
con.execute("DROP INDEX idx_tc")
Q3 = "SELECT * FROM transaksi WHERE pelanggan_id = 12345 ORDER BY tanggal DESC"
con.execute("CREATE INDEX idx_p1 ON transaksi(pelanggan_id)"); con.commit()
rencana(Q3)

P("H3.9  ORDER BY dengan idx(pelanggan_id, tanggal)")
con.execute("DROP INDEX idx_p1")
con.execute("CREATE INDEX idx_p2 ON transaksi(pelanggan_id, tanggal)"); con.commit()
rencana(Q3)
con.execute("DROP INDEX idx_p2"); con.commit()
con.close()

# ---------------- HARI 4 ----------------
P("H4.1  salinan tanpa index")
shutil.copy("besar.db", "coba.db")
c = sqlite3.connect("coba.db")
c.execute("DROP INDEX IF EXISTS idx_ct"); c.execute("VACUUM")
print(f"tanpa index apa pun : {os.path.getsize('coba.db')/1e6:.1f} MB")

P("H4.2  tulis 50.000 baris tanpa index")
def tulis(con, n=50000):
    baris = [(1000000+i, "2024-06-01", "Kemang", 7, "Kopi Susu", 1, 22000) for i in range(n)]
    t = time.perf_counter()
    con.executemany("INSERT INTO transaksi VALUES (?,?,?,?,?,?,?)", baris)
    con.commit()
    return time.perf_counter() - t
t_tanpa = tulis(c); print(f"tanpa index : {t_tanpa:.2f} detik")

P("H4.3  hapus lagi")
c.execute("DELETE FROM transaksi WHERE id >= 1000000"); c.commit()
print("sisa baris:", c.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0])

P("H4.4  bikin tiga index")
for nama, kolom in [("idx_ct","cabang, tanggal"), ("idx_pel","pelanggan_id"), ("idx_prd","produk")]:
    t = time.perf_counter()
    c.execute(f"CREATE INDEX {nama} ON transaksi({kolom})"); c.commit()
    print(f"waktu buat {nama:8s}: {time.perf_counter()-t:.2f} detik")

P("H4.5  ukuran berkas sesudahnya")
c.execute("VACUUM")
print(f"dengan 3 index      : {os.path.getsize('coba.db')/1e6:.1f} MB")

P("H4.6  tulis lagi, sekarang dengan index")
t_dgn = tulis(c)
print(f"dgn 3 index : {t_dgn:.2f} detik")
print(f"perlambatan : {t_dgn/t_tanpa:.1f}x")
c.close(); os.remove("coba.db")

# ---------------- HARI 5 ----------------
P("H5.1  tabel kecil 10.000 baris")
if os.path.exists("q2.db"): os.remove("q2.db")
c = sqlite3.connect("q2.db")
c.execute("ATTACH 'besar.db' AS b")
c.execute("CREATE TABLE kecil AS SELECT * FROM b.transaksi WHERE id <= 10000")
c.commit(); c.execute("DETACH b")
print("baris:", c.execute("SELECT COUNT(*) FROM kecil").fetchone()[0])

korelasi = """SELECT cabang, COUNT(*) AS di_atas_rata FROM kecil t1
WHERE nilai > (SELECT AVG(nilai) FROM kecil t2 WHERE t2.cabang = t1.cabang)
GROUP BY cabang ORDER BY cabang"""
cte = """WITH rata AS (SELECT cabang, AVG(nilai) AS r FROM kecil GROUP BY cabang)
SELECT t.cabang, COUNT(*) AS di_atas_rata FROM kecil t
JOIN rata ON rata.cabang = t.cabang
WHERE t.nilai > rata.r
GROUP BY t.cabang ORDER BY t.cabang"""

P("H5.2  jalankan yang berkorelasi (sabar)")
t = time.perf_counter(); rk = c.execute(korelasi).fetchall(); tk = (time.perf_counter()-t)*1000
print(f"{tk:.1f} ms")
for x in rk: print("   ", x)

P("H5.3  rencananya")
for p in c.execute("EXPLAIN QUERY PLAN " + korelasi): print("   ", p[3])

P("H5.4  versi CTE")
w = []
for _ in range(5):
    t = time.perf_counter(); rc = c.execute(cte).fetchall(); w.append(time.perf_counter()-t)
tc = min(w)*1000
print(f"{tc:.1f} ms")
for x in rc: print("   ", x)
print("sama?", rk == rc)
print(f"(kelipatan {tk/tc:.0f}x)")

P("H5.5  rencana CTE")
for p in c.execute("EXPLAIN QUERY PLAN " + cte): print("   ", p[3])

P("H5.6  tabel skala (± 3 menit)")
c.execute("ATTACH 'besar.db' AS b")
print(f"{'baris':>8} {'berkorelasi':>14} {'CTE':>10}   kelipatan")
for n in [2500, 5000, 10000, 20000, 40000]:
    c.execute("DROP TABLE IF EXISTS kecil")
    c.execute(f"CREATE TABLE kecil AS SELECT * FROM b.transaksi WHERE id <= {n}")
    c.commit()
    t = time.perf_counter(); rk = c.execute(korelasi).fetchall(); tk = time.perf_counter()-t
    w = []
    for _ in range(5):
        t = time.perf_counter(); rc = c.execute(cte).fetchall(); w.append(time.perf_counter()-t)
    tc = min(w)
    print(f"{n:>8} {tk*1000:>12.1f}ms {tc*1000:>8.1f}ms   {tk/tc:>8.0f}x   sama={rk==rc}")
c.close(); os.remove("q2.db")

P("H5.7  latihan senja.db — dua versi")
import pandas as pd
s2 = sqlite3.connect("senja.db")
lama = """SELECT p.nama,
       (SELECT COUNT(*) FROM pesanan WHERE pelanggan_id = p.id) AS jumlah_pesanan
FROM pelanggan p ORDER BY jumlah_pesanan DESC, p.nama LIMIT 5"""
baru = """SELECT p.nama, COUNT(o.id) AS jumlah_pesanan
FROM pelanggan p
LEFT JOIN pesanan o ON o.pelanggan_id = p.id
GROUP BY p.id, p.nama ORDER BY jumlah_pesanan DESC, p.nama LIMIT 5"""
print(pd.read_sql(lama, s2).to_string()); print()
print(pd.read_sql(baru, s2).to_string())

P("H5.8  pelanggan yang belum pernah pesan")
print(s2.execute("""SELECT p.id, p.nama FROM pelanggan p
LEFT JOIN pesanan o ON o.pelanggan_id = p.id
WHERE o.id IS NULL ORDER BY p.id""").fetchall())
print("JOIN biasa menyisakan:",
      len(s2.execute("""SELECT p.id FROM pelanggan p
JOIN pesanan o ON o.pelanggan_id = p.id GROUP BY p.id""").fetchall()), "dari 20")
s2.close()

# ---------------- HARI 6 ----------------
P("H6.1  tabel kas")
shutil.copy("senja.db", "tx.db")
con = sqlite3.connect("tx.db", isolation_level=None)
con.executescript("""
DROP TABLE IF EXISTS kas;
CREATE TABLE kas (
  akun  TEXT PRIMARY KEY,
  saldo INTEGER NOT NULL CHECK (saldo >= 0)
);
INSERT INTO kas VALUES ('Kas Besar', 5000000), ('Kas Kecil', 300000);
""")
def saldo(): return dict(con.execute("SELECT akun, saldo FROM kas").fetchall())
print("saldo:", saldo()); print("total:", sum(saldo().values()))

P("H6.2  perintah pertama")
con.execute("UPDATE kas SET saldo = saldo - 400000 WHERE akun = 'Kas Besar'")
print("saldo:", saldo())

P("H6.3  perintah kedua ditolak")
try:
    con.execute("UPDATE kas SET saldo = saldo - 900000 WHERE akun = 'Kas Kecil'")
except sqlite3.IntegrityError as e:
    print("error:", e)

P("H6.4  hitung totalnya")
print("saldo:", saldo())
print("total:", sum(saldo().values()))

P("H6.5  kembalikan lalu bungkus BEGIN/COMMIT")
con.execute("UPDATE kas SET saldo = 5000000 WHERE akun = 'Kas Besar'")
print("total sebelum:", sum(saldo().values()))
try:
    con.execute("BEGIN")
    con.execute("UPDATE kas SET saldo = saldo - 400000 WHERE akun = 'Kas Besar'")
    con.execute("UPDATE kas SET saldo = saldo - 900000 WHERE akun = 'Kas Kecil'")
    con.execute("COMMIT")
except sqlite3.IntegrityError as e:
    con.execute("ROLLBACK"); print("error:", e, "-> ROLLBACK")
print("saldo:", saldo())
print("total sesudah:", sum(saldo().values()))
con.close(); os.remove("tx.db")

P("H6.6  foreign_keys bawaan")
shutil.copy("senja.db", "fk.db")
c = sqlite3.connect("fk.db")
print("foreign_keys bawaan:", c.execute("PRAGMA foreign_keys").fetchone()[0])

P("H6.7  dua tabel bertaut")
c.executescript("""
DROP TABLE IF EXISTS anak;
DROP TABLE IF EXISTS induk;
CREATE TABLE induk (id INTEGER PRIMARY KEY, nama TEXT);
CREATE TABLE anak  (id INTEGER PRIMARY KEY,
                    induk_id INTEGER REFERENCES induk(id),
                    catatan TEXT);
INSERT INTO induk VALUES (1, 'Sari');
""")
print("induk:", c.execute("SELECT * FROM induk").fetchall())

P("H6.8  baris yatim tetap masuk")
c.execute("INSERT INTO anak VALUES (99, 777, 'induk 777 tidak ada')"); c.commit()
print("tersimpan:", c.execute("SELECT * FROM anak").fetchall())

P("H6.9  nyalakan PRAGMA")
c.execute("PRAGMA foreign_keys = ON")
print("sesudah ON:", c.execute("PRAGMA foreign_keys").fetchone()[0])
try:
    c.execute("INSERT INTO anak VALUES (100, 888, 'induk 888 tidak ada')")
except sqlite3.IntegrityError as e:
    print("ditolak:", e)

P("H6.10 periksa pelanggaran lama")
print(c.execute("PRAGMA foreign_key_check").fetchall())
c.close(); os.remove("fk.db")

# ---------------- HARI 7 ----------------
P("H7.1  bikin VIEW")
shutil.copy("besar.db", "vw.db")
c = sqlite3.connect("vw.db")
c.execute("""CREATE VIEW ringkas AS
SELECT cabang, substr(tanggal,1,7) AS bulan,
       COUNT(*) AS transaksi, SUM(nilai) AS omzet
FROM transaksi GROUP BY cabang, substr(tanggal,1,7)""")
def ukur2(sql, n=5):
    w = []
    for _ in range(n):
        t = time.perf_counter(); r = c.execute(sql).fetchall(); w.append(time.perf_counter()-t)
    return min(w)*1000, r
print("view dibuat")

P("H7.2  ukur VIEW")
mv, rv = ukur2("SELECT * FROM ringkas WHERE cabang='Kemang' ORDER BY bulan")
print(f"VIEW  : {mv:8.1f} ms   {len(rv)} baris")
print("baris pertama:", rv[0])

P("H7.3  bikin snapshot")
t = time.perf_counter()
c.execute("CREATE TABLE ringkas_snapshot AS SELECT * FROM ringkas"); c.commit()
print(f"sekali buat: {time.perf_counter()-t:.2f} detik")

P("H7.4  ukur snapshot")
mt, rt = ukur2("SELECT * FROM ringkas_snapshot WHERE cabang='Kemang' ORDER BY bulan", n=9)
print(f"TABEL : {mt:8.3f} ms   {len(rt)} baris")
print("isi sama?", rv == rt)
print(f"(kelipatan {mv/mt:.0f}x)")

P("H7.5  satu transaksi baru")
c.execute("INSERT INTO transaksi VALUES (9000001,'2024-06-01','Kemang',7,'Kopi Susu',1,22000)")
c.commit()
v = c.execute("SELECT omzet FROM ringkas          WHERE cabang='Kemang' AND bulan='2024-06'").fetchone()[0]
sn = c.execute("SELECT omzet FROM ringkas_snapshot WHERE cabang='Kemang' AND bulan='2024-06'").fetchone()[0]
print(f"view    : {v}")
print(f"snapshot: {sn}")
print(f"selisih : {v-sn}")
c.close(); os.remove("vw.db")

P("H7.6  python uji_mutu.py")
r = subprocess.run([sys.executable,"uji_mutu.py"],capture_output=True,text=True)
print(r.stdout.strip()); print("kode keluar:", r.returncode)

P("H7.7  versi pertama rekonsiliasi")
s2 = sqlite3.connect("senja.db")
q = """SELECT 'hanya di pesanan' AS sisi, id FROM pesanan
WHERE id NOT IN (SELECT id FROM pesanan_kasir)
UNION ALL
SELECT 'hanya di kasir', id FROM pesanan_kasir
WHERE id NOT IN (SELECT id FROM pesanan)"""
rr = s2.execute(q).fetchall()
print(len(rr), "baris bermasalah")
for x in rr[:3]: print("   ", x)

P("H7.8  pecah menurut status")
print(s2.execute("""SELECT status, COUNT(*) FROM pesanan
WHERE id NOT IN (SELECT id FROM pesanan_kasir) GROUP BY status""").fetchall())
