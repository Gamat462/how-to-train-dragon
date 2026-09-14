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
  judul_tab="Bekal Pajak & ERP",
  kunci_simpan="bekal-pajak-erp-v1",
  eyebrow="Bekal · 5 hari · disiapkan untuk satu lowongan sungguhan",
  h1="Bekal Pajak & ERP: memenuhi syarat lowongan Tax Data Automation",
  lede_paras=[
    "Lima hari ini dibuat untuk satu lowongan sungguhan: <strong>Analyst | Tax Data "
    "Automation (Python & SQL)</strong> di Deloitte. Bukan latihan umum — tiap hari "
    "menerjemahkan satu bagian bahasa lowongan itu ke SQL dan Python yang kamu jalankan "
    "sungguhan, dengan aturan pajak progresif dan UMKM sebagai bahan latihannya.",
    "Delapan dari sepuluh syarat wajib lowongan ini sudah tertutup modul lain di rute ini. "
    "Modul ini menutup yang tersisa, membangun contoh precedence-dan-exception yang belum "
    "pernah kamu tulis, dan menyiapkan kalimat CV serta jawaban wawancara yang siap "
    "pakai — semuanya dari angka yang kamu hitung dan buktikan sendiri.",
    "<strong>Berlaku untuk lowongan lain juga.</strong> Pola membaca syarat → memetakan ke "
    "bukti → menutup celah yang genuinely ada ini bisa kamu ulangi untuk lowongan data "
    "analyst mana pun yang kamu temukan.",
  ],
  nav_lbl="Pajak & ERP",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Hari 2-3 memakai tabel '
    '<code>pjk_wp</code> dan <code>pjk_lapisan</code> di basis data <code>senja</code> yang '
    'sama seperti SQL Mahir L1-L2 — jalankan <code>data-dan-skrip/bekal-pajak/pjk_data.sql</code> '
    'sekali sebelum mulai.</p>\n'
    '    <p style="margin-top:10px"><strong>Dari mana angkanya.</strong> Tiap kotak keluaran '
    'SQL dihasilkan dengan menjalankan query-nya ke PostgreSQL 16 sungguhan. Keluaran pytest '
    'di Hari 4 dijalankan dan disalin apa adanya, termasuk dua kegagalan yang disengaja.</p>\n'
    '    <p style="margin-top:10px"><strong>Angka pajaknya disederhanakan untuk latihan.</strong> '
    'Struktur lapisan dan aturan UMKM-nya mengikuti bentuk aturan sungguhan, tapi jangan '
    'dipakai mengisi SPT — selalu rujuk PMK/UU HPP yang berlaku untuk pekerjaan nyata.</p>'),
  kembali_href="https://claude.ai/code/artifact/e60e0d95-6d7b-4245-ac7a-f23e60237cfd",
  kembali_teks="indeks rute",
)
out = AKAR/"minggu1/bekal-pajak-erp.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
