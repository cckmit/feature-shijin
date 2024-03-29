# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import requests
from flash_news import const
from scrapy import signals
import random
from scrapy.http import HtmlResponse
from flash_news.utils import common_utils
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class FlashNewsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class FlashNewsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        return None
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        headers = {"sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
                   "sec-ch-ua-mobile": "?0",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        data = {
            "expanded": "tvolume-suppl.d2020.y2020",
            "expanded": "tvolume-suppl.d2010",
        }
        res = requests.get(url=request.url, headers=headers, verify=False)
        return HtmlResponse(url=request.url, body=res.text, encoding="utf-8", request=request)
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        #return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



# class ProxyMiddleware(object):
#     def process_request(self, request, spider):
#         proxy = common_utils.randomProxyIP()
#         logging.info(f'当前切换到代理IP为 {proxy}')
#         request.meta["proxy"] = proxy

# 设置代理ip
# class ProxyMiddleware(object):
#     def process_request(self, request,spider):
#         ip_str = requests.post(url="http://60.205.151.191:80/es_online/get_dynamic_ip",)
#         # proxy = {'http': ip_str.text}
#         print(f"当前获取到代理IP：",ip_str.text)
#         # print(proxy)
#         request.meta['proxy'] = ip_str.text

