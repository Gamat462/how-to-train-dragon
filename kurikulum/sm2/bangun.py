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
  judul_tab="SQL Mahir Level 2",   # judul tab TIDAK diubah
  kunci_simpan="sql-mahir-l2-v2",
  eyebrow="SQL Mahir · Level 2 dari 5 · PostgreSQL di VS Code · lanjutan dari Level 1",
  h1="SQL Mahir L2: window function sampai tuntas",
  lede_paras=[
    "Modul M6 mengenalkanmu pada <code>row_number</code>, <code>lag</code>, dan "
    "<code>PARTITION BY</code> — cukup untuk menjawab pertanyaan yang biasa. Tapi ia tidak "
    "pernah menyebut <strong>frame</strong>, dan frame adalah bagian yang menentukan apakah "
    "running total-mu benar atau meleset satu hari penuh.",
    "Tujuh hari ini: apa yang sebenarnya terjadi di balik <code>OVER</code>, "
    "<code>ROWS</code> lawan <code>RANGE</code> lawan <code>GROUPS</code> (yang bawaannya bukan "
    "yang kamu kira), klausa <code>WINDOW</code> bernama, jebakan <code>last_value</code>, "
    "peringkat dan persentil, median dengan <code>percentile_cont</code>, recursive CTE berikut "
    "klausa <code>CYCLE</code>, dan <code>LATERAL</code> untuk top-N per kelompok.",
    "Semuanya di <strong>VS Code + PostgreSQL</strong>, memakai basis data <code>senja</code> "
    "yang sama seperti Level 1. <strong>Sembilan kali kamu akan sengaja membuat layarmu "
    "merah.</strong> Tiap angka dan tiap pesan error di halaman ini dihasilkan dengan "
    "menjalankan SQL-nya di PostgreSQL 16 sungguhan, bukan diketik dari ingatan. Kalau angkamu "
    "berbeda, salah satu dari kita salah ketik — dan kamu punya datanya untuk membuktikan "
    "yang mana.",
  ],
  nav_lbl="SQL L2",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Seluruh latihan memakai basis data '
    '<code>senja</code> yang kamu muat di Level 1 Hari 1.</p>\n'
    '    <p style="margin-top:10px"><strong>Dari mana angkanya.</strong> Tiap kotak keluaran di '
    'halaman ini dihasilkan otomatis: SQL-nya dijalankan ke PostgreSQL 16 waktu halaman ini '
    'dibangun, lalu hasilnya — termasuk kesembilan pesan error — ditulis apa adanya.</p>\n'
    '    <p style="margin-top:10px"><strong>Kalau tampilan ekstensimu berbeda.</strong> Kotak '
    'hasil di sini digambar sebagai tabel; SQLTools menampilkannya sebagai grid. Yang perlu '
    'kamu cocokkan <strong>angkanya dan jumlah barisnya</strong>.</p>'),
  kembali_href="https://claude.ai/code/artifact/caff475b-354e-4331-84f9-d7fd36fe51b4",
  kembali_teks="SQL Mahir L1",
)
out = AKAR/"minggu1/sql-mahir-l2.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
