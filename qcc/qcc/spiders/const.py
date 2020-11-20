#

STORE_PATH = '/home/zengxiangxu/temp/'  # 临时文件存储路径

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'upgrade-insecure-requests':'1',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cache-control':'max-age=0',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
}

class MongoTables:
    USER_AGENTS = "user_agents"  # 浏览器 user-agent 集合
    INVEST_CHINA_FUND = "invest_china_fund"  # 对外投资公司数据
    SPIDER_WECHAT_MP = 'wechat_mp'  # 微信公众号的基本信息
    SPIDER_WECHAT_MP_TITLE = 'spider_wechat_mp_title'  # 微信平台获取各个公众号的列表页(存储到mongo中备份一下 )
    SPIDER_CDE_TITLE = 'spider_cde_title'  # 存储cde要爬取的链接

class ESIndex:
    BUSINESS_INFO = 'business_info' #工商数据
    INVEST_NEWS = 'news' #存储微信公众号文章
    INVEST_CHINA_FUND = 'invest_china_fund' #基金数据

class RedisKey:
    SPIDER_CDE_COOKIE = 'spider_cde_cookie'  # 存储cde的cookie
    PROXY_IP = 'spider_proxy_ip' #随机代理ip spider_wechat_mp_title
    WECHAT_MP_TITLE = 'spider_wechat_mp_title'  # 微信平台获取各个公众号的列表页
    BUSINESS_INFO = 'data_clean_business_info'

class QCCAPI:
    BASE_INFO = "http://api.qichacha.com/ECIV4/GetBasicDetailsByName"  # 企业工商详情
    INVEST_INFO = "http://api.qichacha.com/ECIInvestmentThrough/GetInfo"  # 企业对外投资穿透
    MAIN_STAFF = "http://api.qichacha.com/ECIEmployee/GetList"  # 主要人员列表
    SHAREHOLDER_INFO = "http://api.qichacha.com/ECIPartner/GetList"  # 股东列表
    COMPANY_CHANGE = "http://api.qichacha.com/ECIChange/GetList"  # 企业变更记录

class PAGEOPS:
    PAGE_SIZE = 20
