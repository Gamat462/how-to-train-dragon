# -*- coding: utf-8 -*-
"""Hari 35 — L5.5: memo $3 juta. Proyek akhir jalur migas."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Briefingnya",
    blok("catatan", "<p style=\"margin:0\"><strong>Dari: VP Operations · Kepada: "
                    "Analis Data · Perihal: Alokasi anggaran intervensi 2027</strong></p>"
                    "<p style=\"margin-top:10px\">Kita punya <strong>$3.000.000</strong> "
                    "untuk program intervensi sumur tahun depan. Biaya median satu "
                    "workover sekitar $857.000, jadi realistis kita bisa mengerjakan "
                    "tiga sumur.</p><p style=\"margin-top:10px\">Saya butuh satu halaman: "
                    "sumur mana, kenapa, berapa perkiraan hasilnya, dan seberapa yakin "
                    "kamu. Kalau menurutmu uangnya sebaiknya tidak dibelanjakan, "
                    "katakan itu — tapi tunjukkan angkanya.</p>", None),
    "<p>Perhatikan kalimat terakhirnya — itu bukan basa-basi. Analis pemula "
    "menganggap tugas ini “pilih tiga sumur”; analis yang dipercaya "
    "menganggapnya “jawab apakah ini belanja yang benar, dan kalau ya, yang "
    "mana”.</p>")

langkah("Bangun daftar kandidat dari bukti, bukan dari firasat",
    blok("aksi", "Dasar yang paling bisa dipertahankan: uptime. Sumur yang sering "
                 "berhenti kehilangan produksi yang bisa dikembalikan, dan besarnya "
                 "bisa dihitung langsung dari data.", "LAKUKAN"),
    kode("""h1 = prod[prod.tanggal >= "2026-01-01"]
a = h1.groupby("sumur_id").agg(bopd=("oil_bopd","mean"), uptime=("berproduksi","mean"))
a = a.join(sumur.set_index("sumur_id")[["lapangan_id","tipe_sumur","metode_angkat"]])
a = a[a.tipe_sumur == "Producer"]

TARGET = 0.989                                 # uptime median blok
a["gain_bopd"] = (a.bopd * (TARGET/a.uptime - 1)).round(1)
a.loc[a.uptime >= TARGET, "gain_bopd"] = 0
print(a.nsmallest(6, "uptime")[["lapangan_id","bopd","uptime","gain_bopd"]])"""),
    tabel(["sumur", "lap.", "bopd", "uptime", "gain bopd"],
          [["CDN-028", "F02", "274,6", "0,834", "<strong>50,9</strong>"],
           ["CDN-003", "F01", "257,6", "0,878", "32,4"],
           ["CDN-052", "F03", "304,9", "0,884", "<strong>36,2</strong>"],
           ["CDN-046", "F03", "169,0", "0,912", "14,3"],
           ["CDN-025", "F02", "149,1", "0,917", "11,7"],
           ["CDN-011", "F01", "25,2", "0,928", "1,7"]]),
    blok("catatan", "<strong>Kalau baris terakhirmu beda,</strong> cek CDN-049 — ia "
                    "tepat seri dengan CDN-011 di uptime 0,928 (sampai tiga desimal), "
                    "dan pandas memutus serinya lewat urutan sumur_id. Ini bukan "
                    "bug-mu."))

langkah("Uptime terendah belum tentu sumur paling berharga",
    "<p>CDN-011 punya uptime rendah tapi produksinya cuma 25 bopd — kehilangannya "
    "kecil dalam barel apa pun uptime-nya. <strong>Urutkan berdasarkan yang kamu "
    "pedulikan (barel yang bisa kembali), bukan berdasarkan gejalanya (uptime).</strong></p>",
    kode('print(a.nlargest(4,"gain_bopd")[["bopd","uptime","gain_bopd"]])'),
    tabel(["sumur", "bopd", "uptime", "gain bopd"],
          [["CDN-028", "274,6", "0,834", "<strong>50,9</strong>"],
           ["CDN-052", "304,9", "0,884", "36,2"],
           ["CDN-003", "257,6", "0,878", "32,4"],
           ["CDN-049", "468,2", "0,928", "30,7"]]),
    "<p>Peringkat berubah total begitu diurutkan berbasis barel. Tiga teratas: "
    "<strong>CDN-028, CDN-052, CDN-003</strong> — total gain <strong>119,6 bopd</strong>.</p>")

langkah("Nilai dalam dolar — dengan biaya yang bisa kamu pertanggungjawabkan",
    "<p>Kita belum tahu berapa biaya intervensi tiap sumur secara spesifik. Daripada "
    "menebak jenis pekerjaannya, pakai <strong>biaya median seluruh riwayat "
    "workover blok</strong> sebagai estimasi tunggal yang transparan — asumsi yang "
    "bisa kamu tunjukkan sumbernya ke siapa pun yang bertanya.</p>",
    kode('BIAYA_EST = wo.biaya_usd.median()\nprint(f"${BIAYA_EST:,.0f} per workover")'),
    blok("hasil", "<p><code>$857.414 per workover</code></p>", "HARUS MUNCUL"),
    "<p>Tiga sumur × $857.414 = <strong>$2.572.242</strong>, tersisa "
    "<strong>$427.758</strong> dari anggaran $3 juta.</p>")

langkah("Margin per barel, dan berapa lama tiap sumur impas",
    kode("""ICP, LIFT = 69.93, 14.35             # dari Minggu 1 & 4
MARGIN = ICP - LIFT
for w, gain in [("CDN-028",50.9), ("CDN-052",36.2), ("CDN-003",32.4)]:
    hari = BIAYA_EST / MARGIN / gain
    print(f"{w}: impas {hari:.0f} hari ({hari/365:.2f} tahun)")"""),
    blok("hasil", "<p>Margin per barel inkremental <strong>$55,58</strong>.</p>"
                  "<p style=\"margin-top:8px\">CDN-028 impas <strong>303 hari (0,83 "
                  "tahun)</strong> · CDN-052 <strong>426 hari (1,17 tahun)</strong> "
                  "· CDN-003 <strong>476 hari (1,30 tahun)</strong>, dengan asumsi "
                  "kenaikannya bertahan penuh.</p>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Seluruh keputusan ini bergantung pada satu angka yang "
                   "belum pernah kita ukur: berapa lama kenaikannya bertahan.</strong> "
                   "Kalau ternyata cuma bertahan setengah dari asumsi ini, semua "
                   "angka impas di atas berlipat dua."))

langkah("Ukur ketahanan gain dari 79 workover historis — hati-hati, jebakan menanti",
    "<p>Sebagian workover historis sudah cukup lama untuk diamati setahun penuh "
    "tanpa terganggu workover berikutnya. Saring dulu segmen yang bersih (logika "
    "sama seperti Hari 30–31), lalu bandingkan produksi bulan ke-12 terhadap "
    "baseline 90 hari sebelum pekerjaan dimulai.</p>",
    blok("hasil", "<p><strong>19 dari 79</strong> workover cukup lama diamati. Median "
                  "gain bulan ke-3: <strong>+28,3 bopd</strong>. Median gain bulan "
                  "ke-12 (naif, terhadap baseline mentah): <strong>−26,3 bopd</strong>. "
                  "Dari 19 sumur, yang masih di atas baseline di bulan ke-12: "
                  "<strong>nol</strong>.</p>", "HARUS MUNCUL"),
    blok("bahaya", "<strong>Berhenti. Jangan tulis “seluruh workover gagal dalam "
                   "setahun”.</strong> Kamu baru saja mengulangi kesalahan Minggu "
                   "2 dari arah sebaliknya: membandingkan sesudah terhadap sebelum "
                   "<em>tanpa memperhitungkan bahwa sumur memang menurun dengan "
                   "sendirinya.</em> Sumur yang menurun 21% per tahun akan berada di "
                   "bawah baseline-nya 12 bulan kemudian meski workovernya berhasil "
                   "sempurna."))

langkah("Bandingkan terhadap kontrafaktual — bukan terhadap baseline",
    "<p>Pembanding yang benar: <strong>berapa produksinya seandainya workover "
    "tidak dilakukan.</strong> Alat untuk membuat kontrafaktual itu adalah kurva "
    "decline yang kamu bangun Hari 29–32 — ukur laju penurunan alami dari 180 hari "
    "<em>sebelum</em> workover (regresi log-linear), lalu proyeksikan. Buang juga "
    "workover yang jendela “sebelum”-nya sendiri terkontaminasi workover "
    "lain dalam 270 hari terakhir.</p>",
    kode("""D_alami = -np.polyfit((pre.tanggal-pre.tanggal.min()).dt.days/365.0,
                       np.log(pre.oil_bopd.clip(lower=1)), 1)[0]
kontra = baseline * np.exp(-D_alami * dt)          # produksi SEANDAINYA tanpa workover
gain_vs_kontra = aktual_bulan12 - kontra"""),
    blok("hasil", "<p><strong>14 sumur</strong> lolos saringan kontaminasi (5 dibuang). "
                  "Median D alami <strong>0,21/tahun</strong>. Median gain bulan-12 "
                  "<strong>terhadap kontrafaktual: +15,8 bopd</strong>, positif pada "
                  "<strong>12 dari 14 sumur</strong> — tiga terbesar CDN-057 (+257,4), "
                  "CDN-049 (+58,5), CDN-062 (+46,0).</p>", "HARUS MUNCUL"),
    blok("catatan", "<strong>Tandanya berbalik.</strong> Perbandingan naif: "
                    "<strong>−26,3 bopd</strong>, kesimpulan “semua gagal”. "
                    "Perbandingan kontrafaktual: <strong>+15,8 bopd</strong>, kesimpulan "
                    "“efeknya bertahan pada mayoritas kasus”. Data historis "
                    "yang sama — yang beda cuma <em>terhadap apa</em> kamu "
                    "membandingkannya. Rasio ketahanan (gain bulan-12 ÷ gain bulan-3): "
                    "<strong>≈ 56%</strong>."))

langkah("Masukkan angka ketahanan itu ke keputusan $2,57 juta",
    "<p>Pakai rasio 56% pada gain portofolio (119,6 → <strong>66,8 bopd efektif</strong>) "
    "dan hitung ulang NPV pada diskonto 10%/tahun.</p>",
    tabel(["skenario", "NPV proyek"],
          [["100% (tanpa potongan), 2 tahun", "+$1.812.766"],
           ["<strong>56% (sesuai historis)</strong>, 2 tahun", "<strong>−$124.075</strong>"],
           ["56%, 3 tahun", "+$928.853"],
           ["56%, 5 tahun", "+$2.744.756"]]),
    "<p>Dengan rasio ketahanan yang realistis, proyeknya baru positif kalau "
    "kenaikannya bertahan <strong>lebih dari sekitar 2–3 tahun</strong> — dan bukti "
    "yang kita punya baru sampai bulan ke-12, dari 14 sumur.</p>")

langkah("Rekomendasi: bertahap, bukan semua atau tidak sama sekali",
    "<p>Tiga pilihan, dan yang ketiga hampir selalu benar ketika satu asumsi "
    "menguasai seluruh keputusan: belanjakan ketiganya sekarang (mempertaruhkan "
    "$2,57 juta pada ketahanan yang buktinya n = 14); jangan belanjakan sama "
    "sekali (membuang peluang yang tetap positif di skenario 3–5 tahun); atau "
    "<strong>belanjakan tahap pertama, ukur dengan pembanding yang benar, baru "
    "putuskan sisanya.</strong></p>",
    blok("catatan", "<strong>Rekomendasi:</strong> kerjakan <strong>CDN-028 saja</strong> "
                    "sekarang (~$857.414). Gainnya terbesar (50,9 bopd) dan impasnya "
                    "tercepat (0,83 tahun) di antara kandidat. Tahan sisa ~$1,71 juta. "
                    "<p style=\"margin-top:8px\"><strong>Sepakati SEBELUM pekerjaan "
                    "dimulai:</strong> baseline 90 hari pra-kerja, ukur bulan 3/6/9/12, "
                    "bandingkan terhadap <strong>kontrafaktual kurva decline</strong> "
                    "(bukan baseline mentah), dan lanjutkan sumur berikutnya hanya "
                    "kalau gain bulan-12 ≥ 56% gain bulan-3.</p>"))

langkah("Tulis memonya — satu halaman, tidak lebih",
    blok("aksi", "Pakai kerangka ini, isi dengan angkamu sendiri. Jangan lebih dari "
                 "satu halaman.", "LAKUKAN"),
    kode("""MEMO — Program Intervensi Sumur 2027, Blok Cendana
Kepada: VP Operations     Dari: [namamu]     Tanggal: [tanggal]

REKOMENDASI
Setujui tahap pertama ~$857.414 (CDN-028). Tahan sisa ~$1,71 juta sampai hasil
12 bulan terukur terhadap kontrafaktual. Keputusan penuh $3 juta belum bisa
dipertanggungjawabkan dengan data yang ada saat ini.

TEMUAN
1. Tiga sumur berpeluang terbesar: CDN-028, CDN-052, CDN-003. Total potensi
   119,6 bopd, biaya estimasi $2.572.242 (median historis per workover).
2. Pada margin inkremental $55,58/bbl, portofolio balik modal 0,83-1,3 tahun
   BILA kenaikannya bertahan penuh.
3. Ketahanan gain adalah variabel penentu. Pengukuran 14 workover historis
   terhadap kontrafaktual decline (bukan baseline mentah) memberi median
   +15,8 bopd di bulan-12, ~56% dari gain bulan-3. Dengan rasio itu, NPV
   2 tahun -$0,12 juta; 3 tahun +$0,93 juta.

BATASAN
- Kenaikan naif (vs baseline mentah) TIDAK dipakai: seluruhnya negatif median
  -26,3 bopd, karena tidak memperhitungkan decline alami -- perbandingan yang
  salah tandanya.
- Rasio ketahanan 56% berasal dari n=14, sebaran lebar (+257 s/d -2 bopd).
  Ke-14 sumur itu bukan sampel acak: mereka yang tidak perlu di-workover
  ulang, sehingga angkanya bisa jadi optimistis.
- Biaya estimasi memakai median historis seluruh jenis pekerjaan, bukan
  estimasi spesifik per sumur -- akan direvisi begitu survei teknik selesai.

LANGKAH BERIKUTNYA
1. Sepakati metrik & ambang keberhasilan sebelum pekerjaan dimulai.
2. Kerjakan CDN-028, ukur bulan 3/6/9/12 terhadap kontrafaktual decline.
3. Lanjutkan CDN-052 & CDN-003 bila gain bulan-12 >= 56% gain bulan-3.""", salin=False),
    blok("catatan", "<strong>Hitung ulang memo itu: berapa banyak angka, berapa "
                    "banyak batasan?</strong> Kira-kira seimbang — bukan kebetulan. "
                    "Memo yang seluruhnya angka terbaca seperti jualan; yang "
                    "seluruhnya peringatan terbaca seperti orang yang tidak berani "
                    "memutuskan. Yang dipercaya: <strong>rekomendasi jelas di kalimat "
                    "pertama</strong>, lalu titik persis di mana ia bisa salah."))

langkah("Latih menceritakannya — 3 menit, tanpa slide",
    "<p>Pertanyaan wawancara yang hampir pasti muncul: <em>“Ceritakan sebuah "
    "analisis yang kamu kerjakan dari awal sampai akhir.”</em> Rekam dirimu, "
    "sekitar tiga menit, urutan ini:</p>",
    "<ul style=\"font-size:0.93rem;padding-left:20px\">"
    "<li><strong>(15 dtk)</strong> Pertanyaannya: ke mana $3 juta anggaran "
    "intervensi sebaiknya dialokasikan.</li>"
    "<li><strong>(40 dtk)</strong> Jawaban pertamaku salah — kupasang kurva decline "
    "ke semua sumur, dapat 50 juta barel, R² minimumnya negatif. Ternyata 41 dari "
    "59 sumur pernah di-workover; datanya bukan satu decline, melainkan beberapa "
    "yang disambung.</li>"
    "<li><strong>(40 dtk)</strong> Setelah dibatasi ke segmen bersih dan ditambah "
    "terminal decline, angkanya turun ke 17,6 juta barel — 65% lebih kecil. Aku uji "
    "sensitivitas dua parameter kendali mutunya; rentangnya 15,5–22,9 juta, jadi "
    "kulaporkan sebagai rentang.</li>"
    "<li><strong>(35 dtk)</strong> Untuk anggaran intervensi, aku pakai selisih "
    "uptime — bukan kenaikan workover historis mentah, karena itu bias seleksi. "
    "Tiga sumur teratas balik modal 0,83–1,3 tahun kalau kenaikannya bertahan "
    "penuh.</li>"
    "<li><strong>(40 dtk)</strong> Lalu kuuji berapa lama kenaikan bertahan. "
    "Dibandingkan baseline mentah, semua kelihatan gagal — median −26 bopd. Tapi "
    "itu perbandingan salah; sumur memang menurun sendiri. Dibandingkan "
    "kontrafaktual kurva decline, mediannya <em>positif</em> +16 bopd, ketahanan "
    "sekitar 56%.</li>"
    "<li><strong>(30 dtk)</strong> Rekomendasiku: jangan belanjakan ketiganya "
    "sekaligus. Kerjakan satu sumur, ukur setahun terhadap kontrafaktual dengan "
    "ambang disepakati di muka, baru putuskan sisanya.</li></ul>",
    blok("catatan", "<strong>Yang dinilai pewawancara bukan angka akhirnya.</strong> "
                    "Mereka mendengar: kamu memeriksa hasilmu sendiri, kamu menemukan "
                    "kesalahanmu sendiri, kamu tahu bedanya model yang cocok dan model "
                    "yang benar, dan kamu berani merekomendasikan “tunggu "
                    "dulu” kepada orang yang punya anggaran."))

HARI7 = {
  "n": "MIGAS HARI 35 · PROYEK AKHIR",
  "tab": "35",
  "judul": "L5.5 — memo $3 juta",
  "waktu": "± 150 menit",
  "tujuan": "punya satu memo satu halaman yang merekomendasikan keputusan belanja "
            "modal $3 juta, lengkap dengan asumsi, sensitivitas, dan batasan — "
            "dokumen yang bisa kamu bawa ke wawancara.",
  "langkah": L,
  "tutup_judul": "Jalur spesialisasi migas selesai — Hari 29 sampai 35",
  "tutup": "<p>Lima hari lalu kamu memasang fungsi Arps yang meledak pada sumur "
           "pertama yang salah kamu pilih. Sekarang kamu bisa memasang dan "
           "<em>membantah</em> kurva decline-mu sendiri, mendiagnosis kenapa 69% "
           "sumurmu melanggar asumsi model, dan menulis rekomendasi belanja modal "
           "yang menyebutkan dengan tepat di titik mana ia bisa salah.</p>"
           "<p style=\"margin-top:14px\">Yang kamu bawa keluar bukan kumpulan query. "
           "Ini yang kamu bawa: <strong>kebiasaan memeriksa angkamu sendiri sebelum "
           "orang lain memeriksanya.</strong> Setiap angka di lima hari ini kamu "
           "hasilkan dengan menjalankan kode, bukan mengingat. Pertahankan itu, dan "
           "latar belakang auditmu berhenti jadi sesuatu yang perlu dijelaskan — "
           "ia jadi alasan kamu dipilih.</p>"
           "<p style=\"margin-top:14px\">Langkah berikutnya: bawa memo hari ini dan "
           "grafik lima tahap DCA ke portofoliomu (M14), lalu pakai keduanya sebagai "
           "bahan cerita di M15.</p>",
}
