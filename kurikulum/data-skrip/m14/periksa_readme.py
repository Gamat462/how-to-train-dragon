"""Pemeriksa README proyek portofolio (Minggu 14 Hari 93).

Cara pakai:
    python periksa_readme.py README.md

Yang diperiksa bukan selera, tapi hal-hal yang bisa dihitung: apakah judulnya
memuat angka (tanda ia berisi temuan, bukan nama dataset), apakah ada tautan
hidup, gambar, bagian Data, dan bagian Batasan.
"""
import re
import sys

def periksa(md):
    baris = [b.rstrip() for b in md.splitlines()]
    judul = next((b for b in baris if b.startswith("# ")), "")
    rendah = md.lower()
    tautan = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", md)
    gambar = re.findall(r"!\[[^\]]*\]\([^)]+\)", md)
    temuan = [b for b in baris if re.match(r"^\s*(\d+\.|[-*])\s", b) and re.search(r"\d", b)]

    return [
        ("ada judul H1", bool(judul), judul[:60] or "tidak ada baris '# '"),
        ("judul memuat angka", bool(re.search(r"\d", judul)),
         "judul temuan biasanya berangka, mis. '61% harga ditentukan lokasi'"),
        ("judul bukan 'analisis X'", not re.match(r"^#\s*(analisis|analysis)\b", judul, re.I),
         "judul yang dimulai 'Analisis ...' adalah nama dataset, bukan temuan"),
        ("tautan hidup", len(tautan) >= 1, f"{len(tautan)} tautan http ditemukan"),
        ("tautan di paruh atas", any(t in "\n".join(baris[:12]) for t in tautan) if tautan else False,
         "tautan dashboard harus terlihat tanpa menggulung layar"),
        ("gambar", len(gambar) >= 1, f"{len(gambar)} gambar ditemukan"),
        ("temuan berangka", len(temuan) >= 3, f"{len(temuan)} poin berangka (target 3)"),
        ("bagian Data", "## data" in rendah, "menjelaskan sumber, jumlah baris, apa yang rusak"),
        ("bagian Batasan", "## batasan" in rendah or "## limitations" in rendah,
         "bagian yang hampir tidak pernah ditulis pelamar lain"),
        ("cara menjalankan", "## menjalankan" in rendah or "## cara" in rendah or "```" in md,
         "perintah yang benar-benar berhasil dijalankan orang lain"),
    ]

def main():
    if len(sys.argv) < 2:
        print("pakai: python periksa_readme.py README.md")
        raise SystemExit(2)
    hasil = periksa(open(sys.argv[1], encoding="utf-8").read())
    for nama, ok, ket in hasil:
        print(f"[{'OK ' if ok else 'CEK'}] {nama:24} {ket}")
    lolos = sum(1 for _, ok, _ in hasil if ok)
    print(f"\nlolos {lolos} dari {len(hasil)} pemeriksaan")
    raise SystemExit(0 if lolos == len(hasil) else 1)

if __name__ == "__main__":
    main()
