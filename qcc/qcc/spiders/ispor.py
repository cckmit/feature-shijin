
import ast
import re
import scrapy
import logging
import requests
from qcc.spiders import const
from pyquery import PyQuery as pq
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from qcc.spiders.const import ESIndex, RedisKey
from qcc.utils import es_utils
from qcc.utils.date_utils import DateUtils
from qcc.utils.md5_utils import MD5Utils
from qcc.utils.mongo_utils import MongoUtils
from qcc.utils.str_utils import StrUtils

'''
数据需求：ISPOR增刊数据爬虫
数据来源：
Value in Health：https://www.ispor.org/publications/journals/value-in-health/vih-archives
Value in Health Regional Issues：https://www.ispor.org/publications/journals/value-in-health-regional-issues/issue-archives 
'''
# todo 临时，后期需要删除
esid_set = set()

def read_es_history(self):
    pages = self.es_utils.get_page(ESIndex.ISPOR_SUPPLEMENT, page_size=-1, show_fields=['esid'])
    for page in pages:
        esid = page['esid']
        esid_set.add(esid)

class IsporSpider(scrapy.Spider):
    name = 'ispor'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

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
            spider_url_arr = []
            spider_url_arr.append({'url': 'https://www.ispor.org/publications/journals/value-in-health/vih-archives/', 'url_part': 'viharticles'})
            spider_url_arr.append({'url': 'https://www.ispor.org/publications/journals/value-in-health-regional-issues/issue-archives/', 'url_part': 'vihriarticles'})

            url_part = spider_url_arr[0]['url_part']
            if 'viharticles' == url_part:  # todo 补完历史数据之后，后期需要删除翻页操作
                for page_index in range(1, 11):
                    link = spider_url_arr[0]['url'] + str(page_index)
                    logging.info(f'追加列表页采集的页数 {page_index}')
                    yield scrapy.Request(link, callback=self.parse,meta={'url_part': url_part, 'page_index': page_index},headers=const.headers)
            else:
                for page_index in range(1, 2): # todo 补完历史数据之后，后期需要删除翻页操作
                    link = spider_url_arr[0]['url'] + str(page_index)
                    logging.info(f'追加列表页采集的页数 {page_index}')
                    yield scrapy.Request(link, callback=self.parse, meta={'url_part': url_part, 'page_index': page_index}, headers=const.headers)

        if 'vih-archives' in spider_url or 'issue-archives' in spider_url:
            yield from parse_vih_archives(self, meta, doc, scrapy, spider_url)

        if '/issue/' in spider_url:
            url_part = meta['url_part']
            issue_id = doc('#journal-app journal-issue').attr('issue-id')
            meta['skip'] = 0
            meta['issue_id'] = issue_id
            link = f'https://www.ispor.org/api/journals/{url_part}?$orderby=SectionOrder%20asc&$filter=ParentId%20eq%20{issue_id}&$skip=0&$top=10'
            logging.info(f'追加待采集的URL:{issue_id} 当前略过条数：0')
            yield scrapy.Request(link, callback=self.parse, meta=meta, headers=const.headers)

        if 'viharticles' in spider_url or 'vihriarticles' in spider_url:
            yield from parse_viharticles(self, meta=meta, response=response, spider_url=spider_url, scrapy=scrapy)

def parse_viharticles(self, meta, response, spider_url, scrapy):
    skip = meta['skip'] + 10
    issue_id = meta['issue_id']
    url_part = meta['url_part']
    results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
    if len(results['value']) != 0 and len(results['value']) == 10:
        logging.info(f'当前资讯信息需要进行翻页操作 {issue_id}\t{skip}')
        link = f'https://www.ispor.org/api/journals/{url_part}?$orderby=SectionOrder%20asc&$filter=ParentId%20eq%20{issue_id}&$skip={skip}&$top=10'
        meta['skip'] = skip
        logging.info(f'追加待采集的URL  {issue_id} 当前略过之前的条数：{skip}')
        yield scrapy.Request(link, callback=self.parse, meta=meta, headers=const.headers)

    for result in results['value']:
        es_obj = {}
        doi = result['Doi']
        es_obj['doi'] = doi
        full_text_link = result['FullContentURL']
        esid = self.md5_utils.get_md5(data=full_text_link)
        if esid in esid_set:
            logging.info(f'当前数据已经采集，被过滤：{full_text_link}')
            continue
        author = []
        resp = download_page(full_text_link)
        doc = pq(resp.text)
        title = doc('.article-header__title').text()
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
        if 'valuehealthregionalissues' == full_text_link[full_text_link.index('www.') + 4:full_text_link.index('.com')]:
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
        es_obj['full_text_link'] = full_text_link
        es_obj['esid'] = esid
        es_obj['publication'] = publication
        es_obj['spider_wormtime'] = self.date_utils.get_timestamp()
        logging.info(f'------- insert es data -------{esid}')
        self.es_utils.insert_or_replace(ESIndex.ISPOR_SUPPLEMENT, d=es_obj)
        self.redis_server.lpush(RedisKey.CLINICAL_ISPOR_SUPPLEMENT_ESIDS, esid)


def parse_vih_archives(self, meta, doc, scrapy, spider_url):
    page_index = meta['page_index']
    for li_element in doc('ul.border-first li').items():
        title = li_element('span').text().lower()
        if 'issue s' not in title:
            logging.info(f'当前标题不包含指定关键词，被过滤：{title}\t{spider_url}\t{page_index}')
            continue
        year = int(li_element('h4').text().strip().split(',')[0].strip())
        href = li_element('a').attr('href')
        meta['year'] = year
        meta['title_url'] = spider_url
        logging.info(f'追加待采集的URL  {year}\t{title}')
        yield scrapy.Request(href, callback=self.parse, meta=meta, headers=const.headers)


def download_page(url):
    attempts = 0
    success = False
    resp = '<html>'
    while attempts < 6 and not success:
        try:
            logging.info(f'下载详情页：{url}')
            session = requests.Session()
            resp = session.get(url=url, headers=const.headers, timeout=60)  # 维护校验的cookie当前网页地址采集异常
            session.close()
            return resp
            success = True
        except Exception as err:
            print(err)
            logging.info(f'------- 下载详情页失败：{url}，重试中：{attempts} 次数 -------')
            if attempts > 6:
                logging.info(f'------- 当前URL超过指定次数，被过滤： {url} {attempts} -------')
                break
        attempts += 1
    return resp