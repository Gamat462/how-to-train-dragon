import sqlite3, random
from datetime import date, timedelta
rng = random.Random(11)
con = sqlite3.connect("senja.db")
con.executescript("""
DROP TABLE IF EXISTS pelanggan; DROP TABLE IF EXISTS pesanan; DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS produk; DROP TABLE IF EXISTS pegawai; DROP TABLE IF EXISTS kunjungan;
DROP TABLE IF EXISTS pesanan_kasir;
CREATE TABLE pelanggan (id INTEGER PRIMARY KEY, nama TEXT, kota TEXT, tanggal_daftar TEXT, id_perujuk INTEGER);
CREATE TABLE produk    (id INTEGER PRIMARY KEY, nama TEXT, kategori TEXT, harga INTEGER, harga_beli INTEGER);
CREATE TABLE pesanan   (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, tanggal TEXT, cabang TEXT, kanal TEXT, status TEXT);
CREATE TABLE item      (id INTEGER PRIMARY KEY, pesanan_id INTEGER, produk_id INTEGER, jumlah INTEGER, harga_saat_itu INTEGER);
CREATE TABLE pegawai   (id INTEGER PRIMARY KEY, nama TEXT, jabatan TEXT, cabang TEXT, id_atasan INTEGER, gaji INTEGER);
CREATE TABLE kunjungan (id INTEGER PRIMARY KEY, pelanggan_id INTEGER, waktu TEXT);
CREATE TABLE pesanan_kasir (id INTEGER PRIMARY KEY, tanggal TEXT, cabang TEXT, nilai INTEGER);
""")
produk = [(1,"Kopi Susu","Minuman",22000,7000),(2,"Americano","Minuman",18000,5000),
          (3,"Teh Manis","Minuman",10000,2000),(4,"Roti Bakar","Makanan",15000,6000),
          (5,"Croissant","Makanan",25000,11000),(6,"Cheesecake","Makanan",30000,None),
          (7,"Matcha Latte","Minuman",26000,None)]
con.executemany("INSERT INTO produk VALUES (?,?,?,?,?)", produk)
kota = ["Jakarta","Bandung","Yogyakarta",None]
nama = ["Rina","Bayu","Sari","Dimas","Putri","Agus","Maya","Fajar","Intan","Yoga",
        "Nadia","Reza","Lita","Hendra","Tari","Wawan","Sinta","Bagus","Vira","Andi"]
con.executemany("INSERT INTO pelanggan VALUES (?,?,?,?,?)", [
    (i, n, kota[rng.randrange(4)], (date(2023,1,1)+timedelta(days=rng.randrange(500))).isoformat(),
     (rng.choice([None,None,rng.randint(1,max(1,i-1))]) if i>1 else None)) for i,n in enumerate(nama,1)])
con.executemany("INSERT INTO pegawai VALUES (?,?,?,?,?,?)", [
    (1,"Pak Hardi","Pemilik",None,None,25000000),(2,"Bu Rina","Manajer Area","Jakarta",1,14000000),
    (3,"Sinta","Kepala Cabang","Kemang",2,9000000),(4,"Bagus","Kepala Cabang","Dago",2,8500000),
    (5,"Vira","Kepala Cabang","Seturan",2,8500000),(6,"Andi","Barista","Kemang",3,4500000),
    (7,"Tari","Barista","Kemang",3,4500000),(8,"Wawan","Barista","Dago",4,4200000),
    (9,"Yoga","Kasir","Seturan",5,4000000),(10,"Lita","Kasir","Kemang",3,4000000)])
cab=["Kemang","Dago","Seturan"]; kan=["Dine-in","Take-away","Ojol"]; pid=iid=1
for _ in range(400):
    p = rng.choice([None]+list(range(1,18))+list(range(1,18)))
    con.execute("INSERT INTO pesanan VALUES (?,?,?,?,?,?)", (pid, p,
        (date(2024,1,1)+timedelta(days=rng.randrange(182))).isoformat(),
        rng.choice(cab), rng.choice(kan), rng.choices(["selesai","batal"],weights=[92,8])[0]))
    for _ in range(rng.randint(1,3)):
        pr = rng.randrange(1,8)
        con.execute("INSERT INTO item VALUES (?,?,?,?,?)", (iid,pid,pr,rng.randint(1,4),produk[pr-1][3])); iid+=1
    pid+=1
kid=1
for p in range(1,21):
    t = date(2024,3,1)
    for _ in range(rng.randint(3,12)):
        t += timedelta(days=rng.choice([0,0,1,1,2,5,9,20]))
        con.execute("INSERT INTO kunjungan VALUES (?,?,?)",
                    (kid,p,t.isoformat()+f" {rng.randrange(8,21):02d}:{rng.randrange(60):02d}")); kid+=1
nilai = dict(con.execute("""SELECT o.id, SUM(i.jumlah*i.harga_saat_itu) FROM pesanan o
    JOIN item i ON i.pesanan_id=o.id WHERE o.status='selesai' GROUP BY o.id""").fetchall())
info = {r[0]:(r[1],r[2]) for r in con.execute("SELECT id,tanggal,cabang FROM pesanan")}
beda = {12:50000, 199:-25000}
for oid,v in nilai.items():
    if oid in (7,88,251): continue
    con.execute("INSERT INTO pesanan_kasir VALUES (?,?,?,?)", (oid,info[oid][0],info[oid][1],v+beda.get(oid,0)))
for e,v in [(9001,120000),(9002,75000)]:
    con.execute("INSERT INTO pesanan_kasir VALUES (?,?,?,?)", (e,"2024-04-15","Kemang",v))
con.commit()
print("Basis data 'senja.db' siap.")
for t in ["pelanggan","produk","pesanan","item","pegawai","kunjungan","pesanan_kasir"]:
    print(f"  {t:<14}", con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "baris")
