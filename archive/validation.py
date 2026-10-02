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
    return False
def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
def validate_id(value):
    """An ID is the letters 'MS' followed by exactly three digits.

    Valid:   "MS001", "MS742"
    Invalid: "MS1", "MS0012", "ms001", "XX001", "", "MS00A"

    Returns (bool, str).
    """
    if is_null(value):
        return (False,"NO ID!")
    if len(value) != 5:
        return (False,"ID's length is too short")
    elif value[:3]!="MS":
        return (False,"Invalid ID,ID is supposed to start with MS")
    elif not is_int(value[3:]):
        return (False,"Invalid ID,ID is supposed to end with a three digit integer")
    elif 1 < int(value[3:]) <= 999:
        return (False,"Invalid ID,ID is supposed to end with a three digit integer between 1 and 999")
    else:
        return (True, "Valid ID")
    raise NotImplementedError("validate_id")

def validate_title(value):
    """A title must be present and at least 3 characters once stripped.

    Valid:   "Tarikh al-Sudan"
    Invalid: "", "   ", "Ab"

    Returns (bool, str).
    """
    if is_null(value):
        return (False,"Title is not present")
    elif len(value) < 3:
        return (False,"Title must have at least 3 cahracters")
    else:
        return (True,"Valid")
    raise NotImplementedError("validate_title")
    
def validate_city(value):
    """A city must be present and appear in KNOWN_CITIES.

    Comparison is case-insensitive: "timbuktu" is acceptable.
    "Kano" is not in our list, so it is rejected — and that is a real
    decision with a cost. Write about it in your README.

    Returns (bool, str).
    """
    if is_null(value):
        return (False,"City is not present")
    elif value not in KNOWN_CITIES:
        return(False,"City must be in KNOWN CITIES")
    else:
        return (True,"Valid")
    raise NotImplementedError("validate_city")


def validate_year(value):
    """A year must be present, numeric, and between MIN_YEAR and MAX_YEAR
    INCLUSIVE.

    Valid:   "1655", "1100", "1900"
    Invalid: "", "   ", "c.1590", "sixteen fifty", "1099", "1901", "2087"

    Note that "2087" parses perfectly well as a number. It is still wrong.
    That is the whole point of a range check.

    Returns (bool, str).
    """
    if is_null(value):
        return (False,"Year is not present")
    elif not is_int(value):
        return (False,"Year is supposed to be an integer between 1100 and 1900 inclusive")
    elif not MIN_YEAR <= value <= MAX_YEAR:
        return (False,"Year must in between 1100 and 1900 inclusive")
    else:
        return (True,"Valid")
    raise NotImplementedError("validate_year")


def validate_condition(value):
    """A condition must be one of VALID_CONDITIONS, case-insensitively.

    Valid:   "fragile", "GOOD", "Fair"
    Invalid: "excellent", "", "ok"

    Returns (bool, str).
    """
    
    
    raise NotImplementedError("validate_condition")


def validate_record(record):
    """Validate a whole record dictionary.

    record is a dict with the keys: id, title, city, year, condition.

    Returns a LIST of reasons the record is invalid — one string per broken
    rule, in this field order: id, title, city, year, condition.
    An empty list means the record is valid.

    Do not re-write the rules here. Call the five functions above.
    """
    raise NotImplementedError("validate_record")
