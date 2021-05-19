import requests,re,time
import json
# 第一三共中国
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"2606",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"ASP.NET_SessionId=kqhjwozwps0qftpkr3zbuvqg",
    "Host":"www.daiichisankyo.com.cn",
    "Origin":"http://www.daiichisankyo.com.cn",
    "Referer":"http://www.daiichisankyo.com.cn/News/newsList.aspx",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
data = {
    "__VIEWSTATE":"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",
    "__VIEWSTATEGENERATOR":"03E81997",
    "__EVENTTARGET":"ctl00$ContentPlaceHolder4$AspNetPager1",
    "__EVENTARGUMENT":3,
    "__EVENTVALIDATION":"/wEdAANimHpLGEQDyTJAqT9pdPZl6vfEPw+XJaWkL+0bgua3J6mWJ8rYvCIRwecByvlZSQcWVZHWjqNSxtuKuZqnKEL9nG4WbX9X9ckYjzhMq0Z/lg=="
}
url="http://www.daiichisankyo.com.cn/News/newsList.aspx"
res = requests.post(url,headers=headers,data=data,verify=False)
print(res.status_code)
print(res.text)