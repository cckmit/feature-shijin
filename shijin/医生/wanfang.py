import requests,json
import time
import logging
import xlrd
import scrapy
from flash_news.utils import es_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news import const
from flash_news.utils.date_utils import DateUtils

'''
万方医生：
tapd网址：
https://www.tapd.cn/60111173/prong/stories/view/1160111173001003329?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：
http://analytics.med.wanfangdata.com.cn/Author/List
'''


class Doctor(scrapy.Spider):
    name = 'wanfang_doctors'
    allowed_domains = []
    start_urls = ['https://www.baidu.com/',]
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    ## 拿到各省的url
    def parse(self,response):
        # logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        # spider_url = response.xpath('//div[@class="left-content left-content-list"]/div[1]/div/p/a/@href').extract()
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%e6%be%b3%e9%97%a8"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%e5%8f%b0%e6%b9%be"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E9%A6%99%E6%B8%AF"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%e6%96%b0%e7%96%86"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E5%AE%81%E5%A4%8F"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E9%9D%92%E6%B5%B7"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E7%94%98%E8%82%83"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E9%99%95%E8%A5%BF"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E8%A5%BF%E8%97%8F"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E4%BA%91%E5%8D%97"]
        # spider_url = [i for i in spider_url if i != "/Author/List?Province=%E8%B4%B5%E5%B7%9E"]
        # for url in spider_url:
        #     url = "http://analytics.med.wanfangdata.com.cn" + url
        #     yield scrapy.Request(url=url, callback=self.province_subject,)
        #     if 'Captcha' in url:
        #         yield scrapy.Request(url=url, callback=self.province_subject,dont_filter=True,priority=50)

    ## 各省下的各学科url
    # def province_subject(self,response):
    #     urls = response.xpath('//div[@class="left-content left-content-list"]/div[2]/div/p/a/@href').extract()
    #     for i in urls:
    #         second_url = "http://analytics.med.wanfangdata.com.cn" + i
    #         yield scrapy.Request(url=second_url, callback=self.province_subject_letter,priority=100)
    #         if 'Captcha' in second_url:
    #             yield scrapy.Request(url=second_url, callback=self.province_subject_letter,dont_filter=True)
    #
    # ## 各省下的各学科各个字母url
    # def province_subject_letter(self,response):
    #     url = response.xpath('//ul[@class="index-list clear"]/li/a/@href').extract()
    #     url.pop(0)
    #     for i in url:
    #         url = "http://analytics.med.wanfangdata.com.cn" + i
    #         yield scrapy.Request(url=url, callback=self.page_turning,priority=150)
    #         if 'Captcha' in url:
    #             yield scrapy.Request(url=url, callback=self.page_turning,dont_filter=True)

    ## 列表页 翻页
    # def page_turning(self,response):
    #     list_url = response.xpath('//div[@class="detail"]/div/ul/li/a/@href').extract()
    #     for i in list_url:
    #         id = i[i.rfind("/")+1:]
    #         keyword_list = []
    #         mongo_list = self.mongo_utils.find_all(coll_name=const.MongoTables.WANFANG_DOCTOR)
    #         # for mongo_data in mongo_list:
    #         #     keyword = mongo_data['scholarID']
    #         #     keyword_list.append(keyword)
    #         # if id in keyword_list:
    #         #     break
    #         url = "http://analytics.med.wanfangdata.com.cn" + i
    #         yield scrapy.Request(url=url, callback=self.wanfang_doctor_deep,priority=200)
    #         if 'Captcha' in url:
    #             yield scrapy.Request(url=url, callback=self.wanfang_doctor_deep,dont_filter=True)
    #
    #     next_url = response.xpath('//li[@class="next"]/a/@href').extract()
    #     next_url = ''.join(next_url)
    #     next_url = 'http://analytics.med.wanfangdata.com.cn' + next_url
    #     if next_url:
    #         yield scrapy.Request(url=next_url, callback=self.page_turning)
    #         if 'Captcha' in next_url:
    #             yield scrapy.Request(url=next_url, callback=self.page_turning,dont_filter=True)

    ## 详情页
    # def wanfang_doctor_deep(self,response):
    #     ## 医生ID
    #     url = response.url
    #     scholarID = url[url.rfind("/")+1:]
    #     print(scholarID)
    #     ## 医生名称
    #     doctor_name = response.xpath('//div[@class="hos-detail"]/div[1]/h1/text()').extract()
    #     doctor_name = ''.join(doctor_name).strip()
    #     print(doctor_name)
    #     ## 所属医院
    #     hospital_name = response.xpath('//div[@class="hos-addr author-organ"]/text()').extract()
    #     hospital_name = ''.join(hospital_name).strip()
    #     print(hospital_name)
    #     ## 发文数
    #     published_num = response.xpath('//span[@class="data-item first"]/span/text()').extract()
    #     published_num = ''.join(published_num).strip()
    #     print(published_num)
    #     ## 学者数
    #     doctor_num = response.xpath('//div[@class="hos-data clear"]/span[2]/span/text()').extract()
    #     doctor_num = ''.join(doctor_num).strip()
    #     print(doctor_num)
    #     ## H指数
    #     H_index = response.xpath('//div[@class="hos-data clear"]/span[2]/span[2]/text()').extract()
    #     H_index = ''.join(H_index).strip()
    #     print(H_index)
    #     ## 被引频次
    #     cited_frequency = response.xpath('//div[@class="hos-data clear"]/span[3]/span[2]/text()').extract()
    #     cited_frequency = ''.join(cited_frequency).strip()
    #     print(cited_frequency)

        ## 合作分析
        # 打开文件
        data = xlrd.open_workbook("D:\software\百度下载\work\万方ID.xlsx")
        # 查看工作表
        data.sheet_names()
        # 通过文件名获得工作表,获取工作表1
        table = data.sheet_by_name('Sheet1')
        scholarID_list = table.col_values(0)
        for scholarID in scholarID_list:
            cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/RelationChartData"
            headers = {
                "Cookie":"WFMed.Auth.IsAutoLogin=; Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1618211341,1618451904,1618575452,1619319239; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%22eca70707-1512-4ac6-982a-b7bfbb54dd60%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-25T03%3a32%3a13Z%22%2c%22TicketSign%22%3a%22JYYLnk9OUEaOpUubaPsqlg%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619321532"
            }
            cookies ={"StartYear": "2012",
                    "EndYear": "2021",
                    "Id": scholarID,}
            yield scrapy.Request(url=cooperation_url, headers=headers,cookies=cookies,method="POST",callback=self.cooperative_partner,meta={"scholarID":scholarID,})

    ## 合作分析
    def cooperative_partner(self,response):
        print(response.text)
        ress = json.loads(response.text)
        listdata = ress['list']
        for i in listdata:
            # 合作者
            AuthorName = i['AuthorName']
            # 合作者ID
            AuthorId = i['AuthorId']
            # 合作者单位
            OrgName = i['OrgName']
            # 合作发文数
            Count = i['Count']
            print(AuthorName, AuthorId, OrgName, Count)
            scholarID = response.meta["scholarID"]
            ## 主题分析
            cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/KeywordsChartData"
            headers = {
                "Cookie":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T03%3a27%3a47Z%22%2c%22TicketSign%22%3a%22qPxz4iYs0Wslk85sl4O7Bg%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617852467"
            }
            cookies = {"StartYear": "2012",
                      "EndYear": "2021",
                      "Id": scholarID, }
            yield scrapy.Request(url=cooperation_url, headers=headers,cookies=cookies, callback=self.theme,meta={"scholarID":scholarID,
                                                                                                 "AuthorName":AuthorName,"AuthorId":AuthorId,"OrgName":OrgName,"Count":Count,})

    ## 主题分析
    def theme(self,response):
        ress = json.loads(response.text)
        for i in ress['ListData']:
            # 关键词
            name = i['name']
            # 词频数
            count = i['count']
            print(name,count)
            scholarID = response.meta["scholarID"]
            AuthorName = response.meta["AuthorName"]
            AuthorId = response.meta["AuthorId"]
            OrgName = response.meta["OrgName"]
            Count = response.meta["Count"]
            ## 期刊分析
            cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/PeriodicalChartData"
            headers = {
                "Cookie":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T03%3a28%3a37Z%22%2c%22TicketSign%22%3a%22R8vv8aEl93QARGssr114HA%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617852517"
            }
            cookies = {"StartYear": "2012",
                       "EndYear": "2021",
                       "Id": scholarID, }
            yield scrapy.Request(url=cooperation_url, headers=headers,cookies=cookies, callback=self.periodical,meta={"scholarID": scholarID,
                                                                                                 "AuthorName":AuthorName,"AuthorId":AuthorId,"OrgName":OrgName,"Count":Count,
                                                                                                "name":name,"count":count})

    ## 期刊分析
    def periodical(self,response):
        ress = json.loads(response.text)
        listdata = ress['list']
        for i in listdata:
            # 期刊名称
            PeriodicalName = i['PeriodicalName']
            # 影响因子
            ImpactFactor = i['ImpactFactor']
            # 总发文数
            ArticleCount = i['ArticleCount']
            # 第一作者
            FirstArticleCount = i['FirstArticleCount']
            print(PeriodicalName, ImpactFactor, ArticleCount, FirstArticleCount)
            scholarID = response.meta["scholarID"]
            AuthorName = response.meta["AuthorName"]
            AuthorId = response.meta["AuthorId"]
            OrgName = response.meta["OrgName"]
            Count = response.meta["Count"]
            name = response.meta["name"]
            count = response.meta["count"]


            mongo_dict = {}
            mongo_dict['scholarID'] = scholarID
            mongo_dict['AuthorName'] = AuthorName
            mongo_dict['AuthorId'] = AuthorId
            mongo_dict['OrgName'] = OrgName
            mongo_dict['Count'] = Count
            mongo_dict['name'] = name
            mongo_dict['count'] = count
            mongo_dict['PeriodicalName'] = PeriodicalName
            mongo_dict['ImpactFactor'] = ImpactFactor
            mongo_dict['ArticleCount'] = ArticleCount
            mongo_dict['FirstArticleCount'] = FirstArticleCount
            logging.info(f'------- @@@insert mongo data ------- {scholarID}')
            self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.WANFANG_DOCTOR)
