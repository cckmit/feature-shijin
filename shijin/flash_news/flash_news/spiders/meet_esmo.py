import requests,json
import copy
import logging
import scrapy
import re
import time
import datetime
from lxml import etree
from pyquery import PyQuery as pq
from flash_news.utils import es_utils
from flash_news.utils import qiniu_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news.utils.file_utils import DownloadFile
from flash_news.utils import pdf_utils
from flash_news import const
from flash_news.const import ESIndex
from flash_news.utils.es_utils import Query, QueryType
from flash_news.utils.date_utils import DateUtils


class Doctor(scrapy.Spider):
    name = 'meet_esmo'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    es_utils = es_utils
    pdf_utils = pdf_utils
    mongo_utils = MongoUtils()
    md5_utils = MD5Utils()
    date_utils = DateUtils()
    file_utils = DownloadFile()
    redis_server = from_settings(get_project_settings())
    ## 主页面
    def parse(self,response):
        url = "https://www.annalsofoncology.org/issue/S0923-7534(16)X6400-9"
        headers = {
            "Cookie":"__gads=ID=f7dcee886ada20fa:T=1619507151:S=ALNI_MbrLZRKbPG2t2ti7-vj199Y-1IWyA; OptanonAlertBoxClosed=2021-04-27T07:11:42.726Z; _hjid=1c29b2b4-1d4c-4fba-8675-b0ed3e0ad229; MAID=owsprRDNaRg4MYyiVyj//w==; I2KBRCK=1; at_check=true; _hjTLDTest=1; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; SERVER=WZ6myaEXBLEEYvrnizi8SQ==; JSESSIONID=aaaCLoIiPJqTK6yC6n5Lx; mbox=PC#a8ef1d6c3ca6409d804bfe320ac6b6a4.38_0#1684554253|session#e7ed287497184bbaac89e0ca2fc01e08#1621317240; _hjAbsoluteSessionInProgress=0; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18765%7CMCMID%7C06922899760792832342026577101411592376%7CMCAAMLH-1621920551%7C11%7CMCAAMB-1621920551%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1621322951s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-554789566%7CvVersion%7C5.0.1; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+18+2021+13%3A42%3A23+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.15.0&hosts=&consentId=cfbc70af-67f9-457b-8903-09ab8e84bfdd&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&AwaitingReconsent=false&geolocation=CN%3BBJ; __atuvc=12%7C17%2C51%7C18%2C33%7C19%2C34%7C20; __atuvs=60a34f3460b27cc8002; s_pers=%20v8%3D1621316547756%7C1715924547756%3B%20v8_s%3DLess%2520than%25201%2520day%7C1621318347756%3B%20c19%3Djb%253Apastissuetoc%7C1621318347760%3B%20v68%3D1621316537256%7C1621318347765%3B; s_sess=%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20e41%3D1%3B%20s_ppvl%3Djb%25253Apastissuetoc%252C16%252C16%252C1531%252C1920%252C531%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Djb%25253Afulltext%25253Ahtml%252C38%252C38%252C1761%252C1920%252C530%252C1920%252C1080%252C1%252CP%3B"
        }
        # headers = headers,
        yield scrapy.Request(url=url,headers = headers,callback=self.parsel,)

    ## 二级页面
    def parsel(self,response):
        href_list = response.xpath('//ul[@class="rlist--inline download-links"]/li[1]/a/@href').extract()
        meeting_name = ''.join(response.xpath('//div[@class="toc-header__sub-title"]/text()').extract())
        for href in href_list:
            if 'pdf' not in href:
                url = "https://www.annalsofoncology.org" + href
                headers = {
                    "Cookie":"__gads=ID=f7dcee886ada20fa:T=1619507151:S=ALNI_MbrLZRKbPG2t2ti7-vj199Y-1IWyA; OptanonAlertBoxClosed=2021-04-27T07:11:42.726Z; _hjid=1c29b2b4-1d4c-4fba-8675-b0ed3e0ad229; MAID=owsprRDNaRg4MYyiVyj//w==; I2KBRCK=1; at_check=true; _hjTLDTest=1; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18765%7CMCMID%7C06922899760792832342026577101411592376%7CMCAAMLH-1621913124%7C11%7CMCAAMB-1621913124%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1621315524s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-554789566%7CvVersion%7C5.0.1; mbox=PC#a8ef1d6c3ca6409d804bfe320ac6b6a4.38_0#1684554253|session#63d6410fd97046cf8e80ca868f1aec2b#1621310181; __atuvc=12%7C17%2C51%7C18%2C33%7C19%2C31%7C20; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+18+2021+11%3A44%3A20+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.15.0&hosts=&consentId=cfbc70af-67f9-457b-8903-09ab8e84bfdd&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&AwaitingReconsent=false&geolocation=CN%3BBJ; s_pers=%20v8%3D1621315353951%7C1715923353951%3B%20v8_s%3DLess%2520than%25201%2520day%7C1621317153951%3B%20c19%3Djb%253Afulltext%253Ahtml%7C1621317153955%3B%20v68%3D1621309448263%7C1621317153959%3B; s_sess=%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Djb%25253Afulltext%25253Ahtml%252C20%252C20%252C937%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20e41%3D1%3B%20s_ppv%3Djb%25253Afulltext%25253Ahtml%252C97%252C20%252C4518%252C1920%252C445%252C1920%252C1080%252C1%252CP%3B; SERVER=WZ6myaEXBLEEYvrnizi8SQ==; JSESSIONID=aaaCLoIiPJqTK6yC6n5Lx"
                }
                yield scrapy.Request(url=url,headers=headers,callback=self.detail_page,meta={"meeting_name":meeting_name})
        headers = {
            "Cookie":"__gads=ID=f7dcee886ada20fa:T=1619507151:S=ALNI_MbrLZRKbPG2t2ti7-vj199Y-1IWyA; OptanonAlertBoxClosed=2021-04-27T07:11:42.726Z; _hjid=1c29b2b4-1d4c-4fba-8675-b0ed3e0ad229; MAID=owsprRDNaRg4MYyiVyj//w==; I2KBRCK=1; at_check=true; _hjTLDTest=1; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18765%7CMCMID%7C06922899760792832342026577101411592376%7CMCAAMLH-1621913124%7C11%7CMCAAMB-1621913124%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1621315524s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-554789566%7CvVersion%7C5.0.1; mbox=PC#a8ef1d6c3ca6409d804bfe320ac6b6a4.38_0#1684554253|session#63d6410fd97046cf8e80ca868f1aec2b#1621310181; __atuvc=12%7C17%2C51%7C18%2C33%7C19%2C31%7C20; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+18+2021+11%3A44%3A20+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.15.0&hosts=&consentId=cfbc70af-67f9-457b-8903-09ab8e84bfdd&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&AwaitingReconsent=false&geolocation=CN%3BBJ; s_pers=%20v8%3D1621315353951%7C1715923353951%3B%20v8_s%3DLess%2520than%25201%2520day%7C1621317153951%3B%20c19%3Djb%253Afulltext%253Ahtml%7C1621317153955%3B%20v68%3D1621309448263%7C1621317153959%3B; s_sess=%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Djb%25253Afulltext%25253Ahtml%252C20%252C20%252C937%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20e41%3D1%3B%20s_ppv%3Djb%25253Afulltext%25253Ahtml%252C97%252C20%252C4518%252C1920%252C445%252C1920%252C1080%252C1%252CP%3B; SERVER=WZ6myaEXBLEEYvrnizi8SQ==; JSESSIONID=aaaCLoIiPJqTK6yC6n5Lx"
        }
        next_url = 'https://www.annalsofoncology.org' + ''.join(response.xpath('//div[@class="toc__pagination--next"]/a/@href').extract())
        if next_url:
            yield scrapy.Request(url=next_url, headers=headers,callback=self.parsel)

    ## 详情页
    def detail_page(self,response):
        ## 会议名称
        meeting_name = response.meta["meeting_name"]
        # print("会议名称:",meeting_name)
        ## URL
        url = response.url
        # print('URL:',url)
        ## esid
        esid = self.md5_utils.get_md5(url)
        # print('ESID:',esid)
        ## 标题
        title = ''.join(response.xpath('//div[@class="article-header__middle"]/h1/text()').extract())
        # print('标题:',title)
        ## 期刊
        journal = 'Annuals of Oncology'
        # print('期刊:',journal)
        ## 期刊年卷
        doc = pq(response.text)
        journal_info_all = doc('.article-header__meta').text()
        journal_info = journal_info_all[journal_info_all.rfind("|") + 2:]
        # print('期刊年卷:',journal_info)
        ## 发表日期
        old_paper_release_time_str = ''.join(response.xpath('//span[@class="article-header__date faded"]/text()').extract())
        mon_eng = old_paper_release_time_str[:old_paper_release_time_str.rfind(" ")-4]
        month = mon_eng_china(mon_eng)
        day = old_paper_release_time_str[-8:-6]
        year = old_paper_release_time_str[-4:]
        paper_release_date_str = '{}{}{}{}{}'.format(year, '-', month, '-', day)
        # print('发表日期:',paper_release_date_str)
        ## 发表日期
        paper_release_date = int(time.mktime(time.strptime(paper_release_date_str, "%Y-%m-%d"))) * 1000
        # print('发表日期:',paper_release_date)
        ## 作者
        author = ','.join(response.xpath('//div[@class="dropBlock article-header__info"]/a/text()').extract())
        # print('作者:',author)
        ## DOI
        doi = ''.join(response.xpath('//a[@class="article-header__doi__value"]/text()').extract())
        # print('DOI:',doi)
        ## 附件
        attached = []
        j = ''.join(response.xpath('//li[@class="article-tools__item article-tools__pdf"]/a/@href').extract())
        pdf_url = 'https://www.annalsofoncology.org' + ''.join(response.xpath('//li[@class="article-tools__item article-tools__pdf"]/a/@href').extract())
        dic = {}
        dic["file_name"] = j[j.rfind("="):].replace('/', '').replace('_', '').replace('-', '').replace('=', '').replace('%', '')
        dic["file_url"] = pdf_url
        self.file_utils.download_file(dic)
        file_name = dic['file_name']
        local_file_path = f'{"E:/workspace/pharmcube-spider-platform/shijin/flash_news/flash_news/temporary_file/"}{file_name}'
        self.pdf_utils.check_pdf(local_file_path)
        qiniu_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_name, is_keep_file=False)
        dic["orig_url"] = qiniu_url
        attached.append(dic)
        # print('附件:', attached)
        ## 摘要
        abstract_info = str(doc('.section-paragraph'))
        # print('摘要:',abstract_info)
        ## nct_ids
        nct_ids_list = ''.join(response.xpath('//section[@id="sec5"]/div/text()').extract())
        if "NCT" in nct_ids_list:
            nct_ids_list = nct_ids_list.split("; ")
            print(nct_ids_list)


        es_dict = {}
        es_dict["esid"] = esid
        es_dict["url"] = url
        es_dict["title"] = title
        es_dict["meeting_name"] = meeting_name
        es_dict["author"] = author
        es_dict["doi"] = doi
        es_dict["journal"] = journal
        es_dict["journal_info"] = journal_info
        es_dict["spider_wormtime"] = int(time.time()) * 1000
        es_dict["paper_release_date_str"] = paper_release_date_str
        es_dict["paper_release_date"] = paper_release_date
        es_dict["attached"] = attached
        es_dict["abstract_info"] = abstract_info
        es_dict["nct_ids_list"] = nct_ids_list
        print(es_dict)
        self.es_utils.update_or_insert(index=ESIndex.MEETING_PAPER, d=es_dict)
        logging.info("------- insert es data -------" + esid + title)


def mon_eng_china(mon_eng):
    if 'Jan' in mon_eng:
        return 1
    if 'Feb' in mon_eng:
        return 2
    if 'Mar' in mon_eng:
        return 3
    if 'Apr' in mon_eng:
        return 4
    if 'May' in mon_eng:
        return 5
    if 'Jun' in mon_eng:
        return 6
    if 'Jul' in mon_eng:
        return 7
    if 'Aug' in mon_eng:
        return 8
    if 'Sep' in mon_eng:
        return 9
    if 'Oct' in mon_eng:
        return 10
    if 'Nov' in mon_eng:
        return 11
    if 'Dec' in mon_eng:
        return 12