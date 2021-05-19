import zipfile
import os.path
import codecs
import hashlib
import time
import xml.dom.minidom
import pymongo
import datetime
import bson

# # 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['spider_py']
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
d = {}
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
                cpc_scheme_dict.update(big_cpc_scheme_dict)

            value = ''.join(list(big_cpc_scheme_dict.values()))
            if value == '2':
                super_key = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('2')]
            if value == '4':
                keyy = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('4')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)

            if value == '4':
                super_key = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('4')]
            if value == '5':
                keyy = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('5')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)

    if len(str(i)) == 19:
        # 打开xml文档
        dom = xml.dom.minidom.parse(os.path.join(path,i))
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
                cpc_scheme_dict.update(small_cpc_scheme_dict)

            ## 上级分类号1
            value = ''.join(list(small_cpc_scheme_dict.values()))
            if value == '5':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('5')]
            if value == '7':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('7')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)

            ## 上级分类号2
            if value == '7':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('7')]
            if value == '8':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('8')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)

            ## 上级分类号3
            if value == '8':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('8')]
            if value == '9':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('9')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)

            ## 上级分类号4
            if value == '9':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('9')]
            if value == '10':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('10')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
                print(dd)

            ## 上级分类号5
            if value == '10':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('10')]
            if value == '11':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('11')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号6
            if value == '11':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('11')]
            if value == '12':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('12')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号7
            if value == '12':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('12')]
            if value == '13':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('13')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号8
            if value == '13':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('13')]
            if value == '14':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('14')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号9
            if value == '14':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('14')]
            if value == '15':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('15')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号10
            if value == '15':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('15')]
            if value == '16':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('16')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号11
            if value == '16':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('16')]
            if value == '17':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('17')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号12
            if value == '17':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('17')]
            if value == '18':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('18')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)
            ## 上级分类号13
            if value == '18':
                super_key = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('18')]
            if value == '19':
                keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('19')]
                dd = {}
                dd[keyy] = super_key
                d.update(dd)


# print(d,'上级分类')
# print(cpc_scheme_dict,'读一：')

# # 2.打开txt文档解析 title_list
# title_dict = {}
# path_title_list = "./title_list/"
# file_title_list = os.listdir(path_title_list)  # 得到文件夹下所有文件名称
# len_file_title_list = len(file_title_list)
# m = 0
# while True:
#     m += 1
#     file = file_title_list.pop(0)
#     f = codecs.open(path_title_list+file, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
#     line = f.readline()  # 以行的形式进行读取文件
#     while True:
#         a = line.split()
#         if len(a) == 0:
#             break
#         cpc_title_list = a[0]
#         definition_en = a[1:]
#         definition_en = ' '.join(definition_en)
#         title_list_dict = {}
#         title_list_dict[cpc_title_list] = definition_en
#         title_dict.update(title_list_dict)
#         line = f.readline()
#     if m == len_file_title_list:
#         break
# f.close()
#
# # print(title_dict,'读二：')
#
# # # # 3.打开txt文档解析 validity_file
# validity_dict = {}
# file_validity_file = os.listdir(path_validity_file)  # 得到文件夹下所有文件名称
# file = file_validity_file[0]
# # # 打开txt文件
# f = codecs.open(path_validity_file+'/'+file, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
# line = f.readline()  # 以行的形式进行读取文件
# while True:
#     a = line.split()
#     if len(a) == 0:
#         break
#     cpc_symbol = a[0]
#     valid_from_data = a[1]
#     if '-' not in valid_from_data:
#         pass
#     else:
#         timeArray = time.strptime(valid_from_data,"%Y-%m-%d")
#         valid_from_data= bson.int64.Int64(int(time.mktime(timeArray)))
#     try:
#         valid_to_data = a[2]
#     except:
#         valid_to_data = ''
#     if len(valid_to_data) == 0:
#         pass
#     if '-' not in valid_to_data:
#         pass
#     else:
#         timeArray = time.strptime(valid_to_data, "%Y-%m-%d")
#         valid_to_data = bson.int64.Int64(int(time.mktime(timeArray)))
#     validity_file_dict_next = {}
#     validity_file_dict_next["valid_from_data"] = valid_from_data
#     validity_file_dict_next["valid_to_data"] = valid_to_data
#     validity_file_dict = {}
#     validity_dict[cpc_symbol] = validity_file_dict_next
#     validity_dict.update(validity_file_dict)
#     line = f.readline()
# f.close()
#
# # print(validity_dict,'读三：')
#
# scheme_title = {}
# for key in title_dict:
#     if cpc_scheme_dict.get(key):
#         scheme_title[key] = title_dict[key]
# # print('组合一：',scheme_title)
#
# scheme_validity = {}
# for keys in validity_dict:
#     if cpc_scheme_dict.get(keys):
#         scheme_validity[keys] = validity_dict[keys]
# # print('组合二：',scheme_validity)
#
# title_validity = {}
# for i in scheme_title:
#     if scheme_validity.get(i):
#         title_validity[i] = scheme_title[i]
# # print('组合三：',title_validity)
#
# super = {}
# for j in d:
#     if title_validity.get(j):
#         super[j] = d[j]
# # print('组合四',super)
#
# for cpc_no in title_validity:
#     leval = cpc_scheme_dict[cpc_no]
#     superior_cpc = d[cpc_no]
#     definition_en = title_dict[cpc_no]
#     valid_from_date = validity_dict[cpc_no]['valid_from_data']
#     valid_to_date = validity_dict[cpc_no]['valid_to_data']
#     def md5Encode(str):
#         m = hashlib.md5()  # 创建md5对象
#         m.update(str)  # 传入需要加密的字符串进行MD5加密
#         return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
#     esid = md5Encode(cpc_no.encode('utf-8'))  # 必须先进行转码，否则会报错
#     creat_time = bson.int64.Int64(int(time.time()))
#
#     all_dict = {}
#     all_dict["esid"] = esid
#     all_dict["cpc_no"] = cpc_no
#     all_dict["superior_cpc"] = superior_cpc
#     all_dict["leval"] = leval
#     all_dict["definition_en"] = definition_en
#     all_dict["creat_time"] = creat_time
#     all_dict["valid_from_date"] = valid_from_date
#     all_dict["valid_to_date"] = valid_to_date
#     # table.insert(all_dict)
#     print(esid,cpc_no,superior_cpc,leval,definition_en,creat_time,valid_from_date,valid_to_date)

end = datetime.datetime.now()
print(end-start)

""""
1 = {'CPC_Symbol':{"Valid_From_Date":'2012-01-01','Valid_To_Date':'2012-01-02'}}
2 = {}
3 ={}
data ={}
for 遍历这些字典的键。把值带上。对比之后加入新的字典中。
"""



