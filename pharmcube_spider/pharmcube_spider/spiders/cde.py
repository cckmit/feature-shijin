import logging
import re
import ast
import json
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


class CdeSpider(scrapy.Spider):
    name = 'cde'
    allowed_domains = []

    def __init__(self, spider_test=None, *args, **kwargs):
        logging.info(f'=======>{spider_test}')
        self.spider_test = spider_test
        super(CdeSpider, self).__init__(*args, **kwargs)
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.pdf_utils = pdf_utils
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.redis_server = from_settings(get_project_settings())
        const.spider_init(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):


        es_dict_1 = {}
        es_dict_1['esid'] = '689d3225519a38ba5db6adbb343e10f9'
        original_approvals_list_1 = [{"id":"1e96d0e3e2cfcb43d2ad9db118bb9ae4","action_date":1419177600000,"submission":"ORIG-1","action_type":"Approval","submission_classification":"","rPOS":"N/A; Orphan","lrlppi":[{"orig_link":"https://www.accessdata.fda.gov/drugsatfda_docs/label/2014/125554lbl.pdf","Label (PDF)":"http://spider.pharmcube.com/718e308d4572962bd388b7b9d99ffe1e.pdf"},{"orig_link":"https://www.accessdata.fda.gov/drugsatfda_docs/appletter/2014/125554Orig1s000ltr.pdf","Letter (PDF)22222222":"http://spider.pharmcube.com/eaf58adcf7d2dab7c68257deb925daa.pdf"}],"notes":"","review":[{"orig_link":"https://www.accessdata.fda.gov/drugsatfda_docs/nda/2014/125554Orig1s000Approv.pdf","file_name":"11111111","file_name_url":"http://spider.pharmcube.com/6f8fb9a08d0a033116c3fb37c709dde3.pdf"}]}]
        es_dict_1['original_approvals'] = str(json.dumps(original_approvals_list_1).encode('utf-8').decode('unicode_escape'))
        logging.info(f'------- update es data original_approvals  689d3225519a38ba5db6adbb343e10f9 ------- ')
        es_utils.update('drug_us_drugs', d=es_dict_1)




    def close(spider, reason):
        logging.info('------ cde数据采集完毕，开始统计被删除的数据 -------')

