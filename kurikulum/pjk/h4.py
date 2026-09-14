# -*- coding: utf-8 -*-
"""Hari 4 — golden dataset: bahasa lowongan untuk yang sudah kamu kuasai."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Empat istilah lowongan ini, dan kamu sudah punya ketiganya",
    blok("aksi", "Baca tabel ini sekali.", "LAKUKAN"),
    tabel(["Istilah di lowongan", "Artinya", "Yang kamu punya"],
          [["Reference dataset", "Data yang dianggap benar, dipakai sebagai pembanding",
            "Tabel <code>pjk_wp</code> — tujuh wajib pajak yang angkanya sudah kamu hitung "
            "manual dan periksa di hari 2-3"],
           ["Golden dataset / golden values", "Jawaban yang sudah diverifikasi benar untuk "
            "kasus-kasus tertentu", "Tujuh angka pajak yang kamu <strong>hitung sendiri lewat "
            "SQL</strong> dua hari terakhir"],
           ["Output comparison", "Membandingkan hasil kode dengan golden values",
            "Persis yang kamu lakukan tiap kali membandingkan <code>pajak_naif</code> dan "
            "<code>pajak_benar</code>"],
           ["Regression control", "Alat yang berteriak kalau perubahan kode merusak jawaban "
            "yang tadinya benar", "<strong>Belum kamu punya — ini yang hari ini kamu bangun</strong>"]]),
    "<p>Tiga dari empat sudah ada, cuma belum berbentuk kode yang bisa dijalankan otomatis. "
    "Hari ini kamu mengubah yang keempat jadi nyata.</p>")

langkah("Pindahkan aturan pajak dari SQL ke fungsi Python",
    blok("aksi", "Berkas baru: <code>hitung_pajak.py</code>. Ini terjemahan langsung dari "
                 "query hari 2-3, ditulis sebagai fungsi.", "LAKUKAN"),
    kode('LAPISAN = [(0, 60_000_000, 0.05), (60_000_000, 250_000_000, 0.15),\n'
         '           (250_000_000, 500_000_000, 0.25), (500_000_000, 5_000_000_000, 0.30),\n'
         '           (5_000_000_000, None, 0.35)]\n'
         'BATAS_UMKM = 4_800_000_000'),
    "<p>Angka yang sama persis dengan tabel <code>pjk_lapisan</code>. Kalau tabelnya berubah, "
    "daftar ini juga harus berubah — dua sumber kebenaran yang harus tetap sinkron, persis "
    "risiko yang dihadapi tim yang membangun modul pajak sungguhan.</p>")

langkah("Fungsi progresif, terjemahan langsung dari query GREATEST/LEAST",
    blok("aksi", "Tambahkan ke berkas yang sama.", "LAKUKAN"),
    kode('def pajak_progresif(penghasilan):\n'
         '    total = 0\n'
         '    for bawah, atas, tarif in LAPISAN:\n'
         '        atas_efektif = atas if atas is not None else penghasilan\n'
         '        bagian = max(0, min(penghasilan, atas_efektif) - bawah)\n'
         '        total += bagian * tarif\n'
         '    return round(total)'),
    "<p>Bandingkan baris <code>bagian = max(0, min(...))</code> dengan "
    "<code>GREATEST(0, LEAST(...))</code> di SQL hari 2 — pola yang <strong>persis "
    "sama</strong>, cuma bahasanya beda. Itu inti kenapa lowongan minta Python "
    "<em>dan</em> SQL: aturan yang sama harus bisa hidup di keduanya.</p>")

langkah("Fungsi final, terjemahan dari CASE WHEN dua syarat kemarin",
    blok("aksi", "Tambahkan.", "LAKUKAN"),
    kode('def pajak_final(jenis, penghasilan, omzet=None):\n'
         '    if jenis == "umkm" and omzet is not None and omzet <= BATAS_UMKM:\n'
         '        return round(omzet * 0.005)\n'
         '    return pajak_progresif(penghasilan)'),
    "<p><code>if ... and ...</code> di Python, <code>CASE WHEN ... AND ...</code> di SQL — "
    "aturan tiga-tingkat yang sama dari hari 3, ditulis ulang di bahasa kedua.</p>")

langkah("Golden values: angka yang sudah kamu buktikan benar",
    blok("aksi", "Berkas baru: <code>test_pajak.py</code>. Tiap angka di sini <strong>disalin "
                 "dari kotak keluaran SQL hari 2-3</strong>, bukan dari ingatan.", "LAKUKAN"),
    kode('from hitung_pajak import pajak_final\n\n'
         'def test_perorangan_bayu():\n'
         '    assert pajak_final("perorangan", 180_000_000) == 21_000_000\n\n'
         'def test_umkm_agus_lewat_batas():\n'
         '    assert pajak_final("umkm", 980_000_000, omzet=5_100_000_000) == 238_000_000'),
    blok("catatan", "Dua fungsi ditampilkan di sini; berkas lengkapnya berisi tujuh — satu per "
                    "wajib pajak di tabelmu. <code>21_000_000</code> dan <code>238_000_000</code> "
                    "adalah angka <strong>output comparison</strong> yang disebut lowongan, "
                    "ditulis sebagai kode, bukan sebagai kalimat di laporan."))

langkah("Jalankan — dan lihat golden values-mu lolos semua",
    blok("aksi", "Terminal VS Code.", "LAKUKAN"),
    kode("python3 -m pytest test_pajak.py -v", salin=False),
    blok("hasil", "<pre><code>test_pajak.py::test_perorangan_rina PASSED             [ 14%]\n"
                  "test_pajak.py::test_perorangan_bayu PASSED             [ 28%]\n"
                  "test_pajak.py::test_perorangan_sari PASSED             [ 42%]\n"
                  "test_pajak.py::test_perorangan_maya PASSED             [ 57%]\n"
                  "test_pajak.py::test_umkm_dimas PASSED                  [ 71%]\n"
                  "test_pajak.py::test_umkm_putri PASSED                  [ 85%]\n"
                  "test_pajak.py::test_umkm_agus_lewat_batas PASSED       [100%]\n\n"
                  "============ 7 passed in 0.02s ============</code></pre>",
         "HARUS MUNCUL"),
    "<p>Tujuh hijau. Ini <strong>bukti yang dilihat pewawancara</strong>, bukan cuma "
    "klaim — kamu bisa menjalankan ini ulang di depan mereka kalau diminta.</p>",
    blok("catatan", "Kalau hasilmu ada yang merah di sini, itu normal kalau kamu mengetik "
                    "ulang salah satu angka golden values-nya. Cocokkan lagi dengan kotak "
                    "keluaran SQL hari 2-3 — bukan dari ingatan."))

langkah("Sekarang rusak satu angka, seperti yang terjadi di dunia nyata",
    blok("aksi", "Bayangkan tim lain \"memperbaiki\" batas UMKM, tapi salah ketik — tiga nol "
                 "hilang dari Rp 4,8 miliar. Ganti baris ini di <code>hitung_pajak.py</code>.",
         "LAKUKAN"),
    kode("BATAS_UMKM = 4_800_000   # seharusnya 4_800_000_000"),
    blok("bahaya", "<strong>Jangan buru-buru sadar ini salah.</strong> Bayangkan kamu tidak "
                   "menulis baris ini sendiri — kamu cuma menerima perubahan dari rekan kerja "
                   "lewat pull request. Tanpa tes, kamu akan menyetujuinya karena kelihatan "
                   "seperti perbaikan kecil."))

langkah("Jalankan ulang — dan lihat regression control-mu bekerja",
    blok("aksi", "Terminal.", "LAKUKAN"),
    kode("python3 -m pytest test_pajak.py -v", salin=False),
    blok("hasil", "<pre><code>test_pajak.py::test_umkm_dimas FAILED              [ 71%]\n"
                  "test_pajak.py::test_umkm_putri FAILED               [ 85%]\n"
                  "test_pajak.py::test_umkm_agus_lewat_batas PASSED    [100%]\n\n"
                  "________________ test_umkm_dimas ________________\n\n"
                  "    def test_umkm_dimas():\n"
                  ">       assert pajak_final(\"umkm\", 150_000_000, omzet=900_000_000) == 4_500_000\n"
                  "E       AssertionError: assert 16500000 == 4500000\n\n"
                  "========== 2 failed, 5 passed in 0.03s ==========</code></pre>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    "<p>Dua tes gagal <strong>dalam sepersekian detik</strong>, sebelum kode ini pernah "
    "menyentuh data pajak sungguhan siapa pun. Dimas yang seharusnya bayar 4,5 juta jadi "
    "dihitung 16,5 juta — salah arah, dan pytest menangkapnya sebelum sempat terkirim.</p>")

langkah("Ini jawaban lengkap untuk syarat nomor lima lowongan",
    blok("aksi", "Baca sekali, ucapkan dengan suara.", "LAKUKAN"),
    blok("hasil", "<p>\"Saya membangun rangkaian tes dengan golden values yang saya verifikasi "
                  "sendiri lewat SQL, lalu membuktikan tes itu benar-benar berfungsi sebagai "
                  "regression control dengan sengaja merusak satu aturan dan melihat pytest "
                  "menangkapnya dalam dua tes yang gagal.\"</p>", "KALIMAT WAWANCARA"),
    "<p>Itu bukan definisi buku teks — itu <strong>demonstrasi yang baru saja kamu jalankan "
    "sendiri</strong>, dua kali, dengan hasil yang berbeda dan bisa kamu tunjukkan.</p>")

langkah("Draf kalimat CV ketiga — yang paling kuat dari lima hari ini",
    blok("aksi", "Salin ke catatan lamaranmu.", "LAKUKAN"),
    blok("hasil", "<p>\"Membangun suite pengujian regresi (pytest) dengan golden dataset "
                  "terverifikasi untuk logika penghitungan pajak bertingkat, memvalidasi "
                  "efektivitasnya dengan menyuntikkan kesalahan yang disengaja dan "
                  "mengonfirmasi tes gagal sebagaimana mestinya.\"</p>", "DRAF CV #3"),
    blok("catatan", "\"Memvalidasi efektivitas tesnya sendiri\" adalah kalimat yang jarang "
                    "ditulis pelamar lain — kebanyakan orang menulis tes lalu berhenti, tanpa "
                    "pernah membuktikan tesnya benar-benar bisa gagal kalau memang harus "
                    "gagal. Kamu baru saja melakukannya."))

HARI4 = {
  "n": "HARI 4", "tab": "4",
  "judul": "Golden dataset: bahasa lowongan untuk yang sudah kamu kuasai",
  "waktu": "± 50 menit",
  "tujuan": "menerjemahkan aturan SQL hari 2-3 jadi fungsi Python, membangun regression "
            "control dengan pytest, lalu membuktikannya bekerja dengan merusaknya sendiri.",
  "langkah": L,
  "tutup_judul": "Hari 4 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> reference dataset, golden values, output "
           "comparison — tiga istilah yang sudah kamu praktikkan sejak hari 2 · regression "
           "control bukan cuma \"punya tes\", tapi <strong>membuktikan tesnya bisa gagal</strong> "
           "· satu kesalahan tiga-nol menyebabkan dua tes merah dalam sepersekian detik, "
           "bukan berbulan-bulan kemudian di produksi.</p>"
           "<p style=\"margin-top:8px\">Besok, hari terakhir: celah yang genuinely belum kamu "
           "punya — dan cara bicara soal itu tanpa berbohong.</p>",
}
