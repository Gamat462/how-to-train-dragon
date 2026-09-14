# -*- coding: utf-8 -*-
"""Hari 33 — batas ekonomis dan alokasi biaya: dua tempat angka bisa dibuat jadi apa saja."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Batas ekonomis: kapan sumur berhenti layak diproduksi",
    "<p>Sebuah sumur ditutup bukan ketika minyaknya habis, melainkan ketika hasil "
    "jualnya tidak lagi menutup biaya menjalankannya.</p>",
    kode("batas_ekonomis (bopd) = biaya_per_sumur_per_bulan / (30,44 × harga_per_bbl)",
         salin=False),
    blok("aksi", "Muat biaya operasi 2025, tapi hati-hati mengetik nama kolomnya.",
         "LAKUKAN"))

langkah("Ketik ulang cepat, dan lihat layar merahmu",
    "<p>Kolom tanggal periodenya bernama <code>periode</code>. Kalau tanganmu lebih "
    "cepat dari matamu (sangat mudah terjadi kalau kamu terbiasa <code>periods</code> "
    "dari Excel/BI lain):</p>",
    kode('opex25 = biaya[(biaya.jenis=="OPEX") & (biaya.periods.str.startswith("2025"))]',
         salin=True),
    blok("hasil", "<div class=\"kode\"><pre><code>Traceback (most recent call last):\n"
                  "  File \"&lt;stdin&gt;\", line 1, in &lt;module&gt;\n"
                  "AttributeError: 'DataFrame' object has no attribute 'periods'</code></pre></div>",
         "HARUS MUNCUL — TULISAN MERAH, DAN ITU DISENGAJA"),
    blok("catatan", "<strong>Itu wajar — pandas mengizinkan <code>biaya.periode</code> "
                    "(titik) sebagai jalan pintas dari <code>biaya[\"periode\"]</code>, "
                    "tapi jalan pintas itu cuma bekerja untuk nama kolom yang benar.</strong> "
                    "Salah eja satu huruf, dan Python membacanya sebagai mencari atribut "
                    "Python biasa yang tidak ada — bukan mencari kolom. Perbaikannya: "
                    "<code>biaya.periode</code>, atau lebih aman lagi <code>biaya[\"periode\"]</code>, "
                    "yang akan memberi <code>KeyError</code> yang lebih jelas kalau salah."))

langkah("Sekarang jalankan yang benar",
    kode("""opex25 = biaya[(biaya.jenis=="OPEX") & (biaya.periode.str.startswith("2025"))]
opex_lap = opex25.groupby("lapangan_id").nilai_usd.sum()
n_sumur  = sumur[sumur.tipe_sumur=="Producer"].groupby("lapangan_id").size()
opex_bln = (opex_lap / 12 / n_sumur).round(0)
print(opex_bln)
for harga in [50, 65, 80]:
    el = (opex_bln / (30.44*harga)).round(1)
    print(f"@ ${harga}/bbl :", ", ".join(f"{k}={v}" for k,v in el.items()))"""),
    blok("hasil", "<p>OPEX per sumur per bulan: F01 $55.227 · F02 $51.791 · F03 "
                  "$145.551 · F04 $328.570</p>", "HARUS MUNCUL"),
    tabel(["harga", "F01", "F02", "F03", "F04"],
          [["$50/bbl", "36,3 bopd", "34,0", "95,6", "215,9"],
           ["$65/bbl", "27,9 bopd", "26,2", "73,6", "166,1"],
           ["$80/bbl", "22,7 bopd", "21,3", "59,8", "134,9"]]),
    "<p>Bandingkan dengan produksi aktual kuartal terakhir: pada $65/bbl, "
    "<strong>1 sumur dari 59</strong> di bawah batasnya — <strong>CDN-011</strong> "
    "(F01), 27,3 bopd terhadap batas 27,9 bopd.</p>")

langkah("Jebakan pertama: harga yang mana?",
    "<p>Kita baru pakai harga ICP penuh, $65/bbl. Tapi kontraktor tidak menerima $65 "
    "per barel — dari Migas L1 kamu tahu government take sekitar 70,5%, bagian bersih "
    "kontraktor cuma <strong>$19,79/bbl</strong>. Kalau angka itu dipakai:</p>",
    blok("hasil", "<p>Batas ekonomis melonjak jadi F01 91,7 · F02 86,0 · F03 241,6 "
                  "· F04 545,4 bopd — dan yang di bawah batas bukan 1 sumur lagi, "
                  "melainkan <strong>26 dari 59.</strong></p>", "HARUS MUNCUL"),
    "<p><strong>Satu sumur atau dua puluh enam sumur.</strong> Datanya identik. "
    "Selisihnya cuma soal harga mana yang dipakai — dan itu keputusan analis.</p>",
    "<details><summary>Mana yang benar? Pikirkan dulu, baru buka.</summary><div class=\"isi\">"
    "<p>Yang benar: <strong>harga penuh ($65)</strong>. Di PSC cost recovery, OPEX "
    "<em>dikembalikan lebih dulu dari gross revenue</em> sebelum sisanya dibagi — jadi "
    "“apakah sumur ini layak” dijawab di tingkat gross. Netback $19,79 adalah "
    "<em>hasil</em> dari pembagian setelah biaya dipulihkan; memakainya berarti "
    "menghitung biaya dua kali.</p>"
    "<p><strong>Yang wajib kamu tulis:</strong> “Batas ekonomis dihitung terhadap "
    "harga gross ICP karena OPEX bersifat cost-recoverable di dalam PSC ini.”</p>"
    "</div></details>")

langkah("Jebakan kedua: biaya rata-rata bukan biaya marjinal",
    "<p>Kita membagi seluruh OPEX lapangan rata ke semua sumurnya — untuk F04 itu "
    "$328.570 per sumur per bulan.</p>",
    blok("bahaya", "<strong>Kalau satu sumur F04 ditutup, apakah perusahaan menghemat "
                   "$328.570 sebulan? Tidak.</strong> Sebagian besar OPEX lapangan "
                   "adalah biaya fasilitas — pompa induk, pemisah, tenaga kerja, "
                   "pemeliharaan pipa — yang tetap berjalan apakah ada 9 atau 8 sumur. "
                   "Batas ekonomis versi biaya rata-rata karenanya <strong>terlalu "
                   "tinggi.</strong>"),
    blok("catatan", "<strong>Cara menuliskannya tanpa data biaya per sumur yang "
                    "sebenarnya:</strong> “Batas ini merupakan <em>batas atas</em>; "
                    "keputusan penutupan sumur tertentu memerlukan pemisahan biaya "
                    "tetap dan variabel yang tidak tersedia dalam data ini.” Kalimat "
                    "itu menyatakan metode, arah biasnya, dan data yang dibutuhkan "
                    "untuk memperbaikinya sekaligus."))

langkah("L5.3 — alokasi G&A: tiga metode, tiga jawaban, nol yang salah",
    "<p>Biaya G&A (kantor pusat, keuangan, hukum, SDM) tidak melekat pada lapangan "
    "mana pun, tapi laporan per lapangan tetap harus memuatnya. Ini kertas kerja yang "
    "sudah kamu kenal dari KAP — alokasi biaya bersama ke unit-unit yang berbagi "
    "biayanya.</p>",
    kode("""vol25 = prod[prod.tanggal.dt.year==2025].merge(sumur[["sumur_id","lapangan_id"]], on="sumur_id")
v   = vol25.groupby("lapangan_id").oil_bopd.sum()                   # basis: volume
n   = n_sumur                                                        # basis: jumlah sumur
akt = vol25[vol25.berproduksi==1].groupby("lapangan_id").size()      # basis: hari-sumur aktif
ga  = biaya[(biaya.kategori_biaya=="G&A Allocation") & (biaya.periode.str.startswith("2025"))].nilai_usd.sum()

alok = pd.DataFrame({"per_volume": ga*v/v.sum(), "per_sumur": ga*n/n.sum(),
                     "per_hari_aktif": ga*akt/akt.sum()}).round(0)
print(f"total G&A 2025: ${ga:,.0f}"); print(alok)"""),
    blok("hasil", "<p>Total G&A 2025 yang dialokasikan: <strong>$8.128.457</strong></p>",
         "HARUS MUNCUL"),
    tabel(["lapangan", "per volume", "per sumur", "per hari aktif"],
          [["F01", "1.336.455", "2.755.409", "2.745.716"],
           ["F02", "1.073.328", "2.342.098", "2.334.761"],
           ["F03", "2.227.649", "1.791.016", "1.803.593"],
           ["F04", "<strong>3.491.025</strong>", "<strong>1.239.934</strong>", "1.244.387"]]))

langkah("F04 untung besar, atau untung biasa saja — bergantung metodenya",
    "<p>F04 menanggung $3,49 juta atau $1,24 juta — selisih $2,25 juta, cukup untuk "
    "mengubah F04 dari lapangan paling untung jadi lapangan biasa saja di laporan "
    "profitabilitas per lapangan.</p>",
    blok("catatan", "<strong>Ketiganya bisa dibela.</strong> Per volume: yang paling "
                    "banyak menghasilkan, paling banyak memakai jasa kantor pusat. Per "
                    "sumur: G&A didorong jumlah aset yang dikelola. Per hari-sumur "
                    "aktif: mirip per sumur, tapi memperhitungkan sumur yang lama "
                    "tidak jalan. <strong>Yang salah adalah menyajikan satu angka "
                    "tanpa menyebut metodenya</strong> — sama seperti kamu tidak akan "
                    "meloloskan kertas kerja klien yang mengalokasikan biaya bersama "
                    "tanpa mendokumentasikan dasarnya."),
    blok("bahaya", "<strong>Ini juga tempat tekanan datang.</strong> Manajer F04 punya "
                   "alasan kuat menyukai alokasi per sumur; manajer F01 menyukai per "
                   "volume. Perlindunganmu: sajikan <strong>ketiganya sekaligus</strong> "
                   "di lampiran, dan pilih satu sebagai dasar dengan alasan tertulis "
                   "eksplisit — supaya yang bisa didebat adalah alasannya, bukan "
                   "integritasmu."))

HARI5 = {
  "n": "MIGAS HARI 33",
  "tab": "33",
  "judul": "Batas ekonomis dan alokasi biaya: dua tempat angka bisa dibuat jadi apa saja",
  "waktu": "± 85 menit",
  "tujuan": "menghitung kapan sebuah sumur berhenti layak diproduksi, dan menunjukkan "
            "bagaimana metode alokasi biaya yang berbeda menghasilkan jawaban berbeda "
            "tanpa satu pun yang salah.",
  "langkah": L,
  "tutup_judul": "Hari 33 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu error nyata (kolom salah eja), "
           "dan dua kalimat siap pakai untuk laporan mana pun — “dihitung terhadap "
           "harga gross karena cost-recoverable” dan “angka ini batas atas "
           "karena sebagian biaya bersifat tetap”.</p>",
}
