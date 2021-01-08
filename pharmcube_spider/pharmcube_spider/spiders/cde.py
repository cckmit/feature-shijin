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
        pages = self.es_utils.get_page("base_company", queries=Query(QueryType.NE, 'is_delete', '是'), page_index=-1,
                                       show_fields=['name', 'name_en', 'name_jp', 'name_used', 'short_name',
                                                    'short_name_en', 'company_variant', 'id'])
        type = 'AG'
        for page in pages:
            id = page['id']
            name = page['name']
            name_en = page['name_en']
            name_jp = page['name_jp']
            name_used = page['name_used']
            short_name = page['short_name']
            short_name_en = page['short_name_en']
            company_variant = page['company_variant']
            print()



        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        doc = pq(response.text)

        logging.info(f'接收到传输的参数：{self.spider_test}')
        if 'baidu.com' in spider_url:
            pages = es_utils.get_page('drug_us_drugs', page_size=-1, show_fields=['original_approvals', 'supplement', 'label_arr'])
            for page in pages:
                esid = page['esid']
                if "60f416d99a72a8c26adf9e1c871faec0" == esid:
                    if 'label_arr' in page:
                        label_arr_list = []
                        label_arr_es_list = ast.literal_eval(page['label_arr'])
                        for label_arr_es in label_arr_es_list:
                            submission = label_arr_es['submission']
                            submission_classification_approvaltype = label_arr_es[
                                'submission_classification_approvaltype']
                            action_date = label_arr_es['action_date']
                            action_date_str = DateUtils().defined_format_time(action_date, '%m/%d/%Y')
                            id = MD5Utils().get_md5(
                                action_date_str + submission + submission_classification_approvaltype)
                            label_arr_es['id'] = id
                            label_arr_list.append(label_arr_es)
                        es_dict = {}
                        es_dict['esid'] = esid
                        es_dict['label_arr'] = str(json.dumps(label_arr_list).encode('utf-8').decode('unicode_escape'))
                        logging.info(f'------- update es data label_arr -------{esid} ')
                        es_utils.update('drug_us_drugs', d=es_dict)

                    if 'supplement' in page:
                        supplement_list = []
                        supplement_es_list = ast.literal_eval(page['supplement'])
                        for supplement_es in supplement_es_list:
                            submission = supplement_es['submission']
                            submission_classification = supplement_es['submission_classification']
                            action_date = supplement_es['action_date']
                            action_date_str = DateUtils().defined_format_time(action_date, '%m/%d/%Y')
                            id = MD5Utils().get_md5(action_date_str + submission + submission_classification)
                            supplement_es['id'] = id
                            supplement_list.append(supplement_es)
                        es_dict = {}
                        es_dict['esid'] = esid
                        es_dict['supplement'] = str(
                            json.dumps(supplement_list).encode('utf-8').decode('unicode_escape'))
                        logging.info(f'------- update es data supplement -------{esid}')
                        es_utils.update('drug_us_drugs', d=es_dict)

                    if 'original_approvals' in page:
                        original_approvals_list = []
                        original_approvals_es_list = ast.literal_eval(page['original_approvals'])
                        for original_approvals_es in original_approvals_es_list:
                            submission = original_approvals_es['submission']
                            action_type = original_approvals_es['action_type']
                            action_date = original_approvals_es['action_date']
                            action_date_str = DateUtils().defined_format_time(action_date, '%m/%d/%Y')
                            id = MD5Utils().get_md5(action_date_str + submission + action_type)
                            original_approvals_es['id'] = id
                            original_approvals_list.append(original_approvals_es)
                        es_dict = {}
                        es_dict['esid'] = esid
                        es_dict['original_approvals'] = str(json.dumps(original_approvals_list).encode('utf-8').decode('unicode_escape'))
                        logging.info(f'------- update es data original_approvals -------{esid}')
                        es_utils.update('drug_us_drugs', d=es_dict)



            '''

           
                pass
            '''


    def close(spider, reason):
        logging.info('------ cde数据采集完毕，开始统计被删除的数据 -------')

