import json
import logging
import scrapy
import execjs
import time
from flash_news.utils import qiniu_utils
from flash_news.utils import pdf_utils
from flash_news.utils import es_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news.const import ESIndex,RedisKey
from flash_news.utils.es_utils import Query, QueryType
from flash_news.utils.file_utils import DownloadFile
from flash_news.utils.date_utils import DateUtils
'''
上海证券交易所——科创版股票审核：
tapd网址：https://www.tapd.cn/22397031/prong/stories/view/1122397031001001135
爬虫网址：http://kcb.sse.com.cn/disclosure/#
'''
class Doctor(scrapy.Spider):
    name = 'shanghai_kechuang'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    es_utils = es_utils
    pdf_utils = pdf_utils
    qiniu_utils = qiniu_utils
    file_utils = DownloadFile()
    mongo_utils = MongoUtils()
    md5_utils = MD5Utils()
    date_utils = DateUtils()
    redis_server = from_settings(get_project_settings())

    def parse(self, response):
        for page_index in range(1, 6):
            # print(page_index)
            time.sleep(0.1)
            url = f'http://query.sse.com.cn/commonSoaQuery.do?&isPagination=true&sqlId=GP_GPZCZ_SHXXPL&pageHelp.pageSize=20&pageHelp.pageNo={page_index}&fileType=30%2C5%2C6&_=1616838543482'
            data = {'Referer': 'http://kcb.sse.com.cn/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', }
            yield scrapy.Request(url=url, headers=data, callback=self.parses)

    def parses(self,response):
        res = json.loads(response.text)
        stock = res['pageHelp']['data']
        ss = set()
        for i in stock:
            id = i['stockAuditNum']
            ss.add(id)
        for j in ss:
            urll = "http://query.sse.com.cn/commonSoaQuery.do?&isPagination=true&sqlId=SH_XM_LB&stockAuditNum={}&_={}".format(j,str(int(time.time()) * 1000))
            header = {"Referer": "http://kcb.sse.com.cn/",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",}
            yield scrapy.Request(url=urll,headers=header,callback=self.parsel,meta={"auditId":j,"header":header})

    def parsel(self,response):
        auditId = response.meta["auditId"]
        # print('auditId',auditId)
        header = response.meta["header"]
        ress = json.loads(response.text)
        currStatus = ress['pageHelp']['data'][0]['currStatus']
        collectType = ress['pageHelp']['data'][0]['collectType']
        registeResult = ress['pageHelp']['data'][0]['registeResult']
        with open(r'kechuangban.js', encoding='UTF-8') as file:result = file.read()
        context1 = execjs.compile(result)
        approval_status = context1.call("status_transfer",{"currStatus": currStatus, "collectType": collectType,"registeResult": registeResult})# 审核状态
        spider_update_date = ress['pageHelp']['data'][0]['updateDate']
        timeArray = time.strptime(spider_update_date, "%Y%m%d%H%M%S")
        spider_update_date = int(time.mktime(timeArray)) * 1000# 更新日期
        company_name = ress['pageHelp']['data'][0]['stockAuditName']# 公司全称
        company_abbreviation = ress['pageHelp']['data'][0]['stockIssuer'][0]['s_issueCompanyAbbrName']# 公司简称
        accept_date_str = ress['result'][0]['auditApplyDate']# 受理日期
        timeArray = time.strptime(accept_date_str, "%Y%m%d%H%M%S")
        accept_date = int(time.mktime(timeArray)) * 1000# 受理日期
        financing_amount = ress['pageHelp']['data'][0]['planIssueCapital']
        financing_amount = round(financing_amount, 2)# 融资金额(亿元)
        sponsor_institution = ress['pageHelp']['data'][0]['intermediary'][0]['i_intermediaryName']# 保荐机构
        accounting_firm = ress['pageHelp']['data'][0]['intermediary'][1]['i_intermediaryName']# 会计师事务所
        law_office = ress['pageHelp']['data'][0]['intermediary'][2]['i_intermediaryName']# 律师事务所
        try:
            Assessment_agency = ress['pageHelp']['data'][0]['intermediary'][3]['i_intermediaryName']# 评估机构
        except:
            Assessment_agency = None
        spider_wormtime = int(time.time()) * 1000
        urls = "http://query.sse.com.cn/commonSoaQuery.do?&isPagination=false&sqlId=GP_GPZCZ_SHXXPL&stockAuditNum={}&_={}".format(auditId,str(int(time.time()) * 1000))
        time.sleep(1)
        yield scrapy.Request(url=urls,headers=header,callback=self.pages,meta={"approval_status":approval_status,"spider_update_date":spider_update_date,"company_name":company_name,"company_abbreviation":company_abbreviation,"accept_date_str":accept_date_str,"accept_date":accept_date,"financing_amount":financing_amount,"sponsor_institution":sponsor_institution,"accounting_firm":accounting_firm,"law_office":law_office,"Assessment_agency":Assessment_agency,"spider_wormtime":spider_wormtime,"auditId":auditId})

    def pages(self,reaponse):
        approval_status = reaponse.meta["approval_status"]
        spider_update_date = reaponse.meta["spider_update_date"]
        company_name = reaponse.meta["company_name"]
        company_abbreviation = reaponse.meta["company_abbreviation"]
        accept_date_str = reaponse.meta["accept_date_str"]
        accept_date = reaponse.meta["accept_date"]
        financing_amount = reaponse.meta["financing_amount"]
        sponsor_institution = reaponse.meta["sponsor_institution"]
        accounting_firm = reaponse.meta["accounting_firm"]
        law_office = reaponse.meta["law_office"]
        Assessment_agency = reaponse.meta["Assessment_agency"]
        spider_wormtime = reaponse.meta["spider_wormtime"]
        stock_audit_num = reaponse.meta["auditId"]
        spider_url = "http://kcb.sse.com.cn/renewal/xmxq/index.shtml?auditId="+stock_audit_num
        esid = self.md5_utils.get_md5(spider_url)
        resp = json.loads(reaponse.text)

        reveal_info = []
        inquiry = []
        # m = -1
        # while True:
        #     m += 1
        # 30改成动态
        for m in range(1,30):
            dic1 = {}
            dic2 = {}
            try:
                if '-' not in resp['result'][int(m)]['fileTitle']:
                    prospectus_declare_repprt = resp['result'][int(m)]['fileTitle']
                    if '招股说明书' in prospectus_declare_repprt:
                        reveal_file_type = '招股说明书'
                    if '发行保荐书' in prospectus_declare_repprt:
                        reveal_file_type = '发行保荐书'
                    if '上市保荐书' in prospectus_declare_repprt:
                        reveal_file_type = '上市保荐书'
                    if '审计报告' in prospectus_declare_repprt:
                        reveal_file_type = '审计报告'
                    if '法律意见书' in prospectus_declare_repprt:
                        reveal_file_type = '法律意见书'
                    else:
                        pass
                    prospectus_declare_repprt_time = resp['result'][int(m)]['publishDate']
                    timeArray = time.strptime(prospectus_declare_repprt_time, "%Y-%m-%d")
                    prospectus_declare_repprt_time = int(time.mktime(timeArray)) * 1000
                    prospectus_declare_repprt_pdf = 'http://static.sse.com.cn/stock' + resp['result'][int(m)]['filePath']
                    dic1["file_name"] = prospectus_declare_repprt + '.pdf'
                    dic1["file_url"] = prospectus_declare_repprt_pdf
                    dic1["update_date"] = prospectus_declare_repprt_time
                    dic1["reveal_file_type"] = reveal_file_type
                    self.file_utils.download_file(dic1)
                    file_url = dic1['file_url']
                    file_url = file_url[file_url.rfind("/") + 1:]
                    file_name = dic1['file_name']
                    local_file_path = f'{"E:/workspace/pharmcube-spider-platform/shijin/flash_news/flash_news/temporary_file/"}{file_name}'
                    self.pdf_utils.check_pdf(local_file_path)
                    qiniu_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_url, is_keep_file=False)
                    dic1["declare_repprt_url"] = qiniu_url
                    dic1["declare_repprt_name"] = prospectus_declare_repprt
                    dic1.pop('file_name')
                    dic1.pop('file_url')
                    # print(dic1)
                else:
                    file_namee = resp['result'][int(m)]['fileTitle']
                    file_name_url = 'http://static.sse.com.cn/stock' + resp['result'][int(m)]['filePath']
                    update_date = resp['result'][int(m)]['publishDate']
                    timeArray = time.strptime(update_date, "%Y-%m-%d")
                    update_date = int(time.mktime(timeArray)) * 1000
                    dic2["file_name"] = file_namee + '.pdf'
                    dic2["file_url"] = file_name_url
                    dic2["update_date"] = update_date
                    self.file_utils.download_file(dic2)
                    file_url = dic2['file_url']
                    file_url = file_url[file_url.rfind("/") + 1:]
                    file_name = dic2['file_name']
                    local_file_path = f'{"E:/workspace/pharmcube-spider-platform/shijin/flash_news/flash_news/temporary_file/"}{file_name}'
                    self.pdf_utils.check_pdf(local_file_path)
                    qiniu_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_url, is_keep_file=False)
                    dic2["file_name_url"] = qiniu_url
                    dic2["file_name"] = file_namee
                    dic2.pop('file_url')
                    # print(dic2)
            except:
                break
            reveal_info.append(dic1)
            inquiry.append(dic2)
        reveal_info = [i for i in reveal_info if i != {}]
        inquiry = [i for i in inquiry if i != {}]
        print(reveal_info)
        print(inquiry)
    #     # logging.info("------- insert es data -------" + esid + "\t" + company_name)
        pages = self.es_utils.get_page(ESIndex.STIB, queries=Query(QueryType.EQ, 'stock_audit_num', stock_audit_num), page_size=-1, show_fields=['approval_status','spider_update_date','spider_wormtime','spider_url'])
        print(pages)
        if None != pages:
            for page in pages:
                esid = page['esid']
                try:
                    page['spider_url']
                except:
                    continue
                if page['spider_update_date'] != spider_update_date or page['approval_status'] != approval_status:
                    update_es_dict = {}
                    print(esid)
                    update_es_dict['esid'] = esid
                    update_es_dict['approval_status'] = approval_status
                    update_es_dict['spider_update_date'] = spider_update_date
                    update_es_dict['reveal_info'] = reveal_info
                    update_es_dict['inquiry'] = inquiry
                    logging.info(f'------- update es data -------{esid} {spider_wormtime}')
                    # self.es_utils.update(ESIndex.STIB, d=update_es_dict)
                    # self.redis_server.lpush(RedisKey.STIB,json.dumps(update_es_dict).encode('utf-8').decode('unicode_escape'))
                else:
                    pass
        else:
            es_dict = {}
            es_dict["esid"] = esid
            es_dict["spider_url"] = spider_url
            es_dict["approval_status"] = approval_status
            es_dict["spider_update_date"] = spider_update_date
            es_dict["company_name"] = company_name
            es_dict["company_abbreviation"] = company_abbreviation
            es_dict["accept_date_str"] = accept_date_str
            es_dict["accept_date"] = accept_date
            es_dict["financing_amount"] = financing_amount
            es_dict["sponsor_institution"] = sponsor_institution
            es_dict["accounting_firm"] = accounting_firm
            es_dict["law_office"] = law_office
            es_dict["assessment_agency"] = Assessment_agency
            es_dict["spider_wormtime"] = spider_wormtime
            es_dict["reveal_info"] = reveal_info
            es_dict["inquiry"] = inquiry
            es_dict["stock_audit_num"] = stock_audit_num
            print('数据库新增数据')
            self.es_utils.insert_or_replace('stib', d=es_dict)
            self.redis_server.lpush(RedisKey.STIB, json.dumps(es_dict).encode('utf-8').decode('unicode_escape'))



