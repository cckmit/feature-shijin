import scrapy
import logging
import xlrd
import re
import pymongo
import os
import requests
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
会议爬虫
tapd网址：https://www.tapd.cn/49171570/prong/tasks/view/1149171570001003492?url_cache_key=4fc5daf22b16e07d38d86ec2d61eb5f6&action_entry_type=task_list
'''

# # 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['spider_py']
table = mdb['meeting_new']

class Doctor(scrapy.Spider):
    name = 'meet'
    allowed_domains = []
    # start_urls = ['http://kcb.sse.com.cn/disclosure/#',]
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        # 打开文件
        data = xlrd.open_workbook("D:\software\百度下载\work\meeting_new.xlsx")
        # 查看工作表
        data.sheet_names()
        # 通过文件名获得工作表,获取工作表1
        table = data.sheet_by_name('Sheet1')
        title = table.col_values(7)
        spider_url = table.col_values(8)
        dic = dict(zip(spider_url,title))
        for spider_url,title in dic.items():
            yield scrapy.Request(url=spider_url, callback=self.parse,meta={"title":title})

    ## 进入详情页
    def parse(self,response):
        title = response.meta["title"]
        url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        pic = response.xpath('//img/@src').extract()
        ll_pic = []
        for i in pic:
            # if 'news-files' not in i:
            #     del i
            if 'http' in i:
                ll_pic.append(i)
            else:
                pic_url = "https:" + i
                ll_pic.append(pic_url)
        title = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',title,re.S)
        title = ''.join(title)
        # print(url)
        # print(title)
        all_dict = {}
        all_dict["url"] = url
        all_dict["title"] = title

        path = r'D://software//百度下载//work//meeting//' + title
        os.mkdir(path)
        # try:
        #     os.mkdir(path)
        # except:
        #     os.mkdir(path+str(2))
        n = 0
        for j in ll_pic:
            print(j)
            n += 1
            nb = str(n)
            # try:
            res = requests.get(url=j,verify=False).content
            # except:
            #     pass
            with open(path+'//'+str(n)+'.png','wb') as w:
                w.write(res)
            # pic_dic = {}
            # pic_dic[nb] = j
            # all_dict.update(pic_dic)

            # all_dict.setdefault('pic',[]).append(pic_dic)
        print(all_dict)
        # table.insert(all_dict)




