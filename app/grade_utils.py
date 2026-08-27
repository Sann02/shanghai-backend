# app/grade_utils.py  — DO NOT MODIFY THIS FILE
# Write your tests in tests/test_grade_utils.py


def calculate_average(grades: list[float]) -> float:
    """Return the average of a list of grades (0-100).
    Raises ValueError if the list is empty.
    """
    if not grades:
        raise ValueError("grades list cannot be empty")
    return round(sum(grades) / len(grades), 2)


def letter_grade(score: float) -> str:
    """Convert a numeric score to a letter grade.
    A: 90-100  B: 80-89  C: 70-79  D: 60-69  F: 0-59
    Raises ValueError if score is outside 0-100.
    """
    if not 0 <= score <= 100:
        raise ValueError(f"Score must be between 0 and 100, got {score}")
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    return "F"


def is_passing(score: float, threshold: float = 60.0) -> bool:
    """Return True if score >= threshold."""
    return score >= threshold


def format_report(name: str, score: float) -> str:
    """Return a formatted grade report string.
    Raises TypeError if name is not a string or score is not a number.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    if not isinstance(score, (int, float)):
        raise TypeError("score must be a number")
    grade = letter_grade(score)
    status = "PASSING" if is_passing(score) else "FAILING"
    return f"{name} | Score: {score} | Grade: {grade} | Status: {status}"
