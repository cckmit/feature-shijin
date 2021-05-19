#coding=utf-8

import datetime
import time

# now=datetime.datetime.now()
# # print(now)
# delta=datetime.timedelta(hours=3)
# # print(delta)
# n_days=now+delta
# time_arr = n_days.strftime('%Y-%m-%d %H:%M:%S')
#
# timestamp = int(time.mktime(time_arr))
# print(timestamp)



from lxml import etree
import requests
# res=requests.get('http://www.w3school.com.cn/')
# tree=etree.HTML(res.content)
# div=tree.xpath('//div[@id="d1"]')[0]
# div_str=etree.tostring(div,encoding='utf-8')
# print(div_str)




# url = "https://www.gelonghui.com/news/473812"
# res = requests.get(url)
# print(res)
# tree = etree.HTML(res.content)
# div = tree.xpath('//article[@class="main-news article-with-html"]')[0]
# print(div)
# div_str = etree.tostring(div, encoding='utf-8')
# print(div_str)




# from lxml import etree
# import requests
#
# res=requests.get('http://www.w3school.com.cn/')
# tree=etree.HTML(res.content)
# print(tree)
# div=tree.xpath('//div[@id="d1"]')[0]
# div_str=etree.tostring(div,encoding='utf-8')
# print(div_str)




# import json
# # filename = "./base_channel.txt"
# # f_obj = open(filename,'r',encoding='utf-8')
# # base_channel = json.load(f_obj)
# # print(base_channel)
#
# with open('./base_channel.json','r',encoding='utf-8') as fp:
#     strF = fp.read()
#     json_data = json.loads(strF)
#     print(fp)

# __author__ = 'Administrator'
#-*- coding: utf-8 -*-



# import hashlib
# aa = '123456' #需要加密的字符串
# def md5Encode(str):
#     m = hashlib.md5() # 创建md5对象
#     m.update(str)  # 传入需要加密的字符串进行MD5加密
#     return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
# bb = md5Encode(aa.encode('utf-8')) # 必须先进行转码，否则会报错
# print(bb)


# from pymongo import MongoClient
# client = MongoClient(host='127.0.0.1',port=27021)
# db = client.blog_database
# collection = db.blog
# all={'a':'1',
#      'b':'2'
#      }
# collection.insert_one(all)


#
# base_chanel_list = []
import pymongo
# import pandas as pd
# # 连接数据库
# client = pymongo.MongoClient('localhost', 27017)
# mdb = client['pharmcube']
# table = mdb['classification_cpc']
# all={'a':'1',
#      'b':'2'
#      }
# table.insert(all)
#
# # 读取数据
# data = pd.DataFrame(list(table.find()))
# print(data)
# # 选择需要显示的字段
# data = data['keywords']
#
# # 打印输出
# print(data)
# industry_news_type = ["获批上市","通过一致性评价","突破性疗法","纳入优先审评","首仿获批","申报临床","获批临床","启动I期临床","启动II期临床","启动III期临床",
#                       "收购","受让","并购","交易","转让","融资","领投","跟投","A轮","B轮","C轮","D轮","E轮","本轮","天使轮","筹集","科创板","IPO",
#                       "靶点","通路","综述","介导","新疗法"
#                       ]

# import re
#
# aa = '港股收盘|恒指收跌2.55%再失三万点  百奥家庭互动逆市涨超40%'
# bb = '智通AH统计|1月26日'
# cc = '智通财经APP获悉，1月26日美股盘前，诺华制药(NVS.US)公布2020年第四季度业绩和2020财年业绩。，高于销售额。'
#
# ee = aa[aa.find('|'):]
# print(ee)
# # re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',ee,re.S)
# ee = re.sub('u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])"',"",ee)
# print(ee)
#
# dd = cc[:cc.find(','[0])]
# print(dd)



# aa = '昨天23:30'
# if '昨天' in aa:
#     c = aa[2:4]
#     c = int(24) - int(c)
#     print(c)

# aa = "2021年1月29日 11:31:04"
# aa.replace()
# print(aa)
# timeArray = time.strptime(aa,"%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()


# while True:
#     n = 0
#     for keyword in a:
#         for type in b:
#             if keyword in c:
#                 n += 1
#                 if n == 1:
#                     print(1111)
#             if type in c:
#                 if n == 2:
#                     print(2222)
# else:
#     print(222222)
#     print(333333333)
# print(4444444444)
# a = [1,2,3,3]
# b = [3,4,5,6]
# c = [2,3,4,3]
#
# # cc_break = False
# dd_break = False
# for keyword in a:
#     if keyword not in c:
#         continue
#     dd_break = True
#     for type_temp in a:
#         if type_temp not in c:
#             continue
#         # cc_break = True
#         break
#     break
# if dd_break:
#     print('okokokokokokok')
# else:
#     print('cccccccccccccc')


dica = {'a': 2, 'b': 2, 'c': 3, 'd': 2, 'f': "hello",'aa': 1, 'bb': 1, 'cc': 3, 'dd': 2, 'ff': "hello"}
dicb = {'b': 4, 'd': 4, 'e': 7, 'm': 9, 'k': 'world','bb': 3, 'dd': 4, 'ee': 7, 'mm': 9, 'kk': 'world'}
dicc = {'b': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}, 'e': 6, 'a': 7, 'm': 9, 'k': 'world','bb': {'valid_from_data': 1356969600, 'valid_to_data': ''}, 'ee': 6, 'aa': 7, 'mm': 9, 'kk': 'world'}

ab = {}
for key in dicb:
    # print(key)
    if dica.get(key):
        ab[key] = dicb[key]
print(ab)
ac = {}
for keys in dicc:
    # print(keys)
    if dica.get(keys):
        ac[keys] = dicc[keys]
print(ac)
bc = {}
for i in ab:
    if ac.get(i):
        bc[i] = ab[i]
print(bc)
for i in bc:
    a = dica[i]
    b = dicb[i]
    c = dicc[i]['valid_from_data']
    d = dicc[i]['valid_to_data']
    print(i)
    print(a)
    print(b)
    print(c)
    print(d)

# cpc_scheme_dict = {}
# title_dict = {}
# validity_dict = {}
#
# scheme_title = {}
# for key in title_dict:
#     # print(key)
#     if cpc_scheme_dict.get(key):
#         scheme_title[key] = title_dict[key]
# print(scheme_title)
#
# scheme_validity = {}
# for keys in validity_dict:
#     if cpc_scheme_dict.get(keys):
#         scheme_validity[keys] = validity_dict[keys]
# print(scheme_validity)
#
# title_validity = {}
# for i in scheme_title:
#     if scheme_validity.get(i):
#         title_validity[i] = scheme_title[i]
# print(title_validity)
#
# for cpc_no in title_validity:
#     leval = cpc_scheme_dict[cpc_no]
#     definition_en = title_dict[cpc_no]
#     valid_from_date = validity_dict[cpc_no]['valid_from_data']
#     valid_to_date = validity_dict[cpc_no]['valid_to_data']
#     def md5Encode(str):
#         m = hashlib.md5() # 创建md5对象
#         m.update(str)  # 传入需要加密的字符串进行MD5加密
#         return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
#     esid = md5Encode(cpc_no.encode('utf-8')) # 必须先进行转码，否则会报错
#
#     all_dict = {}
#     all_dict["esid"] = esid
#     all_dict["cpc_no"] = cpc_no
#     all_dict["leval"] = leval
#     all_dict["definition_en"] = definition_en
#     all_dict["valid_from_date"] = valid_from_date
#     all_dict["valid_to_date"] = valid_to_date
#     table.insert(all_dict)
#     print(cpc_no,leval,definition_en,valid_from_date,valid_to_date)


