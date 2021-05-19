# Scrapy settings for flash_news project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import requests
import json
import time
from flash_news.run_env import get_run_env_dict
BOT_NAME = 'flash_news'

SPIDER_MODULES = ['flash_news.spiders']
NEWSPIDER_MODULE = 'flash_news.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 全局并发数
CONCURRENT_REQUESTS = 1

#设置超时时间
DOWNLOAD_TIMEOUT = 120
# 每次请求间隔时间 秒
DOWNLOAD_DELAY = 0.26
# 启用后，当从相同的网站获取数据时，Scrapy将会等待一个随机的值，延迟时间为0.5到1.5之间的一个随机值乘以DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True

#禁止重定向
#REDIRECT_ENABLED = False
CLOSESPIDER_ITEMCOUNT = 50

#设置重试次数
RETRY_TIMES = 9
RETRY_ENABLED = True
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 网络延时
# import random
# random = random.randint(1,2)
# DOWNLOAD_DELAY = random

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 128
CONCURRENT_REQUESTS_PER_IP = 128

# 禁止cookies
# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

# Obey robots.txt rules

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'flash_news.middlewares.FlashNewsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'flash_news.middlewares.FlashNewsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'flash_news.pipelines.FlashNewsPipeline': 543
# }


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# DOWNLOADER_MIDDLEWARES = {
#     'flash_news.middlewares.ProxyMiddleware': 543,
# }

DOWNLOADER_MIDDLEWARES = {
    'flash_news.middlewares.FlashNewsDownloaderMiddleware': 543,
}

# res = requests.get('http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=').text
# res = json.loads(res)
# for i in res['data']:
#     ip = i['ip']
#     port = i['port']
#     proxies = "http://"+str(ip)+":"+str(port)
#     print(proxies)



# Redis集群地址(线上)
REDIS_MASTER_NODES = get_run_env_dict()['redis']['redis_nodes']

# 设置redis集群使用的编码
REDIS_CLUSTER_ENCODING = 'utf-8'
# 使用的哈希函数数，默认为6
BLOOMFILTER_HASH_NUMBER = 6
# Bloomfilter使用的Redis内存位，30表示2 ^ 30 = 128MB，默认为22 (1MB 可去重130W URL)
BLOOMFILTER_BIT = 22
# 不清空redis队列
SCHEDULER_PERSIST = True
# 调度队列
SCHEDULER = "scrapy_redis_cluster.scheduler.Scheduler"
# 去重
DUPEFILTER_CLASS = "scrapy_redis_cluster.dupefilter.RFPDupeFilter"
# queue
SCHEDULER_QUEUE_CLASS = 'scrapy_redis_cluster.queue.PriorityQueue'
#自动管理 redis key 数据
SCHEDULER_FLUSH_ON_START = True
#最大空闲时间
SCHEDULER_IDLE_BEFORE_CLOSE = 20