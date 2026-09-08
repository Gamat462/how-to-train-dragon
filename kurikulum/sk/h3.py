# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L=[]
def langkah(judul,*isi): L.append({"judul":judul,"isi":"\n".join(isi)})

langkah("Buat berkasnya",
    kode("python gen_k3.py"),
    blok("hasil","Berkas <code>RAB vs Realisasi CV Karya Mandiri.xlsx</code> muncul, "
        "berisi dua sheet: <code>RAB</code> dan <code>Realisasi</code>.","HARUS MUNCUL"))

langkah("Lihat kedua sheet-nya",
    kode('import pandas as pd\nB = "RAB vs Realisasi CV Karya Mandiri.xlsx"\nrab  = pd.read_excel(B, sheet_name="RAB", skiprows=2)\nreal = pd.read_excel(B, sheet_name="Realisasi")\nprint(rab.shape, real.shape)'),
    blok("hasil", kode("(7, 4) (86, 5)", salin=False),"HARUS MUNCUL"),
    "<p>Tujuh proyek, 86 baris biaya. <code>skiprows=2</code> lagi — sheet RAB juga berkop.</p>")

langkah("Kolom Biaya: separuhnya bukan angka",
    kode('print(real["Biaya"].astype(str).head(6).tolist())'),
    blok("hasil", kode("['26520000', '87820000', '29080000', '35210000',\n 'Rp 91.190.000', 'Rp 43.280.000']", salin=False),"HARUS MUNCUL"),
    kode('print("sel bukan angka:", pd.to_numeric(real["Biaya"], errors="coerce").isna().sum())'),
    blok("hasil", kode("sel bukan angka: 44", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>44 dari 86 baris.</strong> Ada yang mengetik <code>Rp</code> dan titik, "
        "ada yang tidak. Kalau kamu <code>sum()</code> langsung, separuh biayanya hilang — "
        "dan laba proyekmu jadi terlihat dua kali lipat lebih baik."))

langkah("Satu fungsi kecil, dipakai di semua kasus",
    kode('import re\ndef ke_angka(s):\n    t = re.sub(r"[^0-9\\-]", "", str(s))\n    return int(t) if t not in ("", "-") else 0'),
    kode('real["biaya"] = real["Biaya"].map(ke_angka)\nprint(f\'{real["biaya"].sum():,}\')'),
    blok("hasil", kode("3,282,000,000", salin=False),"HARUS MUNCUL"),
    blok("catatan","Fungsi ini sudah kamu tulis di Kasus 1. <strong>Jangan salin-tempel lagi</strong> — "
        "taruh di berkas sendiri dan panggil. Cara melakukannya ada di modul Python Produksi."))

langkah("Sekarang coba gabungkan kedua sheet",
    kode('m = rab.merge(real, left_on="Nama Proyek", right_on="Proyek")\nprint("baris hasil:", len(m))'),
    blok("hasil", kode("baris hasil: 0", salin=False),"HARUS MUNCUL"),
    "<p><strong>Nol.</strong> Bukan sedikit — <em>tidak ada satu pun</em> yang cocok.</p>")

langkah("Lihat kenapa",
    kode('print(sorted(rab["Nama Proyek"])[:3])\nprint(sorted(real["Proyek"].unique())[:3])'),
    blok("hasil", kode("['Gudang Logistik Cibitung', 'Kios Pasar Modern Bekasi',\n 'Masjid Al-Ikhlas Tahap 2']\n['GUDANG CIBITUNG', 'KIOS PASAR BEKASI',\n 'MASJID AL IKHLAS TAHAP II']", salin=False),"HARUS MUNCUL"),
    "<p>Proyek yang sama, ditulis dua orang berbeda, di dua waktu berbeda. "
    "Tidak ada aturan yang bisa menghubungkannya secara otomatis.</p>")

langkah("Tabel pemetaan dibuat manusia — dan itu memang seharusnya",
    kode('PETA = {\n "GUDANG CIBITUNG":               "Gudang Logistik Cibitung",\n "KIOS PASAR BEKASI":             "Kios Pasar Modern Bekasi",\n "MASJID AL IKHLAS TAHAP II":     "Masjid Al-Ikhlas Tahap 2",\n "PAGAR TAMAN GRIYA":             "Pagar & Taman Perumahan Griya",\n "RUKO DEPOK - 2024":             "Pembangunan Ruko Depok 2 Lantai",\n "PEK. TAMBAH KURANG RUKO DEPOK": "Pembangunan Ruko Depok 2 Lantai",\n "Rmh Bpk Handoko":               "Rumah Tinggal Bpk. Handoko",\n "renovasi kantor sinarmas":      "Renovasi Kantor PT Sinar Mas",\n}'),
    blok("catatan","<strong>Jangan mencoba mencocokkan nama secara otomatis</strong> dengan kemiripan "
        "huruf. Ia akan benar untuk enam baris dan salah untuk dua — dan yang dua itu tidak akan "
        "memberi tahu kamu."))

langkah("Pasang penjaga supaya tidak ada yang lolos diam-diam",
    kode('belum = set(real["Proyek"].unique()) - set(PETA)\nassert not belum, f"belum dipetakan: {belum}"\nreal["proyek_baku"] = real["Proyek"].map(PETA)\nprint("semua terpetakan")'),
    blok("hasil", kode("semua terpetakan", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>Tanpa baris <code>assert</code> itu</strong>, nama baru yang muncul bulan depan "
        "akan jadi <code>NaN</code>, biayanya lenyap dari rekap, dan laporanmu tetap terbit "
        "dengan angka yang salah tanpa satu pun peringatan."))

langkah("Satu baris pemetaan yang menggeser margin 9 poin",
    "<p>Baris <code>PEK. TAMBAH KURANG RUKO DEPOK</code> — pekerjaan tambah. Masuk ke proyek "
    "induk, atau dihitung terpisah? Coba keduanya:</p>",
    blok("hasil", tabel(["Keputusan","Realisasi Ruko","Laba","Margin"],
        [["Pekerjaan tambah <strong>ikut</strong>","688.590.000","161.410.000","<strong>19,0%</strong>"],
         ["Pekerjaan tambah <strong>tidak ikut</strong>","609.740.000","240.260.000","<strong>28,3%</strong>"]],
        kelas_n=(1,2,3)),"HARUS MUNCUL"),
    blok("bahaya","<strong>9,3 poin margin, dari satu baris di tabel pemetaan.</strong> Tidak ada kode "
        "yang bisa memutuskan ini untukmu. Yang benar adalah bertanya ke pemilik: "
        "\"pekerjaan tambah ini ditagihkan terpisah ke pelanggan, atau sudah masuk nilai kontrak?\" "
        "Jawabannya menentukan angkanya — dan <strong>keputusan itu wajib ditulis di laporan.</strong>"))

langkah("Rekapnya",
    kode('rekap = (real.groupby("proyek_baku")["biaya"].sum().rename("realisasi")\n         .reset_index()\n         .merge(rab, left_on="proyek_baku", right_on="Nama Proyek"))\nrekap["laba"] = rekap["Nilai Kontrak"] - rekap["realisasi"]'),
    kode('print(rekap[["proyek_baku","Total RAB","realisasi","laba"]]\n      .sort_values("laba").to_string(index=False))'),
    blok("hasil", kode("       Masjid Al-Ikhlas Tahap 2  352000000  408020000    1980000\n       Gudang Logistik Cibitung  985000000 1154370000   85630000\n   Renovasi Kantor PT Sinar Mas  268000000  262860000   57140000\nPembangunan Ruko Depok 2 Lantai  690000000  688590000  161410000\n  Pagar & Taman Perumahan Griya  149000000  147800000   37200000\n     Rumah Tinggal Bpk. Handoko  448000000  421770000  118230000\n       Kios Pasar Modern Bekasi  221000000  198590000   76410000", salin=False),"HARUS MUNCUL"))

langkah("Dua proyek yang RAB-nya jebol",
    kode('jebol = rekap[rekap["realisasi"] > rekap["Total RAB"]]\nprint(jebol[["proyek_baku","Total RAB","realisasi"]].to_string(index=False))'),
    blok("hasil", kode("Gudang Logistik Cibitung  985000000 1154370000\nMasjid Al-Ikhlas Tahap 2  352000000  408020000", salin=False),"HARUS MUNCUL"),
    "<p>Gudang Cibitung menghabiskan Rp 169 juta di atas RAB. Masjid Al-Ikhlas Rp 56 juta, "
    "dan labanya tinggal Rp 1,98 juta dari kontrak Rp 410 juta — <strong>margin 0,5%</strong>.</p>")

langkah("Tutup dengan tie-out",
    kode('print(f\'rekap  : {rekap["realisasi"].sum():,}\')\nprint(f\'sumber : {real["biaya"].sum():,}\')\nprint(f\'selisih: {real["biaya"].sum() - rekap["realisasi"].sum():,}\')'),
    blok("hasil", kode("rekap  : 3,282,000,000\nsumber : 3,282,000,000\nselisih: 0", salin=False),"HARUS MUNCUL"))

langkah("Ulangi dari ingatan",
    blok("aksi","Tutup halaman. Tiga pertanyaan, tertulis.","PENGULANGAN · TANPA MEMBUKA CATATAN"),
    kode("1. Kenapa merge langsung memberi 0 baris, dan kenapa itu justru kabar baik?\n2. Apa gunanya baris assert sesudah membuat tabel pemetaan?\n3. Satu baris pemetaan menggeser margin berapa poin, dan siapa yang berhak memutuskannya?", salin=False),
    "<details>\n          <summary>Cek jawabanmu</summary>\n          <div class=\"isi\">"
    "<p><strong>1.</strong> Karena tidak ada nama yang sama persis. Kabar baik, karena 0 baris "
    "<em>terlihat</em> — kalau yang cocok cuma 3 dari 7, kamu mungkin tidak sadar.</p>"
    "<p><strong>2.</strong> Menangkap nama baru yang belum dipetakan, sebelum biayanya diam-diam "
    "lenyap jadi <code>NaN</code>.</p>"
    "<p><strong>3.</strong> 9,3 poin (19,0% lawan 28,3%). Yang berhak memutuskan pemilik proyek, "
    "bukan analisnya — dan keputusannya ditulis di laporan.</p>"
    "</div>\n        </details>")

HARI3=dict(tab="Kasus 3", judul="Kontraktor: tabel pemetaan adalah keputusan bisnis, bukan pekerjaan teknis",
  waktu="± 120 menit",
  tujuan="menggabungkan dua tabel yang tidak punya satu pun kunci yang sama, dan menyadari "
         "bahwa satu baris di tabel pemetaan bisa menggeser margin 9 poin.",
  langkah=L, tutup_judul="Kasus 3 selesai",
  tutup="<p><strong>Yang kamu bawa:</strong> nama proyek bukan kunci · tabel pemetaan dibuat manusia, "
        "bukan ditebak mesin · <code>assert</code> menangkap nama baru sebelum biayanya lenyap · "
        "keputusan pemetaan wajib ditulis di laporan.</p>"
        "<p style=\"margin-top:10px\">Besok: Rp 45 juta yang hilang karena orang mengetik "
        "\"LUNAS\" di kolom angka.</p>")
