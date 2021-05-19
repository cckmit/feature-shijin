import logging
import os
import scrapy
from pyquery import PyQuery as pq
from pharmcube_spider import const
from pharmcube_spider.const import  ESIndex
from pharmcube_spider.utils import  es_utils, qiniu_utils
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.file_utils import DownloadFile
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.str_utils import StrUtils


'''
WHO药品名称&结构
IMGT的底层数据来自WHO的Drug Information，数据证据等级高。
网址：https://www.who.int/medicines/publications/druginformation/innlists/en/
'''

class WhoSpider(scrapy.Spider):
    name = 'who'
    allowed_domains = []
    start_urls = ['https://www.who.int/medicines/publications/druginformation/innlists/en/']

    def start_requests(self):
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.md5_utils = MD5Utils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        doc = pq(response.text)
        parse_page(self, doc, 'rec', '.subcol_1-1_1 div.teaser')
        parse_page(self, doc, 'pro', '.subcol_1-1_2 div.teaser')

def parse_page(self, doc, type, label):
    es_arr = []
    for div_element in doc(label).items():
        if div_element('li').size() == 0:
            continue
        year = int(self.str_utils.get_num(div_element('h3').text())[0])
        for li_element in div_element('li').items():
            no = li_element('a').text()
            orig_link = 'https://www.who.int'+li_element('a').attr('href').replace('\r\n', '')
            create_time = self.date_utils.get_timestamp()
            file_name = type+'_' + str(year) +'_'+ no + orig_link[orig_link.rindex('.'):]
            esid = self.md5_utils.get_md5(data=file_name)
            count = es_utils.get_count(ESIndex.WHO_DRUG_INN, queries=Query(QueryType.EQ, 'esid', esid))
            if count >0:
                logging.info(f'当前数据已存在，被过滤: {esid}')
                continue
            es_dict = {}
            es_dict['no'] = no
            es_dict['type'] = type
            es_dict['esid'] = esid
            es_dict['year'] = year
            es_dict['orig_link'] = orig_link
            es_dict['create_time'] = create_time
            es_dict['file_name'] = file_name
            es_dict['file_url'] = orig_link
            es_arr.append(es_dict)

    DownloadFile().download_file(es_arr)
    for es_dict in es_arr:
        file_name = es_dict['file_name']
        local_file_path = f'{const.STORE_PATH}{file_name}'
        if os.path.exists(os.path.join(local_file_path)):
            qiniu_url = qiniu_utils.up_qiniu(const.STORE_PATH + file_name, file_name=file_name, is_keep_file=False)
            if 'pharmcube' in qiniu_url:
                es_dict['pdf_link'] = qiniu_url
        es_dict.pop('file_url')
        logging.info(f'------- insert es data -------{file_name}')
        self.es_utils.insert_or_replace(ESIndex.WHO_DRUG_INN, d=es_dict)
