
import logging
import os
import ast
import scrapy
from pyquery import PyQuery as pq
from pharmcube_spider import const
from pharmcube_spider.const import MongoTables, ESIndex, RedisKey
from pharmcube_spider.utils import es_utils, qiniu_utils
from pharmcube_spider.utils.date_utils import DateUtils
from pharmcube_spider.utils.es_utils import Query, QueryType
from pharmcube_spider.utils.file_utils import DownloadFile
from pharmcube_spider.utils.md5_utils import MD5Utils
from pharmcube_spider.utils.mongo_utils import MongoUtils
from pharmcube_spider.utils.str_utils import StrUtils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings


'''
从微信公众号平台获取链接后采集详情页的文章
'''


redis_server = from_settings(get_project_settings())


def delete_mongo_data(self, esid):
    mongo_query = {}
    mongo_query['esid'] = esid
    logging.info(f'------- delete mongo data ------- {esid}')
    self.mongo_utils.delete_one(query=mongo_query, coll_name=MongoTables().SPIDER_WECHAT_MP_TITLE)

def insert_es_data(self, esid, title, url, publish_time, content, position, is_original, original_str, wechat_official_accounts_desc):
    es_data = {}
    es_data['url'] = url
    es_data['esid'] = esid
    es_data['title'] = title
    es_data['state'] = '正常'
    es_data['is_delete'] = '否'
    es_data['level'] = 1
    es_data['status'] = 1
    es_data['channel_ids'] = [64]
    es_data['content'] = content
    es_data['position'] = position
    es_data['is_original'] = is_original
    es_data['original_str'] = original_str
    es_data['spider_publish_time'] = publish_time
    es_data['channel_name'] = '医药自媒体'
    es_data['spider_wormtime'] = DateUtils().get_timestamp()
    es_data['source'] = wechat_official_accounts_desc
    if es_utils.insert_or_replace(index=ESIndex.NEWS, d=es_data):
        logging.info(f'------- insert es data success ------- {esid} {title} {DateUtils().defined_format_time(timestamp=publish_time, format="%Y-%m-%d")}')
        delete_mongo_data(self=self, esid=esid)
    else:
        logging.info(f'------- insert es data error ------- {esid} {title} {DateUtils().defined_format_time(timestamp=publish_time, format="%Y-%m-%d")}')

def insert_mongo_data(self,esid, title, link, publish_time, position, wechat_official_accounts_desc):
    mongo_data = {}
    mongo_data['esid'] = esid
    mongo_data['link'] = link
    mongo_data['title'] = title
    mongo_data['position'] = position
    mongo_data['publish_time'] = publish_time
    mongo_data['spider_wormtime'] = DateUtils().get_timestamp()
    mongo_data['wechat_official_accounts_desc'] = wechat_official_accounts_desc
    logging.info(f'------- 备份待采集的URL ------- {esid} \t {title}')
    self.mongo_utils.insert_one(mongo_data=mongo_data, coll_name=MongoTables().SPIDER_WECHAT_MP_TITLE)

def check_es_data(self, esid, title, publish_time):
    es_count = es_utils.get_count(ESIndex.NEWS, queries=Query(QueryType.EQ, 'esid', esid))
    if es_count > 0:
        delete_mongo_data(self, esid)
        logging.info('------- 当前微信公众号文章已采集，被过滤 ------- ' + title + '\t' + DateUtils().defined_format_time(timestamp=publish_time, format="%Y-%m-%d"))
        return True
    return False

def get_position(spider_publish_time, position_dict):
    position = 1
    if spider_publish_time not in position_dict:
        position_dict[spider_publish_time] = 1
    else:
        position = position_dict[spider_publish_time] + 1
        position_dict[spider_publish_time] = position
    return position

class WechatMpSpider(scrapy.Spider):
    name = 'wechat_mp'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.mongo_utils = MongoUtils()
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            if redis_server.llen(RedisKey.WECHAT_MP_TITLE) == 0 and self.mongo_utils.get_count(coll_name=MongoTables().SPIDER_WECHAT_MP_TITLE)==0:
                logging.info('------- 当前没有要采集的微信公众号文章链接，程序终止更新 -------')
                return
            if self.mongo_utils.get_count(coll_name=MongoTables().SPIDER_WECHAT_MP_TITLE) > 0 :
                mongo_all_data = self.mongo_utils.find_all(coll_name=MongoTables().SPIDER_WECHAT_MP_TITLE)
                for mongo_data in mongo_all_data:
                    esid = mongo_data['esid']
                    title = mongo_data['title']
                    position = mongo_data['position']
                    publish_time = mongo_data['publish_time']
                    wechat_official_accounts_desc = mongo_data['wechat_official_accounts_desc']
                    if check_es_data(self=self, esid=esid, title=title, publish_time=publish_time):
                        continue
                    link = mongo_data['link']
                    logging.info(f'追加待采集的URL {title} {link}')
                    yield scrapy.Request(link, callback=self.parse, meta={'esid': esid, 'title': title, 'position': position, 'publish_time': publish_time, 'wechat_official_accounts_desc': wechat_official_accounts_desc}, headers=const.headers)


            while redis_server.llen(RedisKey.WECHAT_MP_TITLE) > 0:
                wechat_mp_info = {}
                mongo_all_data = self.mongo_utils.find_all(coll_name=MongoTables.SPIDER_WECHAT_MP)
                for mongo_data in mongo_all_data:
                    __biz = mongo_data['__biz']
                    wechat_official_accounts_desc = mongo_data['wechat_official_accounts_desc']
                    wechat_mp_info[__biz] = wechat_official_accounts_desc
                results = ast.literal_eval(redis_server.rpop(RedisKey.WECHAT_MP_TITLE).decode().replace('true', 'True').replace('false', 'False').replace('null', 'None'))
                position_dict = {}
                for result in results:
                    link = result['link'].replace('http:', 'https:')
                    __biz = link[link.index('__biz=') + 6:link.index('&mid')]
                    wechat_official_accounts_desc = wechat_mp_info[__biz]
                    title = result['title']
                    publish_time = result['create_time'] * 1000
                    spider_publish_time = DateUtils().defined_format_time(timestamp=publish_time, format='%Y-%m-%d')
                    position = get_position(spider_publish_time, position_dict)
                    esid = MD5Utils().get_md5(title + str(publish_time))
                    if check_es_data(self=self, esid=esid, title=title, publish_time=publish_time):
                        continue
                    insert_mongo_data(self, esid, title, link, publish_time, position, wechat_official_accounts_desc)
                    logging.info(f'追加待采集的URL {title} {link}')
                    yield scrapy.Request(link, callback=self.parse, meta={'esid': esid, 'title': title, 'position': position, 'publish_time': publish_time, 'wechat_official_accounts_desc': wechat_official_accounts_desc}, headers=const.headers)

        if 'weixin.qq.com' in spider_url:
            esid = response.meta['esid']
            title = response.meta['title']
            position = response.meta['position']
            publish_time = response.meta['publish_time']
            wechat_official_accounts_desc = response.meta['wechat_official_accounts_desc']
            doc = pq(response.text)
            if doc('#js_share_source').size() > 0:
                logging.info(f'------- 当前公众号分享了一篇文章，需要二次跳转 -------{esid}\t{title}\t{spider_url}')
                href = doc('#js_share_source')('a').attr('href')
                logging.info(f'追加二次跳转的URL {title} {href}')
                yield scrapy.Request(href, callback=self.parse, meta={'esid': esid, 'title': title, 'position': position,'publish_time': publish_time,'wechat_official_accounts_desc': wechat_official_accounts_desc},headers=const.headers)
                return

            content = doc('#js_content').html()
            if StrUtils().is_blank(content) and doc('#js_mpvedio').size() > 0:
                logging.error(f'------- 当前公众号文章为纯视频内容，被过滤 -------{spider_url}')
                delete_mongo_data(self, esid)
                return

            if (None==content) or ('内容因涉嫌违反相关法律' in doc('.weui-msg__desc').text()):
                err_meta = response.meta
                err_meta['url'] = spider_url
                delete_mongo_data(self, esid)
                logging.error(f'------- 当前公众号文章异常，被过滤 -------{str(err_meta)}')
                return

            wait_img_urls = []
            img_elements = pq(content)('img')
            for img in img_elements:
                img_url = ''
                if 'data-src' in img.attrib:
                    img_url = img.attrib['data-src']
                else:
                    img_url = img.attrib['src']
                file_name = MD5Utils().get_md5(img_url) + '.png'
                if not img_url.startswith('http'):
                    img_url = 'https://mmbiz.qpic.cn'+img_url
                wait_img_url = {}
                wait_img_url['file_name'] = file_name
                wait_img_url['file_url'] = img_url
                wait_img_urls.append(wait_img_url)
            # 异步下载文件
            if len(wait_img_urls) > 0:
                DownloadFile().download_file(wait_img_urls)
            #校验文件是否下载到本地
            for local_file_name in wait_img_urls:
                file_url = local_file_name['file_url']
                file_name = local_file_name['file_name']
                local_file_path = f'{const.STORE_PATH}{file_name}'
                if os.path.exists(os.path.join(local_file_path)):
                    qiniu_url = qiniu_utils.up_qiniu(const.STORE_PATH+file_name, file_name=file_name, is_keep_file=False)
                    if 'pharmcube' in qiniu_url:
                        content = content.replace(file_url, qiniu_url)
            content = content.replace('data-src', 'src')
            logging.info(f'-------- 页面下载成功 {esid}-------')
            is_original = 0 #默认值：不是原创
            original_str = doc('#copyright_logo').text()
            if '原创' == original_str:
                is_original = 1
            insert_es_data(self, esid=esid, title=title, url=spider_url, publish_time=publish_time, content=content, position=position, is_original=is_original, original_str=original_str, wechat_official_accounts_desc=wechat_official_accounts_desc)

