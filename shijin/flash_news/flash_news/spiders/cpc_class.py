import scrapy
import os.path
import codecs
import hashlib
import time
import xml.dom.minidom
import pymongo
import datetime
import bson
import zipfile
from flash_news.utils import es_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news.utils.file_utils import DownloadFile
from flash_news.utils.send_email_utils import SendEmail
from flash_news import const
from flash_news.const import ESIndex
from flash_news.utils.es_utils import Query, QueryType
from flash_news.utils.date_utils import DateUtils

'''
tapd网址：https://www.tapd.cn/55638340/prong/stories/view/1155638340001002764
'''
class Cpc_ClassSpider(scrapy.Spider):
    name = 'cpc_class'
    # allowed_domains = ['wit_finance.com']
    # start_urls = ['http://wit_finance.com/']
    handle_httpstatus_list = [404]
    def start_requests(self):
        self.es_utils = es_utils
        self.file_utils = DownloadFile()
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        self.sendemail = SendEmail()
        url = "https://www.cooperativepatentclassification.org/cpcSchemeAndDefinitions/bulk"
        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        # file_list = []
        # file_dict = {}
        # file2_dict = {}
        # file3_dict = {}
        # file_dict.setdefault("file_name", 'VALIDITY_FILE.zip')
        # file_dict.setdefault("file_url", "https://www.cooperativepatentclassification.org" + ''.join(response.xpath('//*[@id="body"]/p[4]/a/@href').extract()))
        # file2_dict.setdefault("file_name", 'TITLE_LIST.zip')
        # file2_dict.setdefault("file_url", "https://www.cooperativepatentclassification.org" + ''.join(response.xpath('//*[@id="body"]/p[5]/a/@href').extract()))
        # file3_dict.setdefault("file_name", 'SCHEME_XML.zip')
        # file3_dict.setdefault("file_url", "https://www.cooperativepatentclassification.org" + ''.join(response.xpath('//*[@id="body"]/p[8]/a/@href').extract()))
        # file_list.append(file_dict)
        # file_list.append(file2_dict)
        # file_list.append(file3_dict)
        # print(file_list)
        # self.file_utils.download_file(file_list)

        # # 连接mongodb数据库
        client = pymongo.MongoClient('localhost', 27017)
        mdb = client['spider_py']
        table = mdb['classification_cpc']

        start = datetime.datetime.now()

        parent_path = (r'../spiders/')  # 父文件夹路径
        for root, dirs, files in os.walk(parent_path):
            if 'CPC' in root and '\Doc' not in root:
                path_validity_file = root
        #     # 读取文件名  这里在解压缩
        #     for name in files:
        #         if 'SCHEME_XML' in name:
        #             name = 'SCHEME_XML.zip'
        #             extracting = zipfile.ZipFile(name)
        #             extracting.extractall("scheme_xml")
        #             extracting.close()
        #
        #         if 'TITLE_LIST' in name:
        #             name = 'TITLE_LIST.zip'
        #             extracting2 = zipfile.ZipFile(name)
        #             # print(extracting2)
        #             extracting2.extractall("title_list")
        #             extracting2.close()
        #
        #         if 'VALIDITY_FILE' in name:
        #             name = 'VALIDITY_FILE.zip'
        #             extracting3 = zipfile.ZipFile(name)
        #             # print(extracting3)
        #             extracting3.extractall("validity_file")
        #             extracting3.close()

        ## 打开xml文档的解析 scheme_xml
        # cpc_scheme_dict = {}
        # d = {}
        # path = "./scheme_xml/"
        # files = os.listdir(path)  # 得到文件夹下所有文件名称
        # for i in files:
        #     if len(str(i)) == 16:
        #         # 打开xml文档
        #         dom = xml.dom.minidom.parse(os.path.join(path, i))
        #         # 得到文档元素对象
        #         root = dom.documentElement
        #         itemlist = root.getElementsByTagName('classification-item')
        #         for i in range(len(itemlist)):
        #             item = itemlist[i]
        #             level = item.getAttribute("level")
        #             big_cpc_scheme = item.getAttribute("sort-key")
        #             big_cpc_scheme_dict = {}
        #             big_cpc_scheme_dict[big_cpc_scheme] = level
        #             if int(big_cpc_scheme_dict[big_cpc_scheme]) == 3:
        #                 continue
        #             else:
        #                 # print('第一：',big_cpc_scheme_dict)
        #                 cpc_scheme_dict.update(big_cpc_scheme_dict)
        #
        #             value = ''.join(list(big_cpc_scheme_dict.values()))
        #             if value == '2':
        #                 super_key2 = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('2')]
        #             if value == '4':
        #                 keyy = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('4')]
        #                 dd = {}
        #                 dd[keyy] = super_key2
        #                 d.update(dd)
        #
        #             if value == '4':
        #                 super_key4 = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('4')]
        #             if value == '5':
        #                 keyy = list(big_cpc_scheme_dict.keys())[list(big_cpc_scheme_dict.values()).index('5')]
        #                 dd = {}
        #                 dd[keyy] = super_key4
        #                 d.update(dd)
        #
        #     if len(str(i)) == 19:
        #         # 打开xml文档
        #         dom = xml.dom.minidom.parse(os.path.join(path, i))
        #         # 得到文档元素对象
        #         root = dom.documentElement
        #         itemlist = root.getElementsByTagName('classification-item')
        #         for i in range(len(itemlist)):
        #             item = itemlist[i]
        #             level = item.getAttribute("level")
        #             small_cpc_scheme = item.getAttribute("sort-key")
        #             small_cpc_scheme_dict = {}
        #             small_cpc_scheme_dict[small_cpc_scheme] = level
        #             if int(small_cpc_scheme_dict[small_cpc_scheme]) == 6:
        #                 continue
        #             else:
        #                 # print('第二：',small_cpc_scheme_dict)
        #                 cpc_scheme_dict.update(small_cpc_scheme_dict)
        #             ## 上级分类号1
        #             value = ''.join(list(small_cpc_scheme_dict.values()))
        #             if value == '5':
        #                 super_key5 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('5')]
        #             if value == '7':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('7')]
        #                 dd = {}
        #                 dd[keyy] = super_key5
        #                 d.update(dd)
        #             ## 上级分类号2
        #             if value == '7':
        #                 super_key7 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('7')]
        #             if value == '8':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('8')]
        #                 dd = {}
        #                 dd[keyy] = super_key7
        #                 # print(dd)
        #                 d.update(dd)
        #             ## 上级分类号3
        #             if value == '8':
        #                 super_key8 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('8')]
        #             if value == '9':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('9')]
        #                 dd = {}
        #                 dd[keyy] = super_key8
        #                 # print(dd)
        #                 d.update(dd)
        #             ## 上级分类号4
        #             if value == '9':
        #                 super_key9 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('9')]
        #             if value == '10':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('10')]
        #                 dd = {}
        #                 dd[keyy] = super_key9
        #                 # print(dd)
        #                 d.update(dd)
        #             ## 上级分类号5
        #             if value == '10':
        #                 super_key10 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('10')]
        #             if value == '11':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('11')]
        #                 dd = {}
        #                 dd[keyy] = super_key10
        #                 d.update(dd)
        #             ## 上级分类号6
        #             if value == '11':
        #                 super_key11 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('11')]
        #             if value == '12':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('12')]
        #                 dd = {}
        #                 dd[keyy] = super_key11
        #                 d.update(dd)
        #             ## 上级分类号7
        #             if value == '12':
        #                 super_key12 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('12')]
        #             if value == '13':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('13')]
        #                 dd = {}
        #                 dd[keyy] = super_key12
        #                 d.update(dd)
        #             ## 上级分类号8
        #             if value == '13':
        #                 super_key13 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('13')]
        #             if value == '14':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('14')]
        #                 dd = {}
        #                 dd[keyy] = super_key13
        #                 d.update(dd)
        #             ## 上级分类号9
        #             if value == '14':
        #                 super_key14 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('14')]
        #             if value == '15':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('15')]
        #                 dd = {}
        #                 dd[keyy] = super_key14
        #                 d.update(dd)
        #             ## 上级分类号10
        #             if value == '15':
        #                 super_key15 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('15')]
        #             if value == '16':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('16')]
        #                 dd = {}
        #                 dd[keyy] = super_key15
        #                 d.update(dd)
        #             ## 上级分类号11
        #             if value == '16':
        #                 super_key16 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('16')]
        #             if value == '17':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('17')]
        #                 dd = {}
        #                 dd[keyy] = super_key16
        #                 d.update(dd)
        #             ## 上级分类号12
        #             if value == '17':
        #                 super_key17 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('17')]
        #             if value == '18':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('18')]
        #                 dd = {}
        #                 dd[keyy] = super_key17
        #                 d.update(dd)
        #             ## 上级分类号13
        #             if value == '18':
        #                 super_key18 = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('18')]
        #             if value == '19':
        #                 keyy = list(small_cpc_scheme_dict.keys())[list(small_cpc_scheme_dict.values()).index('19')]
        #                 dd = {}
        #                 dd[keyy] = super_key18
        #                 d.update(dd)
        #
        # # print('读一：', cpc_scheme_dict)
        #
        # # # 2.打开txt文档解析 title_list
        # title_dict = {}
        # path_title_list = "./title_list/"
        # file_title_list = os.listdir(path_title_list)  # 得到文件夹下所有文件名称
        # len_file_title_list = len(file_title_list)
        # m = 0
        # while True:
        #     m += 1
        #     file = file_title_list.pop(0)
        #     f = codecs.open(path_title_list + file, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
        #     line = f.readline()  # 以行的形式进行读取文件
        #     while True:
        #         a = line.split()
        #         if len(a) == 0:
        #             break
        #         number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ]
        #         if a[1] in number_list:
        #             a.remove(a[1])
        #         else:
        #             pass
        #         cpc_title_list = a[0]
        #         definition_en = a[1:]
        #         definition_en = ' '.join(definition_en)
        #         title_list_dict = {}
        #         title_list_dict[cpc_title_list] = definition_en
        #         # print('第三：',title_list_dict)
        #         title_dict.update(title_list_dict)
        #         line = f.readline()
        #     if m == len_file_title_list:
        #         break
        # f.close()
        #
        # # print('读二：', title_dict)
        #
        # # # # 3.打开txt文档解析 validity_file
        # validity_dict = {}
        # file_validity_file = os.listdir(path_validity_file)  # 得到文件夹下所有文件名称
        # # print(path_validity_file)
        # file = file_validity_file[0]
        # # # 打开txt文件
        # # f = codecs.open('./validity_file/CPCValidityFile202102/CPCValidityFile202102.txt', mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
        # f = codecs.open(path_validity_file+'/'+file, mode='r', encoding='utf-8')  # 打开txt文件，以‘utf-8'编码读取
        # line = f.readline()  # 以行的形式进行读取文件p
        # # print(line)
        # while True:
        #     a = line.split()
        #     if len(a) == 0:
        #         break
        #     cpc_symbol = a[0]
        #     valid_from_data = a[1]
        #     if '-' not in valid_from_data:
        #         pass
        #     else:
        #         timeArray = time.strptime(valid_from_data, "%Y-%m-%d")
        #         valid_from_data = bson.int64.Int64(int(time.mktime(timeArray)))
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
        #     validity_file_dict[cpc_symbol] = validity_file_dict_next
        #     validity_dict.update(validity_file_dict)
        #     line = f.readline()
        # f.close()
        #
        # # print('读三：', validity_dict)
        #
        # scheme_title = {}
        # for key in title_dict:
        #     # print(key)
        #     if cpc_scheme_dict.get(key):
        #         scheme_title[key] = title_dict[key]
        # # print('组合一：', scheme_title)
        #
        # scheme_validity = {}
        # for keys in validity_dict:
        #     if cpc_scheme_dict.get(keys):
        #         scheme_validity[keys] = validity_dict[keys]
        # # print('组合二：', scheme_validity)
        #
        # title_validity = {}
        # for i in scheme_title:
        #     if scheme_validity.get(i):
        #         title_validity[i] = scheme_title[i]
        # # print('组合三：', title_validity)
        #
        # super = {}
        # for j in d:
        #     if title_validity.get(j):
        #         super[j] = d[j]
        # # print('组合四',super)
        #
        # for cpc_no in title_validity:
        #     level = cpc_scheme_dict[cpc_no]
        #     superior_cpc = d[cpc_no]
        #     definition_en = title_dict[cpc_no]
        #     valid_from_date = validity_dict[cpc_no]['valid_from_data']
        #     valid_to_date = validity_dict[cpc_no]['valid_to_data']
        #     if valid_to_date != '':
        #         valid_to_date = int(valid_to_date) * 1000
        #     esid = self.md5_utils.get_md5(cpc_no)
        #     creat_time = bson.int64.Int64(int(time.time()) * 1000)
        #     read_es_cpc = self.es_utils.get_page(ESIndex.CLASSIFICATION_CPC,queries=Query(QueryType.EQ,'cpc_no',cpc_no),page_size=-1,show_fields=['definition_en','status'])
        #     if None != read_es_cpc:
        #         for cpc in read_es_cpc:
        #             en_interpretation = cpc['definition_en']
        #             en_esid = cpc['esid']
        #             # re_status = cpc['status']
        #             # if re_status == "正常":
        #             #     break
        #             if en_interpretation != definition_en:
        #                 update_es_dict = {}
        #                 update_es_dict['esid'] = en_esid
        #                 update_es_dict['status'] = '变更'
        #                 update_es_dict["spider_wormtime"] = int(time.time()) * 1000
        #                 update_es_dict['definition_en'] = definition_en
        #                 self.es_utils.update(index=ESIndex.CLASSIFICATION_CPC, d=update_es_dict)
        #             read_status = cpc['status']
        #             if read_status == "变更" and en_interpretation == definition_en:
        #                 update_es_dict2 = {}
        #                 update_es_dict2['esid'] = en_esid
        #                 update_es_dict2['status'] = '正常'
        #                 update_es_dict2["spider_wormtime"] = int(time.time()) * 1000
        #                 self.es_utils.update(index=ESIndex.CLASSIFICATION_CPC, d=update_es_dict2)
        #
        #     if None == read_es_cpc:
        #         all_dict = {}
        #         all_dict["esid"] = esid
        #         all_dict["cpc_no"] = cpc_no
        #         all_dict["superior_cpc"] = superior_cpc
        #         all_dict["level"] = level
        #         all_dict["creat_time"] = creat_time
        #         all_dict["valid_from_date"] = int(valid_from_date) * 1000
        #         all_dict["definition_en"] = definition_en
        #         all_dict["status"] = '新增'
        #         print(all_dict)
                all_dict = {'esid': '6fc7d388f02773f203e8bf64db9d3824', 'cpc_no': 'A61M1/067', 'superior_cpc': 'A61M1/062', 'level': 10, 'creat_time': 1620712825000, 'valid_from_date': 1619798400000, 'definition_en': '{with means for hands-free operation}', 'status': '新增'}
                self.es_utils.insert_or_replace(index=ESIndex.CLASSIFICATION_CPC, d=all_dict)

                # self.mongo_utils.insert_one(mongo_data=all_dict, coll_name=const.MongoTables.CPC)

        #     """
        #     入es数据库
        #
        #     如果新增分类号对比数据库，没有。all_dict["status"] = '新增'
        #
        #     新增分类号对比数据库，有。对比 definition_en 字段，如果不相等，用新的英文释义（其他字段也用新的）。all_dict["status"] = '变更'。
        #     """

        # end = datetime.datetime.now()
        # print(end - start)













