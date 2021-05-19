# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlashNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    esid = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    timeStamp = scrapy.Field()
    contents = scrapy.Field()
    ress = scrapy.Field()

class Wit_FinanceItem(scrapy.Item):
    hs = scrapy.Field()
    name = scrapy.Field()
    timee = scrapy.Field()
    contents = scrapy.Field()
    ress = scrapy.Field()