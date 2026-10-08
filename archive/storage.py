"""Reading and writing the Archive file."""

import os
from archive.errors import MalformedRecordError
from archive.validation import validate_record

FIELD_NAMES = ["id", "title", "city", "year", "condition"]


def parse_line(line):
    """Turn one CSV line into a dict with the five FIELD_NAMES as keys."""
    clean_line = line.replace("\r", "").replace("\n", "").strip()
    if clean_line == "":
        raise MalformedRecordError("Empty line cannot be parsed as a record")

    fields = clean_line.split(",")
    if len(fields) != 5:
        raise MalformedRecordError(
            "Expected exactly 5 fields, got " + str(len(fields))
        )

    cleaned_fields = []
    for f in fields:
        field_val = f.strip().replace("\r", "").replace("\n", "")
        cleaned_fields.append(field_val)

    record = {}
    record["id"] = cleaned_fields[0]
    record["title"] = cleaned_fields[1]
    record["city"] = cleaned_fields[2]
    record["year"] = cleaned_fields[3]
    record["condition"] = cleaned_fields[4]

    return record


def load_archive(path):
    """Read the file at path and return (valid_records, rejected_lines)."""
    if os.path.exists(path) == False:
        return ([], [])

    valid_records = []
    rejected_lines = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw_line = line.replace("\r", "").replace("\n", "")
            if raw_line.strip() == "":
                continue

            try:
                record = parse_line(raw_line)
                reasons = validate_record(record)
                if len(reasons) == 0:
                    valid_records.append(record)
                else:
                    rejected_lines.append(raw_line)
            except MalformedRecordError:
                rejected_lines.append(raw_line)

    return (valid_records, rejected_lines)


def save_archive(path, records):
    """Write every record to path as CSV, one per line, no header."""
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            if "id" in record:
                id_str = str(record["id"]).replace("\r", "").replace("\n", "")
            else:
                id_str = ""

            if "title" in record:
                title_str = str(record["title"]).replace("\r", "").replace("\n", "")
            else:
                title_str = ""

            if "city" in record:
                city_str = str(record["city"]).replace("\r", "").replace("\n", "")
            else:
                city_str = ""

            if "year" in record:
                year_str = str(record["year"]).replace("\r", "").replace("\n", "")
            else:
                year_str = ""

            if "condition" in record:
                cond_str = str(record["condition"]).replace("\r", "").replace("\n", "")
            else:
                cond_str = ""

            row = id_str + "," + title_str + "," + city_str + "," + year_str + "," + cond_str
            f.write(row + "\n")
