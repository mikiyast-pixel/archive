"""Reading and writing the Archive file.

YOU IMPLEMENT THIS FILE.

The file format is CSV with no header row. One record per line, five fields
separated by commas, in this order:

    id,title,city,year,condition
    MS001,Tarikh al-Sudan,Timbuktu,1655,fragile

Remember Session 1: a file is one long line of characters. The comma
separates fields; the newline separates records. Nothing else is doing
any work.
"""

from archive.errors import MalformedRecordError
from archive.validation import validate_record

FIELD_NAMES = ["id", "title", "city", "year", "condition"]


def parse_line(line):
    stripped_line = line.strip()
    fields = [field.strip() for field in stripped_line.split(",")]

    if len(fields) != len(FIELD_NAMES):
        raise MalformedRecordError(f"Expected {len(FIELD_NAMES)} fields, got {len(fields)}")

    return dict(zip(FIELD_NAMES, fields))


def load_archive(path):
    valid_records = []
    rejected_lines = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    record = parse_line(line)
                    validate_record(record)
                    valid_records.append(record)
                except Exception:
                    rejected_lines.append(line)
    except FileNotFoundError:
        return [], []

    return valid_records, rejected_lines


def save_archive(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            line_str = ",".join(str(record[field]) for field in FIELD_NAMES)
            f.write(f"{line_str}\n")