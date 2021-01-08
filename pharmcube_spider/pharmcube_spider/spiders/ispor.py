import logging
import re
import scrapy
from pyquery import PyQuery as pq
from pharmcube_spider import const
from pharmcube_spider.const import  ESIndex, RedisKey
from pharmcube_spider.utils import  es_utils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings


'''
数据需求：ISPOR增刊数据爬虫
数据来源：
Value in Health：https://www.ispor.org/publications/journals/value-in-health/vih-archives
Value in Health Regional Issues：https://www.ispor.org/publications/journals/value-in-health-regional-issues/issue-archives 
'''

esid_set = set()

class IsporSpider(scrapy.Spider):
    name = 'ispor'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'pharmcube_spider.middlewares.CustomMiddleware': 1,# 指定下载中间件
        },
    }

    def start_requests(self):
        self.es_utils = es_utils
        self.md5_utils = MD5Utils()
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.mongo_utils = MongoUtils()
        self.redis_server = from_settings(get_project_settings())
        read_es_history(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        doc = pq(response.text)

        if 'baidu.com' in spider_url:
            wait_url_list = []
            wait_url_list.append({'url': 'https://www.valueinhealthjournal.com/issues', 'url_prefix': 'https://www.valueinhealthjournal.com'})
            wait_url_list.append({'url': 'https://www.valuehealthregionalissues.com/issues', 'url_prefix': 'https://www.valuehealthregionalissues.com'})
            for wait_url in wait_url_list:
                url = wait_url['url']
                url_prefix = wait_url['url_prefix']
                logging.info(f'追加待采集网址： {url}')
                yield scrapy.Request(url, callback=self.parse, meta={'url_prefix': url_prefix}, headers=const.headers)

        if spider_url.endswith('issues'):
            a_elements = doc('.supp-loi #issueName')('a')
            yield from parse_title(self, meta, a_elements, scrapy)

            if len(a_elements) == 0: #post
                a_elements = doc('a')
                yield from parse_title(self, meta, a_elements, scrapy)

            if spider_url.endswith('.com/issues'):
                widget_id_str = doc('.group-header-ha-supplement a')[0].attrib['href']
                widget_id = widget_id_str[widget_id_str.index('widget=') + 7:widget_id_str.rindex('#')]
                if spider_url.endswith('valueinhealthjournal.com/issues'):
                    journal_code = 'jval'
                    pb_context = ';website:website:jval-site;page:string:List of Issues;ctype:string:Journal Content;requestedJournal:journal:jval;pageGroup:string:Publication Page;journal:journal:jval;wgroup:string:Migrated Websites;product:product:elsevier\:product\:ha'
                    yield from add_url(self, scrapy, '200', widget_id, meta, pb_context, journal_code)
                    yield from add_url(self, scrapy, '201', widget_id, meta, pb_context, journal_code)
                else:
                    journal_code = 'vhri'
                    pb_context = ';page:string:List of Issues;website:website:vhri-site;ctype:string:Journal Content;journal:journal:vhri;pageGroup:string:Publication Page;wgroup:string:Migrated Websites;requestedJournal:journal:vhri;product:product:elsevier\:product\:ha'
                    yield from add_url(self, scrapy, '201', widget_id, meta, pb_context, journal_code)

        if '/issue/' in spider_url:
            a_elements = doc('.articleCitation h3 a')
            for a_element in a_elements.items():
                title = a_element.text()
                full_text_link = auto_complete_url(a_element, meta)
                esid = self.md5_utils.get_md5(data=full_text_link)
                if esid in esid_set:
                    logging.info(f'当前数据已经采集，被过滤：{title}')
                    continue
                meta['esid'] = esid
                yield scrapy.Request(full_text_link, callback=self.parse, meta=meta, headers=const.headers)

        if spider_url.endswith('fulltext'):
            author = []
            es_obj = {}
            esid =meta['esid']
            title = doc('.article-header__title').text()
            doi = doc('.article-header__doi__value').text().replace('https://doi.org/', '').strip()
            if self.str_utils.is_blank(doi) or self.str_utils.is_blank(title):
                logging.info(f'当前数据 doi 或 title 为空，数据被过滤：{spider_url}')
                return

            es_obj['title'] = title
            article_header_meta = doc('.article-header__meta')
            article_header_meta('span.article-header__journal').remove()
            article_header_meta('span.article-header__sep').remove()
            issue = article_header_meta.text()
            for author_element in doc('.loa__item.author').items():
                name = author_element('a.loa__item__name').text()
                affiliation = author_element('div.article-header__info__group__body').text()
                author_obj = {}
                author_obj['name'] = name
                author_obj['affiliation'] = affiliation
                author.append(author_obj)
            abstract = ''
            abstract_nolabel = ''
            id_set = set()
            article_elements = doc('.article__sections section')
            for article_element in article_elements.items():
                id = article_element('section').attr('id')
                if None == id or (id in id_set):
                    continue
                id_set.add(id)
                abstract += '<br>' + str(article_element)
                abstract_nolabel += '\n' +article_element.text()
            es_obj['issue'] = issue
            search_obj = re.search(r'[a-zA-Z]{1,10}[ ][\d]{1,2}[,][ ][\d]{4}', issue, re.M | re.I)
            publication = 'ISPOR (Value in health)'
            if 'valuehealthregionalissues' == spider_url[spider_url.index('www.') + 4:spider_url.index('.com')]:
                publication = 'ISPOR (Value in health regional issues)'
            if search_obj:
                data_str = search_obj.group()
                pub_date = self.date_utils.unix_time_en(date_str=data_str)
                es_obj['pub_date'] = pub_date
            es_obj['author'] = str(author)
            if not self.str_utils.is_blank(str=abstract_nolabel):
                abstract = '<div>'+abstract+'</div>'
                abstract_nolabel = '<div>'+abstract_nolabel+'</div>'
            es_obj['abstract'] = abstract
            es_obj['abstract_nolabel'] = abstract_nolabel
            es_obj['full_text_link'] = spider_url
            es_obj['doi'] = doi
            es_obj['esid'] = esid
            es_obj['publication'] = publication
            es_obj['spider_wormtime'] = self.date_utils.get_timestamp()
            logging.info(f'------- insert es data -------{esid}')
            self.es_utils.insert_or_replace(ESIndex.ISPOR_SUPPLEMENT, d=es_obj)
            self.redis_server.lpush(RedisKey.CLINICAL_ISPOR_SUPPLEMENT_ESIDS, esid)

def read_es_history(self):
    pages = self.es_utils.get_page(ESIndex.ISPOR_SUPPLEMENT, page_size=-1, show_fields=['esid'])
    for page in pages:
        esid = page['esid']
        esid_set.add(esid)

def auto_complete_url(a_element, meta):
    href = a_element.attr('href')
    if not href.startswith('http'):
        href = meta['url_prefix'] + href
    return href

def add_url(self, scrapy, decade, widget_id, meta, pb_context, journal_code):
    data_dict = {}
    data_dict['decade'] = decade
    url = 'https://www.valueinhealthjournal.com/pb/widgets/loi/issues'
    data_dict['pbContext'] = pb_context
    data_dict['journalCode'] = journal_code
    data_dict['widgetId'] = widget_id
    yield scrapy.FormRequest(url, formdata=data_dict, callback=self.parse, meta=meta, headers=const.headers)

def parse_title(self, meta, a_elements, scrapy):
    for a_element in a_elements.items():
        title = a_element.text()
        href = auto_complete_url(a_element, meta)
        logging.info(f'追加待采集网址： {title}')
        yield scrapy.Request(href, callback=self.parse, meta=meta, headers=const.headers)
