import json
import logging
import scrapy
import re
import time
from lxml import etree
from pyquery import PyQuery as pq
from flash_news.utils import qiniu_utils
from flash_news.utils import pdf_utils
from flash_news.utils import es_utils, file_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news.utils.file_utils import DownloadFile
from flash_news import const
from flash_news.const import ESIndex,RedisKey
from flash_news.utils.es_utils import Query, QueryType
from flash_news.utils.date_utils import DateUtils

'''
tapd网址：https://www.tapd.cn/22397021/prong/stories/view/1122397021001003367
'''

class FlashNewSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        self.file_utils = DownloadFile()
        self.file_utils_1 = file_utils
        self.pdf_utils = pdf_utils
        self.qiniu_utils = qiniu_utils
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        if 'baidu.com' in spider_url:
            yield scrapy.Request(url='http://swzy.gf.bj.cn/api.php/list/93/page/undefined', callback=self.china_biology_pharmacy,) #1中国生物制药
            yield scrapy.Request(url='https://www.fosunpharma.com/news/groupNewsData.aspx?pageid=1&time=0', callback=self.fosunpharma,)#2复星医药
            yield scrapy.Request(url='https://www.3sbio.com/news/list.aspx', callback=self.sansheng_pharmacy,)#3三生制药
            yield scrapy.Request(url='http://next.innoventbio.com:8000/api/reports?limit=10&offset=0', callback=self.innovent_biologics,)#4信达生物
            yield scrapy.Request(url='http://cn.hspharm.com/news/ji-tuan-xin-wen-list-0.htm', callback=self.hanlin_pharmacy,)#5翰森制药
            yield scrapy.Request(url='https://www.simcere.com/news/news.aspx?mtt=1', callback=self.first_signs,)#6先声药业
            yield scrapy.Request(url='http://www.e-cspc.com/news/index.html', callback=self.shi_pharmacy,)#7石药集团
            yield scrapy.Request(url='https://www.hutch-med.com/sc/news/news-archive/?cat=117,105,113,101&in', callback=self.hehaung_pharmacy,)#8和黄医药
            yield scrapy.Request(url='http://www.zailaboratory.com/ch/pressnews/list.aspx?lcid=87', callback=self.zaiding_pharmacy,)#9再鼎医药
            yield scrapy.Request(url='http://www.rongchang.com/news/rong-chang-dong-tai.jsp?nowPage=1', callback=self.rongchang_pharmacy,)#10荣昌制药
            yield scrapy.Request(url='https://www.luye.cn/lvye/news.php?fid=1065', callback=self.green_tree_pharmacy,)#11绿叶制药
            yield scrapy.Request(url='https://www.akesobio.com/cn/media/akeso-news/', callback=self.kangfang_pharmacy,)#12康方生物
            yield scrapy.Request(url='https://www.cstonepharma.com/news/company_news.html', callback=self.footstone_pharmacy,)#13基石药业
            yield scrapy.Request(url='https://www.ascentagepharma.com/news/press-releases/?lang=zh-hant', callback=self.yasheng_pharmacy,)#14亚盛医药
            yield scrapy.Request(url='http://www.sphchina.com/api/Public/v1/?service=News.GetNewsListByCategory&category=news_release&lang=cn&size=10&page=1&_={}'.format(str(int(time.time()) * 1000)), callback=self.shanghai_pharmacy,)#15上海医药
            yield scrapy.Request(url='https://www.cms.net.cn/CmsNewWeb/news/media-reports.aspx',callback=self.kangzhe_pharmacy,)#16康哲药业    图片路径经常变
            yield scrapy.Request(url='http://www.alphamabonc.com/news/press_release.html', callback=self.kangning_pharmacy,)#17康宁杰瑞
            yield scrapy.Request(url='https://www.everestmedicines.com/CN/News.aspx?cid=2733', callback=self.yunding_pharmacy,)#18云顶新耀
            yield scrapy.Request(url='http://www.grandpharma.cn/News/7.aspx', callback=self.yuanda_pharmacy,)#19远大医药
            yield scrapy.Request(url='https://www.jwtherapeutics.com/cn/media/press-release/', callback=self.junuo_pharmacy,)#20药明巨诺
            yield scrapy.Request(url='http://www.sciclone.com/Modules/news.aspx', callback=self.shaisheng_pharmacy,)#21赛生药业
            yield scrapy.Request(url='https://www.livzon.com.cn/news/1/', callback=self.lizhu_pharmacy,)#22丽珠医药
            yield scrapy.Request(url='http://www.jacobiopharma.com/news/14/', callback=self.jiakesi_pharmacy,)#23加科思
            yield scrapy.Request(url='https://www.crpharm.com/xwzx/hryydt/', callback=self.huarun_pharmacy,)#24华润医药
            yield scrapy.Request(url='https://www.antengene.com/cn',callback=self.deqi_pharmacy,)#25德琪医药
            headers = {"pageid": "1",
                       "pagecount": "11",
                       "isCount": "true"}
            yield scrapy.Request(url='https://www.sihuanpharm.com/data/pages.aspx?createId=0&typeName=YJnews_list&tp=0&dataType=GET',method='POST',headers=headers,callback=self.fourth_ring_pharmacy,)#26四环医药
            yield scrapy.Request(url='https://www.ocumension.com/api/News/list?newsType=release&year=2021&keywords=',callback=self.oukang_pharmacy,)#27欧康维视
            yield scrapy.Request(url='https://cn.innocarepharma.com/cn/media/press-release/?page=1',callback=self.nuocheng_pharmacy,)#28诺诚健华
            yield scrapy.Request(url='http://www.cansinotech.com.cn/html/1//179/180/index.html',callback=self.kangxinuo_pharmacy,)#29康希诺生物
            yield scrapy.Request(url='https://www.harbourbiomed.com/zh/news',callback=self.hebai_pharmacy,)#30和铂医药
            yield scrapy.Request(url='https://www.ascletis.com/news/175.html',callback=self.geli_pharmacy,)#31歌礼制药
            yield scrapy.Request(url='https://www.hrs.com.cn/xwzxlist/4/1.html',callback=self.hengrui_pharmacy,)#32恒瑞医药
            yield scrapy.Request(url='https://www.junshipharma.com/News.html',callback=self.junshi_pharmacy,)#33君实生物
            yield scrapy.Request(url='http://www.bettapharma.com/News/index/cid/48/page/1',callback=self.beida_pharmacy,)#34贝达药业
            yield scrapy.Request(url='https://www.tasly.com/list-38-1.html',callback=self.tianshili_pharmacy,)#35天士力
            yield scrapy.Request(url='http://www.zelgen.com/xinwenzhongxin/',callback=self.zejing_pharmacy,)#36泽璟制药
            yield scrapy.Request(url='https://www.bio-thera.com/plus/list.php?tid=24&TotalResult=32&PageNo=1',callback=self.baiaotai_pharmacy,)#37百奥泰
            yield scrapy.Request(url='https://www.chipscreen.com/list-16.html',callback=self.weixin_pharmacy,)#38微芯生物
            yield scrapy.Request(url='https://www.haihepharma.com/news',callback=self.haihe_pharmacy,)#39海和生物
            yield scrapy.Request(url='https://www.apollomicsinc.com/zh-hans/%e6%96%b0%e9%97%bb%e7%a8%bf/',callback=self.guanke_pharmacy,)#40冠科美博
            yield scrapy.Request(url='http://www.canbridgepharma.com/index/news?lang=cn',callback=self.beihai_pharmacy,)#41北海康成
            yield scrapy.Request(url='https://www.i-mabbiopharma.com/cn/news.aspx',callback=self.tianjing_pharmacy,)#42天境生物

            yield scrapy.Request(url='https://www.prnasia.com/releases/all/listpage-all-9-all-all-all-industry-1.shtml',callback=self.meitongshe,)#1美通社中国
            yield scrapy.Request(url='https://www.gsk-china.com/zh-cn/media/press-releases/?page=all',callback=self.gsk,)#2gsk中国
            yield scrapy.Request(url='https://www.xian-janssen.com.cn/news/type/corporate-news',callback=self.qiangsheng,)#3强生中国
            yield scrapy.Request(url='https://www.takeda.com/zh-cn/news-room/news-releases',callback=self.wutian,)#4武田中国
            yield scrapy.Request(url='http://www.pfizer.cn/(S(sp254l452wzp1xnvbqt2p045))/news/pfizer_press_releases_cn.aspx',callback=self.huirui,)#5辉瑞中国
            yield scrapy.Request(url='https://www.amgen.cn/cn/media/press-release.html',callback=self.anjin,)#6安进中国
            yield scrapy.Request(url='https://www.msdchina.com.cn/media-center/newsroom/',callback=self.moshadong,)#7默沙东中国
            yield scrapy.Request(url='https://www.abbvie.com.cn/pressroom/2019-news-archive1.html',callback=self.abbvie,)#8艾伯维
            yield scrapy.Request(url='https://www.bayer.com.cn/index.php/NewsCenter/allNews',callback=self.baier,)#9拜耳中国
            yield scrapy.Request(url='https://hkexir.beigene.com/cn/press-release/',callback=self.baiji,)#10百济神州
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "ASP.NET_SessionId=nxnwjnpdizthvh0brtxw3bsc",
                "Host": "www.daiichisankyo.com.cn",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
            }
            yield scrapy.Request(url='http://www.daiichisankyo.com.cn/News/newsList.aspx',headers=headers,method="POST",callback=self.first_third,)#11第一三共中国
            yield scrapy.Request(url='https://www.gileadchina.cn/en/news/press-releases',callback=self.jilide,)#12吉利德科学
            yield scrapy.Request(url=f'https://www.boehringer-ingelheim.cn/%E6%96%B0%E9%97%BB%E5%AA%92%E4%BD%93/%E6%9C%80%E6%96%B0%E6%96%B0%E9%97%BB%E7%A8%BF',method='POST',callback=self.bolin,)#13勃林格殷格翰中国
            yield scrapy.Request(url='https://www.novartis.com.cn/xin-wen-zhong-xin/xin-wen-fa-bu',callback=self.nuohua,)#14诺华集团
            yield scrapy.Request(url='https://www.sanofi.cn/zh/media/press-release-center',callback=self.sainuofei,)#15赛诺菲中国

    ## 1中国生物制药
    def china_biology_pharmacy(self,response):
        res = json.loads(response.text)
        for i in res['data']:
            id = i['id']
            title = i['title']
            source = "中国生物制药"
            spider_publish_time_str = i['time']
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://swzy.gf.bj.cn/api.php/content/' + i['id']
            yield scrapy.Request(url, callback=self.china_biology_pharmacy_details, meta={"id":id,"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def china_biology_pharmacy_details(self,response):
            esid = response.meta["esid"]
            url = 'http://www.sinobiopharm.com/index.html#/news/newsdeatil?id=' + response.meta["id"]
            title = response.meta["title"]
            source = "中国生物制药"
            spider_publish_time_str = response.meta["spider_publish_time_str"]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            content = json.loads(response.text)['data']['content']
            src = etree.HTML(content).xpath('//img/@src')
            dic = {}
            for j in src:
                img_src = 'http://www.sinobiopharm.com' + j
                qiniu_url = qiniu(self,dic,img_src,j)
                content = content.replace(j, qiniu_url).strip()
            content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
            insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 2复星医药
    def fosunpharma(self,response):
        doc = pq(response.text)
        title_elements = doc('.listBlock')('li')
        for title_element in title_elements.items():
            title = title_element('.col-sm-10')('p:nth-child(2)').text()
            source = "复星医药"
            spider_publish_time_str = title_element('.col-sm-10')('.color555:first').text().replace('年', '-').replace('月', '-').replace('日', '')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.fosunpharma.com/news/'+title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.fosunpharma_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def fosunpharma_details(self,response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source ="复星医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d")))* 1000
        doc = pq(response.text)
        content = doc('.news_Info')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j,qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 3三生制药
    def sansheng_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.fadeInUp')('li')
        for title_element in title_elements.items():
            title = title_element('h3').text()
            source = "三生制药"
            spider_publish_time_str = title_element('h6').text().replace('年', '-').replace('月', '-')[:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.3sbio.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.sansheng_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def sansheng_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "三生制药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.fckBody')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'https://www.3sbio.com' + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j,qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid,url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 4信达生物
    def innovent_biologics(self, response):
        res = json.loads(response.text)
        for i in res['data']:
            url = 'http://innoventbio.com/#/news/' + str(i['id'])
            title = i['title']
            source = "信达生物"
            spider_publish_time_str = i['created_at']
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d %H:%M:%S"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            content = i['content']
            content_nolabel = ''.join(etree.HTML(content).xpath('//p/text()')).strip()
            insert_es_data(self, esid,url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 5翰森制药
    def hanlin_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.news_lists')('li')
        for title_element in title_elements.items():
            title = title_element('.tit')('div').text()
            source = "翰森制药"
            year = title_element('.year')('div').text()
            month = title_element('.month')('div').text()
            spider_publish_time_str = '{}{}{}'.format(year,'-',month)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://cn.hspharm.com/news/' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.hanlin_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def hanlin_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "翰森制药"
        spider_publish_time_str = response.meta['spider_publish_time_str']
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.myart')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'http://cn.hspharm.com' + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j,qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid,url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 6先声药业
    def first_signs(self, response):
        doc = pq(response.text)
        title_elements = doc('.news1')('li')
        for title_element in title_elements.items():
            title = title_element('.t1')('a').text()
            source = "先声药业"
            day = title_element('.time')('h1').text()
            year_month = title_element('.time')('span').text()
            spider_publish_time_str = '{}{}{}'.format(year_month, '-', day)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.simcere.com/news/' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.first_signs_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def first_signs_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "先声药业"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.new-nr-zi')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'https://www.simcere.com' + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j,qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid,url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 7石药集团
    def shi_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.ratio-img:first')('li')
        for title_element in title_elements.items():
            title = title_element('h2')('a').text()
            source = "石药集团"
            spider_publish_time_str = title_element('div')('span').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.e-cspc.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.shi_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def shi_pharmacy_details(self, response):
        res = response.text
        esid = response.meta["esid"]
        url = response.url
        title = ''.join(etree.HTML(res).xpath('//h1[@class="fnt_40"]/text()'))
        source = "石药集团"
        spider_publish_time_str = ''.join(etree.HTML(res).xpath('//div[@class="btxt"]/span[1]/text()'))[5:]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.edit_con_original')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        for jj in src:
            if 'http' not in jj and '.png' or '.jpg' in jj:
                j = 'http://www.e-cspc.com' + jj
            if '.png' or '.jpg' and 'http' in jj:
                j = ''.join(re.findall(r'.*?png',jj)) + ''.join(re.findall(r'.*?jpg',jj))
            if '.png' or '.jpg' not in jj and 'http' in jj:
                j = jj.replace(".image",".jpg")
            img_src = j
            content = content.replace(jj,img_src)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid,url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 8和黄医药
    def hehaung_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.news-item')
        for title_element in title_elements.items():
            title = title_element('.h24').text()
            source = "和黄医药"
            spider_publish_time_text = title_element('.meta')('div').text()
            spider_publish_time_str = spider_publish_time_text[spider_publish_time_text.rfind("|") + 2:]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('.subcontent')('a').attr('href')
            yield scrapy.Request(url, callback=self.hehaung_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def hehaung_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "和黄医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.textWidget')('div').html()
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 9再鼎医药
    def zaiding_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.newlist')('li')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "再鼎医药"
            spider_publish_time_str = title_element('time').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "http://www.zailaboratory.com" + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.zaiding_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def zaiding_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta['title']
        source = "再鼎医药"
        spider_publish_time_str = response.meta['spider_publish_time_str']
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content')('div').html()
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 10荣昌制药
    def rongchang_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.nynewlist')('li')
        for title_element in title_elements.items():
            title = title_element('h2').text()
            source = "荣昌制药"
            spider_publish_time_str = title_element('a')('span').text()[1:]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.rongchang.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.rongchang_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def rongchang_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "荣昌制药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.newdetanr')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = "http://www.rongchang.com" + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 11绿叶制药
    def green_tree_pharmacy(self, response):
        rese = response.text
        res = etree.HTML(rese).xpath('//div[@class="lists"]/div/@onclick')
        ll = etree.HTML(rese).xpath('//div[@class="inner-left"]/div/text()')
        for i,j in enumerate(res):
            title = ''.join(etree.HTML(rese).xpath('//div[@class="kn1"]/text()')[i]).strip()
            source = "绿叶制药"
            url = 'https://www.luye.cn/lvye/' + j[15:-2]
            year_month = ll.pop(1)
            day = ll.pop(0)
            spider_publish_time_str = year_month + '-' +day
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            yield scrapy.Request(url, callback=self.green_tree_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def green_tree_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "绿叶制药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content-inf')('div').html()
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 12康方生物
    def kangfang_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.company-news-container')('.col-sm-6')
        for title_element in title_elements.items():
            title = title_element('.title')('a').text()
            source = "康方生物"
            spider_publish_time_str = title_element('.published-date').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.akesobio.com' + title_element('.title')('a').attr('href')
            yield scrapy.Request(url, callback=self.kangfang_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def kangfang_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "康方生物"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content')('div').html()
        src = etree.HTML(str(content)).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png',j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg',j))
            img_src = "https://www.akesobio.com" + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 13基石药业
    def footstone_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.s_news')('li')
        for title_element in title_elements.items():
            title = title_element('.title').text()
            source = "基石药业"
            day = title_element('.time')('span').text()
            year_month = title_element('.time')('em').text()
            spider_publish_time_str = '{}{}{}'.format(year_month,'-',day)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.cstonepharma.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.footstone_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def footstone_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta['title']
        source = "基石药业"
        spider_publish_time_str = response.meta['spider_publish_time_str']
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.newssrc')('div').html()
        src = etree.HTML(str(content)).xpath('//p/img/@src')
        dic = {}
        for j in src:
            img_src = "https://www.cstonepharma.com/" + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid,url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 14亚盛医药
    def yasheng_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.blog-post')
        for title_element in title_elements.items():
            title = title_element('.post-title')('a')('span').text()
            source = "亚盛医药"
            spider_publish_time_str = title_element('.post-date').text().replace(' 月 ', '-').replace(', ','-')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%m-%d-%Y"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('h2')('a').attr('href')
            yield scrapy.Request(url, callback=self.yasheng_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def yasheng_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "亚盛医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%m-%d-%Y"))) * 1000
        content = ''.join(re.findall(r'<p>.*?</p>', response.text))
        src = etree.HTML(content).xpath('//p/a/img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 15上海医药
    def shanghai_pharmacy(self, response):
        res = json.loads(response.text)
        for i in res['data']['list']:
            title = i['title']
            source = "上海医药"
            spider_publish_time = i['showtime']*1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            id = i['id']
            url = 'http://www.sphchina.com/api/Public/v1/?service=News.GetNewsInfo&id={}&lang=cn'.format(id)
            yield scrapy.Request(url, callback=self.shanghai_pharmacy_details,meta={"esid":esid,"id":id})
    def shanghai_pharmacy_details(self, response):
        res = json.loads(response.text)
        esid = response.meta["esid"]
        url = 'http://www.sphchina.com/news_center/news_detail.html?id=' + response.meta["id"]
        title = res['data']['current']['title']
        source = "上海医药"
        spider_publish_time_str = res['data']['current']['showtime1']
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        content = res['data']['current']['content']
        src = etree.HTML(content).xpath('//p/img/@src')
        dic = {}
        for j in src:
            img_src = "http://www.sphchina.com" + j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//p/text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 16康哲药业
    def kangzhe_pharmacy(self,response):
        doc = pq(response.text)
        title_elements = doc('.newsList')('li')
        for title_element in title_elements.items():
            title = title_element('h2')('a').text()
            source = "康哲药业"
            spider_publish_time_str = title_element('small').text()[1:-1]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.cms.net.cn/CmsNewWeb/news/'+title_element('h2')('a').attr('href')
            yield scrapy.Request(url,callback=self.kangzhe_pharmacy_details,meta={"esid":esid,"title":title,"spider_publish_time_str":spider_publish_time_str,"spider_publish_time":spider_publish_time})
    def kangzhe_pharmacy_details(self,response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source ="康哲药业"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = response.meta["spider_publish_time"]
        doc = pq(response.text)
        content = doc('#new-content').html()
        src = etree.HTML(content).xpath('//img/@src')
        for jj in src:
            if 'http' in jj:
                j = jj
            if 'http' not in jj:
                j = 'https://www.cms.net.cn' + jj
            img_src = j
            content = content.replace(jj,img_src)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 17康宁杰瑞
    def kangning_pharmacy(self,response):
        doc = pq(response.text)
        title_elements = doc('.s_newslist')('li')
        for title_element in title_elements.items():
            title = title_element('.txt')('span').text()
            source = "康宁杰瑞"
            day = title_element('.time')('span').text()
            year_month = title_element('.time')('em').text().replace(' ','-')
            spider_publish_time_str = '{}{}{}'.format(day,'-',year_month)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%d-%m-%Y"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.alphamabonc.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.kangning_pharmacy_details,meta={"esid": esid, "title": title, "spider_publish_time_str": spider_publish_time_str})
    def kangning_pharmacy_details(self,response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source ="康宁杰瑞"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%d-%m-%Y"))) * 1000
        doc = pq(response.text)
        content = doc('.s_info')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'http://www.alphamabonc.com/'+j
            qiniu_url = qiniu(self,dic,img_src,j)
            content = content.replace(j,qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 18云顶新耀
    def yunding_pharmacy(self,response):
        doc = pq(response.text)
        title_elements = doc('.newslist')('li')
        for title_element in title_elements.items():
            title = title_element('h2')('a').text()
            source = "云顶新耀"
            day = title_element('.date')('span:first').text()
            year_month = title_element('.date')('span:nth-child(2)').text().replace('/', '-')
            spider_publish_time_str = '{}{}{}'.format(day, '-', year_month)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%d-%Y-%m"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.everestmedicines.com/CN/'+title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.yunding_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def yunding_pharmacy_details(self,response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source ="云顶新耀"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%d-%Y-%m"))) * 1000
        doc = pq(response.text)
        content = doc('.news_info_content')('div').html()
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 19远大医药
    def yuanda_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.word-news-show')
        for title_element in title_elements.items():
            title = title_element('h4')('a').text()
            source = "远大医药"
            day = title_element('.left-time')('h4').text()
            year_month = title_element('.left-time')('p').text()
            spider_publish_time_str = '{}{}{}'.format(year_month, '-',day)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.grandpharma.cn' + title_element('h4')('a').attr('href')
            yield scrapy.Request(url, callback=self.yuanda_pharmacy_details, meta={"esid": esid,"spider_publish_time_str": spider_publish_time_str})
    def yuanda_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = ''.join(etree.HTML(response.text).xpath('//h4[@class="font-28"]/text()')).strip()
        source = "远大医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content_elements = doc('.news-details-show')('.clearfix')
        content = content_elements.remove('.jump').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'http://www.grandpharma.cn' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 20药明巨诺
    def junuo_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.item-box')
        for title_element in title_elements.items():
            title = title_element('.title')('a').text()
            source = "药明巨诺"
            spider_publish_time_str = title_element('.date').text().replace('年','-').replace('月','-').replace('日','')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.jwtherapeutics.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.junuo_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def junuo_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "药明巨诺"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = 'https://www.jwtherapeutics.com/' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 21赛生药业
    def shaisheng_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.NewList')
        for title_element in title_elements.items():
            title = title_element('.ListTitle')('h4').text()
            source = "赛生药业"
            year_month = title_element('.SmallNum').text().replace('/','-')
            day = title_element('.BigNum').text()
            spider_publish_time_str = '{}{}{}'.format(year_month,'-',day)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.sciclone.com/Modules/' + title_element('.NewList').attr('onclick')[22:-1]
            yield scrapy.Request(url, callback=self.shaisheng_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def shaisheng_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "赛生药业"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.news-d-main').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.news-d-main').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 22丽珠医药
    def lizhu_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.borderB_default')
        for title_element in title_elements.items():
            title = title_element('.js_coverUrlTitle').text()
            source = "丽珠医药"
            spider_publish_time_str = title_element('.color_assist').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.livzon.com.cn' + title_element('.p_TitleBox')('a').attr('href')
            yield scrapy.Request(url, callback=self.lizhu_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def lizhu_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "丽珠医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.p_articles').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = 'https://www.livzon.com.cn/'+j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.p_articles').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 23加科思
    def jiakesi_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.p_content')('.p_header')
        for title_element in title_elements.items():
            title = title_element('.p_TitleBox')('.p_title').text()
            source = "加科思"
            spider_publish_time_str = title_element('.p_time')('.font').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.jacobiopharma.com' + title_element('.p_TitleBox')('a').attr('href')
            yield scrapy.Request(url, callback=self.jiakesi_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def jiakesi_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "加科思"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.resetHtmlCssStyle div')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = 'http://www.jacobiopharma.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 24华润医药
    def huarun_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.v1_gtgx')('li')
        for title_element in title_elements.items():
            title = title_element('.v1_dtBox').text()
            source = "华润医药"
            spider_publish_time_str = title_element('.yy_view').text().replace('.','-').replace('.','-')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.crpharm.com/xwzx/hryydt' + title_element('.v1_dtBox')('a').attr('href')[1:]
            yield scrapy.Request(url, callback=self.huarun_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def huarun_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "华润医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.TRS_Editor')('div').html()
        content_nolabel = ''.join(etree.HTML(content).xpath('//text()')).strip()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 25德琪医药
    def deqi_pharmacy(self, response):
        url = 'https://www.antengene.cn/news'
        yield scrapy.Request(url, callback=self.deqi_news)
    def deqi_news(self,response):
        doc = pq(response.text)
        title_elements = doc('#ajax_list')('li')
        for title_element in title_elements.items():
            title = title_element('h3').text()
            source = "德琪医药"
            spider_publish_time_str = title_element('.data').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.deqi_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def deqi_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "德琪医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.detail')('div').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.detail')('div').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 26四环医药
    def fourth_ring_pharmacy(self, response):
        res = json.loads(response.text)
        for i in res['data']:
            title = i['name']
            source = "四环医药"
            spider_publish_time_str = i['addtime'][:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            content = i['PDF']
            url = 'https://www.sihuanpharm.com/news/detail0-{}.html'.format(i['id'])
            content_nolabel = ''.join(etree.HTML(str(content)).xpath('//text()')).strip()
            insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 27欧康维视
    def oukang_pharmacy(self, response):
        res = json.loads(response.text)
        for i in res["list"]:
            title = i['title']
            source = "欧康维视"
            spider_publish_time_str = i['publishDate'][:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.ocumension.com/news/' + i['newsGuid']
            yield scrapy.Request(url, callback=self.oukang_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def oukang_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "欧康维视"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.my-12').html()
        content_nolabel = doc('.my-12').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 28诺诚健华
    def nuocheng_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.media-item')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "诺诚健华"
            spider_publish_time_str = title_element('.date').text().replace('年','-').replace('月','-').replace('日','')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://cn.innocarepharma.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.nuocheng_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def nuocheng_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "诺诚健华"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.current-news-content').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = 'https://cn.innocarepharma.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.current-news-content').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 29康希诺生物
    def kangxinuo_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.TrendsList')('li')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "康希诺生物"
            spider_publish_time_str = title_element('.date').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.kangxinuo_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def kangxinuo_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "康希诺生物"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.NewsContent').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.NewsContent').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 30和铂医药
    def hebai_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('#ajax_list')('li')
        for title_element in title_elements.items():
            title = title_element('h3').text()
            source = "和铂医药"
            spider_publish_time_str = title_element('.data').text().replace('年','-').replace('月','-').replace('日','')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.harbourbiomed.com/' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.hebai_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def hebai_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "和铂医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.detailed').html()
        content_nolabel = doc('.detailed').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 31歌礼制药
    def geli_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.news_bottom')('ul')('li')
        for title_element in title_elements.items():
            title = title_element('span').text()
            source = "歌礼制药"
            spider_publish_time_str = title_element('h3').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.ascletis.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.geli_pharmacy_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def geli_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "歌礼制药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.team_text').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'https://www.ascletis.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.team_text').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 32恒瑞医药
    def hengrui_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.ggtj_top')
        for title_element in title_elements.items():
            title = title_element('.ggtj_top_right_title').text()
            source = "恒瑞医药"
            spider_publish_time_str = title_element('.ggtj_top_right_date').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.hrs.com.cn' + title_element('.pull-left_1').attr('href')
            yield scrapy.Request(url, callback=self.hengrui_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def hengrui_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "恒瑞医药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.detailsPage-content').html()
        src = etree.HTML(content).xpath('//img/@src')
        for j in src:
            img_src = 'https://www.hrs.com.cn' + j
            content = content.replace(j, img_src)
        content_nolabel = doc('.detailsPage-content').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 33君实生物
    def junshi_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.effect-2')('li')
        for title_element in title_elements.items():
            title = title_element('h3').text()
            source = "君实生物"
            year = title_element('.time')('span').text()
            month_day = title_element('.time div:first').text()
            spider_publish_time_str ='{}{}{}'.format(year,'-',month_day)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.junshipharma.com/tools/submit_ajax.ashx?action=get_News&article_id=' + title_element('li').attr('onclick')[6:-1]
            yield scrapy.Request(url, callback=self.junshi_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def junshi_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "君实生物"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.modal-body').html()
        content_nolabel = doc('.modal-body').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 34贝达药业
    def beida_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.list-c')('.list')
        for title_element in title_elements.items():
            title = title_element('a').text()[2:]
            source = "贝达药业"
            spider_publish_time_str = title_element('.r').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.bettapharma.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.beida_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def beida_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "贝达药业"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('#noshowimgt').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'http://www.bettapharma.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('#noshowimgt').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 35天士力
    def tianshili_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.newslist')('li')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "天士力"
            spider_publish_time_str = title_element('.date').text()[1:-1]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.tianshili_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def tianshili_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "天士力"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.col-md-9').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.col-md-9').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 36泽璟制药
    def zejing_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.nynewslist')('ul')('li')
        for title_element in title_elements.items():
            title = title_element('h2').text()
            source = "泽璟制药"
            spider_publish_time_str = title_element('.newsdate')('p').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'http://www.zelgen.com' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.zejing_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def zejing_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = ''.join(etree.HTML(response.text).xpath('//div[@class="nynews warp"]/div/h1/text()')).strip()
        source = "泽璟制药"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'http://www.zelgen.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.content').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 37百奥泰
    def baiaotai_pharmacy(self, response):
        rese = response.text
        res = re.findall(r'/plus/view.php.*?"', rese)
        ss = set()
        for i in res:
            ss.add(i)
        for j in ss:
            url = 'https://www.bio-thera.com' + j[:-1]
            yield scrapy.Request(url, callback=self.baiaotai_pharmacy_details,)
    def baiaotai_pharmacy_details(self, response):
        url = response.url
        title = ''.join(etree.HTML(response.text).xpath('//header[@class="title"]/h1/text()')).strip()
        source = "百奥泰"
        spider_publish_time_str = ''.join(etree.HTML(response.text).xpath('//header[@class="title"]/p/span[1]/text()')).strip()[5:]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
        if check_es_data(self,esid):
            return
        doc = pq(response.text)
        content = doc('.info').html()
        content_nolabel = doc('.info').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 38微芯生物
    def weixin_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.news-list')('a')
        for title_element in title_elements.items():
            title = title_element('h4').text()
            source = "微芯生物"
            month_day =  title_element('.date')('h5').text()
            year = title_element('.date')('p').text()[1:]
            spider_publish_time_str = '{}{}{}'.format(year,'-',month_day)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.chipscreen.com/' + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.weixin_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def weixin_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "微芯生物"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'Uploads/image' in j:
                j = j
            else:
                j = '123'
            img_src = 'https://www.chipscreen.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.content').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 39海和生物
    def haihe_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.wap1600')('.xwListLb')('li')
        for title_element in title_elements.items():
            title = title_element('.xwListLb03')('a').text()
            source = "海和生物"
            spider_publish_time_str = title_element('.xwListLb02').text().replace('.','-').replace('.','-')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.haihepharma.com' + title_element('.xwListLb01')('a').attr('href')
            yield scrapy.Request(url, callback=self.haihe_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def haihe_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "海和生物"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.xwContentA').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'https://www.haihepharma.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.xwContentA').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 40冠科美博
    def guanke_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.fl-post-feed')('.fl-post-feed-post')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "冠科美博"
            spider_publish_time_str = title_element('h2').text().replace('.', '-').replace('.', '-')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.guanke_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def guanke_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "冠科美博"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content_elements = doc('.fl-module-fl-post-content')('div')
        content = content_elements.remove('table').html()
        content_nolabel = doc('.fl-module-fl-post-content')('div').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 41北海康成
    def beihai_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('.newentry')('li')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "北海康成"
            spider_publish_time_str = title_element('.newtime').text().replace('年','-').replace('月','-').replace('日','')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.beihai_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def beihai_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "北海康成"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.ndbox').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = 'http://www.canbridgepharma.com' + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.ndbox').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 42天境生物
    def tianjing_pharmacy(self, response):
        doc = pq(response.text)
        title_elements = doc('#row2')('.list-h1')('li')
        for title_element in title_elements.items():
            title = title_element('h3')('a').text()
            source = "天境生物"
            spider_publish_time_str = title_element('.date1').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.i-mabbiopharma.com/cn/' + title_element('h3')('a').attr('href')
            yield scrapy.Request(url, callback=self.tianjing_pharmacy_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str})
    def tianjing_pharmacy_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "天境生物"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.m-txt1').html()
        content_nolabel = doc('.m-txt1').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 1美通社中国
    def meitongshe(self, response):
        doc = pq(response.text)
        title_elements = doc('.width-large')('.card-text-wrap')
        for title_element in title_elements.items():
            title = title_element('h3').text()
            source = "美通社中国"
            spider_publish_time_str = title_element('div')('span').text()[:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('h3')('a').attr('href')
            yield scrapy.Request(url, callback=self.meitongshe_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def meitongshe_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "美通社中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content= doc('#dvContent')
        src = etree.HTML(str(content)).xpath('//img/@src')
        dic = {}
        for jj in src:
            if 'png' in jj:
                j = ''.join(re.findall(r'.*?png', jj))
            if 'jpg' in jj:
                j = ''.join(re.findall(r'.*?jpg', jj))
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j,src_index=-7)
            content = str(content).replace(jj, qiniu_url)
        content_nolabel = doc('#dvContent').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 2gsk中国
    def gsk(self, response):
        doc = pq(response.text)
        title_elements = doc('.listing-item')
        for title_element in title_elements.items():
            title = title_element('h3')('a').text()
            source = "gsk中国"
            spider_publish_time_str = title_element('time').attr('datetime').split(" ")[0].replace("/","-").replace("/","-")
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.gsk-china.com' + title_element('h3')('a').attr('href')
            yield scrapy.Request(url, callback=self.gsk_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def gsk_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "gsk中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.body-content')('p')
        src = etree.HTML(str(content)).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = "https://www.gsk-china.com" + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = str(content).replace(j, qiniu_url)
        content_nolabel = doc('.body-content').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 3强生中国
    def qiangsheng(self, response):
        doc = pq(response.text)
        title_elements = doc('.news-type-list')('.views-row')
        for title_element in title_elements.items():
            title = title_element('a:first').text()
            source = "强生中国"
            spider_publish_time_str = title_element('.date-display-single').text().replace('/','-').replace('/','-')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = 'https://www.xian-janssen.com.cn' + title_element('a:first').attr('href')
            yield scrapy.Request(url, callback=self.qiangsheng_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def qiangsheng_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "强生中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.content-middle').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = "https://www.xian-janssen.com.cn" + j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.content-middle').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 4武田中国
    def wutian(self, response):
        doc = pq(response.text)
        title_elements = doc('.news-list__content__item')
        for title_element in title_elements.items():
            title = title_element('a:first').text()
            source = "武田中国"
            spider_publish_time_str = title_element('.hide-on-desktop-inline').text().replace('/','-').replace('/','-')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a:first').attr('href')
            yield scrapy.Request(url, callback=self.wutian_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def wutian_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "武田中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.mainBody').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.mainBody').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 5辉瑞中国
    def huirui(self, response):
        doc = pq(response.text)
        title_elements = doc('#news_nav')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "辉瑞中国"
            spider_publish_time_str = title_element('.date').text().replace('年','-').replace('月','-').replace('日','')
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "http://www.pfizer.cn/(S(2pfnsd553yrsru55npkbnxzl))/news/" + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.huirui_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def huirui_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "辉瑞中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content_elements = doc('#news_content')
        content_elements = content_elements.remove('.date')
        content_elements = content_elements.remove('li:first')
        content = content_elements.html()
        content_nolabel = doc('#news_content').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 6安进中国
    def anjin(self, response):
        doc = pq(response.text)
        title_elements = doc('.articles-by-month')('span')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "安进中国"
            date = title_element('p:first').text().strip().replace(", ","-").replace("，","-").replace(",","-").split(" ")
            month = date[0].replace('.','')
            month_num = china_num(month)
            day_year = date[1][:7].strip()
            spider_publish_time_str = '{}{}{}'.format(month_num,'-',day_year)
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%m-%d-%Y"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.amgen.cn/cn/media/" + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.anjin_details,meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def anjin_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "安进中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%m-%d-%Y"))) * 1000
        doc = pq(response.text)
        content_elements = doc('.Content')
        content_elements.remove('p:first')
        content_elements.remove('p:first')
        content_elements.remove('center')
        content_elements.remove('center')
        content = content_elements
        content_nolabel = doc('.Content').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 7默沙东中国
    def moshadong(self, response):
        doc = pq(response.text)
        title_elements = doc('#ul_zc_mediacenter_newslist')('li')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "默沙东中国"
            spider_publish_time_str = title_element('li:first').text()[:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.msdchina.com.cn" + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.moshadong_details,meta={"esid": esid,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def moshadong_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = ''.join(etree.HTML(response.text).xpath('//h3/strong/text()')).strip()
        source = "默沙东中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('p')
        content_nolabel = doc('p').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 8艾伯维
    def abbvie(self, response):
        res = response.xpath('//div[@class="text"]/div/p/a/@href')
        for i,j in enumerate(res):
            try:
                spider_publish_time_str = ''.join(etree.HTML(response.text).xpath('//div[@class="heading"]/p/text()')[i]).strip().replace("年","-").replace("月","-").replace("日","")
            except:
                spider_publish_time_str = ''.join(etree.HTML(response.text).xpath('//div[@class="heading"]/p/text()')[i-5]).strip().replace("年","-").replace("月","-").replace("日","")
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            title = response.xpath('//div[@class="text"]/div/p/a/text()')[i].extract()
            source = "艾伯维"
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.abbvie.com.cn" + response.xpath('//div[@class="text"]/div/p/a/@href')[i].extract()
            yield scrapy.Request(url, callback=self.abbvie_details,meta={"esid": esid,"title":title ,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def abbvie_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "艾伯维"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.parsys')('p')
        content_nolabel = doc('.parsys').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 9拜耳中国
    def baier(self, response):
        doc = pq(response.text)
        title_elements = doc('.mediatips')('ul')('li')
        for title_element in title_elements.items():
            title = title_element('a:first').text()
            source = "拜耳中国"
            spider_publish_time_str = title_element('div:first').text()[:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.bayer.com.cn" + title_element('a:first').attr('href')
            yield scrapy.Request(url, callback=self.baier_details,meta={"esid": esid,"title":title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def baier_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = ''.join(etree.HTML(response.text).xpath('//div[@class="DetailHeadline"]/text()')).strip()
        source = "拜耳中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.DetailBody').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = "https://www.bayer.com.cn" + j
            # qiniu_url = qiniu(self, dic, img_src, j,)
            content = content.replace(j, img_src)
        content_nolabel = doc('.DetailBody').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 10百济神州
    def baiji(self, response):
        doc = pq(response.text)
        title_elements = doc('.press-release-item')
        for title_element in title_elements.items():
            title = title_element('h3').text()
            source = "百济神州"
            spider_publish_time_str = title_element('li').text()[:10].strip().replace("年","-").replace("月","-").replace("日","")
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            j= title_element('a').attr('href')
            pdf_url = "https://hkexir.beigene.com" + title_element('a').attr('href')
            dic = {}
            dic["file_name"] = j[j.rfind("/"):].replace('/', '').replace('_', '').replace('-', '')
            dic["file_url"] = pdf_url
            self.file_utils.download_file(dic)
            file_name = dic['file_name']
            local_file_path = f'{"E:/workspace/pharmcube-spider-platform/shijin/flash_news/flash_news/temporary_file/"}{file_name}'
            self.pdf_utils.check_pdf(local_file_path)
            pdf_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_name, is_keep_file=False)
            es_dict = {}
            es_dict["esid"] = esid
            es_dict["url"] = pdf_url
            es_dict["title"] = title
            es_dict["source"] = source
            es_dict["channel_name"] = "医药自媒体"
            es_dict["spider_publish_time_str"] = spider_publish_time_str
            es_dict["spider_publish_time"] = spider_publish_time
            es_dict["spider_wormtime"] = int(time.time()) * 1000
            # print(es_dict)
            self.es_utils.update_or_insert('news', d=es_dict)
            # logging.info("------- insert es data -------" + esid + title)
            self.redis_server.lpush(RedisKey.NEWS_LIST, esid)

    ## 11第一三共中国
    def first_third(self, response):
        doc = pq(response.text)
        title_elements = doc('.newslist')('li')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "第一三共中国"
            spider_publish_time_str = title_element('span').text()
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "http://www.daiichisankyo.com.cn/News/" + title_element('a').attr('href')
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "ASP.NET_SessionId=nxnwjnpdizthvh0brtxw3bsc",
                "Host": "www.daiichisankyo.com.cn",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
            }
            yield scrapy.Request(url,headers=headers ,callback=self.first_third_details,meta={"esid": esid,"title":title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def first_third_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "第一三共中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.storytopleft').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'http' in j:
                img_src = j
            if 'http' not in j:
                img_src = 'http://www.daiichisankyo.com.cn/' + j
            img_src = img_src
            qiniu_url = qiniu(self, dic, img_src, j,)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.storytopleft').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 12吉利德科学
    def jilide(self, response):
        doc = pq(response.text)
        title_elements = doc('.Press-Release-List')
        for title_element in title_elements.items():
            title = title_element('a').text()
            source = "吉利德科学"
            spider_publish_time_str = title_element('span').text().replace("/","-").replace("/","-")
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%m-%d-%Y"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.gileadchina.cn" + title_element('a').attr('href')
            yield scrapy.Request(url, callback=self.jilide_details, meta={"esid": esid, "title": title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def jilide_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = ''.join(etree.HTML(response.text).xpath('//h2[@class="body-title"]/text()')).strip()
        source = "吉利德科学"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%m-%d-%Y"))) * 1000
        doc = pq(response.text)
        content_elements = doc('.center-without-sidebar')
        content_elements.remove('h2')
        content_elements.remove('div')
        content = content_elements.html()
        content = content.replace('amp;','')
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for jj in src:
            if 'http' in jj:
                j = jj
            if 'http' not in jj:
                j = "https://www.gileadchina.cn" + ''.join(re.findall(r'.*?jpg', jj)) + ''.join(re.findall(r'.*?png', jj))
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j,)
            content = content.replace(jj, qiniu_url)
        content_nolabel = content_elements.text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 13勃林格殷格翰中国
    def bolin(self, response):
        doc = pq(response.text)
        title_elements = doc('.masonry-item')('.-nd-tiles-text')
        for title_element in title_elements.items():
            title = title_element('a:first').text()
            source = "勃林格殷格翰中国"
            old_year = title_element('.-nd-tiles-timestamp').text()
            day = title_element('.-nd-tiles-timestamp').text()[:2]
            month = title_element('.-nd-tiles-timestamp').text()[2:6].strip()
            month = china_num(month)
            if '十一月' in old_year:
                year = old_year[7:11]
            elif '十二月' in old_year:
                year = old_year[7:11]
            else:
                year = old_year[6:10]
            spider_publish_time_str = '{}{}{}{}{}'.format(year,'-',month,'-',day)
            if 'None' in spider_publish_time_str:
                spider_publish_time_str = time.strftime("%Y-%m-%d", time.localtime())
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = title_element('a:first').attr('href')
            yield scrapy.Request(url, callback=self.bolin_details,method='POST',meta={"esid": esid,"title":title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def bolin_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "勃林格殷格翰中国"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content1 = doc('.field--type-text-with-summary')('.field__item')('li')
        content2 = doc('.field--type-text-with-summary')('.field__item')('p')
        content = '{}{}'.format(content1,content2)
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            if 'png' in j:
                j = ''.join(re.findall(r'.*?png', j))
            if 'jpg' in j:
                j = ''.join(re.findall(r'.*?jpg', j))
            img_src = "https://www.boehringer-ingelheim.cn" + j
            qiniu_url = qiniu(self, dic, img_src, j,)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.field--type-text-with-summary').text()
        insert_es_data(self, esid, url, title, source, str(content), content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 14诺华集团
    def nuohua(self, response):
        doc = pq(response.text)
        title_elements = doc('.views-row')
        for title_element in title_elements.items():
            title = title_element('h4')('a').text()
            source = "诺华集团"
            spider_pub_time= title_element('.teaser')('.date')('span').text().replace(", ","-").replace("月 ","-")
            spider_publish_time_str = spider_pub_time[:spider_pub_time.rfind(" -")]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.novartis.com.cn" + title_element('h4')('a').attr('href')
            yield scrapy.Request(url, callback=self.nuohua_details,meta={"esid": esid,"title":title,"spider_publish_time_str": spider_publish_time_str},priority=100)
    def nuohua_details(self, response):
        esid = response.meta["esid"]
        url = response.url
        title = response.meta["title"]
        source = "诺华集团"
        spider_publish_time_str = response.meta["spider_publish_time_str"]
        spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
        doc = pq(response.text)
        content = doc('.field-type-text-with-summary')('.field-items')('.field-item').html()
        src = etree.HTML(content).xpath('//img/@src')
        dic = {}
        for j in src:
            img_src = j
            qiniu_url = qiniu(self, dic, img_src, j,)
            content = content.replace(j, qiniu_url)
        content_nolabel = doc('.field-item').text()
        insert_es_data(self, esid, url, title, source, content, content_nolabel, spider_publish_time_str,spider_publish_time)

    ## 15赛诺菲中国
    def sainuofei(self, response):
        doc = pq(response.text)
        title_elements = doc('.osw-pagelist-element-middle')
        for title_element in title_elements.items():
            title = title_element('.osw-pagelist-title').text()
            source = "赛诺菲中国"
            spider_publish_time_str = title_element('.osw-js-date').text().replace(".", "-").replace(".", "-")[:10]
            spider_publish_time = int(time.mktime(time.strptime(spider_publish_time_str, "%Y-%m-%d"))) * 1000
            esid = self.md5_utils.get_md5(title + source + str(spider_publish_time))
            if check_es_data(self,esid):
                continue
            url = "https://www.sanofi.cn" + title_element('a').attr('href')
            j = ''.join(re.findall(r'.*?pdf', title_element('a').attr('href')))
            pdf_url = ''.join(re.findall(r'.*?pdf', url))
            dic = {}
            dic["file_name"] = j[j.rfind("/"):].replace('/', '').replace('_', '').replace('-', '')
            dic["file_url"] = pdf_url
            self.file_utils.download_file(dic)
            file_name = dic['file_name']
            local_file_path = f'{"E:/workspace/pharmcube-spider-platform/shijin/flash_news/flash_news/temporary_file/"}{file_name}'
            self.pdf_utils.check_pdf(local_file_path)
            pdf_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_name, is_keep_file=False)
            es_dict = {}
            es_dict["esid"] = esid
            es_dict["url"] = pdf_url
            es_dict["title"] = title
            es_dict["source"] = source
            es_dict["channel_name"] = "医药自媒体"
            es_dict["spider_publish_time_str"] = spider_publish_time_str
            es_dict["spider_publish_time"] = spider_publish_time
            es_dict["spider_wormtime"] = int(time.time()) * 1000
            # print(es_dict)
            self.es_utils.update_or_insert(index=ESIndex.NEWS, d=es_dict)
            # logging.info("------- insert es data -------" + esid + title)
            self.redis_server.lpush(RedisKey.NEWS_LIST, esid)


def china_num(month):
    if '一月' == month:
        return 1
    if '二月' == month:
        return 2
    if '三月' in month:
        return 3
    if '四月' in month:
        return 4
    if '五月' in month:
        return 5
    if '六月' in month:
        return 6
    if '七月' in month:
        return 7
    if '八月' in month:
        return 8
    if '九月' in month:
        return 9
    if '十月' in month:
        return 10
    if '十一月' in month:
        return 11
    if '十二月' in month:
        return 12

def mon_eng_china(mon_eng):
    if 'Jan' in mon_eng:
        return 1
    if 'Feb' in mon_eng:
        return 2
    if 'Mar' in mon_eng:
        return 3
    if 'Apr' in mon_eng:
        return 4
    if 'May' in mon_eng:
        return 5
    if 'Jun' in mon_eng:
        return 6
    if 'Jul' in mon_eng:
        return 7
    if 'Aug' in mon_eng:
        return 8
    if 'Sep' in mon_eng:
        return 9
    if 'Oct' in mon_eng:
        return 10
    if 'Nov' in mon_eng:
        return 11
    if 'Dec' in mon_eng:
        return 12

def qiniu(self,dic,img_src,j,src_index=1):
    dic["file_name"] = j[j.rfind("/")+src_index:].replace('/','').replace('_','').replace('-','')
    dic["file_url"] = img_src
    self.file_utils.download_file(dic)
    file_name = dic['file_name']
    local_file_path = f'{"E:/workspace/pharmcube-spider-platform/shijin/flash_news/flash_news/temporary_file/"}{file_name}'
    self.pdf_utils.check_pdf(local_file_path)
    qiniu_url = qiniu_utils.up_qiniu(local_file_path, file_name=file_name, is_keep_file=False)
    return qiniu_url

def check_es_data(self,esid):
    es_count = self.es_utils.get_exist(ESIndex.NEWS, esid)
    if es_count > 0:
        logging.info('------- 当前文章已采集，被过滤es数据库 ------- ' + esid )
        return True
    return False

def insert_es_data(self,esid,url,title,source,content,content_nolabel,spider_publish_time_str,spider_publish_time):
    es_dict = {}
    es_dict["esid"] = esid
    es_dict["url"] = url
    es_dict["title"] = title
    es_dict["source"] = source
    es_dict["channel_name"] = "医药自媒体"
    es_dict["spider_publish_time_str"] = spider_publish_time_str
    es_dict["spider_publish_time"] = spider_publish_time
    es_dict["spider_wormtime"] = int(time.time()) * 1000
    es_dict["content"] = content.replace('\n','').replace('\r','').replace('<br>','').replace('<br />','').strip()
    es_dict["content_nolabel"] = content_nolabel.replace('\r',  '').replace('\n', '<br/>').replace('<br>','').strip()
    # print(es_dict)
    self.es_utils.update_or_insert(index=ESIndex.NEWS, d=es_dict)
    logging.info("------- insert es data -------" + esid + title)
    # self.redis_server.lpush(RedisKey.NEWS_LIST,esid)

