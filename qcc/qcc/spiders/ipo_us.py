
import ast
import json
import logging
import os
import scrapy
from qcc import run_env
from qcc.utils import pdf_utils, file_utils, common_utils, send_email_utils
from qcc.spiders.const import ESIndex, RedisKey, MongoTables
from qcc.utils import es_utils, qiniu_utils
from pyquery import PyQuery as pq
from qcc.spiders import const
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from qcc.utils.date_utils import DateUtils
from qcc.utils.es_utils import Query, QueryType
from qcc.utils.file_utils import DownloadFile
from qcc.utils.md5_utils import MD5Utils
from qcc.utils.mongo_utils import MongoUtils
from qcc.utils.send_email_utils import SendEmail
from qcc.utils.str_utils import StrUtils

'''
美国库：
 * 列表页：https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm
 * 详情页：https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=017377  meta={'source': 'us', }
橙皮书：
 * 列表页：https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm
 * 详情页：https://www.accessdata.fda.gov/scripts/cder/ob/results_product.cfm?Appl_Type=N&Appl_No=205858  meta={'source': 'orange', }
 
'''


def clean_data(base_info_dict):
    for key in base_info_dict.keys():
        if  None == base_info_dict[key] or '' == base_info_dict[key]:
            continue
        if type(base_info_dict[key]) != str:
            continue
        base_info_dict[key] = base_info_dict[key].replace('\r\n', '').strip()
    return base_info_dict


def update_drugs_join_data(self, esid, label_list, supplement_list, original_approvals_list, status):
    es_dict = {}
    es_dict['esid'] = esid
    es_dict['label_arr'] = str(json.dumps(label_list).encode('utf-8').decode('unicode_escape'))
    es_dict['supplement'] = str(json.dumps(supplement_list).encode('utf-8').decode('unicode_escape'))
    es_dict['original_approvals'] = str(json.dumps(original_approvals_list).encode('utf-8').decode('unicode_escape'))
    if 'update' == status:
        logging.info(f'------- 更新美国库PDF label_arr、supplement、original_approvals  -------{esid}')
        self.es_utils.update(ESIndex.DRUG_US_DRUGS, d=es_dict)
    else:
        logging.info(f'------- 新增美国库PDF label_arr、supplement、original_approvals  -------{esid}')
        self.es_utils.insert_or_replace(ESIndex.DRUG_US_DRUGS, d=es_dict)


def append_wait_orange_url(self, sponsor_applicant, scrapy):
    formdata = {}
    formdata['sponsor_applicant'] = sponsor_applicant
    formdata['discontinued'] = 'RX,OTC,DISCN'
    formdata['submit'] = 'Search'
    logging.info(f'追加橙皮书待采集的公司名称：{sponsor_applicant}')
    yield scrapy.FormRequest('https://www.accessdata.fda.gov/scripts/cder/ob/search_product.cfm', formdata=formdata,
                             callback=self.parse,
                             meta={'source': 'orange_company', 'sponsor_applicant': sponsor_applicant},
                             headers=const.headers)

class IpoUsSpider(scrapy.Spider):
    name = 'ipo_us'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.es_utils = es_utils
        self.pdf_utils = pdf_utils
        self.file_utils = file_utils
        self.str_utils = StrUtils()
        self.date_utils = DateUtils()
        self.md5_utils = MD5Utils()
        self.mongo_utils = MongoUtils()
        self.send_email_drugs_review = []
        self.send_email_utils = SendEmail()
        self.redis_server = from_settings(get_project_settings())
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        meta = response.meta
        doc = pq(response.text)
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            url = f'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo=213661'
            yield scrapy.Request(url, callback=self.parse, meta={'source': 'us', }, headers=const.headers)


            """
            url = f'https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm'
            yield scrapy.Request(url, callback=self.parse, meta={'source': 'orange_title', }, headers=const.headers)

            for a in range(ord('A'), ord('Z') + 1):
                url = f'https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=browseByLetter.page&productLetter={chr(a)}'
                yield scrapy.Request(url, callback=self.parse, meta={'source': 'us_title', }, headers=const.headers)
            """

        if 'source' in meta and 'orange_title' == meta['source']:
            option_elements = doc('#chosen')('option')
            for option_element in option_elements.items():
                sponsor_applicant = option_element.attr('value')
                yield from append_wait_orange_url(self, sponsor_applicant, scrapy)

            pages = self.es_utils.get_page(ESIndex.DRUG_US_DRUGS, page_size=-1, show_fields=['spider_company'])
            for page in pages:
                if 'spider_company' not in page:
                    continue
                spider_company = page['spider_company']
                yield from append_wait_orange_url(self, spider_company, scrapy)


        if 'source' in meta and 'orange_company' == meta['source']:
            tr_elements = doc('#example')('tbody')('tr')
            for tr_element in tr_elements.items():
               a_element = pq(tr_element('td')[3])('a')
               application_num = a_element.text()
               logging.info(f'追加待采集橙皮书详情页数据：{application_num}')
               url = 'https://www.accessdata.fda.gov/scripts/cder/ob/'+a_element.attr('href')
               yield scrapy.Request(url, callback=self.parse, meta={'source': 'orange', }, headers=const.headers)

        if 'source' in meta and 'orange_patent' == meta['source']:
            product_no = response.meta['product_no']
            application_num = response.meta['application_num']
            patent_list = []
            for patent_elment in doc('#example0 tbody tr').items():
                if 'no unexpired patent' not in patent_elment.text():
                    td_elements = patent_elment('td')
                    product_no = td_elements[0].text
                    patent_no = td_elements[1].text
                    patent_expiration = td_elements[2].text
                    drug_substance_claim = td_elements[3].text
                    drug_product_claim = td_elements[4].text
                    temp = pq( td_elements[5])
                    temp('span').remove()
                    patent_use_code = temp.text().replace('\n' , ' ')
                    delist_requested = td_elements[6].text
                    submission_date = td_elements[7].text
                    patent_dict = {}
                    patent_dict['product_no'] = product_no
                    patent_dict['patent_no'] = patent_no
                    patent_dict['patent_expiration'] = patent_expiration
                    patent_dict['drug_substance_claim'] = drug_substance_claim
                    patent_dict['drug_product_claim'] = drug_product_claim
                    patent_dict['product_no'] = product_no
                    patent_dict['patent_use_code'] = patent_use_code
                    patent_dict['delist_requested'] = delist_requested
                    patent_dict['submission_date'] = submission_date
                    patent_list.append(patent_dict)

            exclusivity_list = []
            for exclusivity_elment in doc('#example1 tbody tr').items():
                if 'no unexpired exclusivity' not in exclusivity_elment.text():
                    td_elements = exclusivity_elment('td')
                    product_no = td_elements[0].text
                    temp = pq(td_elements[1])
                    temp('span').remove()
                    exclusivity_code = temp.text().replace('\n' , ' ')
                    exclusivity_expiration = td_elements[2].text
                    exclusivity_dict = {}
                    exclusivity_dict['product_no'] = product_no
                    exclusivity_dict['exclusivity_code'] = exclusivity_code
                    exclusivity_dict['exclusivity_expiration'] = exclusivity_expiration
                    exclusivity_list.append(exclusivity_dict)

            if len(exclusivity_list) >0 or len(patent_list) >0:
                patent_obj = {}
                patent_obj['product_no'] = product_no
                patent_obj['application_num'] = application_num
                patent_obj['exclusivity_data'] = exclusivity_list
                patent_obj['patent_data'] = patent_list
                logging.info(f'存储橙皮书专利的信息：{application_num}')
                self.file_utils.write_file(file_name=const.STORE_PATH+ESIndex.DRUG_US_ORANGE+'.txt', data_type='a', content=json.dumps(patent_obj).encode('utf-8').decode('unicode_escape'))

        if 'source' in meta and 'orange' == meta['source']:
            content_elements = doc('.ui-accordion-content')
            if len(content_elements) == 0:
                logging.info(f'当前橙皮书页面数据无效，被过滤：{spider_url}')
                return
            spider_company = ''
            application_type = ''
            application_type_elements = doc('.search-title')
            base_info_list = []
            dosage_form_set = set()
            active_ingredient_set = set()
            if len(application_type_elements) >0:
                application_type = application_type_elements.text().split(' ')[3].strip()
            for content_element in content_elements.items():
                elements = content_element('p')
                if len(elements) == 0:
                    elements = content_element('div')
                content_dict = {}
                splits = elements.html().split('<br/>')
                for split in splits:
                    split_doc = pq(split)
                    if len(split_doc('a'))>0:
                        content_dict['href'] = 'https://www.accessdata.fda.gov/scripts/cder/ob/'+split_doc('a').attr('href')
                        continue
                    key = self.str_utils.remove_mark(str=pq(split)('strong').text().lower())
                    split_doc('strong').remove()
                    if split_doc('strong').size()>0:
                        content_dict[key] = ''
                        continue
                    value = split_doc.text().replace('\r\n', '').strip()
                    content_dict[key] = value
                active_ingredient = content_dict['activeingredient']
                proprietary_name = content_dict['proprietaryname']
                dosage_form_str = content_dict['dosageformrouteofadministration']
                splits = dosage_form_str.split(';')
                route = ''
                dosage_form = splits[0]
                dosage_form_set.add(dosage_form)
                active_ingredient_set.add(active_ingredient)
                if len(splits) > 1:
                    route = splits[1].strip()
                strength = content_dict['strength']
                reference_listed_drug = content_dict['referencelisteddrug']
                reference_standard = 'Yes'
                if 'yes' not in content_dict['referencestandard'].lower():
                    reference_standard = 'No'
                te_code = content_dict['tecode']
                application_num = self.str_utils.get_num(content_dict['applicationnumber'])[0]
                product_no = content_dict['productnumber']
                approval_date = self.date_utils.unix_time_en(date_str=content_dict['approvaldate'])
                spider_company = content_dict['applicantholderfullname']
                marketing_status = content_dict['marketingstatus']
                if 'href' in content_dict:
                    href = content_dict['href']
                    if not href.endswith('.cfm'):
                        yield scrapy.Request(href, callback=self.parse, meta={'source': 'orange_patent', 'application_num': application_num, 'product_no': product_no, }, headers=const.headers)
                spider_inn_formulation = active_ingredient+'|'+dosage_form
                base_info_dict = {}
                base_info_dict['product_no'] = product_no
                base_info_dict['spider_company'] = spider_company
                base_info_dict['active_ingredient'] = active_ingredient
                base_info_dict['proprietary_name'] = proprietary_name
                base_info_dict['dosage_form'] = dosage_form
                base_info_dict['route'] = route
                base_info_dict['strength'] = strength
                base_info_dict['spider_inn_formulation'] = spider_inn_formulation
                base_info_dict['reference_listed_drug'] = reference_listed_drug
                base_info_dict['reference_standard'] = reference_standard
                base_info_dict['te_code'] = te_code
                if None != approval_date:
                    base_info_dict['approval_date'] = approval_date
                base_info_dict['marketing_status'] = marketing_status
                base_info_list.append(base_info_dict)
            md5 = self.md5_utils.get_md5(data=base_info_list)
            base_info_obj = {}
            base_info_obj['md5'] = md5
            base_info_obj['url'] = spider_url
            base_info_obj['application_num'] = application_num
            base_info_obj['spider_company'] = spider_company
            base_info_obj['application_type'] = application_type
            base_info_obj['base_info'] = base_info_list
            base_info_obj['active_ingredient'] = ';'.join(active_ingredient_set)
            base_info_obj['dosage_form'] = ';'.join(dosage_form_set)
            logging.info(f'存储橙皮书基本信息：{application_num}')
            self.file_utils.write_file(file_name=const.STORE_PATH+ESIndex.DRUG_US_ORANGE+'.txt', data_type='a', content=json.dumps(base_info_obj).encode('utf-8').decode('unicode_escape'))

        if 'source' in meta and 'us_title' == meta['source']:  # 美国库-列表页
            for a_element in doc('tbody li a').items():
                href = 'https://www.accessdata.fda.gov'+a_element.attr('href')
                yield scrapy.Request(href, callback=self.parse, meta={'source': 'us', }, headers=const.headers)

        if 'source' in meta and 'us' == meta['source']: #美国库
            accordion_elements = doc('#accordion')
            appl_details_elements = accordion_elements('span.appl-details-top')
            if appl_details_elements.size() == 0 and 'index.cfm' in spider_url:
                logging.info(f'当前页面无效，被过滤: {spider_url}')
                return
            application_num = appl_details_elements[0].text #申请号
            if self.str_utils.is_blank(application_num):
                logging.info(f'获取的申请号为空，视为无效，被过滤：{spider_url}')
                return

            pages = es_utils.get_page('drug_us_drugs', page_size=-1,queries=Query(QueryType.EQ, 'application_num', application_num,), show_fields=['original_approvals', 'supplement', 'label_arr','md5'])

            application_type = '' #申请类型
            application_type_str = accordion_elements('strong:nth-child(1)').text() #获取第一个节点
            application_type_list = self.str_utils.get_parentheses_str(str=application_type_str)
            if len(application_type_list) > 0 :
                application_type = application_type_list[0]
            spider_company = appl_details_elements[1].text  #申请机构

            original_approvals_list = []
            original_approvals_id_set = set()
            approval_date_revised = 0 #批准日期(默认值不传)
            extract_data_dict = {}
            original_approvals_elements = doc('#exampleApplOrig') #Original Approvals or Tentative Approvals
            if original_approvals_elements.size() > 0:
                for tr_element in original_approvals_elements('tr').items():
                    td_elements = tr_element('td')
                    if len(td_elements) == 0:
                        continue
                    action_date_str = td_elements[0].text.replace('    ', '').strip()
                    action_date = self.date_utils.unix_defined_format(date_str=td_elements[0].text, format='%m/%d/%Y')#执行日期(转换时间戳异常则过滤)
                    submission = td_elements[1].text.replace('    ', '').strip() #意见
                    action_type = td_elements[2].text.replace('    ', '').strip() #批准类型
                    submission_classification = td_elements[3].text.replace('    ', '').strip() #意见分类
                    rPOS = td_elements[4].text.replace('    ', '').strip() #优先审评 / 孤儿药状态
                    a_elements = pq(td_elements[5])('a')
                    id = self.md5_utils.get_md5(action_date_str + submission + action_type)
                    original_approvals_id_set.add(id)
                    lrlppi_list, file_name_set = yield from parse_download_pdf(self, id, a_elements, application_num, meta, scrapy, 'original_approvals')
                    notes = td_elements[6].text.replace('    ', '').strip()  # 优先审评 / 孤儿药状态
                    if 'approval' == action_type.lower(): #申请日期：取action_type等于approval且为最小的值
                        if None != action_date and approval_date_revised < action_date:
                            approval_date_revised = action_date
                            extract_data_dict['rPOS'] = rPOS
                            extract_data_dict['submission'] = submission
                            extract_data_dict['action_type'] = action_type
                            extract_data_dict['submission_classification'] = submission_classification
                    original_approvals_dict = {}
                    original_approvals_dict['id'] = id
                    if None != action_date:
                        original_approvals_dict['action_date'] = action_date
                    original_approvals_dict['submission'] = submission
                    original_approvals_dict['action_type'] = action_type
                    original_approvals_dict['submission_classification'] = submission_classification
                    original_approvals_dict['rPOS'] = rPOS
                    original_approvals_dict['lrlppi'] = lrlppi_list
                    original_approvals_dict['notes'] = notes
                    original_approvals_list.append(original_approvals_dict)

            original_approvals_list = join_es_data(pages, original_approvals_list, original_approvals_id_set,'original_approvals')
            supplement_list = []
            supplement_list_id_set = set()
            supplement_elements = doc('#exampleApplSuppl')  # Supplements
            if supplement_elements.size() > 0:
                for tr_element in supplement_elements('tr').items():
                    td_elements = tr_element('td')
                    if len(td_elements) == 0:
                        continue
                    action_date_str = td_elements[0].text.replace('    ', '').strip()
                    action_date = self.date_utils.unix_defined_format(date_str=td_elements[0].text, format='%m/%d/%Y')
                    submission = td_elements[1].text.replace('    ', '').strip()
                    submission_classification = td_elements[2].text.replace('    ', '').strip()
                    id = self.md5_utils.get_md5(action_date_str + submission + submission_classification)
                    supplement_list_id_set.add(id)
                    a_elements = pq(td_elements[3])('a')
                    lrlppi_list, file_name_set = yield from parse_download_pdf(self, id, a_elements, application_num, meta, scrapy, 'supplement')
                    note = td_elements[4].text.replace('    ', '').strip()
                    supplements_dict = {}
                    supplements_dict['id'] = id
                    supplements_dict['note'] = note
                    if None != action_date:
                        supplements_dict['action_date'] = action_date
                    supplements_dict['lrlppi'] = lrlppi_list
                    supplements_dict['submission'] = submission
                    supplements_dict['submission_classification'] = submission_classification
                    supplement_list.append(supplements_dict)

            label_list = []
            label_id_set = set()
            label_elements = doc('#examplelabel')  # label for BLA 125554
            if label_elements.size()==0:
                label_elements = doc('#exampleLabels')
            if label_elements.size() > 0:
                for tr_element in label_elements('tr').items():
                    td_elements = tr_element('td')
                    if len(td_elements) == 0:
                        continue
                    action_date_str = td_elements[0].text.replace('    ', '').strip()
                    action_date = self.date_utils.unix_defined_format(date_str=td_elements[0].text, format='%m/%d/%Y')
                    submission = td_elements[1].text.replace('    ', '').strip()
                    submission_classification_approvaltype = td_elements[2].text.replace('    ', '').strip()
                    id = self.md5_utils.get_md5(action_date_str + submission + submission_classification_approvaltype)
                    label_id_set.add(id)
                    a_elements = pq(td_elements[3])('a')
                    lrlppi_list, file_name_set = yield from parse_download_pdf(self, id, a_elements, application_num, meta, scrapy, 'label_arr')
                    note = td_elements[4].text.replace('    ', '').strip()
                    label_dict = {}
                    label_dict['id'] = id
                    label_dict['note'] = note
                    label_dict['submission'] = submission
                    if None != action_date:
                        label_dict['action_date'] = action_date
                    label_dict['lrlppi'] = lrlppi_list
                    label_dict['submission_classification_approvaltype'] = submission_classification_approvaltype
                    label_list.append(label_dict)

            #组装历史数据 + 当前采集数据
            original_approvals_list = join_es_data(pages, original_approvals_list, original_approvals_id_set, 'original_approvals')
            supplement_list = join_es_data(pages, supplement_list, supplement_list_id_set, 'supplement')
            label_list = join_es_data(pages, label_list, label_id_set, 'label_arr')

            if None != pages:
                for page in pages:
                    esid = page['esid']
                    update_drugs_join_data(self, esid, label_list, supplement_list, original_approvals_list, 'update')
            else: #新增数据
                update_drugs_join_data(self, self.md5_utils.get_md5(data=application_num), label_list, supplement_list, original_approvals_list, 'create')

            base_info_list = []
            dosage_form_set = set()
            active_ingredient_set = set()
            for base_info_element in doc('tr.prodBoldText').items():
                td_elements = base_info_element('td')
                proprietary_name = pq(td_elements[0]).text() #药物名称
                active_ingredient = pq(td_elements[1]).text() #活性成分
                strength = pq(td_elements[2]).text() #规格
                dosage_form_route = pq(td_elements[3]).text() #剂型/给药途径
                route = ''
                dosage_form = '' #剂型
                if ';' in dosage_form_route:
                    dosage_form = dosage_form_route.split(';')[0]
                    route = dosage_form_route.split(';')[1]
                else:
                    dosage_form = dosage_form_route
                dosage_form_set.add(dosage_form)
                active_ingredient_set.add(active_ingredient)
                marketing_status = pq(td_elements[4]).text()  # 剂型/给药途径
                te_code = pq(td_elements[5]).text()
                reference_listed_drug = pq(td_elements[6]).text()
                if self.str_utils.is_blank(reference_listed_drug):
                    reference_listed_drug = 'No'
                reference_standard =pq(td_elements[7]).text()
                spider_inn_formulation = active_ingredient+'|'+dosage_form
                base_info_dict = {}
                base_info_dict['proprietary_name'] = proprietary_name
                base_info_dict['active_ingredient'] = active_ingredient
                base_info_dict['strength'] = strength
                base_info_dict['dosage_form'] = dosage_form
                base_info_dict['spider_inn_formulation'] = spider_inn_formulation
                base_info_dict['route'] = route
                base_info_dict['marketing_status'] = marketing_status
                base_info_dict['te_code'] = te_code
                base_info_dict['reference_listed_drug'] = reference_listed_drug
                base_info_dict['reference_standard'] = reference_standard
                base_info_dict['spider_company'] = spider_company
                base_info_list.append(clean_data(base_info_dict))

            spider_wormtime = self.date_utils.get_timestamp()
            md5 = self.md5_utils.get_md5(data=str(base_info_list))
            redis_dict = {}
            redis_dict['md5'] = md5
            redis_dict['base_info'] = str(base_info_list)
            redis_dict['active_ingredient'] = ';'.join(active_ingredient_set)
            redis_dict['dosage_form'] = ';'.join(dosage_form_set)
            redis_dict['application_num'] = application_num
            redis_dict['application_type'] = application_type
            redis_dict['spider_wormtime'] = spider_wormtime
            redis_dict['approval_date'] = approval_date_revised
            redis_dict['rPOS'] = extract_data_dict.get('rPOS', None)
            redis_dict['submission'] = extract_data_dict.get('submission', None)
            redis_dict['action_type'] = extract_data_dict.get('action_type', None)
            redis_dict['submission_classification'] = extract_data_dict.get('submission_classification', None)
            redis_dict['url'] = spider_url
            redis_dict['spider_company'] = spider_company
            redis_dict['base_info'] = base_info_list
            type = '新增'
            esid = self.md5_utils.get_md5(data=application_num)
            if None != pages:
                if md5 != pages[0]['md5']:
                    type = '修改'
                else:
                    logging.info(f'当前申请号基本信息未发生变更，被过滤：{application_num}')
                    return
            redis_obj = {}
            redis_obj['id'] = esid
            redis_obj['type'] = type
            redis_obj['collection'] = ''
            redis_obj['datestamp'] = spider_wormtime
            redis_obj['table'] = ESIndex.DRUG_US_DRUGS
            redis_obj['content'] = clean_data(redis_dict)
            logging.info(f'------- 美国库 redis data {type} -------{application_num}')
            self.redis_server.lpush(RedisKey.DATA_CLEAN_US, json.dumps(redis_obj).encode('utf-8').decode('unicode_escape'))

        if 'source' in meta and 'review' == meta['source']:  # 美国库
            id = meta['id']
            local_web = meta['local_web']
            application_num = meta['application_num']
            url_prefix = spider_url[:spider_url.rindex('/')+1]
            for a_element in doc('a').items():
                url = a_element.attr('href')
                if None == a_element.attr('href'):
                    continue
                elif not url.lower().endswith('.pdf'):
                    continue
                elif not url.startswith('http'):
                    url = url_prefix + a_element.attr('href')
                a_element.attr('href', url)
            a_elements = doc('#user_provided li a')
            review_list, file_name_set = yield from parse_download_pdf(self, id, a_elements, application_num, meta, scrapy, '')
            pages = self.es_utils.get_page(ESIndex.DRUG_US_DRUGS, queries=Query(QueryType.EQ, 'application_num', application_num), show_fields=[local_web])
            for page in pages:
                esid = page['esid']
                local_es_list = ast.literal_eval(page[local_web])
                for local_es in local_es_list:
                    id_es = local_es['id']
                    if id != id_es:
                        continue
                    local_es_list.remove(local_es)
                    if 'review' in local_es:
                        review_es_list = local_es['review']
                        for review_es in review_es_list:
                            if review_es['file_name'] not in file_name_set:
                                file_name_set.add(review_es['file_name'])
                                review_list.append(review_es)
                    local_es['review'] = review_list
                    local_es_list.append(local_es)
                es_dict = {}
                es_dict['esid'] = esid
                es_dict[local_web] = str(json.dumps(local_es_list).encode('utf-8').decode('unicode_escape'))
                logging.info(f'------- update es data -------{esid} {local_web} review 值!')
                self.es_utils.update(ESIndex.DRUG_US_DRUGS, d=es_dict)

    def close(spider, reason):
        logging.info('------- 美国库和橙皮书数据采集完毕 -------')
        if len(spider.send_email_drugs_review)>0:
            send_content = ''
            for send_email_drugs_review in spider.send_email_drugs_review:
                id = send_email_drugs_review['id']
                local_web = send_email_drugs_review['local_web']
                application_num = send_email_drugs_review['application_num']
                send_content = "<tr><td>" + application_num + "</td><td>" + local_web + "</td><td>" + id + "</td></tr>"
            send_content = "<table border=\"1\"><tr><th>application_num</th><th>field_type</th><th>id</th>" + send_content + "</tr></table>"
            query = {'send_project_list.send_project_name': 'ipo_us'}
            receiver = common_utils.get_send_email_receiver(query=query)
            spider.send_email_utils.send_email_content(content=send_content, receiver=receiver, subject='美国上市药品review文件需翻墙获取')

        content_obj = {}
        local_file_path = const.STORE_PATH + ESIndex.DRUG_US_ORANGE + '.txt'
        if os.path.exists(local_file_path):
            logging.info('------- 开始传输橙皮书的数据 -------')
            with open(file=const.STORE_PATH + ESIndex.DRUG_US_ORANGE + '.txt', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    line_dict = ast.literal_eval(line.replace('null', 'None'))
                    application_num = line_dict['application_num']
                    if 'base_info' in line_dict:
                        content_obj[application_num] = line_dict
                    else:
                        join_orange_data(application_num, line_dict, 'patent_data', content_obj)
                        join_orange_data(application_num, line_dict, 'exclusivity_data', content_obj)
        content_es_obj = {}
        pages = spider.es_utils.get_page(ESIndex.DRUG_US_ORANGE, page_size=-1, show_fields=['patent_data', 'exclusivity_data', 'md5', 'patent_data_md5', 'exclusivity_data_md5', 'application_num'])
        for page in pages:
            application_num = page['application_num']
            content_es_obj[application_num] = page

        send_email_orange_content = []
        for application_num in content_obj.keys():
            type = '新增'
            is_send_redis = False
            if application_num in content_es_obj:
                value_dict = content_obj[application_num]
                if application_num in content_es_obj:
                    value_es_dict = content_es_obj[application_num]
                    patent_data_md5 = spider.md5_utils.get_md5(data=value_dict.get('patent_data', []))
                    exclusivity_data_md5 = spider.md5_utils.get_md5(data=value_dict.get('exclusivity_data', []))
                    if value_dict['md5'] != value_es_dict['md5']:
                        type = '修改'
                        is_send_redis = True
                    elif value_es_dict['patent_data_md5'] != patent_data_md5:
                        type = '修改'
                        is_send_redis = True
                    elif value_es_dict['exclusivity_data_md5'] != exclusivity_data_md5:
                        type = '修改'
                        is_send_redis = True
                    join_orange_and_es_data(spider, send_email_orange_content, application_num, content_obj, value_dict, value_es_dict, 'patent_data', 'patent_no', 'product_no')
                    join_orange_and_es_data(spider, send_email_orange_content, application_num, content_obj, value_dict, value_es_dict, 'exclusivity_data', 'exclusivity_code', 'product_no')
            if not is_send_redis:
                logging.info(f'当前橙皮书未发生变更，被过滤：{application_num}')
                continue
            spider_wormtime = spider.date_utils.get_timestamp()
            redis_obj = {}
            redis_obj['type'] = type
            redis_obj['collection'] = ''
            value_dict['spider_wormtime'] = spider_wormtime
            value_dict['patent_data_md5'] = patent_data_md5
            value_dict['exclusivity_data_md5'] = exclusivity_data_md5
            redis_obj['content'] = value_dict
            redis_obj['datestamp'] = spider_wormtime
            redis_obj['table'] = ESIndex.DRUG_US_ORANGE
            redis_obj['id'] = content_es_obj[application_num]['esid']
            logging.info(f'橙皮书数据: {type} {application_num}')
            spider.redis_server.lpush(RedisKey.DATA_CLEAN_US, json.dumps(redis_obj).encode('utf-8').decode('unicode_escape'))

        if len(send_email_orange_content) >0:
            send_orange_content = ''
            for send_email_orange in send_email_orange_content:
                patent_no = send_email_orange['patent_no']
                product_no = send_email_orange['product_no']
                application_num = send_email_orange['application_num']
                send_orange_content += "<tr><td>" + application_num + "</td><td>" + product_no + "</td><td>" + patent_no + "</td><td>" + spider.date_utils.defined_format_time(timestamp = spider.date_utils.get_timestamp(), format='%Y-%m-%d') + "</td></tr>";
            send_content =  "<table border=\"1\"><tr><th>application_num</th><th>product_no</th><th>patent_no</th><th>spider_wormtime</th>"+send_orange_content+"</tr></table>"
            query = {'send_project_list.send_project_name': 'ipo_orange'}
            receiver = common_utils.get_send_email_receiver(query=query)
            spider.send_email_utils.send_email_content(content=send_content, receiver=receiver, subject='桔皮书专利新增')

        #todo 全量测试完成之后要开启删除文件方式
        # os.remove(local_file_path)


def join_orange_and_es_data(spider, send_email_orange_content, application_num, content_obj, value_dict, value_es_dict, filed_1, filed_2, filed_3):
    value_dict_list = value_dict.get(filed_1, [])
    value_es_dict_list = value_es_dict.get(filed_1, [])
    product_no_set = set()
    patent_data_add_set = set()
    for patent_data_es in value_es_dict_list:
        patent_data_add_set.add(patent_data_es[filed_2] + patent_data_es[filed_3])

    for patent_data in value_dict_list:
        id = patent_data[filed_2]+patent_data[filed_3]
        if id not in patent_data_add_set and 'patent_data' == filed_1: #发送邮件通知晓文
            send_email_orange_dict = {}
            send_email_orange_dict[filed_2] = patent_data[filed_2]
            send_email_orange_dict[filed_3] = patent_data[filed_3]
            send_email_orange_dict['application_num'] = application_num
            send_email_orange_content.append(send_email_orange_dict)
        product_no_set.add(id)

    for patent_data_es in value_es_dict_list:
        if (patent_data_es[filed_2]+patent_data_es[filed_3]) in product_no_set:
            continue
        expiration_date = spider.date_utils.get_timestamp()
        patent_data_es['expiration_date'] = expiration_date
        value_dict_list.append(patent_data_es)
    value_dict[filed_1] = value_dict_list
    content_obj[application_num] = value_dict

def join_orange_data(application_num, lines, filed, content_obj):
    #判断过期日期
    if filed in lines:
        patent_data = lines[filed]
        dict = content_obj[application_num]
        if filed not in dict:
            dict[filed] = lines[filed]
        else:
            patent_data_list = dict[filed]
            patent_data_list.extend(patent_data)
            dict[filed] = patent_data_list
    return content_obj

def join_es_data(pages, original_approvals_list, original_approvals_id_set, filed):
    join_data = []
    if pages != None:
        if filed in pages[0]:
            join_data.extend(original_approvals_list)
            original_approvals_es_list = ast.literal_eval(pages[0][filed])
            for original_approvals_es in original_approvals_es_list:
                id_es = original_approvals_es['id']
                if id_es not in original_approvals_id_set:  # 补充官网已删除的历史数据 lrlppi
                    original_approvals_list.append(original_approvals_es)
                    join_data.append(original_approvals_es)

            for original_approvals in original_approvals_list: #补充 lrlppi 中的数据
                id = original_approvals['id']
                for original_approvals_es in original_approvals_es_list:
                    id_es = original_approvals_es['id']
                    if id_es != id:
                        continue
                    if 'lrlppi' not in original_approvals and 'lrlppi' in original_approvals_es:
                        join_data.remove(original_approvals)
                        original_approvals['lrlppi'] = original_approvals_es['lrlppi']
                        join_data.append(original_approvals)
                    elif 'lrlppi' in original_approvals and 'lrlppi' in original_approvals_es:
                        lrlppi_list = original_approvals['lrlppi']
                        lrlppi_es_list = original_approvals_es['lrlppi']
                        for lrlppi_es in lrlppi_es_list:
                            for key_es in lrlppi_es.keys():
                                is_exsited = False
                                for lrlppi in lrlppi_list:
                                    for key in lrlppi.keys():
                                        if key_es == key:
                                            is_exsited = True
                                if not is_exsited:
                                    lrlppi_list.append(lrlppi_es)
                                    join_data.remove(original_approvals)
                                    original_approvals['lrlppi'] = lrlppi_list
                                    join_data.append(original_approvals)
    else:
        join_data.extend(original_approvals_list)
    return join_data


# 处理下载PDF文件
def parse_download_pdf(self, id, a_elements, application_num, meta, scrapy, field):
    lrlppi_list = []
    file_name_set = set()
    if len(a_elements) > 0:
        for a_element in a_elements.items():
            file_name = a_element.text()
            file_name_set.add(file_name)
            file_name_lower = file_name.lower()
            file_name_url = a_element.attr('href')
            file_name_md5 = self.md5_utils.get_md5(data=file_name_url)
            if '.' in file_name_url:
                suffix = file_name_url[file_name_url.rindex('.'):]
                file_name_md5 += suffix
            # 文件不存在七牛云则重新下载文件
            file_dict = {}
            file_dict['orig_link'] = file_name_url
            qiniu_url = f'http://spider.pharmcube.com/{file_name_md5}'
            if not qiniu_utils.is_already_qiniu(qiniu_url):
                if 'review' != meta['source']:
                    file_dict[file_name] = file_name_url
                if file_name_url.endswith('.pdf'):
                    download_pdf_dict = {}
                    download_pdf_dict['file_url'] = file_name_url
                    download_pdf_dict['file_name'] = file_name_md5
                    DownloadFile().download_file(download_pdf_dict)
                    local_file_path = f'{const.STORE_PATH}{file_name_md5}'
                    if os.path.exists(local_file_path):#校验pdf是否有效
                        if self.pdf_utils.check_pdf(local_file_path):
                            qiniu_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_name_md5, is_keep_file=False)
                            if 'pharmcube' in qiniu_url:
                                if 'review' == meta['source']:
                                    file_dict['file_name'] = file_name
                                    file_dict['file_name_url'] = qiniu_url
                                else:
                                    file_dict[file_name] = qiniu_url
                elif 'review' == file_name_lower and 'review' != meta['source']:
                    meta = {'application_num': application_num, 'source': 'review', 'local_web': field, 'id': id}
                    if 'dev' == run_env.run_evn and file_name_url.startswith('https://web.archive.org'): #需要翻墙，借助VPN
                        yield scrapy.Request(file_name_url, callback=self.parse, meta=meta, headers=const.headers)
                    else: #发送邮件通知
                        self.send_email_drugs_review.append(meta)
                    continue
            elif 'review' == meta['source']:
                file_dict['file_name'] = file_name
                file_dict['file_name_url'] = qiniu_url
            else:
                file_dict[file_name] = qiniu_url
            lrlppi_list.append(file_dict)
    return lrlppi_list, file_name_set
