import re

def remove_reference(value):
    return value.replace('Reference: ', '').strip()


def remove_fwork(value):
    return value.replace('Framework Agreements', '').strip()


def get_start_date(value):
    p = r"\d*?\s*?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(" \
        r"?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\b\s\d\d\d\d"
    dates = re.finditer(p, value, re.MULTILINE)
    for i, date in enumerate(dates):
        if i == 0:
            return date.group()


def get_end_date(value):
    p1 = r"\d*?\s*?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(" \
         r"?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\b\s(2022|2023|2024|2025|2026|2027|2028|2029)"
    dates1 = re.finditer(p1, value, re.MULTILINE)

    for i, date1 in enumerate(dates1):
        if i == 0:
            return date1.group()


def extend(value):
    p1 = r"\d+\s\bmonth(s*)\b"
    p2 = r"(exten)"
    result1 = re.search(p1, value)
    result2 = re.search(p2, value)
    if result2:
        if result1:
            return result1.group()
        elif '1 year' in value:
            return '12 months'
        elif '2023' and '2025' in value:
            return '24 months'
        elif '2024' and '2026' in value:
            return '24 months'
        elif '2027' and '2023' in value:
            return '48 months'
        else:
            pass


def get_lot_number(value):
    p = r"\b(?:LOT|Lot)\b\s\d+"
    lot_numbers = re.findall(p, value, re.MULTILINE)
    for i, numbers in enumerate(lot_numbers):
        return numbers


def get_lot_description(value):
    p = r"\b(?:LOT|Lot)\b\s\d+"
    result = re.search(p, value, re.MULTILINE)
    if result:
        return re.split(p, value, re.MULTILINE)


def no_dot(value):
    p = r"[a-zA-Z]"
    result = re.findall(p, value)
    if result:
        return value


def get_single_supplier(value):
    pass