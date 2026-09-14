# -*- coding: utf-8 -*-
"""Hari 30 — Tahap B: diagnosis, lihat datanya sebelum menyalahkan modelnya."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Godaan yang harus kamu tolak hari ini",
    "<p>Setelah melihat R² 0,701 dengan minimum negatif, refleks paling umum adalah: "
    "coba model lain, coba polinomial, coba longgarkan batasnya, coba buang sumur yang "
    "aneh.</p>",
    blok("bahaya", "<strong>Semua itu menebak.</strong> Mengganti model sampai R² naik "
                   "namanya bukan analisis, namanya mencari angka yang enak dilihat. "
                   "Kalau kamu tidak tahu kenapa model sekarang gagal, kamu tidak punya "
                   "alasan percaya model berikutnya berhasil — kamu cuma tahu angkanya "
                   "lebih besar."),
    "<p>Urutan yang benar: <strong>lihat datanya dulu.</strong> Ambil sumur terburuk, "
    "gambar produksinya, cari tahu bentuk apa yang sebenarnya ada di sana.</p>")

langkah("Gambar sumur terburuk: CDN-028 (R² −0,047)",
    blok("aksi", "Muat tabel workover, lalu plot produksi bulanan CDN-028 dengan garis "
                 "vertikal di tiap tanggal workover-nya.", "LAKUKAN"),
    kode("""import matplotlib.pyplot as plt
con = sqlite3.connect("migas.db")
wo = pd.read_sql("SELECT * FROM workover", con, parse_dates=["tanggal_mulai"])
con.close()

W = "CDN-028"
g = prod[(prod.sumur_id==W) & (prod.berproduksi==1)]
m = g.set_index("tanggal").oil_bopd.resample("MS").mean()

fig, ax = plt.subplots(figsize=(11,4.5))
ax.plot(m.index, m.values, marker="o", markersize=4, color="#2b5d4f")
for _, r in wo[wo.sumur_id==W].iterrows():
    ax.axvline(r.tanggal_mulai, color="#c0392b", linestyle="--")
plt.show()"""),
    blok("hasil", "<p>Grafik <strong>gigi gergaji</strong>: turun landai, melonjak tajam, "
                  "turun lagi, melonjak lagi. Tiap lonjakan jatuh persis pada satu garis "
                  "merah putus-putus.</p>", "YANG HARUS TERLIHAT"))

langkah("Angka di balik gambarnya",
    "<p>CDN-028 punya <strong>empat workover</strong>: Acidizing (Okt 2024), "
    "Reperforation (Mar 2025), Scale Removal (Nov 2025), Zone Change (Apr 2026).</p>",
    tabel(["periode", "bopd sebelum", "bopd sesudah lompat"],
          [["Mar → Nov 2024", "305,7 → 262,4", "→ <strong>344,3</strong>"],
           ["Des 2024 → Mar 2025", "295,9 (Feb)", "→ <strong>402,9</strong>"],
           ["2025 → Nov 2025", "276,3 (Okt)", "→ <strong>385,1</strong>"],
           ["2026 → Mei 2026", "300,4", "→ <strong>367,7</strong>"]]),
    "<p>Setiap lompatan besar berbaris rapi di belakang satu tanggal workover. Itu bukan "
    "kebetulan — itu jawabannya.</p>")

langkah("Sekarang kamu tahu kenapa fit-nya gagal",
    "<p>Persamaan Arps memodelkan <strong>satu</strong> penurunan alami yang tidak "
    "diganggu. CDN-028 bukan satu penurunan — ia <strong>empat penurunan</strong> yang "
    "disambung oleh intervensi manusia. Memaksa satu kurva menurun melewati data yang "
    "naik-turun empat kali, satu-satunya kurva yang “muat” adalah kurva nyaris "
    "datar di tengah-tengahnya.</p>",
    blok("catatan", "<strong>Masalahnya tidak pernah ada di modelnya.</strong> Persamaan "
                    "Arps bekerja persis sebagaimana mestinya; masalahnya ada di data yang "
                    "kita berikan — data itu melanggar asumsi dasar model, dan model tidak "
                    "punya cara memberitahu kita. Model yang “gagal” hampir "
                    "selalu model yang diberi makan data yang tidak sesuai asumsinya."))

langkah("Seberapa luas masalahnya? Jangan menebak, hitung",
    "<p>Satu sumur bermasalah bisa dibuang. Kalau separuh blok bermasalah, itu menuntut "
    "perubahan metode. Ukur dulu.</p>",
    kode("""print("producer               :", (sumur.tipe_sumur=="Producer").sum())
print("pernah workover        :", wo.sumur_id.nunique())
print(wo.groupby("sumur_id").size().value_counts().sort_index())"""),
    blok("hasil", "<p>59 producer, <strong>41 pernah di-workover</strong> — 14 sumur "
                  "satu kali, 19 dua kali, 5 tiga kali, 3 empat kali.</p>", "HARUS MUNCUL"),
    "<p><strong>69% sumur</strong> punya riwayat yang melanggar asumsi model. Ini bukan "
    "pencilan yang bisa dibuang; ini sifat datanya. Metodenya yang harus berubah.</p>")

langkah("Rancang perbaikannya di kertas dulu, sebelum menulis kode",
    "<p>Sebelum melihat jawabannya, tulis jawabanmu sendiri: kalau model butuh satu "
    "penurunan tak terganggu, potongan data mana dari CDN-028 yang memenuhi syarat "
    "itu?</p>",
    "<details><summary>Setelah kamu menulis jawabanmu, buka ini</summary><div class=\"isi\">"
    "<p>Potongan yang sah: bagian <strong>setelah workover terakhir</strong> — "
    "satu-satunya rentang yang dijamin tak terpotong intervensi berikutnya.</p>"
    "<p>Tapi ada jebakan: tepat setelah workover, produksinya belum stabil. Lihat "
    "CDN-028 setelah Maret 2025: 402,9 → 385,7 → 363,1 → 342,9 → 320,0 — penurunan "
    "curam itu efek workover yang meluruh, bukan sifat reservoirnya.</p>"
    "<p>Jadi butuh <strong>dua</strong> aturan: mulai dari workover terakhir + "
    "<strong>270 hari</strong> masa tunggu (supaya efeknya sudah meluruh), dan sisa "
    "potongannya minimal <strong>14 bulan</strong> panjangnya. Kedua angka itu pilihan, "
    "bukan kebenaran — besok kamu uji apa yang terjadi kalau diubah.</p></div></details>")

HARI2 = {
  "n": "MIGAS HARI 30",
  "tab": "30",
  "judul": "Tahap B: diagnosis — lihat datanya sebelum menyalahkan modelnya",
  "waktu": "± 75 menit",
  "tujuan": "menemukan penyebab kegagalan model dengan memandang data mentahnya, "
            "bukan dengan kamu mengganti-ganti model sampai ada yang kelihatan bagus.",
  "langkah": L,
  "tutup_judul": "Hari 30 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> CDN-028 bukan sumur “rusak” — "
           "ia sumur normal yang datanya melanggar asumsi Arps karena empat workover. "
           "Dan kamu sudah tahu persis dua angka apa yang perlu dipilih untuk "
           "memperbaikinya.</p>",
}
