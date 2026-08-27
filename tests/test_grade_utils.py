# tests/test_grade_utils.py
import pytest
from app.grade_utils import calculate_average, letter_grade, is_passing, format_report


# ─── calculate_average ────────────────────────────────────────

def test_calculate_average_of_multiple_grades():
    result = calculate_average([80, 90, 100])
    assert result == 90.0
    assert isinstance(result, float)


def test_calculate_average_of_single_grade():
    result = calculate_average([75])
    assert result == 75.0


def test_calculate_average_empty_list_raises():
    with pytest.raises(ValueError) as exc_info:
        calculate_average([])
    assert "grades list cannot be empty" in str(exc_info.value)


# ─── letter_grade ─────────────────────────────────────────────

def test_letter_grade_90_and_above_returns_A():
    assert letter_grade(95) == "A"
    assert letter_grade(90) == "A"
    assert letter_grade(100) == "A"


def test_letter_grade_70_to_79_returns_C():
    assert letter_grade(70) == "C"
    assert letter_grade(75) == "C"
    assert letter_grade(79) == "C"


def test_letter_grade_below_zero_raises():
    with pytest.raises(ValueError) as exc_info:
        letter_grade(-1)
    assert "Score must be between 0 and 100" in str(exc_info.value)


# ─── is_passing ───────────────────────────────────────────────

def test_is_passing_above_threshold_returns_true():
    assert is_passing(85) is True
    assert is_passing(61) is True


def test_is_passing_exactly_at_threshold_returns_true():
    assert is_passing(60) is True
    assert is_passing(70, threshold=70) is True


def test_is_passing_below_threshold_returns_false():
    assert is_passing(59) is False
    assert is_passing(0) is False


# ─── format_report ────────────────────────────────────────────

def test_format_report_contains_name_and_grade():
    report = format_report("Alice", 92)
    assert "Alice" in report
    assert "A" in report
    assert "PASSING" in report
    assert isinstance(report, str)


def test_format_report_failing_student_shows_failing_status():
    report = format_report("Bob", 50)
    assert "Bob" in report
    assert "FAILING" in report
    assert "F" in report


def test_format_report_non_string_name_raises():
    with pytest.raises(TypeError) as exc_info:
        format_report(123, 85)
    assert "name must be a string" in str(exc_info.value)
