import requests,json
import copy
import logging
import scrapy
import time
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
万方医生：
tapd网址：
https://www.tapd.cn/60111173/prong/stories/view/1160111173001003329?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：
http://analytics.med.wanfangdata.com.cn/Author/List
'''

class Doctor(scrapy.Spider):
    name = 'wanfang_doctors'
    allowed_domains = []
    start_urls = ['http://analytics.med.wanfangdata.com.cn/Author/List',]
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

        ## 合作分析
        cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/RelationChartData"
        headers = {
            "Cookie": "Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T02%3a46%3a50Z%22%2c%22TicketSign%22%3a%2207HFW7aFLU5%5c%2fzRbUYXA%5c%2fpQ%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617850010"}
        data = {"StartYear": "2012",
                "EndYear": "2021",
                "Id": scholarID, }
        res = requests.post(url=cooperation_url,headers=headers,data=data).text
        ress = json.loads(res)
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

        ## 主题分析
        theme_url = "http://analytics.med.wanfangdata.com.cn/Author/KeywordsChartData"
        headers = {
                    "Cookie": "Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T02%3a46%3a50Z%22%2c%22TicketSign%22%3a%2207HFW7aFLU5%5c%2fzRbUYXA%5c%2fpQ%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617850010"}
        data={"StartYear": "2012",
            "EndYear": "2021",
            "Id": scholarID,}
        res = requests.post(url=theme_url, headers=headers,data=data).text
        # import random
        # random = random.randint(1,2)
        # time.sleep(random)
        ress = json.loads(res)
        for i in ress['ListData']:
            # 关键词
            name = i['name']
            # 词频数
            count = i['count']
            print(name,count)

        ## 期刊分析
        periodical_url = "http://analytics.med.wanfangdata.com.cn/Author/PeriodicalChartData"
        headers = {
            "Cookie": "Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T02%3a46%3a50Z%22%2c%22TicketSign%22%3a%2207HFW7aFLU5%5c%2fzRbUYXA%5c%2fpQ%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617850010"}
        data = {"StartYear": "2012",
               "EndYear": "2021",
               "Id": scholarID, }
        # import random
        # random = random.randint(1, 2)
        # time.sleep(random)
        res = requests.post(url=periodical_url, headers=headers,data=data).text
        ress = json.loads(res)
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

            mongo_dict = {}
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
