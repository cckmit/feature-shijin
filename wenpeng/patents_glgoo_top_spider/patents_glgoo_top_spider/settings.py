# Scrapy settings for patents_glgoo_top_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'patents_glgoo_top_spider'

SPIDER_MODULES = ['patents_glgoo_top_spider.spiders']
NEWSPIDER_MODULE = 'patents_glgoo_top_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'patents_glgoo_top_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 50

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

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
#    'patents_glgoo_top_spider.middlewares.PatentsGlgooTopSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html

DOWNLOADER_MIDDLEWARES = {
#    'patents_glgoo_top_spider.middlewares.PatentsGlgooTopSpiderDownloaderMiddleware': 543,
   'patents_glgoo_top_spider.middlewares.UserAgent_MiddleWare': 300,
   'patents_glgoo_top_spider.middlewares.RetryMiddlewares': 200,
   'patents_glgoo_top_spider.middlewares.ProxyMiddleware': 300,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'patents_glgoo_top_spider.pipelines.PatentsGlgooTopSpiderPipeline': 300,
#}

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
import json
import datetime
import os
to_day = datetime.datetime.now()
filePath = r'..\logs'
if not os.path.exists(filePath):
    os.makedirs(filePath)
logFilePath = r'..\logs\BOT_NAME_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day,)
LOG_FILE = logFilePath
#LOG_LEVEL = 'DEBUG'
LOG_LEVEL = 'INFO'
REDIRECT_ENABLED = True #重定向
DOWNLOAD_TIMEOUT =60
#设置重试次数
RETRY_TIMES = 4

######

######


# Redis集群地址(测试)
# REDIS_MASTER_NODES = [
#     {"host": "172.24.56.160", "port": "7000"},
#     {"host": "172.24.56.160", "port": "7001"},
#     {"host": "172.24.56.160", "port": "7002"},
#     {"host": "172.24.56.160", "port": "7003"},
#     {"host": "172.24.56.160", "port": "7004"},
#     {"host": "172.24.56.160", "port": "7005"},
# ]

#10.27.217.22 8000-8007
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

    {"host": "10.27.217.22", "port": "8000"},
    {"host": "10.27.217.22", "port": "8001"},
    {"host": "10.27.217.22", "port": "8002"},
    {"host": "10.27.217.22", "port": "8003"},
    {"host": "10.27.217.22", "port": "8004"},
    {"host": "10.27.217.22", "port": "8005"},
    {"host": "10.27.217.22", "port": "8006"},
    {"host": "10.27.217.22", "port": "8007"},



]

# redis主机名
#REDIS_HOST = '119.29.131.145'
#REDIS_PORT = 7001








