# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class StarcrawlerItem(scrapy.Item):

    def initField(self):
        default = ""
        item = {}
        item["name"] = default
        item["avatar"] = default
        item["gender"] = default
        item["nationality"] = default
        item["birthday"] = default
        item["native_place"] = default
        item["constellation"] = default
        item["hobby"] = default
        item["job"] = default
        item["height"] = default
        item["weight"] = default
        item["introduction"] = default
        item["photos"] = default
        return item

class AstrocrawlerItem(scrapy.Item):
        pass
