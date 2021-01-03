# -*- coding: utf-8 -*-

import hashlib

class MD5Utils:

    def get_md5(self, data):
        m = hashlib.md5(str(data).encode())
        return m.hexdigest()
        #return m.hexdigest().lstrip('0')



