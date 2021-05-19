import json
import time
import requests
import pymongo
import xlrd

# ## 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['spider_py']
country_pharm = mdb['country_pharm']

url = "https://fuwu.nhsa.gov.cn/ebus/fuwu/api/base/api/drugOptins/queryDrugOptinsInfoDetail"
headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; LYA-AL10 Build/LYZ28N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36HSABrowser/1.2.2",
    "Content-Type":"application/json;charset=UTF-8",
    "Accept":"application/json, text/plain, */*",
    "orgCode":"110101",
    "channel":"app",
    "Referer":"https://fuwu.nhsa.gov.cn/hsafront/",
    "Accept-Language":"zh-CN,en-US;q=0.8",
    "X-Requested-With":"cn.hsa.app",
}
# 打开文件
# data = xlrd.open_workbook("D:\software\百度下载\work\医保省份.xlsx")
# # 查看工作表
# data.sheet_names()
# # 通过文件名获得工作表,获取工作表1
# table = data.sheet_by_name('Sheet1')
# province_ll = table.col_values(0)
# for province in province_ll:
#     ll = [
#         '乙磺酸尼达尼布软胶囊',
#         '依达拉奉氯化钠注射液',
#         '地舒单抗注射液',
#         '度普利尤单抗注射液',
#         '恩扎卢胺软胶囊',
#         '曲美替尼片',
#         '替雷利珠单抗注射液',
#         '氘丁苯那嗪片',
#         '注射用伊尼妥单抗',
#         '注射用卡瑞利珠单抗',
#         '注射用贝利尤单抗',
#         '泽布替尼胶囊',
#         '特瑞普利单抗注射液',
#         '甲磺酸仑伐替尼胶囊',
#         '甲磺酸氟马替尼片',
#         '甲磺酸达拉非尼胶囊',
#         '甲磺酸阿美替尼片',
#         '甲苯磺酸尼拉帕利胶囊',
#         '盐酸可洛派韦胶囊',
#           ]
#     for pharm in ll:
#         dataa = {"data":{"pageNum":2,"pageSize":20,"drugName":pharm,"medinsType":1,"province":province,"region":""}}
dataa = {"data":{"pageNum":3,"pageSize":20,"drugName":"特瑞普利单抗注射液","medinsType":1,"province":"河南省","region":""}}
res = requests.post(url=url,headers=headers,data=json.dumps(dataa),verify=False)
res = json.loads(res.text)
for i in res["data"]["list"]:
    # 药品名称
    drugName = i["drugName"]
    print(drugName)

    # 省
    province = i["province"]
    print(province)

    # 区
    region = i["region"]
    print(region)

    # 医院名
    medinsName = i["medinsName"]
    print(medinsName)

    # 医院地址
    addr = i["addr"]
    print(addr)

    pharm_dict = {}
    pharm_dict['drugName'] = drugName
    pharm_dict['province'] = province
    pharm_dict['region'] = region
    pharm_dict['medinsName'] = medinsName
    pharm_dict['addr'] = addr
    country_pharm.insert(pharm_dict)









