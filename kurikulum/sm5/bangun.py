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
  judul_tab="SQL Mahir L5",
  kunci_simpan="sql-mahir-l5-v2",
  eyebrow="SQL Mahir · Level 5 dari 5 · ditulis ulang mengikuti pola Bekal Python",
  h1="SQL Mahir L5: ujian, wawancara, dan bukti bahwa kamu bisa",
  lede_paras=[
    "Empat level sebelumnya membangun kemampuanmu. Level ini soal "
    "<strong>menunjukkannya</strong> — di depan pewawancara yang menatap layarmu, atau di depan "
    "klien yang menunggu jawaban dan tidak peduli query-mu seindah apa.",
    "Tujuh hari, 95 langkah, sembilan soal di bawah pengatur waktu, sepuluh pertanyaan lisan yang "
    "kamu jawab <strong>dengan suara keras</strong>, dan satu ujian akhir dua jam. "
    "Tujuh kali kamu akan <strong>sengaja membuat layarmu merah</strong>, dan dua kali melihat "
    "SQL <strong>menerima kesalahanmu tanpa berkedip</strong> — karena yang kedua itulah yang "
    "sebenarnya berbahaya, dan satu-satunya cara mengenalinya adalah pernah membuatnya sendiri.",
    "Semua soal dijawab pada <code>senja.db</code> dan <code>besar.db</code> yang sudah kamu "
    "punya, dan <strong>tiap kunci jawaban di halaman ini dijalankan sungguhan sebelum "
    "ditulis</strong>. Kalau angkamu beda, salah satu dari kita salah ketik — dan kamu punya "
    "datanya untuk membuktikan yang mana.",
  ],
  nav_lbl="SQL L5",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Semua soal memakai '
    '<code>senja.db</code> (dari <code>gen_final.py</code>) dan <code>besar.db</code> (dari '
    '<code>besar.py</code>) — keduanya ada di <code>data-dan-skrip/sql-mahir/</code> di paket zip.</p>\n'
    '    <p style="margin-top:10px"><strong>Dari mana angkanya.</strong> Tiap kotak keluaran di '
    'halaman ini disalin dari menjalankan query-nya sungguhan pada SQLite 3.45.1 — termasuk '
    'keenam pesan error, yang dipicu dulu sebelum ditulis. Tidak ada satu angka pun yang '
    'diketik dari ingatan.</p>'),
  kembali_href="https://claude.ai/code/artifact/2d44eed8-d057-4afc-b429-974231efea42",
  kembali_teks="SQL Mahir L4",
)
out = AKAR/"minggu1/sql-mahir-l5.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
