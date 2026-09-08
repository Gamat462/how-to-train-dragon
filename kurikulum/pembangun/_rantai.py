import re, os
exec(open('_peta.py').read()); exec(open('_urutan.py').read()); exec(open('_slug.py').read())
slug2id   = {v: k for k, v in SLUG.items()}
id2berkas = {k: v[0] for k, v in PETA.items()}
INDEKS = "https://claude.ai/code/artifact/e60e0d95-6d7b-4245-ac7a-f23e60237cfd"
urut  = [u[0] for u in URUTAN]
judul = {u[0]: u[1] for u in URUTAN}

def nama_tombol(j):
    """'M6 — SQL Lanjutan' -> 'M6: SQL Lanjutan'.

    Judul modul terpanjang di rute ini 48 karakter, jadi tidak ada yang dipotong.
    Dulu batasnya 42 dan menghasilkan tombol berbunyi 'melamar ke tempat yang…'
    -- terpotong di tengah frasa, dan pembaca tidak tahu ia menuju ke mana.
    Kalau nanti ada judul yang benar-benar kepanjangan, potong di tanda baca,
    jangan di tengah frasa.
    """
    return j.replace(" — ", ": ")

def sisip_sebelum_tutup_blok(teks, penanda, sisipan):
    """Sisipkan tepat sebelum </div> penutup blok TERAKHIR bernama `penanda`."""
    i = teks.rfind(penanda)
    if i < 0: return None
    j, depth = i, 0
    while j < len(teks):
        m = re.compile(r'<(/?)div\b').search(teks, j)
        if not m: return None
        depth += -1 if m.group(1) else 1
        j = m.end()
        if depth == 0:
            k = teks.index('>', m.start()) + 1
            return teks[:m.start()] + sisipan + teks[m.start():]
    return None

diubah = []
for i, slug in enumerate(urut):
    berkas = id2berkas[slug2id[slug]]
    t = open(berkas).read()
    asli = t

    # --- tautan mundur (modul pertama -> indeks) ---
    sebelum = INDEKS if i == 0 else "https://claude.ai/code/artifact/" + slug2id[urut[i-1]]
    label   = "indeks rute" if i == 0 else nama_tombol(judul[urut[i-1]])
    blok_mundur = f'<div class="kembali"><a href="{sebelum}">← Kembali ke {label}</a></div>'
    if 'class="kembali"' not in t:
        # Jangan ditempel di posisi 0 -- di sana ia mendarat SEBELUM <style>,
        # jadi tampil sebagai tautan telanjang di atas judul halaman.
        # Modul minggu-pertama pernah begitu selama berminggu-minggu.
        if '</style>' in t:
            t = t.replace('</style>\n', '</style>\n\n' + blok_mundur + '\n', 1)
        else:
            t = blok_mundur + '\n\n' + t
    else:
        # timpa yang lama supaya sasarannya selalu benar
        t = re.sub(r'<div class="kembali">.*?</div>', lambda m: blok_mundur, t, count=1, flags=re.S)

    # --- tombol maju ---
    if True:
        if i + 1 < len(urut):
            href, teks_tombol = "https://claude.ai/code/artifact/" + slug2id[urut[i+1]], \
                                f"Lanjut ke {nama_tombol(judul[urut[i+1]])} →"
        else:
            href, teks_tombol = INDEKS, "Seluruh rute selesai — kembali ke indeks →"
        tombol = f'      <a class="lanjut" href="{href}">{teks_tombol}</a>\n'
        if 'class="lanjut"' in t:
            # sudah ada: timpa href dan teksnya, jangan menambah tombol kedua
            t = re.sub(r'<a class="lanjut"[^>]*>.*?</a>',
                       lambda m: tombol.strip(), t, count=1, flags=re.S)
            baru = t
        else:
            # Tombol harus mendarat di penutup HARI TERAKHIR. Sebagian modul
            # menutup hari terakhirnya dengan .grad (mis. M15 'kelulusan'),
            # bukan .selesai-hari -- kalau langsung mencari .selesai-hari
            # terakhir, tombolnya nyangkut di hari kedua-terakhir.
            baru = None
            for penanda in ('<div class="grad">', '<div class="selesai-hari">'):
                if t.rfind(penanda) > t.rfind('<section class="day'):
                    baru = sisip_sebelum_tutup_blok(t, penanda, tombol)
                    if baru is not None:
                        break
            if baru is None:
                baru = sisip_sebelum_tutup_blok(t, '<div class="selesai-hari">', tombol)
        if baru is None:
            print(f"  !! {slug}: blok selesai-hari tidak ditemukan"); continue
        t = baru

    for kelas in ('kembali', 'lanjut'):
        if f'class="{kelas}"' in t and not re.search(rf'\.{kelas}\s*{{', t):
            print(f"  !! {slug}: pakai .{kelas} tapi CSS-nya tidak ada di berkas ini")

    if t != asli:
        open(berkas, 'w').write(t)
        diubah.append((slug, berkas))

print(f"{len(diubah)} berkas diperbarui:")
for s, b in diubah: print(f"  {s:34s} {b}")
