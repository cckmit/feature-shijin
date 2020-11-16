# -*- coding:utf-8 -*-
import json
import logging
import random
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from qcc.spiders.const import RedisKey

def is_success_set(fund_name_set, data_str):
    if data_str in fund_name_set:
        return True
    fund_name_set.add(data_str)
    return False

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

# 指定整数范围产生随机数
def randomInt(min, max):
    return random.randint(min, max)

#获取随机代理IP http://180.175.2.68:8060
def randomProxyIP():
    redis_server = from_settings(get_project_settings())
    proxy_ip_list = redis_server.lrange(RedisKey.PROXY_IP, 0, -1)
    proxy_ip = str(proxy_ip_list[random.randint(0, redis_server.llen(RedisKey.PROXY_IP) - 1)], 'utf-8')
    proxy_ip_json = json.loads(proxy_ip)
    proxy_ip = f'http://{proxy_ip_json["ip"]}:{proxy_ip_json["port"]}'
    return proxy_ip