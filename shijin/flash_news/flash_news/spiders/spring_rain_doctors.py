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
医生：
tapd网址：https://www.tapd.cn/60111173/prong/stories/view/1160111173001003318?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：https://www.chunyuyisheng.com/pc/doctors/
'''

class Doctor(scrapy.Spider):
    name = 'spring_rain_doctors'
    allowed_domains = []
    start_urls = ['https://www.chunyuyisheng.com/pc/doctors/',]
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

    ## 拿到一级科室的url
    def parse(self,response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        spider_url = response.xpath('//ul[@class="tab-type-one first-clinic j-tab-wrap"]/li/a/@href').extract()
        for url in spider_url:
            url = "https://www.chunyuyisheng.com" + url
            yield scrapy.Request(url=url, callback=self.spring_rain_doctor)

    ## 拿到二级科室的url
    def spring_rain_doctor(self,response):
        urls = response.xpath('//ul[@class="tab-type-one tab-type-free slider-item cur"]/li/a/@href').extract()
        for i in urls:
            second_url = "https://www.chunyuyisheng.com" + i
            yield scrapy.Request(url=second_url, callback=self.spring_rain_doctor_province)

    ## 拿到二级科室下各个省份的url
    def spring_rain_doctor_province(self,response):
        province = response.xpath('//select[@class="province-select city-select"]/option/@value').extract()
        province.pop(0)
        for j in province:
            province_url = "https://www.chunyuyisheng.com" + j
            yield scrapy.Request(url=province_url, callback=self.spring_rain_doctor_deep)

    ## 拿到二级科室下各个省份下各个城市的url
    def spring_rain_doctor_deep(self, response):
        city = response.xpath('//select[@class="city-select"]/option/@value').extract()
        for i in city:
            city_url = "https://www.chunyuyisheng.com" + i
            yield scrapy.Request(url=city_url, callback=self.spring_rain_doctor_deep_page,priority=100)

    ## 列表页用来做翻页  拿到每个详情页的url
    def spring_rain_doctor_deep_page(self,response):
        particulars_url = response.xpath('//div[@class="doctor-list"]/div/div[2]/div[1]/a/@href').extract()
        for i in particulars_url:
            url = 'https://www.chunyuyisheng.com' + i
            yield scrapy.Request(url=url, callback=self.spring_rain_doctor_deep_deep,priority=150)

        next_url = response.xpath('//a[@class="next"]/@href').extract()
        next_url = ''.join(next_url)
        next_url = 'https://www.chunyuyisheng.com' + next_url
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.spring_rain_doctor_deep_page)

    ## 详情页解析
    def spring_rain_doctor_deep_deep(self,response):
        ## 医生名称
        doctor_name = response.xpath('//span[@class="name"]/text()').extract()
        doctor_name = ''.join(doctor_name).strip()
        # print(doctor_name)

        ## 医生职称
        title_of_public_health_technician = response.xpath('//span[@class="grade"]/text()').extract()
        title_of_public_health_technician = ''.join(title_of_public_health_technician).strip()

        ## 医院
        hospital_name = response.xpath('//a[@class="hospital"]/text()').extract()
        hospital_name = ''.join(hospital_name).strip()

        ## 科室
        subject = response.xpath('//a[@class="clinic"]/text()').extract()
        subject = ''.join(subject).strip()

        ## 医生标签
        label = response.xpath('//div[@class="doctor-hospital"]/span/text()').extract()
        label = ''.join(label).strip()

        ## 擅长
        specialize = response.xpath('//div[@class="ui-grid ui-main clearfix"]/div[4]/p/text()').extract()
        specialize = ''.join(specialize).strip()

        ## 简介
        intro = response.xpath('//div[@class="ui-grid ui-main clearfix"]/div[3]/p/text()').extract()
        intro = ''.join(intro).strip()

        ## 医院地址
        hospital_place = response.xpath('//div[@class="ui-grid ui-main clearfix"]/div[5]/p/text()').extract()
        hospital_place = ''.join(hospital_place).strip()
        hospital_place = hospital_place[:hospital_place.rfind("【")]

        logging.info('------- 正在爬取 ------- '+subject)

        mongo_dict = {}
        mongo_dict['doctor_name'] = doctor_name
        mongo_dict['title_of_public_health_technician'] = title_of_public_health_technician
        mongo_dict['hospital_name'] = hospital_name
        mongo_dict['subject'] = subject
        mongo_dict['label'] = label
        mongo_dict['specialize'] = specialize
        mongo_dict['intro'] = intro
        mongo_dict['hospital_place'] = hospital_place
        # logging.info(f'------- @@@insert mongo data ------- {esid}')
        self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.SPRING_RAIN_DOCTOR)
