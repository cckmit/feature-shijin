
import json
import logging
import ast
import os
import scrapy
from pyquery import PyQuery as pq
from pharmcube_spider import const
from pharmcube_spider.const import ESIndex
from pharmcube_spider.utils import es_utils, file_utils
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings

'''
基金数据采集：
* 私募基金公示：http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html
* 私募基金管理人综合查询列表页：http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html
* 证券公司直投基金：http://gs.amac.org.cn/amac-infodisc/res/aoin/product/index.html
'''

headers = const.json_headers
headers['Referer'] = 'https://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html'
local_file_path = const.STORE_PATH + 'fund_data.txt'

class FundSpider(scrapy.Spider):
    name = 'fund'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.es_utils = es_utils
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.md5_utils = MD5Utils()
        self.file_utils = file_utils
        self.mongo_utils = MongoUtils()
        self.file_utils.delete_file_or_dir(path=local_file_path)
        self.redis_server = from_settings(get_project_settings())
        self.invalid_fund_name_set = read_invalid_fund_name(self, False)
        self.fund_name_dict = read_invalid_fund_name(self, True)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        spider_url = response.url
        logging.info(
            f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            wait_url_list = []
            wait_url_list.append({'type': 'list', 'url': 'https://gs.amac.org.cn/amac-infodisc/api/pof/fund?size=100&page=0', 'source':'fund_name', 'prefix_url': 'https://gs.amac.org.cn/amac-infodisc/res/pof/fund/'})
            wait_url_list.append({'type': 'list', 'url': 'https://gs.amac.org.cn/amac-infodisc/api/pof/manager?size=100&page=0', 'source':'fund_manager', 'prefix_url': 'https://gs.amac.org.cn/amac-infodisc/res/pof/manager/'})
            wait_url_list.append({'type': 'list', 'url': 'https://gs.amac.org.cn/amac-infodisc/api/aoin/product?size=100&page=0', 'source': 'fund_product', 'prefix_url': 'https://gs.amac.org.cn/amac-infodisc/res/aoin/product/'})
            for wait_url in wait_url_list:
                yield scrapy.Request(wait_url['url'], method='post', body=json.dumps({}), callback=self.parse, meta=wait_url, headers=headers)

        if 'source' in meta and 'list' == meta['type']:  # 基金名录列表页
            results = ast.literal_eval(
                response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            if 'page=0' in spider_url:
                for page_index in range(1, results['totalPages']):
                    title_url = spider_url.replace('page=0', f'page={page_index}')
                    logging.info(f'追加待采集的列表页：{page_index} {meta["source"]}')
                    meta['type'] = 'list'
                    yield scrapy.Request(title_url, method='post', body=json.dumps({}), callback=self.parse, meta=meta, headers=headers)

            for content in results['content']:
                url = ''
                fund_name = ''
                source = meta['source']
                if 'fund_product' != source:
                    url = meta['prefix_url'] + content['url']
                else:
                    url = meta['prefix_url'] + content['id'] + '.html'
                source = meta['source']
                if 'fund_name' == source:
                    fund_name = self.str_utils.cn_mark2en_mark(str=content['fundName'])
                elif 'fund_manager' == source:
                    fund_name = self.str_utils.cn_mark2en_mark(str=content['managerName'])
                else:
                    fund_name = self.str_utils.cn_mark2en_mark(str=content['name'])
                if self.str_utils.remove_mark(str=fund_name) in self.invalid_fund_name_set:
                    logging.info(f'当前基金已经打入ES冷宫，过滤中: {fund_name}')
                    continue
                logging.info(f'追加待采集的列表页：{source} {fund_name} ')
                meta['type'] = 'detail'
                yield scrapy.Request(url, callback=self.parse, meta=meta, headers=headers)
            return

        if 'source' in meta and 'detail' == meta['type']:  # 基金名录详情页
            doc = pq(response.text)
            tr_elements = doc('.table-response tr')
            content_dict = {}
            for tr_element in tr_elements.items():
                td_elements = tr_element('td')
                if len(td_elements) < 2:
                    continue
                key = self.str_utils.remove_mark(str=pq(td_elements[0]).text())
                if '基金协会特别提示' in key and 'fund_name' == meta['source']:
                    break
                value = ''
                if pq(td_elements[1])('#complaint1').size() > 0:
                    value = pq(td_elements[1])('#complaint1').text()
                else:
                    value = pq(td_elements[1]).text()
                content_dict[key] = self.str_utils.strip(str=value)

            if 'fund_name' == meta['source']:  # 私募基金公示
                parse_fund(self, content_dict, meta)

            if 'fund_manager' == meta['source']:  # 私募基金管理人综合查询
                parse_manager(self, content_dict, meta)

            if 'fund_product' == meta['source']:  # 证券公司直投基金
                fund_name = self.str_utils.cn_mark2en_mark(str=content_dict['产品名称'])
                fund_no = content_dict['产品编码']
                if self.str_utils.is_blank(str=fund_no):
                    logging.info(f'当前证券公司直投基金编号不存在，被过滤：{fund_name}')
                    return
                register_date = content_dict['设立日期']
                record_date = content_dict['备案日期']
                fund_type = content_dict['基金类型']
                trustee = content_dict['托管人名称']
                status = content_dict['运作状态']
                fund_manager = self.str_utils.cn_mark2en_mark(str=content_dict['管理机构名称'])
                writer_product_file(self, fund_name, fund_no, register_date, record_date, fund_type, trustee, status, fund_manager, meta['source'])

    def close(spider, reason):
        logging.info(f'------- 当前基金数据已经更新完毕，开始传输 redis 数据 -------')
        """
        if not os.path.exists(local_file_path):
            logging.info(f'------- 未发现存储文件 {local_file_path}，程序停止 -------')
            return
        with open(file=local_file_path, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                spider.redis_server.lpush(const.RedisKey.DATA_CLEAN_INVEST_CHINA_FUND, line)
        """


def read_invalid_fund_name(self, is_spider):
    queries = None
    if is_spider:
        self.fund_name_dict = {}  # 需要更新的基金信息
        queries = Query(QueryType.EQ, 'is_paid_attention', '是')
    else:
        self.invalid_fund_name_set = set()
        queries = Query(QueryType.NE, 'is_paid_attention', '是')
        if is_spider:
            logging.info(f'------- 读取ES待更新基金名称 -------')
        else:
            logging.info(f'------- 读取ES已被打入冷宫的基金名称 -------')
    pages = es_utils.get_page(ESIndex.INVEST_CHINA_FUND, page_size=-1, queries=queries,
                              show_fields=['fund_name', 'used_name', 'last_updated', 'securities_fund_md5'])
    for page in pages:
        last_updated = None
        if 'fund_name' not in page:
            continue
        fund_name = self.str_utils.remove_mark(str=page['fund_name'])
        securities_fund_md5 = ''
        if 'securities_fund_md5' in page:
            securities_fund_md5 = page['securities_fund_md5']
        elif 'last_updated' in page:
            last_updated = self.date_utils.defined_format_time(timestamp=page['last_updated'], format='%Y-%m-%d')
        if is_spider:
            self.fund_name_dict[fund_name] = last_updated
            if not self.str_utils.is_blank(securities_fund_md5):
                self.fund_name_dict[fund_name] = securities_fund_md5
        else:
            self.invalid_fund_name_set.add(fund_name)
        if 'used_name' in page and None != page['used_name']:
            for used_name in page['used_name']:
                used_name = self.str_utils.remove_mark(str=used_name)
                if is_spider:
                    self.fund_name_dict[used_name] = last_updated
                    if not self.str_utils.is_blank(securities_fund_md5):
                        self.fund_name_dict[fund_name] = securities_fund_md5
                else:
                    self.invalid_fund_name_set.add(used_name)
    if is_spider:
        return self.fund_name_dict
    else:
        return self.invalid_fund_name_set

def writer_product_file(self, fund_name, fund_no, register_date, record_date, fund_type, trustee, status, fund_manager,
                        source):
    spider_wormtime = self.date_utils.get_timestamp()
    securities_fund_md5 = self.md5_utils.get_md5(
        data=fund_name + register_date + record_date + fund_type + trustee + status + fund_manager)
    type = '新增'
    if self.str_utils.remove_mark(str=fund_name) in self.fund_name_dict:
        securities_fund_md5_es = self.fund_name_dict[self.str_utils.remove_mark(str=fund_name)]
        if securities_fund_md5 != securities_fund_md5_es:
            type = '修改'
        else:
            logging.info(f'当前证券基金信息未发生变更，被过滤：{fund_name}')
            return
    redis_dict = {}
    redis_dict['fund_name'] = fund_name
    redis_dict['fund_no'] = fund_no
    redis_dict['register_date'] = register_date
    redis_dict['record_date'] = record_date
    redis_dict['fund_type'] = fund_type
    redis_dict['fund_manager'] = fund_manager
    redis_dict['trustee'] = trustee
    redis_dict['status'] = status
    redis_dict['securities_fund_md5'] = securities_fund_md5
    redis_dict['spider_wormtime'] = spider_wormtime
    writer_file(self, source, redis_dict, fund_name, spider_wormtime, type)

def parse_manager(self, content_dict, meta):
    fund_name = self.str_utils.cn_mark2en_mark(str=content_dict['基金管理人全称中文'])
    fund_manager_en = self.str_utils.cn_mark2en_mark(str=content_dict['基金管理人全称英文'])
    register_no = self.str_utils.cn_mark2en_mark(str=content_dict['登记编号'])
    if self.str_utils.is_blank(str=register_no):
        logging.info(f'当前基金管理人编号不存在，被过滤：{fund_name}')
        return
    record_date = content_dict['登记时间']
    register_date = content_dict['成立时间']
    registered_address = content_dict['注册地址']
    office_address = content_dict['办公地址']
    registered_capital = content_dict['注册资本万元人民币'].replace(',', '')
    paid_in_capital = content_dict['实缴资本万元人民币'].replace(',', '')
    business_nature = content_dict['企业性质']
    proportion = content_dict['注册资本实缴比例']
    orgniztion_type = content_dict['机构类型']
    last_updated = content_dict.get('机构信息最后更新时间', None)
    type = '新增'
    if self.str_utils.remove_mark(str=fund_name) in self.fund_name_dict:
        last_updated_es = self.fund_name_dict[self.str_utils.remove_mark(str=fund_name)]
        if last_updated != last_updated_es:
            type = '修改'
        else:
            logging.info(f'当前基金管理人信息未发生变更，被过滤：{fund_name}')
            return

    '''
    website = content_dict['机构网址']
    employ_num = content_dict['员工人数']
    business_type = content_dict['业务类型'] 后台未用，暂时注释
    legal_state = content_dict['法律意见书状态']
    legal_representative = content_dict['法定代表人执行事务合伙人委派代表姓名']
    qualification = content_dict.get('是否有从业资格', None)
    if self.str_utils.is_blank(str=qualification):
        qualification = content_dict.get('是否有基金从业资格', None)
    credit_information = content_dict.get('机构诚信信息', None)
    special_message = content_dict.get('特别提示信息', None)
    '''
    writer_manager_file(self, fund_name, fund_manager_en, register_no, record_date, register_date, registered_address,
                        office_address, registered_capital,
                        paid_in_capital, business_nature, proportion, orgniztion_type, last_updated, meta['source'],
                        type)


def writer_file(self, source, redis_dict, fund_name, spider_wormtime, type):
    redis_obj = {}
    redis_obj['type'] = type
    redis_obj['id'] = fund_name
    redis_obj['content'] = redis_dict
    redis_obj['datestamp'] = spider_wormtime
    redis_obj['table'] = 'invest_china_fund'
    logging.info(f'数据存储到文件中：{source} {fund_name}')
    self.file_utils.write_file(file_name=local_file_path, data_type='a',
                               content=json.dumps(redis_obj).encode('utf-8').decode('unicode_escape'))


def writer_manager_file(self, fund_name, fund_manager_en, register_no, record_date, register_date, registered_address,
                        office_address, registered_capital, paid_in_capital, business_nature, proportion,
                        orgniztion_type, last_updated, source, type):
    spider_wormtime = self.date_utils.get_timestamp()
    redis_dict = {}
    redis_dict['fund_no'] = register_no
    redis_dict['fund_name'] = fund_name
    redis_dict['fund_manager'] = fund_name
    redis_dict['fund_manager_en'] = fund_manager_en
    redis_dict['last_updated'] = last_updated
    redis_dict['proportion'] = proportion
    redis_dict['record_date'] = record_date
    redis_dict['register_date'] = register_date
    redis_dict['registered_address'] = registered_address
    redis_dict['office_address'] = office_address
    redis_dict['registered_capital'] = registered_capital
    redis_dict['paid_in_capital'] = paid_in_capital
    redis_dict['business_nature'] = business_nature
    redis_dict['orgniztion_type'] = orgniztion_type
    redis_dict['spider_wormtime'] = spider_wormtime
    writer_file(self, source, redis_dict, fund_name, spider_wormtime, type)


def parse_fund(self, content_dict, meta):
    fund_name = self.str_utils.cn_mark2en_mark(str=content_dict['基金名称'])
    if len(self.str_utils.get_cn(str=fund_name)) == 0:
        logging.info(f'当前基金名称不包含中文，被过滤：{fund_name}')
        return
    fund_no = content_dict['基金编号']
    if self.str_utils.is_blank(str=fund_no):
        logging.info(f'当前基金对应的基金编号为空，被过滤：{fund_name} {fund_no}')
        return
    last_updated = content_dict['基金信息最后更新时间']
    type = '新增'
    if self.str_utils.remove_mark(str=fund_name) in self.fund_name_dict:
        last_updated_es = self.fund_name_dict[self.str_utils.remove_mark(str=fund_name)]
        if last_updated != last_updated_es:
            type = '修改'
        else:
            logging.info(f'当前基金公示信息未发生变更，被过滤：{fund_name}')
            return
    register_date = content_dict['成立时间']
    record_date = content_dict['备案时间']
    filing = content_dict.get('基金备案阶段', None)
    fund_type = content_dict['基金类型']
    currency = content_dict['币种']
    fund_manager = self.str_utils.cn_mark2en_mark(content_dict['基金管理人名称'])
    manager_type = content_dict['管理类型']
    trustee = content_dict['托管人名称']
    status = content_dict['运作状态']
    writer_fund_file(self, fund_name, fund_no, register_date, record_date, filing, fund_type, currency, fund_manager,
                     manager_type, trustee, status, last_updated, meta['source'], type)


def writer_fund_file(self, fund_name, fund_no, register_date, record_date, filing, fund_type, currency,
                     fund_manager, manager_type, trustee, status, last_updated, source, type):
    spider_wormtime = self.date_utils.get_timestamp()
    redis_dict = {}
    redis_dict['fund_name'] = fund_name
    redis_dict['fund_no'] = fund_no
    redis_dict['register_date'] = register_date
    redis_dict['filing'] = filing
    redis_dict['fund_type'] = fund_type
    redis_dict['currency'] = currency
    redis_dict['fund_manager'] = fund_manager
    redis_dict['record_date'] = record_date
    redis_dict['manager_type'] = manager_type
    redis_dict['trustee'] = trustee
    redis_dict['status'] = status
    redis_dict['last_updated'] = last_updated
    redis_dict['spider_wormtime'] = spider_wormtime
    writer_file(self, source, redis_dict, fund_name, spider_wormtime, type)
