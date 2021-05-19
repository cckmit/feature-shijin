import time
# res = requests.get('http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=').text
# res = json.loads(res)
# for i in res['data']:
#     ip = i['ip']
#     port = i['port']
#     proxies = "http://"+str(ip)+":"+str(port)
#     print(proxies)

# ip_str = requests.post(url="http://60.205.151.191:80/es_online/get_dynamic_ip", timeout=5)
# proxy = {'http': ip_str.text}
# print(f"当前获取到代理IP：{ip_str.text}")

# a = [11, 22, 33, 44, 55, 66]
# for i, j in enumerate(a):
#     print(i)
#     print(j)
#     print("1111111111111")
import re
# aa = '稿, 监管信息公告, 肿瘤学 / 免疫学 | 2020-06-01'
# bb = aa[aa.rfind("|")+2:]
# print(bb)

# str = "this is string example....wow!!! this is really string"
# # print(str.replace("is", "was"))
# aa=str.replace("is", "was", )
# print(aa)

# aa = '/media/1371/16decnews.png?width=500&height=327.5563258232236'
# bb = ''.join(re.findall(r'.*?png',aa))
# print(bb)

# jj = ""
# aa = ''.join(re.findall(r'style="text-align:left;">.*?',jj))
# print(aa)

# spider_publish_time_str = '12-8-2020'
# spider_publish_time_list = list(spider_publish_time_str)
# spider_publish_time_list.insert(3,'0')
# spider_publish_time_str = ''.join(spider_publish_time_list)
# print(spider_publish_time_str)

# j = "2020-11-7 - 18:00"
# aa = j[:j.rfind(" -")]
# print(aa)

aa = "八月. 27-2015"
bb = aa.split(" ")[0]
print(bb)

# 47f8124d86ea124533ba5d30015dc8978348efb7
# 6087fd5c2a928686312606715aa99e8b

# aa = time.strftime("%Y-%m-%d", time.localtime())
# print(aa)

# j = [2,3,4,5,6]
# for i,j in enumerate(j):
#     print(i,j)