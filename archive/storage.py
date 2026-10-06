"""Reading and writing the Archive file."""

import os
from archive.errors import MalformedRecordError
from archive.validation import validate_record

FIELD_NAMES = ["id", "title", "city", "year", "condition"]


def parse_line(line):
    """Turn one CSV line into a dict with the five FIELD_NAMES as keys."""
    stripped_line = line.strip()
    if not stripped_line:
        raise MalformedRecordError("Empty line cannot be parsed as a record")

    fields = stripped_line.split(",")
    if len(fields) != 5:
        raise MalformedRecordError(
            f"Expected exactly 5 fields, got {len(fields)}"
        )

    cleaned_fields = [f.strip() for f in fields]
    return dict(zip(FIELD_NAMES, cleaned_fields))


def load_archive(path):
    """Read the file at path and return (valid_records, rejected_lines)."""
    if not os.path.exists(path):
        return ([], [])

    valid_records = []
    rejected_lines = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw_line = line.rstrip("\r\n")
            if not raw_line.strip():
                continue

            try:
                record = parse_line(raw_line)
                reasons = validate_record(record)
                if not reasons:
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
            row = ",".join(str(record.get(field, "")) for field in FIELD_NAMES)
            f.write(row + "\n")