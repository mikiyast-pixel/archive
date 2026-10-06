"""Questions we ask the Archive."""


def count_before(records, year):
    """How many manuscripts were written strictly BEFORE `year`?"""
    count = 0
    for rec in records:
        if int(rec["year"]) < year:
            count += 1
    return count


def find_by_city(records, city):
    """Every record whose city matches `city`, case-insensitively. Order is preserved."""
    target = city.strip().lower()
    return [rec for rec in records if rec["city"].strip().lower() == target]


def oldest(records):
    """The record with the smallest year. Return None if empty.

    If two records tie on year, return the one that appears FIRST.
    """
    if not records:
        return None
    return min(records, key=lambda rec: int(rec["year"]))


def cities_summary(records):
    """How many manuscripts come from each city?"""
    summary = {}
    for rec in records:
        city_name = rec["city"]
        summary[city_name] = summary.get(city_name, 0) + 1
    return summary
    for rec in records:
        if int(rec["year"]) < year:
            count += 1
    return count


def find_by_city(records, city):
    """Every record whose city matches `city`, case-insensitively. Order is preserved."""
    target = city.strip().lower()
    return [rec for rec in records if rec["city"].strip().lower() == target]


def oldest(records):
    """The record with the smallest year. Return None if empty.

    If two records tie on year, return the one that appears FIRST.
    """
    if not records:
        return None
    return min(records, key=lambda rec: int(rec["year"]))


def cities_summary(records):
    """How many manuscripts come from each city?"""
    summary = {}
    for rec in records:
        city_name = rec["city"]
        summary[city_name] = summary.get(city_name, 0) + 1
    return summary
    """If two records tie on year, return the one that appears FIRST.
    """
    if not records:
        return None
    return min(records, key=lambda rec: int(rec["year"]))


def cities_summary(records):
    """How many manuscripts come from each city?"""
    summary = {}
    for rec in records:
        city_name = rec["city"]
        summary[city_name] = summary.get(city_name, 0) + 1
    return summary