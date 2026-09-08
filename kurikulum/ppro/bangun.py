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
  judul_tab="Python Produksi",
  kunci_simpan="python-produksi-v2",
  eyebrow="Python Produksi · modul penutup jalur teknis · ditulis ulang mengikuti pola Bekal Python",
  h1="Python Produksi: dari sel notebook jadi alat",
  lede_paras=[
    "Saya mencacah seluruh 44 modul sebelumnya untuk mencari kata-kata ini. Hasilnya: "
    "<strong><code>logging</code> nol, <code>argparse</code> nol, <code>yield</code> nol, "
    "<code>chunksize</code> nol, modul buatan sendiri nol, <code>pytest</code> tiga kali.</strong> "
    "Artinya seluruh kurikulummu mengajarkan Python <em>sebagai skrip notebook</em> — dan tidak "
    "pernah sebagai kode yang dipasang, dijadwalkan, dan dipercaya orang lain.",
    "Tujuh hari, 83 langkah. Di akhir kamu punya satu paket Python sungguhan: berfungsi, ber-uji, "
    "ber-log, dan dijalankan dari baris perintah dengan argumen. "
    "Dan di sepanjang jalan kamu akan <strong>menemukan dan menambal dua bug sungguhan</strong> di "
    "fungsi yang selama ini kamu percaya.",
    "Semua angka di halaman ini hasil menjalankan kodenya di "
    "<strong>Python 3.11.15, pandas 3.0.5, pytest 9.1.1</strong>. "
    "<strong>Angka memorimu bisa jauh berbeda kalau pandas-mu versi 2</strong> — dan kenapa itu "
    "terjadi justru salah satu pelajaran Hari 3.",
  ],
  nav_lbl="Py Produksi",
  hari=[HARI1, HARI2, HARI3, HARI4, HARI5, HARI6, HARI7],
  footer_html=(
    '    <p>Kemajuanmu tersimpan otomatis di browser ini. Paket <code>laporan/</code> dan '
    '<code>tests/</code> yang selesai — hasil akhir ketujuh hari — ada di '
    '<code>data-dan-skrip/python-produksi/</code> di paket zip, untuk kamu cocokkan kalau ada '
    'langkah yang tidak jalan. <strong>Cocokkan sesudah mencoba sendiri, bukan sebelum.</strong></p>\n'
    '    <p style="margin-top:10px"><strong>Dari mana angkanya.</strong> Seluruh keluaran di kotak '
    'HARUS MUNCUL disalin dari menjalankan kodenya sungguhan pada berkas 800.000 baris '
    '(<code>besar.db</code> dari SQL Mahir L4) — bukan dari perkiraan, dan bukan disalin dari '
    'versi modul sebelumnya. Angka waktu dan jam akan berbeda di mesinmu; jumlah baris, ukuran '
    'memori, dan jumlah uji yang lulus tidak boleh berbeda.</p>'),
  kembali_href="https://claude.ai/code/artifact/2d44eed8-d057-4afc-b429-974231efea42",
  kembali_teks="SQL Produksi",
)
out = AKAR/"minggu1/python-produksi.html"
out.write_text(html, encoding="utf-8")
print("ditulis:", out, len(html), "byte")
