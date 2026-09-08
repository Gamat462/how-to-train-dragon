"""Pemeriksa CV sederhana untuk pelamar posisi data (Minggu 14 Hari 95).

Cara pakai:
    python periksa_cv.py cv.txt
    python periksa_cv.py cv.txt iklan.txt      # sekalian cek kata kunci iklan

cv.txt dibuat dengan menyalin seluruh teks dari PDF CV-mu (Ctrl+A, Ctrl+C di
pembaca PDF, lalu tempel ke berkas teks). Kalau hasil salinannya berantakan atau
kosong, itu sendiri sudah temuan: mesin penyaring membaca CV-mu sama seperti ini.
"""
import re
import sys

BAGIAN_WAJIB = ["experience", "education", "skills"]
KATA_LEMAH = ["responsible for", "helped with", "worked on", "assisted in",
              "involved in", "duties included"]

def kalimat_poin(teks):
    return [b.strip(" -•\t") for b in teks.splitlines()
            if b.strip().startswith(("-", "•", "*"))]

def periksa(cv, iklan=None):
    kata = cv.split()
    rendah = cv.lower()
    poin = kalimat_poin(cv)
    berangka = [p for p in poin if re.search(r"\d", p)]
    lemah = [k for k in KATA_LEMAH if k in rendah]
    hilang = [b for b in BAGIAN_WAJIB if b not in rendah]

    hasil = []
    hasil.append(("panjang", len(kata) <= 700,
                  f"{len(kata)} kata (batas wajar satu halaman: 700)"))
    hasil.append(("bagian baku", not hilang,
                  "lengkap" if not hilang else "tidak ada: " + ", ".join(hilang)))
    hasil.append(("email", bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", cv)), "kontak email"))
    hasil.append(("linkedin", "linkedin.com/in/" in rendah, "tautan LinkedIn"))
    hasil.append(("github", "github.com/" in rendah, "tautan GitHub"))
    hasil.append(("poin berangka", len(poin) > 0 and len(berangka) / len(poin) >= 0.6,
                  f"{len(berangka)} dari {len(poin)} poin memuat angka (target 60%)"))
    hasil.append(("tanpa kata lemah", not lemah,
                  "bersih" if not lemah else "ditemukan: " + ", ".join(lemah)))

    if iklan:
        kunci = sorted({w for w in re.findall(r"[A-Za-z][\w+#.]{2,}", iklan.lower())
                        if w in KAMUS_ALAT})
        belum = [k for k in kunci if k not in rendah]
        ket = f"{len(kunci) - len(belum)} dari {len(kunci)} kata kunci alat ada di CV"
        if belum:
            ket += " | belum ada: " + ", ".join(belum)
        hasil.append(("kata kunci iklan",
                      len(kunci) > 0 and (len(kunci) - len(belum)) / len(kunci) >= 0.7,
                      ket))
    return hasil

KAMUS_ALAT = {"sql", "python", "pandas", "dbt", "tableau", "looker", "airflow",
              "bigquery", "snowflake", "excel", "git", "spark", "powerbi",
              "statistics", "dashboard", "etl", "warehouse"}

def main():
    if len(sys.argv) < 2:
        print("pakai: python periksa_cv.py cv.txt [iklan.txt]")
        raise SystemExit(2)
    cv = open(sys.argv[1], encoding="utf-8").read()
    iklan = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else None

    hasil = periksa(cv, iklan)
    lolos = sum(1 for _, ok, _ in hasil if ok)
    for nama, ok, ket in hasil:
        print(f"[{'OK ' if ok else 'CEK'}] {nama:18} {ket}")
    print(f"\nlolos {lolos} dari {len(hasil)} pemeriksaan")
    raise SystemExit(0 if lolos == len(hasil) else 1)

if __name__ == "__main__":
    main()
