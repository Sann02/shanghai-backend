# tests/test_utils.py
from app.utils import add, is_palindrome, clamp, celsius_to_fahrenheit, divide
import pytest 

def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-1, -4) == -5


def test_is_palindrome_true():
    assert is_palindrome("racecar") is True


def test_is_palindrome_false():
    assert is_palindrome("hello") is False


def test_clamp_within_range():
    assert clamp(5, 1, 10) == 5
    assert clamp(-3, 0, 100) == 0
    assert clamp(150, 0, 100) == 100


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212


def test_divide_by_zero_message():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "Cannot divide by zero" in str(exc_info.value)
