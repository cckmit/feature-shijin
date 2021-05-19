import pymongo
import requests
import json
import xlrd
# # 连接mongodb数据库
client = pymongo.MongoClient('localhost', 27017)
mdb = client['spider_py']
cooperation = mdb['wangfang_cooperation']
periodica = mdb['wangfang_periodical']
theme = mdb['wangfang_theme']


# 打开文件
data = xlrd.open_workbook("D:\software\百度下载\work\万方ID.xlsx")
# 查看工作表
data.sheet_names()
# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('Sheet1')
scholarID_list = table.col_values(0)
for scholarID in scholarID_list:
    ## 合作分析
    cooperation_url = "http://analytics.med.wanfangdata.com.cn/Author/RelationChartData"
    headers = {
        "Cookie": "Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1617673219,1617698806,1617760225; WFMed.Auth.IsAutoLogin=; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%2c%7b%22Key%22%3a%22CMAUID%22%2c%22Value%22%3a%22BUFOU8kjjd9Utd8BnPlryg%3d%3d%22%7d%5d%2c%22SessionId%22%3a%22ccbcc5eb-dbb7-4a48-965c-0c0c9932b802%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-08T02%3a46%3a50Z%22%2c%22TicketSign%22%3a%2207HFW7aFLU5%5c%2fzRbUYXA%5c%2fpQ%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1617850010"}
    data = {"StartYear": "2012",
            "EndYear": "2021",
            "Id": scholarID, }
    ip_str = requests.post(url="http://60.205.151.191:80/es_online/get_dynamic_ip", ).text
    print(ip_str)
    res = requests.post(url=cooperation_url,headers=headers,data=data,proxies={"http":ip_str}).text
    ress = json.loads(res)
    # import random
    # random = random.randint(1, 2)
    # time.sleep(random)
    listdata = ress['list']
    for i in listdata:
        # 合作者
        cooperative_scholar_name = i['AuthorName']
        # 合作者ID
        AuthorId = i['AuthorId']
        # 合作者单位
        cooperative_scholar_hospital = i['OrgName']
        # 合作发文数
        cooperative_published_num = i['Count']

        print(cooperative_scholar_name, AuthorId, cooperative_scholar_hospital, cooperative_published_num)
        cooperation_dict = {}
        cooperation_dict['scholarID'] = scholarID
        cooperation_dict['AuthorName'] = cooperative_scholar_name
        cooperation_dict['AuthorId'] = AuthorId
        cooperation_dict['OrgName'] = cooperative_scholar_hospital
        cooperation_dict['Count'] = cooperative_published_num
        cooperation.insert(cooperation_dict)

    ## 主题分析
    theme_url = "http://analytics.med.wanfangdata.com.cn/Author/KeywordsChartData"
    headers = {
        "Cookie":"WFMed.Auth.IsAutoLogin=; Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1618211341,1618451904,1618575452,1619319239; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%22eca70707-1512-4ac6-982a-b7bfbb54dd60%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-25T05%3a33%3a09Z%22%2c%22TicketSign%22%3a%22861CMDSVp7xEWxkFLfttgw%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619328785"
    }
    data={"StartYear": "2012",
        "EndYear": "2021",
        "Id": scholarID,
        "IETag":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
    ip_str = requests.post(url="http://60.205.151.191:80/es_online/get_dynamic_ip", ).text
    print(ip_str)
    res = requests.post(url=theme_url, headers=headers,data=data,proxies={"http":ip_str}).text
    # import random
    # random = random.randint(1,2)
    # time.sleep(random)
    ress = json.loads(res)
    for i in ress['ListData']:
        # 关键词
        topic_keyword = i['name']
        # 词频数
        word_count = i['count']
        print(topic_keyword,word_count)
        theme_dict = {}
        theme_dict['scholarID'] = scholarID
        theme_dict['name'] = topic_keyword
        theme_dict['count'] = word_count
        theme.insert(theme_dict)

    ## 期刊分析
    periodical_url = "http://analytics.med.wanfangdata.com.cn/Author/PeriodicalChartData"
    headers = {
        "Cookie":"WFMed.Auth.IsAutoLogin=; Hm_lvt_af200f4e2bd61323503aebc2689d62cb=1618211341,1618451904,1618575452,1619319239; WFMed.Auth=%7b%22Context%22%3a%7b%22AccountIds%22%3a%5b%22MedPerson.yudi0515%22%5d%2c%22Data%22%3a%5b%7b%22Key%22%3a%22MedPerson.yudi0515.DisplayName%22%2c%22Value%22%3a%22%22%7d%5d%2c%22SessionId%22%3a%22eca70707-1512-4ac6-982a-b7bfbb54dd60%22%2c%22Sign%22%3a%22kHNAparyYhsEpMB%5c%2fya3iEbOCwyhEvWs6DjxcloviI58GsKTTzZg5sjekCyVvp1u7%22%7d%2c%22LastUpdate%22%3a%222021-04-25T05%3a34%3a48Z%22%2c%22TicketSign%22%3a%223y0%5c%2f%2bK3UUkctBuTMT84wYw%3d%3d%22%7d; Hm_lpvt_af200f4e2bd61323503aebc2689d62cb=1619328888"
    }
    data = {"StartYear": "2012",
           "EndYear": "2021",
           "Id": scholarID, }
    # import random
    # random = random.randint(1, 2)
    # time.sleep(random)
    ip_str = requests.post(url="http://60.205.151.191:80/es_online/get_dynamic_ip", ).text
    print(ip_str)
    res = requests.post(url=periodical_url, headers=headers,data=data,proxies={"http":ip_str}).text
    ress = json.loads(res)
    listdata = ress['list']
    for i in listdata:
        # 期刊名称
        journal_name = i['PeriodicalName']
        # 影响因子
        impact_factor = i['ImpactFactor']
        # 总发文数
        published_num = i['ArticleCount']
        # 第一作者
        first_author_paper_num = i['FirstArticleCount']
        print(journal_name, impact_factor, published_num, first_author_paper_num)

        periodical_dict = {}
        periodical_dict['scholarID'] = scholarID
        periodical_dict['PeriodicalName'] = journal_name
        periodical_dict['ImpactFactor'] = impact_factor
        periodical_dict['ArticleCount'] = published_num
        periodical_dict['FirstArticleCount'] = first_author_paper_num
        # logging.info(f'------- @@@insert mongo data ------- {scholarID}')
        periodica.insert(periodical_dict)

