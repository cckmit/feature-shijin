# -*- coding: utf-8 -*-
# flake8: noqa
import logging
import os
import time

import requests
from qiniu import Auth, put_file
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)

#需要填写你的 Access Key 和 Secret Key
access_key = 'RPEoJfcPJREYLrPfxrsBUyWJEj2JEHwACfDQB28n'
secret_key = 'bB3a_3pXpcoPsRIU3UYvW3MeyhhXKWF2HGNmx7b7'
q = Auth(access_key, secret_key) # 构建鉴权对象
bucket_name = 'pharmcube-spider' # 要上传的空间



def is_already_qiniu(file_url):
    resq = requests.get(url=file_url)
    if 200 == resq.status_code:
        logging.info(f'------- 当前图片链接已经存在七牛云上了，无需再次上传 -------{file_url}')
        return True
    return False

#local_file_path: /home/zengxiangxu/temp/bb0f106ca101b94b046261ed374ff2f91.pdf
def up_qiniu(local_file_path, file_name,is_keep_file):
    attempts = 0
    success = False
    qiniu_url = ''
    qiniu_url_temp = f'http://spider.pharmcube.com/{file_name}'
    if is_already_qiniu(file_url=qiniu_url_temp):
        return qiniu_url_temp
    while attempts < 3 and not success:
        try:
            token = q.upload_token(bucket_name, file_name, 3600)  # 生成上传 Token，可以指定过期时间等
            info = put_file(token, file_name, local_file_path)  # 要上传文件的本地路径
            if 200 == info[1]._ResponseInfo__response.status_code:
                if not is_keep_file:
                    logging.info('------- 删除指定文件 -------' + file_name)
                    if os.path.exists(os.path.join(local_file_path)):
                        os.remove(os.path.join(local_file_path))
                logging.info('------- 当前图片成功上传到七牛云 -------' + file_name)
                qiniu_url = f'http://spider.pharmcube.com/{file_name}'
                success = True
            else:
                logging.info(f'------- 当前图片上传到七牛云上失败，重试中 {attempts} 次数 -------' + file_name)
        except Exception as err:
            print(err)
            logging.info(f'------- 当前图片上传到七牛云上失败，重试中 {attempts} 次数 -------' + file_name)
            if attempts > 2:
                break
        attempts += 1
    return qiniu_url
