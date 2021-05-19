import scrapy
from openpyxl import load_workbook
from openpyxl import Workbook
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils import file_utils
from flash_news import const

mongo_utils = MongoUtils()

# workbook = load_workbook(filename=r'D:/download/academic_stu.xlsx')
# sheet = workbook.active
# n = 0

class Doctor(scrapy.Spider):
    name = 'mongodb_excel'
    n = 0
    mongo_list = mongo_utils.find_all(coll_name=const.MongoTables.MEET)
    mongo_ll = []
    for mongo_data in mongo_list:
        del mongo_data['_id']
        mongo_ll.append(mongo_data)
        n += 1
    file_utils.write_xls(r'D:/download/','meeting_new.xlsx',mongo_ll)


    name = 'mongodb_excel'

#     mongo_list = mongo_utils.find_all(coll_name=const.MongoTables.BAIDU_STU)
#
#     for mongo_data in mongo_list:
#         # print(mongo_data)
#         del mongo_data['_id']
#         n += 1
#         data_id = mongo_data["data_id"]
#         cooperative_scholar_number = mongo_data["cooperative_scholar_number"]
#         cooperative_schola_scholarID = mongo_data["cooperative_schola_scholarID"]
#         cooperative_scholar_name = mongo_data["cooperative_scholar_name"]
#         cooperative_scholar_hospital = mongo_data["cooperative_scholar_hospital"]
#         # H_index = mongo_data["H_index"]
#         # G_index = mongo_data["G_index"]
#         # field = mongo_data["field"]
#         # periodical = mongo_data["periodical"]
#         # conference = mongo_data["conference"]
#         # monograph = mongo_data["monograph"]
#         # other = mongo_data["other"]
#         # cooperative_institution1 = mongo_data["cooperative_institution1"]
#         # cooperative_number1 = mongo_data["cooperative_number1"]
#         # cooperative_institution2 = mongo_data["cooperative_institution2"]
#         # cooperative_number2 = mongo_data["cooperative_number2"]
#         # cooperative_institution3 = mongo_data["cooperative_institution3"]
#         # cooperative_number3 = mongo_data["cooperative_number3"]
#         # cooperative_institution4 = mongo_data["cooperative_institution4"]
#         # cooperative_number4 = mongo_data["cooperative_number4"]
#         # cooperative_institution5 = mongo_data["cooperative_institution5"]
#         # cooperative_number5 = mongo_data["cooperative_number5"]
#         # cooperative_institution6 = mongo_data["cooperative_institution6"]
#         # cooperative_number6 = mongo_data["cooperative_number6"]
#         # cooperative_institution7 = mongo_data["cooperative_institution7"]
#         # cooperative_number7 = mongo_data["cooperative_number7"]
#         # cooperative_institution8 = mongo_data["cooperative_institution8"]
#         # cooperative_number8 = mongo_data["cooperative_number8"]
#         # cooperative_institution9 = mongo_data["cooperative_institution9"]
#         # cooperative_number9 = mongo_data["cooperative_number9"]
#         # cooperative_institution10 = mongo_data["cooperative_institution10"]
#         # cooperative_number10 = mongo_data["cooperative_number10"]
#         # data_id = mongo_data["data_id"]
#         str1 = 'A' + str(n)
#         str2 = 'B' + str(n)
#         str3 = 'C' + str(n)
#         str4 = 'D' + str(n)
#         str5 = 'E' + str(n)
#         # str6 = 'F' + str(n)
#         # str7 = 'G' + str(n)
#         # str8 = 'H' + str(n)
#         # str9 = 'I' + str(n)
#         # str10 = 'J' + str(n)
#         # str11 = 'K' + str(n)
#         # str12 = 'L' + str(n)
#         # str13 = 'M' + str(n)
#         # str14 = 'N' + str(n)
#         # str15 = 'O' + str(n)
#         # str16 = 'P' + str(n)
#         # str17 = 'Q' + str(n)
#         # str18 = 'R' + str(n)
#         # str19 = 'S' + str(n)
#         # str20 = 'T' + str(n)
#         # str21 = 'U' + str(n)
#         # str22 = 'V' + str(n)
#         # str23 = 'W' + str(n)
#         # str24 = 'X' + str(n)
#         # str25 = 'Y' + str(n)
#         # str26 = 'Z' + str(n)
#         # str27 = 'AA' + str(n)
#         # str28 = 'AB' + str(n)
#         # str29 = 'AC' + str(n)
#         # str30 = 'AD' + str(n)
#         # str31 = 'AE' + str(n)
#         # str32 = 'AF' + str(n)
#         # str33 = 'AG' + str(n)
#         sheet[str1].value = data_id
#         sheet[str2].value = cooperative_scholar_number
#         sheet[str3].value = cooperative_schola_scholarID
#         sheet[str4].value = cooperative_scholar_name
#         sheet[str5].value = cooperative_scholar_hospital
#         # sheet[str6].value = H_index
#         # sheet[str7].value = G_index
#         # sheet[str8].value = field
#         # sheet[str9].value = periodical
#         # sheet[str10].value = conference
#         # sheet[str11].value = monograph
#         # sheet[str12].value = other
#         # sheet[str13].value = cooperative_institution1
#         # sheet[str14].value = cooperative_number1
#         # sheet[str15].value = cooperative_institution2
#         # sheet[str16].value = cooperative_number2
#         # sheet[str17].value = cooperative_institution3
#         # sheet[str18].value = cooperative_number3
#         # sheet[str19].value = cooperative_institution4
#         # sheet[str20].value = cooperative_number4
#         # sheet[str21].value = cooperative_institution5
#         # sheet[str22].value = cooperative_number5
#         # sheet[str23].value = cooperative_institution6
#         # sheet[str24].value = cooperative_number6
#         # sheet[str25].value = cooperative_institution7
#         # sheet[str26].value = cooperative_number7
#         # sheet[str27].value = cooperative_institution8
#         # sheet[str28].value = cooperative_number8
#         # sheet[str29].value = cooperative_institution9
#         # sheet[str30].value = cooperative_number9
#         # sheet[str31].value = cooperative_institution10
#         # sheet[str32].value = cooperative_number10
#         # sheet[str33].value = data_id
#
#         print(n)
#
# workbook.save(filename=r'D:/download/academic_stu.xlsx')
