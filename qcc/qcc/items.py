# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QccItem(scrapy.Item):
    name = scrapy.Field() #公司名称

