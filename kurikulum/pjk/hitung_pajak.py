LAPISAN = [(0, 60_000_000, 0.05), (60_000_000, 250_000_000, 0.15),
           (250_000_000, 500_000_000, 0.25), (500_000_000, 5_000_000_000, 0.30),
           (5_000_000_000, None, 0.35)]
BATAS_UMKM = 4_800_000_000

def pajak_progresif(penghasilan):
    total = 0
    for bawah, atas, tarif in LAPISAN:
        atas_efektif = atas if atas is not None else penghasilan
        bagian = max(0, min(penghasilan, atas_efektif) - bawah)
        total += bagian * tarif
    return round(total)

def pajak_final(jenis, penghasilan, omzet=None):
    if jenis == "umkm" and omzet is not None and omzet <= BATAS_UMKM:
        return round(omzet * 0.005)
    return pajak_progresif(penghasilan)
