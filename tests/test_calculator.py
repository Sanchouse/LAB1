import pytest
from toolkit.calculator import calculate


class TestCalculator:
    def test_add(self):
        assert calculate("2+ 2") == 4
    
    def test_subtract(self):
        assert calculate("5 - 3") == 2

    def test_multiply(self):
        assert calculate("3 * 4") == 12

    def test_diviosion(self):
        assert calculate("4 / 5") == 0.8

    def test_with_brackets(self):
        assert calculate("5 * (4 + 2)") == 30

    def test_with_unar(self):
        assert calculate("-5 * 2") == -10

    def test_pow(self):
        assert calculate("(5-3)**4") == 16

    def test_integer_division(self):
        assert calculate("9//3 + 2") == 5

    def test_with_wrong_brackets(self):
        with pytest.raises(ValueError):
            calculate("5 * 2(")

    def test_with_double_operators(self):
        with pytest.raises(ValueError):
            calculate("5 ++ 2")

    def test_with_operator_at_the_end(self):
        with pytest.raises(ValueError):
            calculate("5 * 2 +")

    def test_without_ops(self):
        with pytest.raises(ValueError): 
            calculate("10 0")

    def test_with_incorrect_char(self):
        with pytest.raises(ValueError):
            calculate("67 & 34")