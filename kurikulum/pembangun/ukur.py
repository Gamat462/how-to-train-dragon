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
    return dict(
        hari=hari, langkah=langkah,
        lgkh_hr=langkah / hari if hari else 0,
        kata=statistics.mean(kata) if kata else 0,
        med=statistics.median(panjang) if panjang else 0,
        maks=max(panjang) if panjang else 0,
        kode=len(panjang), kotak=kotak,
        rasio=kotak / len(panjang) if panjang else 0,
    )

TARGET = dict(lgkh_hr=5, kata=120, med=4, maks=15, rasio=0.7)

def jarak(m):
    d = 0
    d += max(0, (TARGET["lgkh_hr"] - m["lgkh_hr"]) / TARGET["lgkh_hr"])
    d += max(0, (m["kata"] - TARGET["kata"]) / TARGET["kata"])
    d += max(0, (m["med"] - TARGET["med"]) / TARGET["med"])
    d += max(0, (m["maks"] - TARGET["maks"]) / TARGET["maks"])
    d += max(0, (TARGET["rasio"] - m["rasio"]) / TARGET["rasio"])
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
print(f"{'jarak':>6} {'slug':30} {'hr':>3} {'lgkh':>5} {'l/hr':>5} {'kata':>5} {'med':>4} {'maks':>5} {'rasio':>6}")
for d, slug, judul, m in hasil:
    print(f"{d:6.2f} {slug[:30]:30} {m['hari']:3d} {m['langkah']:5d} {m['lgkh_hr']:5.1f} {m['kata']:5.0f} {m['med']:4.0f} {m['maks']:5d} {m['rasio']:6.2f}")
print("\njumlah modul terukur:", len(hasil))
print("sudah memenuhi standar (jarak 0):", sum(1 for d,_,_,_ in hasil if d == 0))
