import json
import logging
import math
import re
import ast
import scrapy
from pharmcube_spider.const import ESIndex, RedisKey, PAGEOPS, QCCAPI
from pharmcube_spider.utils import es_utils, file_utils
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


redis_server = from_settings(get_project_settings())


def is_blank(self, key, value, base_info_redis_content):
    if (not self.str_utils.is_blank(value)):
        base_info_redis_content[key] = value


def get_es_md5(results_es, param):
    if results_es != None and param in results_es[0]:
        return results_es[0][param]
    return None


def redis_base_info(self, name, credit_id, representative, registered_capital, register_date, approved_date,
                    term_from, term_to, authority, company_status, address, business_scope, company_type, base_info_md5,
                    results_es):
    data_type = '新增'
    spider_wormtime = DateUtils().get_timestamp()
    base_info_es_md5 = get_es_md5(results_es, 'base_info_md5')
    if base_info_es_md5 != base_info_md5:
        data_type = '修改'
    else:
        logging.info(f'公司名称：{name} ,该公司 ‘基本信息’ 相同，被过滤！')
        update_es_dict = {}  # 更新爬虫时间
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
    base_info_redis_content['spider_wormtime'] = spider_wormtime
    base_info_redis_obj['id'] = credit_id
    base_info_redis_obj['type'] = data_type
    base_info_redis_obj['collection'] = 'base_info'
    base_info_redis_obj['datestamp'] = spider_wormtime
    base_info_redis_obj['table'] = ESIndex.BUSINESS_INFO
    base_info_redis_obj['base_info_md5'] = base_info_md5
    base_info_redis_obj['content'] = base_info_redis_content
    logging.info('------- redis ' + data_type + ' 企业 ‘基本信息’ -------' + credit_id)
    redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(base_info_redis_obj).encode('utf-8').decode('unicode_escape'))


def parse_base_info(self, scrapy, name, results):
    result_dict = results['Result']
    credit_id = result_dict['CreditCode']  # 统一社会信用代码
    # todo 临时记录公司采集的公司名称
    file_utils.write_file('/home/zengxiangxu/jinqiu.txt', data_type='a', content=name)

    if None == credit_id or not bool(re.search(r'\d', credit_id)):
        logging.info(f'公司名称：{name} , 统一社会信用代码: {credit_id} 不包含数字，被过滤！')
        return
    registered_capital = result_dict['RegistCapi']  # 注册资本
    unit_list = self.str_utils.get_cn(registered_capital)  # 货币单位
    unit = ''
    for u in unit_list:
        unit += u
    register_date = result_dict['StartDate'].split(' ')[0]  # 注册时间
    approved_date = result_dict['CheckDate'].split(' ')[0]  # 核准日期
    representative = result_dict['OperName']  # 法定代表人
    term_from = result_dict['TermStart'].split(' ')[0]  # 营业期限自
    term_to = result_dict['TeamEnd'].split(' ')[0]  # 营业期限至
    name = self.str_utils.cn_mark2en_mark(result_dict['Name'])  # 公司名称
    authority = result_dict['BelongOrg']  # 登记机关
    company_status = result_dict['Status']  # 登记状态
    address = result_dict['Address']  # 企业地址
    business_scope = result_dict['Scope']  # 经营范围
    company_type = result_dict['EconKind']  # 企业类型
    results_es = self.es_utils.get_page(ESIndex.BUSINESS_INFO, queries=Query(QueryType.EQ, 'credit_id', credit_id),
                                        page_index=1,
                                        show_fields=['base_info_md5', 'shareholder_info_md5', 'main_staff_md5',
                                                     'company_change'])
    # 带出 company_change 只做第一次初始化使用，后期删除
    company_change_last_date = -28800000  # 默认值 1970-01-01 00:00:00
    company_change_es = []
    if results_es != None and 'company_change' in results_es[0]:
        company_change_es = results_es[0]['company_change']
        for company_change_str in company_change_es:
            if 'change_date' not in company_change_str:
                continue
            change_date = company_change_str['change_date']
            if not self.str_utils.has_nums(str(change_date)):
                continue
            if company_change_last_date < change_date:
                company_change_last_date = change_date
    base_info_md5 = MD5Utils().get_md5(
        company_type + representative + term_from + term_to + authority + company_status + address + business_scope + name + approved_date)
    redis_base_info(self, name, credit_id, representative, registered_capital, register_date, approved_date, term_from,
                    term_to, authority, company_status, address, business_scope, company_type, base_info_md5,
                    results_es)

    # 企业变更
    logging.info(f'公司名称：{name} ,追加待采集 ‘企业变更’ 链接！')
    company_change_url = QCCAPI.COMPANY_CHANGE + '?key=' + QCCUtils.APPKEY + '&searchKey=' + name
    yield scrapy.Request(company_change_url, callback=self.parse, meta={'name': name, 'credit_id': credit_id,
                                                                        'company_change_last_date': company_change_last_date,
                                                                        'company_change_es': company_change_es},
                         headers=self.qcc_utils.get_qcc_token_headers(), priority=100)

    # 股东列表
    logging.info(f'公司名称：{name} ,追加待采集 ‘股东列表’ 链接！')
    shareholder_info_url = QCCAPI.SHAREHOLDER_INFO + '?key=' + QCCUtils.APPKEY + '&searchKey=' + name + '&pageIndex=' + str(
        1) + '&pageSize=' + str(PAGEOPS.PAGE_SIZE)
    yield scrapy.Request(shareholder_info_url, callback=self.parse,
                         meta={'name': name, 'credit_id': credit_id, 'unit': unit, 'page_index': 1,
                               'page_size': PAGEOPS.PAGE_SIZE,
                               'shareholder_info_md5': get_es_md5(results_es, 'shareholder_info_md5')},
                         headers=self.qcc_utils.get_qcc_token_headers(), priority=100)

    # 主要人员信息解析数据
    main_staff_url = QCCAPI.MAIN_STAFF + '?key=' + QCCUtils.APPKEY + '&searchKey=' + name + '&pageIndex=' + str(
        1) + '&pageSize=' + str(PAGEOPS.PAGE_SIZE)
    logging.info(f'公司名称：{name} ,追加待采集 ‘主要人员’ 链接！')
    yield scrapy.Request(main_staff_url, callback=self.parse,
                         meta={'name': name, 'credit_id': credit_id, 'page_index': 1,
                               'page_size': PAGEOPS.PAGE_SIZE,
                               'main_staff_md5': get_es_md5(results_es, 'main_staff_md5')},
                         headers=self.qcc_utils.get_qcc_token_headers(), priority=100)


# 数据翻页操作
def page_ops(self, spider_url, page_size, page_index, meta, scrapy, log_info):
    for page_index in range(page_index + 1, page_index + 2):
        logging.info(log_info)
        url = spider_url + '&pageIndex=' + str(page_index) + '&pageSize=' + str(page_size)
        yield scrapy.Request(url, callback=self.parse, meta=meta, headers=self.qcc_utils.get_qcc_token_headers(),
                             priority=100)


def getID(data_arr_name, response):
    id = 0
    data_arr = []
    if data_arr_name in response.meta:
        data_arr = response.meta[data_arr_name]
        for i in range(0, len(data_arr)):  # 获取序号最大的值
            id_before = data_arr[i]['id']
            if id < id_before:
                id = id_before
    return [id, data_arr]


# 主要人员列表
def parse_eci_employee(self, response, scrapy, name, page_index, page_size, results):
    credit_id = response.meta['credit_id']
    main_staff_es_md5 = response.meta['main_staff_md5']
    total_records = results['Paging']['TotalRecords']  # 总条数(校验是否需要翻页)
    if total_records == 0:
        logging.info(f'公司名称：{name} ,没有‘主要人员’信息！')
        return
    id_list = getID('main_staff_arr', response)
    id = id_list[0]
    main_staff_arr = id_list[1]
    for result in results['Result']:
        id = id + 1
        main_staff_obj = {}
        main_staff_obj['id'] = id  # 序号
        main_staff_obj['position'] = result['Job']  # 职位
        main_staff_obj['name_person'] = result['Name']  # 姓名
        main_staff_arr.append(main_staff_obj)

    total_pages = math.ceil(total_records / page_size)
    if page_index == total_pages:
        main_staff_md5 = MD5Utils().get_md5(data=str(main_staff_arr))
        if response.meta['main_staff_md5'] == main_staff_md5:
            logging.info(f'公司名称：{name} , ‘主要人员’ 信息未发生变更，被过滤！')
            return
        data_type = ''
        if None is response.meta['main_staff_md5']:
            data_type = '新增'
        else:
            data_type = '修改'
        logging.info(f'公司名称：{name} ,‘主要人员’ 已采集完毕！')
        main_staff_content = {}
        main_staff_redis_obj = {}
        main_staff_content['main_staff'] = main_staff_arr
        main_staff_redis_obj['content'] = main_staff_content
        main_staff_redis_obj['id'] = credit_id
        main_staff_redis_obj['type'] = data_type  # 类型：新增，修改
        main_staff_redis_obj['table'] = 'business_info'
        main_staff_redis_obj['collection'] = 'main_staff'
        main_staff_redis_obj['datestamp'] = DateUtils().get_timestamp()
        main_staff_redis_obj['main_staff_md5'] = main_staff_md5
        logging.info('redis ‘主要人员’ 信息：' + name)
        redis_server.lpush(RedisKey.BUSINESS_INFO,
                           json.dumps(main_staff_redis_obj).encode('utf-8').decode('unicode_escape'))
    else:
        meta = {'name': name, 'credit_id': credit_id, 'page_index': page_index + 1, 'page_size': page_size,
                "main_staff_md5": main_staff_es_md5, "main_staff_arr": main_staff_arr}
        yield from page_ops(self, QCCAPI.MAIN_STAFF + '?key=' + QCCUtils.APPKEY + '&searchKey=' + name, page_size,
                            page_index, meta, scrapy, f'公司名称：{name} ,‘主要人员’ 添加待采集页数：{page_index + 1}')


def get_resp_meta(param, resp):
    page_param = 0
    if param in resp.meta:
        page_param = resp.meta[param]
    return page_param


# 股东信息列表
def parse_eci_partner(self, response, scrapy, name, page_index, page_size, results):
    credit_id = response.meta['credit_id']
    shareholder_info_es_md5 = response.meta['shareholder_info_md5']
    total_records = results['Paging']['TotalRecords']  # 总条数(校验是否需要翻页)
    if total_records == 0:
        logging.info(f'公司名称：{name} ,没有‘股东信息’信息！')
        return
    unit = response.meta['unit']
    id_list = getID('shareholder_info_arr', response)
    id = id_list[0]
    shareholder_info_arr = id_list[1]
    for result in results['Result']:
        id = id + 1
        mshareholder_info_obj = {}
        mshareholder_info_obj['id'] = id  # 序号
        mshareholder_info_obj['shareholder'] = result['StockName']  # 股东及出资信息
        subscriptions = result['ShouldCapi']
        if self.str_utils.has_nums(subscriptions):
            mshareholder_info_obj['subscriptions'] = subscriptions  # 认缴出资额
            mshareholder_info_obj['subscriptions_str'] = result['ShouldCapi'] + unit  # 认缴出资额(数字 + 货币单位)
        mshareholder_info_obj['subscriptions_actual'] = ''  # 实缴额
        shareholder_info_arr.append(mshareholder_info_obj)

    total_pages = math.ceil(total_records / page_size)
    if page_index == total_pages:
        shareholder_info_md5 = MD5Utils().get_md5(data=str(shareholder_info_arr))
        if response.meta['shareholder_info_md5'] == shareholder_info_md5:
            logging.info(f'公司名称：{name} , ‘股东信息’ 信息未发生变更，被过滤！')
            return
        data_type = ''
        if None is response.meta['shareholder_info_md5']:
            data_type = '新增'
        else:
            data_type = '修改'
        logging.info(f'公司名称：{name} ,‘股东信息’ 已采集完毕！')
        shareholder_info_content = {}
        shareholder_info_redis_obj = {}
        shareholder_info_content['shareholder_info'] = shareholder_info_arr
        shareholder_info_redis_obj['content'] = shareholder_info_content
        shareholder_info_redis_obj['id'] = credit_id
        shareholder_info_redis_obj['type'] = data_type  # 类型：新增，修改
        shareholder_info_redis_obj['table'] = 'business_info'
        shareholder_info_redis_obj['collection'] = 'shareholder_info'
        shareholder_info_redis_obj['datestamp'] = DateUtils().get_timestamp()
        shareholder_info_redis_obj['shareholder_info_md5'] = shareholder_info_md5
        logging.info('redis ‘股东信息’ 信息：' + name)
        redis_server.lpush(RedisKey.BUSINESS_INFO,
                           json.dumps(shareholder_info_redis_obj).encode('utf-8').decode('unicode_escape'))
    else:
        meta = {'name': name, 'credit_id': credit_id, 'unit': unit, 'page_index': page_index + 1,
                'page_size': page_size, "shareholder_info_md5": shareholder_info_es_md5,
                "shareholder_info_arr": shareholder_info_arr}
        yield from page_ops(self, QCCAPI.SHAREHOLDER_INFO + '?key=' + QCCUtils.APPKEY + '&searchKey=' + name, page_size,
                            page_index, meta, scrapy, f'公司名称：{name} ,‘股东信息’ 添加待采集页数：{page_index + 1}')


# 企业变更
def get_company_change_info(result):
    if len(result) == 0:
        return ''
    return result


def parse_eci_change(self, response, results):
    company_change_set_md5 = set()
    name = response.meta['name']
    credit_id = response.meta['credit_id']
    company_change_last_date = response.meta['company_change_last_date']

    company_change = []
    company_change_es_size = len(response.meta['company_change_es'])
    if 'company_change_es' in response.meta:
        company_change = response.meta['company_change_es']

    for result in results['Result']:
        change_date_str = result['ChangeDate']  # 变更日期
        change_date = DateUtils().unix_time(change_date_str)
        change_project = result['ProjectName']  # 变更项目
        before_change = get_company_change_info(result['BeforeList'])  # 变更前
        after_change = get_company_change_info(result['AfterList'])  # 变更后
        company_change_set_md5.add(
            MD5Utils().get_md5(str(change_date) + change_project + str(before_change) + str(after_change)))
        if change_date > company_change_last_date:
            company_change_obj = {}
            company_change_obj['change_date'] = change_date
            company_change_obj['change_project'] = change_project
            company_change_obj['before_change'] = before_change
            company_change_obj['after_change'] = after_change
            company_change.append(company_change_obj)
    if len(company_change) == 0:
        logging.info(f'公司名称：{name} ,‘企业变更’ 无数据，被过滤！')
        return
    if len(company_change) == company_change_es_size:
        logging.info(f'公司名称：{name} ,‘企业变更’ 未发生，被过滤！')
        return
    company_change_obj = {}
    company_change_redis_obj = {}
    company_change_obj['company_change'] = company_change
    company_change_redis_obj['type'] = '新增'
    company_change_redis_obj['id'] = credit_id
    company_change_redis_obj['table'] = 'business_info'
    company_change_redis_obj['content'] = company_change_obj
    company_change_redis_obj['collection'] = 'company_change'
    company_change_redis_obj['datestamp'] = DateUtils().get_timestamp()
    company_change_redis_obj['company_change_set_md5'] = company_change_set_md5
    logging.info('redis ‘企业变更’ 信息：' + name)
    # dict 转换为json（中包含set集合数据）
    redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(company_change_redis_obj, default=set_default).encode('utf-8').decode('unicode_escape'))


# 基本信息、股东信息、主要人员、企业变更
class QccSpider(scrapy.Spider):
    name = 'qcc'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(
            f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            # registered_country=中国 and (registered_type=非上市公司 or 上市公司) and is_delete !=是
            query = Query.queries(Query(QueryType.EQ, 'registered_country', '中国'),
                                  Query(QueryType.NE, 'is_delete', '是'),
                                  Query.queries(Query(QueryType.EQ, 'registered_type', '非上市公司'),
                                                Query(QueryType.EQ, 'registered_type', '上市公司'),
                                                and_perator=False), )

            pages = es_utils.get_page(index=ESIndex.BASE_COMPANY, queries=query, show_fields=['name'], page_size=-1)
            for page in pages:
                name = self.str_utils.cn_mark2en_mark(page['name'])
                cn_list = self.str_utils.get_cn(str=name)
                if len(cn_list) == 0:
                    logging.info(f'公司名称不包含中文，被过滤：{name}')
                    continue
                logging.info(f'公司名称：{name}, 追加待采集 ‘基本信息’ 链接！')
                base_info_url = QCCAPI.BASE_INFO + '?key=' + QCCUtils.APPKEY + '&keyword=' + name
                yield scrapy.Request(base_info_url, callback=self.parse, meta={'name': name},
                                     headers=self.qcc_utils.get_qcc_token_headers())

            # 设置优先级
            # yield scrapy.Request('https://www.baidu.com?9999', callback=self.parse, headers=self.qcc_utils.get_qcc_token_headers(), priority=100)

        if 'qichacha' in spider_url:
            name = response.meta['name']
            page_index = get_resp_meta(param='page_index', resp=response)
            page_size = get_resp_meta(param='page_size', resp=response)

            results = ast.literal_eval(
                response.body.decode(QCCUtils.ENCODE).replace('true', 'True').replace('false', 'False').replace('null',
                                                                                                                'None'))
            status = results.get('Status')
            if (status != '200'):
                logging.info(f'接口调用状态码：{response.status} 企查查接口返回状态码: {status} ,请求URL: {spider_url}')
                return

            if 'GetBasicDetailsByName' in spider_url:  # 企业工商详情
                yield from parse_base_info(self, scrapy=scrapy, name=name, results=results)

            if 'ECIChange' in spider_url:  # 企业变更
                parse_eci_change(self, response=response, results=results)

            if 'ECIPartner' in spider_url:  # 股东信息
                yield from parse_eci_partner(self, response=response, scrapy=scrapy, name=name, page_index=page_index,
                                             page_size=page_size, results=results)

            if 'ECIEmployee' in spider_url:  # 主要人员列表页信息
                yield from parse_eci_employee(self, response=response, scrapy=scrapy, name=name, page_index=page_index,
                                              page_size=page_size, results=results)

    def close(spider, reason):
        logging.info('------- 当前更新结束 -------')
        pass
