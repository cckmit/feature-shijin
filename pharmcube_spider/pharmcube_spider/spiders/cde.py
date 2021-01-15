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


class CdeSpider(scrapy.Spider):
    name = 'cde'
    allowed_domains = []

    def __init__(self, spider_test=None, *args, **kwargs):
        logging.info(f'=======>{spider_test}')
        self.spider_test = spider_test
        super(CdeSpider, self).__init__(*args, **kwargs)
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.str_utils = StrUtils()
        self.pdf_utils = pdf_utils
        self.date_utils = DateUtils()
        self.file_utils = file_utils
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.redis_server = from_settings(get_project_settings())
        const.spider_init(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        if 'baidu.com' in spider_url:
            base_info_url = f'https://purplebooksearch.fda.gov/api/v1/products?_={self.date_utils.get_timestamp()}'
            headers = const.headers
            headers['Cookie'] = '_ga=GA1.2.657327046.1610440747; _gid=GA1.2.522349874.1610596542; _gat_gtag_UA_150233968_1=1'
            headers['Referer'] = 'https://purplebooksearch.fda.gov/advanced-search'
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Referer'] = 'https://purplebooksearch.fda.gov/advanced-search'
            yield scrapy.Request(base_info_url, callback=self.parse, headers=headers )

        else:
            pass






    def close(spider, reason):
        logging.info('------ cde数据采集完毕，开始统计被删除的数据 -------')

