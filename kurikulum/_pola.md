# Pola Bekal Python — standar penulisan modul

Diturunkan dengan mengukur `bekal-python.html` (yang dibilang paling jelas)
terhadap 43 modul lain. Semua angka di bawah hasil hitungan, bukan selera.

## Ukuran yang harus dipenuhi

| Ukuran | Target | Rata-rata modul lama | Kenapa |
|---|---|---|---|
| Langkah per hari | **≥ 5** | 3,4 | Satu langkah = satu gagasan baru. Kalau satu hari cuma 3 langkah, tiap langkah memuat terlalu banyak. |
| Kata per langkah | **≤ 120** | 157 | Di atas itu pembaca berhenti mengerjakan dan mulai membaca. |
| Baris per blok kode (median) | **≤ 4** | 7 | Kode 10 baris menyembunyikan 4 gagasan sekaligus. |
| Baris per blok kode (maks) | **≤ 15** | 26 | Tidak ada blok yang tidak muat di satu layar HP. |
| Kotak HARUS MUNCUL per blok kode | **≥ 0,7** | 0,58 | Tiap kode yang dijalankan harus bisa dicocokkan. |
| Langkah "ulangi dari ingatan" | **wajib tiap hari** | sering tidak ada | Memanggil dari ingatan mengikat, membaca ulang tidak. |

## Bentuk satu langkah

Urutannya tetap, dan tidak boleh dibalik:

1. **LAKUKAN** — perintah fisik. "Klik di kotak abu-abu", "buka tab baru",
   "hapus isi editor dulu". Bukan "sekarang kita akan mempelajari".
2. **Kode 1–4 baris.** Satu hal baru saja. Kalau butuh 10 baris, itu
   tiga langkah, bukan satu.
3. **HARUS MUNCUL** — keluaran persisnya, hasil dijalankan sungguhan.
4. **Kalimat yang menjelaskan** — sesudah dikerjakan, bukan sebelum.
   Maksimal 2–3 kalimat.
5. *(kalau perlu)* **YANG NORMAL TAPI BIKIN PANIK** — "lambat 5–20 detik
   itu wajar", "tidak ada hasil yang muncul itu memang benar".
6. *(kalau perlu)* `<details>` untuk "kenapa begitu" dan "kalau punyaku beda".

## Yang dilarang

- Paragraf penjelasan tanpa satu pun hal yang dikerjakan.
  (M7 langkah 2 sekarang: 33 kata prosa, nol kode, nol verifikasi.)
- Blok kode yang memperkenalkan lebih dari satu hal baru.
  (MAT L2 langkah 2 sekarang: norma + dot product + cosinus + definisi
  fungsi, semuanya dalam 10 baris.)
- Kode 100 baris. (Studi Kasus Nyata punya satu.)
- Menyebut istilah sebelum dipakai. Pakai dulu, beri namanya belakangan.
- Angka yang tidak dihasilkan dengan menjalankan kodenya.

## Yang tetap dipertahankan

- Bahasa Indonesia, tanpa istilah teknis yang tidak dijelaskan.
- Tiap langkah punya kotak centang.
- Kunci jawaban di dalam `<details>`, bukan langsung terlihat.
- Menyebut batasan dan apa yang tidak dijawab modul itu.
