import requests

url = "https://dl.slt6.com/-----http://www.chictr.org.cn/searchproj.aspx"
headers = {"sec-ch-ua-mobile":"?0",
           "Upgrade-Insecure-Requests":"1",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}

res = requests.get(url=url,headers=headers).text
print(res)