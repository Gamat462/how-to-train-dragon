# -*- coding: utf-8 -*-
"""Ukur tiap modul terhadap _pola.md. Semua angka hasil hitung, bukan kira-kira."""
import re, statistics, sys
from _urutan import URUTAN
from _slug import SLUG
from _peta import PETA

# slug -> berkas lokal
berkas = {}
for aid, v in PETA.items():
    berkas[SLUG[aid]] = v[0]

def bersih(h):
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    return h

def ukur(path):
    h = open(path, encoding="utf-8").read()
    h = bersih(h)
    hari = len(re.findall(r'<section class="day', h))
    langkah = len(re.findall(r'<div class="langkah"', h))
    # blok kode yang DIJALANKAN = punya tombol Salin
    dijalankan = re.findall(r'<button class="salin"[^>]*>.*?</button>\s*<pre><code>(.*?)</code></pre>', h, flags=re.S)
    panjang = [t.strip().count("\n") + 1 for t in dijalankan]
    kotak = len(re.findall(r'HARUS MUNCUL', h))
    # kata per langkah
    blok = re.findall(r'<div class="langkah">(.*?)(?=<div class="langkah">|<div class="selesai-hari">|<div class="grad">|</section>)', h, flags=re.S)
    kata = []
    for b in blok:
        b2 = re.sub(r"<pre>.*?</pre>", " ", b, flags=re.S)
        b2 = re.sub(r"<[^>]+>", " ", b2)
        kata.append(len(b2.split()))
    # --- ciri cara mengajar, diturunkan dari mengukur bekal-python.html ---
    # Kerangka saja (langkah pendek, kode pendek, kotak keluaran) ternyata
    # tidak cukup: dua modul bisa sama-sama berjarak 0 pada ukuran lama dan
    # tetap terasa berbeda dibaca. Lima ukuran di bawah menangkap bedanya.
    teks = re.sub(r"<[^>]+>", " ", h)
    teks = teks.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    per10 = (lambda n: n / langkah * 10) if langkah else (lambda n: 0)

    salah = len(re.findall(
        r"(?i)(tulisan merah|pesan merah|layar merah|Traceback|"
        r"Error: |Error\b[^<]{0,40}(not defined|failed|expected)|"
        r"AssertionError|IntegrityError|ModuleNotFoundError|sengaja gagal|"
        r"harus gagal|harus merah|lihat merahnya)", teks))
    tenang = len(re.findall(
        r"(?i)(itu normal|itu wajar|itu memang benar|bukan bencana|jangan panik|"
        r"tidak apa-apa|wajar kalau|normal kalau|memang disengaja|itu disengaja|"
        r"tidak perlu khawatir|biarkan saja|sabar)", teks))
    jembatan = len(re.findall(
        r"(?i)\b(excel|audit|auditor|kertas kerja|jurnal|neraca|debit|kredit|"
        r"rekonsiliasi|buku besar|laporan keuangan|klien)\b", teks))
    beda = len(re.findall(
        r"(?i)kalau (punyamu|hasilmu|angkamu|milikmu|layarmu|versimu|angka|hasil|"
        r"kamu tidak|tidak muncul|muncul|nomor|jumlahmu|waktunya|angkanya)", teks))
    sapa = len(re.findall(r"(?i)\bkamu\b", teks))

    return dict(
        hari=hari, langkah=langkah,
        lgkh_hr=langkah / hari if hari else 0,
        kata=statistics.mean(kata) if kata else 0,
        med=statistics.median(panjang) if panjang else 0,
        maks=max(panjang) if panjang else 0,
        kode=len(panjang), kotak=kotak,
        rasio=kotak / len(panjang) if panjang else 0,
        salah=per10(salah), tenang=per10(tenang), jemb=per10(jembatan),
        beda=per10(beda), sapa=sapa / langkah if langkah else 0,
    )

# Angka target = hasil mengukur bekal-python.html, modul acuan.
# lgkh_hr/kata/med/maks/rasio: kerangkanya.
# salah..sapa: cara mengajarnya, per 10 langkah (kecuali sapa: per langkah).
TARGET = dict(lgkh_hr=5, kata=120, med=4, maks=15, rasio=0.7,
              salah=1.5, tenang=1.2, jemb=0.9, beda=0.2, sapa=1.4)

# Ukuran yang dilanggar kalau NILAINYA TERLALU KECIL (lantai), bukan terlalu besar.
LANTAI = ("lgkh_hr", "rasio", "salah", "tenang", "jemb", "beda", "sapa")

def jarak(m):
    d = 0
    for k, t in TARGET.items():
        if k in LANTAI:
            d += max(0, (t - m[k]) / t)
        else:
            d += max(0, (m[k] - t) / t)
    return d

hasil = []
for slug, judul, hr, fase, cat in URUTAN:
    p = berkas.get(slug)
    if not p:
        continue
    try:
        m = ukur(p)
    except Exception as e:
        print("!!", slug, e); continue
    if m["hari"] == 0:
        continue
    hasil.append((jarak(m), slug, judul, m))

hasil.sort(reverse=True)
print(f"{'jarak':>6} {'slug':30} {'hr':>3} {'lgkh':>5} {'l/hr':>5} {'kata':>5} "
      f"{'med':>4} {'maks':>5} {'rasio':>6} | {'salah':>6} {'tenang':>6} {'jemb':>5} "
      f"{'beda':>5} {'sapa':>5}")
for d, slug, judul, m in hasil:
    print(f"{d:6.2f} {slug[:30]:30} {m['hari']:3d} {m['langkah']:5d} {m['lgkh_hr']:5.1f} "
          f"{m['kata']:5.0f} {m['med']:4.0f} {m['maks']:5d} {m['rasio']:6.2f} | "
          f"{m['salah']:6.1f} {m['tenang']:6.1f} {m['jemb']:5.1f} {m['beda']:5.1f} {m['sapa']:5.2f}")
print("\njumlah modul terukur:", len(hasil))
print("sudah memenuhi standar (jarak 0):", sum(1 for d,_,_,_ in hasil if d == 0))
