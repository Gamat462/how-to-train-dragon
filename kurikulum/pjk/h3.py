# -*- coding: utf-8 -*-
"""Hari 3 — aturan khusus yang harus menang: UMKM, batas omzet, klasifikasi basi."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "mat"))
from _gen import kode, tabel, blok
from _sql import muat, keluaran
H = muat(pathlib.Path(__file__).parent / "hasil.json")

L = []
def langkah(judul, *isi):
    L.append({"judul": judul, "isi": "\n".join(isi)})

langkah("Tiga wajib pajak berlabel \"umkm\" — dan satu aturan yang berbeda total",
    blok("aksi", "Berkas <code>senja/pjk-hari-3.sql</code>. Usaha kecil (UMKM) tidak memakai "
                 "tarif berjenjang kemarin — mereka boleh memakai tarif final 0,5% dari "
                 "omzet. Jalankan.", "LAKUKAN"),
    kode("SELECT nama, omzet_tahunan, round(omzet_tahunan * 0.005) AS pajak_umkm_naif\n"
         "FROM pjk_wp WHERE jenis = 'umkm' ORDER BY id;"),
    keluaran(H, "h3_umkm_naif"),
    "<p>Dimas: 4,5 juta. Putri: 16 juta. Agus: 25,5 juta. Semua kelihatan wajar — satu "
    "aturan, satu tarif, tidak ada tulisan merah.</p>")

langkah("Satu angka yang belum kamu periksa: batas omzetnya",
    blok("aksi", "Tarif final UMKM cuma berlaku sampai omzet Rp 4,8 miliar/tahun — di atas "
                 "itu, aturannya kembali ke tarif berjenjang biasa. Jalankan.", "LAKUKAN"),
    kode("SELECT nama, omzet_tahunan, omzet_tahunan > 4800000000 AS lewat_batas_umkm\n"
         "FROM pjk_wp WHERE jenis = 'umkm' ORDER BY id;"),
    keluaran(H, "h3_cek_lewat_batas"),
    blok("bahaya", "<strong>Agus lewat batas.</strong> Kolom <code>jenis</code>-nya masih "
                   "berbunyi <code>umkm</code>, tapi omzetnya Rp 5,1 miliar — angka itu "
                   "berubah sejak label <code>umkm</code>-nya ditulis, dan tidak ada yang "
                   "memperbarui labelnya."))

langkah("Kalau kamu percaya label itu mentah-mentah",
    blok("aksi", "Ini yang terjadi kalau kamu menghitung Agus seperti dua langkah lalu — "
                 "cuma memakai kolom <code>jenis</code>, tanpa mengecek batas.", "LAKUKAN"),
    kode("SELECT nama, jenis, omzet_tahunan,\n"
         "  CASE WHEN jenis = 'umkm' THEN round(omzet_tahunan * 0.005)\n"
         "       ELSE NULL END AS pajak_umkm_tanpa_cek_batas\n"
         "FROM pjk_wp WHERE nama = 'Agus';"),
    keluaran(H, "h3_diam_tanpa_cek_batas"),
    "<p>25,5 juta. Kelihatan sama seperti Dimas dan Putri tadi — konsisten, rapi, dan "
    "jauh lebih rendah dari yang seharusnya.</p>")

langkah("Hitung yang benar untuk Agus: kembali ke tarif berjenjang",
    blok("aksi", "Karena lewat batas, Agus dihitung persis seperti Sari dan Maya kemarin — "
                 "progresif, dari penghasilannya, bukan dari omzetnya. Jalankan.", "LAKUKAN"),
    kode("WITH potong AS (\n"
         "  SELECT w.nama, l.tarif,\n"
         "    GREATEST(0, LEAST(w.penghasilan_tahunan,\n"
         "      COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian\n"
         "  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah\n"
         "  WHERE w.nama = 'Agus')\n"
         "SELECT nama, round(sum(bagian * tarif)) AS pajak_benar FROM potong GROUP BY nama;"),
    keluaran(H, "h3_agus_progresif"),
    blok("bahaya", "<strong>238 juta — sembilan koma tiga kali lipat</strong> dari 25,5 juta "
                   "tadi. Bukan salah hitung kecil; ini beda urutan besaran, dari satu "
                   "klasifikasi yang tidak diperbarui."))

langkah("Kenapa ini persis \"precedence and exceptions\" yang disebut lowongan",
    blok("aksi", "Baca sekali.", "LAKUKAN"),
    blok("hasil", "<p>Ada <strong>tiga tingkat aturan</strong>, dan urutannya menentukan "
                  "segalanya: (1) apakah <code>umkm</code>, (2) <em>kalau ya</em>, apakah "
                  "omzetnya masih di bawah batas, (3) <em>kalau tidak keduanya</em>, kembali "
                  "ke tarif berjenjang biasa.</p>", "TIGA TINGKAT ATURAN"),
    "<p>Aturan khusus (UMKM) <strong>tidak otomatis menang</strong> — ia menang <em>dengan "
    "syarat</em>. Melewatkan syaratnya bukan bug kecil; ia membalikkan hasilnya "
    "sepuluh kali lipat.</p>")

langkah("Tulis ketiga tingkat itu jadi satu query",
    blok("aksi", "Jalankan.", "LAKUKAN"),
    kode("WITH potong AS (\n"
         "  SELECT w.id, w.nama, w.jenis, w.omzet_tahunan,\n"
         "    GREATEST(0, LEAST(w.penghasilan_tahunan,\n"
         "      COALESCE(l.batas_atas, w.penghasilan_tahunan)) - l.batas_bawah) AS bagian, l.tarif\n"
         "  FROM pjk_wp w JOIN pjk_lapisan l ON w.penghasilan_tahunan > l.batas_bawah),\n"
         "progresif AS (\n"
         "  SELECT id, nama, jenis, omzet_tahunan, round(sum(bagian*tarif)) AS pajak_progresif\n"
         "  FROM potong GROUP BY id, nama, jenis, omzet_tahunan)\n"
         "SELECT nama, jenis,\n"
         "  CASE WHEN jenis='umkm' AND omzet_tahunan <= 4800000000\n"
         "       THEN round(omzet_tahunan*0.005) ELSE pajak_progresif END AS pajak_final,\n"
         "  CASE WHEN jenis='umkm' AND omzet_tahunan <= 4800000000\n"
         "       THEN 'umkm final 0,5% omzet' ELSE 'progresif normal' END AS aturan_dipakai\n"
         "FROM progresif ORDER BY id;"),
    keluaran(H, "h3_final"),
    "<p>Tujuh baris, dua kolom penting: <strong>angkanya</strong>, dan <strong>alasan aturan "
    "mana yang dipakai</strong>. Kolom kedua ini yang sering dilupakan — laporan yang cuma "
    "menampilkan angka tanpa menyebut aturannya tidak bisa diperiksa orang lain.</p>",
    blok("catatan", "Perhatikan <code>CASE WHEN</code>-nya mengecek <strong>dua syarat "
                    "sekaligus</strong> dengan <code>AND</code> — <code>jenis='umkm'</code> "
                    "saja tidak cukup. Ini pola yang akan kamu tulis ulang setiap kali aturan "
                    "khusus punya batas berlaku."))

langkah("Bahasa audit untuk temuan ini, kalau kamu menuliskannya di kertas kerja",
    blok("aksi", "Baca sekali — ini jembatan langsung ke pengalamanmu.", "LAKUKAN"),
    blok("hasil", "<p>\"Ditemukan wajib pajak berstatus UMKM dengan omzet melebihi ambang "
                  "batas Rp 4,8 miliar, namun masih dihitung menggunakan tarif final — "
                  "mengakibatkan potensi kurang bayar signifikan. Disarankan validasi "
                  "otomatis pada setiap perhitungan periodik.\"</p>", "KALIMAT TEMUAN"),
    "<p>Itu kalimat yang <strong>sudah bisa kamu tulis</strong>, dari pengalaman KAP-mu. "
    "Bedanya sekarang kamu juga bisa membuktikan temuan itu lewat query, bukan cuma lewat "
    "sampling manual.</p>")

langkah("Draf kalimat CV kedua",
    blok("aksi", "Salin ke catatan lamaranmu.", "LAKUKAN"),
    blok("hasil", "<p>\"Merancang dan menguji logika precedence bertingkat (klasifikasi → "
                  "syarat batas → aturan default) di SQL untuk skenario penghitungan pajak "
                  "berjenjang dan tarif final, termasuk kasus klasifikasi kedaluwarsa yang "
                  "menyebabkan selisih hingga 9x.\"</p>", "DRAF CV #2"),
    blok("catatan", "Angka \"9x\" ini bukan hiasan — itu angka yang barusan kamu hitung "
                    "sendiri di langkah 4. Setiap klaim di CV-mu sekarang punya query yang "
                    "membuktikannya."))

HARI3 = {
  "n": "HARI 3", "tab": "3",
  "judul": "Aturan khusus yang harus menang: UMKM, batas omzet, klasifikasi basi",
  "waktu": "± 50 menit",
  "tujuan": "membuktikan sendiri kenapa aturan khusus harus dicek syaratnya sebelum dipakai, "
            "dan menulis logika tiga-tingkat (klasifikasi, syarat, default) dalam satu query.",
  "langkah": L,
  "tutup_judul": "Hari 3 selesai",
  "tutup": "<p><strong>Yang kamu bawa:</strong> label klasifikasi bisa basi sementara "
           "datanya berubah · aturan khusus menang <em>dengan syarat</em>, bukan otomatis · "
           "mempercayai label tanpa cek batas membuat Agus dihitung 9,3x terlalu rendah · "
           "satu <code>CASE WHEN</code> dengan syarat ganda menutup ketiga tingkat aturan "
           "sekaligus.</p>"
           "<p style=\"margin-top:8px\">Besok: bahasa lowongan untuk hal yang paling kuat "
           "sudah kamu kuasai — validasi dengan <em>golden dataset</em>.</p>",
}
