import sqlite3, sys

# batas = berapa banyak baris bermasalah yang MASIH boleh ada.
# 0 = harus bersih.  Angka di atas 0 adalah utang yang sudah kita tahu,
# dan angkanya tidak boleh naik tanpa kita sadari.
PEMERIKSAAN = [
 dict(nama="Pesanan tanpa pelanggan", batas=12,
      sql="SELECT id FROM pesanan WHERE pelanggan_id IS NULL"),
 dict(nama="Produk tanpa harga beli", batas=2,
      sql="SELECT id, nama FROM produk WHERE harga_beli IS NULL"),
 dict(nama="Pelanggan tanpa kota", batas=6,
      sql="SELECT id, nama FROM pelanggan WHERE kota IS NULL"),
 dict(nama="Item menunjuk pesanan hantu", batas=0,
      sql="""SELECT i.id FROM item i
             LEFT JOIN pesanan p ON p.id = i.pesanan_id WHERE p.id IS NULL"""),
 dict(nama="Jumlah atau harga tidak masuk akal", batas=0,
      sql="SELECT id FROM item WHERE jumlah <= 0 OR harga_saat_itu <= 0"),
 dict(nama="Pesanan selesai yang hilang dari kasir", batas=0,
      sql="""SELECT id FROM pesanan WHERE status = 'selesai'
             AND id NOT IN (SELECT id FROM pesanan_kasir)"""),
 dict(nama="Struk kasir tanpa pesanan", batas=0,
      sql="""SELECT id FROM pesanan_kasir
             WHERE id NOT IN (SELECT id FROM pesanan)"""),
 dict(nama="Nilai pesanan beda antara sistem dan kasir", batas=0,
      sql="""SELECT p.id, k.nilai - SUM(i.jumlah * i.harga_saat_itu) AS selisih
             FROM pesanan p
             JOIN item i          ON i.pesanan_id = p.id
             JOIN pesanan_kasir k ON k.id = p.id
             GROUP BY p.id HAVING selisih <> 0"""),
]

con = sqlite3.connect("senja.db")
gagal = 0
for p in PEMERIKSAAN:
    baris = con.execute(p["sql"]).fetchall()
    n, batas = len(baris), p["batas"]
    if n > batas:
        gagal += 1
        print(f"GAGAL  {p['nama']}: {n} baris (batas {batas})")
        for b in baris[:3]:
            print(f"          {b}")
    elif n == batas and batas > 0:
        print(f"utang  {p['nama']}: {n} baris (sesuai batas {batas})")
    else:
        print(f"bersih {p['nama']}")

print(f"\n{len(PEMERIKSAAN) - gagal} lolos, {gagal} gagal")
sys.exit(1 if gagal else 0)
