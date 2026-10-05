"""Validation rules for manuscript records.

YOU IMPLEMENT THIS FILE.

Every validate_* function takes a raw string (exactly as it came out of the
CSV file) and returns a tuple:

    (True, "")              the value is trustworthy
    (False, "reason here")  the value is not, and here is why

The reason is a short human-readable string. The autograder checks the
boolean, not your exact wording — but a teammate reading your rejection log
should understand it, so write it for them.

READ THIS BEFORE YOU START
--------------------------
The year range is INCLUSIVE at both ends: 1100 and 1900 are VALID.
1099 and 1901 are not. Most marks lost in Part A are lost on that line.
"""

from archive.errors import MalformedRecordError  # noqa: F401  (you may not need it here)

KNOWN_CITIES = ["Timbuktu", "Djenne", "Gao", "Walata", "Chinguetti"]
VALID_CONDITIONS = ["fragile", "fair", "good"]

MIN_YEAR = 1100
MAX_YEAR = 1900


def is_null(val):
    if val is None:
        return True
    if isinstance(val, str) and len(val.strip()) == 0:
        return True
    return False


def is_int(val):
    try:
        int(val)
        return True
    except (ValueError, TypeError):
        return False


def validate_id(value):
    """An ID is the letters 'MS' followed by exactly three digits.

    Valid:   "MS001", "MS742"
    Invalid: "MS1", "MS0012", "ms001", "XX001", "", "MS00A"

    Returns (bool, str).
    """
    if is_null(value):
        return (False, "ID is missing")
    if len(value) != 5:
        return (False, "ID must be exactly 5 characters long")
    if value[:2] != "MS":
        return (False, "ID must start with uppercase 'MS'")
    if not value[2:].isdigit():
        return (False, "ID must end with exactly three digits")

    return (True, "Valid ID")


def validate_title(value):
    """A title must be present and at least 3 characters once stripped.

    Valid:   "Tarikh al-Sudan"
    Invalid: "", "   ", "Ab"

    Returns (bool, str).
    """
    if is_null(value):
        return (False, "Title is missing")

    cleaned_title = value.strip()
    if len(cleaned_title) < 3:
        return (False, "Title must be at least 3 characters once stripped")

    return (True, "Valid Title")


def validate_city(value):
    """A city must be present and appear in KNOWN_CITIES.

    Comparison is case-insensitive: "timbuktu" is acceptable.
    "Kano" is not in our list, so it is rejected — and that is a real
    decision with a cost. Write about it in your README.

    Returns (bool, str).
    """
    if is_null(value):
        return (False, "City is missing")

    known_cities_lower = [c.lower() for c in KNOWN_CITIES]
    if value.strip().lower() not in known_cities_lower:
        return (False, f"City '{value}' is not in known cities list")

    return (True, "Valid City")


def validate_year(value):
    """A year must be present, numeric, and between MIN_YEAR and MAX_YEAR
    INCLUSIVE.

    Valid:   "1655", "1100", "1900"
    Invalid: "", "   ", "c.1590", "sixteen fifty", "1099", "1901", "2087"

    Note that "2087" parses perfectly well as a number. It is still wrong.
    That is the whole point of a range check.

    Returns (bool, str)
    """
    if is_null(value):
        return (False, "Year is missing")

    stripped = value.strip()
    if not is_int(stripped):
        return (False, "Year must be an integer")

    year_int = int(stripped)
    if not (MIN_YEAR <= year_int <= MAX_YEAR):
        return (False, f"Year must be between {MIN_YEAR} and {MAX_YEAR} inclusive")

    return (True, "Valid Year")


def validate_condition(value):
    """A condition must be one of VALID_CONDITIONS, case-insensitively.

    Valid:   "fragile", "GOOD", "Fair"
    Invalid: "excellent", "", "ok"

    Returns (bool, str).
    """
    if is_null(value):
        return (False, "Condition is missing")

    if value.strip().lower() not in [c.lower() for c in VALID_CONDITIONS]:
        return (False, f"Condition must be one of {VALID_CONDITIONS}")

    return (True, "Valid Condition")


def validate_record(record):
    """Validate a whole record dictionary.

    record is a dict with the keys: id, title, city, year, condition.

    Returns a LIST of reasons the record is invalid — one string per broken
    rule, in this field order: id, title, city, year, condition.
    An empty list means the record is valid.

    Do not re-write the rules here. Call the five functions above.
    """
    reasons = []

    field_validators = [
        ("id", validate_id),
        ("title", validate_title),
        ("city", validate_city),
        ("year", validate_year),
        ("condition", validate_condition),
    ]

    for key, validator in field_validators:
        val = record.get(key, "")
        is_valid, reason = validator(val)
        if not is_valid:
            reasons.append(reason)

    return reasons