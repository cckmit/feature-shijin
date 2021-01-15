
import json
import logging
import base64
import hashlib
import ast
import sys
import requests
from pharmcube_spider.const import WindAPI


def product_wind_token(self): #get_wind_token
    if self.redis_server.hlen('wind')> 0 and self.date_utils.get_timestamp() - ast.literal_eval(self.redis_server.hget('wind', 'wind_token').decode())['spider_wormtime'] < 2*3600*1000:
        return
    wind_user = 'EA1968482002'
    password = "94375596"
    m = hashlib.md5()
    b = password.encode(encoding='UTF-8')
    m.update(b)
    b64 = base64.b64encode(m.digest())
    verifyCode = bytes.decode(b64) #通过密码生成验证码
    token_resp = requests.get(f"http://eapi.wind.com.cn/wind.ent.risk/openapi/getToken?windUser={wind_user}&userType=S31&verifyCode="+requests.utils.quote(verifyCode))
    token_dict = json.loads(token_resp.text)
    token = ''
    if token_dict["errorCode"] == 0:
        token = token_dict["source"]["token"]
    if self.str_utils.is_blank(str=token):
        logging.info(f'当前获取 wind 的token出现异常，程序终止中：{token_resp}')
        sys.exit(1)
    logging.info(f'获取到token：{token}')
    self.redis_server.hset('wind', 'wind_token', {'token': token, 'spider_wormtime':  self.date_utils.get_timestamp()})

def get_wind_id(self, search_name):
    wind_id = ''
    wind_id_url = WindAPI.wind_Id + f'{search_name}&token={self.wind_token}'
    resp = requests.get(wind_id_url)
    results = json.loads(resp.text)
    if results["errorCode"] == 0:
        if results.get("source") is not None and results.get("source")["total"] > 0:
            for item in results["source"]["items"]:
                wind_name = item['corpName']
                if self.str_utils.remove_mark(wind_name) == self.str_utils.remove_mark(search_name):
                    wind_id = item["windId"]
                    break
    logging.info(f'获取公司：{search_name} wind_id：{wind_id}')
    return wind_id

def get_resp_meta(param, resp):
    page_param = 0
    if param in resp.meta:
        page_param = resp.meta[param]
    return page_param

# 数据翻页操作
def page_ops(self, spider_url, page_size, page_index, meta, scrapy, log_info):
    for page_index in range(page_index+1, page_index+2):
        logging.info(log_info)
        url = spider_url + f'&pageIndex={page_index}&pageSize={page_size}'
        yield scrapy.Request(url, callback=self.parse, meta=meta, priority=100)

def get_wind_token(self):
    token = ''
    wind_token_dict = ast.literal_eval(self.redis_server.hget('wind', 'wind_token').decode())
    if self.date_utils.get_timestamp() - wind_token_dict['spider_wormtime'] < 2*3600*1000: #token值在2小时以内，视为有效值
        token = wind_token_dict['token']
    else:
        product_wind_token()
        token = ast.literal_eval(self.redis_server.hget('wind', 'wind_token').decode())['token']
    return token

def is_invalid_windid(self, wind_id, name):
    if self.str_utils.is_blank(str=wind_id):
        logging.info(f'wind接口没有该公司对应的wind_id：{name}')
        return True
    return False