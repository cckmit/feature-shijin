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
    name = 'guojiayibao'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    es_utils = es_utils
    mongo_utils = MongoUtils()
    md5_utils = MD5Utils()
    date_utils = DateUtils()
    redis_server = from_settings(get_project_settings())
    ## 主页面
    def parse(self,response):
        url = 'https://fuwu.nhsa.gov.cn/ebus/fuwu/api/base/api/drugOptins/queryDrugOptinsInfoDetail'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 5.1.1; LYA-AL10 Build/LYZ28N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36HSABrowser/1.2.2'
        headers['Content-Type'] = 'application/json;charset=UTF-8'
        headers['Accept'] = 'application/json, text/plain, */*'
        headers['orgCode'] = '110101'
        headers['channel'] = 'app'
        headers['Referer'] = 'https://fuwu.nhsa.gov.cn/hsafront/'
        headers['Accept-Language'] = 'zh-CN,en-US;q=0.8'
        headers['X-Requested-With'] = 'cn.hsa.app'
        post_dict = {"data": {"pageNum": 1, "pageSize": 20, "drugName": "乙磺酸尼达尼布软胶囊", "medinsType": 2, "province": "北京市","region": "朝阳区"}}
        yield scrapy.FormRequest(url=url,method="POST",body=json.dumps(post_dict),callback=self.parsel,headers=headers,)

    ## 二级页面
    def parsel(self,response):
        content = json.loads(response.text)
        print(content)