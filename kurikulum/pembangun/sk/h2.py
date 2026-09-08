# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L=[]
def langkah(judul,*isi): L.append({"judul":judul,"isi":"\n".join(isi)})

langkah("Buat kedua berkasnya",
    blok("aksi","Dari folder yang sama, jalankan:","LAKUKAN"),
    kode("python gen_k2.py"),
    blok("hasil", kode("kunjungan       : 240\ntagihan (baris) : 233\ntagihan ganda   : 11\nkunjungan tanpa tagihan: 18", salin=False),"HARUS MUNCUL"),
    "<p><strong>Empat angka itu jawabannya.</strong> Hari ini kamu harus sampai ke sana sendiri, "
    "lewat tiga cara yang salah dulu.</p>")

langkah("Dua berkas, dua format berbeda",
    kode('import pandas as pd\nk = pd.read_excel("Kunjungan Pasien 2024.xlsx")\nt = pd.read_csv("Tagihan Klinik 2024.csv", sep=";", decimal=",")\nprint(len(k), len(t))'),
    blok("hasil", kode("240 233", salin=False),"HARUS MUNCUL"),
    blok("catatan","<strong><code>sep=\";\"</code> itu wajib.</strong> CSV dari sistem Indonesia sering "
         "memakai titik koma, karena koma sudah dipakai sebagai pemisah desimal. Tanpa itu seluruh baris "
         "masuk ke satu kolom dan kamu akan menyangka berkasnya rusak."))

langkah("Cara salah #1: gabungkan apa adanya",
    kode('a = k.merge(t, on="Kode Kunjungan")\nprint("baris hasil:", len(a))'),
    blok("hasil", kode("baris hasil: 233", salin=False),"HARUS MUNCUL"),
    "<p>233 dari 240 kunjungan. Kelihatannya cuma tujuh yang hilang. "
    "<strong>Itu salah, dan salahnya jauh lebih besar.</strong></p>")

langkah("233 baris itu bukan 233 kunjungan",
    kode('print("kunjungan berbeda:", a["Kode Kunjungan"].nunique())\nprint("baris kembar    :", len(a) - a["Kode Kunjungan"].nunique())\nprint("kunjungan hilang:", k["Kode Kunjungan"].nunique() - a["Kode Kunjungan"].nunique())'),
    blok("hasil", kode("kunjungan berbeda: 222\nbaris kembar    : 11\nkunjungan hilang: 18", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>Dua kesalahan sekaligus, dan sebagian saling menutupi:</strong>"
         "<div class=\"kode\" style=\"margin-top:8px\"><pre><code>240 kunjungan − 18 hilang + 11 kembar = 233 baris</code></pre></div>"
         "Jumlah baris yang terlihat wajar itu justru yang membuatnya tidak ketahuan. "
         "Kalau kamu berhenti di <code>len(a)</code>, kamu tidak akan pernah tahu."))

langkah("Kenapa 18 kunjungan lenyap",
    "<p>Karena <code>merge</code> bawaannya <em>inner</em> — hanya menyimpan baris yang cocok "
    "di kedua sisi. Kunjungan yang belum ditagih tidak punya pasangan, jadi dibuang tanpa peringatan.</p>",
    blok("catatan","<strong>Ini kebiasaan yang harus dibalik.</strong> Bawaan pandas adalah "
         "<em>buang yang tidak cocok</em>. Bawaan seorang auditor seharusnya <em>hitung dulu yang "
         "tidak cocok, baru putuskan</em> — karena di situlah temuannya."))

langkah("Cara salah #2: left join, tapi lupa tagihan gandanya",
    kode('b = k.merge(t, on="Kode Kunjungan", how="left")\nprint("baris hasil:", len(b))\nprint("total      :", f\'{b["Total"].sum():,.0f}\')'),
    blok("hasil", kode("baris hasil: 251\ntotal      : 31,580,000", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>251 baris dari 240 kunjungan.</strong> Hasil gabungan yang <em>lebih banyak</em> "
         "daripada tabel kirinya selalu berarti satu hal: kunci di tabel kanan tidak unik. "
         "Sebelas tagihan ganda menggandakan sebelas kunjungan."))

langkah("Cara yang benar: buang gandanya dulu",
    kode('tb = t.drop_duplicates("Kode Kunjungan", keep="first")\nc = k.merge(tb, on="Kode Kunjungan", how="left", indicator=True)\nprint("baris hasil:", len(c), "| cocok?", len(c) == len(k))\nprint("total      :", f\'{c["Total"].sum():,.0f}\')'),
    blok("hasil", kode("baris hasil: 240 | cocok? True\ntotal      : 30,165,000", salin=False),"HARUS MUNCUL"),
    blok("catatan","<strong><code>len(hasil) == len(kiri)</code> adalah pemeriksaan wajib</strong> setiap "
         "kali kamu <code>merge</code> dengan <code>how=\"left\"</code>. Satu baris kode, dan ia menangkap "
         "kesalahan yang paling mahal di seluruh pekerjaan analis."))

langkah("Berapa yang tercatat dua kali",
    kode('ganda = t[t.duplicated("Kode Kunjungan", keep="first")]\nprint(f\'{ganda["Total"].sum():,.0f}\')'),
    blok("hasil", kode("1,415,000", salin=False),"HARUS MUNCUL"),
    "<p>Rp 31.580.000 − Rp 30.165.000 = <strong>Rp 1.415.000</strong> yang dilaporkan dua kali. "
    "Untuk klinik kecil, itu bukan angka yang bisa diabaikan.</p>")

langkah("Dan yang belum ditagih sama sekali",
    kode('belum = c[c["_merge"] == "left_only"]\nprint("kunjungan :", len(belum))\nprint("nilainya  :", f\'{belum["Tarif"].sum():,.0f}\')'),
    blok("hasil", kode("kunjungan : 18\nnilainya  : 2,745,000", salin=False),"HARUS MUNCUL"),
    blok("catatan","<strong>Inilah temuan yang tidak diminta klien, dan yang paling dia butuhkan.</strong> "
         "Bu Ratih bertanya \"berapa pendapatan kami\". Jawaban yang berguna: pendapatan Rp 30,2 juta, "
         "<em>dan ada Rp 2,7 juta pekerjaan yang sudah dikerjakan tapi belum pernah ditagih</em>."))

langkah("Nama pasien: 20 ejaan untuk 15 orang",
    kode('print("nama berbeda:", k["Nama Pasien"].nunique())\nprint("ID berbeda  :", k["ID Pasien"].nunique())'),
    blok("hasil", kode("nama berbeda: 20\nID berbeda  : 15", salin=False),"HARUS MUNCUL"),
    kode('per_id = k.groupby("ID Pasien")["Nama Pasien"].unique()\nprint(per_id[per_id.map(len) > 1].to_string())'),
    blok("hasil", kode("1  ['SITI NURHALIZA' 'Siti Nurhalizah' 'siti nurhaliza']\n4  ['BAMBANG WIJAYA' 'Bambang Widjaja' 'Bambang Wijaya']\n9  ['Fitri Handayani' 'Fitri Handayanti']", salin=False),"HARUS MUNCUL"),
    blok("bahaya","Kalau kamu mengelompokkan pasien berdasarkan <strong>nama</strong>, Siti dihitung "
         "sebagai tiga orang. Kelompokkan berdasarkan <strong>ID</strong> — dan pakai nama hanya untuk "
         "ditampilkan, tidak pernah untuk mengelompokkan."))

langkah("Penjamin: sembilan tulisan untuk tiga hal",
    kode('print(sorted(k["Penjamin"].dropna().unique()))'),
    blok("hasil", kode("['Asuransi', 'B.P.J.S', 'BPJS', 'BPJS Kesehatan', 'UMUM',\n 'Umum', 'asuransi swasta', 'bpjs', 'umum']", salin=False),"HARUS MUNCUL"),
    blok("catatan","Sembilan tulisan, tiga penjamin sesungguhnya. Merapikannya "
         "<strong>bukan pekerjaan teknis</strong> — kamu harus memutuskan apakah "
         "\"asuransi swasta\" sama dengan \"Asuransi\". Itu keputusan yang harus kamu tanyakan "
         "ke Bu Ratih, bukan kamu tebak sendiri."))

langkah("Ulangi dari ingatan",
    blok("aksi","Tutup halaman. Jawab empat hal, tertulis.","PENGULANGAN · TANPA MEMBUKA CATATAN"),
    kode("1. Sesudah merge how=\"left\", satu baris pemeriksaan apa yang wajib kamu tulis?\n2. Kalau hasil merge LEBIH BANYAK dari tabel kiri, apa penyebabnya?\n3. Kenapa 233 baris hasil inner join itu menyesatkan?\n4. Kenapa pasien dikelompokkan pakai ID, bukan nama?", salin=False),
    "<details>\n          <summary>Cek jawabanmu</summary>\n          <div class=\"isi\">"
    "<p><strong>1.</strong> <code>len(hasil) == len(kiri)</code>.</p>"
    "<p><strong>2.</strong> Kunci di tabel kanan tidak unik — ada baris kembar yang menggandakan.</p>"
    "<p><strong>3.</strong> 240 − 18 hilang + 11 kembar = 233. Dua kesalahan saling menutupi.</p>"
    "<p><strong>4.</strong> Karena satu orang bisa punya beberapa ejaan nama — Siti punya tiga.</p>"
    "</div>\n        </details>")

HARI2=dict(tab="Kasus 2", judul="Klinik: dua berkas, dan tiga cara menggabungkannya dengan salah",
  waktu="± 120 menit",
  tujuan="menggabungkan dua tabel tanpa kehilangan baris dan tanpa menggandakannya — "
         "dan tahu satu baris pemeriksaan yang menangkap keduanya.",
  langkah=L, tutup_judul="Kasus 2 selesai",
  tutup="<p><strong>Yang kamu bawa:</strong> <code>merge</code> bawaannya membuang yang tidak cocok · "
        "hasil lebih banyak dari tabel kiri = kunci kanan tidak unik · "
        "<code>len(hasil)==len(kiri)</code> wajib · kelompokkan pakai ID, bukan nama.</p>"
        "<p style=\"margin-top:10px\">Besok: nama yang sama sekali tidak cocok, dan satu baris "
        "pemetaan yang menggeser margin 9 poin.</p>")
