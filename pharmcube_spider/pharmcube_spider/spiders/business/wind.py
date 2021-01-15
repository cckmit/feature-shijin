
import math
import logging
import ast
import json
import re
import scrapy
from pharmcube_spider.utils import es_utils, qiniu_utils, common_utils
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.const import WindAPI
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from pharmcube_spider.const import PAGEOPS
from pharmcube_spider.utils.common_utils import set_default
from pharmcube_spider.utils import file_utils
from pharmcube_spider.spiders.business.wind_utils import product_wind_token, \
    page_ops, get_wind_id, get_resp_meta, is_invalid_windid, get_wind_token
from pharmcube_spider.const import RedisKey, ESIndex

'''
万得对接工商接口
* 接口文档地址：http://share.wind.com.cn/wind.ent.openapi/#/api
* 账号：EA1968482002 密码已初始化为：94375596
'''





class WindSpider(scrapy.Spider):
    name = 'wind'
    allowed_domains = []
    start_urls = ['https://www.baidu.com/']
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [403],
    }

    def start_requests(self):
        self.es_utils = es_utils
        self.md5_utils = MD5Utils()
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.common_utils = common_utils
        self.wind_token = product_wind_token()
        self.redis_server = from_settings(get_project_settings())
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            search_name = '江苏恒瑞医药股份有限公司'
            wind_id = get_wind_id(self, search_name, )
            if is_invalid_windid(self, wind_id, search_name):
                return
            base_info_url = WindAPI.BASE_INFO + f'{wind_id}&token={self.wind_token}'
            logging.info(f'获取到公司对应的wind_id:{wind_id}，追加待采集公司 ‘基本信息’： {search_name}')
            yield scrapy.Request(base_info_url, callback=self.parse, meta={'search_name': search_name, 'name':search_name, 'spider_source': 'base_info', 'wind_id': wind_id}, )

        if None != response.meta and 'spider_source' in response.meta:
            spider_source = response.meta['spider_source']
            results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            status = results.get('errorCode')
            if (status != 403 ):
                logging.info(f'接口调用状态码：403，token已经过期，需重新获取token值！{spider_url}')
                self.wind_token = get_wind_token(self)
                yield scrapy.Request(spider_url, callback=self.parse, meta=response.meta, dont_filter=True)
                return
            source = results["source"]
            if 'base_info' in spider_source:
                yield from parse_base_info(self, source, response)
                return

            page_index = get_resp_meta(param='page_index', resp=response)
            page_size = get_resp_meta(param='page_size', resp=response)
            name = response.meta['name']
            if 'main_staff' in spider_source:
                yield from parse_eci_employee(self, response=response, scrapy=scrapy, name=name, page_index=page_index, page_size=page_size, results=results)

            if 'shareholder_info' in spider_source:
                yield from parse_eci_partner(self, response=response, scrapy=scrapy, name=name, page_index=page_index, page_size=page_size, results=results)

            if 'eci_change' in spider_source:  # 企业变更
                yield from parse_eci_change(self, response=response, results=results, page_index=page_index, page_size=page_size, spider_url=spider_url)


def parse_eci_change(self, response, results, page_index, page_size, spider_url):
    company_change_set_md5 = set()
    meta = response.meta
    name = meta['name']
    wind_id = meta['wind_id']
    credit_id = meta['credit_id']
    company_change_last_date = meta['company_change_last_date']
    company_change = []
    source = results['source']
    total_records = source['total']  # 总条数(校验是否需要翻页)
    if 'pageIndex=1' in spider_url:
        if total_records == 0:
            logging.info(f'公司名称：{name} ,没有 ‘企业变更’ 信息！')
            return
        company_change_es_size = len(meta['company_change_es'])
        if 'company_change_es' in meta:
            company_change = meta['company_change_es']
    else:
         company_change = meta['company_change_list']
         company_change_set_md5 = meta['company_change_set_md5']
    for result in source['items']:
        change_date_str = result['changeDate']  # 变更日期
        change_date = self.date_utils.unix_time(change_date_str)
        change_project = result['changeItem']  # 变更项目
        before_change = self.common_utils.unicode2str(get_company_change_info(result['changeBefore']))  # 变更前
        after_change = self.common_utils.unicode2str(get_company_change_info(result['changeAfter']))  # 变更后
        company_change_set_md5.add(self.md5_utils.get_md5(str(change_date) + change_project + str(before_change) + str(after_change)))
        if change_date > company_change_last_date:
            company_change_obj = {}
            #todo 临时加 change_date_str 便于测试 后期删除
            company_change_obj['change_date_str'] = change_date_str
            company_change_obj['change_date'] = change_date
            company_change_obj['change_project'] = change_project
            company_change_obj['before_change'] = before_change
            company_change_obj['after_change'] = after_change
            company_change.append(company_change_obj)
    if len(company_change) == 0:
        logging.info(f'公司名称：{name} ,‘企业变更’ 无数据，被过滤！')
        return
    if 'pageIndex=1' in spider_url:
        if len(company_change) == company_change_es_size:
            logging.info(f'公司名称：{name} ,‘企业变更’ 未发生，被过滤！')
            return
    total_pages = math.ceil(total_records / page_size)
    if page_index == total_pages:
        logging.info(f'公司名称：{name} ,‘企业变更’ 已采集完毕！')
        company_change_obj = {}
        company_change_redis_obj = {}
        company_change_obj['company_change'] = company_change
        company_change_redis_obj['type'] = '新增'
        company_change_redis_obj['id'] = credit_id
        company_change_redis_obj['table'] = 'business_info'
        company_change_redis_obj['content'] = company_change_obj
        company_change_redis_obj['collection'] = 'company_change'
        company_change_redis_obj['datestamp'] = self.date_utils.get_timestamp()
        company_change_redis_obj['company_change_set_md5'] = company_change_set_md5
        logging.info('redis ‘企业变更’ 信息：' + name)
        self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(company_change_redis_obj, default=set_default).encode('utf-8').decode('unicode_escape'))

        file_utils.write_file('/home/zengxiangxu/test.txt' ,data_type='a', content=json.dumps(company_change_redis_obj, default=set_default).encode('utf-8').decode('unicode_escape'))

    else:
        meta = {'name': name, 'credit_id': credit_id, 'wind_id': wind_id, 'company_change_last_date': company_change_last_date,
                'page_index': page_index+1, 'page_size': PAGEOPS.PAGE_SIZE, 'company_change_set_md5': company_change_set_md5,
                'spider_source': 'eci_change', 'company_change_list': company_change}
        company_change_url = WindAPI.COMPANY_CHANGE + f'{wind_id}&token={self.wind_token}'
        yield from page_ops(self, company_change_url, page_size, page_index, meta, scrapy, f'公司名称：{name}, ‘企业变更’ 添加待采集页数：{page_index+1}')

def parse_eci_partner(self, response, scrapy, name, page_index, page_size, results):
    meta = response.meta
    credit_id = meta['credit_id']
    wind_id = meta['wind_id']
    shareholder_info_es_md5 = response.meta['shareholder_info_md5']
    source = results['source']
    total_records = source['total']  # 总条数(校验是否需要翻页)
    if total_records == 0:
        logging.info(f'公司名称：{name} ,没有‘股东信息’信息！')
        return
    unit = response.meta['unit']
    id_list = get_id('shareholder_info_arr', response)
    id = id_list[0]
    shareholder_info_arr = id_list[1]
    for result in source['items']:
        id = id + 1
        mshareholder_info_obj = {}
        mshareholder_info_obj['id'] = id  # 序号
        mshareholder_info_obj['shareholder'] = result['name']  # 股东及出资信息
        subscriptions = result['amount']
        if self.str_utils.has_nums(subscriptions):
            mshareholder_info_obj['subscriptions'] = subscriptions  # 认缴出资额
            mshareholder_info_obj['subscriptions_str'] = result['amount'] + unit  # 认缴出资额(数字 + 货币单位)
        mshareholder_info_obj['subscriptions_actual'] = ''  # 实缴额
        shareholder_info_arr.append(mshareholder_info_obj)

    total_pages = math.ceil(total_records / page_size)
    if page_index == total_pages:
        shareholder_info_md5 = self.md5_utils.get_md5(data=str(shareholder_info_arr))
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
        self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(shareholder_info_redis_obj).encode('utf-8').decode('unicode_escape'))

        file_utils.write_file('/home/zengxiangxu/test.txt', data_type='a',
                              content=json.dumps(shareholder_info_redis_obj, default=set_default).encode('utf-8').decode(
                                  'unicode_escape'))



    else:
        meta = {'name': name, 'credit_id': credit_id, 'unit': unit, 'page_index': page_index + 1,
                'page_size': page_size, "shareholder_info_md5": shareholder_info_es_md5, 'wind_id': wind_id,
                "shareholder_info_arr": shareholder_info_arr, 'spider_source': 'shareholder_info'}
        shareholder_info_url = WindAPI.SHAREHOLDER_INFO + f'{wind_id}&token={self.wind_token}'
        yield from page_ops(self, shareholder_info_url, page_size, page_index, meta, scrapy, f'公司名称：{name} ,‘股东信息’ 添加待采集页数：{page_index + 1}')

# 主要人员列表
def parse_eci_employee(self, response, scrapy, name, page_index, page_size, results):
    meta = response.meta
    wind_id = meta['wind_id']
    credit_id = meta['credit_id']
    main_staff_es_md5 = response.meta['main_staff_md5']
    source = results['source']
    total_records = source['total']  # 总条数(校验是否需要翻页)
    if total_records == 0:
        logging.info(f'公司名称：{name} ,没有‘主要人员’信息！')
        return
    id_list = get_id('main_staff_arr', response)
    id = id_list[0]
    main_staff_arr = id_list[1]
    main_staff_temp_dict = {}
    for result in source['items']:
        name = result['name']
        title = result['title']
        if name not in main_staff_temp_dict:
            main_staff_temp_dict[name] = title
        else:
            main_staff_temp_dict[name] = main_staff_temp_dict[name]+';'+title
    for key in main_staff_temp_dict.keys():
        id = id + 1
        main_staff_obj = {}
        main_staff_obj['id'] = id  # 序号
        main_staff_obj['position'] = main_staff_temp_dict[key] # 职位
        main_staff_obj['name_person'] = key  # 姓名
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
        self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(main_staff_redis_obj).encode('utf-8').decode('unicode_escape'))

        file_utils.write_file('/home/zengxiangxu/test.txt', data_type='a',
                              content=json.dumps(main_staff_redis_obj, default=set_default).encode('utf-8').decode('unicode_escape'))

    else:
        meta = {'name': name, 'credit_id': credit_id, 'page_index': page_index + 1, 'page_size': page_size,
                "main_staff_md5": main_staff_es_md5, "main_staff_arr": main_staff_arr, 'wind_id': wind_id}
        main_staff_url = WindAPI.MAIN_STAFF + f'{wind_id}&token={self.wind_token}'
        yield from page_ops(self, main_staff_url, page_size, page_index, meta, scrapy, f'公司名称：{name} ,‘主要人员’ 追加待采集页数：{page_index + 1}')


def parse_base_info(self, source, response):
    search_name = response.meta['search_name']
    wind_id = response.meta['wind_id']
    credit_id = source['creditId']  # 统一社会信用代码
    if None == credit_id or not bool(re.search(r'\d', credit_id)):
        logging.info(f'公司名称：{search_name} , 统一社会信用代码: {credit_id} 不包含数字，被过滤！')
        return
    unit = source['regCapCur']  # 注册资本单位
    if '万' not in unit:
        unit = '万' + unit
    registered_capital = source['regCap'] + unit  # 注册资本
    register_date = source['establishDate']  # 注册时间
    approved_date = source['dateApproved']  # 核准日期
    representative = source['legalRepName']  # 法定代表人
    term_from = source['openFrom']  # 营业期限自
    term_to = source['openTo']  # 营业期限至
    name = self.str_utils.cn_mark2en_mark(source['corpName'])  # 公司名称
    authority = source['regOrg']  # 登记机关
    company_status = source['regStatus']  # 登记状态
    address = source['busAddress']  # 企业地址
    business_scope = source['businessScope']  # 经营范围
    company_type = source['corpType']  # 企业类型
    results_es = self.es_utils.get_page(ESIndex.BUSINESS_INFO,
                                        queries=Query(QueryType.EQ, 'credit_id', credit_id), page_index=1,
                                        show_fields=['base_info_md5', 'shareholder_info_md5', 'main_staff_md5', 'company_change'])
    if None == results_es:
        name = search_name
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
    base_info_md5 = MD5Utils().get_md5(company_type + representative + term_from + term_to + authority + company_status + address + business_scope + name + approved_date)
    redis_base_info(self, name, credit_id, representative, registered_capital, register_date, approved_date, term_from,
                    term_to, authority, company_status, address, business_scope, company_type, base_info_md5, results_es)


    logging.info(f'公司名称：{name} , 追加待采集 ‘主要人员’ 链接！')
    main_staff_url = WindAPI.MAIN_STAFF + f'{wind_id}&token={self.wind_token}&pageIndex=1&pageSize={PAGEOPS.PAGE_SIZE}'
    yield scrapy.Request(main_staff_url, callback=self.parse,
                         meta={'name': name, 'credit_id': credit_id, 'page_index': 1, 'spider_source': 'main_staff', 'page_size': PAGEOPS.PAGE_SIZE,
                               'main_staff_md5': get_es_md5(results_es, 'main_staff_md5'), 'wind_id': wind_id}, priority=100)

    logging.info(f'公司名称：{name} ,追加待采集 ‘股东列表’ 链接！')
    shareholder_info_url = WindAPI.SHAREHOLDER_INFO + f'{wind_id}&token={self.wind_token}&pageIndex=1&pageSize={PAGEOPS.PAGE_SIZE}'
    yield scrapy.Request(shareholder_info_url, callback=self.parse,
                         meta={'name': name, 'credit_id': credit_id, 'unit': unit, 'page_index': 1, 'page_size': PAGEOPS.PAGE_SIZE, 'wind_id': wind_id,
                               'shareholder_info_md5': get_es_md5(results_es, 'shareholder_info_md5'), 'spider_source': 'shareholder_info'}, priority=100)

    # 企业变更
    logging.info(f'公司名称：{name} ,追加待采集 ‘企业变更’ 链接！')
    company_change_url = WindAPI.COMPANY_CHANGE + f'{wind_id}&token={self.wind_token}&pageIndex=1&pageSize={PAGEOPS.PAGE_SIZE}'
    yield scrapy.Request(company_change_url, callback=self.parse, meta={'name': name, 'credit_id': credit_id, 'wind_id':wind_id,
                                                                        'company_change_last_date': company_change_last_date,
                                                                        'page_index': 1, 'page_size': PAGEOPS.PAGE_SIZE,
                                                                        'company_change_es': company_change_es,'spider_source':'eci_change'}, priority=100)

def redis_base_info(self, name, credit_id, representative, registered_capital, register_date,
                    approved_date, term_from, term_to, authority, company_status, address, business_scope,
                    company_type, base_info_md5, results_es):
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
    self.redis_server.lpush(RedisKey.BUSINESS_INFO, json.dumps(base_info_redis_obj).encode('utf-8').decode('unicode_escape'))

    file_utils.write_file('/home/zengxiangxu/test.txt', data_type='a',
                          content=json.dumps(base_info_redis_obj, default=set_default).encode('utf-8').decode(
                              'unicode_escape'))


# 企业变更
def get_company_change_info(result):
    if len(result) == 0:
        return ''
    return result.replace('\n', '<br>')

def get_id(data_arr_name, response):
    id = 0
    data_arr = []
    if data_arr_name in response.meta:
        data_arr = response.meta[data_arr_name]
        for i in range(0, len(data_arr)):  # 获取序号最大的值
            id_before = data_arr[i]['id']
            if id < id_before:
                id = id_before
    return [id, data_arr]


def get_es_md5(results_es, param):
    if results_es != None and param in results_es[0]:
        return results_es[0][param]
    return None

def is_blank(self, key, value, base_info_redis_content):
    if (not self.str_utils.is_blank(value)):
        base_info_redis_content[key] = value

