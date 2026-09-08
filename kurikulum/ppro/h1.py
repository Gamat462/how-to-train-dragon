# -*- coding: utf-8 -*-
"""Hari 1 — berhenti menyalin-tempel fungsi antar-notebook."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bikin kerangka foldernya",
    blok("aksi", "Buat folder dan berkas kosong dengan susunan persis ini. "
                 "Nama <code>proyek</code> boleh kamu ganti, sisanya jangan.", "LAKUKAN"),
    kode("""proyek/
├── laporan/
│   ├── __init__.py      <- menandai folder ini paket Python
│   ├── bersih.py        <- fungsi pembersihan   (hari ini)
│   ├── hitung.py        <- fungsi agregasi      (Hari 7)
│   └── cli.py           <- titik masuk terminal (Hari 7)
└── tests/
    └── test_bersih.py   <- pengujian            (Hari 2)""", salin=False),
    blok("hasil", "<p>Enam berkas kosong. Belum ada isinya — itu memang benar.</p>",
         "HARUS ADA DI DISKMU"),
    blok("bahaya", "<strong>Semua perintah di modul ini dijalankan dari <code>proyek/</code></strong>, "
                   "bukan dari dalam <code>laporan/</code>. Salah folder = pesan error di langkah 9."))

langkah("Isi __init__.py, dan buktikan Python melihatnya",
    blok("aksi", "Berkas ini boleh kosong — tapi isi saja dua baris supaya ada gunanya.", "LAKUKAN"),
    kode('''"""Alat laporan penjualan — dipakai ulang, bukan disalin-tempel."""
__version__ = "0.1.0"'''),
    blok("aksi", "Lalu dari <code>proyek/</code>, jalankan:", "LAKUKAN"),
    kode('python -c "import laporan; print(laporan.__version__)"'),
    blok("hasil", "<pre><code>0.1.0</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Keberadaan <code>__init__.py</code> itulah</strong> yang memberi tahu Python "
    "“folder ini paket, isinya boleh di-<code>import</code>”. Tanpa berkas itu, langkah 7 gagal.</p>")

langkah("Fungsi pertama: pindahkan ke_angka ke berkasnya sendiri",
    blok("aksi", "Simpan ini sebagai <code>laporan/bersih.py</code>. Fungsinya sama dengan yang "
                 "kamu tulis di Studi Kasus — yang baru adalah <strong>bentuknya</strong>.", "LAKUKAN"),
    kode('''"""Fungsi pembersihan yang bisa diuji satu per satu."""
import re
import pandas as pd


def ke_angka(nilai: object) -> int | None:
    if nilai is None or (isinstance(nilai, float) and pd.isna(nilai)):
        return None
    if isinstance(nilai, (int,)):
        return int(nilai)
    teks = re.sub(r"[^0-9\\-]", "", str(nilai))
    return int(teks) if teks not in ("", "-") else None'''),
    blok("hasil", "<p>Tidak ada yang tercetak — ini berkas definisi, belum dijalankan.</p>",
         "HARUS MUNCUL"),
    "<p>Perhatikan barisnya: <code>(nilai: object) -&gt; int | None</code>. Itu "
    "<strong>tanda tipe</strong>, dan artinya dibahas di langkah 8.</p>")

langkah("Tambahkan docstring — dan contoh yang bisa dijalankan",
    blok("aksi", "Sisipkan tepat di bawah baris <code>def ke_angka(...)</code>.", "LAKUKAN"),
    kode('''    """Ubah teks berformat Indonesia jadi bilangan bulat.

    >>> ke_angka("3.200.000")
    3200000
    >>> ke_angka("Rp 91.190.000")
    91190000
    >>> ke_angka(None) is None
    True
    """'''),
    blok("aksi", "Lalu dari <code>proyek/</code>:", "LAKUKAN"),
    kode('python -c "from laporan.bersih import ke_angka; help(ke_angka)"'),
    blok("hasil", "<pre><code>ke_angka(nilai: object) -&gt; int | None\n"
                  "    Ubah teks berformat Indonesia jadi bilangan bulat.\n\n"
                  "    &gt;&gt;&gt; ke_angka(\"3.200.000\")\n    3200000\n"
                  "    &gt;&gt;&gt; ke_angka(\"Rp 91.190.000\")\n    91190000\n"
                  "    &gt;&gt;&gt; ke_angka(None) is None\n    True</code></pre>", "HARUS MUNCUL"),
    "<p>Docstring itu ditulis <strong>untuk dirimu enam bulan lagi</strong>. Dan tiga baris "
    "<code>&gt;&gt;&gt;</code> itu bukan hiasan — besok mereka jadi soal ujinya.</p>")

langkah("Fungsi kedua: rapikan_nama",
    blok("aksi", "Tambahkan di bawahnya, di berkas yang sama.", "LAKUKAN"),
    kode('''def rapikan_nama(s: pd.Series) -> pd.Series:
    """Samakan penulisan nama: spasi ganda, huruf besar-kecil, badan usaha."""
    return (s.str.strip()
             .str.replace(r"\\s+", " ", regex=True)
             .str.title()
             .str.replace(r"^(Cv|Pt|Ud)\\s+",
                          lambda m: m.group(1).upper() + " ", regex=True))'''),
    blok("hasil", "<p>Masih belum ada yang tercetak.</p>", "HARUS MUNCUL"),
    "<p>Baris terakhir mengembalikan <code>CV</code>/<code>PT</code>/<code>UD</code> jadi huruf "
    "besar, karena <code>.str.title()</code> sudah terlanjur mengubahnya jadi <code>Cv</code>.</p>")

langkah("Fungsi ketiga: buang_baris_bukan_data",
    blok("aksi", "Satu lagi, lalu berkasnya selesai.", "LAKUKAN"),
    kode('''def buang_baris_bukan_data(df: pd.DataFrame, kolom_no: str = "No") -> pd.DataFrame:
    """Sisakan hanya baris yang kolom nomornya benar-benar angka."""
    return df[df[kolom_no].fillna("").astype(str).str.fullmatch(r"\\d+")].copy()'''),
    blok("hasil", "<p>Belum ada keluaran. Langkah berikutnya baru menjalankannya.</p>",
         "HARUS MUNCUL"),
    "<p>Ini yang membuang baris <code>\"Dicetak oleh: Admin\"</code> dan baris kosong yang selalu "
    "menempel di ekspor Excel klien.</p>")

langkah("Sekarang pakai dari mana saja",
    blok("aksi", "Dari <code>proyek/</code>, buka Python atau notebook.", "LAKUKAN"),
    kode('''from laporan.bersih import ke_angka, rapikan_nama
import pandas as pd

print(ke_angka("Rp 91.190.000"))
print(ke_angka("3.200.000"))
print(ke_angka(None))
print(list(rapikan_nama(pd.Series([" budi santoso ", "BUDI SANTOSO", "cv karya abadi"]))))'''),
    blok("hasil", "<pre><code>91190000\n3200000\nNone\n"
                  "['Budi Santoso', 'Budi Santoso', 'CV Karya Abadi']</code></pre>", "HARUS MUNCUL"),
    "<p>Sekarang ada <strong>satu</strong> <code>ke_angka</code> di seluruh pekerjaanmu. "
    "Perbaiki di sini, dan semua yang memakainya ikut terperbaiki — termasuk skrip klien yang "
    "sudah berjalan tiga bulan.</p>")

langkah("Tiga hal yang layak kamu tiru di tiap fungsi mulai sekarang",
    blok("aksi", "Baca tabel ini sambil melihat berkas yang barusan kamu tulis.", "LAKUKAN"),
    tabel(["Yang ditambahkan", "Contohnya", "Gunanya"],
          [["Tanda tipe", "<code>(nilai: object) -&gt; int | None</code>",
            "Editormu memperingatkanmu <em>sebelum</em> dijalankan. Dan pembaca tahu fungsi ini "
            "bisa mengembalikan <code>None</code> — jadi hasilnya harus diperiksa."],
           ["Docstring", "<code>\"\"\"Ubah teks berformat Indonesia…\"\"\"</code>",
            "Muncul saat kamu mengetik <code>help(ke_angka)</code>."],
           ["Contoh di docstring", "<code>&gt;&gt;&gt; ke_angka(\"3.200.000\")</code>",
            "Contoh yang <strong>bisa dijalankan</strong> — dan yang jadi soal ujinya besok."]]),
    blok("catatan", "<strong>Tanda tipe tidak memaksa apa pun saat program berjalan.</strong> "
                    "Python tetap menerima <code>ke_angka([1,2,3])</code>. Gunanya untuk manusia "
                    "dan alat pemeriksa — dan itu sudah cukup, karena sebagian besar bug yang "
                    "menyita waktumu adalah salah tipe."))

langkah("Kalau muncul ModuleNotFoundError",
    blok("aksi", "Buat error-nya dengan sengaja: masuk ke dalam folder <code>laporan/</code>, "
                 "lalu ulangi import-nya.", "LAKUKAN"),
    kode('''cd laporan
python -c "from laporan.bersih import ke_angka"'''),
    blok("hasil", "<pre><code>ModuleNotFoundError: No module named 'laporan'</code></pre>",
         "HARUS MUNCUL"),
    "<p>Python mencari paket mulai dari <strong>folder tempat kamu menjalankannya</strong>. "
    "Harus dari <code>proyek/</code>, bukan dari dalam <code>laporan/</code>. "
    "Kembali dulu: <code>cd ..</code></p>",
    blok("catatan", "Di Colab: <code>import os; os.chdir('/content/proyek')</code> lebih dulu."))

langkah("Temukan satu bug di fungsimu sendiri",
    blok("aksi", "Excel akuntansi menulis angka <strong>negatif</strong> sebagai "
                 "<code>(1.000)</code>, bukan <code>-1000</code>. Coba.", "LAKUKAN"),
    kode('''print(ke_angka("(1.000)"))
print(ke_angka("(91.190.000)"))
print(ke_angka("-96.000"))'''),
    blok("hasil", "<pre><code>1000\n91190000\n-96000</code></pre>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Dua angka pertama harusnya negatif.</strong> Fungsimu membuang tanda "
                   "kurungnya lalu mengembalikan bilangan positif — <em>tanpa error</em>. "
                   "Retur penjualan senilai 91 juta terbaca sebagai penjualan 91 juta, dan "
                   "selisih 182 juta itu tidak akan pernah muncul sebagai pesan apa pun."),
    "<p>Jangan diperbaiki sekarang. <strong>Hari 3 kamu akan memperbaikinya di satu tempat</strong> "
    "— dan melihat sendiri apa artinya “satu tempat” itu.</p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas, tanpa melihat.", "LAKUKAN"),
    kode("""1. Berkas apa yang membuat sebuah folder jadi paket Python?
2. Dari folder mana perintah python harus dijalankan?
3. Apa yang dilakukan tanda tipe saat program berjalan?
4. Kenapa menaruh fungsi di satu berkas lebih baik daripada menyalinnya?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>__init__.py</code>, boleh kosong. "
    "2. <code>proyek/</code> — folder di atas paketnya. "
    "3. <strong>Tidak apa-apa.</strong> Ia untuk manusia dan alat pemeriksa saja. "
    "4. Karena bug diperbaiki sekali dan semua pemakainya ikut terperbaiki — "
    "seperti bug kurung akuntansi yang baru kamu temukan.</p></details>")

HARI1 = {
  "n": "HARI 1",
  "tab": "1",
  "judul": "Berhenti menyalin-tempel fungsi antar-notebook",
  "waktu": "± 55 menit",
  "tujuan": "menaruh fungsi di berkas sendiri dan memanggilnya dari mana saja — supaya perbaikan "
            "satu tempat berlaku di semua tempat.",
  "langkah": L,
  "tutup_judul": "Hari 1 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu paket Python yang bisa di-<code>import</code>, "
           "tiga fungsi bertanda tipe dan ber-docstring, dan <strong>satu bug yang kamu temukan "
           "sendiri</strong> di fungsi yang selama ini kamu percaya.</p>"
           "<p style=\"margin-top:8px\">Bug itu sengaja dibiarkan. Ia jadi bahan Hari 2 dan Hari 3.</p>"
           "<p style=\"margin-top:8px\">Besok: cara berhenti memeriksa hasil dengan mata.</p>",
}
