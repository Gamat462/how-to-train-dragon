import pandas as pd
import pytest
from laporan.bersih import ke_angka, rapikan_nama, buang_baris_bukan_data


@pytest.mark.parametrize("masuk,harap", [
    ("3.200.000", 3200000),
    ("Rp 91.190.000", 91190000),
    ("96.000", 96000),
    (22000, 22000),
    ("-96.000", -96000),
    ("", None),
    (None, None),
])
def test_ke_angka(masuk, harap):
    assert ke_angka(masuk) == harap


def test_rapikan_nama_menyatukan_empat_ejaan():
    s = pd.Series([" budi santoso ", "BUDI SANTOSO", "Budi  Santoso", "Budi Santoso"])
    assert rapikan_nama(s).nunique() == 1


def test_rapikan_nama_tidak_merusak_cv():
    s = pd.Series(["cv karya abadi", "PT mitra bangun"])
    assert list(rapikan_nama(s)) == ["CV Karya Abadi", "PT Mitra Bangun"]


def test_buang_baris_bukan_data():
    df = pd.DataFrame({"No": ["1", "2", "Dicetak oleh: Admin", None], "x": [1, 2, 3, 4]})
    assert len(buang_baris_bukan_data(df)) == 2


@pytest.mark.parametrize("masuk,harap", [
    ("(1.000)", -1000),
    ("(91.190.000)", -91190000),
    ("-96.000", -96000),
    ("96.000", 96000),
])
def test_ke_angka_kurung_akuntansi(masuk, harap):
    """Excel akuntansi menulis angka negatif sebagai (1.000), bukan -1000."""
    assert ke_angka(masuk) == harap, f"{masuk!r} terbaca {ke_angka(masuk)}, harusnya {harap}"


def test_rapikan_nama_badan_usaha_bertitik():
    """Klien menulis "PT. MAJU JAYA" sesering "PT MAJU JAYA"."""
    s = pd.Series(["PT. MAJU JAYA", "cv. karya abadi"])
    assert list(rapikan_nama(s)) == ["PT. Maju Jaya", "CV. Karya Abadi"], \
        f"hasilnya {list(rapikan_nama(s))}"
