import os, html, pathlib
os.chdir('/tmp/claude-0/-home-user-how-to-train-dragon/10410e99-6fc8-5544-93e1-5420df84173a/scratchpad')
exec(open('_urutan.py').read())
OUT = pathlib.Path("paket/Rute-Data-Analyst")

# hitung minggu tiap modul dari aritmetika, bukan diketik
baris, cum = [], 0
for slug, judul, h, f, catatan in URUTAN:
    mulai_hk = -(-cum // 2) + 1
    cum += h
    selesai_hk = -(-cum // 2)
    baris.append(dict(slug=slug, judul=judul, hari=h, fase=f, catatan=catatan,
                      mg_mulai=-(-mulai_hk // 5), mg_selesai=-(-selesai_hk // 5), kum=cum))
TOTAL = cum
MINGGU = baris[-1]["mg_selesai"]

def esc(s): return html.escape(s, quote=False)

bagian = []
for f in sorted(FASE):
    nama, jual = FASE[f]
    isi = [b for b in baris if b["fase"] == f]
    mg = f"minggu {isi[0]['mg_mulai']}–{isi[-1]['mg_selesai']}"
    hari = sum(b["hari"] for b in isi)
    rows = []
    for b in isi:
        cat = f'<div class="cat">{esc(b["catatan"])}</div>' if b["catatan"] else ""
        rows.append(f'''    <li>
      <a href="kurikulum/{b["slug"]}.html">
        <span class="judul">{esc(b["judul"])}</span>
        <span class="meta">{b["hari"]} hari materi · minggu {b["mg_mulai"]}{"" if b["mg_mulai"]==b["mg_selesai"] else "–"+str(b["mg_selesai"])}</span>
      </a>
      {cat}
    </li>''')
    bagian.append(f'''  <section class="fase">
    <div class="fase-head">
      <span class="no">Fase {f}</span>
      <h2>{esc(nama)}</h2>
      <span class="rentang">{mg} · {hari} hari materi</span>
    </div>
    <p class="jual"><strong>Di ujung fase ini sudah bisa kamu jual:</strong> {esc(jual)}</p>
    <ol class="daftar">
{chr(10).join(rows)}
    </ol>
  </section>''')

HTML = f'''<!doctype html>
<html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mulai di Sini — Rute Data Analyst</title>
<style>
:root{{
  --bg:#F3EFE4; --surface:#FDFBF5; --surface-2:#EAE2CC;
  --ink:#1C2430; --ink-soft:#5B6472; --line:#DCD3B9;
  --teal:#0F6E63; --teal-soft:#E1EEEA; --gold:#9C6B25; --gold-soft:#F1E4C8;
  --alert:#A33A2A; --alert-soft:#F6E2DD;
}}
@media (prefers-color-scheme: dark){{ :root{{
  --bg:#12161D; --surface:#1A2029; --surface-2:#212939;
  --ink:#EDE9DD; --ink-soft:#98A2B3; --line:#303A4B;
  --teal:#5BCBB7; --teal-soft:rgba(91,203,183,.14);
  --gold:#E0AE5F; --gold-soft:rgba(224,174,95,.14);
  --alert:#E88A76; --alert-soft:rgba(232,138,118,.14);
}} }}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);padding:32px 18px 70px;line-height:1.6;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,system-ui,sans-serif}}
.page{{max-width:880px;margin:0 auto;background:var(--surface);border:1px solid var(--line);
 border-radius:20px;padding:38px 40px 44px;box-shadow:0 24px 48px -30px rgba(0,0,0,.28)}}
@media(max-width:600px){{.page{{padding:24px 18px 30px}}}}
h1,h2,h3{{margin:0;font-family:Georgia,"Times New Roman",serif;text-wrap:balance}}
h1{{font-size:clamp(1.8rem,5vw,2.4rem)}}
p{{margin:0}}
.eyebrow{{font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:9px}}
.lede{{margin-top:12px;color:var(--ink-soft);max-width:64ch}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:24px 0 8px}}
@media(max-width:600px){{.stats{{grid-template-columns:repeat(2,1fr)}}}}
.stat{{background:var(--teal-soft);border-radius:12px;padding:12px 14px}}
.stat b{{display:block;font-size:1.35rem;color:var(--teal);font-variant-numeric:tabular-nums}}
.stat span{{font-size:.76rem;color:var(--ink-soft)}}
.kotak{{border:1px solid var(--line);border-radius:12px;padding:14px 17px;margin-top:18px;font-size:.92rem;color:var(--ink-soft)}}
.kotak strong{{color:var(--ink)}}
.kotak.penting{{background:var(--alert-soft);border-color:transparent}}
.kotak.penting strong{{color:var(--alert)}}
.kotak.info{{background:var(--gold-soft);border-color:transparent}}
.kotak.info strong{{color:var(--gold)}}
.fase{{margin-top:34px}}
.fase-head{{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap;padding-bottom:8px;border-bottom:1px solid var(--line)}}
.fase-head .no{{font-family:ui-monospace,monospace;font-size:.7rem;letter-spacing:.07em;
 text-transform:uppercase;color:var(--gold);background:var(--gold-soft);padding:3px 9px;border-radius:999px}}
.fase-head h2{{font-size:1.2rem;flex:1}}
.fase-head .rentang{{font-family:ui-monospace,monospace;font-size:.76rem;color:var(--ink-soft)}}
.jual{{font-size:.88rem;color:var(--ink-soft);margin-top:10px}}
.jual strong{{color:var(--teal)}}
ol.daftar{{list-style:none;counter-reset:d;margin:14px 0 0;padding:0;display:flex;flex-direction:column;gap:8px}}
ol.daftar li{{counter-increment:d;background:var(--surface-2);border:1px solid var(--line);border-radius:11px;padding:12px 15px}}
ol.daftar a{{display:grid;grid-template-columns:30px 1fr auto;gap:12px;align-items:baseline;
 text-decoration:none;color:inherit}}
ol.daftar a::before{{content:counter(d);font-family:ui-monospace,monospace;font-size:.74rem;color:var(--teal)}}
ol.daftar a:hover .judul{{color:var(--teal);text-decoration:underline}}
.judul{{font-weight:600;font-size:.99rem}}
.meta{{font-family:ui-monospace,monospace;font-size:.72rem;color:var(--ink-soft);white-space:nowrap}}
@media(max-width:600px){{ol.daftar a{{grid-template-columns:24px 1fr}} .meta{{grid-column:2;white-space:normal}}}}
.cat{{font-size:.85rem;color:var(--ink-soft);margin:7px 0 0 42px}}
@media(max-width:600px){{.cat{{margin-left:36px}}}}
table{{width:100%;border-collapse:collapse;font-size:.87rem;margin-top:12px}}
th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
thead th{{background:var(--surface-2);font-family:ui-monospace,monospace;font-size:.68rem;
 letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft)}}
.bungkus{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;margin-top:12px}}
code{{font-family:ui-monospace,monospace;font-size:.87em;background:var(--surface-2);padding:2px 6px;border-radius:5px}}
a{{color:var(--teal)}}
footer{{margin-top:38px;padding-top:20px;border-top:1px solid var(--line);font-size:.85rem;color:var(--ink-soft)}}
</style></head><body>
<div class="page">

<header>
  <span class="eyebrow">Paket lengkap · offline · {len(URUTAN)+3} modul</span>
  <h1>Mulai di sini</h1>
  <p class="lede">Ini urutan membukanya, dari berkas pertama sampai terakhir. Semua tautan di halaman ini menunjuk ke berkas di dalam folder yang sama — <strong>jalan tanpa internet</strong>. Kemajuan centangmu tersimpan di browser, jadi buka lewat browser yang sama tiap kali.</p>

  <div class="stats">
    <div class="stat"><b>{TOTAL}</b><span>hari materi</span></div>
    <div class="stat"><b>{MINGGU}</b><span>minggu penuh waktu</span></div>
    <div class="stat"><b>{len(URUTAN)}</b><span>modul berurutan</span></div>
    <div class="stat"><b>12</b><span>hari freelance paralel</span></div>
  </div>

  <div class="kotak penting">
    <strong>Baca ini dulu, satu menit.</strong> Jangan buka berdasarkan yang paling menarik — buka berdasarkan nomor. Urutan ini bukan selera: <em>Bekal Data Klien</em> memakai pandas dari M3, <em>Studi Kasus</em> memakai pandas dari Bekal Data Klien, <em>SQL Mahir</em> memakai window function dari M6, dan <em>Bekal Rahasia Klien</em> harus selesai <strong>sebelum</strong> M8 menyuruhmu memublikasikan dashboard ke internet. Melompat berarti menabrak tembok, dan temboknya tidak akan memberitahumu bahwa penyebabnya adalah lompatan itu.
  </div>

  <div class="kotak">
    <strong>Ritme hariannya.</strong> Dua "hari materi" per satu hari kerja, lima hari seminggu. Bukan tiga: modul-modul ini punya ulangan berjarak bawaan (ulang +1 hari, +3 hari, +7 hari), dan memampatkannya membuat jaraknya ikut memampat. Kalau ingin lebih cepat, tambah <em>hari</em> (pakai Sabtu), jangan tambah <em>materi per hari</em>. Rinciannya ada di <a href="kurikulum/002-rencana-21-minggu.html">Rencana {MINGGU} Minggu</a>.
  </div>
</header>

{chr(10).join(bagian)}

<section class="fase">
  <div class="fase-head">
    <span class="no">Paralel</span>
    <h2>Dikerjakan berbarengan, bukan sesudahnya</h2>
    <span class="rentang">mulai minggu 5</span>
  </div>
  <p class="jual"><strong>Kenapa paralel:</strong> mencari klien butuh waktu berminggu-minggu untuk berbuah. Kalau baru dimulai setelah semua materi selesai, kamu menunda pemasukan lima bulan tanpa alasan.</p>
  <ol class="daftar">
    <li>
      <a href="kurikulum/080-jalur-freelance.html">
        <span class="judul">Jalur Freelance — dari nol klien sampai dibayar</span>
        <span class="meta">12 hari · 1 hari/minggu</span>
      </a>
      <div class="cat">Satu hari freelance tiap minggu, mulai minggu ke-5, di slot 15.30–16.30. Sebelum minggu 5, pakai slot itu untuk menambah proyek portofolio.</div>
    </li>
  </ol>
</section>

<section class="fase">
  <div class="fase-head">
    <span class="no">Navigasi</span>
    <h2>Dua dokumen yang dibuka berulang, bukan sekali</h2>
    <span class="rentang">rujukan</span>
  </div>
  <ol class="daftar">
    <li>
      <a href="kurikulum/001-indeks-rute.html">
        <span class="judul">Indeks Rute — peta semua modul</span>
        <span class="meta">rujukan</span>
      </a>
      <div class="cat">Deskripsi tiap modul beserta isinya. Berguna kalau kamu lupa modul mana yang membahas sesuatu.</div>
    </li>
    <li>
      <a href="kurikulum/002-rencana-21-minggu.html">
        <span class="judul">Rencana {MINGGU} Minggu + jadwal harian</span>
        <span class="meta">rujukan</span>
      </a>
      <div class="cat">Lima fase, jam per jam satu hari kerja, dan pemetaan kemampuan KAP-mu ke hari-hari modulnya.</div>
    </li>
  </ol>
</section>

<section class="fase">
  <div class="fase-head">
    <span class="no">Catatan</span>
    <h2>Tiga hal yang perlu kamu putuskan sendiri</h2>
  </div>

  <div class="kotak info">
    <strong>1. SQL Mahir boleh ditarik maju.</strong> Fase 5 ada di akhir karena urutan itu paling aman untuk mengejar penghasilan lebih dulu. Tapi kalau kamu mengincar posisi kantoran dan tes SQL-nya sudah di depan mata, kerjakan <strong>SQL Mahir L1–L3</strong> tepat setelah M6 — di situ window function baru diajarkan. Konsekuensinya jujur: 21 hari materi pindah ke depan, jadi fase 3 dan 4 mundur sekitar dua minggu, dan titik "bisa dibayar" ikut mundur.
  </div>

  <div class="kotak info">
    <strong>2. Jalur migas boleh dilewati — tapi pikirkan dulu.</strong> Tiga puluh lima hari itu spesialisasi, bukan dasar. Kalau kamu tidak berminat ke industri migas, waktunya bisa dipakai untuk proyek portofolio lain. Tapi ini satu-satunya bagian di seluruh rute yang membuat latar KAP-mu jadi <em>keunggulan</em> dan bukan sekadar masa lalu — ceruknya sempit, saingannya sedikit, dan tarifnya jauh di atas pekerjaan dashboard umum.
  </div>

  <div class="kotak info">
    <strong>3. Modul referensi tidak masuk urutan, dan memang begitu.</strong> Berkas <code>9xx-*</code> di folder <code>kurikulum/</code> adalah versi awal rencana ini dan delapan modul referensi bertopik. Isinya masih berguna sebagai bacaan pendalaman, tapi <strong>jadwalnya sudah tidak berlaku</strong> — disusun ketika kamu masih bekerja di KAP, dengan tempo paruh waktu 9–12 bulan. Jangan mengikuti jadwal di dalamnya.
  </div>
</section>

<section class="fase">
  <div class="fase-head">
    <span class="no">Isi paket</span>
    <h2>Apa saja yang ada di folder ini</h2>
  </div>
  <div class="bungkus">
    <table>
      <thead><tr><th>Folder / berkas</th><th>Isinya</th></tr></thead>
      <tbody>
        <tr><td><code>MULAI-DI-SINI.html</code></td><td>Halaman ini. Simpan sebagai bookmark.</td></tr>
        <tr><td><code>URUTAN-BELAJAR.md</code></td><td>Urutan yang sama dalam teks polos, untuk dibaca di ponsel atau ditempel di dinding.</td></tr>
        <tr><td><code>kurikulum/</code></td><td>{len(URUTAN)+3} modul utama + arsip &amp; referensi. Nama berkasnya diawali nomor urut, jadi mengurutkan berdasarkan nama = urutan belajar.</td></tr>
        <tr><td><code>data-dan-skrip/sql-mahir/</code></td><td>Pembuat <code>senja.db</code> dan <code>besar.db</code> (800.000 baris), plus berkas uji mutu data.</td></tr>
        <tr><td><code>data-dan-skrip/studi-kasus/</code></td><td>Lima pembuat berkas berantakan (<code>gen_k1</code>–<code>gen_k5</code>) dan lima kunci jawabannya.</td></tr>
        <tr><td><code>data-dan-skrip/bekal-data-klien/</code></td><td>Berkas Excel klien contoh beserta pembuatnya dan hasil bersihnya.</td></tr>
        <tr><td><code>data-dan-skrip/bootcamp-jalur-utama/</code></td><td>Data CSV untuk M1–M15 dan jalur migas, bank soal, kunci jawaban, dan kamus data.</td></tr>
      </tbody>
    </table>
  </div>
  <div class="kotak">
    <strong>Skrip-skrip itu tidak perlu kamu jalankan lebih dulu.</strong> Tiap modul menyisipkan kode pembuat datanya sendiri di langkah pertama, jadi kamu akan mengetik atau menyalinnya di tempat. Salinan di <code>data-dan-skrip/</code> ada supaya kamu bisa membandingkan kalau hasilmu tidak sama — dan karena semua pembuat memakai angka acak berkunci tetap, <strong>hasilmu harus sama persis dengan yang tertulis di modul.</strong> Kalau beda, ada yang salah ketik, dan kamu punya berkas pembandingnya.
  </div>
</section>

<footer>
  <p><strong>Satu kebiasaan yang berlaku di seluruh {TOTAL} hari ini:</strong> tiap angka yang muncul di modul-modul ini dihasilkan dengan menjalankan kodenya sungguhan, bukan dari ingatan. Kalau angka di layarmu berbeda dari angka di modul, salah satunya salah — dan kamu selalu punya datanya untuk membuktikan yang mana. Bawa kebiasaan itu ke pekerjaanmu; itu bagian yang paling sulit ditiru orang.</p>
</footer>

</div></body></html>
'''
(OUT / "MULAI-DI-SINI.html").write_text(HTML)
print("MULAI-DI-SINI.html:", len(HTML), "bytes |", TOTAL, "hari |", MINGGU, "minggu")

# --- versi teks polos ---
md = [f"# RUTE DATA ANALYST — URUTAN BELAJAR\n",
      f"{TOTAL} hari materi · {MINGGU} minggu penuh waktu · 2 hari materi per hari kerja, 5 hari seminggu\n",
      "Buka berdasarkan nomor, bukan berdasarkan yang paling menarik.",
      "Nama berkas di folder kurikulum/ diawali nomor urut, jadi mengurutkan berdasarkan nama = urutan belajar.\n"]
for f in sorted(FASE):
    nama, jual = FASE[f]
    isi = [b for b in baris if b["fase"] == f]
    md.append(f"\n## FASE {f} — {nama}  (minggu {isi[0]['mg_mulai']}–{isi[-1]['mg_selesai']}, {sum(b['hari'] for b in isi)} hari)")
    md.append(f"Di ujung fase ini bisa dijual: {jual}\n")
    for n, b in enumerate(isi, 1):
        md.append(f"{n:2d}. [{b['hari']} hari · minggu {b['mg_mulai']}-{b['mg_selesai']}] {b['judul']}")
        md.append(f"      kurikulum/{b['slug']}.html")
        if b["catatan"]: md.append(f"      -> {b['catatan']}")
md.append("\n\n## PARALEL — mulai minggu 5, satu hari tiap minggu")
md.append("    Jalur Freelance (12 hari)  ->  kurikulum/080-jalur-freelance.html")
md.append("    Dikerjakan di slot 15.30-16.30 tiap hari kerja, bukan setelah semua materi selesai.")
md.append("\n\n## NAVIGASI — dibuka berulang")
md.append("    Indeks Rute            ->  kurikulum/001-indeks-rute.html")
md.append(f"    Rencana {MINGGU} Minggu      ->  kurikulum/002-rencana-21-minggu.html")
md.append("\n\n## CATATAN")
md.append("1. SQL Mahir (fase 5) boleh ditarik maju ke setelah M6 kalau tes SQL sudah di depan mata.")
md.append("   Konsekuensinya: 21 hari materi pindah ke depan, fase 3 dan 4 mundur ~2 minggu.")
md.append("2. Jalur migas (35 hari) boleh dilewati, tapi itu satu-satunya bagian yang membuat")
md.append("   latar KAP jadi keunggulan, bukan sekadar masa lalu.")
md.append("3. Berkas 9xx-* adalah arsip dan referensi. Isinya berguna, jadwalnya TIDAK berlaku.")
(OUT / "URUTAN-BELAJAR.md").write_text("\n".join(md) + "\n")
print("URUTAN-BELAJAR.md ditulis")
