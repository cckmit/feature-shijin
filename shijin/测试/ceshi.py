import json
import time
import requests
from lxml import etree
es_dict = {"aa":"bb"}
# with open("./医药自媒体.json", 'w', encoding="utf-8") as fp:
#     json.dump(es_dict, fp)
#     print('写入文件成功')

# json_str = json.dumps(es_dict)
# with open('医药自媒体.json', 'w') as json_file:
#     json_file.write(json_str)

# j = "https://mma.prnasia.com/media2/1490493/image1.jpg"
# src_index = -7
# aa = j[j.rfind("/")+src_index:].replace('/','').replace('_','')
# print(aa)

# aa = str(int(time.time()))
# print(aa)
import xlrd
import pymongo
## 连接mongodb数据库
# client = pymongo.MongoClient('localhost', 27017)
# mdb = client['spider_py']
# wangfang_id = mdb['wangfang_id']
# # 打开文件
# data = xlrd.open_workbook("D:\software\百度下载\work\期刊分析-四次爬取3000.xlsx")
# # 查看工作表
# data.sheet_names()
# # 通过文件名获得工作表,获取工作表1
# table = data.sheet_by_name('Sheet1')
# scholarID_list = table.col_values(0)
# for scholarID in scholarID_list:
#     wangfang_dict = {}
#     wangfang_dict['scholarID'] = scholarID
#     wangfang_id.insert(wangfang_dict)

import random

# cookie_list = [
# {"Cookie1":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.dylan2021%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.dylan2021.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%22f34ca3e0-c68b-4cc2-bc29-8a764ed00c65%22%2c%22Sign%22%3a%22d3lkH%5c%2fqHhENlTYKDRLqWjAeV75CdSob18Sl%2b8C8nrbuSNl1VE4WrwsTAfT7OIuuw%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a41%3a32Z%22%2c%22TicketSign%22%3a%22FtlEknh%5c%2f5NqI97In4mPbhg%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619494920"},
# {"Cookie2":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.orangerrt%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.orangerrt.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%2287bbf885-66ae-4c66-a394-af0997814096%22%2c%22Sign%22%3a%22t7dos5%2bH4GAjx7jwg%5c%2fbVqyk9FEqIt4peQg7MOqG3O7qEyAwzmTGzXOJ9ExouWTrO%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a48%3a41Z%22%2c%22TicketSign%22%3a%22hvGxJEgCijaUA3DAbWbNlw%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495323"},
# {"Cookie3":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.srj456%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.srj456.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%22cfe11fc3-b1c1-4aa0-9d05-a9ff71a3dfb0%22%2c%22Sign%22%3a%22ctgblh0xWin4iXiWuEY2epOVyjg1wD3DzBmXv5UYY1uL4mWjHlshsxG%5c%2feTuL32ev%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a51%3a34Z%22%2c%22TicketSign%22%3a%2234br4KqNGK1AO6KnSpM2Tg%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495497"},
# {"Cookie4":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.QQ%e5%b0%8f%e4%b8%b8%e5%ad%90%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.QQ%e5%b0%8f%e4%b8%b8%e5%ad%90.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%228533c47e-57ed-4be6-831f-a8a8dab0a2a4%22%2c%22Sign%22%3a%22W3gD%2bDVzCpvNVa4xxd7l8HFowgWcFsB3yibO8zc1xp92X0fvL68s8wNhqolEncxz%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a53%3a03Z%22%2c%22TicketSign%22%3a%22pWnBn2X%5c%2fpnjn1NdmPP8Leg%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495588"},
# {"Cookie5":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.skygrid%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.skygrid.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%228533c47e-57ed-4be6-831f-a8a8dab0a2a4%22%2c%22Sign%22%3a%22g5SNx42veNgOq4PLPTUBV7QNAeDmFrQj6U%2bOvQWXGn6mkXp6NlImsApe%5c%2f4lN%5c%2fK6e%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a54%3a04Z%22%2c%22TicketSign%22%3a%22h94VN52Bd43Bf6swAGMKjA%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495654"},
# {"Cookie6":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.mmqmmq%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.mmqmmq.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%226bbf5372-525b-4439-9ad3-0bcc30495cc0%22%2c%22Sign%22%3a%22rTR9508HjYOCb5fqmZJzDygA0W1ssLC6LeB%2biBNqzCCktKrvWqv6QhKAbN3f2WDz%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a55%3a24Z%22%2c%22TicketSign%22%3a%22MC8qzkREN9%5c%2fBASi5Zt5CXw%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495730"},
# {"Cookie7":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.jjyy2020%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.jjyy2020.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%226bbf5372-525b-4439-9ad3-0bcc30495cc0%22%2c%22Sign%22%3a%22pAumXg5WHBswKojsKqMYBP4l%5c%2fWMBBpMRRaVp3wseO0D%2bF%5c%2f1do3YAisfwn%2bTJFW28%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a56%3a21Z%22%2c%22TicketSign%22%3a%22MrQdnJ9RzoPWWTZ52XgI0A%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495783"},
# {"Cookie8":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.mrmw86%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.mrmw86.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%226bbf5372-525b-4439-9ad3-0bcc30495cc0%22%2c%22Sign%22%3a%22Ba6iQehTQUd05ZpMtG3DA8aPfeniQp0gCXiUa45KGlM1tznYMLkgue8hYQYFm5ON%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a57%3a18Z%22%2c%22TicketSign%22%3a%22gvcj3s6MUdhq6LJ5EyEopQ%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495841"},
# {"Cookie9":"Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1619319239,1619353829,1619400414,1619488517; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.YYMFQX%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.YYMFQX.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%226bbf5372-525b-4439-9ad3-0bcc30495cc0%22%2c%22Sign%22%3a%22wpN8T6axewdLZP32qw0ddn6cTJ9LEtPBVZVtz4zXYwZdBY%2b%5c%2f9i3XIFnuxeA2tFPl%22%7d%2c%22LastUpdate%22%3a%222021-04-27T03%3a58%3a07Z%22%2c%22TicketSign%22%3a%22nP7s4W6C5yLRuSiVrFBS1g%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619495890"},
# ]
# random_cookie = random.choice(cookie_list)
# print(random_cookie)
import re

# jj = '/-/media/gileadchina/image/news/041502.jpg?la=zh-cn&hash=E6E442AC271099CF073E9B75739D114F'
# j = "https://www.gileadchina.cn" + ''.join(re.findall(r'.*?jpg', jj)) + ''.join(re.findall(r'.*?png', jj))
# print(j)

# j = 'Clinical trial information: NCT03676920'
# aa = j[j.rfind(" ")+1:]
# print(aa)

# a = ['A01B1/00', 'Hand', 'tools', '(edge', 'trimmers', 'for', 'lawns', 'A01G3/06', '{;', 'machines', 'for', 'working', 'soil', 'A01B35/00;', 'making', 'hand', 'tools', 'B21D})']
# number_list = ['0','1','2','3','4','5','6','7','8','9',]
# if a[1] in number_list:
#     a.remove(a[1])

# aa = round(time.time())
# print(aa)
# print(type(aa))
# str(round(time.time())-3475)

import requests
from lxml import etree
# headers = {
#             "authority":"ascopubs.org",
#             "method":"GET",
#             "path":"/jco/meeting?expanded=tvolume-suppl.d2020.y2020&expanded=tvolume-suppl.d2010",
#             "scheme":"https",
#             "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#             "accept-encoding":"gzip, deflate, br",
#             "accept-language":"zh-CN,zh;q=0.9",
#             "cache-control":"max-age=0",
#             "cookie":"timezone=480; __na_c=1; __cfduid=d2261fb4b141cee137b326d04d507766d1619502428; MAID=F7hlMFSQxgS/hXTPEnQenQ==; I2KBRCK=1; _ga=GA1.2.518511993.1619502439; __na_u_38176768=14674013713890; __gads=ID=fef9ac3278aed8a0:T=1619502468:S=ALNI_Mb5rrN7HlecHM1yQA5RV8gclF3utg; __adroll_fpc=4401c3e5cb6f125c724a208f814f848b-1619502472992; BCSessionID=de525ae5-a73b-48e7-89f6-ceae57a8ceb8; OptanonAlertBoxClosed=2021-04-27T07:02:01.614Z; SERVER=WZ6myaEXBLH0cjxF1pGSsg==; MACHINE_LAST_SEEN=2021-05-12T23%3A13%3A14.064-07%3A00; AMCVS_FC92401053DA88170A490D4C%40AdobeOrg=1; HSPVerifiedv2=0; at_check=true; s_cc=true; _gid=GA1.2.716570272.1620886410; OptanonConsent=isIABGlobal=false&datestamp=Thu+May+13+2021+16%3A24%3A34+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.3.0&landingPath=NotLandingPage&groups=0_166217%3A1%2C118%3A1%2C1%3A1%2C2%3A1%2C101%3A1%2C3%3A1%2C0_166190%3A1%2C133%3A1%2C103%3A1%2C4%3A1%2C104%3A1%2C0_166216%3A1%2C106%3A1%2C108%3A1%2C109%3A1%2C110%3A1%2C111%3A1%2C112%3A1%2C114%3A1%2C117%3A1%2C119%3A1%2C120%3A1%2C125%3A1%2C130%3A1%2C132%3A1%2C135%3A1%2C0_166191%3A1&AwaitingReconsent=false&consentId=bea1a4ff-90d6-4a83-89f4-5f1f29c0bf5a; __atuvc=14%7C17%2C63%7C18%2C5%7C19; _uetsid=58a74d10b3b211eba2a41d7e61485d3e; _uetvid=0a1935a0a71c11ebb99b97987f65876c; AMCV_FC92401053DA88170A490D4C%40AdobeOrg=-432600572%7CMCIDTS%7C18761%7CMCMID%7C06930884177293802462024934333585990412%7CMCAAMLH-1621499081%7C11%7CMCAAMB-1621499081%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1620901481s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; s_sq=%5B%5BB%5D%5D; mbox=PC#c774fedd96414218b75a9fb34b74bd36.38_0#1684139082|session#03b299fbacd541c7b59c765a07fab260#1620896139; last_visit_bc=1620894310466; __ar_v4=OIH2U2CADJHSBHW2L3UKNL%3A20210427%3A52%7CFWR2SALTD5ALHBY3VF34MI%3A20210427%3A52%7CXGLZLLDJCFFYHBF4LCLF5K%3A20210427%3A52",
#             "sec-ch-ua":'"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
#             "sec-ch-ua-mobile":"?0",
#             "sec-fetch-dest":"document",
#             "sec-fetch-mode":"navigate",
#             "sec-fetch-site":"same-origin",
#             "sec-fetch-user":"?1",
#             "upgrade-insecure-requests":"1",
#             "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

# url = "https://www.annalsofoncology.org/issue/S0923-7534(16)X6400-9"
# headers = {"sec-ch-ua":'"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
#             "sec-ch-ua-mobile":"?0",
#             "Upgrade-Insecure-Requests":"1",
#             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
#
# res = requests.get(url=url,headers=headers)
# print(res.status_code)
# ele = etree.HTML(res.text)
# meeting_name = ele.xpath('//ul[@class="rlist--inline download-links"]/li[1]/a/@href')
# print(meeting_name)
# for i in meeting_name:
#     print(i.strip().replace('\n', '').replace('\r', ''))


aa = "EudraCT 2016-000148-32; NCT02723955."
bb = aa[aa.rfind(" ")+1:-1]
print(bb)