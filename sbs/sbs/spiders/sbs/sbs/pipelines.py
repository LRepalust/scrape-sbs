# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem



class SbsPipeline:
    def process_item(self, item, spider):
        def process_item(self, item, spider):
            if not (all(item.values())):
                raise (DropItem())
            else:
                return item
