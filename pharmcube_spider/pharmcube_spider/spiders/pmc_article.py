
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
from pharmcube_spider.utils.str_utils import StrUtils
from pharmcube_spider.utils import common_utils
from pharmcube_spider.const import ESIndex

'''
PMC全文数据抓取需求
从1 ~ 7738640
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7781395/ 
'''

invalid_list = ['acknowledgements','associateddata','acknowledgments','references','dataavailabilitystatement','ethicsstatement',
                'contributor information','biography','footnotes','authorcontributions','conflictofinterest','notes',
                'author’scontributions','funding','availabilityofdataandmaterials','ethicsapprovalandconsenttoparticipate' ,
                'consentforpublication','competinginterests','acknowledgement','authorscontributions' ]

class PmcArticleSpider(scrapy.Spider):
    name = 'pmc_article'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [404],
    }

    def start_requests(self):
        self.es_utils = es_utils
        self.pdf_utils = pdf_utils
        self.str_utils = StrUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.mongo_utils = MongoUtils()
        self.common_utils = common_utils
        const.spider_init(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        doc = pq(response.text.replace('<?xml', ''))
        if 'baidu.com' in spider_url:
            pmc_id_set = set()
            '''
            pages = self.es_utils.get_page(ESIndex.DRUG_PATENT_GOOGLE, page_size=-1, show_fields=['pmc_id'])
            if None != pages:
                for page in pages:
                    pmc_id_set.add(page['pmc_id'])
            '''
            #for id in range(1, 7738640):
            for search_pmc_id in range(1, 100000):  # 7738640 '1234567'.rjust(7,'0')补零
                if str(search_pmc_id) in pmc_id_set:
                    continue
                logging.info(f'追加待采集PMC全文id：{search_pmc_id}')
                url = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{search_pmc_id}'
                yield scrapy.Request(url, callback=self.parse, meta={'search_pmc_id': search_pmc_id, 'url_prefix':'https://www.ncbi.nlm.nih.gov'}, headers=const.headers)

        if 'ncbi.nlm.nih.gov' in spider_url:
            meta = response.meta
            search_pmc_id = meta['search_pmc_id']
            if 'invalid article id' in doc('h1').text().lower():
                logging.info(f'当前数据 pmcid 无效，被过滤：{search_pmc_id}')
                return
            self.common_utils.auto_content_link(self, doc, 'a', 'href', meta['url_prefix'])
            self.common_utils.auto_content_link(self, doc, 'img', 'src', meta['url_prefix'])
            fm_citation_elements = doc('.fm-citation')
            issue = fm_citation_elements('.cit').text()
            pm_id = fm_citation_elements('.fm-citation-pmid a').text()
            pmc_id = fm_citation_elements('.fm-citation-pmcid span:nth-child(2)').text()
            if not self.str_utils.has_nums(str=pmc_id):
                logging.info(f'当前数据 pmcid 无效，被过滤：{search_pmc_id} {pmc_id}')
                return
            doi = fm_citation_elements('.doi a').text()
            title = doc('.content-title').text()
            pdf = ''
            li_elements = doc('.format-menu li')
            for li_element in li_elements.items():
                key = li_element('a').text()
                if key.startswith('PDF'):
                    pdf = li_element('a').attr('href')
            supplement_str = doc('.box-data-suppmats').html() # 附注
            references_str = doc('#reference-list').html() #注释
            content = doc('#maincontent').html()
            insert_es_data(self, doi, pdf, pmc_id, pm_id, issue, title, spider_url, supplement_str, references_str, search_pmc_id, content)

def insert_es_data(self, doi, pdf, pmc_id, pm_id, issue, title, spider_url, supplement_str, references_str,
                   search_pmc_id, content):
    esid = self.md5_utils.get_md5(data=pmc_id)
    es_dict = {}
    es_dict['doi'] = doi
    es_dict['pdf'] = pdf
    es_dict['esid'] = esid
    es_dict['pm_id'] = pm_id
    es_dict['issue'] = issue
    es_dict['title'] = title
    es_dict['pmc_id'] = pmc_id
    es_dict['url'] = spider_url
    es_dict['supplement_str'] = supplement_str
    es_dict['references_str'] = references_str
    es_dict['search_pmc_id'] = search_pmc_id
    es_dict['spider_wormtime'] = self.date_utils.get_timestamp()
    es_dict['content'] = content
    logging.info(f'------- insert es data -------{pmc_id}')
    self.es_utils.insert_or_replace(ESIndex.PMC_ARTICLE, d=es_dict)
