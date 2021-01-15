import logging
import re
import ast
import json
import time
import scrapy
from pharmcube_spider import const
from pharmcube_spider.utils import pdf_utils
from pyquery import PyQuery as pq
from pharmcube_spider.utils import es_utils
from pharmcube_spider.utils.es_utils import OpType
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from pharmcube_spider.utils.str_utils import StrUtils

from pharmcube_spider.utils import file_utils

from pharmcube_spider.utils.file_utils import DownloadFile

'''
FDA-紫皮书 索引：drug_us_purple					
https://purplebooksearch.fda.gov/advanced-search					


、FDA-CBER


'''
class CdeSpider(scrapy.Spider):
    name = 'cde-1'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.str_utils = StrUtils()
        self.pdf_utils = pdf_utils
        self.es_utils = es_utils
        self.file_utils = file_utils
        self.mongo_utils = MongoUtils()
        self.redis_server = from_settings(get_project_settings())
        const.spider_init(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')






