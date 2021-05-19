import requests
import execjs
import json
import time
import sys

n = 0
while True:
    n += 1
    headers = {'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'Accept': '*/*',
                'Referer': 'http://kcb.sse.com.cn/',
                'Accept-Language': 'zh-CN,zh;q=0.9'}
    params = (('isPagination', 'true'),
            ('sqlId', 'GP_GPZCZ_SHXXPL'),
            ('pageHelp.pageSize', '20'),
            ('fileType', '30,5,6'),
            ('pageHelp.pageNo', n),
            ('pageHelp.beginPage', '1'),
            ('pageHelp.endPage', '1'),
            ('_', '1616394380667'))
    res = requests.get('http://query.sse.com.cn/commonSoaQuery.do', headers=headers, params=params, verify=False).text
    res = json.loads(res)
    stock= res['pageHelp']['data']
    print(res)
    print(n)
    # for i in range(20):
    #     header = {"Referer":"http://kcb.sse.com.cn/",
    #             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    #     data = {"isPagination":"true",
    #             "sqlId":"SH_XM_LB",
    #             "stockAuditNum":stock[i]['stockAuditNum'],
    #             "_":str(int(time.time())*1000)}
    #     stockAuditNum = 'http://kcb.sse.com.cn/renewal/xmxq/index.shtml?auditId=' + stock[i]['stockAuditNum']
    #     print(stockAuditNum)
    #     ress = requests.get("http://query.sse.com.cn/commonSoaQuery.do", headers=header,params=data,verify=False).text
    #     ress = json.loads(ress)
    #     currStatus = ress['pageHelp']['data'][0]['currStatus']
    #     collectType = ress['pageHelp']['data'][0]['collectType']
    #     registeResult = ress['pageHelp']['data'][0]['registeResult']
    #     with open(r'kechuangban.js', encoding='UTF-8') as file:
    #         result =file.read()
    #     context1 = execjs.compile(result)
    #     # 审核状态
    #     approval_status = context1.call("status_transfer",{"currStatus":currStatus,"collectType":collectType,"registeResult":registeResult})
    #     print(approval_status)
        # # 公司全称
        # company_name = ress['pageHelp']['data'][0]['stockAuditName']
        # print(company_name)
        # # 公司简称
        # company_abbreviation = ress['pageHelp']['data'][0]['stockIssuer'][0]['s_issueCompanyAbbrName']
        # print(company_abbreviation)
        # # 受理日期
        # accept_date_str = ress['result'][0]['auditApplyDate']
        # print(accept_date_str)
        # timeArray = time.strptime(accept_date_str,"%Y%m%d%H%M%S")
        # accept_date = int(time.mktime(timeArray))*1000
        # print(accept_date)
        # # 融资金额(亿元)
        # financing_amount = ress['pageHelp']['data'][0]['planIssueCapital']
        # financing_amount = round(financing_amount,2)
        # print(financing_amount)
        # # 保荐机构
        # sponsor_institution = ress['pageHelp']['data'][0]['intermediary'][0]['i_intermediaryName']
        # print(sponsor_institution)
        # # 会计师事务所
        # accounting_firm = ress['pageHelp']['data'][0]['intermediary'][1]['i_intermediaryName']
        # print(accounting_firm)
        # # 律师事务所
        # law_office = ress['pageHelp']['data'][0]['intermediary'][2]['i_intermediaryName']
        # print(law_office)
        # # 评估机构
        # try:
        #     Assessment_agency = ress['pageHelp']['data'][0]['intermediary'][3]['i_intermediaryName']
        # except:
        #     Assessment_agency = None
        # print(Assessment_agency)
        # spider_wormtime = int(time.time())*1000
        # print(spider_wormtime)
        #
        # dataa = {
        #     "isPagination": "false",
        #     "sqlId": "GP_GPZCZ_SHXXPL",
        #     "stockAuditNum": stock[i]['stockAuditNum'],
        #     "_": str(int(time.time()) * 1000),
        # }
        # resp = requests.get("http://query.sse.com.cn/commonSoaQuery.do", headers=header, params=dataa, verify=False).text
        # resp = json.loads(resp)
        # reveal_info = []
        # inquiry = []
        # m = 0
        # while True:
        #     m -= 1
        #     dic1 = {}
        #     dic2 = {}
        #     try:
        #         if '-' not in resp['result'][int(m)]['fileTitle']:
        #             prospectus_declare_repprt = resp['result'][int(m)]['fileTitle']
        #             if '招股说明书' in prospectus_declare_repprt:
        #                 reveal_file_type = '招股说明书'
        #             if '发行保荐书' in prospectus_declare_repprt:
        #                 reveal_file_type = '发行保荐书'
        #             if '上市保荐书' in prospectus_declare_repprt:
        #                 reveal_file_type = '上市保荐书'
        #             if '审计报告' in prospectus_declare_repprt:
        #                 reveal_file_type = '审计报告'
        #             if '法律意见书' in prospectus_declare_repprt:
        #                 reveal_file_type = '法律意见书'
        #             else:
        #                 pass
        #             prospectus_declare_repprt_time = resp['result'][int(m)]['publishDate']
        #             timeArray = time.strptime(prospectus_declare_repprt_time, "%Y-%m-%d")
        #             prospectus_declare_repprt_time = int(time.mktime(timeArray)) * 1000
        #             prospectus_declare_repprt_pdf = 'http://static.sse.com.cn/stock'+resp['result'][int(m)]['filePath']
        #             dic1["declare_repprt_name"] = prospectus_declare_repprt
        #             dic1["declare_repprt_url"] = prospectus_declare_repprt_pdf
        #             dic1["update_date"] = prospectus_declare_repprt_time
        #             dic1["reveal_file_type"] = reveal_file_type
        #         else:
        #             file_name = resp['result'][int(m)]['fileTitle']
        #             file_name_url = 'http://static.sse.com.cn/stock'+resp['result'][int(m)]['filePath']
        #             update_date = resp['result'][int(m)]['publishDate']
        #             timeArray = time.strptime(update_date, "%Y-%m-%d")
        #             update_date = int(time.mktime(timeArray)) * 1000
        #             dic2["file_name"] = file_name
        #             dic2["file_name_url"] = file_name_url
        #             dic2["update_date"] = update_date
        #     except:
        #         break
        #     reveal_info.append(dic1)
        #     inquiry.append(dic2)
        # reveal_info = [i for i in reveal_info if i != {}]
        # inquiry = [i for i in inquiry if i != {}]
        # print(reveal_info)
        # print(inquiry)





