import scrapy
import logging
from pyquery import PyQuery as pq
from pharmcube_spider import const
from pharmcube_spider.const import ESIndex
from pharmcube_spider.utils import es_utils, file_utils
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings

'''
新闻专线：
* 美通社 https://www.prnewswire.com/news-releases/health-latest-news/health-latest-news-list/?page=1&pagesize=100
* 全球通 

* 商业资讯 http://www.businesswire.com/portal/site/home/news/industry/?vnsId=31250

'''


class NewswireSpider(scrapy.Spider):
    name = 'newswire'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.md5_utils = MD5Utils()
        self.file_utils = file_utils
        self.mongo_utils = MongoUtils()
        self.redis_server = from_settings(get_project_settings())
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        spider_url = response.url
        doc = pq(response.text)
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            wait_url_list = []
            #wait_url_list.append({'prefix_url':'https://www.prnewswire.com', 'spider_page_index':4, 'source': '美通社', 'url': 'https://www.prnewswire.com/news-releases/health-latest-news/health-latest-news-list/?page=0&pagesize=100'})
            #wait_url_list.append({'prefix_url':'https://www.businesswire.com', 'spider_page_index':11, 'source': '商业资讯', 'url': 'https://www.businesswire.com/portal/site/home/template.PAGE/news/industry/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31250&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1595674800000*B1598318073021*DgroupByDate*G0*M31250*N1001385&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken'})
            for wait_url in wait_url_list:
               url = wait_url['url']
               source = wait_url['source']
               prefix_url = wait_url['prefix_url']
               spider_page_index = wait_url['spider_page_index']
               #for page_index in range(1, spider_page_index):
               for page_index in range(3, spider_page_index):
                   if '美通社' == source:
                       url = url.replace('page=0', f'page={page_index}')
                   elif '商业资讯' == source:
                       url = url.replace('DgroupByDate*G0', f'DgroupByDate*G{page_index}')
                   yield scrapy.Request(url, callback=self.parse, meta={'source': source, 'type': 'list', 'prefix_url': prefix_url}, headers=const.headers)




        if 'source' in meta and 'list' == meta['type']:
            source = meta['source']
            if '美通社' == meta['source']:
                h3_elements = doc('.col-sm-8:first h3')
                for h3_element in h3_elements.items():
                    yield from add_spider_url(self, h3_element('a'), '美通社', scrapy, meta)
            elif '商业资讯' == source:
                li_elements = doc('#headlines')('li')
                for li_element in li_elements.items():
                    yield from add_spider_url(self, li_element('a'), '商业资讯', scrapy, meta)
            return

        if 'source' in meta and '商业资讯' == meta['source'] and 'detail' == meta['type']:
            title = meta['title']
            spider_publish_time_str = doc('.bw-release-timestamp')('time').attr('datetime').split('T')[0]
            spider_publish_time = self.date_utils.unix_time(date_str=spider_publish_time_str)
            content_elements = doc('.bw-release-main')
            content_elements('meta').remove()
            insert_es_dict(self, title, spider_publish_time_str, spider_publish_time, content_elements, spider_url, '商业资讯')

        if 'source' in meta and '美通社' == meta['source'] and 'detail' == meta['type']:
            title = meta['title']
            doc('.divOverflow').remove()
            spider_publish_time_str = doc('.mb-no').text()
            spider_publish_time_str = spider_publish_time_str[0:spider_publish_time_str.rindex(',')].strip()
            spider_publish_time = self.date_utils.unix_time_en(date_str=spider_publish_time_str)
            content_elements = doc('.release-body')
            insert_es_dict(self, title, spider_publish_time_str, spider_publish_time,content_elements, spider_url, '美通社')

def check_es_data(self, title, href, source):
    queries = Query.queries(Query(QueryType.EQ, 'source', source), Query(QueryType.EQ, 'url', href))
    es_count = self.es_utils.get_count(ESIndex.NEWS, queries=queries)
    if es_count >0:
        logging.info(f'当前数据已存在ES，被过滤：{title}')
        return True
    return False

def add_spider_url(self, a_elements, source, scrapy, meta):
    title = a_elements.text()
    href = a_elements.attr('href')
    if not href.startswith('http'):
        href = meta['prefix_url'] + href
    if not check_es_data(self, title, href, source):
        logging.info(f'追加待采集新闻：{title}')
        yield scrapy.Request(href, callback=self.parse, meta={'source': source, 'title':title, 'type': 'detail'}, headers=const.headers)

def insert_es_dict(self, title, spider_publish_time_str, spider_publish_time, content_elements, url, source):
    content_nolabel = content_elements.text()
    content = content_elements.html()
    spider_wormtime = self.date_utils.get_timestamp()
    esid = self.md5_utils.get_md5(data=title+content)
    es_dict = {}
    es_dict['esid'] = esid
    es_dict['spider_publish_time'] = spider_publish_time
    es_dict['spider_publish_time_str'] = spider_publish_time_str
    es_dict['content'] = content
    es_dict['content_nolabel'] = content_nolabel
    es_dict['url'] = url
    es_dict['state'] = '新增'
    es_dict['is_delete'] = '否'
    es_dict['source'] = source
    es_dict['channel_name'] = '新药动态'
    es_dict['spider_wormtime'] = spider_wormtime
    logging.info(f'------- insert es data -------{esid} {ESIndex.NEWS}')
    if self.es_utils.insert_or_replace(ESIndex.NEWS, esid, d=es_dict):
        self.redis_server.lpush(const.RedisKey.NEWS_LIST, esid)
        if '商业资讯' == source or '美通社' == source or '全球通' == source: #给锦秋扔一份
            queries = Query.queries(Query(QueryType.EQ, 'title', title), Query(QueryType.EQ, 'resource', source), Query(QueryType.EQ, 'url', url))
            es_count = self.es_utils.get_count(ESIndex.INVEST_NEWS, queries=queries)
            if es_count > 0:
                return
            es_obj = {}
            es_obj['esid'] = esid
            es_obj['title'] = title
            es_obj['resource'] = source
            es_obj['spider_resource'] = source
            es_obj['publish_date'] = spider_publish_time
            es_obj['is_publish'] = '0'
            es_obj['label'] = ''
            es_obj['amount'] = ''
            es_obj['invester'] = ''
            es_obj['tag_id'] = ''
            es_obj['company'] = ''
            es_obj['is_new'] = '1'
            es_obj['value'] = ''
            es_obj['tag'] = ''
            es_obj['url'] = url
            es_obj['is_spider'] = 1
            es_obj['content'] = content
            es_obj['spider_wormtime'] = spider_wormtime
            logging.info(f'------- insert es data -------{esid} {ESIndex.INVEST_NEWS}')
            if self.es_utils.insert_or_replace(ESIndex.INVEST_NEWS, es_obj ):
                self.redis_server.lpush(const.RedisKey.INVEST_NEWS_LIST, esid)
