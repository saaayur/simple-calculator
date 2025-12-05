# tests/test_calculator.py
import pytest
from src.calculator import evaluate_expression, CalcError

def test_basic_arithmetic():
    assert evaluate_expression("2 + 3 * 4") == 14
    assert evaluate_expression("(2 + 3) * 4") == 20
    assert evaluate_expression("10 / 2") == 5.0
    assert evaluate_expression("5 - 8") == -3

def test_division_by_zero_raises():
    with pytest.raises(CalcError):
        evaluate_expression("1 / 0")
