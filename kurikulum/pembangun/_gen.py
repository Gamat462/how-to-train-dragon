# -*- coding: utf-8 -*-
"""Generator modul terpandu — memakai kerangka gaya yang sama dengan 50 modul lain."""
import html, pathlib, re

AKAR = pathlib.Path(__file__).resolve().parent.parent

def _kerangka():
    kepala = (AKAR/"s2/_kepala.html").read_text(encoding="utf-8")
    ekor   = (AKAR/"s2/_ekor.html").read_text(encoding="utf-8")
    return kepala, ekor

def bangun(judul_tab, kunci_simpan, eyebrow, h1, lede_paras, nav_lbl, hari, footer_html,
           kembali_href, kembali_teks):
    kepala, ekor = _kerangka()
    kepala = re.sub(r"<title>.*?</title>", f"<title>{judul_tab}</title>", kepala, count=1)
    ekor   = ekor.replace("jalur-s2-luar-negeri-v1", kunci_simpan)

    b = [kepala]
    b.append(f'\n<div class="kembali"><a href="{kembali_href}">← Kembali ke {kembali_teks}</a></div>\n')
    b.append('<nav class="nav" aria-label="Pilih hari">')
    b.append(f'  <span class="lbl">{nav_lbl}</span>')
    for i, h in enumerate(hari, 1):
        sel = "true" if i == 1 else "false"
        b.append(f'  <button type="button" data-hari="{i}" aria-selected="{sel}">{h["tab"]}</button>')
    b.append('</nav>\n')
    b.append('<div class="page">\n')
    b.append('  <header>')
    b.append(f'    <span class="eyebrow mono">{eyebrow}</span>')
    b.append(f'    <h1>{h1}</h1>')
    for j, p in enumerate(lede_paras):
        gaya = '' if j == 0 else ' style="margin-top:10px"'
        b.append(f'    <p class="lede"{gaya}>{p}</p>')
    b.append('''
    <div class="kemajuan">
      <span id="teks-kemajuan">0 dari 0 langkah</span>
      <span class="bar"><span id="isi-bar"></span></span>
    </div>
  </header>\n''')

    for i, h in enumerate(hari, 1):
        aktif = " aktif" if i == 1 else ""
        b.append(f'  <section class="day{aktif}" data-hari="{i}">')
        b.append('    <div class="day-head">')
        # Modul yang penomoran harinya tidak mulai dari 1 (mis. M11 = Hari 71-77)
        # menaruh labelnya sendiri di kunci "n".
        b.append(f'      <span class="n">{h.get("n", f"HARI {i}")}</span>')
        b.append(f'      <h2>{h["judul"]}</h2>')
        b.append(f'      <span class="waktu">{h["waktu"]}</span>')
        b.append('    </div>')
        b.append(f'    <div class="tujuan"><strong>Tujuan hari ini:</strong> {h["tujuan"]}</div>\n')
        for k, s in enumerate(h["langkah"], 1):
            cid = f'{kunci_simpan}-{i}-{k}'
            b.append('    <div class="langkah">')
            b.append('      <div class="langkah-head">')
            b.append(f'        <span class="num">{k}</span>')
            b.append(f'        <h3>{s["judul"]}</h3>')
            b.append(f'        <span class="cek"><input type="checkbox" id="{cid}"><label for="{cid}">selesai</label></span>')
            b.append('      </div>')
            b.append(f'      <div class="langkah-body">\n{s["isi"]}\n      </div>')
            b.append('    </div>\n')
        b.append('    <div class="selesai-hari">')
        b.append(f'      <h3>{h["tutup_judul"]}</h3>')
        b.append(f'      {h["tutup"]}')
        b.append('    </div>')
        b.append('  </section>\n')

    b.append(f'  <footer>\n{footer_html}\n    <button class="tombol-reset" type="button" id="reset">Kosongkan semua centang</button>\n  </footer>\n</div>\n')
    b.append(ekor)
    return "\n".join(b)

def kode(teks, salin=True):
    tombol = '<button class="salin" type="button">Salin</button>\n        ' if salin else ''
    return f'        <div class="kode">{tombol}<pre><code>{html.escape(teks)}</code></pre></div>'

def tabel(kepala, baris, kelas_n=()):
    KN = ' class="n"'
    o = ['        <div class="tabel-bungkus">', '          <table>', '            <thead><tr>']
    for j, k in enumerate(kepala):
        o.append("<th" + (KN if j in kelas_n else "") + ">" + str(k) + "</th>")
    o.append('</tr></thead>')
    o.append('            <tbody>')
    for r in baris:
        sel = "".join("<td" + (KN if j in kelas_n else "") + ">" + str(c) + "</td>"
                      for j, c in enumerate(r))
        o.append('              <tr>' + sel + '</tr>')
    o.append('            </tbody>')
    o.append('          </table>')
    o.append('        </div>')
    return "\n".join(o)

def blok(jenis, isi, tag=None):
    t = f'<span class="tag">{tag}</span>\n          ' if tag else ''
    return f'        <div class="{jenis}">{t}{isi}</div>'
