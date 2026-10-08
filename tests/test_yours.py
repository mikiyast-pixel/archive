"""YOUR test suite — Part B."""

import os
import pytest

from archive.errors import MalformedRecordError
from archive.storage import parse_line, load_archive, save_archive
from archive.validation import (
    validate_id,
    validate_title,
    validate_city,
    validate_year,
    validate_condition,
    validate_record,
)
from archive.queries import count_before, find_by_city, oldest, cities_summary


# ====================================================== WORKED EXAMPLE
def test_condition_normal():
    assert validate_condition("fragile")[0] == True


def test_condition_normal_other():
    assert validate_condition("good")[0] == True


def test_condition_abnormal():
    assert validate_condition("excellent")[0] == False


def test_condition_empty():
    assert validate_condition("")[0] == False


def test_condition_case():
    assert validate_condition("GOOD")[0] == True


# ============================================= validate_year TESTS
def test_year_normal():
    """NORMAL — a year from the middle of the range."""
    assert validate_year("1655")[0] == True


def test_year_abnormal():
    """ABNORMAL — non-numeric text values."""
    assert validate_year("c.1590")[0] == False
    assert validate_year("sixteen fifty")[0] == False
    assert validate_year("")[0] == False


def test_year_extreme_min():
    """EXTREME — lower boundary value (inclusive)."""
    assert validate_year("1100")[0] == True


def test_year_extreme_max():
    """EXTREME — upper boundary value (inclusive)."""
    assert validate_year("1900")[0] == True


def test_year_boundary_below():
    """BOUNDARY — just below the minimum allowed year."""
    assert validate_year("1099")[0] == False


def test_year_boundary_above():
    """BOUNDARY — just above the maximum allowed year."""
    assert validate_year("1901")[0] == False


# ====================================================== ADDITIONAL TESTS

# --- validate_id ---
def test_validate_id_valid():
    assert validate_id("MS001")[0] == True
    assert validate_id("MS999")[0] == True


def test_validate_id_lowercase_prefix():
    assert validate_id("ms001")[0] == False


def test_validate_id_wrong_prefix():
    assert validate_id("XX001")[0] == False


def test_validate_id_invalid_length():
    assert validate_id("MS01")[0] == False
    assert validate_id("MS0001")[0] == False


def test_validate_id_non_digits():
    assert validate_id("MS00A")[0] == False


def test_validate_id_empty():
    assert validate_id("")[0] == False


# --- validate_title ---
def test_validate_title_valid():
    assert validate_title("Tarikh al-Sudan")[0] == True


def test_validate_title_boundary_three_chars():
    assert validate_title("ABC")[0] == True


def test_validate_title_too_short():
    assert validate_title("Ab")[0] == False
    assert validate_title("A")[0] == False


def test_validate_title_whitespace_only():
    assert validate_title("    ")[0] == False


# --- validate_city ---
def test_validate_city_case_insensitive():
    assert validate_city("timbuktu")[0] == True
    assert validate_city("DJENNE")[0] == True


def test_validate_city_unknown():
    assert validate_city("Kano")[0] == False


def test_validate_city_empty():
    assert validate_city("")[0] == False


# --- validate_record ---
def test_validate_record_clean():
    clean_record = {
        "id": "MS001",
        "title": "Tarikh al-Sudan",
        "city": "Timbuktu",
        "year": "1655",
        "condition": "fragile",
    }
    assert validate_record(clean_record) == []


def test_validate_record_multiple_faults():
    bad_record = {
        "id": "ms1",
        "title": "A",
        "city": "Kano",
        "year": "1099",
        "condition": "broken",
    }
    reasons = validate_record(bad_record)
    assert len(reasons) == 5


# --- parse_line ---
def test_parse_line_strips_whitespace():
    line = "  MS001  ,  Tarikh al-Sudan  , Timbuktu , 1655 , fragile \n"
    parsed = parse_line(line)
    assert parsed["id"] == "MS001"
    assert parsed["title"] == "Tarikh al-Sudan"


def test_parse_line_four_fields_raises():
    try:
        parse_line("MS001,Title,Timbuktu,1655")
        assert False
    except MalformedRecordError:
        assert True


def test_parse_line_six_fields_raises():
    try:
        parse_line("MS001,Title,Timbuktu,1655,fragile,extra")
        assert False
    except MalformedRecordError:
        assert True


# --- storage (load & save) ---
def test_load_archive_missing_file():
    records, rejected = load_archive("non_existent_file.csv")
    assert records == []
    assert rejected == []


def test_load_archive_separates_valid_and_rejected():
    content = (
        "MS001,Tarikh al-Sudan,Timbuktu,1655,fragile\n"
        "MS002,Short,Kano,1600,good\n"
        "MS003,Bad Line,Djenne\n"
    )
    f = open("temp_test_file.csv", "w")
    f.write(content)
    f.close()

    valid, rejected = load_archive("temp_test_file.csv")
    assert len(valid) == 1
    assert valid[0]["id"] == "MS001"
    assert len(rejected) == 2

    if os.path.exists("temp_test_file.csv"):
        os.remove("temp_test_file.csv")


def test_save_and_load_round_trip():
    data = [
        {
            "id": "MS001",
            "title": "Tarikh al-Sudan",
            "city": "Timbuktu",
            "year": "1655",
            "condition": "fragile",
        }
    ]

    save_archive("temp_save_file.csv", data)
    loaded, rejected = load_archive("temp_save_file.csv")
    assert loaded == data
    assert rejected == []

    if os.path.exists("temp_save_file.csv"):
        os.remove("temp_save_file.csv")


# --- queries ---
def test_count_before_strict_and_string_years():
    sample = [
        {"year": "1500"},
        {"year": "1600"},
        {"year": "1700"},
    ]
    assert count_before(sample, 1600) == 1


def test_find_by_city_case_insensitive_and_order():
    sample = [
        {"id": "MS001", "city": "Timbuktu"},
        {"id": "MS002", "city": "Djenne"},
        {"id": "MS003", "city": "timbuktu"},
    ]
    matches = find_by_city(sample, "TIMBUKTU")
    assert len(matches) == 2
    assert matches[0]["id"] == "MS001"
    assert matches[1]["id"] == "MS003"


def test_oldest_first_on_tie():
    sample = [
        {"id": "MS001", "year": "1500"},
        {"id": "MS002", "year": "1400"},
        {"id": "MS003", "year": "1400"},
    ]
    res = oldest(sample)
    assert res["id"] == "MS002"


def test_oldest_empty():
    assert oldest([]) == None


def test_cities_summary_spelling():
    sample = [
        {"city": "Timbuktu"},
        {"city": "timbuktu"},
        {"city": "Djenne"},
    ]
    summary = cities_summary(sample)
    assert summary["Timbuktu"] == 1
    assert summary["timbuktu"] == 1
    assert summary["Djenne"] == 1
    assert ("Gao" in summary) == False
