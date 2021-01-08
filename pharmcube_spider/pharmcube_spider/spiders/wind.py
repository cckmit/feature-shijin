
import logging
import scrapy

'''
万得对接工商接口
* 接口文档地址：http://share.wind.com.cn/wind.ent.openapi/#/api
* 账号：EA1968482002 密码已初始化为：94375596
'''

class WindSpider(scrapy.Spider):
    name = 'wind'
    allowed_domains = []
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            pass
