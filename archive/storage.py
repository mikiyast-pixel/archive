import os
from archive.errors import MalformedRecordError
from archive.validation import validate_record

FIELD_NAMES = ['id', 'title', 'city', 'year', 'condition']

def parse_line(line):
    # clean up the line and make a dict
    tmp = line.replace('\r', '').replace('\n', '').strip()
    if tmp == '':
        raise MalformedRecordError('empty line')

    flds = tmp.split(',')
    if len(flds) != 5:
        raise MalformedRecordError('wrong number of fields: ' + str(len(flds)))

    cln = []
    for f in flds:
        cln.append(f.strip().replace('\r', '').replace('\n', ''))

    rec = {}
    rec['id'] = cln[0]
    rec['title'] = cln[1]
    rec['city'] = cln[2]
    rec['year'] = cln[3]
    rec['condition'] = cln[4]
    
    return rec


def load_archive(path):
    # open file and sort valid vs rejected
    if os.path.exists(path) == False:
        return ([], [])

    good_recs = []
    bad_lines = []

    with open(path, 'r', encoding='utf-8') as f:
        for ln in f:
            raw = ln.replace('\r', '').replace('\n', '')
            if raw.strip() == '':
                continue
            
            try:
                rec = parse_line(raw)
                errs = validate_record(rec)
                if len(errs) == 0:
                    good_recs.append(rec)
                else:
                    bad_lines.append(raw)
            except MalformedRecordError:
                bad_lines.append(raw)

    return (good_recs, bad_lines)


def save_archive(path, records):
    # write records back to csv
    with open(path, 'w', encoding='utf-8') as f:
        for r in records:
            if 'id' in r:
                i_str = str(r['id']).replace('\r', '').replace('\n', '')
            else:
                i_str = ''

            if 'title' in r:
                t_str = str(r['title']).replace('\r', '').replace('\n', '')
            else:
                t_str = ''

            if 'city' in r:
                c_str = str(r['city']).replace('\r', '').replace('\n', '')
            else:
                c_str = ''

            if 'year' in r:
                y_str = str(r['year']).replace('\r', '').replace('\n', '')
            else:
                y_str = ''

            if 'condition' in r:
                cond_str = str(r['condition']).replace('\r', '').replace('\n', '')
            else:
                cond_str = ''

            row = i_str + ',' + t_str + ',' + c_str + ',' + y_str + ',' + cond_str
            f.write(row + '\n')
