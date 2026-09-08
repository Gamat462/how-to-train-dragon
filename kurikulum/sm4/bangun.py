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
from h6 import HARI6
from h7 import HARI7

html = bangun(
  judul_tab="SQL Mahir L4",
  kunci_simpan="sql-mahir-l4-v2",
  eyebrow="SQL Mahir · Level 4 dari 5 · ditulis ulang mengikuti pola Bekal Python",
  h1="SQL Mahir L4: cepat, dan tidak diam-diam salah",
  lede_paras=[
    "Sampai Level 3 semua query-mu <strong>benar</strong>. Level ini soal dua hal yang baru "
    "terasa ketika datanya besar dan klienmu nyata: <strong>berapa lama query-nya jalan</strong>, "
    "dan <strong>apakah angkanya bisa dipercaya</strong> ketika ada yang gagal di tengah jalan.",
    "Tujuh hari, 87 langkah. Hampir tiap langkah menyuruhmu menjalankan satu atau dua baris, "
    "lalu mencocokkan keluaranmu dengan kotak <strong>HARUS MUNCUL</strong>. "
    "Kamu tidak akan membaca satu pun klaim kinerja dari saya yang tidak bisa kamu ukur sendiri "
    "dalam semenit.",
    "Semua angka di halaman ini keluar dari <strong>satu kali putaran skrip</strong> pada tabel "
    "800.000 baris yang kamu bikin sendiri di Hari 1 (Python 3.11.15, SQLite 3.45.1). "
    "Angka <em>milidetik</em>-mu akan berbeda — mesinnya beda. Yang harus sama: "
    "jumlah barisnya, ukuran berkasnya, dan kata <strong>SCAN</strong> atau "
    "<strong>SEARCH</strong> di tiap rencana.",
  ],
  nav_lbl="SQL L4",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Dua skrip yang dipakai modul ini — '
    '<code>besar.py</code> (pembuat tabel 800.000 baris) dan <code>uji_mutu.py</code> '
    '(delapan pemeriksaan mutu) — ada di <code>data-dan-skrip/sql-mahir/</code> di paket zip.</p>\n'
    '    <p style="margin-top:10px"><strong>Dari mana angkanya.</strong> Tidak ada angka di '
    'halaman ini yang saya tulis dari ingatan. Seluruhnya keluar dari satu berkas '
    '<code>replay.py</code> yang menjalankan ulang ketujuh hari ini berurutan, dari '
    '<code>besar.db</code> yang baru dibuat, dan keluarannya disalin apa adanya ke tiap kotak '
    'HARUS MUNCUL. Kalau ada kotak yang tidak cocok dengan hasilmu di luar angka milidetik, '
    'itu kesalahan saya — dan kamu berhak menganggapnya begitu.</p>'),
  kembali_href="https://claude.ai/code/artifact/eff7b693-41fe-43a5-a667-14e294c3e7d9",
  kembali_teks="SQL Mahir L3",
)
out = AKAR/"minggu1/sql-mahir-l4.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
