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
  judul_tab="Migas L5 — Cadangan & Keputusan",
  kunci_simpan="migas-minggu5-v2",
  eyebrow="Migas L5 · 7 hari · ditulis ulang mengikuti pola Bekal Python",
  h1="Migas L5: cadangan, batas ekonomis, dan satu memo $3 juta",
  lede_paras=[
    "Tujuh hari, satu database (<code>migas.db</code>, sama sejak Migas L1), dan satu "
    "pertanyaan yang tampaknya teknis tapi sebenarnya soal kehati-hatian: berapa "
    "banyak minyak yang tersisa, dan ke mana uang intervensi sebaiknya dibelanjakan.",
    "Analisis pertamamu akan berjalan tanpa satu pun eror dan memberi jawaban yang "
    "50,5 juta barel — dan salah. Bukan karena kodenya rusak; karena kode yang "
    "berjalan mulus tidak pernah memberitahumu apakah hasilnya benar. Lima hari "
    "berikutnya adalah proses menemukan itu sendiri, memperbaikinya sendiri, dan "
    "berakhir pada angka yang 65% lebih kecil — dan jauh lebih bisa "
    "dipertanggungjawabkan.",
    "Setiap angka di halaman ini keluar dari menjalankan kodenya sungguhan (Python "
    "3.11, scipy 1.17) terhadap <code>migas.db</code>. Kalau angkamu beda, itu "
    "petunjuk untuk diperiksa, bukan alasan untuk diabaikan.",
  ],
  nav_lbl="Migas L5",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. <code>migas.db</code> dan '
    'seluruh skrip yang dipakai modul ini ada di <code>data-dan-skrip/bootcamp-jalur-utama/'
    'migas/</code> di paket zip.</p>\n'
    '    <p style="margin-top:10px">Semua angka di halaman ini dihasilkan dengan '
    'menjalankan kode pada <code>migas.db</code> yang kamu punya — kalau hasilmu '
    'berbeda, ada langkah yang perlu diperiksa.</p>'),
  kembali_href="https://claude.ai/code/artifact/35f58664-afca-4799-8bb3-0e39d0025823",
  kembali_teks="Migas L4",
)
out = AKAR/"minggu1/migas-minggu-5.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
