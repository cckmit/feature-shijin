import datetime
import time
import requests
from lxml import etree
# from flash_news.utils.date_utils import DateUtils
#
# class Aa:
#     def __init__(self):
#         self.date_utils = DateUtils()


# date_str = "2021年1月29日 11:31:04"
# aa = date_str.replace('年','-').replace('月','-').replace('日','')
#
# date_str = "2021/01/29 11:50"
# bb = date_str.replace('/','-').replace('/','-').replace('/','')
# # print(bb)
#
# date_str = "2021年01月29日 12:29"
# cc = date_str.replace('年','-').replace('月','-').replace('日','')
#
# date_str = "2021年01月29日 12:21"
# dd = date_str.replace('年','-').replace('月','-').replace('日','')
#
# ee = "2013-01-01"
# timeArray = time.strptime(ee,"%Y-%m-%d")
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)
# # print(timeStamp)
# # 格隆汇用我自己的转时间戳
#
#
# now = int(time.time()) #返回float数据
# print(now)
#  获取当前时间戳---秒级级
# print(int(now))

# timeArray = time.strptime(ee,"%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)

import re
import time

# shijian ="3分钟前"
# # shijian ="3小时前"
# now_time = datetime.datetime.now()
# print(now_time)
# if '分钟' in shijian:
#     minutes = re.findall('^[0-9><=]', shijian)
#     delta = datetime.timedelta(minutes=int(''.join(minutes)))
#     nows_time = (now_time - delta).strftime('%Y-%m-%d %H:%M:%S')
#     # print(timee)
# elif '小时' in shijian:
#     hours = re.findall('^[0-9><=]',shijian)
#     delta = datetime.timedelta(hours=int(''.join(hours)))
#     nows_time = (now_time - delta).strftime('%Y-%m-%d %H:%M:%S')
#     # print(timee)
# timeArray = time.strptime(nows_time,"%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeArray))
# print(timeStamp)




# aa = {'CPC_Symbol':{"Valid From Date":'2012-01-01', 'Valid To Date':'2012-01-02'}}
# bb = aa.keys()
# print(bb)
# if bb == 'dict_keys(['CPC_Symbol'])':
#     print('ok')
# print(aa['CPC_Symbol']['Valid To Date'])

# start = datetime.datetime.now()
#
#
# cpc_scheme_list = [{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'},{'H05K203/1311': '10'}, {'H05K203/1312': '10'}, {'H05K203/1323': '10'}, {'H05K204/4': '10'}]
# title_list_list = [{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'},{'H05B6/45': 'Establishing desired heat distribution, e.g. to heat particular parts of workpieces'}, {'H05K203/1323': '{for heating gear-wheels}'},{'H05K203/1327': '{for heating gear-wheels}'}]
# validity_file_list = [{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1323': {'valid_from_data': 1356969600, 'valid_to_data': 1234567890}}, {'Y10S152/09': {'valid_from_data': 1356969600, 'valid_to_data': ''}},{'H05K203/1320': {'valid_from_data': 1356969600, 'valid_to_data': ''}}]
# scheme_title_list = []
# for cpc_scheme in cpc_scheme_list:
#     cpc_scheme_str = ''.join(list(cpc_scheme.keys()))
#     # print(cpc_scheme_str)
#     for cpc_title in title_list_list:
#         cpc_title_str = ''.join(list(cpc_title.keys()))
#         if cpc_scheme_str == cpc_title_str:
#             scheme_title_list.append(cpc_scheme_str)
#             scheme_title = {}
#             scheme_title[cpc_scheme_str] = cpc_scheme[cpc_scheme_str]
#             # scheme_title.setdefault(scheme_title[cpc_scheme_str],[]).append(cpc_title[cpc_title_str])
#             print(scheme_title)
#             # scheme_title_list.append(scheme_title)
# # print(scheme_title_list)
# #     for scheme_title in scheme_title_list:
# #         for cpc_validity in validity_file_list:
# #             cpc_validity_str = ''.join(list(cpc_validity.keys()))
# #             # print(cpc_validity_str)
# #             if  scheme_title == cpc_validity_str:
# #                 cpc_no = cpc_scheme_str
#
# end = datetime.datetime.now()
# print(end-start)


#
# url = "https://www.guahao.com/s/甲亢/expert/29/广东/all/不限/p36"
# headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#             "Accept-Encoding":"gzip, deflate, br",
#             "Accept-Language":"zh-CN,zh;q=0.9",
#             "Cache-Control":"max-age=0",
#             "Connection":"keep-alive",
#             "Cookie":"BIDUPSID=21404EC1D0D59137A3A60DE92656350F; PSTM=1611811793; BAIDUID=48891841DA22B8137F336DEFF4E1A331:FG=1; __yjs_duid=1_e84683d4890fdc6e86ff92f11b2456201612149238508; H_PS_PSSID=33425_33581_33258_33273_33570_33335_26350_33568; Hm_lvt_d0e1c62633eae5b65daca0b6f018ef4c=1613729387; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lpvt_d0e1c62633eae5b65daca0b6f018ef4c=1613957080; ab_sr=1.0.0_ODU3ZTUzY2NhYzgwOTI1OTYyZGFjY2E3YjgyZWJmNDg1YTAyMjJlYTQ0NWMxM2IyZGMwNTlkMDQ3NGMxMjk5NTI2MTI0MDViODhmNzgwMjUxNWRjMjM0NWMzMDUyYTQ5; antispam_data=3620979ef016276132a6f53e4d9a245d930b6afe98cd85a51be4f3f1cef653f42fdcd5ff8b7ba209c3d57fa2a4c3fb0967f01b6c55c128dd01b895db389d13ff67bb99dd2794eefa55ed8f67034b7183c50e0b92c24e2e2b3019f28ed0b27e66; antispam_key_id=45; antispam_sign=4d6d349b; antispam_site=ae_xueshu_homepage",
#             "Host":"xueshu.baidu.com",
#             "Referer":"https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=frontpage",
#             "sec-ch-ua":'"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
#             "sec-ch-ua-mobile":"?0",
#             "Sec-Fetch-Dest":"document",
#             "Sec-Fetch-Mode":"navigate",
#             "Sec-Fetch-Site":"same-origin",
#             "Sec-Fetch-User":"?1",
#             "Upgrade-Insecure-Requests":"1",
#             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
# data = {"cmd":"inject_page",
#         "author":"吴媛媛",
#         "affiliate":""}
# res = requests.get(url).text
# print(res)
# aa = '2021.03'
# bb = aa.replace('.','')
# print(bb)

"https://www.guahao.com/s/%E7%94%B2%E4%BA%A2"
"https://www.guahao.com/s/%E7%94%B2%E4%BA%A2/expert/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/p38"


# aa = "曹县人民医院 健康新村1号【春雨提示：部分医院有多个院区，请先与医生确认好地点后再前往就诊】"
# bb = aa[:aa.rfind("【")]
# print(bb)

import requests
from lxml import etree
import json

# url = "http://analytics.med.wanfangdata.com.cn/Author/KeywordsChartData"
# url = "http://analytics.med.wanfangdata.com.cn/Author/RelationChartData"
# headers = {"Cookie":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1614149661; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%2c%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2298ac77b6-ba1e-48e1-b3ea-ec2f01d6688b%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-02-25T09%3a31%3a56Z%22%2c%22TicketSign%22%3a%22j6QU5f9Kq0uypGS7f%2bU3%5c%2fg%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1614245520",}
# data = {"StartYear":"2012",
#         "EndYear":"2021",
#         "Id":"A000491159",
#         "IETag":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
# res = requests.post(url,headers=headers,data=data).text
# print(res)
# try:
#     ress = json.loads(res)
# except:
#     time.sleep(3)
#     ress = json.loads(res)
# # print(ress)
# listdata = ress['list']
# for i in listdata:
#     # 合作者
#     AuthorName = i['AuthorName']
#
#     # 合作者ID
#     AuthorId = i['AuthorId']
#
#     # 合作者单位
#     OrgName = i['OrgName']
#
#     # 合作发文数
#     Count = i['Count']
#
#     print(AuthorName,AuthorId,OrgName,Count)

# url = "https://xueshu.baidu.com/usercenter/data/author"
# headers = {"Cookie":"BIDUPSID=21404EC1D0D59137A3A60DE92656350F; PSTM=1611811793; BAIDUID=48891841DA22B8137F336DEFF4E1A331:FG=1; __yjs_duid=1_e84683d4890fdc6e86ff92f11b2456201612149238508; Hm_lvt_d0e1c62633eae5b65daca0b6f018ef4c=1613729387; H_PS_PSSID=33258_33273_33570_26350; BDSFRCVID=73LOJeCmHCNCaEReMVEm5NVXmeKK0gOTHllnwjo-rLa2BoDVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJkeVIKyJDI3fP36q46E-tCqMfQyb-vt2jIX3b7EfhTFEq7_bf--Dx_yha_Jt4Qu0Jcf_lrCyn68oDQ456oxy5K_hpbIL6byBTPDa4cuMqbqVhvHQT3mbqQbbN3i-4jwL6nMWb3cWKJV8UbS3JoPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKOtj88JbPqV-35b5r5DnQmqtOo5P6HhxoJq5-eBgOZ0lOEWpOFEnjH04oY3xLDjtTpXPr-W20j0h7mWnRSD43FhIcKX-oXLxnRLfT-0bc4KKJxbnLWeIJo5t5lQtAXhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFaDToQDMK; delPer=0; PSINO=2; BDSFRCVID_BFESS=73LOJeCmHCNCaEReMVEm5NVXmeKK0gOTHllnwjo-rLa2BoDVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJkeVIKyJDI3fP36q46E-tCqMfQyb-vt2jIX3b7EfhTFEq7_bf--Dx_yha_Jt4Qu0Jcf_lrCyn68oDQ456oxy5K_hpbIL6byBTPDa4cuMqbqVhvHQT3mbqQbbN3i-4jwL6nMWb3cWKJV8UbS3JoPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKOtj88JbPqV-35b5r5DnQmqtOo5P6HhxoJq5-eBgOZ0lOEWpOFEnjH04oY3xLDjtTpXPr-W20j0h7mWnRSD43FhIcKX-oXLxnRLfT-0bc4KKJxbnLWeIJo5t5lQtAXhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFaDToQDMK; BAIDUID_BFESS=E9BB7EA5AAE3BBF24356238B754CFC60:FG=1; antispam_key_id=45; antispam_site=ae_xueshu_homepage; Hm_lpvt_d0e1c62633eae5b65daca0b6f018ef4c=1614562549; ab_sr=1.0.0_YmYwYjE2YjMxMzdhYTI3MWEyOThlMzVlOWIyYTRmMjBjMTM1Yzg5Njk3YjY1MzhmZjE2YzFlNGEyYjNjNjNjODU4OTJkMDNmMWUwY2U5N2FhMTI1Y2JlYTQ1ZmIyYTg5; antispam_data=3620979ef016276132a6f53e4d9a245d930b6afe98cd85a51be4f3f1cef653f42fdcd5ff8b7ba209c3d57fa2a4c3fb09cb63f90d8414a2190ad0adc231d2168647b7646611083de9bfc37b74abf2dc46cf2e98b86887887c8bf1ddfb4cc7e2f8; antispam_sign=37880dc6",
#            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
# data = {"_token":"0dbc6cb13fb6c983d62c2c6256fd133265fa10af54dffd561ca5c3dd78ac7547",
#         "_ts":"1614562548",
#         "_sign":"10f71d0accc0aba95f2e17837f2bcb8d",
#         "cmd":"show_co_affiliate",
#         "entity_id":"fb4d664b2a985ed2b4fc9b08b0d8e8a4"}
# # data = {"_token":"0dbc6cb13fb6c983d62c2c6256fd133265fa10af54dffd561ca5c3dd78ac7547",}
# res = requests.post(url,headers=headers,data=data).text
# print(res)

# url = "http://analytics.med.wanfangdata.com.cn/Author/Overview/A004290507"
# url = url[url.rfind("/")+1:]
# print(url)

# import random
# random = random.randint(1,3)
# print(random)
# import urllib.parse
# a = '时勘'
# b = urllib.parse.quote(a)
# print(b)
#
# c = '中国'
# d = urllib.parse.quote(c)
# print(d)
#
# url = "https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=search_author&_token=c58720f8a5813af438390526a661c8fc5ecf2ab120578e7df1a3b4afb7d8be29&_ts=1614649756&_sign=d4bc00763bfb289d1258c40619058e27&author={}&affiliate={}&curPageNum=1".format(b,d)
#
# res = requests.get(url).text
# print(res)
import re
# url = "\/homepage\/u\/762185c6d65061cbaa269b7695b57508"
# aa = url.replace("\\","")
# print(aa)

url = 'https://xueshu.baidu.com/homepage/u/7c12ddb522a3eda55ef399bdedbe9927'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
           "Cookie":"BIDUPSID=21404EC1D0D59137A3A60DE92656350F; PSTM=1611811793; BAIDUID=48891841DA22B8137F336DEFF4E1A331:FG=1; __yjs_duid=1_e84683d4890fdc6e86ff92f11b2456201612149238508; Hm_lvt_d0e1c62633eae5b65daca0b6f018ef4c=1613729387; BDSFRCVID=73LOJeCmHCNCaEReMVEm5NVXmeKK0gOTHllnwjo-rLa2BoDVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJkeVIKyJDI3fP36q46E-tCqMfQyb-vt2jIX3b7EfhTFEq7_bf--Dx_yha_Jt4Qu0Jcf_lrCyn68oDQ456oxy5K_hpbIL6byBTPDa4cuMqbqVhvHQT3mbqQbbN3i-4jwL6nMWb3cWKJV8UbS3JoPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKOtj88JbPqV-35b5r5DnQmqtOo5P6HhxoJq5-eBgOZ0lOEWpOFEnjH04oY3xLDjtTpXPr-W20j0h7mWnRSD43FhIcKX-oXLxnRLfT-0bc4KKJxbnLWeIJo5t5lQtAXhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFaDToQDMK; BDSFRCVID_BFESS=73LOJeCmHCNCaEReMVEm5NVXmeKK0gOTHllnwjo-rLa2BoDVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJkeVIKyJDI3fP36q46E-tCqMfQyb-vt2jIX3b7EfhTFEq7_bf--Dx_yha_Jt4Qu0Jcf_lrCyn68oDQ456oxy5K_hpbIL6byBTPDa4cuMqbqVhvHQT3mbqQbbN3i-4jwL6nMWb3cWKJV8UbS3JoPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKOtj88JbPqV-35b5r5DnQmqtOo5P6HhxoJq5-eBgOZ0lOEWpOFEnjH04oY3xLDjtTpXPr-W20j0h7mWnRSD43FhIcKX-oXLxnRLfT-0bc4KKJxbnLWeIJo5t5lQtAXhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFaDToQDMK; antispam_site=ae_xueshu_homepage; antispam_key_id=45; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=9BZkZMT2FpaE9Gc2pCUUJFSWdJcVlaWHZFWXdmaXRsT1RCUjRjbElOaEpZbVZnRVFBQUFBJCQAAAAAAAAAAAEAAAChiKM8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEnVPWBJ1T1gVU; BDUSS_BFESS=9BZkZMT2FpaE9Gc2pCUUJFSWdJcVlaWHZFWXdmaXRsT1RCUjRjbElOaEpZbVZnRVFBQUFBJCQAAAAAAAAAAAEAAAChiKM8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEnVPWBJ1T1gVU; H_PS_PSSID=33258_33273_33595_33570_26350; BAIDUID_BFESS=243B0AC0925C64553AE9498AC6E45723:FG=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=2; BA_HECTOR=2ga125aga00k05853v1g3tr630q; ZD_ENTRY=baidu; Hm_lpvt_d0e1c62633eae5b65daca0b6f018ef4c=1614738193; ab_sr=1.0.0_MDI4MDdjOGYxOWM5ODM4NmM2Mjc5MGU3NzQwYmU4MjI4ZTZjZmRkOTliNWE5MzIwZmQzOGRjZmJlZGNlNzllOGIzOTc5NGZkNGQ1ODJkZDM1Zjc4NDQ2NjlhNWMzOTg2; antispam_data=3620979ef016276132a6f53e4d9a245d930b6afe98cd85a51be4f3f1cef653f42fdcd5ff8b7ba209c3d57fa2a4c3fb094d54830eb081caeba07c099e0d05d441ba14ced4df6218a1e511ac2bf252b77f6b7b607d63f5ebc24411561983e726ac; antispam_sign=c0438edb",}
# data ={"_token":"2b476d2b00df7b34db455ffd6804f8ebfdea498ba09ec6f6e6ca0278c3f3ba94",
#         "entity_id":"8c184ace829e1e5e5d7863642758b064",
#        "_ts":"1614682205",
#        "_sign":"03d51b8c8ce6c2aa104c1efc2b313adc",
# }
# res = requests.get(url,headers=headers).text
# print(res)
# ele = etree.HTML(res)
# cooperative_scholar_number1 = ele.xpath('//div[@class="co_relmap_wrapper"]/a[1]/div/@paper-count')
# print(cooperative_scholar_number1)
# href = ele.xpath('//div[@class="co_relmap_wrapper"]/a[1]/@href')
# print(href)


# url = "https://xueshu.baidu.com/scholarID/CN-BD75QSRJ"
# headers = {"Cookie":"BIDUPSID=21404EC1D0D59137A3A60DE92656350F; PSTM=1611811793; BAIDUID=48891841DA22B8137F336DEFF4E1A331:FG=1; __yjs_duid=1_e84683d4890fdc6e86ff92f11b2456201612149238508; Hm_lvt_d0e1c62633eae5b65daca0b6f018ef4c=1613729387; H_PS_PSSID=33258_33273_33570_26350; BDSFRCVID=73LOJeCmHCNCaEReMVEm5NVXmeKK0gOTHllnwjo-rLa2BoDVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJkeVIKyJDI3fP36q46E-tCqMfQyb-vt2jIX3b7EfhTFEq7_bf--Dx_yha_Jt4Qu0Jcf_lrCyn68oDQ456oxy5K_hpbIL6byBTPDa4cuMqbqVhvHQT3mbqQbbN3i-4jwL6nMWb3cWKJV8UbS3JoPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKOtj88JbPqV-35b5r5DnQmqtOo5P6HhxoJq5-eBgOZ0lOEWpOFEnjH04oY3xLDjtTpXPr-W20j0h7mWnRSD43FhIcKX-oXLxnRLfT-0bc4KKJxbnLWeIJo5t5lQtAXhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFaDToQDMK; BDSFRCVID_BFESS=73LOJeCmHCNCaEReMVEm5NVXmeKK0gOTHllnwjo-rLa2BoDVJeC6EG0Ptf8g0KubUElrogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJkeVIKyJDI3fP36q46E-tCqMfQyb-vt2jIX3b7EfhTFEq7_bf--Dx_yha_Jt4Qu0Jcf_lrCyn68oDQ456oxy5K_hpbIL6byBTPDa4cuMqbqVhvHQT3mbqQbbN3i-4jwL6nMWb3cWKJV8UbS3JoPBTD02-nBat-OQ6npaJ5nJq5nhMJmb67JDMr0eGKOtj88JbPqV-35b5r5DnQmqtOo5P6HhxoJq5-eBgOZ0lOEWpOFEnjH04oY3xLDjtTpXPr-W20j0h7mWnRSD43FhIcKX-oXLxnRLfT-0bc4KKJxbnLWeIJo5t5lQtAXhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TFaDToQDMK; antispam_site=ae_xueshu_homepage; antispam_key_id=45; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=2; BAIDUID_BFESS=76696CAB5EA6ED064F41D70DAC55E221:FG=1; BDUSS=9BZkZMT2FpaE9Gc2pCUUJFSWdJcVlaWHZFWXdmaXRsT1RCUjRjbElOaEpZbVZnRVFBQUFBJCQAAAAAAAAAAAEAAAChiKM8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEnVPWBJ1T1gVU; BDUSS_BFESS=9BZkZMT2FpaE9Gc2pCUUJFSWdJcVlaWHZFWXdmaXRsT1RCUjRjbElOaEpZbVZnRVFBQUFBJCQAAAAAAAAAAAEAAAChiKM8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEnVPWBJ1T1gVU; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; ZD_ENTRY=baidu; Hm_lpvt_d0e1c62633eae5b65daca0b6f018ef4c=1614670926; ab_sr=1.0.0_MmFlZDNlMjNhNDgzMjU1NjY4OWZiYTQ3YTE3MGJmOGFhNGJlYjkwODk3M2VkZmFiMzQwNjA0MTdjY2UwYWVmYmMyYTE3N2Y1MTlmMDdjYWNhZjQ2M2NiYWFhZTQzZWM1; antispam_data=3620979ef016276132a6f53e4d9a245d930b6afe98cd85a51be4f3f1cef653f42fdcd5ff8b7ba209c3d57fa2a4c3fb097c70610749ac6d6d1597e3015e8d0be492b34ec77e07b66951ee0133fa60cfb9c50ca565607929f3473d3b8891b1d87e; antispam_sign=e3904e4c",
#            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
# res = requests.get(url,headers=headers).text
# print(res)


# aa = '20200930'
# bb = '-'
# list_aa = list(aa)
# list_aa.insert(4,bb)
# list_aa.insert(7,bb)
# dd = ''.join(list_aa)
# print(dd)
#
# # dd = list(cc).insert(7,bb)
# timeArray = time.strptime(aa,"%Y%m%d")
# accept_date = int(time.mktime(timeArray))
# print(accept_date)

# dic = {'a': 1, 'b': 2}
# dic["c"] = dic.pop("a")
# print(dic)























