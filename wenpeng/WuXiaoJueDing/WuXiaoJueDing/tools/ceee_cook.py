import json

import re
import random
import asyncio,random,psutil,os,signal,time
from pyppeteer import launch
# import redis
# redisconn=redis.Redis(host='119.29.131.145',port=7001)

from rediscluster import StrictRedisCluster
#conn_list = [{"host": "10.46.176.105", "port": "7000"},{"host": "10.46.176.105", "port": "7001"},
#   {"host": "10.46.176.105", "port": "7002"},{"host": "10.46.176.105", "port": "7003"},{"host": "10.46.176.105", "port": "7004"},
#   {"host": "10.46.176.105", "port": "7005"},{"host": "10.27.217.54", "port": "7000"},{"host": "10.27.217.54", "port": "7001"},
#   {"host": "10.27.217.54", "port": "7002"},{"host": "10.27.217.54", "port": "7003"},{"host": "10.27.217.54", "port": "7004"},
#   {"host": "10.27.217.54", "port": "7005"},{"host": "10.27.217.22", "port": "7000"},{"host": "10.27.217.22", "port": "7001"},
#   {"host": "10.27.217.22", "port": "7002"},{"host": "10.27.217.22", "port": "7003"},{"host": "10.27.217.22", "port": "7004"}]
conn_list = [
    {"host": "10.66.205.48", "port": "8000"},
    {"host": "10.66.205.48", "port": "8001"},
    {"host": "10.66.205.48", "port": "8002"},
    {"host": "10.66.205.48", "port": "8003"},
    {"host": "10.66.205.48", "port": "8004"},
    {"host": "10.66.205.48", "port": "8005"},
    {"host": "10.66.205.48", "port": "8006"},

    {"host": "172.17.108.71", "port": "8000"},
    {"host": "172.17.108.71", "port": "8001"},
    {"host": "172.17.108.71", "port": "8002"},
    {"host": "172.17.108.71", "port": "8003"},
    {"host": "172.17.108.71", "port": "8004"},
    {"host": "172.17.108.71", "port": "8005"},
    {"host": "172.17.108.71", "port": "8006"},
    {"host": "172.17.108.71", "port": "8007"},

 ]



redisconn = StrictRedisCluster(startup_nodes=conn_list)
spider_cookie_key='spider_cookie'
#pip3 install psutil
#pip3 install redis-py-cluster


def randomProxyIP():
    proxy_ip_list = redisconn.lrange('spider_proxy_ip', 0, -1)
    if not proxy_ip_list:return None
    proxy_ip = str(proxy_ip_list[random.randint(0, redisconn.llen('spider_proxy_ip') - 1)], 'utf-8')
    proxy_ip_json = json.loads(proxy_ip)
    proxy_ip = f'http://{proxy_ip_json["ip"]}:{proxy_ip_json["port"]}'
    return proxy_ip

class Get_Cookie():
    async def main(self,url,ip=None):
        width = random.randint(800,1200)
        height = random.randint(700,1080)
        # exepath = r'C:\Users\Administrator.USER-20190313RI\AppData\Local\Google\Chrome\Application\chrome.exe'  # 谷歌浏览器路径
        exepath='/opt/google/chrome/chrome' #linux路径
        args = ['--no-sandbox',  # 取消沙盒模式
                '--disable-gpu',
                '--mute-audio',
                '--allow-hidden-media-playback',
                '--alsa-mute-element-name',
                # '--log-level=3',
                '--disable-web-security',
                '--disable-infobars',  # 不显示信息栏  比如 chrome正在受到自动测试软件的控制
                '--window-size={},{}'.format(width, height),
                ]
        if ip:
            ip1 = re.findall('(\d+\.\d+\.\d+\.\d+:\d+)', ip)
            if len(ip1) > 0:
                args.append("--proxy-server=http://{}".format(ip1[0]))
        params = {
            'headless': True,  # True表示无界面
            # 'devtools':False,
            'autoClose': True, #自动关闭页面
            'handleSIGTERM': True,
            'handleSIGHUP': True,
            'executablePath': exepath,
            "userDataDir": r"./temporary",
            'args': args,
            'dumpio': True}
        self.browser = await launch(params)
        page = await  self.browser.newPage()
        ua='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        await page.setUserAgent(ua)
        page.setDefaultNavigationTimeout(1000 * 60)
        await self.page_evaluate(page)
        await page.goto(url)
        cookies = await page.cookies()
        # cookie ={i['name']:i['value'] for i in cookies}
        cookie='; '.join([i['name']+'='+i['value'] for i in cookies])
        print('cookie:',cookie)
        redisconn.hset(spider_cookie_key,spider_cookie_key,cookie)
        return cookie

    async def page_evaluate(self,page):
        await page.evaluateOnNewDocument('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
        await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
        await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
        await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    def kill_pid(self,name):#杀掉chrome进程
        # linux平台
        try:
            pid = self.browser.process.pid
            pgid = os.getpgid(pid)
            # 强制结束
            os.kill(pid, signal.SIGKILL)
            print("结束进程：%d" % pid)
            print("父进程是：%d" % pgid)
            print("等待结果：%d" % self.browser.process.wait())
        except BaseException as err:
            print("close: {0}".format(err))
        time.sleep(3)
        # 查看是否还有其他进程
        for proc in psutil.process_iter():
            if name in proc.name():
                try:
                    os.kill(proc.pid, signal.SIGTERM)
                    print('已杀死[pid:%s]的进程[pgid：%s][名称：%s]' % (proc.pid, pgid, proc.name()))
                except BaseException as err:
                    print("kill: {0}".format(err))
        signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    def get_cookie(self,url):
        loop = asyncio.get_event_loop()
        ip=randomProxyIP() #获取代理ip
        task = asyncio.ensure_future(self.main(url,ip))
        loop.run_until_complete(task)
        self.kill_pid('chrome')
        cookie = task.result()
        return cookie


import requests
def test(url2,headers):
    res = requests.get(url=url2, headers=headers)
    print(res.status_code)
    # print(res.text)
    # thumb_urls = res.text.split('var thumburl =')
    thumb_urls = res.text.split('var picurl =')
    print('thumb_urls:', thumb_urls)
    for i in range(len(thumb_urls)):
        thumb_url = thumb_urls[i].strip()
        if not thumb_url.startswith('"/freeze.main?'):
            continue
        img_url = 'http://cpquery.cnipa.gov.cn' + thumb_url.split(';')[0].replace('"', '').replace('\'', '').replace(
            '+', '').replace(' ', '').strip()
        print(img_url)
        file_data = requests.get(url=img_url, allow_redirects=True, headers=headers, timeout=60)
        print(file_data.status_code)
        with open('./images/{}.png'.format(i), 'wb') as handler:
            handler.write(file_data.content)
        break


if __name__ == '__main__':
    #正式运行
    url = "http://cpquery.cnipa.gov.cn/txnFsjdFileView.do?select-key:fid=GA000265983677&select-key:wenjiandm=201019&select-key:wenjianlx=0403&select-key:wendanglx=01&select-key:shenqingh=2017303560902"
    #url = "http://cpquery.cnipa.gov.cn/txnFsjdFileView.do?select-key:fid=GA000266425535&select-key:wenjiandm=201019&select-key:wenjianlx=0403&select-key:wendanglx=01&select-key:shenqingh=2005800300946"
    while True:
        try:
            cookie=Get_Cookie().get_cookie(url)
            print('cookie:',cookie)
        except Exception as e:
            print(e)
        #time.sleep(12)
        time.sleep(20)

    #单个测试
    # cookie = Get_Cookie().get_cookie(url)
    # print(cookie)
    # url1='http://cpquery.cnipa.gov.cn/freeze.main?txn-code=txnImgToken&token=6EC26E307D8C0AD016B60D470C379798&imgtoken=B3EEE92D4B0B4F76A1CFB9614B94BDA1'
    # url2='http://cpquery.cnipa.gov.cn/txnFsjdFileView.do?select-key:fid=GA000265983677&select-key:wenjiandm=201019&select-key:wenjianlx=0403&select-key:wendanglx=01&select-key:shenqingh=2017303560902'
    # url3='http://cpquery.cnipa.gov.cn/txnFsjdFileView.do?select-key:fid=GA000266243052&select-key:wenjiandm=2010'
    # headers = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    #     'Host': 'cpquery.cnipa.gov.cn',
    #     'Connection': 'keep-alive',}
    # headers['cookie']=cookie
    # test(url2,headers)






