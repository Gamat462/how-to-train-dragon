# artifact-id -> (berkas lokal, nomor urut belajar, judul pendek, hari)
# nomor urut = urutan membukanya. 0 = navigasi, 900+ = arsip/referensi.
PETA = {
 # navigasi
 "e60e0d95-6d7b-4245-ac7a-f23e60237cfd": ("indeks-rute-data-analyst.html",      1, "Indeks Rute (peta semua modul)", ""),
 "f333a8b3-8341-4a10-b69e-4c603671830e": ("jadwal-harian-data-analyst.html",    2, "Rencana 21 Minggu + jadwal harian", ""),
 # persiapan
 "36da060f-fd96-4381-88b7-7500c6b6ecdf": ("minggu1/bekal-python.html",         10, "Bekal Python", "8 hari"),
 # jalur utama
 "df7c645b-ee38-4ee1-b60c-499ee6055467": ("minggu1/minggu-pertama.html",       20, "M1 — SQL dari nol", "hari 1–7"),
 "b2c56e91-5737-4cf3-9cd9-f865551bed10": ("minggu1/minggu-kedua.html",         21, "M2 — JOIN & data sungguhan", "hari 8–14"),
 "e672ec75-7caf-45aa-b90c-726ce55d46b7": ("minggu1/minggu-ketiga.html",        22, "M3 — Python & pandas", "hari 15–21"),
 "7709a33d-1165-48f7-9534-e29934144e94": ("minggu1/minggu-keempat.html",       23, "M4 — Statistik & A/B Test", "hari 22–28"),
 "0ebf361e-700d-4314-84d8-fd0bdc7b0dd0": ("minggu1/minggu-kelima.html",        24, "M5 — Visualisasi Data", "hari 29–35"),
 "7a1dae30-ebd4-4de7-bbce-722bbbf0be7e": ("minggu1/minggu-keenam.html",        25, "M6 — SQL Lanjutan", "hari 36–42"),
 # sesudah M6: data klien + studi kasus
 "88ce46d0-54b8-4c0b-924d-beb4c8389d7a": ("minggu1/bekal-data-klien.html",     30, "Bekal Data Klien", "6 hari"),
 "e87748bf-c615-4461-951e-248010b4ae34": ("minggu1/studi-kasus-nyata.html",    31, "Studi Kasus Nyata", "5 kasus"),
 # lanjut jalur utama
 "007d7e74-727a-40b9-a698-4835977d084a": ("minggu1/minggu-ketujuh.html",       40, "M7 — Statistik Lanjutan", "hari 43–49"),
 "62446bd7-6166-47dc-b19d-9359b7ea8b99": ("minggu1/minggu-kedelapan.html",     41, "M8 — Visualisasi Lanjutan & BI", "hari 50–56"),
 "e653810a-9c48-4b3e-af6e-8d439618c677": ("minggu1/bekal-rahasia-klien.html",  42, "Bekal Rahasia Klien", "4 hari"),
 "fea52a73-a3eb-400b-8630-d09ccc516fcf": ("minggu1/minggu-kesembilan.html",    43, "M9 — SQL Data Besar", "hari 57–63"),
 "26a3ee5f-9d8a-4679-9977-37c06da48459": ("minggu1/minggu-kesepuluh.html",     44, "M10 — dbt", "hari 64–70"),
 "b38ca0a5-abff-4b2d-b657-06b6503d0cb4": ("minggu1/minggu-kesebelas.html",     45, "M11 — Git, Otomasi & Streamlit", "hari 71–77"),
 "5b5ec5dd-823f-475a-b3ef-7e825575a760": ("minggu1/bekal-kirim-hasil.html",    46, "Bekal Kirim Hasil", "5 hari"),
 "fbf23eb1-4965-46e5-b3d5-b839c25fdfae": ("minggu1/minggu-keduabelas.html",    47, "M12 — Product Analytics", "hari 78–84"),
 "1c78fa92-69e9-4546-a3b1-075eabd3e5c8": ("minggu1/minggu-ketigabelas.html",   48, "M13 — Machine Learning", "hari 85–91"),
 # spesialisasi migas
 "70d5a371-10fd-485b-909f-e7e62d8ac4f0": ("minggu1/migas-minggu-1.html",       50, "Migas L1 — Fondasi blok & PSC", "hari 1–7"),
 "24fee33e-bafb-459c-8560-4a848e1257a8": ("minggu1/migas-minggu-2.html",       51, "Migas L2 — Perbandingan adil & bias", "hari 8–14"),
 "5fc399f9-833f-48f5-88a2-57b9b9f7963c": ("minggu1/migas-minggu-3.html",       52, "Migas L3 — Window function di lapangan", "hari 15–21"),
 "35f58664-afca-4799-8bb3-0e39d0025823": ("minggu1/migas-minggu-4.html",       53, "Migas L4 — Rekonsiliasi PSC", "hari 22–28"),
 "59473952-fe59-4f21-b945-840ac06a7cee": ("minggu1/migas-minggu-5.html",       54, "Migas L5 — Cadangan & keputusan $3 juta", "hari 29–35"),
 # penutup jalur utama
 "595c379b-9f99-4c29-9c03-ab4450b5414c": ("minggu1/minggu-keempatbelas.html",  60, "M14 — Portofolio & CV", "hari 92–98"),
 "010bd5cc-8f09-449b-b3de-7bba52005d31": ("minggu1/minggu-kelimabelas.html",   61, "M15 — Wawancara & Lamaran", "hari 99–105"),
 # sql mahir
 "caff475b-354e-4331-84f9-d7fd36fe51b4": ("minggu1/sql-mahir-l1.html",         70, "SQL Mahir L1 — dasar yang bolong", "7 hari"),
 "07cb0fb0-1240-471b-85b7-f691b8a585bd": ("minggu1/sql-mahir-l2.html",         71, "SQL Mahir L2 — window function tuntas", "7 hari"),
 "eff7b693-41fe-43a5-a667-14e294c3e7d9": ("minggu1/sql-mahir-l3.html",         72, "SQL Mahir L3 — enam pola wawancara", "7 hari"),
 "2d44eed8-d057-4afc-b429-974231efea42": ("minggu1/sql-mahir-l4.html",         73, "SQL Mahir L4 — kinerja & keandalan", "7 hari"),
 "7044e726-f69e-4b48-a3d5-b6e277c79164": ("minggu1/sql-mahir-l5.html",         74, "SQL Mahir L5 — ujian & wawancara", "7 hari"),
 # paralel
 "15ba1f07-96fd-4636-b694-f2cf31f020cd": ("minggu1/sql-produksi.html",       75, "SQL Produksi — kosakata database kantor", "7 hari"),
 "e5ebbbde-69c2-4a12-a118-9eaa29210949": ("minggu1/python-produksi.html",    76, "Python Produksi — dari notebook jadi alat", "7 hari"),
 "9e8025f8-28cb-48cd-bee3-809b610567a6": ("minggu1/jalur-pintu-b.html",     77, "Jalur Pintu B — melamar ke tempat yang tepat", "3 hari"),
 "b20c546a-92f3-480f-81ae-4ba51728dc69": ("minggu1/ujian-bernilai.html",    78, "Ujian Bernilai — 60 poin, berwaktu", "2 hari"),
 "61355282-6fe8-4f54-bd99-18ff4ae63d28": ("minggu1/proyek-buta.html",       79, "Proyek Buta — tanpa kunci jawaban", "5 hari"),
 "d70b6a53-5f3a-483d-83e4-79aba530fdb0": ("minggu1/jalur-s2-luar-negeri.html", 85, "Jalur S2 Luar Negeri — silabus, biaya, keputusan", "7 hari"),
 "f6784136-a13e-47e9-9eae-0264bd514182": ("minggu1/mat-L1-probabilitas.html", 90, "MAT L1 — Probabilitas formal", "7 hari"),
 "f5079d99-9181-47a2-9ce4-7747feca52a3": ("minggu1/mat-L2-aljabar-linear.html", 91, "MAT L2 — Aljabar linear terapan", "7 hari"),
 "6dc7de48-3ed0-4126-8455-a2c82e7bad4c": ("minggu1/mat-L3-optimisasi.html", 92, "MAT L3 — Optimisasi numerik", "7 hari"),
 "bf6f3e02-66dc-40a4-a649-f1c260029d36": ("minggu1/mat-L4-deep-learning.html", 93, "MAT L4 — Deep learning dari nol", "7 hari"),
 "c1664d77-5877-4da8-ade7-764018718b5c": ("minggu1/jalur-freelance.html",      80, "Jalur Freelance", "12 hari, 1/minggu"),
 "ffcc437e-1901-484c-a73b-128865461cd1": ("minggu1/bekal-excel-kantor.html", 62, "Bekal Excel Kantor", "7 hari"),
 "f1e55d95-3ab1-4904-b378-ff0886a08852": ("minggu1/bekal-alat-kantor.html", 63, "Bekal Alat Kantor", "5 hari"),
 "746fbb14-8c40-41a3-9882-5af02e150b66": ("minggu1/bekal-bahasa-inggris.html", 64, "Bekal Bahasa Inggris Kerja", "5 hari"),
 "2427d59c-05e9-4074-98fd-eaa65ca2758e": ("minggu1/menulis-untuk-manajemen.html", 65, "Menulis untuk Manajemen", "3 hari"),
 # arsip & referensi
 "82b73f76-cd26-427b-9aee-bb7ffe05fb48": ("buku-rute-data-analyst.html",      900, "Buku Rute (versi awal)", ""),
 "83f08225-e6a6-46f9-9e63-5dc4bd9fb1f7": ("rute-data-analyst.html",           901, "Rute Data Analyst (versi awal)", ""),
 "3a77a21e-5ef7-414c-a16e-3ebfc931926b": ("skema-setahun-data-analyst.html",  902, "Skema Setahun (versi awal)", ""),
 "0bd92934-cb00-4b7d-91a1-53a77d0ef5a3": ("modul-01-data-dan-excel.html",     910, "Referensi: Data & Excel", ""),
 "e1b8a424-63b9-4dc3-82aa-aa8bb13decb5": ("modul-sql-pandas.html",            911, "Referensi: SQL & pandas", ""),
 "ee0a9356-8cba-4c75-8bc8-bcf1cacf22b2": ("modul-statistik-abtest.html",      912, "Referensi: Statistik & A/B Test", ""),
 "de7bb9b6-0dbf-46cf-87f2-50d6bfc2324a": ("modul-visualisasi-bi.html",        913, "Referensi: Visualisasi & BI", ""),
 "479c1635-d7eb-478b-86d9-adbe0e9df084": ("modul-analytics-engineering.html", 914, "Referensi: Analytics Engineering", ""),
 "cf300cca-518f-453d-a3fe-a356d21e09ea": ("modul-product-analytics.html",     915, "Referensi: Product Analytics", ""),
 "5abc1987-e82a-44ca-8d96-73f1faf2220e": ("modul-machine-learning.html",      916, "Referensi: Machine Learning", ""),
 "ddb16409-f834-4484-9434-c54682526918": ("modul-capstone-kerja.html",        917, "Referensi: Capstone & Kerja", ""),
}
