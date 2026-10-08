def count_before(records, year):
    # find how many are before the given year
    cnt = 0
    for r in records:
        if r == None or type(r) != dict:
            continue
        if 'year' in r:
            y_val = r['year']
            try:
                y_int = int(y_val)
                if y_int < year:
                    cnt = cnt + 1
            except:
                pass
    return cnt


def find_by_city(records, city):
    # match city case insensitive
    tgt = city.strip().lower()
    res = []
    for r in records:
        if r == None or type(r) != dict:
            continue
        if 'city' in r and r['city'] != None:
            c = str(r['city']).strip().lower()
            if c == tgt:
                res.append(r)
    return res


def oldest(records):
    # get the oldest record
    if len(records) == 0:
        return None

    old_rec = None
    min_yr = None

    for r in records:
        if r == None or type(r) != dict:
            continue
        if 'year' in r:
            y_val = r['year']
            try:
                curr = int(y_val)
                if min_yr == None or curr < min_yr:
                    min_yr = curr
                    old_rec = r
            except:
                pass

    return old_rec


def cities_summary(records):
    # count per city
    sum_dict = {}
    for r in records:
        if r == None or type(r) != dict:
            continue
        if 'city' in r and r['city'] != None:
            c_name = r['city']
            if c_name in sum_dict:
                sum_dict[c_name] = sum_dict[c_name] + 1
            else:
                sum_dict[c_name] = 1
    return sum_dict
