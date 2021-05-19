import copy
import logging
import scrapy
import re
import time
import datetime
from flash_news.utils import es_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news import const
from flash_news.const import ESIndex
from flash_news.utils.es_utils import Query, QueryType
from flash_news.utils.date_utils import DateUtils

def read_keysword(self):
    keyword_list = []
    mongo_list = self.mongo_utils.find_all(coll_name=const.MongoTables.BASE_CHANNEL)
    for mongo_data in mongo_list:
        keyword = mongo_data['keyword']
        keyword_list.append(keyword)

    mongo_list2 = self.mongo_utils.find_all(coll_name=const.MongoTables.INDUSTRY_NEWS_TYPE)
    type_dict = {}
    for mongo_data in mongo_list2:
        type = mongo_data['type']
        keywords = mongo_data['keywords']
        for keyword in keywords:
            type_dict[keyword] = type
    return keyword_list,type_dict

def read_esid(self):
    esid_list = []
    mongo_list = self.mongo_utils.find_all(coll_name=const.MongoTables.FLASH_NEW)
    for mongo_esid in mongo_list:
        esid = mongo_esid['esid']
        esid_list.append(esid)
    return esid_list

class FlashNewSpider(scrapy.Spider):
    name = 'flash_new'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        self.esid_list = read_esid(self)
        self.keyword_list,self.type_dict = read_keysword(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self,response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        if 'baidu.com' in spider_url:
            mongo_list3 = self.mongo_utils.find_all(coll_name=const.MongoTables.INDUSTRY_NEWS_SPIDER_PARAMS)
            for mongo_data in mongo_list3:
                url = mongo_data['url']
                source = mongo_data['source']

                #todo test
                if '格隆汇' in source:
                    yield scrapy.Request(url=url, callback=self.longji_remit, meta={'source': copy.deepcopy(source)})
                if '智通财经' in source:
                    yield scrapy.Request(url=url, callback=self.wit_finance, meta={'source': copy.deepcopy(source)})
                if '界面新闻' in source:
                    yield scrapy.Request(url=url, callback=self.interface_news, meta={'source': copy.deepcopy(source)})
                if '东方财富网' in source:
                    yield scrapy.Request(url=url, callback=self.east_treasure, meta={'source': copy.deepcopy(source)})
                if '新浪财经-港股' in source:
                    yield scrapy.Request(url=url, callback=self.sina_finance, meta={'source': copy.deepcopy(source)})
                if '生物谷' in source:
                    yield scrapy.Request(url=url, callback=self.biology_grain, meta={'source': copy.deepcopy(source)})

    # 格隆汇列表页
    def longji_remit(self,response):
        source = response.meta['source']
        url = response.xpath('//section[@class="article-content"]/a[1]/@href').extract()
        list_url = []
        for i in url:
            url = 'https://www.gelonghui.com' + i
            list_url.append(url)
            for detail_url in list_url:
                esid = self.md5_utils.lstrip_zero_get_md5(data=detail_url)
                if esid in self.esid_list:
                    logging.info('------- 当前文章已采集，被过滤 ------- ' + esid)
                    continue
                if check_es_data(self, esid=esid, detail_url=detail_url):
                    continue
                yield scrapy.Request(url=detail_url, callback=self.longji_remitt, meta={"esid": esid})

    # 格隆汇详情页
    def longji_remitt(self, response):
        esid = response.meta['esid']
        url = response.url
        title = re.sub('\(.*?\)', '', ''.join(response.xpath('//h1[@class="title"]/text()').extract()))
        time_now = ''.join(response.xpath('//span[@class="date"]/text()').extract())
        now_time = datetime.datetime.now()
        spider_publish_date = now_time.strftime('%Y-%m-%d %H:%M:%S')
        if '分钟' in time_now:
            delta = datetime.timedelta(minutes=int(''.join(re.findall('^[0-9><=]', time_now))))
            spider_publish_date = (now_time - delta).strftime('%Y-%m-%d %H:%M:%S')
        elif '小时' in time_now:
            delta = datetime.timedelta(hours=int(''.join(re.findall('^[0-9><=]', time_now))))
            spider_publish_date = (now_time - delta).strftime('%Y-%m-%d %H:%M:%S')
        timeArray = time.strptime(spider_publish_date, "%Y-%m-%d %H:%M:%S")
        publish_date = int(time.mktime(timeArray))
        context_nolabel = ''.join(response.xpath('//article[@class="main-news article-with-html"]/p/span/text()').extract())
        if len(context_nolabel) == 0:
            context_nolabel = response.xpath('//article[@class="main-news article-with-html"]/p/text()').extract()
            context_nolabel = ''.join(context_nolabel)
        res = response.text
        ress = re.findall(r'<article class="main-news article-with-html.*?article-details', res)
        context = ''.join(ress)[:-32]
        summary = response.xpath('//article[@class="main-news article-with-html"]/p/span[1]/text()').extract()
        if len(summary) == 0:
            summary = response.xpath('//article[@class="main-news article-with-html"]/p[1]/text()').extract()
        summary = ''.join(summary).strip()
        spider_wormtime = self.date_utils.get_timestamp()
        spider_location = '公告摘要'
        source = '格隆汇'
        type = '其他'
        # print(111111111111111)
        keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location,context_nolabel, spider_publish_date, spider_wormtime, type)

    # 智通财经列表页
    def wit_finance(self,response):
        source = response.meta['source']
        url = response.xpath('//div[@class="tap-body list-a list-art"]/dl/dd/h2/a/@href').extract()
        list_url = []
        for i in url:
            url = "https://www.zhitongcaijing.com" + i
            list_url.append(url)
            for detail_url in list_url:
                esid = self.md5_utils.lstrip_zero_get_md5(data=detail_url)
                if esid in self.esid_list:
                    logging.info('------- 当前文章已采集，被过滤 ------- ' + esid)
                    continue
                if check_es_data(self, esid=esid, detail_url=detail_url):
                    continue
                yield scrapy.Request(url=detail_url, callback=self.wit_financee, meta={"esid": esid})

    # 智通财经详情页
    def wit_financee(self,response):
        esid = response.meta['esid']
        url = response.url
        title = re.sub('\(.*?\)', '', ''.join(response.xpath('//div[@class="detail-m"]/article/h1/text()').extract()).strip())
        timee = ''.join(response.xpath('//div[@class="h-30 line-h-30 color-c size-14 padding-b10"]/text()').extract()).strip()
        spider_publish_date = timee.replace('年', '-').replace('月', '-').replace('日', '')
        timeArray = time.strptime(spider_publish_date, "%Y-%m-%d %H:%M:%S")
        publish_date = int(time.mktime(timeArray))
        context_nolabel = ''.join(response.xpath('//div[@class="detail-m"]/article/p/text()').extract()).strip()
        context = ''.join(re.findall(r'<p>.*?        </article>', response.text))[:-18]
        summary = ''.join(response.xpath('//div[@class="detail-m"]/article/p[1]/text()').extract()).strip()
        spider_wormtime = self.date_utils.get_timestamp()
        spider_location = '资讯-推荐'
        source = '智通财经'
        type = '其他'
        keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location,context_nolabel, spider_publish_date, spider_wormtime, type)

    # # 界面新闻列表页
    def interface_news(self,response):
        source = response.meta['source']
        url = response.xpath('//div[@class="item-main"]/p/a/@href').extract()
        list_url = []
        for i in url:
            i = i[32:]
            url = "https://www.jiemian.com/article/" + i
            list_url.append(url)
            for detail_url in list_url:
                esid = self.md5_utils.lstrip_zero_get_md5(data=detail_url)
                if esid in self.esid_list:
                    logging.info('------- 当前文章已采集，被过滤 ------- ' + esid)
                    continue
                if check_es_data(self, esid=esid, detail_url=detail_url):
                    continue
                yield scrapy.Request(url=detail_url, callback=self.interface_newss, meta={"esid": esid})

    # 界面新闻详情页
    def interface_newss(self,response):
        esid = response.meta['esid']
        url = response.url
        title = re.sub('\(.*?\)', '', ''.join(response.xpath('//div[@class="article-header"]/h1/text()').extract()).strip())
        timee = ''.join(response.xpath('//span[@class="date"]/text()').extract()).strip()
        spider_publish_date = timee.replace('/', '-').replace('/', '-').replace('/', '')
        timeArray = time.strptime(spider_publish_date, "%Y-%m-%d %H:%M")
        publish_date = int(time.mktime(timeArray))
        context_nolabel = ''.join(response.xpath('//div[@class="article-content"]/p/text()').extract()).strip()
        context = ''.join(re.findall(r'<p>.*?</p>', response.text))
        summary = ''.join(response.xpath('//div[@class="article-content"]/p[1]/text()').extract()).strip()
        spider_wormtime = self.date_utils.get_timestamp()
        spider_location = '24小时滚动快讯'
        source = '界面新闻'
        type = '其他'
        keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location,context_nolabel, spider_publish_date, spider_wormtime, type)

    # 东方财富网列表页
    def east_treasure(self,response):
        source = response.meta['source']
        list_url = response.xpath('//div[@class="media-content"]/h2/a/@href').extract()
        for detail_url in list_url:
            esid = self.md5_utils.lstrip_zero_get_md5(data=detail_url)
            if esid in self.esid_list:
                logging.info('------- 当前文章已采集，被过滤 ------- ' + esid)
                continue
            if check_es_data(self,esid=esid, detail_url=detail_url):
                continue
            yield scrapy.Request(url=detail_url, callback=self.east_treasuree, meta={"esid":esid})
    # 东方财富网详情页
    def east_treasuree(self, response):
        esid = response.meta['esid']
        url = response.url
        title = re.sub('\(.*?\)', '', ''.join(response.xpath('//div[@class="newsContent"]/h1/text()').extract()).strip())
        timee = ''.join(response.xpath('//div[@class="time-source"]/div/text()').extract()).strip()[:17]
        spider_publish_date = timee.replace('年', '-').replace('月', '-').replace('日', '')
        timeArray = time.strptime(spider_publish_date, "%Y-%m-%d %H:%M")
        publish_date = int(time.mktime(timeArray))
        contents = response.xpath('//div[@class="b-review"]/text()').extract()
        context_nolabel = re.sub('\【.*?\】','',re.sub('\（.*?\）','',''.join(contents).strip()))
        context = ''.join(re.findall(r'<div class="b-review">.*?</div>', response.text))
        summary = ''.join(response.xpath('//div[@class="b-review"][1]/text()').extract()).strip()
        spider_wormtime = self.date_utils.get_timestamp()
        spider_location = '港股公司新闻'
        source = '东方财富网'
        type = '其他'
        keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location,context_nolabel, spider_publish_date, spider_wormtime, type)

    # 新浪财经-港股列表页
    def sina_finance(self, response):
        source = response.meta['source']
        list_url = response.xpath('//ul[@class="list_009"]/li/a/@href').extract()
        for detail_url in list_url:
            esid = self.md5_utils.lstrip_zero_get_md5(data=detail_url)
            if esid in self.esid_list:
                logging.info('------- 当前文章已采集，被过滤 ------- ' + esid)
                continue
            if check_es_data(self, esid=esid, detail_url=detail_url):
                continue
            yield scrapy.Request(url=detail_url, callback=self.sina_financee, meta={"esid": esid})

    # 新浪财经-港股详情页
    def sina_financee(self, response):
        esid = response.meta['esid']
        url = response.url
        title = re.sub('\(.*?\)', '', ''.join(response.xpath('//h1[@class="main-title"]/text()').extract()).strip())
        timee = ''.join(response.xpath('//div[@class="date-source"]/span/text()').extract()).strip()
        spider_publish_date = timee.replace('年', '-').replace('月', '-').replace('日', '')[:16]
        timeArray = time.strptime(spider_publish_date, "%Y-%m-%d %H:%M")
        publish_date = int(time.mktime(timeArray))
        contents = response.xpath('//div[@class="article"]/p/text()').extract()
        contents = re.sub('\（.*?\）', '', ''.join(contents).strip())
        context_nolabel = re.sub('\【.*?\】', '', contents)
        context = ''.join(re.findall(r'<p>.*?</p>', response.text))
        summary = ''.join(response.xpath('//div[@class="article"]/p[1]/text()').extract()).strip()
        spider_wormtime = self.date_utils.get_timestamp()
        spider_location = '港股公司新闻'
        source = '新浪财经-港股'
        type = '其他'
        keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location, context_nolabel,spider_publish_date, spider_wormtime, type)

    # 生物谷列表页
    def biology_grain(self, response):
        source = response.meta['source']
        list_url = response.xpath('//div[@class="cntx"]/h4/a/@href').extract()
        for detail_url in list_url:
            detail_url = detail_url.strip()
            esid = self.md5_utils.lstrip_zero_get_md5(data=detail_url)
            if esid in self.esid_list:
                logging.info('------- 当前文章已采集，被过滤 ------- ' + esid)
                continue
            if check_es_data(self, esid=esid, detail_url=detail_url):
                continue
            yield scrapy.Request(url=detail_url, callback=self.biology_grainn, meta={"esid": esid})

    # 生物谷详情页
    def biology_grainn(self, response):
        esid = response.meta['esid']
        url = response.url
        title = re.sub('\(.*?\)', '', ''.join(response.xpath('//div[@class="title5"]/h1/text()').extract()).strip())
        timee = ''.join(response.xpath('//div[@class="title5"]/p/text()').extract()).strip()
        timee = timee[timee.find('2'):]
        spider_publish_date = ''.join(timee).strip()
        timeArray = time.strptime(timee, "%Y-%m-%d %H:%M")
        publish_date = int(time.mktime(timeArray))
        contents = ''.join(response.xpath('//div[@class="text3"]/p/text()').extract()).strip()
        context_nolabel = ''.join(contents[:contents.rfind('/')]).strip()
        context = ''.join(re.findall(r'<p>.*?</p>', response.text))
        spider_wormtime = self.date_utils.get_timestamp()
        summary = ''.join(response.xpath('//div[@class="text3"]/p[1]/text()').extract()).strip()
        spider_location = '最新资讯'
        source = '生物谷'
        type = "其他"
        keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location,context_nolabel, spider_publish_date, spider_wormtime, type)

def check_es_data(self,esid,detail_url):
    es_count = self.es_utils.get_count(ESIndex.NEWS, queries=Query(QueryType.EQ, 'esid', esid))
    if es_count > 0:
        logging.info('------- 当前文章已采集，被过滤es数据库 ------- ' + esid )
        return True
    return False

def insert_es_data(self, esid, title, url, source, context, summary, publish_date, spider_location,context_nolabel,spider_publish_date,spider_wormtime,type):
    es_dict = {}
    es_dict["url"] = url
    es_dict["esid"] = esid
    es_dict["type"] = type
    es_dict["title"] = title
    es_dict["source"] = source
    es_dict["context"] = context
    es_dict["summary"] = summary
    es_dict["publish_date"] = publish_date
    es_dict["spider_location"] = spider_location
    es_dict["context_nolabel"] = context_nolabel
    es_dict["spider_publish_date"] = spider_publish_date
    es_dict["spider_wormtime"] = spider_wormtime
    logging.info("------- insert es data -------" + esid + "\t" + title)
    self.es_utils.insert_or_replace('industry_news', d=es_dict)

def insert_mongo_data(self, esid):
    mongo_dict = {}
    mongo_dict['esid'] = esid
    logging.info(f'------- insert mongo data ------- {esid}')
    self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.FLASH_NEW)

def keywords_comparison(self, esid, title, url, source, context, summary, publish_date, spider_location, context_nolabel,spider_publish_date, spider_wormtime, type):
    is_break = False
    for keyword in self.keyword_list:
        if keyword not in context_nolabel:
            continue
        is_break = True
        for type_temp in self.type_dict.keys():
            if type_temp not in context_nolabel:
                continue
            type = self.type_dict[type_temp]
            # is_break = True
            break
        break
    if is_break:
        insert_es_data(self, esid, title, url, source, context, summary, publish_date, spider_location, context_nolabel,spider_publish_date, spider_wormtime, type)
    else:
        insert_mongo_data(self, esid)


