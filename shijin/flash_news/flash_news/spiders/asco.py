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
    name = 'asco'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    es_utils = es_utils
    mongo_utils = MongoUtils()
    md5_utils = MD5Utils()
    date_utils = DateUtils()
    redis_server = from_settings(get_project_settings())
    ## 主页面
    def parse(self,response):
        url = "https://ascopubs.org/jco/meeting?expanded=tvolume-suppl.d2020.y2020&expanded=tvolume-suppl.d2010"
        headers = {"sec-ch-ua":'"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                    "sec-ch-ua-mobile":"?0",
                    "Upgrade-Insecure-Requests":"1",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        res = requests.get(url=url,headers=headers)
        doc = pq(res.text)
        title_elements = doc('.js_issue')
        for title_element in title_elements.items():
            meeting_name = title_element('.issueTitle').text().strip().replace('\n', '').replace('\r', '')
            href_page = title_element('a').attr('href')
            url = 'https://ascopubs.org' + href_page
            headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                       "sec-ch-ua-mobile": "?0",
                       "Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
            res = requests.get(url=url,headers=headers).text
            ele = etree.HTML(res)
            href_page = ele.xpath('//a[@class="ref nowrap abs"]/@href')
            for i in href_page:
                url = 'https://ascopubs.org' + i
                headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                           "sec-ch-ua-mobile": "?0",
                           "Upgrade-Insecure-Requests": "1",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
                res = requests.get(url=url,headers=headers)
                doc = pq(res.text)
                ele = etree.HTML(res.text)
                ## 会议名称
                meeting_name = meeting_name
                # print('会议名称:',meeting_name)
                ## URL
                url = url
                # print('URL:',url)
                ## esid
                esid = self.md5_utils.get_md5(url)
                # print('esid:',esid)
                ## 标题
                title = ''.join(ele.xpath('//h1[@class="chaptertitle"]/text()')).strip()
                # print('标题:',title)
                ## 作者
                author = ','.join(ele.xpath('//span[@class="contribDegrees"]/a/text()'))
                # print('作者:',author)
                ## 机构
                institution = ''.join(ele.xpath('//*[@id="affiliationsContainer"]/text()'))
                # print('机构:',institution)
                ## DOI
                doi = ele.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/text()')[0][5:]
                # print('DOI:',doi)
                ## 期刊
                journal = 'Journal of Clinical Oncology'
                # print('期刊:',journal)
                ## 期刊年卷
                journal_info1 = ele.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/text()')[1].strip().replace('\n', '').replace('\r', '').replace(' ', '')
                journal_info2 = ''.join(ele.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/cite/text()')).strip()
                journal_info = journal_info2 + journal_info1
                # print('期刊年卷:',journal_info)
                ## 发表日期
                old_paper_release_time_str = ele.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p/text()')[2][-22:].strip().replace('.','')
                mon_eng = old_paper_release_time_str[:-9]
                month = mon_eng_china(mon_eng)
                day = old_paper_release_time_str[-8:-6]
                year = old_paper_release_time_str[-4:]
                paper_release_date_str = '{}{}{}{}{}'.format(year,'-',month,'-',day)
                # print('发表日期:',paper_release_date_str)
                ## 发表日期
                paper_release_date = int(time.mktime(time.strptime(paper_release_date_str, "%Y-%m-%d"))) * 1000
                # print('发表日期:',paper_release_date)
                ## PMID
                pmid = ''.join(ele.xpath('//div[@class="widget general-html-asset none ascocitation widget-regular  widget-compact-all"]/div/div/p[3]/a/text()'))
                # print('PMID:',pmid)
                ## 摘要
                abstract_info = doc('.abstractInFull')
                abstract_info.remove('p:first')
                # print('摘要:',abstract_info)
                # NCT
                nct = ''.join(ele.xpath('//div[@class="abstractSection abstractInFull"]/p/a/text()'))
                nct_ids_list = nct[nct.rfind(" ")+1:].replace('.','')
                # print('NCT:',nct_ids_list)

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
                self.es_utils.update_or_insert(index=ESIndex.MEETING_PAPER, d=es_dict)
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