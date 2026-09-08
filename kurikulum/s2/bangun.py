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
  judul_tab="Jalur S2 Luar Negeri",
  kunci_simpan="jalur-s2-luar-negeri-v2",
  eyebrow="Jalur S2 · 7 hari · ditulis ulang mengikuti pola Bekal Python",
  h1="S2 Data Science di luar negeri: hitung sendiri, jangan tanya saya",
  lede_paras=[
    "Tujuh hari untuk menjawab satu pertanyaan mahal: apakah kamu perlu S2 di luar negeri. "
    "Versi sebelumnya menyodorkan sepuluh tabel angka untuk dibaca. Versi ini memberimu "
    "<strong>empat skrip</strong> yang menghitung angka-angka itu dengan asumsimu sendiri — "
    "biaya, tenggat, lubang kurikulum, dan skor keputusanmu.",
    "Bedanya bukan gaya. Tabel yang diketik akan basi diam-diam: modul lama menulis "
    "“tinggal 29 hari” dan “empat topik bernilai nol”, dan dua-duanya sudah tidak benar lagi "
    "hari ini. Skrip menghitungnya ulang tiap kali dijalankan, dan itulah satu-satunya cara "
    "modul seperti ini tetap jujur.",
    "Setiap angka yang tertulis di halaman ini keluar dari menjalankan skripnya sungguhan "
    "(Python 3.11.15). Kalau angkamu berbeda, itu bukan kesalahan — itu asumsimu, dan asumsimu "
    "yang berlaku.",
  ],
  nav_lbl="Jalur S2",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Empat skrip yang dipakai modul ini — '
    '<code>hitung_s2.py</code>, <code>hitung_tenggat.py</code>, <code>pindai_topik.py</code>, dan '
    '<code>skor_rubrik.py</code> — ada di <code>data-dan-skrip/jalur-s2/</code> di paket zip.</p>\n'
    '    <p style="margin-top:10px"><strong>Sumber angka di halaman ini.</strong> Kurikulum &amp; '
    'mata kuliah: halaman resmi NUS Department of Mathematics, University of Melbourne Handbook, '
    'UC Berkeley School of Information, CMU Heinz College, Georgia Tech Professional Education, '
    'UCL, dan Imperial College. Biaya &amp; syarat masuk: halaman program masing-masing kampus. '
    'Beasiswa: LPDP, Chevening, dan Australia Awards Indonesia. Upah: BPS (rilis November 2025); '
    'median gaji data analyst: NodeFlair; lama pencarian kerja 19,8 bulan: LPEM FEB UI atas '
    'Sakernas BPS Agustus 2025. Syarat visa: aturan visa pelajar UK, Australia, dan rekening '
    'terblokir Jerman 2026. Kurs: BCA, BRI, Yahoo Finance per 6 September 2026. Kutipan lowongan: '
    'Indeed Indonesia, September 2026.</p>\n'
    '    <p style="margin-top:10px"><strong>Peringatan yang harus kamu baca.</strong> Riset ini '
    'dikerjakan 7 September 2026 melalui hasil pencarian, karena akses langsung ke situs kampus '
    'diblokir dari lingkungan tempat modul ini disusun. Beberapa sumber saling bertentangan dan '
    'saya selalu memakai angka terendah. Uang kuliah, tenggat, dan aturan visa berubah setiap '
    'tahun. <em>Verifikasi setiap angka ke situs resmi sebelum memakainya untuk mengambil '
    'keputusan.</em> Skrip-skrip di atas dibuat justru supaya kamu bisa mengganti angkanya '
    'sendiri, bukan mempercayai angka saya.</p>'),
  kembali_href="https://claude.ai/code/artifact/61355282-6fe8-4f54-bd99-18ff4ae63d28",
  kembali_teks="Proyek Buta",
)
out = AKAR/"minggu1/jalur-s2-luar-negeri.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
