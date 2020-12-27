import logging
import random
import requests
from pyquery import PyQuery as pq

#字符串拼接的三种方式
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Proxy-Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Referer':'https://mp.weixin.qq.com/',
    'x-requested-with':'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
}
URL = 'https://www.valuehealthregionalissues.com/article/S2212-1099(19)30167-0/fulltext'
session = requests.Session()
try:
    resp = session.get(url=URL, headers=headers, timeout=60)#维护校验的cookie
    doc = pq(resp.text)
    article_elements = doc('.article__sections section')
    abstract = ''
    abstract_nolabel = ''
    for article_element in article_elements.items():
        id = article_element('section').attr('id')
        if None == id:
            continue
        abstract += '<br>' + str(article_element)
        abstract_nolabel += article_element.text()



except Exception as e:
    print(e)
print()





