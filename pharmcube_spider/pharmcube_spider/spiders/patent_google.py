import scrapy
import logging
import ast
import json
from pharmcube_spider import const
from urllib.parse import quote, unquote
from pharmcube_spider.utils.str_utils import StrUtils
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils import pdf_utils, es_utils, qiniu_utils, common_utils, file_utils
from pharmcube_spider.const import ESIndex
from pharmcube_spider.utils.es_utils import Query, QueryType
'''
从 google 采集非标准的专利号（标准化：EPO number-service接口返回）

'''

class PatentGoogleSpider(scrapy.Spider):
    name = 'patent_google'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.esid_set = set()
        self.es_utils = es_utils
        pages = self.es_utils.get_page(ESIndex.DRUG_PATENT_GOOGLE, page_size=-1, show_fields=['esid'])
        if None != pages:
            for page in pages:
                self.esid_set.add(page['esid'])
        self.file_utils = file_utils
        self.date_utils = DateUtils()
        self.md5_utils = MD5Utils()
        self.str_utils = StrUtils()
        self.init_date = init_date(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            # 针对的是 base_company 索引
            name_es_list = []
            name_es_list.append({'name':'恒瑞医药', 'id':['41818', '10598', '7407']})
            name_es_list.append({'name':'佐藤制药', 'id':['28094']})
            name_es_list.append({'name':'住友製薬株式会社', 'id':['431']})
            name_es_list.append({'name':'江苏恒瑞医药有限公司', 'id':['7407']})
            name_es_list.append({'name':'Pfizer, Inc.', 'id':['169']})
            name_es_list.append({'name':'Sanofi - Aventis, S.A.', 'id':['50']})
            name_es_list.append({'name':'上海复星医药(集团)股份有限公司', 'id':['16537']})

            for name_dict in name_es_list:
                name = name_dict['name']
                source_id_list = name_dict['id']
                type = 'AG'
                url = f'https://patents.google.com/xhr/query?url=assignee%3D%22{name}%22%26num%3D100%26page%3D0&exp='
                yield scrapy.Request(url, callback=self.parse, meta={'source_es_index': 'base_company', 'source_id_list': source_id_list,
                                    'is_add_all_year': False, 'is_calculation': True, 'name': name, 'type': type,
                                    'date_range': self.date_utils.defined_format_time(timestamp=self.date_utils.get_timestamp(), format='%Y-%m-%d')}, headers=const.headers)

        if 'google' in spider_url:
            meta = response.meta
            name = meta['name']
            type = meta['type']
            source_id_list = meta['source_id_list']
            source_es_index = meta['source_es_index']
            is_calculation = meta['is_calculation']
            is_add_all_year = meta['is_add_all_year']
            results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            results_dict = results['results']
            total_num_results = results_dict['total_num_results']
            total_num_pages = results_dict['total_num_pages']
            if total_num_pages > 9:
                if is_calculation:
                    if not is_add_all_year:
                        for year_str in self.init_date:
                            year_str_split = year_str.split('-')[0]
                            before = f'{int(year_str_split)+1}-01-01'
                            logging.info(f'追加待采集年份数据：{name} {year_str}:{before}')
                            url = f'https://patents.google.com/xhr/query?url=assignee%3D%22{name}%22%26before%3Dfiling%3A{before.replace("-","")}%26after%3Dfiling%3A{year_str.replace("-","")}%26num%3D100%26page%3D0&exp='
                            yield scrapy.Request(url, callback=self.parse, meta={'source_id_list':source_id_list, 'source_es_index':source_es_index, 'type': type,
                                          'is_add_all_year': True, 'is_calculation': True, 'name': name, 'date_range': f'{year_str_split}-12-31'}, headers=const.headers)

                    date_list = date_calculation(self, total_num_pages, meta)
                    for date_range_new in date_list:
                        date_range_splits = date_range_new['date_range'].replace('-', '').split(':')
                        logging.info(f'追加待采集的URL：{name} {date_range_new}')
                        url = f'https://patents.google.com/xhr/query?url==assignee%3D%22{name}%22%26before%3Dfiling%3A{date_range_splits[1]}%26after%3Dfiling%3A{date_range_splits[0]}%26num%3D100%26page%3D0&exp='
                        yield scrapy.Request(url, callback=self.parse, meta=date_range_new, headers=const.headers)

            elif total_num_pages >1 and total_num_pages <10 and '%26page%3D0' in spider_url:
                for page_index in range(1, total_num_pages):
                    url = spider_url.replace('%26page%3D0', f'%26page%3D{page_index}')
                    logging.info(f'公司进行翻页链接：{name} {page_index} {meta}')
                    yield scrapy.Request(url, callback=self.parse, meta=meta, headers=const.headers)

            cluster_dict = results_dict['cluster'][0]
            if 'result' not in cluster_dict:
                logging.info(f'当前公司检索无结果：{total_num_results} {total_num_pages} {name} {meta}')
                return
            result_list = cluster_dict['result']
            for result in result_list:
                for source_id in source_id_list:
                    publication_spider_comb = result['patent']['publication_number']
                    esid = self.md5_utils.get_md5(data=publication_spider_comb)
                    search_query_dict = {}
                    search_query_list = []
                    search_query_dict['type'] = type
                    search_query_dict['name'] = name
                    search_query_dict['url'] = spider_url
                    search_query_dict['url_decode'] = unquote(spider_url, 'utf-8') #解码
                    search_query_dict['source_id'] = source_id
                    search_query_dict['total_results'] = total_num_pages*100
                    search_query_dict['source_es_index'] = source_es_index
                    search_query_dict['spider_worktime'] = self.date_utils.get_timestamp()
                    search_query_list.append(search_query_dict)
                    es_dict = {}
                    es_dict['esid'] = esid
                    es_dict['status'] = 0 #刚采集到数据
                    es_dict['search_query'] = search_query_list
                    es_dict['publication_spider_comb'] = publication_spider_comb
                    logging.info(f'------- esid 新增：{esid} {publication_spider_comb} -------')
                    if esid not in self.esid_set:
                        self.esid_set.add(esid)
                        logging.info(f'------- insert es data -------{esid}')
                        es_utils.insert_or_replace('drug_patent_google', d=es_dict)
                    else:
                        pages = es_utils.get_page(ESIndex.DRUG_PATENT_GOOGLE, queries=Query(QueryType.EQ, 'esid', esid),
                                                  page_index=-1, show_fields=['search_query'])
                        if None != pages:
                            search_query_es_list = pages[0]['search_query']
                            search_query_es_list.append(search_query_dict)
                            update_es_dict = {}
                            update_es_dict['esid'] = esid
                            update_es_dict['search_query'] = search_query_es_list
                            logging.info(f'------- update es data -------{esid}')
                            es_utils.update(ESIndex.DRUG_PATENT_GOOGLE, d=update_es_dict)
                        else:
                            logging.info(f'当前数据不存在es，可能出现异常：{esid} ')

                    file_utils.write_file(file_name='/root/xiaowen.txt', data_type='a', content=json.dumps(es_dict).encode('utf-8').decode('unicode_escape'))

def init_date(self):
    year_list = []
    for year in range(1990, self.date_utils.custom_year(timestamp=self.date_utils.get_timestamp())):
        year_list.append(f'{year}-01-01')
    return year_list

def product_esid(self, publication_spider_comb):
    publication_docdb_country = publication_spider_comb[0:2]
    publication_docdb_number = publication_spider_comb[2:]
    publication_docdb_kind_list = self.str_utils.get_en_start(str=publication_docdb_number)
    publication_docdb_kind = ''
    if len(publication_docdb_kind_list) > 0:
        publication_docdb_kind = publication_docdb_kind_list[0]
        publication_docdb_number = publication_docdb_number.replace(publication_docdb_kind, '')
    return self.md5_utils.get_md5(data=f'{publication_docdb_country.strip()}|{publication_docdb_number.strip()}|{publication_docdb_kind.strip()}').lstrip('0')

def date_calculation(self, total_num_pages, meta):
    date_list = []
    name = meta['name']
    type = meta['type']
    source_id_list = meta['source_id_list']
    date_range = meta['date_range']
    source_es_index = meta['source_es_index']
    is_calculation = meta['is_calculation']
    if total_num_pages >9 and is_calculation:
        if ':' not in date_range:
            meta['date_range'] = date_range + ':' + date_range.split('-')[0] + '-01-01'
            meta['is_add_all_year'] = True
            date_list.append(meta)
        else:
            date_splits = date_range.split(':')[0].split('-')
            year = int(date_splits[0])
            month = int(date_splits[1])
            half_month = int(month/2)
            after_half_month = int(date_range.split(':')[1].split('-')[1])
            after_year = int(date_range.split(':')[1].split('-')[0])
            month_abs = abs(month - int(date_range.split(':')[1].split('-')[1]))
            if half_month > 0 and half_month != after_half_month and month_abs>1 and year == after_year:
                meta['date_range'] = f'{date_range.split(":")[0]}:{year}-{half_month}-01'
                meta['is_add_all_year'] = True
                date_list.append(meta)
            elif half_month > 0 and half_month == after_half_month and month_abs>1 and year == after_year:
                for month_index in range(1, month+1):
                    meta_dict = {}
                    if month_index+1 == 13:
                        meta_dict['date_range'] = f'{year}-{month_index}-01:{year+1}-01-01'
                    else:
                        meta_dict['date_range'] = f'{year}-{month_index}-01:{year}-{month_index+1}-01'
                    meta_dict['type'] = type
                    meta_dict['name'] = name
                    meta_dict['source_id_list'] = source_id_list
                    meta_dict['source_es_index'] = source_es_index
                    meta_dict['is_calculation'] = True
                    meta_dict['is_add_all_year'] = True
                    date_list.append(meta_dict)
            else:
                day_max = self.date_utils.get_month_range(year=year, month=month)
                for day in range(1, day_max+1):
                    meta_dict = {}
                    meta_dict['type'] = type
                    meta_dict['name'] = name
                    meta_dict['source_id_list'] = source_id_list
                    meta_dict['source_es_index'] = source_es_index
                    meta_dict['is_calculation'] = False
                    meta_dict['is_add_all_year'] = True
                    meta_dict['date_range'] = f'{year}-{month}-{day}:{year}-{month}-{day}'
                    date_list.append(meta_dict)
    return date_list