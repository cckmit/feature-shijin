
import json
import random
import logging

from scrapy.utils.project import get_project_settings

from WuXiaoJueDing.spiders.const import RedisKey
from scrapy_redis_cluster.connection import from_settings

logger = logging.getLogger(__name__)

class CommonUtils:
    # 判断值不等于空
    def is_blank(value, key, item):
        if (value):
            item[key] = value
    # 指定整数范围产生随机数
    def randomInt(self, min, max):
        return random.randint(min, max)

    #获取随机代理IP http://180.175.2.68:8060
    def randomProxyIP(self):
        redis_server = from_settings(get_project_settings())
        proxy_ip_list = redis_server.lrange(RedisKey.PROXY_IP, 0, -1)
        proxy_ip = str(proxy_ip_list[random.randint(0, redis_server.llen(RedisKey.PROXY_IP) - 1)], 'utf-8')
        proxy_ip_json = json.loads(proxy_ip)
        proxy_ip = f'http://{proxy_ip_json["ip"]}:{proxy_ip_json["port"]}'
        logging.info(f'获取到代理IP: {proxy_ip}')
        return proxy_ip















