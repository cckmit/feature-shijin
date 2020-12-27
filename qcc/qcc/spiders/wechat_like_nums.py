
import ast
import scrapy
import logging
from qcc.utils import es_utils
from qcc.utils.date_utils import DateUtils
from qcc.utils.es_utils import Query, QueryType
from scrapy.utils.project import get_project_settings
from qcc.spiders.const import RedisKey, ESIndex, PAGEOPS
from scrapy_redis_cluster.connection import from_settings

'''
采集微信公众号文章对应的点赞数与阅读数
'''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
}

class WechatLikeNumsSpider(scrapy.Spider):
    name = 'wechat_like_nums'
    allowed_domains = []
    start_urls = ['https://www.baidu.com/']

    def start_requests(self):
        self.es_utils = es_utils
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        if 'baidu.com' in spider_url:
            yield from read_wait_like_nums(self, scrapy)

        if 'weixin.qq.com' in spider_url:
            esid = response.meta['esid']
            __biz = response.meta['__biz']
            results = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
            logging.info(f'===>{results}')
            if 'appmsgstat' not in results:
                logging.info(f'-------- 当前文章获取点赞数失败，被过滤 -------{esid}')
            else:
                # 提取其中的阅读数和点赞数
                if not results["appmsgstat"]['show']:
                    logging.info(f'当前微信公众号文章不显示点赞数和阅读数{__biz} {esid}')
                    return
                read_num = results["appmsgstat"]["read_num"]
                like_num = results["appmsgstat"]["like_num"]
                logging.info(f'当前微信公众号文章点赞数 {like_num} 和阅读数 {read_num} {__biz} {esid}')
                update_es_dict = {}
                update_es_dict['esid'] = esid
                update_es_dict['read_num'] = read_num
                update_es_dict['like_num'] = like_num
                logging.info(f'------- 更新微信文章阅读数 -------{esid} {read_num} {like_num}')
                self.es_utils.update(ESIndex.NEWS, d=update_es_dict)

def split_url(url):
    results_dict = {}
    splits_1 = url.split('&')
    for split in splits_1:
        if '__biz' in split:
            results_dict['__biz'] = split[split.index('__biz=') + 6:]
            continue
        results_dict[split.split('=')[0]] =  split.split('=')[1]
    return results_dict

def read_wait_like_nums(self, scrapy):
    like_nums = self.redis_server.llen(RedisKey.WECHAT_MP_LIKE_NUMS)
    if like_nums == 0:
        logging.info(f'======= 当前未接受到需要采集微信文章的点赞数和阅读数，程序退出中 =======')
        return
    # 采集微信文章点赞数：1天 < 爬虫时间 < 3天
    pages_es = es_utils.get_page(ESIndex.NEWS, queries=Query.queries(Query(QueryType.EQ, 'channel_name', '医药自媒体'),
                                                                     Query(QueryType.LE, 'spider_wormtime', self.date_utils.get_timestamp() - 1 * 86400 * 1000),
                                                                     Query(QueryType.GE, 'spider_wormtime', self.date_utils.get_timestamp() - 3 * 86400 * 1000)),
                                                                     page_index=-1, show_fields=['url'])
    results_es_dict = {}
    for page_es in pages_es:
        url = page_es['url']
        if 'weixin.sogou.com' in url:
            continue
        results = split_url(url=url)
        results_es_arr = []
        if results['__biz'] in results_es_dict:
            results_es_arr = results_es_dict[results['__biz']]
        results_es_arr.append(page_es)
        results_es_dict[results['__biz']] = results_es_arr

    while self.redis_server.llen(RedisKey.WECHAT_MP_LIKE_NUMS) > 0:
        results = ast.literal_eval(self.redis_server.rpop(RedisKey.WECHAT_MP_LIKE_NUMS).decode())
        results_dict = split_url(url=results['url'])
        __biz = results_dict['__biz'].replace('%3D', '=')
        appmsg_token = results_dict['appmsg_token']
        if __biz not in results_es_dict:
            logging.info(f'在ES中近 {str(PAGEOPS.LIKE_NUMS_DAY)} 天内未能发现新文章，被过滤：{__biz}')
            continue
        for es_data_dict in results_es_dict[__biz]:
            esid = es_data_dict['esid']
            url_es = es_data_dict['url']
            result_es_dict = split_url(url=url_es)
            sn = result_es_dict['sn']
            mid = result_es_dict['mid']
            idx = result_es_dict['idx']
            headers['Cookie'] = results['cookie']
            logging.info(f'追加待采集微信号：{__biz} {esid} 的对应的阅读数和点赞数')
            appmsgext_url = f'https://mp.weixin.qq.com/mp/getappmsgext?f=json&__biz={__biz}&mid={mid}&sn={sn}&idx={idx}&appmsg_token={appmsg_token}&is_only_read=1&appmsg_type=9'
            # 发送post请求：yield Request(url, method="POST", body=json.dumps(data), headers={'Content-Type': 'application/json'},callback=self.parse_json)
            yield scrapy.Request(url=appmsgext_url, method='POST', callback=self.parse, meta={'esid': esid, '__biz': __biz}, headers=headers)