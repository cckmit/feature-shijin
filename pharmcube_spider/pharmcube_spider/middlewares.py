# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import logging
import requests
from scrapy import signals
from pharmcube_spider import const
from pharmcube_spider.const import MongoTables
from pharmcube_spider.utils import common_utils
from scrapy.utils.python import global_object_name
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils.qcc_utils import QCCUtils
logger = logging.getLogger(__name__)
mongo_cli = MongoUtils()
results = mongo_cli.find_all(MongoTables.USER_AGENTS)

class PharmcubeSpiderSpiderMiddleware:
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


class PharmcubeSpiderDownloaderMiddleware:
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
        logging.info(f'downloading page {request.url}')
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

class CustomMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        url = request.url
        logging.info(f'downloading page {url}')

        if spider.name == 'ispor' and 'baidu' not in url:
            session = requests.Session()
            resp = session.get(url, headers=const.headers, timeout=60)
            cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
            request.cookies = cookie_dict
            session.close()
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#设置随机user_agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        spider_url = request.url
        if 'weixin.qq.com' in spider_url:
            return
        user_agent = results[common_utils.random_int(0, results.count() - 1)]['user_agent']
        request.headers['User-Agent'] = user_agent

#设置代理ip
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = common_utils.randomProxyIP()
        logging.info(f'当前切换到代理IP为 {proxy}')
        request.meta["proxy"] = proxy

class RetryMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        spider_url = request.url
        retries = request.meta.get('retry_times', 0) + 1
        retry_times = self.max_retry_times
        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']
        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.info("Retrying %(request)s (failed %(retries)d times): %(reason)s", {'request': request, 'retries': retries, 'reason': reason}, extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            if 'proxy' in retryreq.meta:
                retryreq.meta['proxy'] = common_utils.randomProxyIP()
            if 'api.qichacha' in spider_url: # 更换token
                retryreq.headers = QCCUtils().get_qcc_token_headers()
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)
            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else: #超时指定重试次数
            stats.inc_value('retry/max_reached')
            logger.info("*************************************** 超时指定重试次数 *********************************************")
            logger.error("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},extra={'spider': spider})