import pytest
from toolkit.converter import convert


class DataForTests:
    def __init__(self, value, from_unit, to_unit):
        self.value, self.from_unit, self.to_unit = value, from_unit, to_unit


class TestConverter:
    def test_m_to_cm(self):
        assert convert(DataForTests(5, "m", "cm")) == 500
    
    def test_km_to_cm(self):
        assert convert(DataForTests(1.5, "km", "cm")) == 150000

    def test_mm_to_km(self):
        assert convert(DataForTests(426752, "mm", "km")) == 0.426752

    def test_kg_to_g(self):
        assert convert(DataForTests(15, "kg", "g")) == 15000

    def test_g_to_kg(self):
        assert convert(DataForTests(45000, "g", "kg")) == 45

    def test_c_to_f(self):
        assert convert(DataForTests(50, "c", "f")) == 122

    def test_f_to_k(self):
        assert convert(DataForTests(100, "f", "k")) == 310.927778

    def test_k_to_c(self):
        assert convert(DataForTests(273, "k", "c")) == 0

    def test_with_minus_distance(self):
        with pytest.raises(ValueError):
            convert(DataForTests(-10, "m", "cm"))

    def test_with_minus_mass(self):
        with pytest.raises(ValueError):
            convert(DataForTests(-50, "kg", "g"))

    def test_with_different_types(self):
        with pytest.raises(ValueError):
            convert(DataForTests(10, "c", "cm"))

    def test_with_different_types_second_variant(self):
        with pytest.raises(ValueError):
            convert(DataForTests(4, "kg", "f"))

    def test_with_unknown_char(self):
        with pytest.raises(ValueError):
            convert(DataForTests(5, "nm", "m"))

    def test_with_absolute_minus(self):
        with pytest.raises(ValueError):
            convert(DataForTests(-50, "k", "c"))