# -*- coding: utf-8 -*-
from scrapy import signals

from .tools.useragents import useragents
import random
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings
settings=get_project_settings()



class UserAgent_MiddleWare():
    def __init__(self):
        self.user_agents = useragents
    def process_request(self, request, spider):
        print('request:',request.url)
        request.headers.setdefault('User-Agent', random.choice(self.user_agents))

    def process_response(self, request, response, spider):
        print(response.status)
        if response.status != 200:
            with open('./error403.txt', 'a+') as f:
                f.write(str(response.status)+':'+response.url+'\n')
            return HtmlResponse(url='exceptions')
        else:
            return response


from .utils.common_utils import CommonUtils
from scrapy.utils.python import global_object_name
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging
from scrapy import signals
logger = logging.getLogger(__name__)
# 当重试次数大于设置次数的时候，后期会单独处理数据
class RetryMiddlewares(RetryMiddleware):
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        retry_times = self.max_retry_times
        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']
        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            #设置代理ip
            # proxy = CommonUtils().randomProxyIP()
            # retryreq.meta['proxy'] = proxy

            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)
            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.info("******************************************")
            logger.error("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})

##设置代理IP
#class ProxyMiddleware(object):
#    def process_request(self,request,spider):
#        proxy = CommonUtils().randomProxyIP()
#        logging.info(f'当前切换的代理IP为 {proxy}')
#        request.meta['proxy'] = proxy

from twisted.internet.error import TimeoutError
from .utils.common_utils import CommonUtils
#设置代理IP
class ProxyMiddleware(object):
    def process_request(self,request,spider):
        proxy = CommonUtils().randomProxyIP()
        logging.info(f'当前切换的代理IP为 {proxy}')
        request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request










class XinwenzixunSpiderMiddleware:
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

class XinwenzixunDownloaderMiddleware:
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

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

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
