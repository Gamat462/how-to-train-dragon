# Tugas 04 — Pembersihan Data
**Modul:** SQL & pandas, Minggu 7 · **Perkiraan waktu:** 5–6 jam
**Berkas keluaran:** `04_pembersihan.ipynb` + `transaksi_bersih.csv`

## Konteks
Tim IT mengirim ekspor dari sistem kasir lama. Bentuknya berantakan seperti
biasa. Bersihkan supaya bisa dianalisis.

## Yang harus dikerjakan
Bersihkan `transaksi_kotor.csv` (2.650 baris) sampai siap pakai.

Untuk **setiap** masalah yang kamu temukan, tulis dalam format ini:

```
### Masalah N: [nama masalah]
- Ditemukan lewat: [perintah apa yang mengungkapnya]
- Terdampak: [berapa baris]
- Keputusan: [apa yang kamu lakukan]
- Alasan: [kenapa itu pilihan terbaik]
```

## Syarat
- **Jangan langsung `dropna()`.** Untuk tiap kolom yang kosong, putuskan
  satu per satu: bisa dihitung ulang, diisi, atau memang harus dibuang?
- Data mentah harus tetap utuh (`.copy()`), supaya bisa menunjukkan sebelum-sesudah.
- Akhiri dengan tabel ringkasan: berapa baris masuk, berapa dibuang per alasan,
  berapa baris keluar.
- Simpan hasilnya sebagai `transaksi_bersih.csv`.

## Yang dinilai paling berat
Bukan jumlah baris yang tersisa, tapi **apakah keputusanmu bisa dipertanggungjawabkan**.
Membuang 40% data boleh saja kalau alasannya kuat dan ditulis. Membuang 5% tanpa
alasan tidak boleh.

## Jebakan
- Total negatif: apakah itu retur (data sah) atau kesalahan input? Kamu tidak
  bisa tahu pasti — jadi tulis asumsimu dan tandai barisnya, jangan diam-diam dibuang.
- `JKT` dan `Jakarta`: apakah kamu yakin JKT itu Jakarta? Periksa `cabang_id`-nya
  sebelum menyimpulkan. Ini bisa diverifikasi, dan kamu harus memverifikasinya.
- Duplikat penuh: apakah benar-benar duplikat, atau dua transaksi berbeda yang
  kebetulan sama persis? Lihat `transaksi_id`-nya.
