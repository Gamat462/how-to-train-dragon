# Pola Bekal Python — standar penulisan modul

Diturunkan dengan mengukur `bekal-python.html` (modul yang dibilang paling jelas)
terhadap 43 modul lain. Semua angka di bawah hasil hitungan, bukan selera.
Jalankan `python3 ukur.py` untuk melihat jarak tiap modul dari standar ini.

Standar ini punya **dua bagian**. Bagian A adalah kerangkanya. Bagian B adalah
cara mengajarnya. Versi pertama standar ini hanya berisi Bagian A — dan itu
ternyata tidak cukup: dua modul bisa sama-sama berjarak 0,00 pada Bagian A dan
tetap terasa jauh berbeda saat dibaca. Bagian B ditambahkan setelah mengukur
kenapa.

## A. Kerangka

| Ukuran | Target | Acuan | Rata-rata modul lama | Kenapa |
|---|---|---|---|---|
| Langkah per hari | **≥ 5** | 5,4 | 3,4 | Satu langkah = satu gagasan baru. |
| Kata per langkah | **≤ 120** | 84 | 157 | Di atas itu pembaca berhenti mengerjakan dan mulai membaca. |
| Baris per blok kode (median) | **≤ 4** | 4 | 7 | Kode 10 baris menyembunyikan 4 gagasan sekaligus. |
| Baris per blok kode (maks) | **≤ 15** | 14 | 26 | Tidak ada blok yang tidak muat di satu layar HP. |
| Kotak keluaran per blok kode | **≥ 0,7** | 0,91 | 0,58 | Tiap kode yang dijalankan harus bisa dicocokkan. |

**Padat bukan berarti baik.** Acuannya 5,4 langkah per hari dan ±40 menit —
bukan 12 langkah dan 60 menit. Target "≥ 5" itu **lantai, bukan sasaran**.
Melampauinya dua kali lipat berarti modulnya jadi daftar periksa, bukan pelajaran.

## B. Cara mengajar

Diukur per 10 langkah (kecuali baris terakhir).

| Ukuran | Target | Acuan | Kenapa |
|---|---|---|---|
| **Error sengaja ditimbulkan** lalu dibaca bersama | **≥ 1,5** | 3,7 | Pembaca harus melihat merah **saat masih ditemani**, bukan pertama kali sendirian jam 11 malam. |
| **Menenangkan** — "itu normal", "bukan bencana" | **≥ 1,2** | 1,4 | Yang membuat pemula berhenti bukan kesulitan, tapi mengira dirinya merusak sesuatu. |
| **Jembatan ke dunia yang sudah dikuasai** — Excel, audit, jurnal, kertas kerja | **≥ 0,9** | 0,9 | Pembaca ini punya bertahun-tahun pengalaman assurance. Menyambung ke situ jauh lebih cepat daripada mengajar dari nol. |
| **"Kalau punyamu beda…"** | **≥ 0,2** | 0,5 | Tanpa ini, hasil yang berbeda = pembaca menyimpulkan dirinya gagal. |
| **Kata "kamu" per langkah** | **≥ 1,4** | 1,86 | Modul yang menjelaskan berbicara tentang materi. Modul yang mengajar berbicara kepada orang. |

## Bentuk satu langkah

Urutannya tetap, dan tidak boleh dibalik:

1. **LAKUKAN** — perintah fisik. "Klik di kotak abu-abu", "buka tab baru",
   "hapus isi editor dulu". Bukan "sekarang kita akan mempelajari".
   Kalau butuh lebih dari satu gerakan, **beri nomor tiap gerakannya** —
   acuan menulis "Buka browser → ketik alamat → Enter → klik New notebook"
   sebagai empat baris terpisah, bukan satu kalimat.
2. **Kode 1–4 baris.** Satu hal baru saja.
3. **Kotak keluaran** — persisnya, hasil dijalankan sungguhan.
   **Labeli sesuai apa yang dilihat mata**, jangan `HARUS MUNCUL` datar
   untuk semuanya. Acuan memakai: `YANG HARUS TERLIHAT` (untuk keadaan layar,
   bukan teks), `HARUS MUNCUL DI BAWAH SEL`, `HARUS MUNCUL — TULISAN MERAH,
   DAN ITU DISENGAJA`, `SETIAP KALI LAYAR MERAH`.
4. **Kalimat yang menjelaskan** — sesudah dikerjakan, bukan sebelum.
   Maksimal 2–3 kalimat.
5. *(kalau perlu)* **YANG NORMAL TAPI BIKIN PANIK** — "lambat 5–20 detik
   itu wajar", "tidak ada hasil yang muncul itu memang benar".
6. *(kalau perlu)* `<details>` untuk "kenapa begitu" dan "kalau punyaku beda".

## Yang dilarang

- Paragraf penjelasan tanpa satu pun hal yang dikerjakan.
- Blok kode yang memperkenalkan lebih dari satu hal baru.
- Kode 100 baris.
- Menyebut istilah sebelum dipakai. Pakai dulu, beri namanya belakangan.
- Angka yang tidak dihasilkan dengan menjalankan kodenya.
- **Modul yang tidak pernah membuat pembacanya melihat pesan error.**
  Kalau tujuh hari berlalu tanpa satu pun layar merah yang disengaja,
  pembaca belum dilatih menghadapi hal yang paling sering ia temui sendirian.

## Yang tetap dipertahankan

- Bahasa Indonesia, tanpa istilah teknis yang tidak dijelaskan.
- Tiap langkah punya kotak centang.
- Kunci jawaban di dalam `<details>`, bukan langsung terlihat.
- Menyebut batasan dan apa yang tidak dijawab modul itu.
- Penutup hari berisi **daftar pendek untuk ditulis tangan di buku fisik** —
  bukan ringkasan untuk dibaca ulang.
