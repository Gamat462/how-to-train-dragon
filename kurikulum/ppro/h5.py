# -*- coding: utf-8 -*-
"""Hari 5 — vektorisasi, dan kapan .apply boleh dibiarkan."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Siapkan alat ukurnya",
    blok("aksi", "Lanjutkan di sesi yang sama dengan Hari 4 (<code>d2</code> masih hidup). "
                 "Kalau sudah ditutup, jalankan ulang langkah 4 Hari 4 dulu.", "LAKUKAN"),
    kode('''import time
kecil = d2.head(50_000).copy()

def ukur(f, n=3):
    w = []
    for _ in range(n):
        t = time.perf_counter(); hasil = f(); w.append(time.perf_counter() - t)
    return min(w), hasil

print(len(kecil), "baris siap")'''),
    blok("hasil", "<pre><code>50000 baris siap</code></pre>", "HARUS MUNCUL"),
    "<p>Kita mulai dari 50.000 baris supaya tiap percobaan selesai dalam sekejap. "
    "800.000 menyusul di langkah 6.</p>")

langkah("Cara pertama: perulangan Python biasa",
    blok("aksi", "Tugasnya: hitung PPN 11% lalu bulatkan.", "LAKUKAN"),
    kode('''t1, h1 = ukur(lambda: [round(v*0.11) for v in kecil["nilai"].tolist()])
print(f"  list comprehension : {t1*1000:8.1f} ms")'''),
    blok("hasil", "<pre><code>  list comprehension :      4.5 ms</code></pre>", "HARUS MUNCUL"),
    "<p>4,5 milidetik. Ini pembandingmu — tulis angka yang kamu dapat, bukan angkaku, karena "
    "empat langkah berikutnya membandingkan ke situ.</p>")

langkah("Cara kedua: itertuples, yang katanya “cara benar”",
    blok("aksi", "Ini yang paling sering diajarkan untuk mengulang DataFrame.", "LAKUKAN"),
    kode('''t2, _ = ukur(lambda: [round(r.nilai*0.11) for r in kecil.itertuples()])
print(f"  itertuples         : {t2*1000:8.1f} ms")'''),
    blok("hasil", "<pre><code>  itertuples         :     57.2 ms</code></pre>", "HARUS MUNCUL"),
    "<p><strong>57,2 ms — dua belas kali lebih lambat</strong> daripada perulangan Python biasa "
    "yang baru kamu ukur. Yang sering kamu temui diajarkan sebagai “cara benar mengulang "
    "DataFrame” justru yang paling mahal, karena tiap baris dibungkus jadi objek dulu.</p>")

langkah("Cara ketiga: .apply",
    blok("aksi", "Yang paling sering kamu tulis sendiri.", "LAKUKAN"),
    kode('''t3, _ = ukur(lambda: kecil["nilai"].apply(lambda v: round(v*0.11)))
print(f"  .apply(lambda)     : {t3*1000:8.1f} ms")'''),
    blok("hasil", "<pre><code>  .apply(lambda)     :     12.6 ms</code></pre>", "HARUS MUNCUL"),
    "<p>12,6 ms. Lebih cepat daripada <code>itertuples</code>, lebih lambat daripada perulangan "
    "biasa. Belum ada yang mengesankan — dan kalau kamu berhenti di sini, kamu akan menyimpulkan "
    "bahwa keempat caranya sama saja.</p>")

langkah("Cara keempat: hapus perulangannya",
    blok("aksi", "Perhatikan: tidak ada <code>for</code>, tidak ada <code>lambda</code>.", "LAKUKAN"),
    kode('''t4, h4 = ukur(lambda: (kecil["nilai"]*0.11).round())
print(f"  vektorisasi        : {t4*1000:8.1f} ms   <- {t3/t4:.0f}x lebih cepat dari .apply")
print("  hasil sama?", int(sum(h1)) == int(h4.sum()))'''),
    blok("hasil", "<pre><code>  vektorisasi        :      0.1 ms   <- 88x lebih cepat dari .apply\n"
                  "  hasil sama? True</code></pre>", "HARUS MUNCUL"),
    "<p>Empat cara, satu jawaban, dan rentangnya <strong>0,1 ms sampai 57,2 ms</strong>. "
    "Kamu menulis keempatnya dalam sepuluh menit; bedanya lima ratus kali lipat.</p>")

langkah("Di 800.000 baris, jaraknya melebar",
    blok("aksi", "Sekarang di data penuh. Yang pertama butuh sepersekian detik — sabar.", "LAKUKAN"),
    kode('''t8, _ = ukur(lambda: d2["nilai"].apply(lambda v: round(v*0.11)), n=1)
t9, _ = ukur(lambda: (d2["nilai"]*0.11).round(), n=3)
print(f"  .apply      : {t8:8.2f} detik")
print(f"  vektorisasi : {t9*1000:8.1f} ms   <- {t8/t9:.0f}x lebih cepat")'''),
    blok("hasil", "<pre><code>  .apply      :     0.34 detik\n"
                  "  vektorisasi :      1.4 ms   <- 248x lebih cepat</code></pre>", "HARUS MUNCUL"),
    "<p>88 kali di 50.000 baris, <strong>248 kali di 800.000</strong>. Selisihnya makin lebar "
    "seiring datanya membesar — persis seperti subquery berkorelasi di SQL Mahir L4.</p>")

langkah("Kenapa begitu",
    blok("aksi", "Baca dua kalimat, lalu lanjut.", "LAKUKAN"),
    blok("hasil", "<p><code>.apply()</code> memanggil fungsi Python-mu sekali untuk "
                  "<strong>tiap baris</strong> — 800.000 panggilan, masing-masing dengan biaya "
                  "tetapnya sendiri. <code>(kolom * 0.11)</code> menyerahkan seluruh kolom ke "
                  "kode C yang mengerjakannya sekaligus.</p>", "SEBABNYA"),
    "<p><strong>Bukan Python-nya yang lambat; yang mahal adalah bolak-baliknya.</strong></p>")

langkah("Sekarang bagian yang jujur: kapan .apply boleh dibiarkan",
    blok("aksi", "Tugas yang berbeda — penggolongan bersyarat, bukan aritmetika.", "LAKUKAN"),
    kode('''def kat(v):
    if v < 30000:  return "kecil"
    if v < 80000:  return "sedang"
    return "besar"

t5, _ = ukur(lambda: kecil["nilai"].apply(kat))
print(f"  .apply(fungsi) : {t5*1000:8.1f} ms")'''),
    blok("hasil", "<pre><code>  .apply(fungsi) :      6.8 ms</code></pre>", "HARUS MUNCUL"),
    "<p>Ini bentuk yang <em>tidak</em> bisa ditulis sebagai satu perkalian. Sekarang bandingkan "
    "dengan dua penggantinya.</p>")

langkah("Dua cara menggantinya, dan selisihnya",
    blok("aksi", "Jalankan dua-duanya.", "LAKUKAN"),
    kode('''import numpy as np
t6, _ = ukur(lambda: pd.Series(np.select(
        [kecil["nilai"]<30000, kecil["nilai"]<80000], ["kecil","sedang"], "besar")))
t7, _ = ukur(lambda: pd.cut(kecil["nilai"], [-1,29999,79999,10**9],
                            labels=["kecil","sedang","besar"]))
print(f"  np.select      : {t6*1000:8.1f} ms   <- {t5/t6:.1f}x")
print(f"  pd.cut         : {t7*1000:8.1f} ms   <- {t5/t7:.1f}x")'''),
    blok("hasil", "<pre><code>  np.select      :      5.5 ms   <- 1.2x\n"
                  "  pd.cut         :      1.5 ms   <- 4.7x</code></pre>", "HARUS MUNCUL"),
    "<p><strong>Cuma 1,2 kali</strong> untuk <code>np.select</code>. Bukan 248. Dan harganya "
    "kode yang jauh lebih sulit dibaca.</p>")

langkah("Aturannya, dalam dua baris",
    blok("aksi", "Tulis ini di catatanmu.", "LAKUKAN"),
    tabel(["Bentuk pekerjaannya", "Yang dilakukan", "Untungnya"],
          [["Aritmetika — kali, bagi, tambah, bulatkan",
            "<strong>ganti</strong> <code>.apply</code> dengan operasi kolom",
            "ratusan kali"],
           ["Logika bercabang yang sulit divektorkan",
            "<strong>biarkan</strong> <code>.apply</code>, kecuali <code>pd.cut</code> pas",
            "1,2 kali — tidak sepadan"]]),
    "<p>Jadi aturannya <strong>bukan</strong> “jangan pernah pakai <code>.apply</code>”. "
    "Menukar keterbacaan demi 1,2 kali adalah pertukaran yang merugi.</p>",
    blok("catatan", "<code>pd.cut</code> menang 4,7 kali <em>dan</em> lebih mudah dibaca — "
                    "untuk penggolongan berdasarkan rentang angka, ia hampir selalu pilihan "
                    "terbaik. Kalau syaratnya bukan rentang, ia tidak bisa dipakai."))

langkah("Aturan di atas semua aturan",
    blok("aksi", "Baca sekali, lalu simpan fungsi <code>ukur()</code> tadi.", "LAKUKAN"),
    blok("hasil", "<p>Kalau kode lambatmu jalan <strong>6,8 ms</strong>, mempercepatnya 4 kali "
                  "menghemat 5 milidetik. Tidak ada artinya.</p>", "UKUR DULU"),
    "<p>Optimasi yang tidak diukur adalah menebak, dan menebak menghabiskan waktumu di tempat "
    "yang salah. <strong>Fungsi <code>ukur()</code> sepuluh baris tadi cukup untuk seluruh "
    "karier analismu.</strong></p>")

langkah("Ulangi dari ingatan",
    blok("aksi", "Tutup halaman ini. Jawab di kertas.", "LAKUKAN"),
    kode("""1. Dari empat cara tadi, mana yang paling lambat?
2. Untuk pekerjaan apa .apply harus diganti, dan untuk apa dibiarkan?
3. Kenapa .apply lambat?
4. Apa yang harus dilakukan sebelum mengoptimasi apa pun?""", salin=False),
    "<details><summary>Buka kunci jawaban</summary>"
    "<p>1. <code>itertuples</code> — 57,2 ms, lebih lambat daripada semuanya. "
    "2. Ganti untuk <strong>aritmetika</strong> (untungnya ratusan kali); biarkan untuk "
    "<strong>logika bercabang</strong> (untungnya 1,2 kali). "
    "3. Ia memanggil fungsi Python sekali per baris; yang mahal adalah bolak-baliknya. "
    "4. <strong>Ukur.</strong></p></details>")

HARI5 = {
  "n": "HARI 5",
  "tab": "5",
  "judul": "248 kali lebih cepat, dengan menghapus satu kata",
  "waktu": "± 60 menit",
  "tujuan": "mengenali kapan <code>.apply()</code> harus diganti, dan — sama pentingnya — "
            "kapan tidak perlu.",
  "langkah": L,
  "tutup_judul": "Hari 5 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> dua angka yang saling menyeimbangkan — "
           "<strong>248×</strong> untuk aritmetika dan <strong>1,2×</strong> untuk logika "
           "bercabang — jadi kamu tidak akan menerapkan nasihat “jangan pakai .apply” secara "
           "membabi buta.</p>"
           "<p style=\"margin-top:8px\">Dan satu fungsi <code>ukur()</code> yang membuatmu tidak "
           "pernah lagi mengoptimasi berdasarkan perasaan.</p>"
           "<p style=\"margin-top:8px\">Besok: berkas yang <strong>tidak muat</strong> di memori.</p>",
}
