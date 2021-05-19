# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy import Item

import pymongo
# from scrapy.conf import settings

class FlashNewsPipeline(object):
    def __init__(self):
        # 获取setting主机名、端口号和数据库名称
        host = '127.0.0.1'
        port = 27017

        # 创建数据库连接
        client = pymongo.MongoClient(host=host,port=port)

        # 指向指定数据库
        mdb = client['pharmcube']

        # 获取数据库里面存放数据的表名
        self.post = mdb['flash_new']

    def process_item(self, item, spider):
        esid = dict(item)
        url = dict(item)
        name = dict(item)
        timeStamp = dict(item)
        contents = dict(item)
        ress = dict(item)

        ## 向指定的表里添加数据
        self.post.insert(esid)
        self.post.insert(url)
        self.post.insert(name)
        self.post.insert(timeStamp)
        self.post.insert(contents)
        self.post.insert(ress)

        return item

