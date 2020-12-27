# -*- coding: utf-8 -*-

import time
import logging
import hashlib
class QCCUtils:
    ENCODE = 'utf-8'
    APPKEY = "023b2da1063340ed9399df802a8755e7"
    SECKEY = "CF0313518DF26AC480A699FB4A1C9DDA"

    def get_qcc_token_headers(self):
        timestamp = str(int(time.time()))
        token = QCCUtils.APPKEY + timestamp + QCCUtils.SECKEY# Http请求头设置
        hl = hashlib.md5()
        hl.update(token.encode(encoding=QCCUtils.ENCODE))
        token = hl.hexdigest().upper()
        logging.info('获取token成功：' + token)
        return {'Token': token, 'Timespan': timestamp} # headers

