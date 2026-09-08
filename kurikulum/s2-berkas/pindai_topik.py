"""Memindai seluruh modul kurikulummu dan menghitung berapa modul yang benar-benar
membahas tiap topik yang menyusun silabus S2 Data Science (Jalur S2, Hari 2).

Jalankan dari folder paket, tempat folder kurikulum/ berada:

    python pindai_topik.py
    python pindai_topik.py /jalur/ke/kurikulum

Sebuah modul dihitung "membahas" kalau topiknya disebut minimal tiga kali —
sekali dua kali biasanya cuma sebutan sambil lalu. Kolom terakhir menyebut modul
yang paling banyak membahasnya, supaya kamu tahu ke mana harus pergi.
"""
import pathlib
import re
import sys

AMBANG = 3   # minimal berapa kali disebut supaya dihitung "membahas"

TOPIK = [
    ("pandas / pembersihan data",      r"\bpandas\b|read_excel|read_csv"),
    ("SQL join & agregasi",            r"\bJOIN\b|GROUP BY"),
    ("Git & rekayasa perangkat lunak", r"\bgit\b|GitHub|pull request"),
    ("A/B test",                       r"A/B|uji A/B|p-value|nilai-p"),
    ("visualisasi",                    r"matplotlib|seaborn|plotly|bar_chart|diagram batang"),
    ("rekayasa data / pipeline",       r"\bpipeline\b|\bdbt\b|\bETL\b"),
    ("big data / Spark / cloud",       r"\bSpark\b|BigQuery|gudang data"),
    ("desain & indeks basis data",     r"CREATE TABLE|CREATE INDEX|EXPLAIN|primary key|normalisasi"),
    ("window function",                r"ROW_NUMBER|PARTITION BY|fungsi jendela"),
    ("machine learning",               r"scikit-learn|machine learning|pembelajaran mesin"),
    ("regresi",                        r"\bregresi\b|regression"),
    ("statistik inferensial",          r"selang kepercayaan|uji hipotesis|distribusi sampel|galat baku"),
    ("etika & privasi data",           r"privasi|kerahasiaan|anonimisasi|\betika\b"),
    ("kalkulus / turunan",             r"\bturunan\b|kalkulus|\bgradien\b"),
    ("probabilitas formal",            r"probabilitas|teorema Bayes|peubah acak"),
    ("aljabar linear / matriks",       r"aljabar linear|perkalian matriks|dot product|vektor"),
    ("optimisasi",                     r"optimisasi|gradient descent|fungsi konveks|pengali Lagrange"),
    ("deep learning",                  r"deep learning|jaringan saraf|neural network"),
]

def tanpa_kode_halaman(t):
    """Buang <script> dan <style>: 'z-index' di CSS bukan pelajaran basis data."""
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    return re.sub(r"<style.*?</style>", "", t, flags=re.S)

def main():
    akar = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "kurikulum")
    berkas = sorted(akar.glob("*.html"))
    if not berkas:
        print(f"tidak ada berkas .html di {akar}/ — jalankan dari folder paketnya")
        raise SystemExit(2)

    isi = [(f.name, tanpa_kode_halaman(f.read_text(encoding="utf-8"))) for f in berkas]
    print(f"memindai {len(isi)} modul di {akar}/  (ambang: disebut >= {AMBANG} kali)\n")
    print(f"{'topik dalam silabus S2':32}{'modul':>6}   modul yang paling membahasnya")

    hasil = []
    for nama, pola in TOPIK:
        hitung = [(len(re.findall(pola, t, re.I)), n) for n, t in isi]
        cocok = [(c, n) for c, n in hitung if c >= AMBANG]
        utama = max(hitung)[1] if max(hitung)[0] >= AMBANG else "-"
        hasil.append((len(cocok), nama, utama))

    for n, nama, utama in hasil:
        print(f"{nama:32}{n:>6}   {utama}")

    tipis = [(n, nama) for n, nama, _ in hasil if n <= 1]
    print(f"\ntopik yang cuma ditopang satu modul atau kurang: {len(tipis)}")
    for n, nama in tipis:
        print(f"  {n} modul  -  {nama}")

if __name__ == "__main__":
    main()
