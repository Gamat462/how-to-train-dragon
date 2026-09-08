# -*- coding: utf-8 -*-
"""Hari 3 — mengubah bug jadi penjaga permanen."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Hitung dulu berapa mahalnya bug kemarin",
    blok("aksi", "Bayangkan tiga baris ini dari buku besar klien. Hitung di kalkulator, "
                 "dua kali.", "LAKUKAN"),
    kode("""Penjualan     91.190.000
Retur        (3.200.000)
Diskon          (96.000)""", salin=False),
    blok("hasil", "<pre><code>total kalau kurung diabaikan : 94.486.000\n"
                  "total yang benar             : 87.894.000\n"
                  "selisih                      :  6.592.000</code></pre>", "HARUS MUNCUL"),
    "<p>Rp 6,6 juta, dari tiga baris. Kalikan dengan buku besar yang berisi ribuan baris.</p>",
    blok("bahaya", "<strong>Dan tidak ada error apa pun.</strong> Angkanya cuma salah. "
                   "Ini persis jenis salah saji yang dulu kamu cari dengan mata."))

langkah("Tulis ujinya sebelum memperbaiki apa pun",
    blok("aksi", "Tambahkan ke <code>tests/test_bersih.py</code>. "
                 "<strong>Jangan sentuh <code>bersih.py</code>.</strong>", "LAKUKAN"),
    kode('''@pytest.mark.parametrize("masuk,harap", [
    ("(1.000)", -1000),
    ("(91.190.000)", -91190000),
    ("-96.000", -96000),
    ("96.000", 96000),
])
def test_ke_angka_kurung_akuntansi(masuk, harap):
    """Excel akuntansi menulis angka negatif sebagai (1.000), bukan -1000."""
    assert ke_angka(masuk) == harap, f"{masuk!r} terbaca {ke_angka(masuk)}, harusnya {harap}"'''),
    blok("hasil", "<p>Belum dijalankan. Dua kasus pertama <em>seharusnya</em> gagal — itu yang "
                  "kita mau.</p>", "HARUS MUNCUL"),
    "<p>Perhatikan dua kasus terakhir: <code>-96.000</code> dan <code>96.000</code>. Itu bukan "
    "pelengkap — <strong>itu penjaga</strong>, supaya tambalanmu nanti tidak merusak yang sudah "
    "benar.</p>")

langkah("Jalankan, dan lihat merahnya",
    blok("aksi", "Sekarang jalankan.", "LAKUKAN"),
    kode("python -m pytest -q"),
    blok("hasil", "<pre><code>..........FF..                        [100%]\n"
                  "...\n"
                  "E   AssertionError: '(1.000)' terbaca 1000, harusnya -1000\n"
                  "E   assert 1000 == -1000\n"
                  "E    +  where 1000 = ke_angka('(1.000)')\n"
                  "...\n"
                  "2 failed, 12 passed in 0.34s</code></pre>", "HARUS MUNCUL"),
    "<p>Dua <code>F</code> di antara titik-titik. Dan pytest menunjukkan "
    "<strong>nilai sebenarnya</strong> — <code>terbaca 1000, harusnya -1000</code> — bukan cuma "
    "“gagal”.</p>")

langkah("Kenapa pesannya sejelas itu",
    blok("aksi", "Lihat lagi baris <code>assert</code> yang kamu tulis.", "LAKUKAN"),
    kode('''assert ke_angka(masuk) == harap, f"{masuk!r} terbaca {ke_angka(masuk)}, harusnya {harap}"
#                                 ^-- koma, lalu pesan''', salin=False),
    blok("hasil", "<p>Tanpa pesan itu, yang muncul cuma <code>assert 1000 == -1000</code> — "
                  "benar, tapi tidak memberitahumu <em>masukan mana</em>.</p>", "BEDANYA"),
    blok("catatan", "<strong>Selalu beri pesan pada assert.</strong> Bedanya antara memperbaiki "
                    "dalam sepuluh detik dan dalam sepuluh menit — dan bedanya baru terasa "
                    "enam bulan lagi, saat kamu sudah lupa kodenya."))

langkah("Sekarang perbaiki — di satu tempat",
    blok("aksi", "Ganti dua baris terakhir <code>ke_angka</code> di "
                 "<code>laporan/bersih.py</code>.", "LAKUKAN"),
    kode('''    asli = str(nilai).strip()
    # Excel akuntansi menulis angka negatif sebagai "(1.000)", bukan "-1.000".
    negatif = asli.startswith("(") and asli.endswith(")")
    teks = re.sub(r"[^0-9\\-]", "", asli)
    if teks in ("", "-"):
        return None
    return -int(teks) if negatif else int(teks)'''),
    kode("python -m pytest -q"),
    blok("hasil", "<pre><code>..............                        [100%]\n14 passed in 0.32s</code></pre>",
         "HARUS MUNCUL"),
    "<p>Hijau. Dan yang penting: <strong>sepuluh uji lama ikut dijalankan</strong> dan tetap "
    "lulus — jadi kamu tahu tambalanmu tidak merusak apa pun.</p>")

langkah("Lihat arti “satu tempat” itu",
    blok("aksi", "Kamu tidak menyentuh kode apa pun selain <code>ke_angka</code>. "
                 "Jalankan ini.", "LAKUKAN"),
    kode('''import pandas as pd
from laporan.bersih import ke_angka

df = pd.DataFrame({"ket": ["Penjualan", "Retur", "Diskon"],
                   "nilai": ["91.190.000", "(3.200.000)", "(96.000)"]})
df["angka"] = df["nilai"].map(ke_angka)
print(df.to_string(index=False))
print("total:", df["angka"].sum())'''),
    blok("hasil", "<pre><code>      ket       nilai    angka\n"
                  "Penjualan  91.190.000 91190000\n"
                  "    Retur (3.200.000) -3200000\n"
                  "   Diskon    (96.000)   -96000\n"
                  "total: 87894000</code></pre>", "HARUS MUNCUL"),
    "<p><strong>87.894.000</strong> — angka yang benar dari langkah 1. Kode ini tidak pernah "
    "diubah; ia cuma memanggil fungsi yang sekarang benar. Itulah seluruh alasan Hari 1 ada.</p>")

langkah("Namanya: regression test",
    blok("aksi", "Baca satu paragraf, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p>Uji yang ditulis <strong>setelah</strong> menemukan bug punya nama: "
                  "<em>regression test</em>. Nilainya bukan menemukan bug baru — tapi "
                  "<strong>memastikan bug lama tidak pernah kembali diam-diam</strong>.</p>",
         "ISTILAHNYA"),
    "<p>Siapa pun yang nanti “merapikan” <code>ke_angka</code> dan tidak sengaja membuang "
    "penanganan kurung itu akan langsung tahu, dalam 0,3 detik.</p>")

langkah("Sekarang cari bug kedua sendiri",
    blok("aksi", "Klien menulis nama badan usaha dengan titik sesering tanpa titik. Coba.", "LAKUKAN"),
    kode('''from laporan.bersih import rapikan_nama
print(list(rapikan_nama(pd.Series(["PT. MAJU JAYA", "cv. karya abadi", "PT mitra bangun"]))))'''),
    blok("hasil", "<pre><code>['Pt. Maju Jaya', 'Cv. Karya Abadi', 'PT Mitra Bangun']</code></pre>",
         "HARUS MUNCUL"),
    "<p>Yang ketiga benar, dua yang pertama <strong>tidak</strong> — <code>Pt.</code> dan "
    "<code>Cv.</code>. Sebelum membaca lebih jauh: tebak sendiri kenapa.</p>",
    "<details><summary>Buka jawabannya</summary>"
    "<p>Pola pengganti di <code>rapikan_nama</code> adalah "
    "<code>r\"^(Cv|Pt|Ud)\\s+\"</code> — ia menuntut <strong>spasi</strong> tepat setelah badan "
    "usahanya. <code>PT.</code> punya titik di situ, jadi polanya tidak cocok dan huruf besarnya "
    "tidak dikembalikan.</p></details>")

langkah("Ulangi urutannya: uji dulu, tambal kemudian",
    blok("aksi", "Kamu sudah tahu polanya. Kerjakan sendiri — uji dulu.", "LAKUKAN"),
    kode('''def test_rapikan_nama_badan_usaha_bertitik():
    """Klien menulis "PT. MAJU JAYA" sesering "PT MAJU JAYA"."""
    s = pd.Series(["PT. MAJU JAYA", "cv. karya abadi"])
    assert list(rapikan_nama(s)) == ["PT. Maju Jaya", "CV. Karya Abadi"], \\
        f"hasilnya {list(rapikan_nama(s))}"'''),
    blok("hasil", "<pre><code>E   AssertionError: hasilnya ['Pt. Maju Jaya', 'Cv. Karya Abadi']\n"
                  "1 failed, 14 passed in 0.32s</code></pre>", "HARUS MUNCUL"),
    "<p>Merah dulu. Kalau ujimu langsung hijau, ia tidak menguji apa pun.</p>")

langkah("Tambal, lalu hijaukan",
    blok("aksi", "Ganti pola pengganti di <code>rapikan_nama</code>: izinkan titik yang "
                 "sifatnya pilihan, dan kembalikan titiknya apa adanya.", "LAKUKAN"),
    kode('''             .str.replace(r"^(Cv|Pt|Ud)(\\.?)\\s+",
                          lambda m: m.group(1).upper() + m.group(2) + " ", regex=True))'''),
    kode("python -m pytest -q"),
    blok("hasil", "<pre><code>...............                       [100%]\n15 passed in 0.33s</code></pre>",
         "HARUS MUNCUL"),
    "<p><code>(\\.?)</code> artinya “titik, boleh ada boleh tidak”, dan "
    "<code>m.group(2)</code> memasangnya kembali. <code>PT mitra bangun</code> yang tanpa titik "
    "tetap benar — uji lama membuktikannya.</p>")

langkah("Bug ketiga: yang sudah diperbaiki orang lain",
    blok("aksi", "Ini bug paling terkenal di kurikulum ini — pelanggan bernama "
                 "<strong>“Nan”</strong> dari Studi Kasus 1. Uji apakah ia masih ada.", "LAKUKAN"),
    kode('''import numpy as np
s = pd.Series(["Budi Santoso", np.nan, "Toko Berkah"])
print(list(s.astype(str)))
print(list(s.astype(str).str.strip().str.title()))'''),
    blok("hasil", "<pre><code>['Budi Santoso', nan, 'Toko Berkah']\n"
                  "['Budi Santoso', nan, 'Toko Berkah']</code></pre>", "HARUS MUNCUL"),
    "<p>Sel kosongnya <strong>tetap kosong</strong>. Di pandas 2, "
    "<code>.astype(str)</code> mengubahnya jadi teks <code>'nan'</code>, lalu "
    "<code>.str.title()</code> menjadikannya pelanggan bernama <code>'Nan'</code> yang muncul "
    "rapi di laporan seolah-olah manusia. <strong>Di pandas 3 itu sudah diperbaiki.</strong></p>",
    blok("bahaya", "<strong>Kode yang sama, hasil yang berbeda, tanpa satu pun error.</strong> "
                   "Skripmu bisa memberi angka berbeda di komputer klien hanya karena versi "
                   "pustakanya berbeda. Itu sebabnya Hari 7 diakhiri dengan "
                   "<code>requirements.txt</code> — dan sekarang kamu punya alasan yang kamu "
                   "lihat sendiri, bukan yang saya klaim."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Urutan yang benar: menambal dulu atau menulis uji dulu?
2. Kenapa uji harus MERAH dulu sebelum ditambal?
3. Apa nama uji yang ditulis setelah menemukan bug?
4. Kenapa dua kasus yang sudah benar ikut dimasukkan ke uji kurung akuntansi?
5. Apa yang membuat kode sama memberi hasil berbeda di komputer lain?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <strong>Uji dulu.</strong> "
    "2. Uji yang tidak pernah merah belum membuktikan bahwa ia benar-benar memeriksa sesuatu. "
    "3. <em>Regression test</em>. "
    "4. Sebagai penjaga — supaya tambalannya tidak merusak yang sudah benar. "
    "5. Versi pustaka yang berbeda.</p></details>")

HARI3 = {
  "n": "HARI 3",
  "tab": "3",
  "judul": "Uji yang menangkap bug yang sungguh pernah kamu buat",
  "waktu": "± 70 menit",
  "tujuan": "membaca laporan kegagalan pytest, dan mengubah dua bug sungguhan jadi penjaga "
            "permanen — dengan urutan yang benar: <strong>uji dulu, tambal kemudian</strong>.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> 15 uji, dua bug yang kamu temukan dan tambal "
           "sendiri, dan satu urutan kerja yang berlaku seumur karier: "
           "<em>uji dulu → lihat merah → tambal → lihat hijau</em>.</p>"
           "<p style=\"margin-top:8px\">Dan satu hal yang tidak ada di modul mana pun sebelumnya: "
           "bukti bahwa <strong>kode yang sama bisa memberi angka berbeda</strong> hanya karena "
           "versi pandas-nya berbeda.</p>"
           "<p style=\"margin-top:8px\">Tiga hari berikutnya berhenti soal benar-salah. "
           "Isinya soal <strong>besar</strong>: memori, kecepatan, dan berkas yang tidak muat.</p>",
}
