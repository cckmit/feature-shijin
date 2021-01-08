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
from pharmcube_spider.utils import common_utils

'''
新闻专线：
* 美通社 https://www.prnewswire.com/news-releases/health-latest-news/health-latest-news-list/?page=1&pagesize=100
* 全球通 http://globenewswire.com/Search/NewsSearch?industry=Health%20Care
* 商业资讯 http://www.businesswire.com/portal/site/home/news/industry/?vnsId=31250

'''


class NewswireSpider(scrapy.Spider):
    name = 'newswire'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        self.md5_utils = MD5Utils()
        self.file_utils = file_utils
        self.date_utils = DateUtils()
        self.mongo_utils = MongoUtils()
        self.common_utils = common_utils
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
            #wait_url_list.append({'prefix_url':'http://www.globenewswire.com', 'spider_page_index':6, 'source': '全球通', 'url': 'http://www.globenewswire.com/Search/NewsSearch?icb=4000&page=0','cookie':'__pnrculture=en-us; GNWTracker=bae2f9b9-ecb0-45b1-a3c8-dd374db97929; visid_incap_1215959=vabwBQR3TNKxXbDBGrQjT9e1iVwAAAAAQUIPAAAAAAC+A8BxYkcaaW0fUZD65OLT; __utmz=202784462.1552528856.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); visid_incap_1816097=gqDL/4QQTvWr1gMSRDx4Wd21iVwAAAAAQUIPAAAAAABSXE39InYetsZ5YpEn++RN; visid_incap_1819681=W8O7VLeqSYqozzZZrnArw3nuiVwAAAAAQUIPAAAAAADBRqsNWo5+aHXuQFvS8fcb; ASP.NET_SessionId=irdtygby4zlrmxrkut1z30o4; __RequestVerificationToken_Lw__=dbkSC7OFHv19YZCDLJlW8cOj6G5PvbRTsrZHPxa/wTndTR26ZXqGc9bLhFRWG1iccWykavLiEstagLpL8qgW9SJFyU++cvK8XONzKLRIXNQuikDHRoPKhQsG+qaq9TY9yQYDWw==; __utmc=202784462; nlbi_1816097=UE/FP3iqHRqKofYjdiQ7sgAAAAD3ffx8Rn9U8/rkr2chqKLG; __atuvc=2%7C31; nlbi_1819681=8PftbAqDlQ7SRmAXjdoNhwAAAADxD9/psy9tZ7YwIqfeg2pP; nlbi_1215959=amZAc5qeBDcaaHohVgkgzwAAAADZTO+nJKOpjK7NYk/6lB9f; incap_ses_219_1215959=/nNtORkkMyNAItqEkQ4KA5SnQl0AAAAA8ONoV8p1sXL7jtkzmivarg==; __utma=202784462.137265757.1552528856.1564630238.1564649365.9; incap_ses_962_1819681=CBslSKejLCuSyGPDsbZZDZunQl0AAAAAgIXEyx2J7FWaS/LkHeHdRQ==; incap_ses_962_1816097=YENqNhLemQ2SyWPDsbZZDZynQl0AAAAAF/d0kvQAxb1+/cyvXpnv3Q==; TBMCookie_331718653375599340=656914001564650947gdQggfKuZ7fcB7z21cJopO4SKL0=; __utmt=1; modelcookie=%7b%22SearchId%22%3anull%2c%22PageIndex%22%3a3%2c%22NewKeyword%22%3a%22Refine+Results%22%2c%22PubDate%22%3anull%2c%22FilteredOrganizations%22%3a%5b%5d%2c%22Parameters%22%3a%7b%22StartIndex%22%3a0%2c%22SearchQuery%22%3a%22%22%2c%22SearchKeywords%22%3a%5b%5d%2c%22MaxRows%22%3a10%2c%22SummaryReplacePre%22%3a%22PNR_HIGHLIGHT_START%22%2c%22SummaryReplacePost%22%3a%22PNR_HIGHLIGHT_END%22%2c%22DateRange%22%3anull%2c%22PrivateCompanies%22%3anull%2c%22NewsroomReleases%22%3afalse%2c%22Fields%22%3a%5b%7b%22Type%22%3a%7b%22IsField%22%3atrue%2c%22Code%22%3a%22Icb%22%2c%22Label%22%3a%22Industry%22%7d%2c%22SearchValue%22%3a%224000%22%2c%22FacetCount%22%3anull%7d%5d%7d%2c%22PagerSetting%22%3anull%2c%22Listing%22%3anull%2c%22HasSaveSearchesEntitlement%22%3afalse%2c%22SavedSearchName%22%3anull%2c%22ReaderAccountSearches%22%3anull%2c%22IsMultimediaRelease%22%3afalse%2c%22IsExistingSearch%22%3afalse%7d; __utmb=202784462.20.10.1564649365'})
            #wait_url_list.append({'prefix_url':'https://www.prnewswire.com', 'spider_page_index':4, 'source': '美通社', 'url': 'https://www.prnewswire.com/news-releases/health-latest-news/health-latest-news-list/?page=0&pagesize=100'})
            #wait_url_list.append({'prefix_url':'https://www.businesswire.com', 'spider_page_index':11, 'source': '商业资讯', 'url': 'https://www.businesswire.com/portal/site/home/template.PAGE/news/industry/?javax.portlet.tpst=08c2aa13f2fe3d4dc1b6751ae1de75dd&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_vnsId=31250&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_08c2aa13f2fe3d4dc1b6751ae1de75dd_ndmHsc=v2*A1595674800000*B1598318073021*DgroupByDate*G0*M31250*N1001385&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken'})
            for wait_url in wait_url_list:
               url = wait_url['url']
               source = wait_url['source']
               prefix_url = wait_url['prefix_url']
               spider_page_index = wait_url['spider_page_index']
               #for page_index in range(1, spider_page_index):
               for page_index in range(1, 2):
                   if '美通社' == source or '全球通' == source:
                       url = url.replace('page=0', f'page={page_index}')
                   elif '商业资讯' == source:
                       url = url.replace('DgroupByDate*G0', f'DgroupByDate*G{page_index}')
                   headers = const.headers
                   if 'cookie' in wait_url:
                       cookie = wait_url['cookie']
                       cookie_temp = cookie[cookie.index('PageIndex%22%3a3'): cookie.index('%2c%22NewKeyword')]
                       headers['Cookie'] = cookie.replace(cookie_temp, f'PageIndex%22%3a{page_index}')
                   yield scrapy.Request(url, callback=self.parse, meta={'source': source, 'type': 'list', 'prefix_url': prefix_url}, headers=headers)

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
            elif '全球通' == source:
                a_elements = doc('.results-link h1')('a')
                for a_element in a_elements.items():
                    yield from add_spider_url(self, a_element('a'), '全球通', scrapy, meta)
            return

        if 'type' in meta and 'detail' == meta['type']:
            self.common_utils.auto_content_link(self, doc, 'a', 'href', meta['prefix_url'])
            self.common_utils.auto_content_link(self, doc, 'img', 'src', meta['prefix_url'])

        if 'source' in meta and '全球通' == meta['source'] and 'detail' == meta['type']:
            title = meta['title']
            spider_publish_time_str = doc('time').attr('datetime').split('T')[0]
            spider_publish_time = self.date_utils.unix_time(date_str=spider_publish_time_str)
            content_elements = doc('#content-L2')
            insert_es_dict(self, title, spider_publish_time_str, spider_publish_time, content_elements, spider_url, '全球通')

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
            insert_es_dict(self, title, spider_publish_time_str, spider_publish_time, content_elements, spider_url, '美通社')

def check_es_data(self, title, href, source):
    queries = Query.queries(Query(QueryType.EQ, 'source', source), Query(QueryType.EQ, 'url', href))
    es_count = self.es_utils.get_count(ESIndex.NEWS, queries=queries)
    if es_count > 0:
        logging.info(f'当前数据已存在ES，被过滤：{title}')
        return True
    return False

def add_spider_url(self, a_elements, source, scrapy, meta):
    prefix_url = meta['prefix_url']
    title = a_elements.text()
    href = a_elements.attr('href')
    href = self.common_utils.auto_url(prefix_url, href)
    if not check_es_data(self, title, href, source):
        logging.info(f'追加待采集新闻：{title}')
        yield scrapy.Request(href, callback=self.parse, meta={'source': source, 'title':title, 'type': 'detail', 'prefix_url':prefix_url}, headers=const.headers)

def insert_es_dict(self, title, spider_publish_time_str, spider_publish_time, content_elements, url, source):
    content_nolabel = content_elements.text()
    content = content_elements.html()
    spider_wormtime = self.date_utils.get_timestamp()
    esid = self.md5_utils.get_md5(data=title+content)
    es_dict = {}
    es_dict['esid'] = esid
    es_dict['title'] = title
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
    if self.es_utils.insert_or_replace(ESIndex.NEWS, d=es_dict):
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
            if self.es_utils.insert_or_replace(ESIndex.INVEST_NEWS, es_obj):
                self.redis_server.lpush(const.RedisKey.INVEST_NEWS_LIST, esid)
