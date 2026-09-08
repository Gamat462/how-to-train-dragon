"""Menghitung skor rubrik keputusan S2 (Jalur S2, Hari 7).

Buat berkas jawaban.txt berisi delapan baris Y atau T (satu per pernyataan),
lalu jalankan:

    python skor_rubrik.py

Isi jawaban.txt dengan jujur. Jangan menjawab Y untuk hal yang "bisa
diusahakan nanti" — rubrik ini menilai keadaanmu hari ini.
"""
import pathlib

PERNYATAAN = [
    (2, "Uang kuliah DAN biaya hidupnya dibayar orang lain (beasiswa penuh)"),
    (1, "Usiaku pada 31 Des tahun depan masih di bawah 33"),
    (1, "Aku mengincar pekerjaan yang benar-benar memfilter 'STEM background'"),
    (1, "Aku ingin bekerja atau menetap di luar negeri, bukan hanya kuliah di sana"),
    (2, "Aku menginginkan riset, S3, atau mengajar"),
    (1, "Aku sudah punya IELTS/TOEFL yang masih berlaku"),
    (1, "Aku sanggup tidak berpenghasilan 12-24 bulan tanpa mengganggu siapa pun"),
    (2, "Aku sudah melamar 20+ posisi analitik audit/risiko dan ditolak karena pendidikan"),
]

BACAAN = [
    (0, 2, "S2 belum menjawab masalahmu",
           "Kerjakan rute dan Jalur Pintu B sampai tuntas dulu."),
    (3, 5, "Lamar beasiswanya, jangan biayai sendiri",
           "Kalau ditolak, tidak ada yang hilang selain waktumu."),
    (6, 11, "S2 masuk akal",
            "Kejar dengan serius, mulai dari yang tenggatnya paling dekat."),
]

def main():
    berkas = pathlib.Path("jawaban.txt")
    if not berkas.exists():
        print("buat dulu jawaban.txt berisi 8 baris Y atau T:\n")
        for i, (poin, teks) in enumerate(PERNYATAAN, 1):
            print(f"  {i}. [{poin} poin] {teks}")
        raise SystemExit(2)

    jawab = [b.strip().upper()[:1] for b in berkas.read_text(encoding="utf-8").splitlines()
             if b.strip()]
    if len(jawab) != len(PERNYATAAN):
        print(f"jawaban.txt berisi {len(jawab)} baris, seharusnya {len(PERNYATAAN)}")
        raise SystemExit(2)

    total = 0
    for (poin, teks), j in zip(PERNYATAAN, jawab):
        dapat = poin if j == "Y" else 0
        total += dapat
        print(f"  [{j}] {dapat:>1}/{poin}  {teks}")

    maks = sum(p for p, _ in PERNYATAAN)
    print(f"\nskor: {total} dari {maks}")
    for bawah, atas, judul, saran in BACAAN:
        if bawah <= total <= atas:
            print(f"bacaan: {judul}")
            print(f"        {saran}")
            break

if __name__ == "__main__":
    main()
