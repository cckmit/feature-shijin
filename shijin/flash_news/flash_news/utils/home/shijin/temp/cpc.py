import zipfile
import os.path
import codecs
import hashlib
import time
import xml.dom.minidom
import pymongo
import json
import datetime
import bson

# # 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['cpc']
table = mdb['classification_cpc']

start = datetime.datetime.now()

parent_path=(r'../temp/') #父文件夹路径
for root, dirs, files in os.walk(parent_path):
    if 'CPC' in root and '\Doc' not in root:
        path_validity_file = root
    # 读取文件名  这里在解压缩
    # for name in files:
    #     # print(name)
    #     if 'SCHEME_XML' in name:
    #         name = 'SCHEME_XML.zip'
    #         extracting = zipfile.ZipFile(name)
    #         print(extracting)
    #         extracting.extractall("scheme_xml")
    #         extracting.close()
    #
    #     if 'TITLE_LIST' in name:
    #         name = 'TITLE_LIST.zip'
    #         extracting2 = zipfile.ZipFile(name)
    #         print(extracting2)
    #         extracting2.extractall("title_list")
    #         extracting2.close()
    #
    #     if 'VALIDITY_FILE' in name:
    #         name = 'VALIDITY_FILE.zip'
    #         extracting3 = zipfile.ZipFile(name)
    #         print(extracting3)
    #         extracting3.extractall("validity_file")
    #         extracting3.close()

# 打开xml文档的解析 scheme_xml
cpc_scheme_dict = {}
path = "./scheme_xml/"
files = os.listdir(path)  # 得到文件夹下所有文件名称
for i in files:
    if len(str(i)) == 16:
        # 打开xml文档
        dom = xml.dom.minidom.parse(os.path.join(path,i))
        # 得到文档元素对象
        root = dom.documentElement
        itemlist = root.getElementsByTagName('classification-item')
        for i in range(len(itemlist)):
            item = itemlist[i]
            level = item.getAttribute("level")
            big_cpc_scheme = item.getAttribute("sort-key")
            big_cpc_scheme_dict = {}
            big_cpc_scheme_dict[big_cpc_scheme] = level
            if int(big_cpc_scheme_dict[big_cpc_scheme]) == 3:
                continue
            else:
                # print('第一：',big_cpc_scheme_dict)
                cpc_scheme_dict.update(big_cpc_scheme_dict)

    if len(str(i)) == 19:
        # 打开xml文档
        dom = xml.dom.minidom.parse(os.path.join(path, i))
        # 得到文档元素对象
        root = dom.documentElement
        itemlist = root.getElementsByTagName('classification-item')
        for i in range(len(itemlist)):
            item = itemlist[i]
            level = item.getAttribute("level")
            small_cpc_scheme = item.getAttribute("sort-key")
            small_cpc_scheme_dict = {}
            small_cpc_scheme_dict[small_cpc_scheme] = level
            if int(small_cpc_scheme_dict[small_cpc_scheme]) == 6:
                continue
            else:
                # print('第二：',small_cpc_scheme_dict)
                cpc_scheme_dict.update(small_cpc_scheme_dict)

print('读一：',cpc_scheme_dict)
#
# # # 2.打开txt文档解析 title_list
title_dict = {}
path_title_list = "./title_list/"
file_title_list = os.listdir(path_title_list)  # 得到文件夹下所有文件名称
len_file_title_list = len(file_title_list)
m = 0
while True:
    m += 1
    file = file_title_list.pop(0)
    f = codecs.open(path_title_list+file, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
    line = f.readline()  # 以行的形式进行读取文件
    while True:
        a = line.split()
        if len(a) == 0:
            break
        cpc_title_list = a[0]
        definition_en = a[1:]
        definition_en = ' '.join(definition_en)
        title_list_dict = {}
        title_list_dict[cpc_title_list] = definition_en
        # print('第三：',title_list_dict)
        title_dict.update(title_list_dict)
        line = f.readline()
    if m == len_file_title_list:
        break
f.close()

print('读二：',title_dict)

# # # 3.打开txt文档解析 validity_file
validity_dict = {}
file_validity_file = os.listdir(path_validity_file)  # 得到文件夹下所有文件名称
print(path_validity_file)
file = file_validity_file[0]
# # 打开txt文件
f = codecs.open(path_validity_file+'/'+file, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
line = f.readline()  # 以行的形式进行读取文件
while True:
    a = line.split()
    if len(a) == 0:
        break
    cpc_symbol = a[0]
    valid_from_data = a[1]
    if '-' not in valid_from_data:
        pass
    else:
        timeArray = time.strptime(valid_from_data,"%Y-%m-%d")
        valid_from_data= bson.int64.Int64(int(time.mktime(timeArray)))
    try:
        valid_to_data = a[2]
    except:
        valid_to_data = ''
    if len(valid_to_data) == 0:
        pass
    if '-' not in valid_to_data:
        pass
    else:
        timeArray = time.strptime(valid_to_data, "%Y-%m-%d")
        valid_to_data = bson.int64.Int64(int(time.mktime(timeArray)))
    validity_file_dict_next = {}
    validity_file_dict_next["valid_from_data"] = valid_from_data
    validity_file_dict_next["valid_to_data"] = valid_to_data
    validity_file_dict = {}
    validity_dict[cpc_symbol] = validity_file_dict_next
    # print('第四：',validity_file_dict)
    validity_dict.update(validity_file_dict)
    line = f.readline()
f.close()

print('读三：',validity_dict)

scheme_title = {}
for key in title_dict:
    # print(key)
    if cpc_scheme_dict.get(key):
        scheme_title[key] = title_dict[key]
print('组合一：',scheme_title)

scheme_validity = {}
for keys in validity_dict:
    if cpc_scheme_dict.get(keys):
        scheme_validity[keys] = validity_dict[keys]
print('组合二：',scheme_validity)

title_validity = {}
for i in scheme_title:
    if scheme_validity.get(i):
        title_validity[i] = scheme_title[i]
print('组合三：',title_validity)

for cpc_no in title_validity:
    leval = cpc_scheme_dict[cpc_no]
    definition_en = title_dict[cpc_no]
    valid_from_date = validity_dict[cpc_no]['valid_from_data']
    valid_to_date = validity_dict[cpc_no]['valid_to_data']
    def md5Encode(str):
        m = hashlib.md5()  # 创建md5对象
        m.update(str)  # 传入需要加密的字符串进行MD5加密
        return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
    esid = md5Encode(cpc_no.encode('utf-8'))  # 必须先进行转码，否则会报错

    all_dict = {}
    all_dict["esid"] = esid
    all_dict["cpc_no"] = cpc_no
    all_dict["leval"] = leval
    all_dict["definition_en"] = definition_en
    all_dict["valid_from_date"] = valid_from_date
    all_dict["valid_to_date"] = valid_to_date
    table.insert(all_dict)
    print(esid,cpc_no, leval, definition_en, valid_from_date, valid_to_date)

end = datetime.datetime.now()
print(end-start)

""""
1 = {'CPC_Symbol':{"Valid_From_Date":'2012-01-01','Valid_To_Date':'2012-01-02'}}
2 = {}
3 ={}
data ={}
for 遍历这些字典的键。把值带上。对比之后加入新的字典中。
"""



