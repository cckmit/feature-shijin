import time


class DateUtils:
    # 获取毫秒级的时间戳
    def get_timestamp(self):
        return int(round(time.time()*1000))

    # 日期转时间戳 2020-10-23 返回单位：秒
    def unix_time(self, date_str):
        time_arr = time.strptime(date_str, "%Y-%m-%d")
        timestamp = int(time.mktime(time_arr))
        return timestamp

    #  时间戳转日期(毫秒)
    def custom_time(self, timestamp):
        time_local = time.localtime(timestamp/1000)
        dt = time.strftime("%Y-%m-%d", time_local)
        return dt

if __name__ == '__main__':
    import datetime


