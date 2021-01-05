# -*- coding: utf-8 -*- 
import hashlib
import re
import time

from datetime import datetime,timedelta

def get_md5(content):
    if isinstance(content, str):
        content = content.encode("utf-8")
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()

def is_collect(keys, title):  # 判断是否存在
    if not title:
        return False
    count = 0
    for i in keys:
        if i in title:
            count += 1
            break
    if count > 0:
        return True
    else:
        return False



def sum_time( ts):
    if '分钟前' in ts:
        a = ts.split('分钟前')[0]
        publish_date = ((datetime.now() - timedelta(minutes=int(a))).date()).strftime('%Y-%m-%d %H:%M:%S')
    elif '小时前' in ts:
        b = ts.split('小时前')[0]
        publish_date = ((datetime.now() - timedelta(hours=int(b))).date()).strftime('%Y-%m-%d %H:%M:%S')
    elif '天前' in ts:
        c = ts.split('天前')[0]
        publish_date = ((datetime.now() - timedelta(minutes=int(c))).date()).strftime('%Y-%m-%d %H:%M:%S')
    elif ts == '刚刚':
        publish_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        publish_date = datetime.strptime(ts, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M:%S')
    publish_date = int(time.mktime(time.strptime(publish_date, "%Y-%m-%d %H:%M:%S")))
    return publish_date
















