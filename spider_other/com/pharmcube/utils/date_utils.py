import datetime
import time


#获取当天零时时间戳
def get_zero_millis():
    now_time = int(time.time())
    return (now_time - now_time % 86400 + time.timezone)*1000

# 日期转时间戳 2020-10-23 返回单位：秒
def unix_time(date_str):
    time_arr = time.strptime(date_str, "%Y-%m-%d")
    timestamp = int(time.mktime(time_arr))
    return timestamp

    #  时间戳转日期(毫秒)
def custom_time( timestamp):
    time_local = time.localtime(timestamp/1000)
    dt = time.strftime("%Y-%m-%d", time_local)
    return dt

# start_time : 9:30 ; end_time = 9:33
def is_contains_date (start_time, end_time):
    # 范围时间
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start_time, '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end_time, '%Y-%m-%d%H:%M')
    # 当前时间
    now_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if now_time > start_time and now_time < end_time:
        return True
    else:
        return False

