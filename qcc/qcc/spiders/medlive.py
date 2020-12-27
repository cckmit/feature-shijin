
import logging
import re
import sys
import time
import ast
import requests
import scrapy
from pyquery import PyQuery as pq
from qcc.spiders import const
from qcc.utils.es_utils import QueryType, Query
from qcc.utils import es_utils, common_utils, pdf_utils, qiniu_utils
from qcc.utils.date_utils import DateUtils
from qcc.utils.md5_utils import MD5Utils
from qcc.utils.mongo_utils import MongoUtils
from qcc.utils.qcc_utils import QCCUtils
from qcc.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings


'''
说明书：医脉通
1','地址获取：医脉通说明书链接可通过数字累加来获取抓取地址，不需要检索词
   网址：http://drugs.medlive.cn/drugref/html/6376.shtml 
2','初始化：将以上地址中的6376替换为1-50000抓取
3','日常新增：每天中午12：00在前一天最大数字上追加200
4','全量更新：每周日中午12：00抓取1-前一天最大数字

tips：
1.medlive_users 医脉通账号与密码
1.拷贝mongo集合 medlive_users 到线上
'''


def check_data(self, medlive_approval_num_list, medlive_import_approval_num_list, spider_url, qiniu_url, medlive_inn_name, medlive_drug_name_en, medlive_manufacturer, approval_num_set):
    is_complete_dict = update_drug_manual_medlive_url(self, medlive_approval_num_list, spider_url, qiniu_url, approval_num_set)
    is_complete_dict = update_drug_manual_medlive_url(self, medlive_import_approval_num_list, spider_url, qiniu_url, approval_num_set)
    for approval_num in is_complete_dict.keys():
        if not is_complete_dict[approval_num]:
            continue
        # 文号匹配不上的用【通用名称 medlive_inn_name+生产企业 medlive_manufacturer】
        # 或【英文名称 medlive_drug_name_en+生产企业 medlive_manufacturer】
        # 分别匹配上市库【药品名称(中文)(NMPA) spider_drug_name+生产企业(中文)(NMPA) spider_manufacture】
        # 或【药品名称(英文)(NMPA) spider_drug_name_en+生产企业(英文)(NMPA) spider_manufacture_en】
        if medlive_approval_num_list.count() > 0:
            queries = Query.queries(Query(QueryType.EQ, 'spider_drug_name', medlive_inn_name),
                                    Query(QueryType.EQ, 'spider_manufacture', medlive_manufacturer), )
            update_es_data(self, queries, spider_url, qiniu_url)
        else:
            queries = Query.queries(Query(QueryType.EQ, 'spider_drug_name_en', medlive_drug_name_en),
                                    Query(QueryType.EQ, 'spider_manufacture_en', medlive_manufacturer), )
            update_es_data(self, queries, spider_url, qiniu_url)


def read_es_data(self):
    approval_num_already_medlive_url_set = set()
    pages = self.es_utils.get_page('drug_ipo', queries=Query(QueryType.NE, 'drug_manual_medlive_url', None),show_fields=['approval_num'])
    if None != pages:
        for page in pages:
            approval_num_already_medlive_url_set.add(page['approval_num'])
    return approval_num_already_medlive_url_set


class MedliveSpider(scrapy.Spider):
    name = 'medlive'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']
    #限制： 自定义并发数和延迟时间
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'DOWNLOADER_MIDDLEWARES' : {
            'qcc.middlewares.QccDownloaderMiddleware': 543,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None, #关闭重定向（301，302）
           # 'qcc.middlewares.ProxyMiddleware': 543,  # 随机代理ip
            'qcc.middlewares.RetryMiddleware': 543,  # 自定义超过重试处理重试次数处理
        },
        'HTTPERROR_ALLOWED_CODES':[302, 301, 404, ]
    }

    def start_requests(self):
        login_status, jsessionid = login_medlive()
        if login_status:
            self.jsessionid = jsessionid
        else:
            logging.error(f'------- 医脉通登录失败，程序退出中 -------')
            sys.exit(1)
        self.pdf_utils = pdf_utils
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        self.md5_utils = MD5Utils()
        self.qcc_utils = QCCUtils()
        self.date_utils = DateUtils()
        self.qiniu_utils = qiniu_utils
        self.mongo_utils = MongoUtils()
        self.redis_server = from_settings(get_project_settings())
        self.approval_num_already_medlive_url_set = read_es_data(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu' in spider_url:
            #todo 待校验 链接字段在es中是否支持空检索
            approval_num_set = set()
            pages = es_utils.get_page(const.ESIndex.DRUG_IPO, queries=Query(QueryType.NE, 'drug_manual_medlive_url', None), page_index=-1, show_fields=['approval_num'])
            if None != pages:
                for page in pages:
                    approval_num_set.add(page['approval_num'])
            headers = const.headers
            headers['Cookie'] = self.jsessionid
            id_set = set()
            """
            mongo_data_list = self.mongo_utils.find_all(coll_name=const.MongoTables.MEDLIVE_DATA)
            for mongo_data in mongo_data_list:
                id_set.add(mongo_data['id'])
                url = mongo_data['url']
                qiniu_url = mongo_data['qiniu_url']
                medlive_inn_name = mongo_data['medlive_inn_name']
                medlive_drug_name_en = mongo_data['medlive_drug_name_en']
                medlive_manufacturer = mongo_data['medlive_manufacturer']
                medlive_approval_num_list = mongo_data['medlive_approval_num_list']
                medlive_import_approval_num_list = mongo_data['medlive_import_approval_num_list']
                check_data(self, medlive_approval_num_list, medlive_import_approval_num_list, url, qiniu_url, medlive_inn_name, medlive_drug_name_en, medlive_manufacturer, approval_num_set)
            """

            id = 20887
            url = f'http://drugs.medlive.cn/drugref/html/{id}.shtml'
            yield scrapy.Request(url, callback=self.parse, meta={'id': id}, headers=headers)

            """"
            for id in range(1, 50000):
                if id in id_set:
                    logging.info(f'当前数据已采集，被过滤：{id}')
                    continue
                logging.info(f'追加待采集的链接: {id}')
                url = f'http://drugs.medlive.cn/drugref/html/{id}.shtml'
                yield scrapy.Request(url, callback=self.parse, meta={'id': id}, headers=headers)
            """

        if 'medlive' in spider_url:
            id = meta['id']
            status = response.status
            if 404 == status:
                insert_no_results(self, id, spider_url)
                return
            if 301 == status or 302 == status:
                logging.error(f'------- 当前登录账号不可用，页面被过滤 {id} -------')
                return
            left_elements = pq(response.text)('.info-left')
            doc = pq(str(left_elements.html()))
            spider_content = ''
            title_elements = doc('.title')
            for title_element in title_elements.items():
                if not self.str_utils.is_blank(spider_content):
                    spider_content += '<br>'
                title = '<b>'+title_element.text()+'</b><br>'
                spider_content += title
                next_elements = title_element.next()
                if next_elements('.w110').size()>0:
                   for next_element in next_elements('.w110').items():
                       spider_content += '&nbsp;&nbsp;&nbsp;&nbsp;'+next_element.parent().text()+'<br>'
                   continue

                if '批准文号' in title or '生产企业' in title:
                    spider_content += '&nbsp;&nbsp;&nbsp;&nbsp;' + next_elements('.more-infomation').children().html() + '<br>'
                    continue
                if next_elements('img').size() == 0:
                    spider_content += '&nbsp;&nbsp;&nbsp;&nbsp;' + next_elements.text()+'<br>'
                else:
                    spider_content += '&nbsp;&nbsp;&nbsp;&nbsp;' + next_elements('.more-infomation').children().html() + '<br>'
            pdf_list = []
            pdf_dict = {}
            pdf_dict['html'] = spider_content
            pdf_name = self.md5_utils.get_md5(spider_content)+'.pdf'
            pdf_dict['pdf_name'] = const.STORE_PATH + pdf_name
            pdf_list.append(pdf_dict)
            self.pdf_utils.auto_html2pdf(pdf_list) #合并PDF
            qiniu_url = ''
            if self.pdf_utils.check_pdf(const.STORE_PATH + pdf_name):
                qiniu_url = self.qiniu_utils.up_qiniu(const.STORE_PATH + pdf_name, file_name=pdf_name, is_keep_file=False)

            base_info = {}
            medlive_approval_num_str = ''
            medlive_import_approval_num_str = ''
            medlive_approval_num_list = [] #批准文号
            medlive_import_approval_num_list = [] #进口药品注册证号
            title_elements = left_elements('.title')
            for title_element in title_elements.items():
                title = title_element.text()
                title = self.str_utils.remove_mark(title)
                value = title_element.next().text()
                if '药品名称' == title:
                    for split in self.str_utils.cn_mark2en_mark(str=value).split('\n'):
                        base_info[self.str_utils.get_brackets_str(str=split)[0]] = split[split.index(']')+1:].strip()

                if '适应症' == title:
                    base_info['适应症'] = title_element.next().text()

                if '批准文号' == title:
                    medlive_approval_num_str = value
                    medlive_approval_num_list = get_clean_approval_num(self, value)

                if '生产企业' == title:
                    value_elements = title_element.next()
                    value_elements.remove('table')
                    base_info['生产企业'] = value_elements.text()

                if '进口药品注册证号' == title:
                    medlive_import_approval_num_str = value
                    medlive_import_approval_num_list = get_clean_approval_num(self, value)

            medlive_inn_name = base_info.get('通用名称', None)
            medlive_drug_name_en = base_info.get('英文名称', None)
            medlive_manufacturer = base_info.get('生产企业', None)
            spider_proprietary_name = base_info.get('商品名称', None)
            indication = base_info.get('适应症', None)

            # 批准文号、历史批准文号(只会走一个)
            check_data(self, medlive_approval_num_list, medlive_import_approval_num_list, spider_url, qiniu_url, medlive_inn_name, medlive_drug_name_en, medlive_manufacturer, None)
            insert_mongo_data(self, medlive_inn_name, medlive_drug_name_en, id, spider_url, qiniu_url,medlive_approval_num_list, indication,
                              medlive_approval_num_str, medlive_import_approval_num_str, medlive_import_approval_num_list, medlive_manufacturer, spider_proprietary_name)


def insert_no_results(self, id, spider_url):
    logging.info(f'当前页面采集成功，但页面无数据，被过滤：{id}')
    mongo_dict = {}
    mongo_dict['id'] = id
    mongo_dict['url'] = spider_url
    mongo_dict['status'] = 404
    mongo_dict['spider_wormtime'] = self.date_utils.get_timestamp()
    logging.info(f'------- insert mongo data ------- {id}')
    self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.MEDLIVE_DATA)


def update_es_data(self, queries, spider_url, qiniu_url):
    pages = self.es_utils.get_page(const.ESIndex.DRUG_IPO, queries=queries)
    if None != pages:
        for page in pages:
            if 'pharmcube' not in qiniu_url:
                logging.info(f'当前批准文号对应的说明书上传到七牛云有问题，被过滤：{spider_url}')
                continue
            esid = page['esid']
            es_dict = {}
            es_dict['esid'] = esid
            es_dict['drug_manual_medlive_url'] = qiniu_url
            logging.info(f'------- 更新 {const.ESIndex.DRUG_IPO} 药品说明书链接 -------{esid}')
            self.es_utils.update(const.ESIndex.DRUG_IPO, d=es_dict)
            return False


def update_drug_manual_medlive_url(self, approval_num_list, spider_url, qiniu_url, approval_num_set):
    is_complete_dict = {}
    field_list = ['approval_num', 'original_approval_num']
    for field in field_list:
        for approval_num in approval_num_list:
            if approval_num in self.approval_num_already_medlive_url_set:
                logging.info(f'当前批准文号说明书在ES中已存在，被过滤：{approval_num}')
                is_complete_dict[approval_num] = False
                continue
            if None != approval_num_set:
                if approval_num in approval_num_set:
                    logging.info(f'当前批准文号已经匹配上说明书链接，被过滤：{approval_num}')
                    is_complete_dict[approval_num] = False
                    continue
            if len(self.str_utils.get_cn(str=approval_num))>0 and '国药准字' not in approval_num:
                logging.info(f'当前批准文号视为异常情况，被过滤: {approval_num}')
                continue
            if approval_num in is_complete_dict and is_complete_dict[approval_num] == False:
                continue
            is_append = True
            queries = Query(QueryType.EQ, field, approval_num)
            is_append = update_es_data(self, queries, spider_url, qiniu_url)
            if approval_num in is_complete_dict and is_complete_dict[approval_num] == False:
                continue
            else:
                is_complete_dict[approval_num] = is_append
    return is_complete_dict


def insert_mongo_data(self, medlive_inn_name, medlive_drug_name_en, id, spider_url, qiniu_url,
                      medlive_approval_num_list, indication, medlive_approval_num_str, medlive_import_approval_num_str,
                      medlive_import_approval_num_list, medlive_manufacturer, spider_proprietary_name):
    mongo_dict = {}
    mongo_dict['id'] = id
    mongo_dict['url'] = spider_url
    mongo_dict['qiniu_url'] = qiniu_url
    mongo_dict['medlive_inn_name'] = medlive_inn_name
    mongo_dict['medlive_drug_name_en'] = medlive_drug_name_en
    mongo_dict['medlive_manufacturer'] = medlive_manufacturer
    mongo_dict['spider_proprietary_name'] = spider_proprietary_name
    mongo_dict['indication'] = indication
    mongo_dict['medlive_approval_num_list'] = medlive_approval_num_list
    mongo_dict['medlive_approval_num_str'] = medlive_approval_num_str
    mongo_dict['medlive_import_approval_num_str'] = medlive_import_approval_num_str
    mongo_dict['medlive_import_approval_num_list'] = medlive_import_approval_num_list
    mongo_dict['spider_wormtime'] = self.date_utils.get_timestamp()
    logging.info(f'------- insert mongo data -------{medlive_inn_name} {str(id)}')
    self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.MEDLIVE_DATA)


def get_clean_approval_num(self, value):
    approval_num_list = []
    value = value.replace(' ', '')
    replace_list = ['国药准宇', '国准字号', '国家准字', '药准字', '国药准', '国药住在你', '国药准字号', '国药淮字', '围药准字', '国药谁字', '国准字', '国药准号', '国标准字']
    for split in self.str_utils.split_mark(str=value):
        medlive_approval_num = self.str_utils.remove_mark(str=split)  # 批准文号
        str = self.str_utils.get_cn(str=medlive_approval_num)
        if str in replace_list:
            medlive_approval_num = medlive_approval_num.replace(str, '国药准字')
        if len(medlive_approval_num) <6 or '每盒' in medlive_approval_num:
            continue
        results = re.findall(r'[0-9]{1,3}[A-Za-z]+', medlive_approval_num)
        for result in results:
            medlive_approval_num = medlive_approval_num.replace(result, '')
        approval_num_list.append(medlive_approval_num.strip().upper())
    return approval_num_list

def login_medlive():
    #username = '18656557851'
    #password = 'zxx123456'

    username = '526090727@qq.com'
    password = '526090727'

    headers = const.headers
    headers['Referer'] = 'http://drugs.medlive.cn/'
    session = requests.Session()
    login_url = 'https://www.medlive.cn/auth/login?service=http%3A%2F%2Fdrugs.medlive.cn%2F'
    time.sleep(0.26 * common_utils.random_int(1, 6))
    res = session.get(url=login_url, headers=headers)
    login_doc = pq(res.text)
    login_form = login_doc('#login_form')
    name_dict = {}
    for input_element in login_form('input').items():
        name = input_element.attr('name')
        value = input_element.attr('value')
        name_dict[name] = value
    lt = name_dict['lt']
    execution = name_dict['execution']
    data = {'loginType': 'password', '_eventId': 'submit', 'username': username, 'password': password, 'rememberMe': True, 'lt': lt, 'execution': execution, }
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    login_url = 'https://www.medlive.cn' + login_form('form').attr('action')
    time.sleep(0.26 * common_utils.random_int(2, 6))
    session.post(url=login_url, data=data, headers=headers)
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Referer'] = 'http://drugs.medlive.cn/'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    time.sleep(0.26 * common_utils.random_int(2, 6))
    check_url = 'http://drugs.medlive.cn/drugref/getUserInfoAjax.do'
    res = session.post(url=check_url, headers=headers)
    if True == ast.literal_eval(res.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))['success']:
        use_cookie = ''
        for cookie in str(session.cookies).split('>, <'):
            if 'JSESSIONID' in cookie and '/auth' not in cookie: #cookie 名称相同值被覆盖了
                use_cookie = cookie[cookie.index('JSESSIONID'):cookie.index(' for')]
        logging.info(f'当前账号： 登录成功！{username}')
        return True, use_cookie
        # 将cookies 转换为字典形式
        #return True, requests.utils.dict_from_cookiejar(session.cookies)['JSESSIONID']
    else:
       return False, None