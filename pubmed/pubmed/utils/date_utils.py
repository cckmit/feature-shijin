# -*- coding:utf-8 -*-
import time

class DateUtils:
    # 获取系统时间的毫秒值,四舍五入
    def system_current_time_millis(self):
        return int(round(time.time()*1000))