import hashlib
import execjs
href = "http://www.sinobiopharm.com/index.html#/news/newsdeatil?id=2740"
# print(href)
def md5Encode(str):
    m = hashlib.md5()  # 创建md5对象
    m.update(str)  # 传入需要加密的字符串进行MD5加密
    return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
esid = md5Encode(href.encode('utf-8'))
print(esid)
print(123)
"""
52252e585acf2b8a8f954650ce4c1e99
"""

# with open(r'kechuangban.js', encoding='UTF-8') as file:
#     result = file.read()
# context1 = execjs.compile(result)
# result1 = context1.call("status_transfer",{"currStatus":5,"collectType":1,"registeResult":1})
# print(result1)
# function(){}

# data=json.dumps(response.body) for i in data[]: #列表解析 title = i[''] 传给下一个函数详情解析 if len(data[]) > 0: page += 1 传给本身翻页
