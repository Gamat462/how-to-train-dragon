# -*- coding: utf-8 -*-
import sys, pathlib
AKAR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR/"mat")); sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _gen import bangun
from h92 import HARI92
from h93 import HARI93
from h94 import HARI94
from h95 import HARI95
from h96 import HARI96
from h97 import HARI97
from h98 import HARI98

html = bangun(
  judul_tab="Minggu Keempat Belas Portofolio &amp; CV",
  kunci_simpan="minggu-keempatbelas-v2",
  eyebrow="Minggu 14 · Hari 92-98 · ditulis ulang mengikuti pola Bekal Python",
  h1="Portofolio, CV, dan wawancara SQL — diukur, bukan dikira",
  lede_paras=[
    "Minggu ini isinya hal-hal yang biasanya cuma bisa dinilai dengan perasaan: apakah README-ku "
    "sudah bagus, apakah CV-ku sudah cukup, apakah aku sudah siap ditanya SQL. "
    "Versi ini mengganti perasaan itu dengan <strong>tiga skrip pemeriksa dan satu basis data "
    "latihan</strong> yang bisa kamu jalankan sendiri.",
    "Versi sebelumnya menjelaskan empat soal SQL wawancara lewat jawaban jadi sepanjang 15 baris "
    "yang tinggal dibaca. Versi ini membangun tiap jawaban selapis demi selapis pada basis data "
    "sungguhan — dan membuktikan dua bug diam yang menjatuhkan kandidat: "
    "<code>NOT IN</code> yang mengembalikan nol karena satu NULL, dan retensi yang terbaca "
    "<strong>100% di setiap kohor</strong> hanya karena satu kata diganti.",
    "Semua keluaran di kotak “HARUS MUNCUL” diperoleh dengan menjalankan perintahnya sungguhan: "
    "DuckDB 1.5.5, Python 3.11.15, git 2.43.0. Kalau angkamu berbeda, salah satu dari kita salah "
    "ketik — dan kamu punya datanya untuk membuktikan yang mana.",
  ],
  nav_lbl="Minggu 14",
  hari=[HARI92, HARI93, HARI94, HARI95, HARI96, HARI97, HARI98],
  footer_html='    <p>Kemajuanmu tersimpan otomatis di browser ini. Skrip dan berkas latihan '
              '(<code>periksa_readme.py</code>, <code>periksa_cv.py</code>, '
              '<code>buat_soal_sql.py</code>, <code>jalankan.py</code>, beserta CV contoh) '
              'ada di <code>data-dan-skrip/minggu-14/</code> di paket zip. Kotak “YANG HARUS '
              'TERLIHAT” menggambarkan tampilan di layar GitHub atau LinkedIn, bukan keluaran '
              'terminal.</p>',
  kembali_href="https://claude.ai/code/artifact/1c78fa92-69e9-4546-a3b1-075eabd3e5c8",
  kembali_teks="M13: Machine Learning",
)
out = AKAR/"minggu1/minggu-keempatbelas.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
