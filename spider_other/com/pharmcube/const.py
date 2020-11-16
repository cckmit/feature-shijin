
class WeChatMP:
    LOGIN_IMG_PATH = '/home/zengxiangxu/temp/' #扫码图片存储路径
    LOGIN_IMG_NAME = 'wechat_mp_login.png' #需要扫码的图片
    SPIDER_WECHAT_MP = 'wechat_mp'  # 微信公众号的基本信息
    WECHAT_MP_ACCOUNT_INFO = 'wechat_mp_account_info'  # 登录微信公众号平台账号与密码

class RedisKey:
    SPIDER_WECHAT_MP = 'spider_wechat_mp' # 微信平台获取各个公众号的列表页
    WECHAT_MP_TITLE = 'spider_wechat_mp_title' # 微信平台获取各个公众号的列表页

