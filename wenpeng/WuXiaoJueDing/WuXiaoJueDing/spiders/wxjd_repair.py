import math

from urllib.parse import urlencode
import scrapy
from datetime import datetime, timedelta
import time
import logging
import json
import re
import os
import requests
import random
from WuXiaoJueDing.utils import es_utils

from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
redis_server = from_settings(get_project_settings())

lists=['2018305325511','2016206204628','2018300881376','2013207448236','2009100978437','2017205734640','2012203643305','2014204108260','2015204022781','2011201876946','2017215336809','2010105705369','201520812893X','2013101898154','2018211740874','2017203227054','2017102218851','2012202157102','2013208528416','2018302268146','2018216827145','2019303059848','2018300859175','2016200245075','2018204928516','200680008515X','2015206116020','2018104894548','2007800311047','201720233643X','201310129421X','2018307316381','201621002677X','2017302686725','2010101400234','201020539571X','2018306968439','2018301008194','2014100927243','2018215286289','2013204428334','2018222562688','201720372343X','201330397525X','2019300956377','2018307401825','2009102660857','2014202257311','2016301538473','2015303980007','2016207714844','2013104649825','2015203805642','2019206227337','201320528554X','2009100500957','2007201314251','2015201312871','2019206793876','2019300571529','001072013','201530015881X','2017306373397','2016302236220','2019305451754','2019300269967','2010101975049','2017201344104','2019304420706','2017207786476','2018304179630','2019303059852','2018218925462','2018302777057','2011800141019','2014800370882','2015201236007','2017211533070','2014302765884','2014302681817','2016300788594','2015301691197','2015209959593','2014203735310','2012202060249','2016301254467','2014302541120','2012204539794','2014301497690','2005100553462','2013102892121','2013100953864','2013200240097','2014106220912','2004800047248','2018301614777','2019208701309','2016210074468','2018220394476','2016300686139','201830106584X','2017202187007','2018300203683','2016212742986','2016213038035','201930022996X','2015207277797','2018303748314','2018215793828','2011102409315','2016212094894','2015202451848','2019203512828','201920860407X','03128776X','2018207181247','2019304541359','2019303007010','2010800278290','201820006606X','2019211169149','2010102676326','2018303930590','2019301632093','2012100374782','2016103771698','2015302658853','2010105383859','2015200512584','2018307391908','2014105511605','2016110477355','2018303205939','2017202811880','2007100700600','2010800355070','2019302724618','2015300288550','201520273841X','2015104244512','2015207128909','008042888','2015102344643','2012305917409','2014106390735','2014300888714','200820127906X','2017209860835','201420405932X','2012206322999','2013303860542','2013203540676','2012200487288','2010800263350','201410854575X','201830100818X','2018213323419','2018303617924','2018221106438','2017106310217','2018211568407']


class WxjdSpider_Repair(scrapy.Spider):
    name = 'wxjd_repair'
    allowed_domains = ['*']
    # allowed_domains = ['reexam-app.cnipa.gov.cn','cpquery.cnipa.gov.cn']
    start_urls = []
    index_name = 'china_review_decision_publication'
    spider_cookie_key = 'spider_cookie'

    def start_requests(self): #重写start_requests
        # count = es_utils.get_count(self.index_name,queries=[es_utils.Query(es_utils.QueryType.EQ,'url', None)])
        # logging.info('------- 总的请求的数量为:%s -------'%(str(count)))
        # if not count > 0: return
        # for i in range(1,math.ceil(count/10)+1):
        #     results = es_utils.get_page(self.index_name, page_size=10,queries=[es_utils.Query(es_utils.QueryType.EQ,'url',None)],
        #                 show_fields=['esid','url_html'],page_index=i)
        #     for docdb_comb in results:
        #         try:
        #             url = docdb_comb['url_html']
        #             if url:
        #                 es_utils.delete(self.spider_cookie_key,docdb_comb['esid']) #
        #                 headers1 = {'Host': 'cpquery.cnipa.gov.cn', 'Connection': 'keep-alive', }
        #                 headers1['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        #                 cookie = redis_server.hget(self.spider_cookie_key, self.spider_cookie_key).decode()
        #                 yield scrapy.Request(url=url,callback=self.parse,meta={'esid':docdb_comb['esid']},
        #                                headers=headers1,cookies={i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')})
        #         except:continue


        # for application_num in lists:
        #     try:
        #         result = es_utils.get_one(self.index_name,es_utils.Query(es_utils.QueryType.EQ, 'application_num',application_num),show_fields=['esid', 'url_html','url'])
        #         logging.info('------- esid为:%s url为:%s-------' % (result['esid'], result.get('url','')))
        #         url = 'http://spider.pharmcube.com/{}.pdf'.format(result['esid'])  # 七牛云PDF路径
        #         res=requests.get(url=url,headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'},timeout=60)
        #         if res.status_code==200:
        #             data = {"url": url, "esid": result['esid']}
        #             logging.info('------- 当前%s文件更新ES-------'%(url))
        #             es_utils.update(self.index_name, d=data)
        #         else:
        #             if result.get('url_html'):
        #                 headers1 = {'Host': 'cpquery.cnipa.gov.cn', 'Connection': 'keep-alive'}
        #                 headers1['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        #                 cookie = redis_server.hget(self.spider_cookie_key, self.spider_cookie_key).decode()
        #                 yield scrapy.Request(url=result['url_html'], callback=self.parse, meta={'esid':result['esid']},
        #                                  headers=headers1, cookies={i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')})
        #     except Exception as e:
        #         logging.info('------- 报错为:%s -------' %str(e))


        # 单个测试 '2018300859175'
        results=[{'esid':'b995acb80ba0ee149214d2bf9058e359','url_html':'http://cpquery.cnipa.gov.cn/txnFsjdFileView.do?select-key:fid=GA000267517034&select-key:wenjiandm=201019&select-key:wenjianlx=0403&select-key:wendanglx=01&select-key:shenqingh=2010102676326'},{'esid':'0377994910f0fdbb4a3d4b4a00880fa3','url_html':'http://cpquery.cnipa.gov.cn/txnFsjdFileView.do?select-key:fid=GA000264207193&select-key:wenjiandm=201019&select-key:wenjianlx=0403&select-key:wendanglx=01&select-key:shenqingh=2017106310217'}]
        for result in results:
            try:
                url = 'http://spider.pharmcube.com/{}.pdf'.format(result['esid'])  # 七牛云PDF路径
                res=requests.get(url=url,headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'},timeout=60)
                if res.status_code==200:
                    data = {"url": url, "esid": result['esid']}
                    logging.info('------- 当前%s文件更新ES-------'%(url))
                    es_utils.update(self.index_name, d=data)
                else:
                    headers1 = {'Host': 'cpquery.cnipa.gov.cn', 'Connection': 'keep-alive'}
                    headers1['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
                    cookie = redis_server.hget(self.spider_cookie_key, self.spider_cookie_key).decode()
                    yield scrapy.Request(url=result['url_html'], callback=self.parse, meta={'esid':result['esid']},
                                     headers=headers1, cookies={i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')})
            except:pass


    def get_publication_date(self,ts):
        return int(datetime.strptime(ts,'%Y%m%d').timestamp()*1000)

    def parse(self, response):
        if not os.path.exists('./images/'):os.makedirs('./images/')
        if not os.path.exists('./pdf_file/'):os.makedirs('./pdf_file/')
        if response.url == 'exceptions':
            return
        esid=response.meta['esid']
        path0 = './images/{}/'.format(esid)
        if not os.path.exists(path0):
            os.makedirs(path0)
        # thumb_urls = response.text.split('var thumburl =')
        try:
            thumb_urls = response.text.split('var picurl =')
            logging.info('------- %s图片数量为%s -------'%(esid,len(thumb_urls)))
            if len(thumb_urls)==1:
                return
            #1.下载图片
            is_true = False
            for i in range(len(thumb_urls)):
                thumb_url = thumb_urls[i].strip()
                if not thumb_url.startswith('"/freeze.main?'):
                    continue
                if not is_true:is_true = True
                img_url = 'http://cpquery.cnipa.gov.cn'+thumb_url.split(';')[0].replace('"', '').replace('\'', '').replace('+','').replace(' ', '').strip()
                # print('img_url:',img_url)
                headers = {'Host':'cpquery.cnipa.gov.cn','Connection': 'keep-alive',}
                headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
                for j in range(6):
                    try:
                        headers['cookie'] = redis_server.hget(self.spider_cookie_key,self.spider_cookie_key).decode()
                        file_data = requests.get(url=img_url, allow_redirects=True, headers=headers,timeout=60)
                        if file_data.status_code == 200:
                            with open('./images/{}/{}.png'.format(esid,i),'wb') as handler:
                                handler.write(file_data.content)
                            break
                    except:pass
            if is_true:
                # 2.合成pdf
                localfile = './pdf_file/'+esid+'.pdf'
                # print('localfile:',localfile)
                path1 = '%s.pdf' %esid
                result=self.jpg_to_pdf(img_dir=path0, pdf_name=localfile) #合成pdf
                if result:
                    info_status = self.up_qiniu(path1, localfile)  # 上传到七牛云
                    print('info_status:', info_status)
                    logging.info('------- 上传七牛云的状态%s -------' % str(info_status))
                    if info_status != 200:
                        if os.path.exists(localfile):
                            os.remove(localfile)
                    else:
                        #3.更新ES的url字段
                        url = 'http://spider.pharmcube.com/{}'.format(path1)  # 七牛云PDF路径
                        data = {"url": url, "esid": esid}
                        logging.info('------- 当前%s文件更新ES -------%s' % (path1,esid))
                        es_utils.update(self.index_name, d=data)
        except:pass

    # 方法1 将图片合成pdf
    def delete_no_img_files(self):  # 删除没有图片的文件夹
        for i in os.listdir('./images/'):
            if '.' in i: continue
            lis = [j for j in os.listdir('./images/' + i) if j.endswith('png') or j.endswith('jpg')]
            if len(lis) == 0:
                os.removedirs('./images/' + i)

    def jpg_to_pdf(self,img_dir='./images/img01/', pdf_name='./pdf_file/result1.pdf'):  # 图片合成PDF
        from PyPDF2 import PdfFileReader, PdfFileMerger
        from reportlab.lib.pagesizes import A4, landscape, portrait
        from reportlab.pdfgen import canvas
        if os.path.exists(pdf_name): os.remove(pdf_name)
        list_jpgs = [os.path.join(img_dir, fn) for fn in os.listdir(img_dir) if fn.endswith('png')]
        if not list_jpgs:
            return False
        self.delete_no_img_files()
        result_pdf = PdfFileMerger()
        temp_pdf = 'temp.pdf'
        for fn in range(1, len(os.listdir(img_dir)) + 1):
            i = os.path.join(img_dir, '%s.png' % fn)
            cnv = canvas.Canvas(temp_pdf, pagesize=portrait(A4))
            cnv.drawImage(i, 0, 0, *portrait(A4))
            cnv.save()
            with open(temp_pdf, 'rb') as f:
                pdf_reader = PdfFileReader(f)
                result_pdf.append(pdf_reader)
        result_pdf.write(pdf_name)
        result_pdf.close()
        if os.path.exists(temp_pdf): os.remove(temp_pdf)
        return True


    def up_qiniu(self,path1, localfile):  # 上传到七牛云
        from qiniu import Auth, put_file, etag
        from qiniu import BucketManager
        """
        :param path1: 文件上传位置路径
        :param localfile: 本地文件路径
        """
        bucket_name = 'pharmcube-spider'  # 七牛云存储的位置名
        access_key = 'RPEoJfcPJREYLrPfxrsBUyWJEj2JEHwACfDQB28n'  # 需要填写七牛云的 Access Key
        secret_key = 'bB3a_3pXpcoPsRIU3UYvW3MeyhhXKWF2HGNmx7b7'  # 需要填写七牛云的 Secret Key
        # 构建鉴权对象
        count = 0
        while True:
            info_status = None
            try:
                q = Auth(access_key, secret_key)
                token = q.upload_token(bucket_name, path1, 5400)
                # 要上传文件的本地路径
                ret, info = put_file(token, path1, localfile)
                assert ret['key'] == path1
                assert ret['hash'] == etag(localfile)
                info_status = info.status_code
                print('info_status:', info)  # 状态码
                if info_status == 200:
                    logging.info('------- 删除指定文件 -------' + path1)
                    logging.info('------- 当前文件成功上传到七牛云 -------' + path1)
                    # if os.path.exists(localfile):
                    #     os.remove(localfile)  # 删除本地文件
                    break
            except:
                pass
            count += 1
            logging.info(f'------- 当前文件上传到七牛云上失败，重试中 {count} 次数 -------' + path1)
            if count > 3:
                break
        return info_status







