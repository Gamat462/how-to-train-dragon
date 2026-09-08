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
  judul_tab="SQL Mahir Level 1",   # judul tab TIDAK diubah — pembaca mengenali tabnya dari ini
  kunci_simpan="sql-mahir-l1-v3",
  eyebrow="SQL Mahir · Level 1 dari 5 · PostgreSQL di VS Code · kerjakan setelah Modul M6",
  h1="SQL Mahir L1: dasar yang bolong",
  lede_paras=[
    "Modul M1, M2, dan M6 sudah membawamu dari nol sampai bisa menulis query bertingkat dengan "
    "window function. Yang belum pernah disinggung sama sekali justru hal-hal yang membuat "
    "query <strong>diam-diam salah</strong> — bukan gagal dengan tulisan merah, tapi "
    "mengembalikan angka yang terlihat wajar dan keliru.",
    "Tujuh hari ini menutup lubang itu: aturan <code>NULL</code>, jebakan <code>NOT IN</code> "
    "yang paling terkenal di dunia SQL, lima jenis JOIN, self join, <code>DISTINCT ON</code>, "
    "<code>HAVING</code> dan urutan eksekusi, <code>ROLLUP</code>, dan operasi himpunan untuk "
    "merekonsiliasi dua sistem. <strong>Delapan kali kamu akan sengaja membuat layarmu "
    "merah</strong>, dan tujuh kali melihat SQL menerima kesalahanmu tanpa berkedip — karena "
    "yang kedua itulah yang sebenarnya mahal.",
    "Semuanya dikerjakan di <strong>VS Code</strong> yang tersambung ke <strong>PostgreSQL</strong> "
    "— mesin yang dipakai perusahaan tempat kamu melamar, bukan mesin latihan. Basis datanya "
    "kamu muat sendiri di Hari 1. <strong>Setiap angka dan setiap pesan error di halaman ini "
    "dihasilkan dengan menjalankan SQL-nya di PostgreSQL 16 sungguhan</strong>, bukan diketik "
    "dari ingatan.",
  ],
  nav_lbl="SQL L1",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Seluruh latihan memakai basis data '
    '<code>senja</code> yang kamu muat di Hari 1 dari '
    '<code>data-dan-skrip/sql-mahir/senja.sql</code> di paket zip.</p>\n'
    '    <p style="margin-top:10px"><strong>Dari mana angkanya.</strong> Tiap kotak keluaran di '
    'halaman ini dihasilkan otomatis: SQL-nya dijalankan ke PostgreSQL 16 waktu halaman ini '
    'dibangun, lalu hasilnya — termasuk kedelapan pesan error — ditulis apa adanya. Tidak ada '
    'satu angka pun yang diketik tangan.</p>\n'
    '    <p style="margin-top:10px"><strong>Kalau tampilan ekstensimu berbeda.</strong> Kotak '
    'hasil di sini digambar sebagai tabel. Ekstensi SQLTools menampilkannya sebagai grid, dan '
    '<code>NULL</code> bisa muncul sebagai sel kosong atau tulisan pudar. Yang perlu kamu '
    'cocokkan <strong>angkanya dan jumlah barisnya</strong>, bukan warnanya.</p>'),
  kembali_href="https://claude.ai/code/artifact/010bd5cc-8f09-449b-b3de-7bba52005d31",
  kembali_teks="M15: Wawancara & Lamaran",
)
out = AKAR/"minggu1/sql-mahir-l1.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
