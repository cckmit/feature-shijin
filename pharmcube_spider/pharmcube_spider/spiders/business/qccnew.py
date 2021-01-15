import json
import logging
import re
import ast
import scrapy
from pharmcube_spider.const import ESIndex, QCCAPI, RedisKey
from pharmcube_spider.utils import es_utils
from pharmcube_spider.utils.common_utils import set_default
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.qcc_utils import QCCUtils
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings


# 企查查登录账号、密码：https://openapi.qcc.com/data?source=websiteHeader
# 企查查充值账号：13810111909  密码：19aa319c
#  请求参数

class QccnewSpider(scrapy.Spider):
    name = 'qccnew'
    allowed_domains = []
    start_urls = ['https://www.baidu.com/']

    def start_requests(self):
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        self.md5_utils = MD5Utils()
        self.qcc_utils = QCCUtils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            # registered_country=中国 and (registered_type=非上市公司 or 上市公司) and is_delete !=是
            query = Query.queries(Query(QueryType.EQ, 'registered_country', '中国'),
                                  Query(QueryType.NE, 'is_delete', '是'),
                                  Query.queries(Query(QueryType.EQ, 'registered_type', '非上市公司'),
                                                Query(QueryType.EQ, 'registered_type', '上市公司'),
                                                and_perator=False), )

            # todo 测试五十家公司名称
            company_times = 0
            pages = es_utils.get_page(index=ESIndex.BASE_COMPANY, queries=query, show_fields=['name'], page_size=-1)
            for page in pages:
                company_times = company_times + 1
                if company_times > 50:
                    break
                name = self.str_utils.cn_mark2en_mark(page['name'])
                if len(self.str_utils.get_cn(str=name)) == 0:
                    logging.info(f'公司名称不包含中文，被过滤：{name}')
                    continue
                logging.info(f'公司名称：{name}, 追加待采集 ‘基本信息’ 链接！')
                base_info_url = QCCAPI.VERIFY_INFO + '?key=' + QCCUtils.APPKEY + '&searchKey=' + name
                yield scrapy.Request(base_info_url, callback=self.parse, meta={'name': name}, headers=self.qcc_utils.get_qcc_token_headers())


        if 'ECIInfoVerify' in spider_url:
            name = meta['name']
            results = ast.literal_eval(response.body.decode(QCCUtils.ENCODE).replace('true', 'True').replace('false', 'False').replace('null','None'))
            status = results.get('Status')
            if (status != '200'):
                logging.info(f'接口调用状态码：{response.status} 企查查接口返回状态码: {status} ,请求URL: {spider_url}')
                return

            result_dict = results['Result']
            credit_id = result_dict['CreditCode']  # 统一社会信用代码
            if None == credit_id or not bool(re.search(r'\d', credit_id)):
                logging.info(f'公司名称：{name} , 统一社会信用代码: {credit_id} 不包含数字，被过滤！')
                return
            registered_capital = result_dict['RegistCapi']  # 注册资本
            unit_list = self.str_utils.get_cn(registered_capital)  # 货币单位
            unit = ''.join(unit_list)
            results_es = self.es_utils.get_page(ESIndex.BUSINESS_INFO,
                                                queries=Query(QueryType.EQ, 'credit_id', credit_id), page_index=1,
                                                show_fields=['base_info_md5', 'shareholder_info_md5', 'main_staff_md5',
                                                             'company_change', 'registered_capital_currency',
                                                             'registered_capital',
                                                             'shareholder_info', 'company_change_list_md5'])
            parse_base_info(self, name, credit_id, result_dict, results_es, registered_capital)  # 基本信息
            parse_main_staff(self, name, credit_id, result_dict, results_es)  # 主要人员
            parse_shareholder_info(self, name, credit_id, result_dict, results_es, unit)  # 股东信息
            parse_company_change(self, name, credit_id, result_dict, results_es)  # 企业变更

def parse_company_change(self, name, credit_id, result_dict, results_es):
    # todo 初始化使用，后期删除，使用company_change_list_md5 判断是否新增
    company_change_es_last_date = -28800000
    if None != results_es and 'company_change' in results_es[0]:
        company_change_es = results_es[0]['company_change']
        for company_change_str in company_change_es:
            if 'change_date' not in company_change_str:
                continue
            change_date = company_change_str['change_date']
            if not self.str_utils.has_nums(str(change_date)):
                continue
            if company_change_es_last_date < change_date:
                company_change_es_last_date = change_date
    company_change_list = []
    company_change_set_md5 = set()
    company_change_list_md5 = []
    change_records = result_dict['ChangeRecords']
    for change_record in change_records:
        change_date_str = change_record['ChangeDate']  # 变更日期
        change_date = self.date_utils.unix_time(change_date_str)
        change_project = change_record['ProjectName']  # 变更项目
        before_change = change_record['BeforeContent']  # 变更前
        after_change = change_record['AfterContent']  # 变更后
        id = self.md5_utils.get_md5(change_date_str + change_project + before_change + after_change)
        company_change_list_md5.append(id)
        if change_date > company_change_es_last_date:
            if id not in company_change_set_md5:
                company_change_obj = {}
                company_change_obj['id'] = id
                company_change_obj['change_date'] = change_date_str
                company_change_obj['change_project'] = change_project
                company_change_obj['before_change'] = before_change
                company_change_obj['after_change'] = after_change
                company_change_list.append(company_change_obj)
        company_change_set_md5.add(id)

    company_change_list_md5_dict = {}
    if None != results_es:
        company_change_list_md5_dict['esid'] = results_es[0]['esid']
        company_change_list_md5_dict['company_change_list_md5'] = company_change_list_md5
    if len(company_change_list) == 0:
        if len(company_change_list_md5_dict) > 0:
            self.es_utils.update(ESIndex.BUSINESS_INFO, d=company_change_list_md5_dict)
        logging.info(f'公司名称：{name} ,‘企业变更’ 无数据或未发生变更，被过滤！')
        return
    if None != results_es and 'company_change' in results_es[0]:
        company_change_es_list = results_es[0]['company_change']
        for company_change_es in company_change_es_list:
            change_date_es = self.date_utils.defined_format_time(timestamp=company_change_es['change_date'], format='%Y-%m-%d')
            company_change_es['change_date'] = change_date_es
            company_change_list.append(company_change_es)
    company_change_obj = {}
    company_change_redis_obj = {}
    company_change_obj['company_change'] = company_change_list
    company_change_obj['company_change_list_md5'] = company_change_list_md5
    company_change_redis_obj['type'] = '新增'
    company_change_redis_obj['id'] = credit_id
    company_change_redis_obj['table'] = 'business_info'
    company_change_redis_obj['content'] = company_change_obj
    company_change_redis_obj['collection'] = 'company_change'
    company_change_redis_obj['datestamp'] = DateUtils().get_timestamp()
    logging.info('------- redis data ‘企业变更’ 信息：' + name +'-------')
    self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(company_change_redis_obj, default=set_default).encode('utf-8').decode('unicode_escape'))

def parse_shareholder_info(self, name, credit_id, result_dict, results_es, unit):
    id = 0
    shareholder_info_arr = []
    partners = result_dict['Partners']
    for partner in partners:
        id = id + 1
        shareholder_info_obj = {}
        shareholder_info_obj['id'] = id  # 序号
        if 'RelatedOrg' in partner and None != partner['RelatedOrg']:
            spider_capital_name_short = partner['RelatedOrg']['Name']  #基金才会传输数据

        shareholder_info_obj['key_no'] = partner['KeyNo']  # 编码
        shareholder_info_obj['shareholder'] = self.str_utils.cn_mark2en_mark(partner['StockName'])  # 股东及出资信息
        subscriptions = partner['ShouldCapi']
        if self.str_utils.has_nums(subscriptions):
            shareholder_info_obj['subscriptions'] = partner['ShouldCapi'] + unit  # 认缴出资额(数字 + 货币单位)
        shareholder_info_obj['subscriptions_actual'] = ''  # 实缴额
        shareholder_info_arr.append(shareholder_info_obj)
    type = '新增'
    shareholder_info_md5 = self.md5_utils.get_md5(data=shareholder_info_arr)
    if None != results_es:
        #天眼查的数据给李昊传（base_company）;备注：基金不传
        shareholder_info_dict = {}
        shareholder_info_dict['credit_id'] = credit_id
        if 'registered_capital_currency' in results_es[0]:
            shareholder_info_dict['pre_registered_capital_currency'] = results_es[0]['registered_capital_currency']
        if 'registered_capital' in results_es[0]:
            shareholder_info_dict['pre_registered_capital'] = results_es[0]['registered_capital']
        shareholder_info_dict['registered_capital'] = results_es[0]['registered_capital']
        shareholder_info_dict['spider_wormtime'] = self.date_utils.get_timestamp()
        self.redis_server.lpush(RedisKey.REGISTERED_CAPITAL_LIST, json.dumps(shareholder_info_dict).encode('utf-8').decode('unicode_escape'))


        shareholder_info_es_md5 = get_es_md5(results_es, 'shareholder_info_md5')
        if shareholder_info_md5 != shareholder_info_es_md5:
            type = '修改'
        else:
            logging.info(f'公司名称：{name} ,该公司 ‘股东信息’ 未发生变更，被过滤！')
            return
    shareholder_info_content = {}
    shareholder_info_redis_obj = {}
    shareholder_info_content['shareholder_info'] = shareholder_info_arr
    shareholder_info_redis_obj['content'] = shareholder_info_content
    shareholder_info_redis_obj['id'] = credit_id
    shareholder_info_redis_obj['type'] = type  # 类型：新增，修改
    shareholder_info_redis_obj['table'] = 'business_info'
    shareholder_info_redis_obj['collection'] = 'shareholder_info'
    shareholder_info_redis_obj['datestamp'] = self.date_utils.get_timestamp()
    shareholder_info_redis_obj['shareholder_info_md5'] = shareholder_info_md5
    logging.info('------- redis data ‘股东信息’ 信息：' + name+' -------')
    shareholder_info_redis = json.dumps(shareholder_info_redis_obj).encode('utf-8').decode('unicode_escape')
    self.redis_server.lpush(RedisKey.BUSINESS_INFO, shareholder_info_redis)

    #通知李昊，股东变更前与变更后的信息传递（base_company）;备注：基金不传
    pre_content = []
    if None != results_es and 'shareholder_info' in results_es[0]:
        pre_content = results_es[0]['shareholder_info']
    shareholder_info_obj = {}
    shareholder_info_obj['credit_id'] = credit_id
    shareholder_info_obj['pre_content'] = pre_content
    shareholder_info_obj['content'] = shareholder_info_redis
    shareholder_info_obj['spider_wormtime'] = self.date_utils.get_timestamp()
    self.redis_server.lpush(RedisKey.SHAREHOLDER_INFO_LIST, shareholder_info_obj)


def parse_main_staff(self, name, credit_id, result_dict, results_es):
    id = 0
    main_staff_arr = []
    employees = result_dict['Employees']
    for employee in employees:
        id = id + 1
        main_staff_dict = {}
        main_staff_dict['id'] = id  # 序号
        main_staff_dict['key_no'] = employee['KeyNo']  # 编码
        main_staff_dict['position'] = employee['Job']  # 职位
        main_staff_dict['name_person'] = employee['Name']  # 姓名
        main_staff_arr.append(main_staff_dict)

    main_staff_md5 = self.md5_utils.get_md5(data=main_staff_arr)
    type = '新增'
    if None != results_es:
        main_staff_es_md5 = get_es_md5(results_es, 'main_staff_md5')
        if main_staff_es_md5 != main_staff_md5:
            type = '修改'
        else:
            logging.info(f'公司名称：{name} ,该公司 ‘主要人员’ 未发生变更，被过滤！')
            return
    logging.info(f'公司名称：{name} ,‘主要人员’ 已采集完毕！')
    main_staff_content = {}
    main_staff_redis_obj = {}
    main_staff_content['main_staff'] = main_staff_arr
    main_staff_redis_obj['content'] = main_staff_content
    main_staff_redis_obj['id'] = credit_id
    main_staff_redis_obj['type'] = type  # 类型：新增，修改
    main_staff_redis_obj['table'] = 'business_info'
    main_staff_redis_obj['collection'] = 'main_staff'
    main_staff_redis_obj['datestamp'] = self.date_utils.get_timestamp()
    main_staff_redis_obj['main_staff_md5'] = main_staff_md5
    logging.info('------- redis data ‘主要人员’ 信息：' + name+'-------')
    self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(main_staff_redis_obj).encode('utf-8').decode('unicode_escape'))

def parse_base_info(self, name, credit_id, result_dict, results_es, registered_capital):
    register_date = result_dict['StartDate'].split(' ')[0]  # 注册时间
    approved_date = result_dict['CheckDate'].split(' ')[0]  # 核准日期
    representative = result_dict['OperName']  # 法定代表人
    term_from = result_dict['TermStart'].split(' ')[0]  # 营业期限自
    term_to = result_dict['TeamEnd'].split(' ')[0]  # 营业期限至
    authority = result_dict['BelongOrg']  # 登记机关
    company_status = result_dict['Status']  # 登记状态
    address = result_dict['Address']  # 企业地址
    business_scope = result_dict['Scope']  # 经营范围
    company_type = result_dict['EconKind']  # 企业类型
    contact_info = result_dict['ContactInfo']
    insured_nums = result_dict['InsuredCount']  # 参保人数
    name_en = result_dict['EnglishName']  # 英文名称
    website = ''
    if 'WebSite' in contact_info and None != contact_info['WebSite']:
        website = contact_info['WebSite'][0]['Url']  # 网址
    tel = contact_info['PhoneNumber']  # 联系方式
    mail = contact_info['Email']  # 邮箱
    area = result_dict['Area']
    tag_list = result_dict['TagList']
    province = area['Province']  # 省
    city = area['City']  # 市
    county = area['County']  # 国家
    if None != results_es:
        name = self.str_utils.cn_mark2en_mark(result_dict['Name'])  # 公司名称
    base_info_md5 = self.md5_utils.get_md5(company_type + representative + term_from + term_to + authority + company_status + address + business_scope + approved_date)
    redis_base_info(self, name, credit_id, representative, registered_capital, register_date, approved_date, term_from,
                    term_to, authority, company_status, address, business_scope, company_type, base_info_md5,
                    results_es,insured_nums, name_en, website, tel, mail, tag_list, province, city, county)

def redis_base_info(self,name, credit_id, representative, registered_capital, register_date, approved_date,
                  term_from, term_to, authority, company_status, address, business_scope, company_type, base_info_md5, results_es,
                    insured_nums, name_en, website, tel, mail, tag_list, province, city, county):
    data_type = '新增'
    spider_wormtime = self.date_utils.get_timestamp()
    base_info_es_md5 = get_es_md5(results_es, 'base_info_md5')
    if None != results_es :
        if base_info_es_md5 != base_info_md5:
            data_type = '修改'
        else:
            logging.info(f'公司名称：{name} ,该公司 ‘基本信息’ 未发生变更，被过滤！')
            update_es_dict = {} #更新爬虫时间
            update_es_dict['esid'] = results_es['esid']
            update_es_dict['spider_wormtime'] = spider_wormtime
            self.es_utils.insert_or_replace(ESIndex.BUSINESS_INFO, d=update_es_dict)
            return
    base_info_redis_obj = {}
    base_info_redis_content = {}
    is_blank(self, key='registered_capital', value=registered_capital, base_info_redis_content=base_info_redis_content)
    is_blank(self, key='register_date', value=register_date, base_info_redis_content=base_info_redis_content)
    is_blank(self, key='approved_date', value=approved_date, base_info_redis_content=base_info_redis_content)
    base_info_redis_content['name'] = name
    base_info_redis_content['credit_id'] = credit_id
    base_info_redis_content['type'] = company_type
    base_info_redis_content['representative'] = representative
    base_info_redis_content['company_status'] = company_status
    base_info_redis_content['term_from'] = term_from
    base_info_redis_content['term_to'] = term_to
    base_info_redis_content['authority'] = authority
    base_info_redis_content['address'] = address
    base_info_redis_content['business_scope'] = business_scope
    # base_info_redis_content['insured_nums'] = insured_nums 暂时不需要
    # base_info_redis_content['name_en'] = name_en 基金的数据
    base_info_redis_content['website'] = website
    base_info_redis_content['tel'] = tel
    base_info_redis_content['mail'] = mail
    base_info_redis_content['tag_list'] = tag_list
    base_info_redis_content['province'] = province
    base_info_redis_content['city'] = city
    base_info_redis_content['county'] = county
    base_info_redis_content['spider_wormtime'] = spider_wormtime
    base_info_redis_obj['id'] = credit_id
    base_info_redis_obj['type'] = data_type
    base_info_redis_obj['collection'] = 'base_info'
    base_info_redis_obj['datestamp'] = spider_wormtime
    base_info_redis_obj['table'] = ESIndex.BUSINESS_INFO
    base_info_redis_obj['base_info_md5'] = base_info_md5
    base_info_redis_obj['content'] = base_info_redis_content
    logging.info('------- redis data ' + data_type + ' 企业 ‘基本信息’ -------' + credit_id)
    self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(base_info_redis_obj).encode('utf-8').decode('unicode_escape'))

def is_blank(self, key, value, base_info_redis_content):
    if(not self.str_utils.is_blank(value)):
        base_info_redis_content[key] = value

def get_es_md5(results_es, param):
    if results_es != None and param in results_es[0]:
        return results_es[0][param]
    return None
