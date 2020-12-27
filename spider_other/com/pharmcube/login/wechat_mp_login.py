# -*- coding:utf-8 -*-

'''
微信公众号平台登录
yssddd@163.com  884833Yss$  74bdd90c7425f4e69ba92190a4547cbf
deyu1982@163.com  343607Meng  1787d21d7032d24539c0ce642a1a213c

{ "_id" : ObjectId("5faa29eac89347ab9f8baf35"), "username" : "deyu1982@163.com", "pwd" : "343607Meng", "pwd_encrypt" : "1787d21d7032d24539c0ce642a1a213c", "spider_wormtime" : 1604386464294, "login_info" : "孟哥" }

微信号：18852667190----qqqq1122
'''
import ast
import os
import random
import sys
import time
import requests
from com.pharmcube.const import WeChatMP, RedisKey
from com.pharmcube.utils import redis_utils, date_utils
from com.pharmcube.utils.mongo_utils import MongoUtils
from com.pharmcube.utils.wechat_work_utils import WeChatUtils
import logging.config
logging.config.fileConfig('/root/spider_py/logging.conf')
logging = logging.getLogger(name='rotatingFileLogger')

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Proxy-Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Referer':'https://mp.weixin.qq.com/',
    'x-requested-with':'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6756.400 QQBrowser/10.3.2473.400',
}

session = requests.session()
wechat_mp_account_info = MongoUtils().find_all(coll_name=WeChatMP().WECHAT_MP_ACCOUNT_INFO)
wechat_mp_account = wechat_mp_account_info[random.randint(0, wechat_mp_account_info.count() - 1)]
username = wechat_mp_account['username']
login_info = wechat_mp_account['login_info']
pwd_encrypt = wechat_mp_account['pwd_encrypt']


class WeChatLogin:

    # 模拟人工输入登录账号、密码
    def input_pw(self):
        data = {'username': username, 'pwd': pwd_encrypt, 'f': 'json', 'userlang': 'zh_CN', 'lang': 'zh_CN','ajax': '1'}
        logging.info(f'======= 开始账号密码登陆网站 =======')
        login_url_1 = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin'
        session.post(url=login_url_1, data=data, headers=headers)

    # 下载需要扫描的二维码并人工确认（二维码10分钟内有效）
    def wait_scan_qr_code(self):
        image_header = headers
        image_header['Accept'] = 'image/webp,image/apng,image/*,*/*;q=0.8'
        image_header['Content-Type'] = ''
        image_header['Referer'] = f'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account={username}&token='
        image_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=211'
        resp_2 = session.get(url=image_url, headers=image_header)
        img = resp_2.content
        logging.info('======= 开始下载需要人工确认的二维码 =======')
        img_path = WeChatMP().LOGIN_IMG_PATH+WeChatMP().LOGIN_IMG_NAME
        if os.path.exists(img_path):
            os.remove(img_path)
        with open( img_path,'wb' ) as f:
            f.write(img)
            f.flush()
        sleep_time(3, 5)
        check_login_url = 'https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1'
        logging.info('======= 人工确认的二维码发送到企业微信 =======')
        WeChatUtils().send_text_data(message='当前正在登陆账号：'+login_info)
        WeChatUtils().send_img_data( filepath=WeChatMP().LOGIN_IMG_PATH, filename=WeChatMP().LOGIN_IMG_NAME )
        is_success = False
        retry_times = 0
        while True:
            time.sleep(15)
            if retry_times > 40:
                logging.info('======= 等待人工确认二维码时间超过 10 分钟，原二维码已失效！重试中 =======')
                break
            resp = session.get(url=check_login_url, headers=headers)
            status = ast.literal_eval(resp.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))['status']
            if status == 1:
                WeChatUtils().send_text_data(message='======= 恭喜,人工扫码成功！ =======')
                is_success = True
                logging.info('======= 恭喜,人工扫码成功！ =======')
                break
            else:
                retry_times = retry_times + 1
                logging.info('======= 等待人工扫码 ======= '+str(retry_times*15) +' 秒！')
                WeChatUtils().send_text_data(message=f'当前正在登陆账号：{login_info} 已等待：{str(retry_times*15)} 秒！请及时扫码！' )
        return is_success

    def get_token(self):
        token_header = headers
        token_username = username.replace('@','%40')
        token_referer = f'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account={token_username}&token='
        token_header['Referer'] = token_referer
        token_url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login'
        token_data = {'f':'json', 'userlang':'zh_CN', 'lang':'zh_CN', 'ajax':'1', 'redirect_url':'', 'token':''}
        token_resp = session.post(url=token_url, data=token_data, headers=token_header)
        redirect_url = ast.literal_eval(token_resp.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))['redirect_url']
        token = redirect_url.split('=')[3]
        logging.info(f'获取到的token值{token}')
        return token

    def get_any_mp_info(self,token,biz,wechat_work):
        mp_url = f'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=10&fakeid={biz}&type=9&query=&token={token}&lang=zh_CN&f=json&ajax=1'
        mp_referer = f'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=10&token={token}&lang=zh_CN'
        mp_headers = headers
        mp_headers['Referer'] = mp_referer
        logging.info(f'======= 获取公众号文章{wechat_work} =======')
        resp = session.get(url=mp_url, headers=mp_headers)
        resutls = ast.literal_eval(resp.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
        if 'app_msg_list' not in resutls:
            logging.info('------- 当前访问被限制，休息 30 ~ 60 分钟！ -------')
            sleep_time(min=60*30, max=60*60)
        else:
            return resutls['app_msg_list']

# 随机等待时间
def sleep_time(min,max):
    random_time = random.randint(min,max)
    logging.info(f'休息 {random_time} 秒，马上回来! ')
    time.sleep(random_time)

if __name__ == '__main__':
    logging.info('======= 开始读取信息 =======')
    sleep_times = 0 #休息次数
    WeChatLogin().input_pw()
    sleep_time(min=2, max=10)
    while not WeChatLogin().wait_scan_qr_code():
        sleep_time(min=2, max=10)
    token = WeChatLogin().get_token()
    sleep_time(min=2, max=10)
    is_spider_date_set = set()
    while 1:
        custom_time = date_utils.custom_time(timestamp=date_utils.get_zero_millis())
        if (custom_time not in is_spider_date_set) and date_utils.is_contains_date('18:00', '19:30'):
            is_spider_date_set.add(custom_time)
            logging.info('------- 当前时间在指定时间范围之内，开始更新数据 -------')
            redis_cli = redis_utils.redis_cluster('false')
            if redis_cli.llen(RedisKey.WECHAT_MP_TITLE) == 0:
                redis_cli.delete(RedisKey.SPIDER_WECHAT_MP)
                wechat_mp = MongoUtils().find_all(coll_name=WeChatMP().SPIDER_WECHAT_MP)
                for wechat in wechat_mp:
                    wechat['_id'] = ''
                    redis_cli.lpush(RedisKey.SPIDER_WECHAT_MP, str(wechat))
                send_times = 0
                while redis_cli.llen(RedisKey.SPIDER_WECHAT_MP) > 0:
                    wechat = eval(redis_cli.rpop(RedisKey.SPIDER_WECHAT_MP))
                    sleep_time(min=10, max=30)
                    logging.info(f'------- 当前待采集的微信公众号数为：{redis_cli.llen(RedisKey.SPIDER_WECHAT_MP)} -------')
                    __biz = wechat['__biz']
                    wechat_official_accounts_desc = wechat['wechat_official_accounts_desc']
                    try:
                        results = WeChatLogin().get_any_mp_info(token=token, biz=__biz, wechat_work=wechat_official_accounts_desc)
                        if None == results:
                            logging.info(f'------- 当前公众号信息采集失败重试中: {str(wechat)} -------')
                            redis_cli.lpush(RedisKey.SPIDER_WECHAT_MP, str(wechat))
                            continue
                        logging.info(f'------- redis data -------{str(results)}')
                        redis_cli.lpush(RedisKey.WECHAT_MP_TITLE, str(results))
                    except Exception as err:
                        print(err)
                        logging.info(f'------- 当前公众号信息采集失败重试中: {str(wechat)} -------')
                        redis_cli.lpush(RedisKey.SPIDER_WECHAT_MP, str(wechat))
                    finally:
                        send_times = send_times+1
                        if send_times % 55 == 0:
                            logging.info(f'------- 当前访问微信公众号文章次数 {send_times}，休息 30 ~ 60 分钟！ -------')
                            sleep_time(min=60*30, max=60*60)
        else:
            sleep_times = sleep_times + 1
            random_times = random.randint(6, 20)
            logging.info(f'------- 休息10分钟 --------{sleep_times} {random_times}')
            time.sleep(10 * 60)
            if sleep_times > random_times:
                logging.info('------- 当前时间不在指定时间范围之内，维护 token 有效期 -------')
                keep_token_url = f'https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&token={token}&lang=zh_CN'
                keep_token_headers = headers
                keep_token_headers['Referer'] = keep_token_url
                keep_token_url = f'https://mp.weixin.qq.com/cgi-bin/filepage?type=2&begin=0&count=12&token={token}&lang=zh_CN'
                resp = session.get(url=keep_token_url, headers=keep_token_headers )
                if 'window.wx.commonData' in str(resp.content):
                    sleep_times = 0
                    logging.info(f'------- 当前token依然有效 -------{token}')
                else:
                    logging.info(f'------- 当前token已失效 -------{token}')
                    WeChatUtils().send_text_data(message='======= 请注意，当前维护的token已失效，程序退出中！ =======')
                    sys.exit(1)
