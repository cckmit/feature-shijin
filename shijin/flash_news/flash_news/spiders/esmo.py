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
    name = 'esmo'
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
        # 翻页
        for page in range(0,10):
            url = "https://www.annalsofoncology.org/issue/S0923-7534(16)X6400-9?pageStart={}".format(page)
            headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                       "sec-ch-ua-mobile": "?0",
                       "Upgrade-Insecure-Requests": "1",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
            res = requests.get(url=url,headers=headers)
            ele = etree.HTML(res.text)
            href_list = ele.xpath('//ul[@class="rlist--inline download-links"]/li[1]/a/@href')
            meeting_name = ''.join(ele.xpath('//div[@class="toc-header__sub-title"]/text()'))
            for href in href_list:
                if 'pdf' not in href:
                    url = "https://www.annalsofoncology.org" + href
                    headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                               "sec-ch-ua-mobile": "?0",
                               "Upgrade-Insecure-Requests": "1",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
                    res = requests.get(url=url, headers=headers)
                    ele = etree.HTML(res.text)
                    # 详情页
                    ## 会议名称
                    meeting_name = meeting_name
                    # print('会议名称:',meeting_name)
                    ## URL
                    url = url
                    # print('URL:',url)
                    ## ESID
                    esid = self.md5_utils.get_md5(url)
                    # print('ESID:',esid)
                    ## 标题
                    title = ''.join(ele.xpath('//div[@class="article-header__middle"]/h1/text()'))
                    # print('标题:',title)
                    ## 期刊
                    journal = 'Annuals of Oncology'
                    # print('期刊:',journal)
                    ## 期刊年卷
                    doc = pq(res.text)
                    journal_info_all = doc('.article-header__meta').text()
                    journal_info = journal_info_all[journal_info_all.rfind("|") + 2:]
                    # print('期刊年卷:',journal_info)
                    ## 发表日期
                    old_paper_release_time_str = ''.join(ele.xpath('//span[@class="article-header__date faded"]/text()'))
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
                    author = ','.join(ele.xpath('//div[@class="dropBlock article-header__info"]/a/text()'))
                    # print('作者:',author)
                    ## DOI
                    doi = ''.join(ele.xpath('//a[@class="article-header__doi__value"]/text()'))
                    # print('DOI:',doi)
                    ## 附件
                    attached = []
                    j = ''.join(ele.xpath('//li[@class="article-tools__item article-tools__pdf"]/a/@href'))
                    pdf_url = 'https://www.annalsofoncology.org' + ''.join(ele.xpath('//li[@class="article-tools__item article-tools__pdf"]/a/@href'))
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
                    # print('附件:',attached)
                    ## 摘要
                    abstract_info = str(doc('.section-paragraph'))
                    # print('摘要:',abstract_info)
                    ## nct_ids
                    nct_ids_list = ''.join(ele.xpath('//div[@class="section-paragraph"]/text()'))
                    if "NCT" in nct_ids_list:
                        nct_ids_list = nct_ids_list.split("; ")
                        # print(nct_ids_list)

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