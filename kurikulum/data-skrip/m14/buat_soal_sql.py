"""Membuat wawancara.duckdb untuk latihan soal SQL wawancara (Minggu 14 Hari 97-98).

Dua tabel:
  pengguna(id, nama, tanggal_daftar, kota)
  pesanan(id, user_id, tanggal, nilai)

Angka acaknya berkunci tetap (Random(97)), jadi hasil querymu sama persis
dengan yang tertulis di modul.
"""
import random
from datetime import date, timedelta
import duckdb

rng = random.Random(97)
KOTA = ["Jakarta", "Bandung", "Surabaya", "Medan"]
DEPAN = ["Andi", "Bella", "Citra", "Dimas", "Eka", "Farhan", "Gita", "Hana",
         "Irfan", "Jihan", "Kirana", "Lukman", "Mira", "Naufal", "Okta", "Putri"]
BLKG = ["Pratama", "Wijaya", "Saputra", "Ramadhan", "Anggraini", "Nugroho"]

AWAL, AKHIR = date(2025, 10, 1), date(2026, 6, 30)

pengguna, pesanan = [], []
for uid in range(1, 121):
    nama = f"{DEPAN[(uid - 1) % 16]} {BLKG[rng.randrange(6)]}"
    daftar = date(2025, 10, 1) + timedelta(days=rng.randrange(150))   # Okt 2025 - Feb 2026
    pengguna.append((uid, nama, daftar, KOTA[rng.randrange(4)]))
    sisa = (AKHIR - daftar).days
    for _ in range(rng.choice([0, 1, 1, 2, 2, 3, 4, 5, 7])):
        pesanan.append((len(pesanan) + 1, uid,
                        daftar + timedelta(days=rng.randrange(sisa + 1)),
                        rng.randrange(50, 900) * 1000))

con = duckdb.connect("wawancara.duckdb")
con.execute("DROP TABLE IF EXISTS pesanan")
con.execute("DROP TABLE IF EXISTS pengguna")
con.execute("CREATE TABLE pengguna(id INTEGER, nama VARCHAR, tanggal_daftar DATE, kota VARCHAR)")
con.execute("CREATE TABLE pesanan(id INTEGER, user_id INTEGER, tanggal DATE, nilai BIGINT)")
con.executemany("INSERT INTO pengguna VALUES (?,?,?,?)", pengguna)
con.executemany("INSERT INTO pesanan VALUES (?,?,?,?)", pesanan)

print("pengguna:", len(pengguna))
print("pesanan :", len(pesanan))
print("pengguna tanpa pesanan:", con.execute(
    "SELECT COUNT(*) FROM pengguna u "
    "WHERE NOT EXISTS (SELECT 1 FROM pesanan p WHERE p.user_id = u.id)").fetchone()[0])
con.close()
