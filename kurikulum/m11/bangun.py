# -*- coding: utf-8 -*-
import sys, pathlib
AKAR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR/"mat")); sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _gen import bangun
from h71 import HARI71
from h72 import HARI72
from h73 import HARI73
from h74 import HARI74
from h75 import HARI75
from h76 import HARI76
from h77 import HARI77

html = bangun(
  judul_tab="Minggu Kesebelas Git &amp; Streamlit",
  kunci_simpan="minggu-kesebelas-v2",
  eyebrow="Minggu 11 · Hari 71-77 · ditulis ulang mengikuti pola Bekal Python",
  h1="Git, Otomasi &amp; Streamlit: berhenti mengirim berkas, mulai mengirim tautan",
  lede_paras=[
    "Minggu ini kamu berhenti menjadi orang yang mengirim <em>laporan-final-v3-REVISI.xlsx</em> "
    "lewat WhatsApp, dan mulai menjadi orang yang mengirim satu tautan yang isinya memperbarui "
    "dirinya sendiri tiap Senin pagi.",
    "Versi sebelumnya menjelaskan alur git dalam satu blok kode 24 baris berisi tujuh perintah "
    "sekaligus. Versi ini memecahnya jadi <strong>langkah-langkah satu gagasan</strong> — satu "
    "sampai empat baris kode, lalu kotak <strong>HARUS MUNCUL</strong> berisi keluaran persis "
    "yang harus kamu lihat sebelum lanjut.",
    "Setiap keluaran git dan Python di halaman ini diperoleh dengan menjalankan perintahnya "
    "sungguhan; setiap angka di bagian Streamlit dibaca dari aplikasi yang benar-benar berjalan "
    "di browser. Kalau angkamu berbeda dariku, salah satu dari kita salah ketik — dan kamu punya "
    "datanya untuk membuktikan yang mana.",
  ],
  nav_lbl="Minggu 11",
  hari=[HARI71, HARI72, HARI73, HARI74, HARI75, HARI76, HARI77],
  footer_html='    <p>Kemajuanmu tersimpan otomatis di browser ini. Keluaran yang tertulis di kotak '
              '“HARUS MUNCUL” dihasilkan dengan menjalankan perintahnya di git 2.43.0, '
              'Python 3.11.15, pandas 3.0.5, dan Streamlit 1.63.0. Kotak “YANG HARUS TERLIHAT” '
              'menggambarkan apa yang muncul di layar GitHub atau di browser, bukan keluaran '
              'terminal.</p>',
  kembali_href="https://claude.ai/code/artifact/26a3ee5f-9d8a-4679-9977-37c06da48459",
  kembali_teks="M10: dbt",
)
out = AKAR/"minggu1/minggu-kesebelas.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
