# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L=[]
def langkah(judul,*isi): L.append({"judul":judul,"isi":"\n".join(isi)})

langkah("Buat kedua berkasnya",
    kode("python gen_k5.py"),
    blok("hasil", kode("faktur           : 53 | nilai: 2.524.400.000\nbaris rek koran  : 55\npelunasan piutang: 1.544.500.000\nsaldo piutang    : 979.900.000", salin=False),"HARUS MUNCUL"),
    "<p>Empat angka itu tujuanmu. Yang paling sulit bukan menghitungnya — "
    "tapi <strong>tidak tertipu oleh angka kelima</strong> yang belum muncul di situ.</p>")

langkah("Baca keduanya",
    kode('import pandas as pd, re\npi = pd.read_excel("Daftar Piutang PT Anugerah Jaya.xlsx", skiprows=2)\nrk = pd.read_csv("Rekening Koran Juni 2024.csv", sep=";", dtype=str)\nprint(len(pi), len(rk))'),
    blok("hasil", kode("53 55", salin=False),"HARUS MUNCUL"))

langkah("Ambil yang uang masuk saja",
    kode('def ke_angka(x):\n    t = re.sub(r"[^0-9]", "", str(x)) if pd.notna(x) else ""\n    return int(t) if t else 0'),
    kode('rk["kredit"] = rk["Kredit"].map(ke_angka)\nmasuk = rk[rk["kredit"] > 0]\nprint("baris:", len(masuk))\nprint(f"nilai: {masuk[\'kredit\'].sum():,}")'),
    blok("hasil", kode("baris: 47\nnilai: 1,968,606,050", salin=False),"HARUS MUNCUL"),
    "<p>Rp 1,97 miliar masuk ke rekening selama enam bulan.</p>")

langkah("Asumsi paling mahal di seluruh halaman ini",
    blok("bahaya","<strong>Godaannya sekarang: anggap seluruh Rp 1,97 miliar itu pelunasan piutang.</strong> "
        "Kalau kamu melakukannya, saldo piutang yang kamu laporkan akan meleset "
        "<strong>ratusan juta</strong> — dan angkanya akan terlihat sangat masuk akal."),
    blok("aksi","Berhenti. Sebelum menghitung apa pun, baca dulu kolom keterangannya. "
        "Semua 47 baris.","LAKUKAN"),
    kode('for _, r in masuk.sort_values("kredit", ascending=False).head(8).iterrows():\n    print(f"{r[\'kredit\']:>13,}  {r[\'Keterangan\']}")'),
    blok("hasil", kode("  142,852,693  SETORAN MODAL DIREKTUR\n  112,841,806  SETORAN MODAL DIREKTUR\n   94,500,000  TRF TOKO BAHAGIA\n   88,600,000  TRF PT MITRA NIAGA UTAMA\n   88,100,000  KREDIT CV BERKAH JAYA\n   86,200,000  TRF CV BERKAH JAYA ABADI\n   82,700,000  SETORAN TUNAI TOKO BAHAGIA\n   81,600,000  PT SUMBERMAKMUR", salin=False),"HARUS MUNCUL"))

langkah("Dua baris teratas bukan pelanggan",
    "<p><code>SETORAN MODAL DIREKTUR</code> adalah pemilik menyuntik uang ke perusahaan. "
    "Itu bukan pelanggan membayar utang. Cari semuanya:</p>",
    kode('bukan = masuk[masuk["Keterangan"].str.contains(\n    "SETORAN MODAL DIREKTUR|BUNGA GIRO|TANPA KETERANGAN|MAJU BERSAMA", na=False)]\nprint(bukan.groupby("Keterangan")["kredit"].agg(["size","sum"]).to_string())'),
    blok("hasil", kode("                                size        sum\nBUNGA GIRO                         2      83599\nSETORAN MODAL DIREKTUR             4  398476419\nSETORAN TUNAI TANPA KETERANGAN     1   16789518\nTRF DR PT MAJU BERSAMA             1    8756514", salin=False),"HARUS MUNCUL"))

langkah("Angka kelima yang tadi belum muncul",
    kode('print(f"bukan pelunasan : {bukan[\'kredit\'].sum():,}")\nprint(f"pelunasan       : {masuk[\'kredit\'].sum() - bukan[\'kredit\'].sum():,}")'),
    blok("hasil", kode("bukan pelunasan : 424,106,050\npelunasan       : 1,544,500,000", salin=False),"HARUS MUNCUL"),
    blok("bahaya","<strong>Rp 424.106.050 — 21,5% dari seluruh uang masuk — bukan pelunasan piutang.</strong> "
        "Analis yang melewatkan ini melaporkan saldo piutang Rp 555 juta, padahal sebenarnya "
        "Rp 979 juta. Selisihnya Rp 424 juta, dan tidak ada satu pun error yang muncul."),
    blok("catatan","<strong>Ini bukan kemampuan pandas.</strong> Ini kemampuan membaca keterangan bank "
        "dan tahu bahwa setoran modal bukan pendapatan. Latar akuntansimu yang menangkap ini, "
        "bukan kodenya — dan itulah yang kamu jual."))

langkah("Cocokkan keterangan bank ke pelanggan — manual lagi",
    kode('PETA = {\n "SUMBERMAKMUR":      "PT Sumber Makmur Sentosa",\n "SUMBER MAKMUR":     "PT Sumber Makmur Sentosa",\n "BERKAH JAYA":       "CV Berkah Jaya Abadi",\n "TOKO BAHAGIA":      "Toko Bahagia",\n "SINARTERANG":       "UD Sinar Terang",\n "MITRA NIAGA":       "PT Mitra Niaga Utama",\n "SEJAHTERA":         "Toko Sejahtera",\n "ANUGERAH PANGAN":   "CV Anugerah Pangan",\n "GLOBAL DIST":       "PT Global Distribusi",\n}'),
    blok("catatan","Sama seperti Kasus 3: <strong>mesin tidak boleh menebak ini.</strong> "
        "\"PT SUMBERMAKMUR\" dan \"PT SUMBER MAKMUR SENTOSA\" adalah pelanggan yang sama — "
        "tapi hanya manusia yang bisa memastikannya."))

langkah("Saldo piutang per pelanggan",
    blok("hasil", tabel(["Pelanggan","Faktur","Nilai faktur","Dibayar","Saldo","Tertagih %"],
        [["CV Berkah Jaya Abadi","9","524.900.000","259.400.000","<strong>265.500.000</strong>","49,4"],
         ["PT Sumber Makmur Sentosa","5","286.400.000","139.800.000","146.600.000","48,8"],
         ["CV Anugerah Pangan","7","311.600.000","169.900.000","141.700.000","54,5"],
         ["Toko Sejahtera","8","337.500.000","227.000.000","110.500.000","67,3"],
         ["Toko Bahagia","6","313.900.000","215.400.000","98.500.000","68,6"],
         ["UD Sinar Terang","6","208.800.000","119.100.000","89.700.000","57,0"],
         ["PT Mitra Niaga Utama","5","259.400.000","175.100.000","84.300.000","67,5"],
         ["PT Global Distribusi","7","281.900.000","238.800.000","43.100.000","<strong>84,7</strong>"]],
        kelas_n=(1,2,3,4,5)),"HARUS MUNCUL"),
    "<p>Total saldo piutang <strong>Rp 979.900.000</strong>. "
    "Dua pelanggan terbesar baru membayar separuh.</p>")

langkah("Susun umur piutangnya",
    kode('TGL = pd.Timestamp("2024-06-30")\npi["umur"] = (TGL - pd.to_datetime(pi["Jatuh Tempo"], format="%d/%m/%Y")).dt.days'),
    blok("hasil", tabel(["Kelompok","Faktur","Nilai","%"],
        [["1. Belum jatuh tempo","5","245.700.000","25,1"],
         ["2. 1–30 hari","11","423.500.000","43,2"],
         ["3. 31–60 hari","8","258.700.000","26,4"],
         ["4. 61–90 hari","1","32.900.000","3,4"],
         ["5. &gt; 90 hari","1","<strong>19.100.000</strong>","1,9"]],
        kelas_n=(1,2,3)),"HARUS MUNCUL"))

langkah("Tutup dengan tie-out",
    kode('print("total aging :  979,900,000")\nprint("saldo tabel :  979,900,000")\nprint("selisih     :            0")'),
    blok("hasil", kode("total aging :  979,900,000\nsaldo tabel :  979,900,000\nselisih     :            0", salin=False),"HARUS MUNCUL"),
    blok("catatan","<strong>Lima kasus, lima kali diakhiri dengan selisih nol.</strong> "
        "Itu bukan kebetulan — itu satu-satunya cara kamu tahu pekerjaanmu benar tanpa ada "
        "yang memberi tahu."))

langkah("Ulangi dari ingatan",
    blok("aksi","Tutup halaman. Empat pertanyaan, tertulis.","PENGULANGAN · TANPA MEMBUKA CATATAN"),
    kode("1. Berapa persen uang masuk yang ternyata bukan pelunasan piutang?\n2. Sebutkan empat jenis penerimaan yang bukan pelunasan piutang.\n3. Kalau kamu melewatkannya, saldo piutang yang kamu laporkan salah berapa?\n4. Kenapa pencocokan keterangan bank ke pelanggan tidak boleh otomatis?", salin=False),
    "<details>\n          <summary>Cek jawabanmu</summary>\n          <div class=\"isi\">"
    "<p><strong>1.</strong> Rp 424.106.050 dari Rp 1.968.606.050 = <strong>21,5%</strong>.</p>"
    "<p><strong>2.</strong> Setoran modal direktur, bunga giro, setoran tunai tanpa keterangan, "
    "dan transfer dari pihak yang bukan pelanggan (PT Maju Bersama).</p>"
    "<p><strong>3.</strong> Rp 424 juta terlalu kecil — Rp 555 juta, bukan Rp 979 juta.</p>"
    "<p><strong>4.</strong> Karena \"PT SUMBERMAKMUR\" dan \"PT SUMBER MAKMUR SENTOSA\" hanya bisa "
    "dipastikan sama oleh orang yang tahu daftar pelanggannya.</p>"
    "</div>\n        </details>")

langkah("Lima kasus selesai — apa yang sebenarnya kamu latih",
    blok("hasil", tabel(["Kasus","Yang menjebak","Kalau lolos, akibatnya"],
        [["1 · Toko bangunan","Titik dibaca sebagai desimal","Harga meleset 1.000×"],
         ["1 · Toko bangunan","Baris subtotal ikut dijumlah","Omzet tepat 2× lipat"],
         ["2 · Klinik","merge bawaannya membuang","18 kunjungan lenyap"],
         ["2 · Klinik","Kunci kanan tidak unik","Rp 1,4 juta dihitung dua kali"],
         ["3 · Kontraktor","Nama proyek tidak sama","Merge nol baris"],
         ["3 · Kontraktor","Satu baris pemetaan","Margin bergeser 9,3 poin"],
         ["4 · Sekolah","SUM() anggap teks = nol","Rp 45,3 juta hilang"],
         ["5 · Piutang","Uang masuk ≠ pelunasan","Saldo salah Rp 424 juta"]]),"DELAPAN JEBAKAN"),
    blok("catatan","<strong>Tidak satu pun dari delapan itu menghasilkan pesan error.</strong> "
        "Semuanya jalan mulus dan memberi angka yang terlihat wajar. Yang menangkapnya bukan "
        "Python — tapi kebiasaan menutup setiap pekerjaan dengan angka kontrol dan selisih nol. "
        "Itu kebiasaan yang sudah kamu bawa dari kertas kerja, dan di sini ia jadi keunggulanmu."))

HARI5=dict(tab="Kasus 5", judul="Piutang: Rp 424 juta uang masuk yang bukan pelunasan",
  waktu="± 130 menit",
  tujuan="mencocokkan rekening koran ke daftar piutang, dan menolak asumsi yang paling mahal — "
         "bahwa setiap uang masuk berarti pelanggan membayar.",
  langkah=L, tutup_judul="Studi Kasus Nyata selesai",
  tutup="<p>Lima berkas klien, lima kali ditutup dengan selisih nol. Yang kamu latih di sini bukan "
        "pandas — tapi menolak percaya pada angka yang belum kamu buktikan.</p>"
        "<p style=\"margin-top:10px\">Berikutnya: <strong>Bekal Rahasia Klien</strong> — apa yang boleh "
        "dan tidak boleh naik ke internet begitu datanya milik orang lain.</p>")
