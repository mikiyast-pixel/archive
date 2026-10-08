import os
import tempfile
import pytest

from archive.errors import MalformedRecordError
from archive.storage import parse_line, load_archive, save_archive
from archive.validation import validate_id, validate_title, validate_city, validate_year, validate_condition, validate_record
from archive.queries import count_before, find_by_city, oldest, cities_summary


def test_condition_normal():
    assert validate_condition('fragile')[0] == True

def test_condition_normal_other():
    assert validate_condition('good')[0] == True

def test_condition_abnormal():
    assert validate_condition('excellent')[0] == False

def test_condition_empty():
    assert validate_condition('')[0] == False

def test_condition_case():
    assert validate_condition('GOOD')[0] == True

def test_year_normal():
    assert validate_year('1655')[0] == True

def test_year_abnormal():
    assert validate_year('c.1590')[0] == False
    assert validate_year('sixteen fifty')[0] == False
    assert validate_year('')[0] == False

def test_year_extreme_min():
    assert validate_year('1100')[0] == True

def test_year_extreme_max():
    assert validate_year('1900')[0] == True

def test_year_boundary_below():
    assert validate_year('1099')[0] == False

def test_year_boundary_above():
    assert validate_year('1901')[0] == False

def test_validate_id_valid():
    assert validate_id('MS001')[0] == True
    assert validate_id('MS999')[0] == True

def test_validate_id_lowercase_prefix():
    assert validate_id('ms001')[0] == False

def test_validate_id_wrong_prefix():
    assert validate_id('XX001')[0] == False

def test_validate_id_invalid_length():
    assert validate_id('MS01')[0] == False
    assert validate_id('MS0001')[0] == False

def test_validate_id_non_digits():
    assert validate_id('MS00A')[0] == False

def test_validate_id_empty():
    assert validate_id('')[0] == False

def test_validate_title_valid():
    assert validate_title('Tarikh al-Sudan')[0] == True

def test_validate_title_boundary_three_chars():
    assert validate_title('ABC')[0] == True

def test_validate_title_too_short():
    assert validate_title('Ab')[0] == False
    assert validate_title('A')[0] == False

def test_validate_title_whitespace_only():
    assert validate_title('    ')[0] == False

def test_validate_city_case_insensitive():
    assert validate_city('timbuktu')[0] == True
    assert validate_city('DJENNE')[0] == True

def test_validate_city_unknown():
    assert validate_city('Kano')[0] == False

def test_validate_city_empty():
    assert validate_city('')[0] == False

def test_validate_record_clean():
    rec = {
        'id': 'MS001',
        'title': 'Tarikh al-Sudan',
        'city': 'Timbuktu',
        'year': '1655',
        'condition': 'fragile',
    }
    assert validate_record(rec) == []

def test_validate_record_multiple_faults():
    bad = {
        'id': 'ms1',
        'title': 'A',
        'city': 'Kano',
        'year': '1099',
        'condition': 'broken',
    }
    errs = validate_record(bad)
    assert len(errs) == 5

def test_parse_line_strips_whitespace():
    ln = '  MS001  ,  Tarikh al-Sudan  , Timbuktu , 1655 , fragile \n'
    res = parse_line(ln)
    assert res['id'] == 'MS001'
    assert res['title'] == 'Tarikh al-Sudan'

def test_parse_line_four_fields_raises():
    try:
        parse_line('MS001,Title,Timbuktu,1655')
        assert False
    except MalformedRecordError:
        assert True

def test_parse_line_six_fields_raises():
    try:
        parse_line('MS001,Title,Timbuktu,1655,fragile,extra')
        assert False
    except MalformedRecordError:
        assert True

def test_load_archive_missing_file():
    good, bad = load_archive('missing_file.csv')
    assert good == []
    assert bad == []

def test_load_archive_separates_valid_and_rejected():
    text = (
        "MS001,Tarikh al-Sudan,Timbuktu,1655,fragile\n"
        "MS002,Short,Kano,1600,good\n"
        "MS003,Bad Line,Djenne\n"
    )
    with tempfile.NamedTemporaryFile('w+', delete=False, mode='w', encoding='utf-8') as f:
        f.write(text)
        path = f.name

    try:
        good, bad = load_archive(path)
        assert len(good) == 1
        assert good[0]['id'] == 'MS001'
        assert len(bad) == 2
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_save_and_load_round_trip():
    data = [{
        'id': 'MS001',
        'title': 'Tarikh al-Sudan',
        'city': 'Timbuktu',
        'year': '1655',
        'condition': 'fragile',
    }]
    
    with tempfile.NamedTemporaryFile('w+', delete=False, mode='w', encoding='utf-8') as f:
        path = f.name

    try:
        save_archive(path, data)
        good, bad = load_archive(path)
        assert good == data
        assert bad == []
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_count_before_strict_and_string_years():
    data = [{'year': '1500'}, {'year': '1600'}, {'year': '1700'}]
    assert count_before(data, 1600) == 1

def test_find_by_city_case_insensitive_and_order():
    data = [
        {'id': 'MS001', 'city': 'Timbuktu'},
        {'id': 'MS002', 'city': 'Djenne'},
        {'id': 'MS003', 'city': 'timbuktu'},
    ]
    res = find_by_city(data, 'TIMBUKTU')
    assert len(res) == 2
    assert res[0]['id'] == 'MS001'
    assert res[1]['id'] == 'MS003'

def test_oldest_first_on_tie():
    data = [
        {'id': 'MS001', 'year': '1500'},
        {'id': 'MS002', 'year': '1400'},
        {'id': 'MS003', 'year': '1400'},
    ]
    assert oldest(data)['id'] == 'MS002'

def test_oldest_empty():
    assert oldest([]) == None

def test_cities_summary_spelling():
    data = [{'city': 'Timbuktu'}, {'city': 'timbuktu'}, {'city': 'Djenne'}]
    sums = cities_summary(data)
    assert sums['Timbuktu'] == 1
    assert sums['timbuktu'] == 1
    assert sums['Djenne'] == 1
    assert ('Gao' in sums) == False
