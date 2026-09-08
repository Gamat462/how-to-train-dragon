# Jadwal Pengulangan Berjarak (Spaced Repetition)

## Kenapa ini yang menentukan

Mengerjakan 60 soal dalam seminggu lalu berhenti = lupa dalam sebulan.
Mengerjakan soal yang sama **tersebar** di hari ke-1, 3, 7, 14, 30 = ingat bertahun-tahun.

Ini bukan pendapat; ini temuan riset memori yang paling mapan (efek jarak / *spacing
effect*). Bootcamp mahal sering justru gagal di sini karena mengejar jadwal padat.

**Aturannya:** tiap konsep diulang 5 kali dengan **variasi soal yang berbeda** dan
kesulitan yang naik. Mengulang soal yang persis sama hanya melatih hafalan.

## Interval

| Ulangan | Jarak dari pertama | Yang dikerjakan |
|---|---|---|
| U1 | hari yang sama | Soal aslinya |
| U2 | +1 hari | Variasi mudah, dari ingatan |
| U3 | +3 hari | Variasi berbeda konteks |
| U4 | +7 hari | Variasi lebih sulit |
| U5 | +14 hari | Gabungan dengan konsep lain |
| U6 | +30 hari | Soal level berikutnya yang memakai konsep ini |

## Jadwal 12 minggu

Tiap baris = satu hari belajar. `[baru]` materi baru, `U2`–`U6` pengulangan.

| Hari | Materi baru | Pengulangan hari itu |
|---|---|---|
| 1 | L1.1–L1.4 `[K1]` | — |
| 2 | L1.5–L1.8 `[K1]` | U2: L1.1–L1.4 |
| 3 | L1.9–L1.12 `[K1]` | U2: L1.5–L1.8 |
| 4 | L2.1–L2.3 `[K2]` | U3: L1.1–L1.4 |
| 5 | L2.4–L2.6 `[K2][K3]` | U2: L2.1–L2.3 · U3: L1.5–L1.8 |
| 6 | L2.7–L2.9 `[K2]` | U3: L1.9–L1.12 |
| 7 | *istirahat* | Tinjau catatan minggu ini |
| 8 | L2.10–L2.12 `[K6]` | U4: L1.1–L1.8 |
| 9 | L3.1–L3.2 `[K4]` | U2: L2.10–L2.12 |
| 10 | L3.3–L3.4 `[K4]` | U3: L2.1–L2.6 · U2: L3.1–L3.2 |
| 11 | L3.5–L3.6 `[K5]` | U4: L1.9–L1.12 |
| 12 | L3.7–L3.8 `[K4][K9]` | U3: L3.1–L3.4 |
| 13 | *kejar ketinggalan* | Ulangi yang nilainya < 3 |
| 14 | *istirahat* | — |
| 15 | L4.1–L4.2 `[K6]` | U5: L1 lengkap (uji 90 menit) |
| 16 | L4.3 `[K8]` | U4: L2.1–L2.6 · U2: L4.1–L4.2 |
| 17 | L4.4–L4.5 `[K6][K8]` | U4: L3.1–L3.4 |
| 18 | L4.6 `[K8]` | U3: L4.1–L4.3 |
| 19 | L4.7–L4.8 `[K9]` | U5: L2 lengkap |
| 20 | *kejar ketinggalan* | — |
| 21 | *istirahat* | — |
| 22–28 | **L5.1** (5 tahap, sepekan penuh) | U4: L4.1–L4.5 |
| 29–32 | L5.2, L5.3 | U6: L1 + L2 (uji gabungan) |
| 33–36 | L5.4 | U5: L3 lengkap |
| 37–49 | **L5.5 proyek akhir** | U6: L3 + L4 |
| 50–56 | Rapikan portofolio, latihan presentasi | Ulangi semua soal bernilai < 3 |

## Kartu ingatan (buat sendiri)

Untuk tiap konsep, tulis satu kartu berisi **pola**, bukan jawaban:

```
K4 — Window function
Kapan dipakai : membandingkan baris dgn baris lain tanpa meringkas
Pola          : FUNC() OVER (PARTITION BY grup ORDER BY urutan)
Jebakan       : hasil window tidak bisa disaring di WHERE, bungkus CTE dulu
Contoh migas  : peringkat sumur per lapangan, decline bulan ke bulan
```

Baca ulang kartu 2 menit sebelum mulai belajar tiap hari. Itu saja sudah menaikkan
retensi secara nyata.

## Aturan yang membuat ini berhasil

1. **Kerjakan pengulangan dari ingatan dulu.** Jangan buka catatan. Buka hanya
   setelah macet lebih dari 5 menit.
2. **Yang sulit diulang lebih sering.** Kalau satu soal terasa berat di U3,
   masukkan lagi di U4 dan U5. Yang terasa mudah boleh dilewati.
3. **Jangan pindah level sebelum level sebelumnya lolos.** Ambang: bisa
   mengerjakan 80% soal tanpa bantuan, dalam batas waktu.
4. **Catat nilaimu.** Pola nilaimu sendiri adalah data — dan kamu sedang belajar
   membaca data.
