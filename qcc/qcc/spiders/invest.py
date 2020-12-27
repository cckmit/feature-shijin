import ast
import json
import re
import uuid
import scrapy
import logging
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from scrapy_redis_cluster.spiders import RedisSpider
from qcc.spiders.const import QCCAPI, MongoTables
from qcc.utils import common_utils
from qcc.utils.date_utils import DateUtils
from qcc.utils.mongo_utils import MongoUtils
from qcc.utils.qcc_utils import QCCUtils
from qcc.utils.str_utils import StrUtils



spider_fund_name_set = set()
mongo_utils = MongoUtils()

#对外投资信息(判断是否追加)
def getFundNameBaseInfo(self, base_fund_name, fund_name, company_name, fund_name_set, proportion, meta):
    if common_utils.is_success_set(fund_name_set=fund_name_set, data_str=company_name):
        logging.info(f'当前对外被投资公司已追加，被过滤：{base_fund_name} \t {company_name}')
        return

    logging.info(f'追加待采集的对外被投资公司的基本信息：{base_fund_name} \t {company_name}')
    meta['proportion'] = proportion
    base_info_url = QCCAPI.BASE_INFO + '?key=' + QCCUtils.APPKEY + '&keyword=' + company_name
    yield scrapy.Request(base_info_url, callback=self.parse, meta=meta, headers=self.qcc_utils.get_qcc_token_headers())

    if '合伙' in company_name or '投资' in company_name or '基金' in company_name or '创业' in company_name or '创投' in company_name or '孵化' in company_name or '管理中心' in company_name:
        logging.info(f'公司名称：{company_name}, 追加待采集 ‘企业对外穿透’ 链接！')
        meta['fund_name'] = company_name
        invest_info_url = QCCAPI.INVEST_INFO + '?key=' + QCCUtils.APPKEY + '&searchKey=' + base_fund_name + "&percent=0"
        yield scrapy.Request(invest_info_url, callback=self.parse, meta=meta, headers=self.qcc_utils.get_qcc_token_headers())

def parseBasicPage(response, base_fund_id, base_fund_name, results):
    fund_name = response.meta['fund_name']
    proportion = response.meta['proportion']  # 投资占比
    result_dict = results['Result']
    credit_id = result_dict['CreditCode']  # 统一社会信用代码
    company_name = result_dict['Name']  # 企查查返回的公司名称
    if not bool(re.search(r'\d', credit_id)):
        logging.info(f'公司名称：{company_name} , 统一社会信用代码: {credit_id} 不包含数字，被过滤！')
        return
    registered_capital = result_dict['RegistCapi']  # 注册资本
    register_date = result_dict['StartDate'].split(' ')[0]  # 注册时间
    legal_representative = result_dict['OperName']  # 被投资法定代表人
    company_state = result_dict['Status']  # 登记状态
    spider_wormtime = DateUtils().get_timestamp()
    invest_china_fund_redis_obj = {}
    invest_china_fund_redis_content = {}
    invest_china_fund_redis_content['base_fund_name'] = base_fund_name
    invest_china_fund_redis_content['base_fund_id'] = base_fund_id
    invest_china_fund_redis_content['fund_name'] = fund_name
    invest_china_fund_redis_content['is_invest_company'] = '否'
    invest_china_fund_redis_content['company_name'] = company_name
    invest_china_fund_redis_content['register_date'] = register_date
    invest_china_fund_redis_content['legal_representative'] = legal_representative
    invest_china_fund_redis_content['registered_capital'] = registered_capital
    invest_china_fund_redis_content['company_state'] = company_state
    invest_china_fund_redis_content['proportion'] = str(proportion)
    invest_china_fund_redis_content['spider_wormtime'] = spider_wormtime
    invest_china_fund_redis_obj['table'] = 'invest_outbound'
    invest_china_fund_redis_obj['type'] = '新增'
    invest_china_fund_redis_obj['datestamp'] = spider_wormtime
    invest_china_fund_redis_obj['content'] = str(invest_china_fund_redis_content)
    invest_china_fund_redis_obj['id'] = base_fund_id + "+" + base_fund_name + "+" + company_name
    query = {"base_fund_id": base_fund_id}
    mongo_value = {"$addToSet": {"foreign_investment": str(invest_china_fund_redis_obj)}}
    logging.info("------- insert mongo data -------" + "fund_name " + fund_name + " company_name " + company_name)
    mongo_utils.update_one(query=query, value=mongo_value, coll_name=MongoTables.INVEST_CHINA_FUND)

def parseInvestPage(self, fund_name, base_fund_id, base_fund_name, results):
    fund_name_set = set()
    meta = {'base_fund_name': base_fund_name, 'base_fund_id': base_fund_id, 'fund_name': fund_name}
    break_through_list = results['Result']['BreakThroughList']
    for break_through in break_through_list:
        detail_info_list = break_through['DetailInfoList']
        is_proportion = False  # 投资比例
        total_stock_percent = float(break_through['TotalStockPercent'].replace('%', ''))
        for detail_info in detail_info_list:
            path = detail_info['Path']
            splits = path.split('->')
            for split_index in range(1, len(splits)):
                company_name = StrUtils().cn_mark2en_mark(splits[split_index])
                if '%' in company_name:
                    rsplits = company_name.rsplit('(')
                    company_name = company_name[0:company_name.rindex('(')]
                    stock_percent = float(rsplits[len(rsplits) - 1].replace('%)', ''))
                elif (split_index != len(splits) - 1 and '%' not in company_name) or is_proportion: #中间公司出现一个没有百分比，后面投资比例重置都为0
                    stock_percent = 0
                    is_proportion = True
                else:
                    stock_percent = total_stock_percent
                yield from getFundNameBaseInfo(self, base_fund_name=base_fund_name, fund_name=fund_name, company_name=company_name, fund_name_set=fund_name_set, proportion=stock_percent, meta=meta)

def writerFileData(content):
    with open('/home/zengxiangxu/business_info_test.txt', mode='a') as filename:
        filename.write(content)
        filename.write('\n')  # 换行

class InvestSpider(scrapy.Spider):
    name = 'invest'
    allowed_domains = []
    redis_key = "invest:start_urls"
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            with open('/home/zengxiangxu/a.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    name = line.replace("\n", '')
                    base_fund_id = str('111')
                    base_fund_name = StrUtils().cn_mark2en_mark(name)
                    logging.info(f'公司名称：{base_fund_name}, 追加待采集 ‘企业对外穿透’ 链接！')
                    invest_info_url = QCCAPI.INVEST_INFO + '?key=' + QCCUtils.APPKEY + '&searchKey=' + base_fund_name + "&percent=0"
                    yield scrapy.Request(invest_info_url, callback=self.parse, meta={'base_fund_name': base_fund_name,
                                        'fund_name': base_fund_name, 'base_fund_id': base_fund_id}, headers=self.qcc_utils.get_qcc_token_headers())

        if 'qichacha' in spider_url:
            fund_name = response.meta['fund_name']
            base_fund_id = response.meta['base_fund_id']
            base_fund_name = response.meta['base_fund_name']
            results = ast.literal_eval(response.body.decode(QCCUtils.ENCODE).replace('true', 'True').replace('false', 'False').replace('null','None'))
            writerFileData(fund_name+"\t"+base_fund_id+"\t"+base_fund_name+"\n"+str(results))

            status = results.get('Status')
            if (status != str('200')):
                logging.info(f'接口调用状态码：{response.status} 企查查接口返回状态码: {status} ,请求URL: {spider_url}')
                return

            if 'GetBasicDetailsByName' in spider_url:  # 企业工商详情
                parseBasicPage(response, base_fund_id, base_fund_name, results)

            if 'ECIInvestmentThrough' in spider_url: #对外投资穿透
                yield from parseInvestPage(self, fund_name, base_fund_id, base_fund_name, results)

    # 静态方法，当spider关闭时，该函数被调用。
    @staticmethod
    def close(spider, reason):
        logging.info('------- 当前对外投资采集完毕，准备传输数据 -------')
        #todo 查询存储数据条数 ： MongoUtils





        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)

