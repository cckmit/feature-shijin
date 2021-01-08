
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
                'author’scontributions','funding' ,'availabilityofdataandmaterials' ,'ethicsapprovalandconsenttoparticipate' ,
                'consentforpublication' ,'competinginterests' , ]





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
            for search_pmc_id in range(2229793, 2229793+1):
                if str(search_pmc_id) in pmc_id_set:
                    continue
                logging.info(f'追加待采集PMC全文id：{search_pmc_id}')
                url = f'https://www.ncbi.nlm.nih.gov/pmc/articles/{search_pmc_id}'
                yield scrapy.Request(url, callback=self.parse, meta={'search_pmc_id': 'search_pmc_id', 'url_prefix':'https://www.ncbi.nlm.nih.gov'}, headers=const.headers)

        if 'ncbi.nlm.nih.gov' in spider_url:
            if 'invalid article id' in doc('h1').text().lower():
                logging.info(f'当前数据 pmcid 无效，被过滤：{search_pmc_id}')
                return
            meta = response.meta
            self.common_utils.auto_content_link(self, doc, 'a', 'href', meta['url_prefix'])
            self.common_utils.auto_content_link(self, doc, 'img', 'src', meta['url_prefix'])
            search_pmc_id = meta['search_pmc_id']
            fm_citation_elements = doc('.fm-citation')
            issue = fm_citation_elements('.cit').text()
            pm_id = fm_citation_elements('.fm-citation-pmid a').text()
            pmc_id = fm_citation_elements('.fm-citation-pmcid span:nth-child(2)').text()
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
            h2_set = set()
            content = get_content(self, doc, '.no_bottom_margin', h2_set)
            is_continue = True
            for h2 in h2_set:
                if 'abstract' in h2.lower():
                    is_continue = False
            if is_continue:
                content = get_content(self, doc, '.p-first-last', None) + '<br>' + content
            if len(pq(content)('h2')) == 1 and 'references' in pq(content)('h2').text().lower():
                content = ''
            insert_es_data(self, doi, pdf, pmc_id, pm_id, issue, title, spider_url, supplement_str, references_str, search_pmc_id, content)

def get_content(self, doc, label, h2_set):
    content = ''
    content_elements = doc(label)
    for content_element in content_elements.items():
        key = self.str_utils.remove_mark(str=content_element('h2').text().lower())
        logging.info('===>' + key)
        is_keep = True
        for invalid_key in invalid_list:
            if key == invalid_key:
                is_keep = False
                break
        if not is_keep:
            continue
        parent_content_elements = content_element.parent()
        parent_content_elements('.no_top_margin').remove()
        h2_title = parent_content_elements('h2').text()
        if None != h2_set:
            if h2_title in h2_set or '' == h2_title:
                continue
            h2_set.add(h2_title)
        content += parent_content_elements.html()
        while len(parent_content_elements.next()('h2')) == 0 and len(parent_content_elements.next()('h3')) > 0:
            content += parent_content_elements.next().html()
            parent_content_elements = parent_content_elements.next()
    return content

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
    self.es_utils.insert_or_replace(ESIndex.PMC_ARTICLE, d=es_dict)