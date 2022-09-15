# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from utilities import remove_reference, remove_fwork, get_start_date, get_end_date, extend, get_lot_number, \
    get_lot_description, get_single_supplier, no_dot

class SbsItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    code_in = MapCompose(remove_reference)
    category_in = MapCompose(remove_fwork)
    start_date_in = MapCompose(get_start_date)
    end_date_in = MapCompose(get_end_date)
    extension_options_in = MapCompose(extend)
    lot_number_in = MapCompose(get_lot_number)
    lot_description_in = MapCompose(get_lot_description, no_dot)




class SbsItems(scrapy.Item):
    code = scrapy.Field()
    organisation = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    framework_title = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    extension_options = scrapy.Field()
    lot_number = scrapy.Field()
    lot_description = scrapy.Field()
    supplier_name = scrapy.Field()
