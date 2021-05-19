import scrapy
import logging
import xlrd
import re
import pymongo
import os
import requests
from lxml import etree

# # 打开文件
# data = xlrd.open_workbook("D:\software\百度下载\work\meeting_new.xlsx")
# # 查看工作表
# data.sheet_names()
# # 通过文件名获得工作表,获取工作表1
# table = data.sheet_by_name('Sheet1')
# title = table.col_values(7)
# spider_url = table.col_values(8)
# dic = dict(zip(spider_url,title))
# for spider_url,title in dic.items():
#     res = requests.get(spider_url).text
#     ele = etree.HTML(res)
#     try:
#         pic = ele.xpath('//p/img/@src')
#     except:
#         pic = ele.xpath('//div/img/@src')
#     # print(pic)
#     ll_pic = []
#     for i in pic:
#         if 'http' in i:
#             ll_pic.append(i)
#         else:
#             pic_url = "https:" + i
#             ll_pic.append(pic_url)
#     title = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', title, re.S)
#     title = ''.join(title)
#     path = r'D://software//百度下载//work//meeting//' + title
#     os.mkdir(path)
#     n = 0
#     for j in ll_pic:
#         n += 1
#         nb = str(n) + 'b'
#         try:
#             res = requests.get(url=j, verify=False).content
#         except:
#             pass
#         with open(path + '//' + str(n) + '.png', 'wb') as w:
#             w.write(res)


## 清除空文件夹
dirpath = 'D:\software\百度下载\work\meeting'
def delfiles(dirpath):
    for root, dirs, files in os.walk(dirpath):
        if dirs == files:
            os.rmdir(root)
delfiles(dirpath)
