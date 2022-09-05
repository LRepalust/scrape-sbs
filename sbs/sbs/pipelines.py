# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


def process_item(self, item, spider):
    adapter = ItemAdapter(item)
    if self.db[self.collection_name].find_one({'id': adapter['id']}) != None:
        dado = self.db[self.collection_name].find_one_and_update({'id': adapter['id']})
        ## ----> raise DropItem(f"Duplicate item found: {item!r}") <------
        print(f"Duplicate item found: {dado!r}")
    else:
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
    return item
