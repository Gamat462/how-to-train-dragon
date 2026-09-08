# -*- coding: utf-8 -*-
import sys, pathlib
AKAR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR/"mat")); sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _gen import bangun
from h1 import HARI1
from h2 import HARI2
from h3 import HARI3
from h4 import HARI4
from h5 import HARI5

html = bangun(
  judul_tab="Studi Kasus Nyata",
  kunci_simpan="studi-kasus-nyata-v2",
  eyebrow="Studi Kasus Nyata · 5 berkas klien · ditulis ulang mengikuti pola Bekal Python",
  h1="Studi Kasus Nyata: lima berkas yang tidak satu pun memberi pesan error",
  lede_paras=[
    "Lima berkas klien sungguhan — toko bangunan, klinik, kontraktor, sekolah, dan daftar piutang. "
    "Tidak satu pun dari delapan jebakan di dalamnya menghasilkan <em>error</em>. Semuanya jalan mulus "
    "dan memberi angka yang terlihat wajar.",
    "Versi sebelumnya menaruh seluruh pembersihan dalam satu blok kode 100 baris. "
    "Versi ini memecahnya jadi <strong>64 langkah kecil</strong>, masing-masing satu gagasan, "
    "kode 1–4 baris, dan kotak <strong>HARUS MUNCUL</strong> di hampir setiap langkah — "
    "bentuk yang sama dengan Bekal Python.",
    "Semua angka di halaman ini dihasilkan dengan menjalankan kodenya pada berkas yang kamu buat sendiri. "
    "Dua angka di versi lama ternyata salah dan sudah diperbaiki di sini.",
  ],
  nav_lbl="Studi Kasus",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5],
  footer_html='    <p>Kemajuanmu tersimpan otomatis di browser ini. Kelima berkas dibuat oleh '
              '<code>gen_k1.py</code> sampai <code>gen_k5.py</code> di paket zip, dan setiap angka '
              '“HARUS MUNCUL” di halaman ini diperoleh dengan menjalankan kodenya pada berkas itu — '
              'pandas 3.0.5, Python 3.11.</p>',
  kembali_href="https://claude.ai/code/artifact/88ce46d0-54b8-4c0b-924d-beb4c8389d7a",
  kembali_teks="Bekal Data Klien",
)
out = AKAR/"minggu1/studi-kasus-nyata.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
