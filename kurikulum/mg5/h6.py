# -*- coding: utf-8 -*-
"""Hari 34 — L5.4: sensitivitas PSC terhadap harga, dan angka 88,8%."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Bangun modelnya — urutan tidak boleh diubah",
    blok("aksi", "Alur PSC dari Migas L1 sekarang jadi kode: FTP dipotong lebih dulu, "
                 "baru cost recovery, sisanya ETS.", "LAKUKAN"),
    kode("""psc = pd.read_sql("SELECT * FROM psc_bulanan", con)

def hitung(faktor_harga):
    d   = psc.copy()
    g   = d.volume_bbl * d.icp_usd_bbl * faktor_harga
    ftp = g * 0.20
    tersedia = g - ftp
    cr  = np.minimum(np.minimum(d.biaya_recoverable_usd, tersedia), g*0.80)
    ets = np.maximum(tersedia - cr, 0)
    gov_pra = ftp*0.60 + ets*0.85
    kon_pra = ftp*0.40 + ets*0.15
    pajak   = np.maximum(kon_pra, 0) * 0.44
    return pd.Series({"gross": g.sum(), "cost_recovery": cr.sum(),
                      "gov_take": (gov_pra+pajak).sum(), "kontraktor": (kon_pra-pajak+cr).sum()})""", salin=False),
    "<p>Simpan fungsi ini — kamu akan panggil berkali-kali di sisa hari ini.</p>")

langkah("Jalankan untuk lima skenario harga",
    kode('for f, lbl in [(0.70,"-30%"),(0.85,"-15%"),(1.00,"dasar"),(1.15,"+15%"),(1.30,"+30%")]:\n'
         '    r = hitung(f)\n'
         '    print(lbl, r.gross, r.cost_recovery, r.gov_take, r.kontraktor)'),
    tabel(["skenario", "gross", "cost recovery", "gov take", "gov %", "kontraktor"],
          [["−30%", "926.080.723", "289.729.877", "556.967.115", "<strong>60,1%</strong>", "369.113.609"],
           ["−15%", "1.124.526.593", "289.729.877", "733.187.047", "65,2%", "391.339.546"],
           ["dasar", "1.322.972.462", "289.729.877", "909.406.979", "68,7%", "413.565.483"],
           ["+15%", "1.521.418.331", "289.729.877", "1.085.626.911", "71,4%", "435.791.421"],
           ["+30%", "1.719.864.201", "289.729.877", "1.261.846.843", "<strong>73,4%</strong>", "458.017.358"]]))

langkah("Perhatikan tiga hal sekaligus",
    "<ul style=\"font-size:0.93rem;padding-left:20px\">"
    "<li><strong>Cost recovery tidak bergerak sama sekali</strong> — $289.729.877 di "
    "kelima skenario. Biaya sudah terjadi; harga tidak mengubahnya.</li>"
    "<li><strong>Porsi pemerintah naik dari 60,1% ke 73,4%</strong> saat harga naik. "
    "Kontrak sama, pembagian sama, tapi persentasenya bergerak 13 poin.</li>"
    "<li><strong>Nilai absolut kontraktor tetap naik</strong>, dari $369 juta ke $458 "
    "juta. Persentasenya turun, dolarnya naik.</li></ul>",
    blok("bahaya", "<strong>Poin ketiga yang paling sering salah dibaca.</strong> "
                   "“Porsi kontraktor turun dari 39,9% ke 26,6%” terdengar "
                   "seperti kabar buruk. Padahal kontraktor menerima $89 juta lebih "
                   "banyak. Melaporkan persentase tanpa dolarnya memberi kesan yang "
                   "persis terbalik."))

langkah("Hitung porsi marjinal — inilah angka yang sebenarnya penting",
    "<p>Persentase rata-rata (68,7%) menjawab “dari seluruh pendapatan, berapa ke "
    "pemerintah”. Pertanyaan yang jauh lebih berguna untuk keputusan investasi: "
    "dari setiap dolar <strong>tambahan</strong>, berapa yang ke pemerintah?</p>",
    kode('a, b = hitung(1.00), hitung(1.15)\n'
         'print("porsi marjinal:", (b.gov_take-a.gov_take)/(b.gross-a.gross)*100)'),
    blok("hasil", "<p>Tambahan gross $198.445.869 · tambahan gov $176.219.932 · "
                  "<strong>porsi marjinal 88,8%</strong> — dan kalau kamu ulangi untuk "
                  "pasangan skenario lain, hasilnya <strong>88,8% persis, setiap "
                  "kali.</strong></p>", "HARUS MUNCUL"))

langkah("Angka 88,8% bisa diturunkan langsung dari kontraknya",
    kode("""FTP ke pemerintah       : 20% x 60%       = 12,0%
ETS ke pemerintah       : 80% x 85%       = 68,0%
                                            -------
sebelum pajak                              80,0%
kontraktor sebelum pajak: 20%x40%+80%x15% = 20,0%
pajak                   : 20,0% x 44%     =  8,8%
                                            -------
TOTAL ke pemerintah                        88,8%""", salin=False),
    blok("catatan", "<strong>Inilah kenapa persentase rata-rata bergerak.</strong> "
                    "Setiap dolar tambahan dibagi 88,8% : 11,2%, jauh lebih berat ke "
                    "pemerintah daripada rata-rata 68,7%. Begitu harga naik dan dolar "
                    "tambahan itu makin banyak porsinya dalam total, rata-ratanya "
                    "tertarik naik mendekati 88,8%."))

langkah("Terjemahkan ke satu kalimat untuk manajemen",
    "<p>Tulis versimu sendiri dulu, dalam bahasa yang dimengerti orang keuangan yang "
    "belum pernah membaca kontrak PSC. Baru buka.</p>",
    "<details><summary>Contoh jawaban</summary><div class=\"isi\">"
    "<p>“Dari setiap dolar pendapatan tambahan, kontraktor menerima 11,2 sen. "
    "Karena itu <strong>penghematan biaya jauh lebih berharga daripada kenaikan "
    "harga</strong>: menghemat $1 juta biaya operasi menambah sekitar $1 juta ke posisi "
    "kontraktor (biaya itu dipulihkan penuh), sementara menaikkan pendapatan $1 juta "
    "hanya menambah $112 ribu.”</p></div></details>",
    blok("catatan", "<strong>Simpan temuan ini.</strong> Besok, saat menilai proyek "
                    "intervensi $3 juta, kamu akan memakainya — proyek yang menaikkan "
                    "produksi dinilai pada 11,2 sen per dolar, proyek yang menurunkan "
                    "biaya dinilai mendekati 100 sen per dolar. Itu mengubah peringkat "
                    "kandidat secara mendasar."))

langkah("Batas model ini — yang wajib kamu sebutkan",
    "<p>Model tadi mengubah harga tapi menahan segalanya yang lain tetap. Di dunia "
    "nyata itu tidak berlaku: harga turun 30% seharusnya menjatuhkan sebagian sumur "
    "di bawah batas ekonomis (volume ikut turun); harga naik 30% membuat workover "
    "yang tadinya tidak layak jadi layak (biaya ikut naik). Model kita menahan "
    "keduanya tetap.</p>",
    blok("catatan", "<strong>Menyebutkan batasan bukan kelemahan laporan; itu yang "
                    "membuatnya bisa dipakai.</strong> Pembaca yang tahu model ini "
                    "menahan volume tetap bisa menilai sendiri seberapa jauh hasilnya "
                    "bisa dipercaya di skenario ekstrem. Pembaca yang tidak diberi tahu "
                    "akan memperlakukan angkanya sebagai ramalan."))

HARI6 = {
  "n": "MIGAS HARI 34",
  "tab": "34",
  "judul": "L5.4 — sensitivitas PSC terhadap harga, dan angka 88,8%",
  "waktu": "± 80 menit",
  "tujuan": "membangun sendiri model sensitivitas PSC dari nol, dan kamu bisa "
            "menjelaskan ke orang non-teknis kenapa porsi pemerintah justru naik "
            "ketika harga minyak naik.",
  "langkah": L,
  "tutup_judul": "Hari 34 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> satu angka konstan (88,8%) yang bisa "
           "kamu turunkan langsung dari klausul kontrak, dan satu kalimat siap pakai "
           "untuk manajemen tentang kenapa penghematan biaya lebih berharga daripada "
           "kenaikan harga.</p>",
}
