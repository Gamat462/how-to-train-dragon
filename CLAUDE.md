# Rute Data Analyst — kurikulum berbahasa Indonesia

Kurikulum belajar mandiri untuk satu pembaca: mantan auditor KAP Indonesia,
pemula murni pemrograman, yang sedang pindah karier jadi data analyst.
Modul diterbitkan sebagai Claude artifact dan juga dipaket sebagai zip offline.

## Aturan yang tidak bisa ditawar

1. **Setiap angka yang ditulis di modul harus dihasilkan dengan menjalankan kodenya.**
   Bukan dari ingatan, bukan dari perkiraan. Kalau tidak bisa dijalankan, jangan ditulis.
2. **Bahasa Indonesia** di seluruh materi, tanpa istilah teknis yang tidak dijelaskan.
3. **Skema rata-rata, bukan batas atas.** Untuk angka gaji, biaya, dan peluang —
   pakai median/rata-rata bersumber, jangan angka terbaik yang pernah dilaporkan orang.
4. **Bentuk pengajaran mengikuti `kurikulum/_pola.md`.** Baca berkas itu
   sebelum menulis atau menulis ulang modul mana pun. Isinya standar terukur,
   bukan selera.

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
| `_pola.md` | standar penulisan, diturunkan dengan mengukur |
| `ukur.py` | mengukur tiap modul terhadap standar itu |
| `_gen.py` | generator HTML (`bangun`, `kode`, `tabel`, `blok`) |
| `_peta.py` | artifact-id → berkas, judul, jumlah hari |
| `_urutan.py` | urutan 44 modul + fase |
| `_rantai.py` | memperbaiki rantai navigasi antar modul |
| `_bangun.py` | menyusun paket zip offline |
| `{sk,m11,m14,s2}/` | pembangun modul yang sudah ditulis ulang |
| `minggu1/*.html` | 65 sumber modul (yang diterbitkan sebagai artifact) |
| `{m11,m14,s2}-berkas/`, `kasus/` | skrip & data latihan yang ikut di dalam zip |

## Yang sudah memenuhi standar (jarak 0,00)

Bekal Python (acuan) · Studi Kasus Nyata · Minggu 11 · Minggu 14 · Jalur S2.
Sisanya menunggu, urut terburuk dulu — jalankan `ukur.py` untuk daftar terkini.

## Biaya sesi

Dua pertiga biaya sesi panjang adalah membaca ulang konteks, dan itu tumbuh
kuadratik terhadap panjang sesi. Kerjakan **3–5 modul per sesi**, lalu mulai
sesi baru. Berkas di repo ini yang membuat sesi baru langsung produktif —
jangan simpan perkakas hanya di scratchpad.
