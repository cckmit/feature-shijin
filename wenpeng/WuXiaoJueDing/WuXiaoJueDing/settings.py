# Scrapy settings for WuXiaoJueDing project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WuXiaoJueDing'

SPIDER_MODULES = ['WuXiaoJueDing.spiders']
NEWSPIDER_MODULE = 'WuXiaoJueDing.spiders'
import json
import datetime
import os

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'WuXiaoJueDing (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
#设置并发数，默认 32
CONCURRENT_REQUESTS = 3
#设置超时时间
DOWNLOAD_TIMEOUT = 180
# 每次请求间隔时间 0.5秒
DOWNLOAD_DELAY = 5

#禁止重定向
#REDIRECT_ENABLED = False

#设置重试次数
RETRY_TIMES = 4
#设置重试返回状态码
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 202, 403, 404]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

#是的设置了2秒
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
#SPIDER_MIDDLEWARES = {
#    'WuXiaoJueDing.middlewares.WuxiaojuedingSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   'WuXiaoJueDing.middlewares.UserAgent_MiddleWare': 300,
   #'WuXiaoJueDing.middlewares.WuxiaojuedingDownloaderMiddleware': 543,
   'WuXiaoJueDing.middlewares.RetryMiddlewares': 350,
   # 'WuXiaoJueDing.middlewares.ProxyMiddleware': 200, #代理ip
}


#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


ITEM_PIPELINES = {
    'WuXiaoJueDing.pipelines.WuxiaojuedingPipeline': 300,
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
#LOG_LEVEL = 'DEBUG'
LOG_LEVEL = 'INFO'

REDIRECT_ENABLED = True #重定向

#scrapy_redis_cluster 集群库
#Redis集群地址(测试)
#REDIS_MASTER_NODES = [
#     {"host": "172.24.56.160", "port": "8000"},
#     {"host": "172.24.56.160", "port": "8001"},
#     {"host": "172.24.56.160", "port": "8002"},
#     {"host": "172.24.56.160", "port": "8003"},
#     {"host": "172.24.56.160", "port": "8004"},
#     {"host": "172.24.56.160", "port": "8005"},
#]

# Redis集群地址(线上)
REDIS_MASTER_NODES = [
    {"host": "10.66.205.48", "port": "8000"},
    {"host": "10.66.205.48", "port": "8001"},
    {"host": "10.66.205.48", "port": "8002"},
    {"host": "10.66.205.48", "port": "8003"},
    {"host": "10.66.205.48", "port": "8004"},
    {"host": "10.66.205.48", "port": "8005"},
    {"host": "10.66.205.48", "port": "8006"},

    {"host": "172.17.108.71", "port": "8000"},
    {"host": "172.17.108.71", "port": "8001"},
    {"host": "172.17.108.71", "port": "8002"},
    {"host": "172.17.108.71", "port": "8003"},
    {"host": "172.17.108.71", "port": "8004"},
    {"host": "172.17.108.71", "port": "8005"},
    {"host": "172.17.108.71", "port": "8006"},
    {"host": "172.17.108.71", "port": "8007"},


]



'''
# 设置redis集群使用的编码
REDIS_CLUSTER_ENCODING = 'utf-8'
# 使用的哈希函数数，默认为6
BLOOMFILTER_HASH_NUMBER = 6
# Bloomfilter使用的Redis内存位，30表示2 ^ 30 = 128MB，默认为22 (1MB 可去重130W URL)
BLOOMFILTER_BIT = 22
#scrapy-redis 分布式设置
SCHEDULER_PERSIST = True
# 配置scrapy-redis调度器
SCHEDULER = "scrapy_redis_cluster.scheduler.Scheduler"
# 配置url去重
DUPEFILTER_CLASS = "scrapy_redis_cluster.dupefilter.RFPDupeFilter"
SCHEDULER_QUEUE_CLASS = 'scrapy_redis_cluster.queue.PriorityQueue'
#自动管理 redis key 数据
SCHEDULER_FLUSH_ON_START = True
#最大空闲时间
SCHEDULER_IDLE_BEFORE_CLOSE = 20
'''
# redis主机名
#REDIS_HOST = '119.29.131.145'
#REDIS_PORT = 7001





