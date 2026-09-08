# Bank Soal Migas — 5 Tingkat Kesulitan

Kerjakan **tanpa membuka jawaban**. Jawaban ada di `02_KUNCI_JAWABAN.md`,
sengaja dipisah supaya kamu tidak tergoda mengintip.

Setiap soal punya kode konsep dalam kurung, misalnya `[K4]`. Kode itu dipakai
oleh jadwal pengulangan berjarak di `03_JADWAL_PENGULANGAN.md` — konsep yang
sama akan muncul lagi beberapa hari kemudian dalam bentuk soal berbeda.

## Peta konsep

| Kode | Konsep | Muncul di level |
|---|---|---|
| K1 | Agregasi & filter | 1, 2, 3 |
| K2 | JOIN multi-tabel | 2, 3, 4 |
| K3 | Rasio & normalisasi | 2, 3, 4, 5 |
| K4 | Window function | 3, 4 |
| K5 | Deret waktu & tren | 3, 4, 5 |
| K6 | Rekonsiliasi & alokasi | 4, 5 |
| K7 | Uptime & keandalan | 2, 4 |
| K8 | Ekonomi & PSC | 4, 5 |
| K9 | Deteksi anomali | 4, 5 |
| K10 | Peramalan & kurva decline | 5 |

---

# LEVEL 1 — FONDASI
*SELECT, WHERE, GROUP BY, ORDER BY. Target: 12 soal dalam 90 menit.*

**L1.1** `[K1]` Berapa total produksi minyak (bbl) sepanjang 2025?

**L1.2** `[K1]` Ada berapa sumur produser dan berapa injektor?

**L1.3** `[K1][K2]` Produksi minyak per lapangan sepanjang 2025, urut terbesar.

**L1.4** `[K1]` Lima sumur dengan produksi kumulatif terbesar sepanjang seluruh periode.

**L1.5** `[K1][K7]` Berapa hari-sumur yang tidak berproduksi sama sekali?

**L1.6** `[K1]` Jumlah insiden HSE per jenis, urut terbanyak.

**L1.7** `[K1][K5]` Rata-rata ICP per tahun.

**L1.8** `[K1]` Total biaya per jenis (OPEX vs CAPEX).

**L1.9** `[K1]` Metode angkat (artificial lift) apa yang paling banyak dipakai?

**L1.10** `[K1]` Volume dan nilai lifting per tujuan (Domestik vs Ekspor).

**L1.11** `[K1][K7]` Penyebab downtime paling sering, dan total hari yang hilang.

**L1.12** `[K1]` Jumlah dan total biaya workover per jenis pekerjaan.

---

# LEVEL 2 — MENENGAH
*JOIN, rasio, HAVING, penanganan tanggal. Target: 12 soal dalam 3 jam.*

**L2.1** `[K2]` Produksi minyak per lapangan per tahun, tampilkan **nama** lapangan (bukan ID).

**L2.2** `[K2][K3]` Watercut rata-rata per lapangan per tahun. Lapangan mana paling "basah",
dan apa artinya bagi umur lapangan itu?

**L2.3** `[K2][K7]` Uptime (%) per lapangan sepanjang 2025. Urut dari yang terburuk.

**L2.4** `[K2][K3]` **Lifting cost per bbl per lapangan 2025** (OPEX saja, jangan masukkan CAPEX).
Ini metrik paling sering ditanya manajemen.

**L2.5** `[K2][K3]` Sumur yang watercut-nya sudah melewati 90% pada data terakhirnya.

**L2.6** `[K2]` Lapangan mana yang insiden HSE tingkat Berat-nya paling banyak?

**L2.7** `[K2][K8]` Produksi bulanan 2026 beserta ICP dan gross revenue perkiraannya.

**L2.8** `[K2]` Bandingkan sumur yang pernah di-workover vs yang belum: berapa jumlahnya
dan berapa rata-rata produksinya? **Hati-hati menyimpulkan sebab-akibat dari sini.**

**L2.9** `[K2][K7]` Sumur produser yang tidak pernah punya catatan downtime sama sekali.
(Petunjuk: anti-join)

**L2.10** `[K2][K6]` Bandingkan volume lifting vs volume produksi per tahun. Apakah cocok?
Berapa persen selisihnya, dan apa penjelasan yang masuk akal?

**L2.11** `[K2][K3][K8]` Rata-rata biaya workover per jenis, dan rata-rata kenaikan produksinya.
Jenis mana yang paling murah per unit kenaikan?

**L2.12** `[K1][K5]` Berapa jumlah LTI dan hari kerja hilang per tahun?

---

# LEVEL 3 — LANJUTAN
*Window function, CTE, Pareto, moving average. Target: 8 soal dalam 4 jam.*

**L3.1** `[K4][K5]` Produksi bulanan lapangan F04 dengan kolom tambahan: volume bulan lalu
dan pertumbuhan persennya. (LAG)

**L3.2** `[K4][K2]` Tiga sumur teratas di **tiap** lapangan berdasarkan produksi 2025.
(ROW_NUMBER + PARTITION BY)

**L3.3** `[K4]` Produksi kumulatif berjalan per bulan untuk lapangan F01. (SUM OVER)

**L3.4** `[K4][K3]` Analisis Pareto: kontribusi tiap sumur terhadap total lapangan F01 di 2025,
plus kolom kumulatif persen. **Berapa sumur yang menyumbang 80% produksi?**

**L3.5** `[K4][K5]` Moving average 30 hari produksi lapangan F03. Kenapa perlu diratakan?

**L3.6** `[K3][K5]` Decline rate tiap sumur: bandingkan rata-rata bopd 2024 vs 2025, urut
dari yang paling curam.

**L3.7** `[K4][K9]` Hari dengan produksi terendah di tiap bulan untuk F01 — kandidat investigasi.

**L3.8** `[K4][K3]` Perubahan pangsa tiap lapangan terhadap total produksi, 2023 vs 2025.
Lapangan mana yang perannya menyusut, dan kenapa?

---

# LEVEL 4 — SULIT
*Rekonsiliasi, efektivitas intervensi, anomali, ekonomi. Target: 8 soal dalam 8 jam.*

**L4.1** `[K6][K8]` **REKONSILIASI:** apakah `gross_revenue_usd` di tabel PSC cocok dengan
`volume produksi × ICP`? Hitung ulang dari data mentah dan cari selisihnya.
Ini persis pekerjaan audit cost recovery.

**L4.2** `[K6][K8]` **UJI KEUTUHAN PSC:** buktikan bahwa
`gross = FTP + cost recovery + ETS` untuk setiap bulan. Kalau ada bulan yang tidak
seimbang, itu temuan audit.

**L4.3** `[K8][K3]` Government take (%) per bulan, disandingkan dengan ICP.
**Apa hubungannya, dan kenapa arahnya begitu?**

**L4.4** `[K6][K9]` **EFEKTIVITAS WORKOVER:** bandingkan rata-rata produksi 30 hari sebelum
workover vs 30 hari sesudah (jangan lupa lewati masa pengerjaannya).
Jenis pekerjaan mana yang paling berhasil?

**L4.5** `[K8][K3]` **PAYBACK WORKOVER:** berapa hari modal workover kembali, memakai ICP
bulan pengerjaan? Urutkan dari yang tercepat.

**L4.6** `[K8][K3]` **BATAS EKONOMIS:** hitung biaya operasi per sumur per bulan, lalu
bandingkan dengan pendapatan tiap sumur di kuartal terakhir. Adakah sumur yang merugi?

**L4.7** `[K9][K3]` **ANOMALI:** temukan sumur yang produksinya turun jauh lebih cepat
daripada rata-rata rekan selapangan. Kandidat intervensi.

**L4.8** `[K6][K7][K8]` **DAMPAK DOWNTIME:** perkirakan berapa bbl hilang akibat tiap
penyebab downtime, lalu nilai dalam USD memakai ICP saat kejadian.
Penyebab mana yang paling mahal?

---

# LEVEL 5 — SANGAT SULIT
*Butuh Python. Ini setara pekerjaan analis senior. Target: 5 soal dalam 20 jam.*

**L5.1** `[K10][K5]` **DECLINE CURVE ANALYSIS & CADANGAN.**

Cocokkan persamaan Arps `q(t) = qi/(1+b·D·t)^(1/b)` ke tiap sumur, lalu ramalkan
sisa cadangan sampai batas ekonomis 15 bopd.

Ini soal berjebak. Kerjakan bertahap dan perhatikan apa yang rusak:

- **Tahap A** — fit langsung ke seluruh data tiap sumur. Catat R² dan sisa cadangannya.
- **Tahap B** — periksa hasil Tahap A. Ada sumur dengan cadangan puluhan juta barel
  dan R² mendekati nol. **Cari tahu kenapa** sebelum lanjut.
- **Tahap C** — perbaiki dengan hanya memakai segmen data yang bersih. Tetapkan
  aturan kendali mutu: berapa lama sesudah workover data boleh dipakai lagi,
  berapa minimum panjang segmen, dan berapa R² minimum yang kamu terima.
- **Tahap D** — periksa lagi. Sekarang R² bagus, tapi ada sumur yang umurnya
  mentok di batas proyeksimu. **Kenapa hiperbolik dengan b besar berbahaya?**
- **Tahap E** — terapkan praktik industri: batasi `b ≤ 1,0` dan beralih ke
  **terminal exponential decline** saat laju decline sesaat turun di bawah 8%/tahun.
  Bandingkan hasilnya dengan Tahap C. Berapa persen selisihnya?

Laporkan: berapa sumur lolos kendali mutu, berapa ditolak dan alasannya, EUR total,
sisa cadangan, dan tingkat pengurasan lapangan.

**L5.2** `[K8][K3]` **BATAS EKONOMIS PER LAPANGAN.**
Hitung *economic limit rate* (bopd minimum agar sumur menutup biayanya) untuk tiap
lapangan pada tiga skenario harga: $50, $65, $80 per bbl. Lalu identifikasi sumur
mana yang saat ini sudah di bawah batas itu. Sertakan asumsimu tentang cara
membagi biaya lapangan ke tiap sumur — dan jelaskan kenapa cara itu bisa diperdebatkan.

**L5.3** `[K6][K3]` **ALOKASI BIAYA G&A: tiga metode, tiga jawaban berbeda.**
Alokasikan total biaya G&A 2025 ke empat lapangan dengan tiga dasar berbeda:
(a) proporsi volume produksi, (b) jumlah sumur, (c) jumlah hari-sumur aktif.
Hitung selisih terbesar antar metode. **Metode mana yang paling adil, dan kenapa
pertanyaan "paling adil" itu sebenarnya keputusan bisnis, bukan keputusan teknis?**

Ini soal paling dekat dengan pekerjaan audit cost recovery yang sesungguhnya.

**L5.4** `[K8][K10]` **SENSITIVITAS PSC TERHADAP HARGA.**
Hitung ulang seluruh mekanisme PSC pada lima skenario harga: −30%, −15%, dasar,
+15%, +30%. Tampilkan gross revenue, cost recovery, government take, dan bagian
kontraktor. **Jelaskan kenapa persentase government take NAIK saat harga naik,
dan apa artinya bagi kontraktor saat harga jatuh.**

**L5.5** `[K9][K10][K6]` **PROYEK AKHIR: rencana intervensi berbasis data.**
Gabungkan semuanya. Pilih 5 sumur kandidat workover untuk anggaran terbatas
$3.000.000. Untuk tiap kandidat wajib ada:

- Bukti bahwa sumur itu berkinerja di bawah potensinya (bandingkan dengan rekan
  selapangan dan dengan kurva decline-nya sendiri)
- Perkiraan kenaikan produksi berdasarkan hasil workover historis pada jenis
  pekerjaan serupa
- Perhitungan payback dan NPV sederhana pada tiga skenario harga
- Risiko dan asumsi yang kamu buat

Keluaran: memo satu halaman untuk manajemen (tanpa istilah statistik) plus
notebook pendukung. **Ini yang akan kamu presentasikan di wawancara.**
