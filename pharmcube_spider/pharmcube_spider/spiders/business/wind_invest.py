
import logging
import ast
import re
import scrapy
from pharmcube_spider.const import WindAPI
from pharmcube_spider.const import MongoTables
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils import es_utils, qiniu_utils, common_utils
from pharmcube_spider.spiders.business.wind_utils import is_invalid_windid, get_wind_token, \
    product_wind_token, page_ops, get_wind_id, get_resp_meta






class InvestSpider(scrapy.Spider):
    name = 'wind_invest'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [403],
    }

    def start_requests(self):
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.mongo_utils = MongoUtils()
        self.common_utils = common_utils
        self.redis_server = from_settings(get_project_settings())
        product_wind_token(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            with open('/home/zengxiangxu/1.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    name = line.replace("\n", '')
                    base_fund_id = str('111')
                    base_fund_name = StrUtils().cn_mark2en_mark(name)
                    self.wind_token = get_wind_token(self, )
                    wind_id = get_wind_id(self, base_fund_name,)
                    if is_invalid_windid(self, wind_id, base_fund_name):
                        continue
                    logging.info(f'公司名称：{base_fund_name}, 追加待采集 ‘企业对外穿透’ 链接！')
                    invest_info_url = "http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/K014?windId=" + wind_id + "&token=" + self.wind_token + "&pageIndex=1&pageSize=10"
                    yield scrapy.Request(invest_info_url, callback=self.parse, meta={'base_fund_name': base_fund_name,
                                         'fund_name': base_fund_name, 'base_fund_id': base_fund_id, 'wind_id': wind_id, 'spider_source': 'invest'}, )

        if 'eapi.wind.com.cn' in spider_url:
            results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            status = results.get('errorCode')
            if (status == 403):
                logging.info(f'接口调用状态码：403，token 已经过期，需重新获取 token 值！{spider_url}')
                self.wind_token = get_wind_token(self)
                yield scrapy.Request(spider_url, callback=self.parse, meta=response.meta, dont_filter=True)
                return

            fund_name = response.meta['fund_name']
            base_fund_id = response.meta['base_fund_id']
            base_fund_name = response.meta['base_fund_name']
            results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            if 'A002?windId' in spider_url:  # 企业工商详情
                parse_basic_page(self, response, base_fund_id, base_fund_name, results)

            if 'K014?windId' in spider_url: #对外投资穿透
                yield from parseInvestPage(self, fund_name, base_fund_id, base_fund_name, results, spider_url, response)


    def close(spider, reason):
        logging.info('------- 当前对外投资采集完毕，准备传输数据 -------')


#对外投资信息(判断是否追加)
def fund_name_base_info(self, base_fund_name, company_name, fund_name_set, proportion, meta):
    if common_utils.is_success_set(fund_name_set=fund_name_set, data_str=company_name):
        logging.info(f'当前对外被投资公司已追加，被过滤：{base_fund_name} \t {company_name}')
        return
    logging.info(f'追加待采集的对外被投资公司的基本信息：{base_fund_name} \t {company_name}')
    meta['proportion'] = proportion
    wind_id = get_wind_id(self, company_name, )
    if not self.str_utils.is_blank(str=wind_id):
        logging.info(f'获取到公司对应的 wind_id:{wind_id}，追加待采集公司 ‘基本信息’： {company_name}')
        base_info_url = WindAPI.BASE_INFO + f'{wind_id}&token={self.wind_token}'
        yield scrapy.Request(base_info_url, callback=self.parse, meta=meta, priority=100)
    else:
        return
    if '合伙' in company_name or '投资' in company_name or '基金' in company_name or '创业' in company_name or \
            '创投' in company_name or '孵化' in company_name or '管理中心' in company_name:
        logging.info(f'公司名称：{company_name}, 追加待采集 ‘企业对外穿透’ 链接！')
        meta['wind_id'] = wind_id
        meta['fund_name'] = company_name
        del meta['proportion']
        invest_info_url = "http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/K014?windId="+wind_id+"&token="+self.wind_token+"&pageIndex=1&pageSize=10"
        yield scrapy.Request(invest_info_url, callback=self.parse, meta=meta, priority=100)

def parse_basic_page(self, response, base_fund_id, base_fund_name, results):
    fund_name = response.meta['fund_name']
    proportion = response.meta['proportion']  # 投资占比
    source = results["source"]
    credit_id = source['creditId']  # 统一社会信用代码
    company_name = self.str_utils.cn_mark2en_mark(source['corpName'])  # 公司名称
    if not bool(re.search(r'\d', credit_id)):
        logging.info(f'公司名称：{company_name} , 统一社会信用代码: {credit_id} 不包含数字，被过滤！')
        return
    unit = source['regCapCur']  # 注册资本单位
    if '万' not in unit:
        unit = '万' + unit
    registered_capital = source['regCap'] + unit  # 注册资本
    register_date = source['establishDate']  # 注册时间
    legal_representative = source['legalRepName']  # 法定代表人
    company_state = source['regStatus'] # 登记状态
    spider_wormtime = self.date_utils.get_timestamp()
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
    self.mongo_utils.update_one(query=query, value=mongo_value, coll_name=MongoTables.INVEST_CHINA_FUND)

def parseInvestPage(self, fund_name, base_fund_id, base_fund_name, results, spider_url, response):
    fund_name_set = set()
    meta = response.meta
    source = results['source']
    if 'pageIndex=1' in spider_url:
        for page_index in range(2, int(source['total']/10)+2):
            invest_info_url = "http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/K014?windId=" + meta['wind_id'] + "&token=" + self.wind_token
            yield from page_ops(self, invest_info_url, 10, page_index-1, meta, scrapy, f'公司名称：{fund_name}, ‘企业对外穿透’ 添加待采集页数：{page_index}')
    else:
        meta = {'base_fund_name': base_fund_name, 'base_fund_id': base_fund_id, 'fund_name': fund_name}
    children_list = source['children']
    for children in children_list:
        company_name = children['name']
        stock_percent = f'{children["percent"]}%'
        yield from fund_name_base_info(self, base_fund_name=base_fund_name, company_name=company_name, fund_name_set=fund_name_set, proportion=stock_percent, meta=meta)

def writerFileData(content):
    with open('/home/zengxiangxu/business_info_test.txt', mode='a') as filename:
        filename.write(content)
        filename.write('\n')  # 换行

