import logging
import ast
import scrapy
from pyquery import PyQuery as pq
from pharmcube_spider import const
from pharmcube_spider.const import MongoTables
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.mongo_utils import MongoUtils


'''
医保药品分类与代码数据库更新:
目的：爬取医保药品分类代码，补充上市药品的商品名，更正药品的ATC代码
URL：http://code.nhsa.gov.cn:8000/search.html?sysflag=100
'''

class NhsaSpider(scrapy.Spider):
    name = 'nhsa'
    allowed_domains = []
    start_urls = ['http://code.nhsa.gov.cn:8000/search.html?sysflag=100']

    def start_requests(self):
        self.mongo_utils = MongoUtils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        spider_url = response.url
        logging.info(
            f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'sysflag=100' in spider_url:
            doc = pq(response.text)
            batch_num = doc('#dataInfo').attr('src').split('=')[1]
            link = f'http://code.nhsa.gov.cn:8000/yp/getPublishGoodsDataInfo.html?rows=100&batchNumber={batch_num}&sidx=t.goods_code&sord=asc&page=1'
            logging.info(f'追加待采集的页数: 1 ')
            yield scrapy.Request(link, callback=self.parse, meta={'page_index': 1, 'batch_num': batch_num, }, headers=const.headers)

        if 'page=' in spider_url:
            batch_num = meta['batch_num']
            page_index = meta['page_index']
            results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            if spider_url.endswith('page=1'):
                total = int(results['total'])
                for page_index in range(2, total+1):
                    link = f'http://code.nhsa.gov.cn:8000/yp/getPublishGoodsDataInfo.html?rows=100&batchNumber={batch_num}&sidx=t.goods_code&sord=asc&page={page_index}'
                    logging.info(f'追加待采集的页数: {page_index}')
                    yield scrapy.Request(link, callback=self.parse, meta={'page_index': page_index, 'batch_num': batch_num}, headers=const.headers)
            mongo_list = []
            for row in results['rows']:
                nhsa_drug_id = row['goodscode'] #药品代码
                nhsa_drug_name = row['registeredproductname'] #注册名称
                nhsa_trade_name = row['goodsname'] #商品名称
                nhsa_formulation = row['registeredmedicinemodel'] #注册剂型
                nhsa_strength = row['registeredoutlook'] #注册规格
                nhsa_pack_material = row['materialname'] #包装材质
                nhsa_pack_num = row['factor'] #最小包装数量
                nhsa_formulation_nhsa_pack_unit = row['minunit'] #最小制剂单位
                nhsa_pack_unit = row['unit'] #最小包装单位
                nhsa_manufacture = row['companynamesc'] #药品企业
                nhsa_approval_num = row['approvalcode'] #批准文号
                nhsa_drug_code = row['goodsstandardcode'] #药品本位码
                insurance_type = is_exist('productinsurancetype', row)  #甲乙类
                insurance_num = is_exist('productcode', row)  #编号
                insurance_drug_name = is_exist('productname', row)  #药品名称
                insurance_formulation = is_exist('productmedicinemodel', row)  #剂型
                mongo_dict = dict_data(batch_num, page_index, nhsa_drug_id, nhsa_drug_name, nhsa_trade_name, nhsa_formulation, nhsa_strength, nhsa_pack_material, nhsa_pack_num,
                          nhsa_formulation_nhsa_pack_unit, nhsa_pack_unit, nhsa_manufacture, nhsa_approval_num, nhsa_drug_code, insurance_type, insurance_num, insurance_drug_name, insurance_formulation)
                mongo_list.append(mongo_dict)
            logging.info(f'------- insert mongo data -------{page_index}\t{batch_num}')
            self.mongo_utils.insert_many(mongo_list=mongo_list, coll_name=MongoTables.DRUG_NHSA)

def dict_data(batch_num, page_index, nhsa_drug_id, nhsa_drug_name, nhsa_trade_name, nhsa_formulation,
              nhsa_strength, nhsa_pack_material, nhsa_pack_num, nhsa_formulation_nhsa_pack_unit, nhsa_pack_unit, nhsa_manufacture, nhsa_approval_num, nhsa_drug_code,
              insurance_type, insurance_num, insurance_drug_name, insurance_formulation):
    mongo_dict = {}
    mongo_dict['batch_num'] = batch_num
    mongo_dict['page_index'] = page_index
    mongo_dict['nhsa_drug_id'] = nhsa_drug_id
    mongo_dict['nhsa_drug_name'] = nhsa_drug_name
    mongo_dict['nhsa_trade_name'] = nhsa_trade_name
    mongo_dict['nhsa_formulation'] = nhsa_formulation
    mongo_dict['nhsa_strength'] = nhsa_strength
    mongo_dict['nhsa_pack_material'] = nhsa_pack_material
    mongo_dict['nhsa_pack_num'] = nhsa_pack_num
    mongo_dict['nhsa_formulation_nhsa_pack_unit'] = nhsa_formulation_nhsa_pack_unit
    mongo_dict['nhsa_pack_unit'] = nhsa_pack_unit
    mongo_dict['nhsa_manufacture'] = nhsa_manufacture
    mongo_dict['nhsa_approval_num'] = nhsa_approval_num
    mongo_dict['nhsa_drug_code'] = nhsa_drug_code
    mongo_dict['insurance_type'] = insurance_type
    mongo_dict['insurance_num'] = insurance_num
    mongo_dict['insurance_drug_name'] = insurance_drug_name
    mongo_dict['insurance_formulation'] = insurance_formulation
    mongo_dict['page_count'] = 100
    mongo_dict['spider_wormtime'] = DateUtils().get_timestamp()
    return mongo_dict


def is_exist(key, row):
    value = ''
    if key in row:
        value = row[key]
    return value