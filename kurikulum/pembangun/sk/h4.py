# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L=[]
def langkah(judul,*isi): L.append({"judul":judul,"isi":"\n".join(isi)})

langkah("Buat berkasnya",
    kode("python gen_k4.py"),
    blok("hasil", kode("siswa pindah      : 5\nsel bertuliskan LUNAS : 95\nversi TU (=SUM Excel) : 305.897.000\nselisih yang disembunyikan LUNAS: 45.350.000", salin=False),"HARUS MUNCUL"),
    "<p>Angka <strong>Rp 305.897.000</strong> itu yang dilaporkan bagian TU ke yayasan. "
    "Hari ini kamu cari tahu kenapa angka itu salah.</p>")

langkah("Bentuknya melebar, bukan memanjang",
    kode('import pandas as pd\nB = "Rekap SPP Yayasan Bina Cendekia.xlsx"\nd = pd.read_excel(B, skiprows=2, dtype=str).dropna(how="all")\nprint(d.columns.tolist())'),
    blok("hasil", kode("['NIS', 'Nama Siswa', 'Kelas', 'SPP/Bulan', 'Jul', 'Agu', 'Sep',\n 'Okt', 'Nov', 'Des', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',\n 'Keterangan']", salin=False),"HARUS MUNCUL"),
    blok("catatan","<strong>Dua belas bulan jadi dua belas kolom.</strong> Manusia membaca bentuk ini "
        "dengan mudah; pandas tidak. Nanti kita ubah — tapi jangan dulu."))

langkah("Jebakan yang sama seperti Kasus 1",
    kode('print(d[["NIS","Nama Siswa"]].tail(2).to_string(index=False))'),
    blok("hasil", kode("2023072            Lukman Saputra\n    NaN TOTAL DITERIMA (versi TU)", salin=False),"HARUS MUNCUL"),
    kode('s = d[d["NIS"].fillna("").str.fullmatch(r"[\\d.]+")].copy()\nprint("baris siswa:", len(s))'),
    blok("hasil", kode("baris siswa: 72", salin=False),"HARUS MUNCUL"),
    blok("bahaya","Baris <code>TOTAL DITERIMA</code> lagi-lagi menggandakan seluruh angka kalau ikut "
        "dijumlahkan — <strong>persis jebakan Kasus 1.</strong> Ini bukan kebetulan: hampir setiap "
        "rekap buatan tangan punya baris total di dalam tabelnya sendiri."))

langkah("Lihat isi sel bulan — bukan cuma angka",
    kode('import re\nBULAN = ["Jul","Agu","Sep","Okt","Nov","Des","Jan","Feb","Mar","Apr","Mei","Jun"]\nteks = set()\nfor b in BULAN:\n    for v in s[b].dropna().unique():\n        if not re.fullmatch(r"[\\d.]+", str(v)): teks.add(str(v))\nprint(sorted(teks))'),
    blok("hasil", kode("['-', 'BELUM', 'LUNAS', 'blm', 'nunggak', 'x']", salin=False),"HARUS MUNCUL"),
    "<p>Enam tulisan. Satu di antaranya berarti <strong>sudah bayar</strong>. Lima sisanya berarti "
    "<strong>belum</strong>. Kalau kamu memperlakukan semuanya sama, kamu salah di kedua arah.</p>")

langkah("Hitung masing-masing",
    kode('for kata in ["LUNAS","-","BELUM","blm","nunggak","x"]:\n    n = sum((s[b] == kata).sum() for b in BULAN)\n    print(f"{kata:9s}: {n}")'),
    blok("hasil", kode("LUNAS    : 95\n-        : 25\nBELUM    : 9\nblm      : 8\nnunggak  : 7\nx        : 5", salin=False),"HARUS MUNCUL"),
    blok("catatan","<strong>Lima cara mengetik \"belum bayar\".</strong> Itu tanda kolomnya diisi "
        "beberapa orang berbeda selama setahun, tanpa aturan. Bukan kesalahan mereka — "
        "tidak ada yang pernah memberi tahu formatnya."))

langkah("Kenapa versi TU salah",
    kode('def ke_angka(x):\n    t = re.sub(r"[^0-9]", "", str(x)) if pd.notna(x) else ""\n    return int(t) if t else 0'),
    kode('tu = sum(s[b].map(ke_angka).sum() for b in BULAN)\nprint(f"versi TU: {tu:,}")'),
    blok("hasil", kode("versi TU: 305,897,000", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>Excel <code>SUM()</code> memperlakukan teks sebagai nol.</strong> "
        "Sembilan puluh lima sel bertuliskan LUNAS — pembayaran yang benar-benar diterima — "
        "dihitung sebagai <strong>nol rupiah</strong>. Tidak ada error, tidak ada peringatan. "
        "Angkanya masuk ke laporan yayasan begitu saja."))

langkah("Berapa yang disembunyikan kata LUNAS",
    kode('s["spp"] = s["SPP/Bulan"].map(ke_angka)\nlunas = sum(s.loc[s[b] == "LUNAS", "spp"].sum() for b in BULAN)\nprint(f"nilai di balik LUNAS: {lunas:,}")\nprint(f"diterima sesungguhnya: {tu + lunas:,}")'),
    blok("hasil", kode("nilai di balik LUNAS: 45,350,000\nditerima sesungguhnya: 351,247,000", salin=False),"HARUS MUNCUL"),
    "<p><strong>Rp 45.350.000</strong> uang yang sudah masuk kas, dilaporkan sebagai belum masuk. "
    "Yayasan mengira tunggakannya Rp 45 juta lebih besar daripada kenyataan.</p>")

langkah("Ubah bentuknya: melebar jadi memanjang",
    kode('p = s.melt(id_vars=["NIS","Nama Siswa","Kelas","spp"],\n           value_vars=BULAN, var_name="bulan", value_name="isi")\nprint(p.shape)'),
    blok("hasil", kode("(864, 6)", salin=False),"HARUS MUNCUL"),
    "<p>72 siswa × 12 bulan = 864 baris. Satu baris = satu siswa, satu bulan. "
    "Bentuk ini yang bisa dikelompokkan, disaring, dan dijumlahkan.</p>",
    blok("catatan","<code>melt</code> adalah satu-satunya perkakas yang kamu butuhkan untuk mengubah "
        "rekap buatan tangan jadi data yang bisa diolah. Hampir semua berkas Excel dari klien "
        "berbentuk melebar."))

langkah("Terjemahkan isi selnya jadi angka yang benar",
    kode('def bayar(baris):\n    v = str(baris["isi"]).strip()\n    if v == "LUNAS": return baris["spp"]\n    return ke_angka(v)'),
    kode('p["dibayar"] = p.apply(bayar, axis=1)\nprint(f\'{p["dibayar"].sum():,}\')'),
    blok("hasil", kode("351,247,000", salin=False),"HARUS MUNCUL"),
    "<p>Cocok dengan hitungan tadi. Dua jalan berbeda, satu jawaban — itu pemeriksaannya.</p>")

langkah("Tunggakan per kelas",
    blok("hasil", tabel(["Kelas","Siswa","Tagihan","Diterima","Tunggakan","%"],
        [["7A","12","60.300.000","52.560.000","7.740.000","12,8"],
         ["7B","12","59.850.000","52.380.000","7.470.000","12,5"],
         ["8A","12","68.400.000","56.908.000","<strong>11.492.000</strong>","<strong>16,8</strong>"],
         ["8B","12","66.500.000","61.799.000","4.701.000","7,1"],
         ["9A","12","72.000.000","64.000.000","8.000.000","11,1"],
         ["9B","12","72.000.000","63.600.000","8.400.000","11,7"]],
        kelas_n=(1,2,3,4,5)),"HARUS MUNCUL"),
    kode('print(f"tagihan  : 399,050,000")\nprint(f"diterima : 351,247,000")\nprint(f"tunggakan:  47,803,000")'),
    "<p>Rp 399.050.000 − Rp 351.247.000 = Rp 47.803.000, yaitu <strong>12,0%</strong>. "
    "Kelas 8A paling berat: 16,8%.</p>")

langkah("Yang tidak diminta, tapi wajib disebut: lima siswa pindah",
    kode('pindah = s[s["Keterangan"].notna()]\nprint(len(pindah), "siswa")\nprint(pindah[["Nama Siswa","Kelas","Keterangan"]].head(3).to_string(index=False))'),
    blok("hasil", kode("5 siswa\nBella Ramadhan    7B  pindah Jan\nNaufal Nugroho    7B  pindah Feb\n  Mira Maulana    7A  pindah Nov", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>Menagih 12 bulan ke siswa yang pindah di bulan ke-4 adalah salah.</strong> "
        "Tunggakan mereka Rp 1.575.000 dari total Rp 47,8 juta — kecil, tapi kalau surat tagihan "
        "terkirim ke orang tua yang anaknya sudah pindah setengah tahun lalu, "
        "yang rusak bukan angkanya, tapi nama sekolahnya."))

langkah("Ulangi dari ingatan",
    blok("aksi","Tutup halaman. Empat pertanyaan, tertulis.","PENGULANGAN · TANPA MEMBUKA CATATAN"),
    kode("1. Kenapa SUM() di Excel memberi angka yang terlalu kecil di berkas ini?\n2. Berapa rupiah yang disembunyikan kata LUNAS, dan kenapa tidak ada error?\n3. Apa gunanya melt(), dan berapa baris hasilnya?\n4. Kenapa siswa pindah harus dipisahkan sebelum menagih?", salin=False),
    "<details>\n          <summary>Cek jawabanmu</summary>\n          <div class=\"isi\">"
    "<p><strong>1.</strong> Karena sel berisi teks dihitung sebagai nol — 95 sel LUNAS.</p>"
    "<p><strong>2.</strong> Rp 45.350.000. Tidak ada error karena mengabaikan teks memang perilaku "
    "normal <code>SUM()</code>, bukan kerusakan.</p>"
    "<p><strong>3.</strong> Mengubah 12 kolom bulan jadi baris. 72 × 12 = 864 baris.</p>"
    "<p><strong>4.</strong> Karena bulan wajib mereka kurang dari 12 — menagih penuh berarti "
    "menagih bulan yang anaknya sudah tidak sekolah di situ.</p>"
    "</div>\n        </details>")

HARI4=dict(tab="Kasus 4", judul="Sekolah: Rp 45 juta yang hilang karena orang mengetik “LUNAS”",
  waktu="± 120 menit",
  tujuan="mengubah rekap Excel berbentuk melebar jadi data yang bisa diolah, dan menemukan "
         "uang yang sudah masuk kas tapi dilaporkan sebagai belum masuk.",
  langkah=L, tutup_judul="Kasus 4 selesai",
  tutup="<p><strong>Yang kamu bawa:</strong> <code>SUM()</code> Excel menganggap teks = nol · "
        "satu kolom bisa punya enam cara penulisan · <code>melt</code> mengubah melebar jadi memanjang · "
        "hitung lewat dua jalan dan cocokkan · dan baris TOTAL di dalam tabel selalu menggandakan.</p>"
        "<p style=\"margin-top:10px\">Besok, kasus terakhir: Rp 424 juta uang masuk yang "
        "<em>bukan</em> pelunasan piutang.</p>")
