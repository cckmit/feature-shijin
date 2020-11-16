#

STORE_PATH = '/home/zengxiangxu/temp/'  # 临时文件存储路径


class MongoTables:
    USER_AGENTS = "user_agents"  # 浏览器 user-agent 集合
    INVEST_CHINA_FUND = "invest_china_fund"  # 对外投资公司数据
    SPIDER_WECHAT_MP = 'wechat_mp'  # 微信公众号的基本信息
    SPIDER_WECHAT_MP_TITLE = 'spider_wechat_mp_title'  # 微信平台获取各个公众号的列表页(存储到mongo中备份一下 )

class ESIndex:
    BUSINESS_INFO = 'business_info' #工商数据
    INVEST_NEWS = 'news' #存储微信公众号文章
    INVEST_CHINA_FUND = 'invest_china_fund' #基金数据

class RedisKey:
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
