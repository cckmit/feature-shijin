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
        url = 'https://fuwu.nhsa.gov.cn/ebus/fuwu/api/base/api/drugOptins/queryDrugOptinsInfoDetail'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 5.1.1; LYA-AL10 Build/LYZ28N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36HSABrowser/1.2.2'
        headers['Content-Type'] = 'application/json;charset=UTF-8'
        headers['Accept'] = 'application/json, text/plain, */*'
        headers['orgCode'] = '110101'
        headers['channel'] = 'app'
        headers['Referer'] = 'https://fuwu.nhsa.gov.cn/hsafront/'
        headers['Accept-Language'] = 'zh-CN,en-US;q=0.8'
        headers['X-Requested-With'] = 'cn.hsa.app'
        post_dict = {"data":{"pageNum":1,"pageSize":20,"drugName":"乙磺酸尼达尼布软胶囊","medinsType":1,"province":"北京市","region":"西城区"}}
        yield scrapy.FormRequest(url, method='POST', body=json.dumps(post_dict), callback=self.parse_title, headers=headers )

    def parse_title(self, response):
        resp = response.text
        print(resp)




    def close(spider, reason):
        logging.info('------ cde数据采集完毕，开始统计被删除的数据 -------')

