# app/utils.py
# Utility functions we will test together

# Re-export db so services can do: from app.utils import db
from app import db  # noqa: F401


def add(a, b):
    return a + b


def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def clamp(value, minimum, maximum):
    """Return value clamped between minimum and maximum."""
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def divide(a, b):
    """Divide a by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
