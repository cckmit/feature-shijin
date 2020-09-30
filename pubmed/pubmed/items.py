# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PubmedItem(scrapy.Item):
    url = scrapy.Field()
    esid = scrapy.Field()
    full_text_links = scrapy.Field()
    journal_info = scrapy.Field()
    doi = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    abstract_info = scrapy.Field()
    abstract_info_nolabel = scrapy.Field()
    nct_id = scrapy.Field()
    nct_id_str = scrapy.Field()
    secondary_source_id = scrapy.Field()
    mesh_terms = scrapy.Field()
    substances = scrapy.Field()
    url = scrapy.Field()
    esid = scrapy.Field()
    pm_id = scrapy.Field()
    medical_source_url = scrapy.Field()
    spider_wormtime = scrapy.Field()
    publication_types = scrapy.Field()
    spider_wormtime = scrapy.Field()
