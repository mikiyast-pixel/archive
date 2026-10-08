"""Questions we ask the Archive."""


def count_before(records, year):
    """How many manuscripts were written strictly BEFORE `year`?"""
    count = 0
    for item in records:
        rec_year = int(item["year"])
        if rec_year < year:
            count = count + 1
    return count


def find_by_city(records, city):
    """Every record whose city matches `city`, case-insensitively. Order is preserved."""
    target = city.strip().lower()
    result = []
    for item in records:
        item_city = item["city"].strip().lower()
        if item_city == target:
            result.append(item)
    return result


def oldest(records):
    """The record with the smallest year. Return None if empty.

    If two records tie on year, return the one that appears FIRST.
    """
    if len(records) == 0:
        return None

    oldest_record = None
    smallest_year = None

    for item in records:
        current_year = int(item["year"])
        if smallest_year == None or current_year < smallest_year:
            smallest_year = current_year
            oldest_record = item

    return oldest_record


def cities_summary(records):
    """How many manuscripts come from each city?"""
    summary = {}
    for item in records:
        city_name = item["city"]
        if city_name in summary:
            summary[city_name] = summary[city_name] + 1
        else:
            summary[city_name] = 1
    return summary
