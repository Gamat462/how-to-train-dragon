# -*- coding: utf-8 -*-
"""Hari 2 — pengujian: cara berhenti memeriksa ulang dengan mata."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Pasang pytest",
    blok("aksi", "Dari <code>proyek/</code>.", "LAKUKAN"),
    kode("pip install pytest"),
    blok("hasil", "<pre><code>Successfully installed ... pytest-9.1.1</code></pre>",
         "HARUS MUNCUL (nomor versinya boleh beda)"),
    blok("catatan", "<strong>Yang normal tapi bikin panik.</strong> Kalau muncul tulisan kuning "
                    "panjang berisi <em>WARNING: Running pip as the root user</em>, atau "
                    "<em>Requirement already satisfied</em>, dua-duanya wajar — yang pertama "
                    "cuma saran, yang kedua berarti pytest sudah terpasang. Kamu boleh lanjut."),
    "<p>Sejauh ini caramu memastikan kode benar adalah <strong>melihat hasilnya</strong> — "
    "cocokkan dengan kotak HARUS MUNCUL. Itu bekerja saat kamu sedang menatap layar. Yang tidak "
    "bekerja: memastikan perubahan hari ini tidak merusak sesuatu yang kamu tulis bulan lalu.</p>")

langkah("Tulis satu uji, sesederhana mungkin",
    blok("aksi", "Simpan sebagai <code>tests/test_bersih.py</code>.", "LAKUKAN"),
    kode('''import pandas as pd
import pytest
from laporan.bersih import ke_angka, rapikan_nama, buang_baris_bukan_data


def test_ke_angka_teks_biasa():
    assert ke_angka("3.200.000") == 3200000'''),
    blok("aksi", "Jalankan dari <code>proyek/</code>:", "LAKUKAN"),
    kode("python -m pytest -q"),
    blok("hasil", "<pre><code>.                                     [100%]\n1 passed in 0.31s</code></pre>",
         "HARUS MUNCUL"),
    "<p>Titik itu satu uji yang lulus. Waktu di layarmu akan beda dari punyaku; "
    "<code>1 passed</code> tidak boleh beda.</p>")

langkah("Tiga aturan penamaan, dan itu saja",
    blok("aksi", "Baca sekali. Ini seluruh yang harus kamu hafal soal pytest.", "LAKUKAN"),
    tabel(["Aturan", "Contoh"],
          [["berkasnya diawali <code>test_</code>", "<code>tests/test_bersih.py</code>"],
           ["fungsinya diawali <code>test_</code>", "<code>def test_ke_angka_teks_biasa():</code>"],
           ["pemeriksaannya pakai <code>assert</code> biasa", "<code>assert ke_angka(…) == …</code>"]]),
    "<p>Tidak ada kerangka kerja yang harus kamu pelajari. Kalau kamu bisa menulis satu "
    "<code>assert</code>, kamu sudah bisa memakai pytest — sisanya cuma penamaan.</p>")

langkah("Tujuh kasus sekaligus, satu fungsi uji",
    blok("aksi", "Ganti fungsi uji tadi dengan bentuk ini.", "LAKUKAN"),
    kode('''@pytest.mark.parametrize("masuk,harap", [
    ("3.200.000", 3200000),
    ("Rp 91.190.000", 91190000),
    ("96.000", 96000),
    (22000, 22000),
    ("-96.000", -96000),
    ("", None),
    (None, None),
])
def test_ke_angka(masuk, harap):
    assert ke_angka(masuk) == harap'''),
    kode("python -m pytest -q"),
    blok("hasil", "<pre><code>.......                               [100%]\n7 passed in 0.29s</code></pre>",
         "HARUS MUNCUL"),
    "<p><strong>Tujuh titik, bukan satu.</strong> pytest menjalankannya sebagai "
    "<em>tujuh uji terpisah</em> — jadi kalau yang gagal cuma <code>\"-96.000\"</code>, ia akan "
    "menyebut persis kasus itu, bukan sekadar “fungsi ke_angka gagal”.</p>",
    blok("catatan", "<code>@pytest.mark.parametrize</code> adalah yang paling berguna untuk kode "
                    "data. Satu fungsi, sederet pasangan masukan-harapan."))

langkah("Tiga uji lagi, untuk dua fungsi lainnya",
    blok("aksi", "Tambahkan di bawahnya.", "LAKUKAN"),
    kode('''def test_rapikan_nama_menyatukan_empat_ejaan():
    s = pd.Series([" budi santoso ", "BUDI SANTOSO", "Budi  Santoso", "Budi Santoso"])
    assert rapikan_nama(s).nunique() == 1


def test_rapikan_nama_tidak_merusak_cv():
    s = pd.Series(["cv karya abadi", "PT mitra bangun"])
    assert list(rapikan_nama(s)) == ["CV Karya Abadi", "PT Mitra Bangun"]'''),
    kode('''def test_buang_baris_bukan_data():
    df = pd.DataFrame({"No": ["1", "2", "Dicetak oleh: Admin", None], "x": [1, 2, 3, 4]})
    assert len(buang_baris_bukan_data(df)) == 2'''),
    kode("python -m pytest -q"),
    blok("hasil", "<pre><code>..........                            [100%]\n10 passed in 0.30s</code></pre>",
         "HARUS MUNCUL"),
    "<p>Sepuluh uji, sepertiga detik. Bandingkan dengan kamu memeriksa sepuluh hal dengan mata "
    "<em>setiap kali</em> kamu mengubah satu baris — dan kamu tahu sendiri kamu tidak akan "
    "melakukannya sampai sepuluh kali.</p>")

langkah("Lihat apa yang sebenarnya dijalankan",
    blok("aksi", "Sekali saja, jalankan dengan <code>-v</code>.", "LAKUKAN"),
    kode("python -m pytest -v"),
    blok("hasil", "<pre><code>collected 10 items\n\n"
                  "tests/test_bersih.py::test_ke_angka[3.200.000-3200000] PASSED\n"
                  "tests/test_bersih.py::test_ke_angka[Rp 91.190.000-91190000] PASSED\n"
                  "...</code></pre>", "HARUS MUNCUL SEMACAM INI"),
    "<p>Tiap kasus <code>parametrize</code> punya namanya sendiri, dengan nilainya di dalam "
    "kurung siku. Itu yang akan muncul kalau salah satunya gagal — dan itulah gunanya.</p>",
    blok("catatan", "Sehari-hari pakai <code>-q</code> saja. <code>-v</code> untuk saat kamu "
                    "sedang mencari tahu uji mana yang bermasalah."))

langkah("Jalankan pytest dari folder yang salah, dengan sengaja",
    blok("aksi", "Buat folder kosong, masuk ke dalamnya, lalu jalankan ujimu dari sana.", "LAKUKAN"),
    kode("mkdir coba\ncd coba\npython -m pytest ../tests -q"),
    blok("bahaya", "<pre><code>E   ModuleNotFoundError: No module named 'laporan'\n"
                   "ERROR ../tests/test_bersih.py\n"
                   "!!!! Interrupted: 1 error during collection !!!!\n"
                   "1 error in 0.39s</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Perhatikan katanya: <strong>error</strong>, bukan <strong>failed</strong>. "
    "Ujimu tidak gagal — ujimu <em>tidak sempat dijalankan sama sekali</em>. pytest berhenti di "
    "tahap mengumpulkan (<em>collection</em>) karena tidak bisa meng-<code>import</code> "
    "paketmu.</p>",
    blok("catatan", "<strong>Bedakan dua kata ini seumur hidup:</strong> <code>failed</code> "
                    "berarti kodemu salah. <code>error</code> saat <em>collection</em> berarti "
                    "ujinya sendiri tidak bisa dibuka — hampir selalu karena kamu berada di folder "
                    "yang salah atau salah menulis nama import."),
    "<p>Bereskan: <code>cd ..</code> lalu hapus folder <code>coba</code>.</p>")

langkah("Apa yang layak diuji",
    blok("aksi", "Baca kolom kiri. Empat baris pertama sudah kamu kerjakan hari ini.", "LAKUKAN"),
    tabel(["Uji ini", "Jangan buang waktu untuk ini"],
          [["Fungsi pembersihan dengan masukan aneh: kosong, <code>NaN</code>, negatif, "
            "teks salah bentuk", "Bahwa pandas bisa menjumlahkan. Itu bukan kodemu."],
           ["Perhitungan bisnis dengan angka yang kamu hitung sendiri di kertas",
            "Bentuk tampilan atau warna grafik"],
           ["Kasus batas: nol baris, satu baris, semua nilai sama",
            "Kode yang sekali pakai lalu dibuang"],
           ["Bug yang <strong>pernah benar-benar terjadi</strong> — supaya tidak kembali",
            "Menargetkan “100% teruji”. Angka itu tidak berarti apa-apa."]]),
    "<p>Baris terakhir kolom kiri adalah yang paling bernilai, dan <strong>besok kamu akan "
    "melakukannya</strong> untuk bug yang kamu temukan sendiri kemarin.</p>")

langkah("Nama uji adalah kalimat, bukan label",
    blok("aksi", "Bandingkan dua nama ini. Tidak ada yang dijalankan.", "LAKUKAN"),
    kode("""def test_1():                                   # buruk
def test_rapikan_nama():                        # masih kabur
def test_rapikan_nama_menyatukan_empat_ejaan(): # bagus""", salin=False),
    "<p>Ketika uji gagal, <strong>yang pertama kamu baca adalah namanya</strong>. Nama yang bagus "
    "sudah memberitahumu apa yang rusak sebelum kamu membuka berkasnya.</p>",
    blok("catatan", "Pola yang enak dipakai: <code>test_&lt;fungsi&gt;_&lt;yang dijanjikan&gt;</code>. "
                    "Panjang tidak masalah — nama uji tidak pernah diketik ulang oleh siapa pun."))

langkah("Satu perintah yang akan kamu pakai tiap hari",
    blok("aksi", "Coba tiga bentuk ini.", "LAKUKAN"),
    kode("""python -m pytest -q                       # semuanya, ringkas
python -m pytest -q -x                    # berhenti di kegagalan pertama
python -m pytest -q -k kurung             # hanya uji yang namanya mengandung "kurung\""""),
    blok("hasil", "<pre><code>10 passed in 0.30s</code></pre>",
         "HARUS MUNCUL (yang pertama)"),
    "<p><code>-x</code> berguna saat kamu sedang memperbaiki sesuatu dan tidak ingin membaca "
    "dua puluh kegagalan yang sebabnya sama. <code>-k</code> berguna saat ujimu sudah ratusan.</p>",
    blok("bahaya", "<code>-k kurung</code> hari ini tidak cocok dengan apa pun dan akan mengeluarkan "
                   "<code>no tests ran</code>. Itu benar — ujinya baru ada besok."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Tiga aturan penamaan pytest?
2. Apa yang dilakukan @pytest.mark.parametrize?
3. Satu hal yang paling layak diuji, menurut tabel tadi?
4. Perintah untuk berhenti di kegagalan pertama?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. Berkas diawali <code>test_</code>, fungsi diawali <code>test_</code>, "
    "pemeriksaannya <code>assert</code>. "
    "2. Menjalankan satu fungsi uji sebagai <strong>beberapa uji terpisah</strong>, satu per "
    "pasangan masukan-harapan. "
    "3. Bug yang pernah benar-benar terjadi. "
    "4. <code>python -m pytest -q -x</code>.</p></details>")

HARI2 = {
  "n": "HARI 2",
  "tab": "2",
  "judul": "Pengujian: cara berhenti memeriksa ulang dengan mata",
  "waktu": "± 60 menit",
  "tujuan": "menulis uji otomatis untuk kode data, dan menjalankan sepuluh pemeriksaan sekaligus "
            "dalam satu perintah dan sepertiga detik.",
  "langkah": L,
  "tutup_judul": "Hari 2 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> sepuluh uji yang berjalan dalam 0,30 detik, dan "
           "tiga aturan penamaan yang cukup untuk seluruh karier analismu.</p>"
           "<p style=\"margin-top:8px\">Sejauh ini semuanya hijau — dan uji yang selalu hijau "
           "belum membuktikan apa pun. <strong>Besok kamu akan membuatnya merah</strong>, dengan "
           "bug sungguhan yang kamu temukan sendiri di Hari 1.</p>",
}
