# -*- coding:utf-8 -*-
import json
import random
import platform
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news.const import MongoTables, RedisKey
from flash_news.utils.mongo_utils import MongoUtils

# 补全 全文图片链接和超链接地址
def auto_content_link(self, doc, label, label_attr, prefix_url):
    label_elements = doc(label)
    for label_element in label_elements.items():
        before_href = label_element.attr(label_attr)
        if None == before_href or before_href.startswith('//') or before_href.startswith('#'):
            continue
        label_element.attr(label_attr, self.common_utils.auto_url(prefix_url, before_href.replace('amp;', '')))

def auto_url(prefix_url, href):
    if not href.startswith('http'):
        href = prefix_url + href
    return href

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
def random_int(min, max):
    return random.randint(min, max)

#获取随机代理IP http://180.175.2.68:8060
def randomProxyIP():
    redis_server = from_settings(get_project_settings())
    proxy_ip_list = redis_server.lrange(RedisKey.PROXY_IP, 0, -1)
    print(proxy_ip_list)
    proxy_ip = str(proxy_ip_list[random.randint(0, redis_server.llen(RedisKey.PROXY_IP) - 1)], 'utf-8')
    proxy_ip_json = json.loads(proxy_ip)
    proxy_ip = f'http://{proxy_ip_json["ip"]}:{proxy_ip_json["port"]}'
    return proxy_ip

def get_send_email_receiver(query):
    receiver = []
    results = MongoUtils().find_query(query=query, coll_name=MongoTables.SEND_EMAIL_LIST)
    for result in results:
        receiver.append(result['email'])
    return receiver

def unicode2str(str):
    if platform.system() == 'Windows':
        return str.encode('unicode_escape').decode('unicode_escape')
    else:
        return str.encode('utf-8').decode('unicode_escape')