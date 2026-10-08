from archive.errors import MalformedRecordError

KNOWN_CITIES = ['Timbuktu', 'Djenne', 'Gao', 'Walata', 'Chinguetti']
VALID_CONDITIONS = ['fragile', 'fair', 'good']

MIN_YEAR = 1100
MAX_YEAR = 1900

def check_empty(v):
    if v == None:
        return True
    if type(v) == str and len(v.strip()) == 0:
        return True
    return False

def validate_id(val):
    # ms prefix and 3 numbers
    if check_empty(val):
        return (False, 'missing id')
    if len(val) != 5:
        return (False, 'bad length')
    if val[0:2] != 'MS':
        return (False, 'needs MS')
    if val[2:].isdigit() == False:
        return (False, 'needs 3 digits')
    return (True, 'ok')

def validate_title(val):
    # needs to be 3 chars min
    if check_empty(val):
        return (False, 'missing title')
    
    cln = val.strip()
    if len(cln) < 3:
        return (False, 'too short')
        
    return (True, 'ok')

def validate_city(val):
    # check if city is in our list
    if check_empty(val):
        return (False, 'missing city')

    lower_cities = []
    for c in KNOWN_CITIES:
        lower_cities.append(c.lower())

    if val.strip().lower() not in lower_cities:
        return (False, 'unknown city')

    return (True, 'ok')

def validate_year(val):
    # number between limits
    if check_empty(val):
        return (False, 'missing year')

    cln = val.strip()
    try:
        y = int(cln)
        if y < MIN_YEAR or y > MAX_YEAR:
            return (False, 'out of range')
        return (True, 'ok')
    except:
        return (False, 'not a number')

def validate_condition(val):
    # must be fragile fair or good
    if check_empty(val):
        return (False, 'missing cond')

    lower_conds = []
    for c in VALID_CONDITIONS:
        lower_conds.append(c.lower())

    if val.strip().lower() not in lower_conds:
        return (False, 'bad cond')

    return (True, 'ok')

def validate_record(rec):
    # run all checks and return errors
    errs = []

    if rec == None or type(rec) != dict:
        return ['needs to be a dict']

    if 'id' in rec:
        v_id = rec['id']
    else:
        v_id = ''
    valid, msg = validate_id(v_id)
    if valid == False:
        errs.append(msg)

    if 'title' in rec:
        v_title = rec['title']
    else:
        v_title = ''
    valid, msg = validate_title(v_title)
    if valid == False:
        errs.append(msg)

    if 'city' in rec:
        v_city = rec['city']
    else:
        v_city = ''
    valid, msg = validate_city(v_city)
    if valid == False:
        errs.append(msg)

    if 'year' in rec:
        v_yr = rec['year']
    else:
        v_yr = ''
    valid, msg = validate_year(v_yr)
    if valid == False:
        errs.append(msg)

    if 'condition' in rec:
        v_cond = rec['condition']
    else:
        v_cond = ''
    valid, msg = validate_condition(v_cond)
    if valid == False:
        errs.append(msg)

    return errs
