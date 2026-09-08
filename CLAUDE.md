# Rute Data Analyst — kurikulum berbahasa Indonesia

Kurikulum belajar mandiri untuk satu pembaca: mantan auditor KAP Indonesia,
pemula murni pemrograman, yang sedang pindah karier jadi data analyst.
Modul diterbitkan sebagai Claude artifact dan juga dipaket sebagai zip offline.

## Lingkungan kerja pembaca (per September 2026)

**VS Code + PostgreSQL 16 di Windows**, dengan ekstensi SQLTools + SQLTools
PostgreSQL/Cockroach Driver. Bukan lagi Colab + SQLite.

- Query ditulis sebagai berkas `.sql` dan dijalankan lewat ekstensi; hasilnya
  tampil sebagai grid, jadi kotak "HARUS MUNCUL" digambar sebagai **tabel**,
  bukan `<pre>`. Yang dicocokkan pembaca: angkanya dan jumlah barisnya.
- Basis data latihan jalur SQL: `sql/senja.sql` (dibuat oleh
  `sql/buat_senja_sql.py` dari `sql/gen_final.py`, datanya identik dengan versi
  SQLite lama supaya angka di L1–L5 tetap cocok).
- Modul yang sudah dipindah: **SQL Mahir L1**. Sisanya masih SQLite/Colab.

### Cara menghasilkan keluaran modul

Jangan salin keluaran dari terminal ke berkas pembangun. Pakai `mat/_sql.py`:

```
<slug>/kueri.py       # dict slug -> SQL
python3 <slug>/jalankan.py   # menjalankan semua ke PostgreSQL -> hasil.json
python3 <slug>/bangun.py     # keluaran(H, "slug") merender hasil.json jadi tabel
```

Pesan error ikut tersimpan apa adanya — itu isi kotak
"HARUS MUNCUL — TULISAN MERAH". Menjalankan server PostgreSQL lokal:

```
su postgres -c "PATH=/usr/lib/postgresql/16/bin:$PATH; pg_ctl -D /var/lib/postgresql/senja \
  -l /var/lib/postgresql/senja/log.txt -o '-p 5433 -k /tmp/pgs -c listen_addresses=127.0.0.1' -w start"
```

## Aturan yang tidak bisa ditawar

1. **Setiap angka yang ditulis di modul harus dihasilkan dengan menjalankan kodenya.**
   Bukan dari ingatan, bukan dari perkiraan. Kalau tidak bisa dijalankan, jangan ditulis.
2. **Bahasa Indonesia** di seluruh materi, tanpa istilah teknis yang tidak dijelaskan.
3. **Skema rata-rata, bukan batas atas.** Untuk angka gaji, biaya, dan peluang —
   pakai median/rata-rata bersumber, jangan angka terbaik yang pernah dilaporkan orang.
4. **Bentuk pengajaran mengikuti `kurikulum/_pola.md`.** Baca berkas itu
   sebelum menulis atau menulis ulang modul mana pun. Isinya standar terukur,
   bukan selera.
5. **Modul yang tidak pernah membuat pembacanya melihat layar merah belum
   selesai.** `_pola.md` Bagian B mengukurnya. Tiap error yang ditulis di modul
   harus benar-benar dijalankan dulu — pesan errornya disalin apa adanya,
   sama seperti keluaran biasa.
6. **Tulis kepada orang, bukan tentang materi.** Diukur sebagai `sapa`.
   Kalimat seperti "Index-nya ada tapi tidak menolong" ditulis ulang jadi
   "Index-mu ada; index-mu tidak menolong."

## Alur kerja menulis ulang satu modul

```
cd kurikulum
python3 ukur.py                  # peringkat modul terburuk, jarak dari _pola.md
# pilih yang jaraknya paling besar, lalu:
#   1. baca modul lamanya di minggu1/<berkas>.html — pertahankan seluruh substansinya
#   2. jalankan kodenya sungguhan; tiap kotak HARUS MUNCUL diisi keluaran nyata
#   3. tulis pembangunnya di <slug>/h1.py .. h7.py + bangun.py (pola: sk/, m11/, m14/, s2/)
python3 <slug>/bangun.py         # menulis ulang minggu1/<berkas>.html
python3 _rantai.py               # memperbaiki tombol kembali/lanjut antar modul
python3 ukur.py                  # wajib 0.00 sebelum diterbitkan
```

Menerbitkan: `Artifact` dengan `url` artifact lama (ID ada di `_peta.py`).
Judul `<title>` **jangan diubah** — pembaca mengenali tab dari judulnya.

Membangun paket zip:
```
python3 _bangun.py               # WAJIB duluan — ia mengosongkan paket/
python3 _mulai.py                # menulis MULAI-DI-SINI.html + URUTAN-BELAJAR.md
```

## Peta berkas

| Berkas | Isi |
|---|---|
| `_pola.md` | standar penulisan, diturunkan dengan mengukur `bekal-python.html` |
| `ukur.py` | mengukur tiap modul terhadap standar itu — 10 ukuran, dua bagian |
| `_gen.py` | generator HTML (`bangun`, `kode`, `tabel`, `blok`) |
| `_peta.py` | artifact-id → berkas, judul, jumlah hari |
| `_urutan.py` | urutan 44 modul + fase |
| `_rantai.py` | memperbaiki rantai navigasi antar modul |
| `_bangun.py` | menyusun paket zip offline |
| `{sk,m11,m14,s2}/` | pembangun modul yang sudah ditulis ulang |
| `minggu1/*.html` | 65 sumber modul (yang diterbitkan sebagai artifact) |
| `{m11,m14,s2}-berkas/`, `kasus/` | skrip & data latihan yang ikut di dalam zip |

## Yang sudah memenuhi standar (jarak 0,00)

Bekal Python (acuan) · SQL Mahir L4 · Python Produksi.

Studi Kasus Nyata, Minggu 11, Minggu 14, dan Jalur S2 dulu berjarak 0,00 —
tapi terhadap standar yang **belum punya Bagian B**. Setelah Bagian B
ditambahkan, keempatnya kembali berjarak (1,4–2,8), hampir seluruhnya karena
`salah` mendekati nol: modulnya tidak pernah membuat pembaca melihat layar
merah. Keempatnya perlu satu putaran lagi, dan itu lebih murah daripada
menulis ulang dari awal.

Jalankan `ukur.py` untuk daftar terkini, urut terburuk dulu.

## Biaya sesi

Dua pertiga biaya sesi panjang adalah membaca ulang konteks, dan itu tumbuh
kuadratik terhadap panjang sesi. Kerjakan **3–5 modul per sesi**, lalu mulai
sesi baru. Berkas di repo ini yang membuat sesi baru langsung produktif —
jangan simpan perkakas hanya di scratchpad.
