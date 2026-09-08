# -*- coding: utf-8 -*-
"""Hari 1 — Kasus 1, ditulis ulang mengikuti _pola.md."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Buat berkasnya — satu perintah",
    blok("aksi", "Buka folder <code>data-dan-skrip/studi-kasus/</code> dari paket zip. "
                 "Buka Terminal di folder itu, lalu ketik satu baris ini dan tekan Enter.", "LAKUKAN"),
    kode("python gen_k1.py"),
    blok("hasil", kode("baris transaksi asli : 167\nbaris terakhir dipakai: 189", salin=False), "HARUS MUNCUL"),
    "<p><strong>Ingat angka 167.</strong> Sampai akhir hari ini kamu harus bisa membuktikan "
    "hasil bersihmu berisi tepat 167 baris — bukan 170, bukan 183.</p>")

langkah("Buka di Excel dulu, sebelum menyentuh Python",
    blok("aksi", "Klik dua kali berkas <code>Laporan Penjualan Toko Sumber Rejeki.xlsx</code> "
                 "yang baru muncul. Lihat saja. Jangan diapa-apakan.", "LAKUKAN"),
    blok("hasil", "Lima baris pertama bukan tabel — itu kop laporan. Judul kolom yang sebenarnya "
                  "ada di <strong>baris ke-6</strong>. Di tengah tabel ada baris "
                  "<code>TOTAL BULAN 01</code> dan seterusnya. Di paling bawah ada tulisan "
                  "<code>Dicetak oleh: Admin Kasir</code>.", "YANG HARUS TERLIHAT"),
    blok("catatan", "<strong>Ini kebiasaan, bukan basa-basi.</strong> Berkas klien selalu dibuka mata "
                    "dulu. Tiga hal yang barusan kamu lihat semuanya akan menjebak Python nanti — "
                    "dan kamu sudah tahu bentuknya sebelum ketemu."))

langkah("Baca dengan refleks pertama",
    blok("aksi", "Buka Colab baru. Unggah berkas Excel tadi lewat ikon folder di kiri. Lalu:", "LAKUKAN"),
    kode('import pandas as pd\ndf = pd.read_excel("Laporan Penjualan Toko Sumber Rejeki.xlsx")\nprint(df.shape)\nprint(df.columns.tolist()[:3])'),
    blok("hasil", kode("(188, 10)\n['Unnamed: 0', 'TOKO BANGUNAN SUMBER REJEKI', 'Unnamed: 2']", salin=False), "HARUS MUNCUL"),
    "<p><strong>Nama tokonya jadi nama kolom.</strong> pandas mengira baris pertama adalah judul kolom. "
    "Judul aslinya masih tersembunyi di baris ke-6.</p>")

langkah("Lompati lima baris kop",
    kode('raw = pd.read_excel("Laporan Penjualan Toko Sumber Rejeki.xlsx", skiprows=5)\nprint(raw.columns.tolist())'),
    blok("hasil", kode("['Unnamed: 0', 'No', 'Tanggal', 'No. Nota', 'Kode Barang',\n 'Nama Barang', 'Qty', 'Harga Satuan', 'Jumlah', 'Pelanggan']", salin=False), "HARUS MUNCUL"),
    "<p>Judul kolomnya benar sekarang. Masih ada satu kolom sampah bernama "
    "<code>Unnamed: 0</code> — itu kolom kosong di kiri tabel.</p>")

langkah("Buang kolom Unnamed",
    kode('raw = raw.drop(columns=[c for c in raw.columns if str(c).startswith("Unnamed")])\nprint(raw.shape)'),
    blok("hasil", kode("(183, 9)", salin=False), "HARUS MUNCUL"),
    "<p>183 baris. Tapi tadi generator bilang transaksinya cuma <strong>167</strong>. "
    "Enam belas baris sisanya bukan transaksi — nanti kita hitung satu per satu.</p>")

langkah("Sekarang lihat tipe tiap kolom — satu di antaranya sudah rusak",
    kode("print(raw.dtypes.to_string())"),
    blok("hasil", kode("No               object\nTanggal             str\nNo. Nota            str\nKode Barang         str\nNama Barang         str\nQty             float64\nHarga Satuan    float64\nJumlah              str\nPelanggan           str", salin=False), "HARUS MUNCUL"),
    blok("aksi", "Berhenti di sini. Satu kolom di daftar itu sudah rusak permanen — dan justru "
                 "kolom yang tipenya terlihat <em>paling benar</em>. Yang mana? Tebak dulu, baru lanjut.", "LAKUKAN"))

langkah("Buktinya",
    kode('print(raw["Harga Satuan"].head(3).to_string(index=False))'),
    blok("hasil", kode("185.0\n320.0\n 24.0", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Harga cat itu Rp 185.000, bukan 185.</strong> pandas membaca teks "
                   "<code>\"185.000\"</code> sebagai bilangan desimal <em>185 koma nol nol nol</em> — "
                   "karena di sebagian besar dunia, titik adalah pemisah desimal. "
                   "<strong>Tiga angka nol hilang, tanpa satu pun pesan error</strong>, dan hasilnya "
                   "<code>float64</code> yang terlihat sangat meyakinkan."))

langkah("Kenapa kolom Jumlah selamat — dan kenapa itu keberuntungan",
    kode('print(raw["Jumlah"].head(3).to_string(index=False))'),
    blok("hasil", kode("  370.000\n3.200.000\n   96.000", salin=False), "HARUS MUNCUL"),
    "<p>Kolom <code>Jumlah</code> tetap teks. Alasannya bukan karena kamu pintar. Hitung sendiri:</p>",
    kode('d = raw[raw["No"].fillna("").str.fullmatch(r"\\d+")]\nprint("bertitik dua :", d["Jumlah"].str.count(r"\\.").eq(2).sum())\nprint("bertitik satu:", d["Jumlah"].str.count(r"\\.").eq(1).sum())'),
    blok("hasil", kode("bertitik dua : 32\nbertitik satu: 135", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>32 transaksi kebetulan bernilai di atas satu juta</strong>, jadi angkanya "
                   "bertitik dua — dan <code>\"3.200.000\"</code> tidak bisa jadi desimal. Satu nilai "
                   "saja yang gagal membuat pandas menyerah dan menyimpan <em>seluruh</em> kolom sebagai teks. "
                   "Kalau toko ini tidak pernah menjual di atas Rp 999.999, kolom <code>Jumlah</code> "
                   "juga hancur diam-diam dan laporanmu meleset seribu kali lipat."))

langkah("Aturannya, dan mulai sekarang tidak ada pengecualian",
    blok("catatan", "<strong>Untuk berkas dari luar: baca semuanya sebagai teks dulu.</strong> "
                    "Kamu yang memutuskan mana yang jadi angka, bukan pandas. Tebakan pandas benar 95% "
                    "dan salahnya tidak bersuara — dan 5% itu yang masuk laporan klien."),
    kode('raw = pd.read_excel("Laporan Penjualan Toko Sumber Rejeki.xlsx",\n                    skiprows=5, dtype=str)\nraw = raw.drop(columns=[c for c in raw.columns if str(c).startswith("Unnamed")])\nprint(raw["Harga Satuan"].head(3).to_string(index=False))'),
    blok("hasil", kode("185.000\n320.000\n 24.000", salin=False), "HARUS MUNCUL"),
    "<p>Tiga angka nolnya kembali.</p>")

langkah("Ambil angka kontrolnya — sebelum barisnya dibuang",
    "<p>Baris <code>TOTAL BULAN</code> itu bukan sampah. Itu angka kontrol yang diberikan "
    "klien tanpa sadar. Ambil dulu, baru buang.</p>",
    kode('import re\ndef ke_angka(s):\n    t = re.sub(r"[^0-9\\-]", "", str(s))\n    return int(t) if t not in ("", "-") else 0'),
    kode('sub = raw[raw["Nama Barang"].astype(str).str.startswith("TOTAL BULAN", na=False)]\nKONTROL = sub["Jumlah"].map(ke_angka).sum()\nprint(len(sub), "baris subtotal")\nprint(f"KONTROL = {KONTROL:,}")'),
    blok("hasil", kode("6 baris subtotal\nKONTROL = 140,581,000", salin=False), "HARUS MUNCUL"))

langkah("Saring baris transaksi — dan kenapa dropna() salah",
    kode('d = raw[raw["No"].fillna("").str.fullmatch(r"\\d+")].copy()\nsalah = raw.dropna(subset=["No"])\nprint("fullmatch:", len(d))\nprint("dropna   :", len(salah))'),
    blok("hasil", kode("fullmatch: 167\ndropna   : 170", salin=False), "HARUS MUNCUL"),
    "<p>Selisih tiga. Lihat siapa yang lolos:</p>",
    kode('print(salah[~salah.index.isin(d.index)]["Nama Barang"].tolist())'),
    blok("hasil", kode("['Dicetak oleh: Admin Kasir',\n 'Tanggal cetak: 05/07/2024',\n 'Aplikasi Kasir Pro v2.1 - Lisensi: TOKO SUMBER REJEKI']", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<code>dropna()</code> cuma membuang baris <em>kosong</em>. Tiga baris footer itu "
                   "kolom <code>No</code>-nya <strong>terisi teks</strong>, jadi lolos — dan masuk "
                   "laporanmu sebagai tiga transaksi hantu bertanggal kosong."))

langkah("Ubah jadi angka, lalu buktikan bersihnya",
    kode('d["Jumlah"] = d["Jumlah"].map(ke_angka)\ntotal = d["Jumlah"].sum()\nprint(f"baris   : {len(d)}")\nprint(f"total   : {total:,}")\nprint(f"selisih : {KONTROL - total:,}")'),
    blok("hasil", kode("baris   : 167\ntotal   : 140,581,000\nselisih : 0", salin=False), "HARUS MUNCUL"),
    blok("catatan", "<strong>Selisih nol itu bukan hiasan.</strong> Tanpa baris terakhir itu kamu cuma "
                    "<em>berharap</em> pembersihanmu benar. Dengan baris itu kamu <em>tahu</em>. "
                    "Ini prosedur yang sama persis dengan menyandingkan buku besar ke neraca saldo."))

langkah("Jebakan terakhir: lupa membuang baris subtotal",
    kode('semua = raw["Jumlah"].map(ke_angka).sum()\nprint(f"lupa buang subtotal : {semua:,}")\nprint(f"yang benar          : {total:,}")\nprint(f"kelebihan           : {semua - total:,}")'),
    blok("hasil", kode("lupa buang subtotal : 281,162,000\nyang benar          : 140,581,000\nkelebihan           : 140,581,000", salin=False), "HARUS MUNCUL"),
    blok("bahaya", "<strong>Tepat dua kali lipat.</strong> Bukan kebetulan — enam baris subtotal "
                   "menjumlahkan seluruh transaksi sekali lagi. Angka Rp 281 juta itu tidak terlihat aneh "
                   "bagi siapa pun yang tidak tahu omzet toko ini, dan tidak ada satu pun error yang muncul."))

langkah("Rapikan nama pelanggan — satu jebakan kecil yang klien langsung lihat",
    kode('n = d["Pelanggan"].str.strip().str.replace(r"\\s+", " ", regex=True).str.title()\nprint([x for x in n.unique() if x[:2] in ("Cv", "Pt", "Ud")][:2])'),
    blok("hasil", kode("['Cv Karya Abadi', 'Pt Mitra Bangun']", salin=False), "HARUS MUNCUL"),
    "<p><code>.str.title()</code> merusak singkatan badan usaha. Kembalikan:</p>",
    kode('n = n.str.replace(r"^(Cv|Pt|Ud)\\s+", lambda m: m.group(1).upper()+" ", regex=True)\nprint([x for x in n.unique() if x[:2] in ("CV", "PT", "UD")][:2])'),
    blok("hasil", kode("['CV Karya Abadi', 'PT Mitra Bangun']", salin=False), "HARUS MUNCUL"),
    blok("catatan", "Klien akan langsung melihat ini di laporanmu, dan yang mereka simpulkan bukan "
                    "\"ada bug kecil\" tapi \"orang ini tidak memeriksa hasil kerjanya\"."))

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Tanpa melihat, jawab empat hal — tulis, jangan cuma dipikir.", "PENGULANGAN · TANPA MEMBUKA CATATAN"),
    kode("1. Kenapa berkas dari luar dibaca dengan dtype=str?\n2. Kenapa dropna() tidak cukup untuk menyaring baris transaksi?\n3. Dari mana angka kontrol 140.581.000 datang?\n4. Kalau lupa membuang baris subtotal, hasilnya jadi berapa kali lipat?", salin=False),
    "<details>\n          <summary>Cek jawabanmu</summary>\n          <div class=\"isi\">"
    "<p><strong>1.</strong> Karena tebakan pandas salah tanpa bersuara — <code>\"185.000\"</code> jadi 185,0 "
    "dan tiga angka nol hilang.</p>"
    "<p><strong>2.</strong> Karena baris footer kolom <code>No</code>-nya terisi teks, bukan kosong. "
    "170 baris, bukan 167.</p>"
    "<p><strong>3.</strong> Dari enam baris <code>TOTAL BULAN</code> di dalam berkas klien sendiri, "
    "dijumlahkan sebelum dibuang.</p>"
    "<p><strong>4.</strong> Tepat dua kali lipat — Rp 281.162.000.</p>"
    "</div>\n        </details>")

HARI1 = dict(tab="Kasus 1", judul="Toko bangunan: kolom yang paling terlihat bersih justru yang sudah rusak",
    waktu="± 120 menit",
    tujuan="membaca ekspor aplikasi kasir yang headernya bukan di baris satu, menemukan satu kolom "
           "yang diam-diam kehilangan tiga angka nol, dan membuktikan hasil bersihmu dengan angka kontrol "
           "yang diberikan klien tanpa sadar.",
    langkah=L,
    tutup_judul="Kasus 1 selesai",
    tutup="<p><strong>Yang kamu bawa:</strong> <code>dtype=str</code> untuk berkas dari luar · "
          "saring dengan <code>str.fullmatch(r\"\\d+\")</code>, bukan <code>dropna()</code> · "
          "ambil angka kontrol sebelum barisnya dibuang · dan tutup dengan selisih nol.</p>"
          "<p style=\"margin-top:10px\">Besok: dua berkas, dan tiga cara menggabungkannya dengan salah.</p>")
