# -*- coding: utf-8 -*-

import hashlib

class MD5Utils:
    # 保留以 0 开头的
    def get_md5(self, data):
        m = hashlib.md5(str(data).encode())
        return m.hexdigest()
        #return m.hexdigest().lstrip('0')

    # 与java生成md5一致
    def lstrip_zero_get_md5(self, data):
        m = hashlib.md5(str(data).encode())
        return m.hexdigest().lstrip('0')

