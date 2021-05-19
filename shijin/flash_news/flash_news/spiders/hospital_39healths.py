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

'''
39健康网 医院：
tapd网址：https://www.tapd.cn/60111173/prong/stories/view/1160111173001003303?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：http://yyk.39.net/beijing/hospitals/
'''

class Doctor(scrapy.Spider):
    name = 'hospital_39healths'
    allowed_domains = []
    start_urls = ['http://yyk.39.net/beijing/hospitals/',]
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    ## 拿到各省的url 翻页
    def parse(self,response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        spider_url = response.xpath('//div[@class="localtab tab"]/div[2]/ul/li/a/@href').extract()
        spider_url.pop(0)
        for url in spider_url:
            city = "".join(re.findall("','(.*?)','",url))
            n = 0
            while n < 100:
                n += 1
                url = "http://yyk.39.net/"+city+"/hospitals/"+"c_p{}/".format(n)
                # print(url)
                yield scrapy.Request(url=url, callback=self.hospital_39health)

    ## 列表页
    def hospital_39health(self,response):
        urls = response.xpath('//ul[@class="hospitalfulllist"]/li/a/@href').extract()
        for i in urls:
            second_url = "http://yyk.39.net" + i
            # print(second_url)
            yield scrapy.Request(url=second_url, callback=self.hospital_39health_detail,priority=100)

    ## 详细介绍
    def hospital_39health_detail(self,response):
        url = response.xpath('//section[@class="block detailnav"]/ul/li[2]/a/@href').extract()
        url = "".join(url)
        url = "http://yyk.39.net" + url
        # print(url)
        yield scrapy.Request(url=url, callback=self.hospital_39health_deep,priority=150)

    ## 详情页
    def hospital_39health_deep(self,response):
        ## 医院名称
        hospital_name = response.xpath('//div[@class="hospitalinfo"]/h1/text()').extract()
        hospital_name = ''.join(hospital_name).strip()
        print(hospital_name)

        ## 医院等级
        hospital_label_item = response.xpath('//i[@class="tag_orange"]/text()').extract()
        hospital_label_item = ''.join(hospital_label_item).strip()
        print(hospital_label_item)

        ## 专科性质
        specialized_nature = response.xpath('//i[@class="tag_green"]/text()').extract()
        specialized_nature = ''.join(specialized_nature).strip()
        print(specialized_nature)

        ## 别名
        anothe_name = response.xpath('//div[@class="hospitalinfo"]/p/text()').extract()
        anothe_name = ''.join(anothe_name).strip()[3:]
        print(anothe_name)

        ## 盈利性质
        state_operated_nature = response.xpath('//ul[@class="hospitaltags"]/li[2]/b/text()').extract()
        state_operated_nature = ''.join(state_operated_nature).strip()
        print(state_operated_nature)

        ## 主任医师数量
        chief_physician_num = response.xpath('//div[@class="introduction"]/dl[1]/b[1]/text()').extract()
        chief_physician_num = ''.join(chief_physician_num).strip()
        print(chief_physician_num)

        ## 副主任医师数量
        associate_chief_physician_num = response.xpath('//div[@class="introduction"]/dl[1]/b[2]/text()').extract()
        associate_chief_physician_num = ''.join(associate_chief_physician_num).strip()
        print(associate_chief_physician_num)

        ## 床位数
        bednum = response.xpath('//div[@class="introduction"]/dl[1]/b[3]/text()').extract()
        bednum = ''.join(bednum).strip()
        print(bednum)

        ## 门诊量
        outpatient_amount = response.xpath('//div[@class="introduction"]/dl[1]/b[4]/text()').extract()
        outpatient_amount = ''.join(outpatient_amount).strip()
        print(outpatient_amount)

        ## 电话
        tel = response.xpath('//div[@class="introduction"]/dl[2]/dd/text()').extract()
        tel = ''.join(tel).strip()
        print(tel)

        ## 医院地址
        address = response.xpath('//div[@class="introduction"]/dl[3]/dd/text()').extract()
        address = ''.join(address).strip()
        print(address)

        ## 分院
        branch = response.xpath('//div[@class="introduction"]/dl[4]/dd/text()').extract()
        branch = ''.join(branch).strip()
        print(branch)

        # print(hospital_name,hospital_label_item,specialized_nature,anothe_name,state_operated_nature,chief_physician_num,associate_chief_physician_num,bednum,outpatient_amount,tel,address,branch)

        mongo_dict = {}
        mongo_dict['hospital_name'] = hospital_name
        mongo_dict['hospital_label_item'] = hospital_label_item
        mongo_dict['specialized_nature'] = specialized_nature
        mongo_dict['anothe_name'] = anothe_name
        mongo_dict['state_operated_nature'] = state_operated_nature
        mongo_dict['chief_physician_num'] = chief_physician_num
        mongo_dict['associate_chief_physician_num'] = associate_chief_physician_num
        mongo_dict['bednum'] = bednum
        mongo_dict['outpatient_amount'] = outpatient_amount
        mongo_dict['tel'] = tel
        mongo_dict['address'] = address
        mongo_dict['branch'] = branch
        # logging.info(f'------- @@@insert mongo data ------- {esid}')
        self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.HOSPITAL_HEALTH)
