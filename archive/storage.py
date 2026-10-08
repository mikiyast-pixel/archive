import os
from archive.errors import MalformedRecordError
from archive.validation import validate_record

FIELD_NAMES = ["id", "title", "city", "year", "condition"]

def parse_line(line):
    stripped_line = line.strip()
    if stripped_line == "":
        raise MalformedRecordError("Empty line cannot be parsed as a record")
    
    fields = stripped_line.split(",")
    if len(fields) != 5:
        raise MalformedRecordError("Expected exactly 5 fields, got " + str(len(fields)))
    
    cleaned_fields = []
    for f in fields:
        cleaned_fields.append(f.strip())
        
    record = {}
    record["id"] = cleaned_fields[0]
    record["title"] = cleaned_fields[1]
    record["city"] = cleaned_fields[2]
    record["year"] = cleaned_fields[3]
    record["condition"] = cleaned_fields[4]
    
    return record


def load_archive(path):
    if os.path.exists(path) == False:
        return [], []
    
    valid_records = []
    rejected_lines = []
    
    f = open(path, "r", encoding="utf-8")
    for line in f:
        # manually remove newline at the end
        if line.endswith("\n"):
            raw_line = line[:-1]
        else:
            raw_line = line
            
        if raw_line.endswith("\r"):
            raw_line = raw_line[:-1]
            
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
            
    f.close()
    return valid_records, rejected_lines


def save_archive(path, records):
    f = open(path, "w", encoding="utf-8")
    for record in records:
        row = ""
        row = row + str(record["id"]) + ","
        row = row + str(record["title"]) + ","
        row = row + str(record["city"]) + ","
        row = row + str(record["year"]) + ","
        row = row + str(record["condition"])
        f.write(row + "\n")
    f.close()
