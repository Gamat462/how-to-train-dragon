from hitung_pajak import pajak_final

def test_perorangan_rina():
    assert pajak_final("perorangan", 45_000_000) == 2_250_000

def test_perorangan_bayu():
    assert pajak_final("perorangan", 180_000_000) == 21_000_000

def test_perorangan_sari():
    assert pajak_final("perorangan", 620_000_000) == 130_000_000

def test_perorangan_maya():
    assert pajak_final("perorangan", 7_200_000_000) == 2_214_000_000

def test_umkm_dimas():
    assert pajak_final("umkm", 150_000_000, omzet=900_000_000) == 4_500_000

def test_umkm_putri():
    assert pajak_final("umkm", 410_000_000, omzet=3_200_000_000) == 16_000_000

def test_umkm_agus_lewat_batas():
    assert pajak_final("umkm", 980_000_000, omzet=5_100_000_000) == 238_000_000
