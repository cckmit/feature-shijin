# Scrapy settings for pharmcube_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from pharmcube_spider.run_env import get_run_env_dict

BOT_NAME = 'pharmcube_spider'

SPIDER_MODULES = ['pharmcube_spider.spiders']
NEWSPIDER_MODULE = 'pharmcube_spider.spiders'


LOG_LEVEL = 'INFO'

#设置超时时间
DOWNLOAD_TIMEOUT = 35
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

#设置重试返回状态码(115 企查查：身份验证错误或者已过期)
RETRY_HTTP_CODES = [202, 500, 502, 503, 504, 522, 524, 408, 429, 403, 115, 412, ]
#设置允许指定异常状态通过
#HTTPERROR_ALLOWED_CODES = [302, ]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pharmcube_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOADER_MIDDLEWARES = {
    'pharmcube_spider.middlewares.PharmcubeSpiderDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None, #关闭重定向（301，302）
    'pharmcube_spider.middlewares.RetryMiddleware': 543, # 自定义超过重试处理重试次数处理
    'pharmcube_spider.middlewares.RandomUserAgent': 543, # 随机user-agent
    # todo test 关闭
    #'pharmcube_spider.middlewares.ProxyMiddleware': 543, # 随机代理ip
}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

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
#    'pharmcube_spider.middlewares.PharmcubeSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'pharmcube_spider.middlewares.PharmcubeSpiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'pharmcube_spider.pipelines.PharmcubeSpiderPipeline': 300,
#}

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
