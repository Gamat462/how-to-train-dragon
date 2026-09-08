# -*- coding: utf-8 -*-
"""Menjalankan query modul ke PostgreSQL sungguhan, lalu menyimpan hasilnya.

Alasan berkas ini ada: aturan nomor 1 di CLAUDE.md — tiap angka di modul harus
dihasilkan dengan menjalankan kodenya. Dulu keluarannya disalin tangan dari
terminal ke berkas pembangun, dan salin-tangan bisa meleset. Sekarang:

    python3 <slug>/jalankan.py      # menjalankan semua query -> hasil.json
    python3 <slug>/bangun.py        # membaca hasil.json, menulis HTML

Kalau sebuah query gagal, pesan errornya ikut tersimpan apa adanya — itu yang
dipakai untuk kotak "HARUS MUNCUL — TULISAN MERAH".
"""
import html as _html, json, pathlib, re

DSN = "host=127.0.0.1 port=5433 user=postgres dbname=senja"


def jalankan(kueri, tujuan, dsn=DSN):
    """kueri: dict slug -> SQL. Menulis tujuan (JSON) berisi hasil tiap slug."""
    import psycopg
    hasil = {}
    for slug, sql in kueri.items():
        with psycopg.connect(dsn, autocommit=True) as con:
            with con.cursor() as cur:
                try:
                    cur.execute(sql)
                    kolom = [d.name for d in cur.description]
                    baris = [[_teks(v) for v in r] for r in cur.fetchall()]
                    hasil[slug] = {"kolom": kolom, "baris": baris}
                except Exception as e:
                    hasil[slug] = {"galat": _pesan(e)}
    pathlib.Path(tujuan).write_text(
        json.dumps(hasil, ensure_ascii=False, indent=1), encoding="utf-8")
    return hasil


def _teks(v):
    if v is None:
        return None
    if v is True:
        return "true"
    if v is False:
        return "false"
    return str(v)


def _pesan(e):
    """Pesan error PostgreSQL apa adanya, tanpa jejak Python."""
    return str(e).strip()


def muat(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


def keluaran(H, slug, batas=None, tag=None, catatan=None):
    """Kotak HARUS MUNCUL, isinya hasil sungguhan dari hasil.json."""
    h = H[slug]
    if "galat" in h:
        t = tag or "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"
        return ('        <div class="hasil"><span class="tag">' + t + '</span>\n'
                '          <pre><code>' + _html.escape(h["galat"]) + '</code></pre></div>')
    kolom, baris = h["kolom"], h["baris"]
    tampil = baris if batas is None else baris[:batas]

    def angka(j):
        ada = [r[j] for r in baris if r[j] is not None]
        return bool(ada) and all(re.fullmatch(r"-?\d+(\.\d+)?", v) for v in ada)

    kn = [angka(j) for j in range(len(kolom))]
    K = lambda j: ' class="n"' if kn[j] else ''
    o = ['        <div class="hasil"><span class="tag">' + (tag or "HARUS MUNCUL") + '</span>',
         '          <div class="tabel-bungkus">', '            <table>',
         '              <thead><tr>' +
         "".join('<th' + K(j) + '>' + _html.escape(k) + '</th>'
                 for j, k in enumerate(kolom)) +
         '</tr></thead>', '              <tbody>']
    for r in tampil:
        sel = "".join(
            '<td' + K(j) + '>' + ('<span class="nihil">NULL</span>' if v is None
                                  else _html.escape(v)) + '</td>'
            for j, v in enumerate(r))
        o.append('                <tr>' + sel + '</tr>')
    o.append('              </tbody>')
    o.append('            </table>')
    o.append('          </div>')
    n = len(baris)
    sisa = ("" if batas is None or n <= batas
            else f" — ditampilkan {batas} teratas dari {n}")
    o.append(f'          <p class="cacah">({n} baris{sisa})</p>')
    if catatan:
        o.append('          <p style="margin-top:8px">' + catatan + '</p>')
    o.append('        </div>')
    return "\n".join(o)
