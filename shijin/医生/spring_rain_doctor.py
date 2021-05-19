import requests,json,time
from lxml import etree
import pymongo
import hashlib

# # 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['spider_py']
table = mdb['springrain_doctor']
while True:
    url = "https://www.chunyuyisheng.com/pc/doctor/clinic_web_3c8d944448ba68c7/"
    headers = {"authority":"www.chunyuyisheng.com",
                "method":"GET",
                "path":"/pc/doctor/c4bf333ff3f4732e0d18/",
                "scheme":"https",
                "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding":"gzip, deflate, br",
                "accept-language":"zh-CN,zh;q=0.9",
                "cache-control":"max-age=0",
                "cookie":"Hm_lvt_c153f37e6f66b16b2d34688c92698e4b=1613731547,1614332414,1615258108,1615258186; Hm_lpvt_c153f37e6f66b16b2d34688c92698e4b=1615271485",
                "referer":"https://www.chunyuyisheng.com/pc/doctors/?page=31",
                "sec-ch-ua-mobile":"?0",
                "sec-fetch-dest":"document",
                "sec-fetch-mode":"navigate",
                "sec-fetch-site":"same-origin",
                "sec-fetch-user":"?1",
                "upgrade-insecure-requests":"1",
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    time.sleep(1)
    try:
        res = requests.get(url,headers=headers).text
    except:
        time.sleep(5)
    ele = etree.HTML(res)

    ##医生名称
    doctor_name = ele.xpath('//span[@class="name"]/text()')
    doctor_name = ''.join(doctor_name).strip()
    # print(doctor_name)

    ##医生职称
    title_of_public_health_technician = ele.xpath('//span[@class="grade"]/text()')
    title_of_public_health_technician = ''.join(title_of_public_health_technician).strip()
    # print(title_of_public_health_technician)

    ##医院
    hospital_name = ele.xpath('//a[@class="hospital"]/text()')
    hospital_name = ''.join(hospital_name).strip()
    # print(hospital_name)

    ##科室
    subject = ele.xpath('//a[@class="clinic"]/text()')
    subject = ''.join(subject).strip()
    # print(subject)

    ##医生标签
    label = ele.xpath('//div[@class="doctor-hospital"]/span/text()')
    label = ''.join(label).strip()
    # print(label)

    ##擅长
    specialize = ele.xpath('//div[@class="ui-grid ui-main clearfix"]/div[4]/p/text()')
    specialize = ''.join(specialize).strip()
    # print(specialize)

    ##简介
    intro = ele.xpath('//div[@class="ui-grid ui-main clearfix"]/div[3]/p/text()')
    intro = ''.join(intro).strip()
    # print(intro)

    ##医院地址
    hospital_place = ele.xpath('//div[@class="ui-grid ui-main clearfix"]/div[5]/p/text()')
    hospital_place = ''.join(hospital_place).strip()
    # print(hospital_place)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    aa = doctor_name+' '+hospital_name
    print(aa)
    def md5Encode(str):
        m = hashlib.md5()  # 创建md5对象
        m.update(str)  # 传入需要加密的字符串进行MD5加密
        return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
    esid = md5Encode(aa.encode('utf-8'))  # 必须先进行转码，否则会报错

    mongo_dict = {}
    mongo_dict['doctor_name'] = doctor_name
    mongo_dict['title_of_public_health_technician'] = title_of_public_health_technician
    mongo_dict['hospital_name'] = hospital_name
    mongo_dict['subject'] = subject
    mongo_dict['label'] = label
    mongo_dict['specialize'] = specialize
    mongo_dict['intro'] = intro
    mongo_dict['hospital_place'] = hospital_place
    table.insert(mongo_dict)