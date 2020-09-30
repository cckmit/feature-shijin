# Scrapy settings for pubmed project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import datetime
import os

BOT_NAME = 'pubmed'

SPIDER_MODULES = ['pubmed.spiders']
NEWSPIDER_MODULE = 'pubmed.spiders'


#设置并发数，默认 32
CONCURRENT_REQUESTS = 10
#设置超时时间
DOWNLOAD_TIMEOUT = 30
# 每次请求间隔时间 0.5秒
DOWNLOAD_DELAY = 0.5
#禁止重定向
#REDIRECT_ENABLED = False

#设置重试次数
RETRY_TIMES = 3
#设置重试返回状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 202, 403, 404]

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#接收异常状态码
#HTTPERROR_ALLOWED_CODES = [301]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pubmed (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'pubmed.middlewares.PubmedSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'pubmed.middlewares.PubmedDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'pubmed.pipelines.PubmedPipeline': 300,
#}

ITEM_PIPELINES  = {
    'scrapy_redis_sentinel.pipelines.RedisPipeline': 543,
}

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

# log日志设置
to_day = datetime.datetime.now()
filePath = r'..\logs'
if not os.path.exists(filePath):
    os.makedirs(filePath)
logFilePath = r'..\logs\pubmed_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day,)
LOG_FILE = logFilePath
LOG_LEVEL = 'INFO'

'''


'''


ITEM_PIPELINES = {
    'pubmed.pipelines.PaperPubmedPipeline': 300, #持久化处理
}

DOWNLOADER_MIDDLEWARES = {
   # 'pubmed.middlewares.ProxyMiddleware': 543, # 隧道代理IP
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': True, #关闭默认的user—agent
    'pubmed.middlewares.RandomUserAgent': 543, # 随机user-agent
    'pubmed.middlewares.RetryMiddleware': 220, # 自定义超过重试处理重试次数处理
}


'''
# Redis集群地址(本地)
REDIS_MASTER_NODES = [
    {"host": "192.168.1.136", "port": "7000"},
    {"host": "192.168.1.136", "port": "7001"},
    {"host": "192.168.1.136", "port": "7002"},
    {"host": "192.168.1.136", "port": "7003"},
    {"host": "192.168.1.136", "port": "7004"},
    {"host": "192.168.1.136", "port": "7005"},
]
'''


'''

'''
# Redis集群地址(线上)
REDIS_MASTER_NODES = [
    {"host": "10.46.176.105", "port": "7000"},
    {"host": "10.46.176.105", "port": "7001"},
    {"host": "10.46.176.105", "port": "7002"},
    {"host": "10.46.176.105", "port": "7003"},
    {"host": "10.46.176.105", "port": "7004"},
    {"host": "10.46.176.105", "port": "7005"},
    {"host": "10.27.217.54", "port": "7000"},
    {"host": "10.27.217.54", "port": "7001"},
    {"host": "10.27.217.54", "port": "7002"},
    {"host": "10.27.217.54", "port": "7003"},
    {"host": "10.27.217.54", "port": "7004"},
    {"host": "10.27.217.54", "port": "7005"},
    {"host": "10.27.217.22", "port": "7000"},
    {"host": "10.27.217.22", "port": "7001"},
    {"host": "10.27.217.22", "port": "7002"},
    {"host": "10.27.217.22", "port": "7003"},
    {"host": "10.27.217.22", "port": "7004"},
]

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