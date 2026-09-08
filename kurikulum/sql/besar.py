import sqlite3, random, time
from datetime import date, timedelta
rng = random.Random(7)
con = sqlite3.connect("besar.db")
con.executescript("DROP TABLE IF EXISTS transaksi;")
con.execute("""CREATE TABLE transaksi (
  id INTEGER PRIMARY KEY, tanggal TEXT, cabang TEXT, pelanggan_id INTEGER,
  produk TEXT, jumlah INTEGER, nilai INTEGER)""")
cab = ["Kemang","Dago","Seturan","Renon","Seturan2"]
prd = ["Kopi Susu","Americano","Teh Manis","Roti Bakar","Croissant","Cheesecake","Matcha Latte"]
t0 = time.time()
rows = []
for i in range(1, 800001):
    d = date(2023,1,1) + timedelta(days=rng.randrange(730))
    j = rng.randint(1,4)
    rows.append((i, d.isoformat(), cab[rng.randrange(5)], rng.randint(1,50000),
                 prd[rng.randrange(7)], j, j*rng.choice([10000,15000,18000,22000,25000,26000,30000])))
    if len(rows) == 100000:
        con.executemany("INSERT INTO transaksi VALUES (?,?,?,?,?,?,?)", rows); rows=[]
if rows: con.executemany("INSERT INTO transaksi VALUES (?,?,?,?,?,?,?)", rows)
con.commit()
print(f"dibuat dalam {time.time()-t0:.1f} detik")
print("baris:", con.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0])
import os; print(f"ukuran berkas: {os.path.getsize('besar.db')/1e6:.1f} MB")
