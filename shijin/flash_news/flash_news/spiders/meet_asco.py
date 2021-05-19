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
from flash_news import const
from flash_news.const import ESIndex
from flash_news.utils.es_utils import Query, QueryType
from flash_news.utils.date_utils import DateUtils


class Doctor(scrapy.Spider):
    name = 'meet_asco'
    allowed_domains = []
    start_urls = ['https://ascopubs.org/jco/meeting?expanded=tvolume-suppl.d2020.y2020&expanded=tvolume-suppl.d2010']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'HTTPERROR_ALLOWED_CODES': [302, 301],
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        'DOWNLOADER_MIDDLEWARES': {
            'flash_news.pipelines.FlashNewsPipeline': 100,  # 指定下载中间件
        },
    }

    es_utils = es_utils
    mongo_utils = MongoUtils()
    md5_utils = MD5Utils()
    date_utils = DateUtils()
    redis_server = from_settings(get_project_settings())
    ## 主页面
    def parse(self,response):
        url = "https://ascopubs.org/jco/meeting?expanded=tvolume-suppl.d2020.y2020&expanded=tvolume-suppl.d2010"
        headers = {
            "cookie":"timezone=480; __na_c=1; __cfduid=d2261fb4b141cee137b326d04d507766d1619502428; MAID=F7hlMFSQxgS/hXTPEnQenQ==; I2KBRCK=1; _ga=GA1.2.518511993.1619502439; __na_u_38176768=14674013713890; __gads=ID=fef9ac3278aed8a0:T=1619502468:S=ALNI_Mb5rrN7HlecHM1yQA5RV8gclF3utg; __adroll_fpc=4401c3e5cb6f125c724a208f814f848b-1619502472992; BCSessionID=de525ae5-a73b-48e7-89f6-ceae57a8ceb8; OptanonAlertBoxClosed=2021-04-27T07:02:01.614Z; HSPVerifiedv2=0; SERVER=WZ6myaEXBLH0cjxF1pGSsg==; at_check=true; _gid=GA1.2.139402419.1621308568; AMCVS_FC92401053DA88170A490D4C%40AdobeOrg=1; s_cc=true; MACHINE_LAST_SEEN=2021-05-17T23%3A46%3A11.791-07%3A00; s_sq=%5B%5BB%5D%5D; __ar_v4=XGLZLLDJCFFYHBF4LCLF5K%3A20210427%3A72%7CFWR2SALTD5ALHBY3VF34MI%3A20210427%3A71%7COIH2U2CADJHSBHW2L3UKNL%3A20210427%3A71; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+18+2021+16%3A18%3A53+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.3.0&landingPath=NotLandingPage&groups=0_166217%3A1%2C118%3A1%2C1%3A1%2C2%3A1%2C101%3A1%2C3%3A1%2C0_166190%3A1%2C133%3A1%2C103%3A1%2C4%3A1%2C104%3A1%2C0_166216%3A1%2C106%3A1%2C108%3A1%2C109%3A1%2C110%3A1%2C111%3A1%2C112%3A1%2C114%3A1%2C117%3A1%2C119%3A1%2C120%3A1%2C125%3A1%2C130%3A1%2C132%3A1%2C135%3A1%2C0_166191%3A1&AwaitingReconsent=false&consentId=bea1a4ff-90d6-4a83-89f4-5f1f29c0bf5a; mbox=PC#c774fedd96414218b75a9fb34b74bd36.38_0#1684568740|session#6945dfadd70d40b0bb2b0be0b980ae71#1621327798; __atuvc=14%7C17%2C63%7C18%2C33%7C19%2C15%7C20; __atuvs=60a3786dad99ffa1000; _gat=1; _uetsid=4074a770b78911eb96595fe301120c95; _uetvid=0a1935a0a71c11ebb99b97987f65876c; AMCV_FC92401053DA88170A490D4C%40AdobeOrg=-432600572%7CMCIDTS%7C18765%7CMCMID%7C06930884177293802462024934333585990412%7CMCAAMLH-1621930738%7C11%7CMCAAMB-1621930738%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1621333138s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; last_visit_bc=1621325970547"
        }
        # headers = headers,
        yield scrapy.Request(url=url,callback=self.parsel,)

    ## 进入二级页面
    def parsel(self,response):
        doc = pq(response.text)
        title_elements = doc('.js_issue')
        for title_element in title_elements.items():
            meeting_name = title_element('.issueTitle').text().strip().replace('\n', '').replace('\r', '')
            href_page = title_element('a').attr('href')
            url = 'https://ascopubs.org' + href_page
            headers = {
                "cookie":"timezone=480; __na_c=1; __cfduid=d2261fb4b141cee137b326d04d507766d1619502428; MAID=F7hlMFSQxgS/hXTPEnQenQ==; I2KBRCK=1; _ga=GA1.2.518511993.1619502439; __na_u_38176768=14674013713890; __gads=ID=fef9ac3278aed8a0:T=1619502468:S=ALNI_Mb5rrN7HlecHM1yQA5RV8gclF3utg; __adroll_fpc=4401c3e5cb6f125c724a208f814f848b-1619502472992; BCSessionID=de525ae5-a73b-48e7-89f6-ceae57a8ceb8; OptanonAlertBoxClosed=2021-04-27T07:02:01.614Z; HSPVerifiedv2=0; SERVER=WZ6myaEXBLH0cjxF1pGSsg==; at_check=true; _gid=GA1.2.139402419.1621308568; AMCVS_FC92401053DA88170A490D4C%40AdobeOrg=1; s_cc=true; s_sq=%5B%5BB%5D%5D; __ar_v4=XGLZLLDJCFFYHBF4LCLF5K%3A20210427%3A72%7CFWR2SALTD5ALHBY3VF34MI%3A20210427%3A71%7COIH2U2CADJHSBHW2L3UKNL%3A20210427%3A71; AMCV_FC92401053DA88170A490D4C%40AdobeOrg=-432600572%7CMCIDTS%7C18765%7CMCMID%7C06930884177293802462024934333585990412%7CMCAAMLH-1621930738%7C11%7CMCAAMB-1621930738%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1621333138s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; JSESSIONID=891f9e48-393b-4491-bc19-e1d19191ace5; MACHINE_LAST_SEEN=2021-05-18T01%3A19%3A37.009-07%3A00; __atuvc=14%7C17%2C63%7C18%2C33%7C19%2C16%7C20; __atuvs=60a3786dad99ffa1001; last_visit_bc=1621326013831; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+18+2021+16%3A20%3A58+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.3.0&landingPath=NotLandingPage&groups=0_166217%3A1%2C118%3A1%2C1%3A1%2C2%3A1%2C101%3A1%2C3%3A1%2C0_166190%3A1%2C133%3A1%2C103%3A1%2C4%3A1%2C104%3A1%2C0_166216%3A1%2C106%3A1%2C108%3A1%2C109%3A1%2C110%3A1%2C111%3A1%2C112%3A1%2C114%3A1%2C117%3A1%2C119%3A1%2C120%3A1%2C125%3A1%2C130%3A1%2C132%3A1%2C135%3A1%2C0_166191%3A1&AwaitingReconsent=false&consentId=bea1a4ff-90d6-4a83-89f4-5f1f29c0bf5a; _gat_gtag_UA_6730686_2=1; _uetsid=4074a770b78911eb96595fe301120c95; _uetvid=0a1935a0a71c11ebb99b97987f65876c; mbox=PC#c774fedd96414218b75a9fb34b74bd36.38_0#1684570864|session#6945dfadd70d40b0bb2b0be0b980ae71#1621327798"
            }
            yield scrapy.Request(url=url,callback=self.detail_page,meta={"meeting_name":meeting_name})

    ## 进入三级页面
    def detail_page(self,response):
        meeting_name = response.meta["meeting_name"]
        href_page = response.xpath('//a[@class="ref nowrap abs"]/@href').extract()
        for i in href_page:
            url = 'https://ascopubs.org' + i
            headers = {
                "cookie":"timezone=480; __na_c=1; __cfduid=d2261fb4b141cee137b326d04d507766d1619502428; MAID=F7hlMFSQxgS/hXTPEnQenQ==; I2KBRCK=1; _ga=GA1.2.518511993.1619502439; __na_u_38176768=14674013713890; __gads=ID=fef9ac3278aed8a0:T=1619502468:S=ALNI_Mb5rrN7HlecHM1yQA5RV8gclF3utg; __adroll_fpc=4401c3e5cb6f125c724a208f814f848b-1619502472992; BCSessionID=de525ae5-a73b-48e7-89f6-ceae57a8ceb8; OptanonAlertBoxClosed=2021-04-27T07:02:01.614Z; HSPVerifiedv2=0; SERVER=WZ6myaEXBLH0cjxF1pGSsg==; at_check=true; _gid=GA1.2.139402419.1621308568; AMCVS_FC92401053DA88170A490D4C%40AdobeOrg=1; s_cc=true; s_sq=%5B%5BB%5D%5D; AMCV_FC92401053DA88170A490D4C%40AdobeOrg=-432600572%7CMCIDTS%7C18765%7CMCMID%7C06930884177293802462024934333585990412%7CMCAAMLH-1621930738%7C11%7CMCAAMB-1621930738%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1621333138s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; JSESSIONID=891f9e48-393b-4491-bc19-e1d19191ace5; MACHINE_LAST_SEEN=2021-05-18T01%3A19%3A37.009-07%3A00; _gat=1; last_visit_bc=1621326092426; __ar_v4=OIH2U2CADJHSBHW2L3UKNL%3A20210427%3A72%7CFWR2SALTD5ALHBY3VF34MI%3A20210427%3A72%7CXGLZLLDJCFFYHBF4LCLF5K%3A20210427%3A73; __atuvc=14%7C17%2C63%7C18%2C33%7C19%2C17%7C20; __atuvs=60a3786dad99ffa1002; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+18+2021+16%3A22%3A10+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.3.0&landingPath=NotLandingPage&groups=0_166217%3A1%2C118%3A1%2C1%3A1%2C2%3A1%2C101%3A1%2C3%3A1%2C0_166190%3A1%2C133%3A1%2C103%3A1%2C4%3A1%2C104%3A1%2C0_166216%3A1%2C106%3A1%2C108%3A1%2C109%3A1%2C110%3A1%2C111%3A1%2C112%3A1%2C114%3A1%2C117%3A1%2C119%3A1%2C120%3A1%2C125%3A1%2C130%3A1%2C132%3A1%2C135%3A1%2C0_166191%3A1&AwaitingReconsent=false&consentId=bea1a4ff-90d6-4a83-89f4-5f1f29c0bf5a; _gat_gtag_UA_6730686_2=1; _uetsid=4074a770b78911eb96595fe301120c95; _uetvid=0a1935a0a71c11ebb99b97987f65876c; mbox=PC#c774fedd96414218b75a9fb34b74bd36.38_0#1684570934|session#6945dfadd70d40b0bb2b0be0b980ae71#1621327798"
            }
            yield scrapy.Request(url=url,callback=self.detail_page_page,meta={"meeting_name":meeting_name})

    ## 进入详情页
    def detail_page_page(self,response):
        doc = pq(response.text)
        ## 会议名称
        meeting_name = response.meta["meeting_name"]
        print('会议名称:',meeting_name)
        ## url
        url = response.url
        print('URL:',url)
        ## esid
        esid = self.md5_utils.get_md5(url)
        print('ESID:',esid)
        ## 标题
        title = ''.join(response.xpath('//h1[@class="chaptertitle"]/text()').extract()).strip()
        print('标题:',title)
        ## 作者
        author = ",".join(response.xpath('//span[@class="contribDegrees"]/a/text()').extract())
        print('作者:',author)
        ## 机构
        institution = ''.join(response.xpath('//*[@id="affiliationsContainer"]/text()').extract())
        print('机构:',institution)
        ## DOI
        doi = response.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/text()').extract()[0][5:]
        print('DOI:',doi)
        ## 期刊
        journal = 'Journal of Clinical Oncology'
        print('期刊:',journal)
        ## 期刊年卷
        journal_info1 = response.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/text()').extract()[1].strip().replace('\n', '').replace('\r', '').replace(' ', '')
        journal_info2 = ''.join(response.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/cite/text()').extract()).strip()
        journal_info = journal_info2 + journal_info1
        print('期刊年卷:',journal_info)
        ## 发表日期（爬虫）
        old_paper_release_time_str = response.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/text()').extract()[2][-22:].strip().replace('.','')
        mon_eng = old_paper_release_time_str[:-9]
        month = mon_eng_china(mon_eng)
        day = old_paper_release_time_str[-8:-6]
        year = old_paper_release_time_str[-4:]
        paper_release_date_str = '{}{}{}{}{}'.format(year,'-',month,'-',day)
        print('发表日期:',paper_release_date_str)
        ## 发表日期
        paper_release_date = int(time.mktime(time.strptime(paper_release_date_str, "%Y-%m-%d"))) * 1000
        print('发表日期:',paper_release_date)
        ## PMID
        pmid = ''.join(response.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p[3]/a/text()').extract())
        print('PMID:',pmid)
        ## 摘要
        abstract_info = doc('.abstractInFull')
        abstract_info.remove('p:first')
        print('摘要:',abstract_info)
        # NCT
        nct = ''.join(response.xpath('//div[@class="abstractSection abstractInFull"]/p/a/text()').extract())
        nct_ids_list = nct[nct.rfind(" ")+1:].replace('.','')
        print(nct_ids_list)

        es_dict = {}
        es_dict["esid"] = esid
        es_dict["url"] = url
        es_dict["title"] = title
        es_dict["meeting_name"] = meeting_name
        es_dict["author"] = author
        es_dict["institution"] = institution
        es_dict["doi"] = doi
        es_dict["journal"] = journal
        es_dict["journal_info"] = journal_info
        es_dict["spider_wormtime"] = int(time.time()) * 1000
        es_dict["paper_release_date_str"] = paper_release_date_str
        es_dict["paper_release_date"] = paper_release_date
        es_dict["pmid"] = pmid
        es_dict["abstract_info"] = str(abstract_info)
        es_dict["nct_ids_list"] = nct_ids_list
        print(es_dict)
        # self.es_utils.update_or_insert(index=ESIndex.MEETING_PAPER, d=es_dict)
        # logging.info("------- insert es data -------" + esid + title)


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