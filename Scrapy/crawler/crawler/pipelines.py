# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class NintendoPipeline(object):

    def process_item(self, item, spider):
        if item['title']:
            item["title"] = clean_spaces(item["title"])
            return item
        else:
            raise DropItem(f"Missing title in {item}")


def clean_spaces(string):
    if string:
        return " ".join(string.split())