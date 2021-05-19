import logging
import scrapy
from flash_news.utils import es_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news import const
from flash_news.utils.date_utils import DateUtils

'''
好大夫在线：
tapd网址：https://www.tapd.cn/60111173/prong/stories/view/1160111173001003318?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：https://www.haodf.com/
'''

class Doctor(scrapy.Spider):
    name = 'good_doctors'
    allowed_domains = []
    start_urls = ['https://www.haodf.com/keshi/list.htm',]
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        # self.esid_list = read_esid(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    ## 主要爬取的网站
    def parse(self,response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        if 'haodf.com' in spider_url:
            url = "https://www.haodf.com/keshi/list.htm"
            yield scrapy.Request(url=url, callback=self.good_doctor)

    ## 拿到各个科室
    def good_doctor(self,response):
        url = response.xpath('//div[@class="m_ctt_green"]/ul/li/a/@href').extract()
        for i in url:
            url_deep = "https://www.haodf.com/"+i[:-4]+"/daifu_all_1.htm"
            # print(url_deep)
            yield scrapy.Request(url=url_deep, callback=self.good_doctor_deep,priority=100)

    ## 列表页
    def good_doctor_deep(self, response):
        url = response.xpath('//td[@class="good_doctor_list_td"]/table/tr[1]/td[2]/a[1]/@href').extract()
        for i in url:
            yield scrapy.Request(url=i, callback=self.good_doctor_deep_deep,priority=150)
        next_url = response.xpath('//table[@class="bluegpanel"]/tr[3]/td[2]/table[2]/tr/td/div/a[8]/@href').extract()
        next_url = ''.join(next_url)
        next_url = 'https://haoping.haodf.com' + next_url
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.good_doctor_deep)

    ## 详情页解析
    def good_doctor_deep_deep(self,response):
        ## 医生名称
        doctor_name = response.xpath('//div[@class="profile-txt"]/h1/text()').extract()
        doctor_name = ''.join(doctor_name).strip()

        ## 医生职称
        title_of_public_health_technician = response.xpath('//div[@class="profile-txt"]/span/text()').extract()
        title_of_public_health_technician = ''.join(title_of_public_health_technician).strip()

        ## 医院1
        hospital_name_1 = response.xpath('//ul[@class="doctor-faculty-wrap"]/li[1]/a[1]/text()').extract()
        hospital_name_1 = ''.join(hospital_name_1).strip()

        ## 科室1
        subject_1 = response.xpath('//ul[@class="doctor-faculty-wrap"]/li[1]/a[2]/text()').extract()
        subject_1 = ''.join(subject_1).strip()

        ## 医院2
        hospital_name_2 = response.xpath('//ul[@class="doctor-faculty-wrap"]/li[2]/a[1]/text()').extract()
        hospital_name_2 = ''.join(hospital_name_2).strip()

        ## 科室2
        subject_2 = response.xpath('//ul[@class="doctor-faculty-wrap"]/li[2]/a[2]/text()').extract()
        subject_2 = ''.join(subject_2).strip()

        ## 擅长
        specialize = response.xpath('//div[@class="content-wrap expertise-content-wrap"]/p/text()').extract()
        specialize = ''.join(specialize).strip()

        ## 简介
        intro = response.xpath('//div[@class="content-wrap brief-content-wrap"]/p/text()').extract()
        intro = ''.join(intro).strip()

        logging.info('------- 正在爬取 ------- '+doctor_name)

        mongo_dict = {}
        mongo_dict['doctor_name'] = doctor_name
        mongo_dict['title_of_public_health_technician'] = title_of_public_health_technician
        mongo_dict['hospital_name_1'] = hospital_name_1
        mongo_dict['subject_1'] = subject_1
        mongo_dict['hospital_name_2'] = hospital_name_2
        mongo_dict['subject_2'] = subject_2
        mongo_dict['specialize'] = specialize
        mongo_dict['intro'] = intro
        self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.GOOG_DOCTOR)
