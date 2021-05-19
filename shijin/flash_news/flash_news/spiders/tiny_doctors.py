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
微医生：
tapd网址：https://www.tapd.cn/60111173/prong/stories/view/1160111173001003318?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：https://www.guahao.com/search/expert?q=内科
'''

class Doctor(scrapy.Spider):
    name = 'tiny_doctors'
    allowed_domains = []
    start_urls = ['https://www.guahao.com/',]
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    ## 拿到各种病的url
    def parse(self,response):
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        spider_url = response.xpath('//div[@class="nav-subcats-wrapper"]/div/div/ul/li/p/a/@href').extract()
        for url in spider_url:
            # print(url)
            yield scrapy.Request(url=url, callback=self.tiny_doctor)

    ## 拿到各个省份+病的url
    def tiny_doctor(self,response):
        urls = response.xpath('//div[@class="J_BottomInnerModuleContent"]/div[3]/div[2]/div/a/@href').extract()
        for i in urls:
            n = 0
            while n < 38:
                n += 1
                url = i + "/p" + str(n)
                yield scrapy.Request(url=url, callback=self.tiny_doctor_deep,priority=100)

    ## 列表页
    def tiny_doctor_deep(self, response):
        urll = response.url
        # print(urll)
        url = response.xpath('//div[@class="g-doctor-items to-margin"]/ul/li/div[2]/a/@href').extract()
        for i in url:
            yield scrapy.Request(url=i, callback=self.tiny_doctor_deep_deep,priority=150)

    ## 详情页解析
    def tiny_doctor_deep_deep(self,response):

        ## 医生名称
        doctor_name = response.xpath('//strong[@class="J_ExpertName"]/text()').extract()
        doctor_name = ''.join(doctor_name).strip()

        ## 医生职称
        title_of_public_health_technician = response.xpath('//div[@class="detail word-break"]/h1/span[1]/text()').extract()
        title_of_public_health_technician = ''.join(title_of_public_health_technician).strip()

        ## 医生职称2
        title_of_public_health_technician_2 = response.xpath('//div[@class="detail word-break"]/h1/span[3]/text()').extract()
        title_of_public_health_technician_2 = ''.join(title_of_public_health_technician_2).strip()

        ## 医院1
        hospital_name_1 = response.xpath('//div[@class="hospital"]/p[1]/a[1]/text()').extract()
        hospital_name_1 = ''.join(hospital_name_1).strip()

        ## 科室1
        subject_1 = response.xpath('//div[@class="hospital"]/p[1]/a[2]/text()').extract()
        subject_1 = ''.join(subject_1).strip()

        ## 医院2
        hospital_name_2 = response.xpath('//div[@class="hospital"]/p[2]/a[1]/text()').extract()
        hospital_name_2 = ''.join(hospital_name_2).strip()

        ## 科室2
        subject_2 = response.xpath('//div[@class="hospital"]/p[2]/a[2]/text()').extract()
        subject_2 = ''.join(subject_2).strip()

        ## 适应症
        indication = response.xpath('//div[@class="detail word-break"]/div[2]/a[1]/text()').extract()
        indication = ''.join(indication).strip()

        ## 适应症2
        indication2 = response.xpath('//div[@class="detail word-break"]/div[2]/a[2]/text()').extract()
        indication2 = ''.join(indication2).strip()

        ## 适应症3
        indication3 = response.xpath('//div[@class="detail word-break"]/div[2]/a[3]/text()').extract()
        indication3 = ''.join(indication3).strip()

        ## 适应症4
        indication4 = response.xpath('//div[@class="detail word-break"]/div[2]/a[4]/text()').extract()
        indication4 = ''.join(indication4).strip()

        ## 适应症5
        indication5 = response.xpath('//div[@class="detail word-break"]/div[2]/a[5]/text()').extract()
        indication5 = ''.join(indication5).strip()

        ## 适应症6
        indication6 = response.xpath('//div[@class="detail word-break"]/div[2]/a[6]/text()').extract()
        indication6 = ''.join(indication6).strip()

        ## 擅长
        specialize = response.xpath('//div[@class="goodat"]/span/text()').extract()
        specialize = ''.join(specialize).strip()

        ## 简介
        intro = response.xpath('//div[@class="about"]/a/@data-description').extract()
        intro = ''.join(intro).strip()

        logging.info('------- 正在爬取 ------- '+doctor_name)

        mongo_dict = {}
        mongo_dict['doctor_name'] = doctor_name
        mongo_dict['title_of_public_health_technician'] = title_of_public_health_technician
        mongo_dict['title_of_public_health_technician_2'] = title_of_public_health_technician_2
        mongo_dict['hospital_name_1'] = hospital_name_1
        mongo_dict['subject_1'] = subject_1
        mongo_dict['hospital_name_2'] = hospital_name_2
        mongo_dict['subject_2'] = subject_2
        mongo_dict['indication'] = indication
        mongo_dict['indication2'] = indication2
        mongo_dict['indication3'] = indication3
        mongo_dict['indication4'] = indication4
        mongo_dict['indication5'] = indication5
        mongo_dict['indication6'] = indication6
        mongo_dict['specialize'] = specialize
        mongo_dict['intro'] = intro
        self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.TINY_DOCTOR)
