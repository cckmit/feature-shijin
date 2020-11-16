# Scrapy settings for qcc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime
import os

BOT_NAME = 'qcc'

SPIDER_MODULES = ['qcc.spiders']
NEWSPIDER_MODULE = 'qcc.spiders'

# log日志设置
'''
to_day = datetime.datetime.now()
filePath = r'/root/logs/'
logFilePath = r'/root/logs/qcc_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day,)
LOG_FILE = logFilePath
LOG_LEVEL = 'INFO'
'''




#设置超时时间
DOWNLOAD_TIMEOUT = 8
# 每次请求间隔时间 秒
DOWNLOAD_DELAY = 0
#禁止重定向
#REDIRECT_ENABLED = False
CLOSESPIDER_ITEMCOUNT = 50

#设置重试次数
RETRY_TIMES = 10
RETRY_ENABLED = True

#设置重试返回状态码(115 企查查：身份验证错误或者已过期)
RETRY_HTTP_CODES = [202, 500, 502, 503, 504, 522, 524, 408, 429, 403, 404, 115,]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'qcc (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 开启线程数量，默认16
CONCURRENT_REQUESTS = 16


DOWNLOADER_MIDDLEWARES = {
    'qcc.middlewares.QccDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware' : None,
    'qcc.middlewares.RetryMiddleware': 220, # 自定义超过重试处理重试次数处理
}



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
#    'qcc.middlewares.QccSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'qcc.middlewares.QccDownloaderMiddleware': 543,
    'qcc.middlewares.RandomUserAgent': 543, # 随机user-agent
    #todo test 关闭
    #'qcc.middlewares.ProxyMiddleware': 543, # 随机代理ip
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

'''

# Redis集群地址(测试)
REDIS_MASTER_NODES = [
    {"host": "172.24.56.160", "port": "7000"},
    {"host": "172.24.56.160", "port": "7001"},
    {"host": "172.24.56.160", "port": "7002"},
    {"host": "172.24.56.160", "port": "7003"},
    {"host": "172.24.56.160", "port": "7004"},
    {"host": "172.24.56.160", "port": "7005"},
]



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



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay  开始下载时限速并延迟时间
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies 高并发请求时最大延迟时间
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
