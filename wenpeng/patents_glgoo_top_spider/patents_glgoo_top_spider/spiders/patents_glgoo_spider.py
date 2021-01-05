import json
import os
import random
import re
import math
import requests
import scrapy
from datetime import datetime, timedelta
import time
import logging
from ..utils import es_utils
from ..tools.useragents import useragents
from qiniu import Auth, put_file, etag
# from scrapy_redis_cluster.spiders import RedisSpider
# select fulltext_pdf,publication_docdb_comb from drug_patent_info_v2 where esid='fe7b49cc81883165739301a59521df56'

from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
redis_server = from_settings(get_project_settings())


"""
1.https://patents.glgoo.top/xhr/parse?text=US2017354788A1&cursor=14&exp= 获取patent/US20170354788A1/en
2.https://patents.glgoo.top/xhr/result?id=patent/US20170354788A1/en&qs=oq=US2017354788A1&exp=
"""

#SELECT count(publication_docdb_comb) FROM drug_patent_info_v2 where fulltext_pdf and publication_docdb_country='EP'
class PatentsGlgooSpiderSpider(scrapy.Spider):
    name = 'patents_glgoo_spider'
    redis_key = 'patents_glgoo_spider:url'
    allowed_domains = ['patents.glgoo.top','spider.pharmcube.com']
    start_urls = []
    index_name = 'drug_patent_info_v2' #索引
    bucket_name='pharmcube-spider' #七牛云存储的位置名
    countrys = ['EP', 'CN', 'WO', 'US', 'JP']
    #countrys = ['US']
    url = 'https://patents.glgoo.top/xhr/parse?text={}&cursor=11&exp='
    hash_key = 'is_not_exist_pdf'  # 存储不存在PDF的publication_docdb_comb


    def start_requests(self): #重写start_requests
        for country in self.countrys:
            count = es_utils.get_count(self.index_name,queries=[es_utils.Query(es_utils.QueryType.EQ, 'fulltext_pdf', None),
                                                                es_utils.Query(es_utils.QueryType.EQ, 'publication_docdb_country',country)])
            logging.info('------- 总的请求的数量为:%s -------'%(str(count)))
            if not count > 0: return
            for i in range(1,math.ceil(count/2000)+1):
                results = es_utils.get_page(self.index_name, page_size=2000,queries=[es_utils.Query(es_utils.QueryType.EQ, 'fulltext_pdf',None),
                        es_utils.Query(es_utils.QueryType.EQ, 'publication_docdb_country',country)],show_fields=['esid', 'publication_docdb_comb'],
                        page_index=i)
                hash_key_num = redis_server.hlen(self.hash_key)
                logging.info('------- %s没有pdf的publication_docdb_comb数量为%s -------' % (country, str(hash_key_num)))
                for docdb_comb in results:
                    try:
                        if redis_server.hexists(self.hash_key, docdb_comb['publication_docdb_comb']): continue
                        url = self.url.format(docdb_comb['publication_docdb_comb'])
                        yield scrapy.Request(url=url, callback=self.parse,
                            meta={'docdb_comb':docdb_comb['publication_docdb_comb'],'esid':docdb_comb['esid']})
                    except:
                        continue


        #单个测试
        #一千多条的那个吗？ 有上传数据
        # docdb_comb={'publication_docdb_comb':'CN106573971A','esid':'2b97b8cf9e19bd3be6a41e24e52b50f6'}
        # url = self.url.format(docdb_comb['publication_docdb_comb'], 12)
        # yield scrapy.Request(url=url, callback=self.parse,
        #                      meta={'docdb_comb': docdb_comb['publication_docdb_comb'], 'esid': docdb_comb['esid']})




    def parse(self, response):
        docdb_comb=response.meta['docdb_comb']
        esid=response.meta['esid']
        logging.info('------- 当前请求的publication_docdb_comb为:%s,esid为:%s -------' %(docdb_comb,esid))
        try:
            patent=json.loads(response.text)['results'][0]['result']['id']
            number = json.loads(response.text)['results'][0]['result']['number']
        except:
            # self.save_file('error_down.txt', docdb_comb)
            logging.info('-------%s搜索不到pdf-------' %docdb_comb)
            return
        detail_url='https://patents.glgoo.top/xhr/result?id={}&qs=oq={}&exp='.format(patent,number)
        yield scrapy.Request(url=detail_url,
            callback=self.detail_page,
            meta={'docdb_comb':docdb_comb,'esid':esid})

    def detail_page(self,response):
        docdb_comb = response.meta['docdb_comb']
        esid = response.meta['esid']
        # total_url = len(self.crawler.engine.slot.inprogress)  # 当前正在运行请求
        # prepare_url = len(self.crawler.engine.slot.scheduler)  # 待采集URL条数
        # logging.info(f"待采集URL条数：{prepare_url}，当前运行请求数：{total_url}")
        headers = {'user-agent': random.choice(useragents)}
        if not os.path.exists('./pdf_files/'): os.makedirs('./pdf_files/')
        try:
            # pdfurl = re.findall('<meta name="citation_pdf_url" content="(https://.*?\.pdf)">', response.text, re.S)
            # if not pdfurl:
            #     pdfurl = re.findall('<a href="(https://.*?\.pdf)" itemprop="pdfLink">Download PDF</a>', response.text, re.S)
            pdfurl=re.findall('<a href="(http.*?pdf)" itemprop="pdfLink">',response.text,re.S)
            print('pdfurl:', pdfurl)
            logging.info('------- 请求的URL为%s -------'%str(pdfurl))
            if pdfurl:
                res1 = requests.get(url=pdfurl[0], headers=headers, timeout=60)
                localfile = './pdf_files/' + '%s.pdf' % docdb_comb  # 本地PDF文件存储位置路径
                path1 = '%s.pdf' % docdb_comb  # 七牛云上传位置路径
                with open(localfile, 'ab+') as f:
                    f.write(res1.content)
                info_status = self.up_qiniu(path1, localfile)  # 上传到七牛云
                print('info_status:', info_status)
                logging.info('------- 上传七牛云的状态%s -------'%str(info_status))
                if info_status != 200:
                    if os.path.exists(localfile):
                        os.remove(localfile)
                    # self.save_file('error_down.txt', docdb_comb)  # 将下载错误的fultext_pdf保存
                else:
                    # 'http://spider.pharmcube.com/US2020171043A1.pdf'
                    fulltext_pdf = 'http://spider.pharmcube.com/{}'.format(path1)  # 七牛云PDF路径
                    data = {"fulltext_pdf": fulltext_pdf, "esid": esid}
                    logging.info('------- 当前fulltext_pdf为%s -------esid为%s' % (path1,esid))
                    es_utils.update(self.index_name, d=data)
            else:
               if '.pdf' not in response.text: #将没有pdf的docdb_comb存入哈希队列，下次不再请求
                   redis_server.hset(self.hash_key, response.meta['docdb_comb'], 1)

        except:
            pass
            # self.save_file('error_down.txt', docdb_comb)

    def save_file(self, name, content):
        with open(name, 'a+', encoding='utf-8') as f:
            f.write(content + '\n')

    def up_qiniu(self,path1,localfile): #上传到七牛云
        """
        :param path1: 文件上传位置路径
        :param localfile: 本地文件路径
        """
        access_key = 'RPEoJfcPJREYLrPfxrsBUyWJEj2JEHwACfDQB28n'  #需要填写七牛云的 Access Key
        secret_key = 'bB3a_3pXpcoPsRIU3UYvW3MeyhhXKWF2HGNmx7b7' #需要填写七牛云的 Secret Key
        # 构建鉴权对象
        count=0
        while True:
            try:
                q = Auth(access_key, secret_key)
                token = q.upload_token(self.bucket_name, path1, 5400)
                # 要上传文件的本地路径
                ret, info = put_file(token, path1, localfile)
                assert ret['key'] == path1
                assert ret['hash'] == etag(localfile)
                info_status = info.status_code
                print('info_status:', info_status) #状态码
                if info_status == 200:
                    # logging.info('------- 删除指定文件 -------' + path1)
                    logging.info('------- 当前文件成功上传到七牛云 -------' + path1)
                    if os.path.exists(localfile):
                        os.remove(localfile)  # 删除本地文件
                    break
            except:
                pass
            count += 1
            logging.info(f'------- 当前文件上传到七牛云上失败，重试中 {count} 次数 -------' + path1)
            if count > 3:
                break
        return info_status