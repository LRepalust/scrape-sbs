# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
import re


def remove_reference(value):
    return value.replace('Reference: ', '').strip()


def remove_fwork(value):
    return value.replace('Framework Agreements', '').strip()


def start_date(value):
    p = r"\d*?\s*?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\b\s\d\d\d\d"
    dates = re.finditer(p, value, re.MULTILINE)
    for i, date in enumerate(dates):
        if i == 0:
            return date.group()
        elif i == 1:
            pass


def end_date(value):
    p = r"\d*?\s*?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\b\s\d\d\d\d"
    dates = re.finditer(p, value, re.MULTILINE)
    for i, date in enumerate(dates):
        if i == 1:
            return date.group()
        elif i == 0:
            pass


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
    results = re.findall(p, value)
    for i, result in enumerate(results):
        return result


def get_lot_description(value):
    p = r"\b(?:LOT|Lot)\b\s\d+"
    result = re.search(p, value)
    if result:
        return re.split(p, value)

def no_dot(value):
    p = r"[a-zA-Z]"
    result = re.findall(p, value)
    if result:
        return value







class SbsOverview(scrapy.Item):
    code = scrapy.Field(input_processor=MapCompose(remove_reference), output_processor=TakeFirst())
    organisation = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(input_processor=MapCompose(remove_fwork), output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    framework_title = scrapy.Field(output_processor=TakeFirst())
    start_date = scrapy.Field(input_processor=MapCompose(start_date), output_processor=TakeFirst())
    end_date = scrapy.Field(input_processor=MapCompose(end_date), output_processor=TakeFirst())
    extension_options = scrapy.Field(input_processor=MapCompose(extend), output_processor=TakeFirst())
    lot_number = scrapy.Field(input_processor=MapCompose(get_lot_number))
    lot_description = scrapy.Field(input_processor=MapCompose(get_lot_description, no_dot))
    supplier_name = scrapy.Field()
