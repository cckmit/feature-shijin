#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import logging
import os
import time
import requests
import json
from anaconda_project.internal.test.multipart import MultipartEncoder
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)

'''
利用企业微信接口发送信息 和 发送图片
'''

def returnRespInfo(type, subject, respone):
    if 'ok' == respone["errmsg"]:
        logging.info(f'======= {type}\t{subject}\t数据发送成功 =======')
        return
    logging.info(f'======= {type}\t{subject}\t数据发送失败 =======')

def get_media_id(filepath, filename, token):
    file_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=file'
    if not os.path.exists(filepath+filename):
        logging.info('发生异常：当前文件不存在：'+filepath + filename)
        return
    m = MultipartEncoder(fields={filename: ('file', open(filepath + filename, 'rb'), 'text/plain')},)
    r = requests.post(url=file_url, data=m, headers={'Content-Type': m.content_type})
    media_id = ast.literal_eval(r.text)['media_id']
    logging.info(f'获取到图片的ID是：{media_id}')
    return media_id

class WeChatUtils:
    def __init__(self):
        self.LOGIN_IMG_PATH = '/home/zengxiangxu/temp/'
        self.LOGIN_IMG_NAME = 'wechat_mp_login.png'
        self.TOKEN_CONF_PATH = './access_token.conf'
        self.CORPID = 'wx65282324fd407a3a'  #企业ID，在管理后台获取
        self.CORPSECRET = 'tlMKOFtaxWVwTtyMiMFgUfH7jcHhJxdVbelChhLcmVs'#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000008'  #应用ID，在后台应用中获取
        self.TOUSER = "ZengXiangXu|YangShanShan"  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,'corpsecret': self.CORPSECRET }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open(self.TOKEN_CONF_PATH, 'r') as f:
                t, access_token = f.read().split()
        except:
            with open(self.TOKEN_CONF_PATH, 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open(self.TOKEN_CONF_PATH, 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_img_data(self, filepath, filename):
        media_id = get_media_id(filepath=filepath, filename=filename, token=self.get_access_token())
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "image",
            "agentid": self.AGENTID,
            "image": {
                "media_id": media_id
            },
            "safe": "0"
            }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()   #当返回的数据是json串的时候直接用.json即可将respone转换成字典
        returnRespInfo('图片', filename ,respone)

    def send_text_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
              },
            "safe": "0"
            }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()   #当返回的数据是json串的时候直接用.json即可将respone转换成字典
        returnRespInfo('文本',message,respone)
if __name__ == '__main__':
    pass
    #WeChatUtils().send_img_data(filepath='d:/',filename='111.jpg')