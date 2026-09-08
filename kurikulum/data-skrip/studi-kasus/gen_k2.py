"""Kasus 2 — Klinik Pratama Sehat Bersama.
Dua berkas dari dua aplikasi berbeda yang harus disambung:
  kunjungan.xlsx  -> ID pasien tersimpan sebagai ANGKA (nol di depan hilang)
  tagihan.csv     -> ID pasien sebagai TEKS '0007', pemisah ';', desimal ','
"""
import random, csv
from datetime import date, timedelta
from openpyxl import Workbook

rng = random.Random(7)

NAMA = [
 (1, "Siti Nurhaliza"), (2, "Ahmad Fauzi"), (3, "Dewi Lestari"), (4, "Bambang Wijaya"),
 (5, "Rina Marlina"), (6, "Joko Susilo"), (7, "Maya Sari"), (8, "Hendra Gunawan"),
 (9, "Fitri Handayani"), (10, "Agus Setiawan"), (11, "Nur Aini"), (12, "Rudi Hartono"),
 (13, "Lilis Suryani"), (14, "Dedi Kurniawan"), (15, "Sri Wahyuni"),
]
# variasi ejaan nama untuk pasien yang sama (dientri ulang oleh petugas berbeda)
VARIASI = {
 1: ["Siti Nurhaliza", "Siti Nurhalizah", "SITI NURHALIZA", "siti nurhaliza"],
 4: ["Bambang Wijaya", "Bambang Widjaja", "BAMBANG WIJAYA"],
 9: ["Fitri Handayani", "Fitri Handayanti"],
}
LAYANAN = [
 ("Pemeriksaan Umum",       50000),
 ("Pemeriksaan Gigi",      150000),
 ("Cek Laboratorium",      275000),
 ("Suntik Imunisasi",      120000),
 ("Kontrol Kehamilan",     180000),
 ("Perawatan Luka",         85000),
]
PENJAMIN = ["BPJS", "bpjs", "B.P.J.S", "BPJS Kesehatan", "Umum", "umum", "UMUM",
            "Asuransi", "asuransi swasta"]

kunjungan = []
kode = 0
for _ in range(240):
    kode += 1
    pid = rng.randrange(1, 16)
    nama = rng.choice(VARIASI.get(pid, [dict(NAMA)[pid]]))
    d = date(2024, 1, 1) + timedelta(days=rng.randrange(182))
    lay, tarif = LAYANAN[rng.randrange(len(LAYANAN))]
    pj = PENJAMIN[rng.randrange(len(PENJAMIN))]
    kunjungan.append(dict(kode=f"K{kode:04d}", pid=pid, nama=nama, tgl=d,
                          layanan=lay, tarif=tarif, penjamin=pj))

# --- kunjungan.xlsx : ID pasien sebagai ANGKA ---
wb = Workbook(); ws = wb.active; ws.title = "Kunjungan"
ws.append(["Kode Kunjungan", "ID Pasien", "Nama Pasien", "Tanggal", "Layanan", "Penjamin"])
for k in kunjungan:
    ws.append([k["kode"], k["pid"], k["nama"], k["tgl"].strftime("%d/%m/%Y"),
               k["layanan"], k["penjamin"]])
wb.save("Kunjungan Pasien 2024.xlsx")

# --- tagihan.csv : ID pasien sebagai TEKS berpadding, ';' dan desimal ',' ---
baris = []
no = 0
digandakan = 0
for k in kunjungan:
    # 92% kunjungan ada tagihannya
    if rng.random() > 0.92:
        continue
    no += 1
    diskon = rng.choice([0, 0, 0, 0, 0.10, 0.20])
    total = k["tarif"] * (1 - diskon)
    baris.append([f"INV{no:05d}", k["kode"], f"{k['pid']:04d}",
                  k["tgl"].strftime("%Y-%m-%d"),
                  f"{k['tarif']:.2f}".replace(".", ","),
                  f"{diskon*100:.2f}".replace(".", ","),
                  f"{total:.2f}".replace(".", ",")])
    # 4% tagihan tercatat DUA KALI untuk kunjungan yang sama
    if rng.random() < 0.04:
        no += 1
        digandakan += 1
        baris.append([f"INV{no:05d}", k["kode"], f"{k['pid']:04d}",
                      k["tgl"].strftime("%Y-%m-%d"),
                      f"{k['tarif']:.2f}".replace(".", ","),
                      f"{diskon*100:.2f}".replace(".", ","),
                      f"{total:.2f}".replace(".", ",")])

with open("Tagihan Klinik 2024.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["No Invoice","Kode Kunjungan","ID Pasien","Tanggal","Tarif","Diskon %","Total"])
    w.writerows(baris)

print("kunjungan       :", len(kunjungan))
print("tagihan (baris) :", len(baris))
print("tagihan ganda   :", digandakan)
print("kunjungan tanpa tagihan:", len(kunjungan) - (len(baris) - digandakan))
