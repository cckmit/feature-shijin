import calendar
import datetime
import re
import time
import logging
from datetime import timedelta
from flash_news.utils.str_utils import StrUtils

logger = logging.getLogger(__name__)

month_list = {'dec':'december','nov':'november','oct':'october','sept':'september','aug':'august','jul':'july','jun':'june','may':'may','apr':'april','mar':'march','feb':'february','jan':'january',}

class DateUtils:
    def __init__(self):
        self.str_utils = StrUtils()

    # 获取毫秒级的时间戳
    def get_timestamp(self):
        return int(round(time.time()*1000))

    # 日期转时间戳 2020-10-23 返回单位：秒
    def unix_time(self, date_str):
        try:
            time_arr = time.strptime(date_str, "%Y-%m-%d")
            timestamp = int(time.mktime(time_arr))
            return timestamp*1000
        except Exception as e:
            logger.info(f'当前传入待转换日期异常：{date_str} {str(e)}')
            return None

    # 日期转时间戳 September 01, 2019(%B %d, %Y); Jul 23, 2014(%b %d, %Y) 返回单位：毫秒
    def unix_time_en(self, date_str):
        try:
            date_str = date_str.lower()
            month_date_str = date_str.split(' ')[0]
            for month in month_list.items():
                if month[0] != month_date_str:
                    continue
                date_str = date_str.replace(month[0],month[1])
            time_arr = time.strptime(date_str, "%B %d, %Y")
            timestamp = int(time.mktime(time_arr))
            return timestamp*1000
        except Exception as e:
            logger.info(f'当前传入待转换日期异常：{date_str} {str(e)}')
            return None

    #解析自定义日期格式
    def unix_defined_format(self, date_str, format):
        try:
            time_arr = time.strptime(date_str, format)
            if time_arr.tm_year < 1970:
                timestamp = int((datetime.datetime(time_arr.tm_year, time_arr.tm_mon, time_arr.tm_mday, time_arr.tm_hour) - datetime.datetime(1970, 1, 1)).total_seconds())-3600*8
            else:
                timestamp = int(time.mktime(time_arr))
            return timestamp*1000
        except Exception as e:
            logger.info(f'当前传入待转换日期异常：{date_str} {str(e)}')
            return None

    #时间戳转日期(毫秒：正数与负数)-  %Y-%m-%d
    def defined_format_time(self, timestamp, format):
        dt = None
        try:
            if timestamp > 0:
                time_local = time.localtime(timestamp/1000)
                dt = time.strftime(format, time_local)
            else:
                dt = (datetime.datetime(1970, 1, 2) + datetime.timedelta(seconds=timestamp/1000)).strftime(format)
        except Exception as e:
            logger.info(f'当前传入待转换日期异常：{timestamp} {str(e)}')
        return dt

    #获取当前年份
    def custom_year(self, timestamp):
        dt = time.strftime("%G", time.localtime(timestamp/1000))
        return int(dt)

    #获取当月最大的天数
    def get_month_range(self, year, month):
        return calendar.monthrange(year, month)[1]

    def sum_time(self, ts):
        if '分钟前' in ts:
            a = ts.split('分钟前')[0]
            publish_date = ((datetime.now() - timedelta(minutes=int(a))).date()).strftime('%Y-%m-%d %H:%M:%S')
        elif '小时前' in ts:
            b = ts.split('小时前')[0]
            publish_date = ((datetime.now() - timedelta(hours=int(b))).date()).strftime('%Y-%m-%d %H:%M:%S')
        elif '昨天' in ts:
            aa = ts[2:4]
            c = int(24) - int(aa)
            publish_date = ((datetime.now() + timedelta(hours=c)).date()).strftime('%Y-%m-%d %H:%M:%S')
        elif ts == '刚刚':
            publish_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            publish_date = datetime.strptime(ts, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M:%S')
        publish_date = int(time.mktime(time.strptime(publish_date, "%Y-%m-%d %H:%M:%S")) * 1000)
        return publish_date
