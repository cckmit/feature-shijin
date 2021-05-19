import json
import time
import logging
import random
import scrapy
from flash_news.utils import es_utils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news import const
from flash_news.utils.date_utils import DateUtils
from flash_news.utils.mongo_utils import MongoUtils
'''
万方医生：
tapd网址：
https://www.tapd.cn/60111173/prong/stories/view/1160111173001003329?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：
http://analytics.med.wanfangdata.com.cn/Author/List
'''
mongo_utils = MongoUtils()
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
        ## 主题分析
        mongo_list = mongo_utils.find_all(coll_name=const.MongoTables.WANFANG_ID)
        for scholar in mongo_list:
            del scholar['_id']
            scholarID = scholar["scholarID"]
            cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/PeriodicalChartData"
            cookie_list = [
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.orangerrt%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.orangerrt.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22t7dos5%2bH4GAjx7jwg%5c%2fbVqyk9FEqIt4peQg7MOqG3O7qEyAwzmTGzXOJ9ExouWTrO%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a05%3a43Z%22%2c%22TicketSign%22%3a%22MyqD0cGqMo7xOQezMl8dGA%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612344"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.srj456%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.srj456.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22ctgblh0xWin4iXiWuEY2epOVyjg1wD3DzBmXv5UYY1uL4mWjHlshsxG%5c%2feTuL32ev%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a06%3a35Z%22%2c%22TicketSign%22%3a%22y5tIFJzbnwCq05NQIohUqA%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612396"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.QQ%e5%b0%8f%e4%b8%b8%e5%ad%90%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.QQ%e5%b0%8f%e4%b8%b8%e5%ad%90.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22W3gD%2bDVzCpvNVa4xxd7l8HFowgWcFsB3yibO8zc1xp92X0fvL68s8wNhqolEncxz%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a07%3a27Z%22%2c%22TicketSign%22%3a%22M%2bFXsxfeIQ4tx2ggp2Sqrg%3d%3d%22%7d; WFMed.Auth.IsAutoLogin=; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612447"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.skygrid%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.skygrid.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22g5SNx42veNgOq4PLPTUBV7QNAeDmFrQj6U%2bOvQWXGn6mkXp6NlImsApe%5c%2f4lN%5c%2fK6e%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a08%3a08Z%22%2c%22TicketSign%22%3a%22mimDyjU1ZAYsijp34PpgVQ%3d%3d%22%7d; WFMed.Auth.IsAutoLogin=; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612489"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.mmqmmq%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.mmqmmq.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22rTR9508HjYOCb5fqmZJzDygA0W1ssLC6LeB%2biBNqzCCktKrvWqv6QhKAbN3f2WDz%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a08%3a54Z%22%2c%22TicketSign%22%3a%22fXXX0iO3d5YALlU0LLDe3w%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612535"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.jjyy2020%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.jjyy2020.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22pAumXg5WHBswKojsKqMYBP4l%5c%2fWMBBpMRRaVp3wseO0D%2bF%5c%2f1do3YAisfwn%2bTJFW28%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a09%3a42Z%22%2c%22TicketSign%22%3a%22ALupIlUhalEoA4E0PcWr0w%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612583"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.mrmw86%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.mrmw86.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22Ba6iQehTQUd05ZpMtG3DA8aPfeniQp0gCXiUa45KGlM1tznYMLkgue8hYQYFm5ON%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a10%3a37Z%22%2c%22TicketSign%22%3a%226svwuTRjFyPic7O3j3HiLA%3d%3d%22%7d; WFMed.Auth.IsAutoLogin=; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612637"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.dylan2021%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.dylan2021.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22d3lkH%5c%2fqHhENlTYKDRLqWjAeV75CdSob18Sl%2b8C8nrbuSNl1VE4WrwsTAfT7OIuuw%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a11%3a47Z%22%2c%22TicketSign%22%3a%22E4Cchb%5c%2fvQp3g0G5J%2bjb2ow%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612707"),
                ("Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1620438138,1620459982,1620610504,1620610988; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.YYMFQX%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.YYMFQX.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2201c14961-84b1-4168-9370-591fa26c1c92%22%2c%22Sign%22%3a%22wpN8T6axewdLZP32qw0ddn6cTJ9LEtPBVZVtz4zXYwZdBY%2b%5c%2f9i3XIFnuxeA2tFPl%22%7d%2c%22LastUpdate%22%3a%222021-05-10T02%3a12%3a31Z%22%2c%22TicketSign%22%3a%22Fv1dM6kH6FFrbWT88P447A%3d%3d%22%7d; WFMed.Auth.IsAutoLogin=; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1620612751"),
                  ]
            random_cookie = random.choice(cookie_list)
            cookies={
                "Cookie":random_cookie,
                "StartYear": "2012",
                "EndYear": "2021",
                "Id": scholarID,
            }
            yield scrapy.FormRequest(url=cooperation_url,formdata=cookies,method="POST",callback=self.theme,meta={"scholarID":scholarID,},dont_filter=True)

    ## 合作分析
    def theme(self,response):
        ress = json.loads(response.text)
        scholarID = response.meta["scholarID"]
        for i in ress['list']:
            # 期刊名称
            PeriodicalName = i['PeriodicalName']
            # 影响因子
            ImpactFactor = i['ImpactFactor']
            # 总发文数
            ArticleCount = i['ArticleCount']
            # 第一作者
            FirstArticleCount = i['FirstArticleCount']
            mongo_dict = {}
            mongo_dict['scholarID'] = scholarID
            mongo_dict['PeriodicalName'] = PeriodicalName
            mongo_dict['ImpactFactor'] = ImpactFactor
            mongo_dict['ArticleCount'] = ArticleCount
            mongo_dict['FirstArticleCount'] = FirstArticleCount
            logging.info(f'------- @@@insert mongo data ------- {scholarID}')
            self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.WANFANG_THEME)



    # ## 主题分析

    #         ## 期刊分析
    #         cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/PeriodicalChartData"
    #         cookies = {
    #             "Cookie":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T03%3a28%3a37Z%22%2c%22TicketSign%22%3a%22R8vv8aEl93QARGssr114HA%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617852517",
    #             "StartYear": "2012",
    #             "EndYear": "2021",
    #             "Id": scholarID,
    #             "IETag":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
    #         yield scrapy.FormRequest(url=cooperation_url, formdata=cookies, callback=self.periodical,meta={"scholarID": scholarID,
    #                                                                                              "AuthorName":AuthorName,"AuthorId":AuthorId,"OrgName":OrgName,"Count":Count,
    #                                                                                             "name":name,"count":count})
    #
    # ## 期刊分析
    # def periodical(self,response):
    #     ress = json.loads(response.text)
    #     scholarID = response.meta["scholarID"]
    #     listdata = ress['list']
    #     for i in listdata:
    #         # 期刊名称
    #         PeriodicalName = i['PeriodicalName']
    #         # 影响因子
    #         ImpactFactor = i['ImpactFactor']
    #         # 总发文数
    #         ArticleCount = i['ArticleCount']
    #         # 第一作者
    #         FirstArticleCount = i['FirstArticleCount']
    #         print(scholarID,PeriodicalName, ImpactFactor, ArticleCount, FirstArticleCount)
    #         AuthorName = response.meta["AuthorName"]
    #         AuthorId = response.meta["AuthorId"]
    #         OrgName = response.meta["OrgName"]
    #         Count = response.meta["Count"]
    #         name = response.meta["name"]
    #         count = response.meta["count"]
    #
