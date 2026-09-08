import os, re, shutil, pathlib
# Akar = folder tempat skrip ini berada, bukan jalur mutlak.
# Sebelumnya jalur scratchpad ditulis mati di sini, sehingga menjalankannya
# dari klon repo diam-diam menulis ke folder sesi lama — bukan ke klonnya.
BASE = pathlib.Path(__file__).resolve().parent
os.chdir(BASE)
exec(open('_peta.py').read())
exec(open('_slug.py').read())

OUT = BASE / "paket" / "Rute-Data-Analyst"
if OUT.parent.exists(): shutil.rmtree(OUT.parent)
(OUT / "kurikulum").mkdir(parents=True)
(OUT / "data-dan-skrip").mkdir(parents=True)

POLA = re.compile(r'https://claude\.ai/code/artifact/([0-9a-f-]{36})')
tak_dikenal = set()

def lokalkan(teks, dari_kurikulum=True):
    def ganti(m):
        i = m.group(1)
        if i not in SLUG:
            tak_dikenal.add(i); return m.group(0)
        return (SLUG[i] + ".html") if dari_kurikulum else ("kurikulum/" + SLUG[i] + ".html")
    return POLA.sub(ganti, teks)

# --- salin + tulis ulang tautan ---
disalin = []
for i, (berkas, urut, judul, hari) in sorted(PETA.items(), key=lambda kv: kv[1][1]):
    src = BASE / berkas
    dst = OUT / "kurikulum" / (SLUG[i] + ".html")
    dst.write_text(lokalkan(src.read_text()))
    disalin.append((urut, SLUG[i], judul, hari, dst.stat().st_size))

print("berkas kurikulum disalin:", len(disalin))
print("id tanpa slug yang ditemukan di isi:", tak_dikenal or "tidak ada")

# --- data & skrip ---
D = OUT / "data-dan-skrip"
(D / "sql-mahir").mkdir()
for f in ["gen_final.py", "besar.py", "uji_mutu.py"]:
    shutil.copy(BASE / "sql" / f, D / "sql-mahir" / f)

(D / "python-produksi").mkdir()
(D / "python-produksi" / "laporan").mkdir()
(D / "python-produksi" / "tests").mkdir()
for f in ["__init__.py", "bersih.py", "hitung.py", "cli.py"]:
    shutil.copy(BASE / "pp-berkas" / "laporan" / f, D / "python-produksi" / "laporan" / f)
shutil.copy(BASE / "pp-berkas" / "tests" / "test_bersih.py",
            D / "python-produksi" / "tests" / "test_bersih.py")

(D / "studi-kasus").mkdir()
for f in sorted((BASE / "kasus").glob("gen_k*.py")) + sorted((BASE / "kasus").glob("sol_k*.py")):
    shutil.copy(f, D / "studi-kasus" / f.name)

(D / "bekal-data-klien").mkdir()
for f in ["gen_final.py"]:
    shutil.copy(BASE / "klien" / f, D / "bekal-data-klien" / f)
for f in (BASE / "klien").glob("*.xlsx"):
    shutil.copy(f, D / "bekal-data-klien" / f.name)

(D / "proyek-buta").mkdir()
for f in (BASE / "buta").glob("P[123]*"):
    shutil.copy(f, D / "proyek-buta" / f.name)
shutil.copy(BASE / "buta" / "periksa.py", D / "proyek-buta" / "periksa.py")

(D / "minggu-11").mkdir()
shutil.copy(BASE / "m11-berkas" / "buat_contoh.py", D / "minggu-11" / "buat_contoh.py")

(D / "minggu-14").mkdir()
for f in ["periksa_readme.py", "periksa_cv.py", "cv-lemah.txt", "cv-kuat.txt",
          "iklan.txt", "buat_soal_sql.py", "jalankan.py"]:
    shutil.copy(BASE / "m14-berkas" / f, D / "minggu-14" / f)

(D / "jalur-s2").mkdir()
for f in ["hitung_s2.py", "hitung_tenggat.py", "pindai_topik.py", "skor_rubrik.py"]:
    shutil.copy(BASE / "s2-berkas" / f, D / "jalur-s2" / f)

if (BASE / "bootcamp").exists():
    shutil.copytree(BASE / "bootcamp", D / "bootcamp-jalur-utama")

print("\nisi data-dan-skrip:")
for p in sorted(D.rglob("*")):
    if p.is_file():
        print(f"  {p.relative_to(D)}  ({p.stat().st_size//1024} KB)" if p.stat().st_size > 1024
              else f"  {p.relative_to(D)}")
