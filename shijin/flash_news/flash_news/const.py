from flash_news.utils import es_utils
from flash_news.utils.date_utils import DateUtils
from flash_news.utils.md5_utils import MD5Utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.str_utils import StrUtils

# STORE_PATH = 'E://workspace//pharmcube-spider-platform//shijin//flash_news//flash_news//temporary_file//'  # 临时文件存储路径
STORE_PATH = 'E://workspace//pharmcube-spider-platform//shijin//flash_news//flash_news//temporary_file'  # 临时文件存储路径

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
}

json_headers = {
 'Accept': 'application/json, text/javascript, */*; q=0.01',
 'Content-Type': 'application/json',
 'X-Requested-With': 'XMLHttpRequest',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
}

class MongoTables:
    USER_AGENTS = "user_agents"  # 浏览器 user-agent 集合
    INVEST_CHINA_FUND = "invest_china_fund"  # 对外投资公司数据
    SPIDER_WECHAT_MP = 'wechat_mp'  # 微信公众号的基本信息
    SPIDER_WECHAT_MP_TITLE = 'spider_wechat_mp_title'  # 微信平台获取各个公众号的列表页(存储到mongo中备份一下 )
    SPIDER_CDE_TITLE = 'spider_cde_title'  # 存储cde要爬取的链接
    DRUG_NHSA = 'drug_nhsa'  # 医保药品分类与代码数据库更新（2020年8月）
    SEND_EMAIL_LIST = 'send_email_list'#邮件发送集合
    MEDLIVE_USERS_LIST = 'medlive_users' #医脉通网站登录的用户名与密码
    MEDLIVE_DATA = 'medlive_data' #医脉通网站采集的数据
    FUND_DATA = 'fund_data' #基金数据

    BASE_CHANNEL = "base_channel" #基础数据
    INDUSTRY_NEWS_TYPE = "industry_news_type" #产业新类型
    INDUSTRY_NEWS_SPIDER_PARAMS = "industry_news_spider_params" #产业新爬虫

    # shijin
    FLASH_NEW = "flash_new" #快讯
    GOOG_DOCTOR = "good_doctor" #好大夫
    TINY_DOCTOR = "tiny_doctors" #微医生
    SPRING_RAIN_DOCTOR = "spring_rain_doctor" #医生
    HOSPITAL_HEALTH = "hospital_39healths" #39健康，拿医院数据
    WANFANG_DOCTOR = "wanfang_xiangqing" #万方医学网
    BAIDU_ACADEMIC = "baidu_academic" #百度学术
    BAIDU_STU = "baidu_stu" #百度学术
    MEET = "meeting_new" #会议
    CPC = "cpc" #cpc
    NEWS = "news" #医药自媒体
    WANFANG_COOPERATION = "wangfang_cooperation" #万方合作学者
    WANFANG_THEME = "wangfang_theme" #万方主题分析
    WANFANG_PERIODICAL = "wangfang_periodical" #万方期刊分析
    WANFANG_ID = "wangfang_id"


class ESIndex:
    BASE_COMPANY = 'base_company' #录入公司名称
    BUSINESS_INFO = 'business_info' #工商数据
    NEWS = 'news' #存储微信公众号文章
    INVEST_CHINA_FUND = 'invest_china_fund' #基金数据
    ISPOR_SUPPLEMENT = 'ispor_supplement' #ISPOR文献
    WHO_DRUG_INN = 'who_drug_inn' #WHO的Drug Information
    DRUG_US_DRUGS = 'drug_us_drugs' #美国库
    DRUG_US_ORANGE = 'drug_us_orange' #橙皮书
    DRUG_IPO = 'drug_ipo' #上市库
    INVEST_NEWS = 'invest_news'
    DRUG_REGISTER = 'drug_register'#注册库
    DRUG_PATENT_INFO_V2 = 'drug_patent_info_v2'
    DRUG_PATENT_GOOGLE = 'drug_patent_google' #专利号临时索引（需清洗专利号）
    DRUG_EARTH_NEWS_STAT = 'drug_earth_news_stat'
    PMC_ARTICLE = 'pmc_article' #PMC全文
    STIB = 'stib' #科创版
    CLASSIFICATION_CPC = 'classification_cpc' #cpc分类号
    MEETING_PAPER = 'meeting_paper' #asco  esmo

class RedisKey:
    SPIDER_CDE_COOKIE = 'spider_cde_cookie'  # 存储cde的cookie
    PROXY_IP = 'spider_proxy_ip' #随机代理ip spider_wechat_mp_title
    WECHAT_MP_TITLE = 'spider_wechat_mp_title'  # 微信平台获取各个公众号的列表页
    WECHAT_MP_LIKE_NUMS = 'wechat_mp_like_nums' #微信点赞数阅读数等
    BUSINESS_INFO = 'data_clean_business_info'
    DATA_CLEAN_US = 'data_clean_us'
    CLINICAL_ISPOR_SUPPLEMENT_ESIDS = 'clinical:ispor_supplement_esids' #通知秋颖处理数据
    REGISTERED_CAPITAL_LIST = 'registered_capital_list' #记录注册资本变更(李昊)
    SHAREHOLDER_INFO_LIST = 'shareholder_info_list' #股东，变更前与变更后的信息(李昊)
    NEWS_LIST = 'news_list'
    INVEST_NEWS_LIST = 'invest_news_list'
    DATA_CLEAN_INVEST_CHINA_FUND = 'data_clean_invest_china_fund'
    STIB = 'stib'  # 科创版

class QCCAPI:
    BASE_INFO = "http://api.qichacha.com/ECIV4/GetBasicDetailsByName"  # 企业工商详情
    INVEST_INFO = "http://api.qichacha.com/ECIInvestmentThrough/GetInfo"  # 企业对外投资穿透
    MAIN_STAFF = "http://api.qichacha.com/ECIEmployee/GetList"  # 主要人员列表
    SHAREHOLDER_INFO = "http://api.qichacha.com/ECIPartner/GetList"  # 股东列表
    COMPANY_CHANGE = "http://api.qichacha.com/ECIChange/GetList"  # 企业变更记录
    VERIFY_INFO = "http://api.qichacha.com/ECIInfoVerify/GetInfo"  #企业工商核验信息

class WindAPI:
    wind_Id = 'http://eapi.wind.com.cn/wind.ent.risk/openapi/searchcorplist?corpName='
    BASE_INFO = 'http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/A002?windId='
    MAIN_STAFF = 'http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/A003?windId='
    SHAREHOLDER_INFO = 'http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/A004?windId='
    COMPANY_CHANGE = 'http://eapi.wind.com.cn/wind.ent.risk/openapi/corpinfo/A006?windId='



class PAGEOPS:
    PAGE_SIZE = 20

def spider_init(self):
    self.es_utils = es_utils
    self.mongo_utils = MongoUtils()
    self.str_utils = StrUtils()
    self.date_utils = DateUtils()
    self.md5_utils = MD5Utils()
    return self
