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
    if is_null(value) == True:
        return (False, "ID is missing")
    if len(value) != 5:
        return (False, "ID must be exactly 5 characters long")
    if value[0:2] != "MS":
        return (False, "ID must start with uppercase 'MS'")
    if value[2:].isdigit() == False:
        return (False, "ID must end with exactly three digits")

    return (True, "Valid ID")


def validate_title(value):
    """A title must be present and at least 3 characters once stripped.

    Valid:   "Tarikh al-Sudan"
    Invalid: "", "   ", "Ab"

    Returns (bool, str).
    """
    if is_null(value) == True:
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
    if is_null(value) == True:
        return (False, "City is missing")

    known_cities_lower = []
    for c in KNOWN_CITIES:
        known_cities_lower.append(c.lower())

    if value.strip().lower() not in known_cities_lower:
        return (False, "City is not in known cities list")

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
    if is_null(value) == True:
        return (False, "Year is missing")

    stripped = value.strip()
    if is_int(stripped) == False:
        return (False, "Year must be an integer")

    year_int = int(stripped)
    if year_int < MIN_YEAR or year_int > MAX_YEAR:
        return (False, "Year must be between 1100 and 1900 inclusive")

    return (True, "Valid Year")


def validate_condition(value):
    """A condition must be one of VALID_CONDITIONS, case-insensitively.

    Valid:   "fragile", "GOOD", "Fair"
    Invalid: "excellent", "", "ok"

    Returns (bool, str).
    """
    if is_null(value) == True:
        return (False, "Condition is missing")

    valid_conditions_lower = []
    for c in VALID_CONDITIONS:
        valid_conditions_lower.append(c.lower())

    if value.strip().lower() not in valid_conditions_lower:
        return (False, "Condition must be one of valid conditions")

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

    if record == None or not isinstance(record, dict):
        return ["Record must be a dictionary"]

    if "id" in record:
        id_val = record["id"]
    else:
        id_val = ""
    is_valid, reason = validate_id(id_val)
    if is_valid == False:
        reasons.append(reason)

    if "title" in record:
        title_val = record["title"]
    else:
        title_val = ""
    is_valid, reason = validate_title(title_val)
    if is_valid == False:
        reasons.append(reason)

    if "city" in record:
        city_val = record["city"]
    else:
        city_val = ""
    is_valid, reason = validate_city(city_val)
    if is_valid == False:
        reasons.append(reason)

    if "year" in record:
        year_val = record["year"]
    else:
        year_val = ""
    is_valid, reason = validate_year(year_val)
    if is_valid == False:
        reasons.append(reason)

    if "condition" in record:
        condition_val = record["condition"]
    else:
        condition_val = ""
    is_valid, reason = validate_condition(condition_val)
    if is_valid == False:
        reasons.append(reason)

    return reasons
