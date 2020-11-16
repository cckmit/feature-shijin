# -*- coding: utf-8 -*-
# flake8: noqa
import logging
import os
import time

from qiniu import Auth, put_file
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.INFO)

#需要填写你的 Access Key 和 Secret Key
access_key = 'RPEoJfcPJREYLrPfxrsBUyWJEj2JEHwACfDQB28n'
secret_key = 'bB3a_3pXpcoPsRIU3UYvW3MeyhhXKWF2HGNmx7b7'
#构建鉴权对象
q = Auth(access_key, secret_key)

def up_qiniu(local_file_path, file_name, retry_err_times,current_times,is_keep_file):
    #要上传的空间
    bucket_name = 'pharmcube-spider'
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, file_name, 3600)
    #要上传文件的本地路径
    info = put_file(token, file_name, local_file_path)
    if 200 == info[1]._ResponseInfo__response.status_code:
        if not is_keep_file:
            logging.info('------- 删除指定文件 -------'+file_name)
            if os.path.exists(os.path.join(local_file_path)):
                os.remove(os.path.join(local_file_path))
        logging.info('------- 当前图片成功上传到七牛云上 -------'+file_name)
        return True, f'http://spider.pharmcube.com/{file_name}'
    else:
        if current_times < retry_err_times:
            time.sleep(3)
            current_times = current_times + 1
            logging.info(f'------- 当前图片上传到七牛云上失败，重试中 {current_times} 次数 -------' + file_name)
            up_qiniu(local_file_path=local_file_path, file_name=file_name, retry_err_times=retry_err_times, current_times=current_times, is_keep_file=False)
        else:
            logging.info(f'------- 当前图片上传到七牛云上失败，超过了指定的次数，不再进行重试 -------' + local_file_path)
        return False, None

if __name__ == '__main__':
    file_name = 'test.png'
    local_file_path = '/home/zengxiangxu/test.png'
    resultsup_qiniu(local_file_path=local_file_path, file_name=file_name, retry_err_times=3, current_times=0,is_keep_file=False)
