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

"""
 * 爬取巨潮资讯信息: http://www.cninfo.com.cn/new/index
 * A股票、港股、新三板（全国中小板）

"""

class CninfoSpider(scrapy.Spider):
    name = 'cninfo'
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
            '''
         List<Query> list = new ArrayList<>(); // 补充资讯的 pdf 链接
		list.add(new Query(true,new Query(QueryType.IN,"event_type", "注册进展", "研发进展"),
				new Query(QueryType.EQ, "source", "资讯"), new Query(QueryType.EQ, "new_source", "巨潮资讯网")));
		List<Map<String, Object>> search_list = service.getList("drug_earth_news_stat", list, null, null, -1,  null);
            '''
            queries = Query.queries(Query(QueryType.EQ, 'channel_name', '医药自媒体'), Query(QueryType.GE, 'spider_wormtime', 1604851200000),and_perator=False)
            self.es_utils.get_page()

            pass
