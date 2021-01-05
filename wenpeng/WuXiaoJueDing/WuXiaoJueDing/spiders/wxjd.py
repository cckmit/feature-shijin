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
from WuXiaoJueDing.tools.useragents import useragents
from WuXiaoJueDing.items import WuxiaojuedingItem
from WuXiaoJueDing.tools.common import get_md5
from WuXiaoJueDing.utils import es_utils

from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
redis_server = from_settings(get_project_settings())

# import redis
# redis_server = redis.Redis(host=get_project_settings()['REDIS_HOST'],port=get_project_settings()['REDIS_PORT'])

"""
linux
pyppeteer_get.py文件中修改谷歌浏览器路径为exepath ='/opt/google/chrome/chrome'
find / -name page.py
vi page.py
注释 clip = dict(x=0, y=0, width=width, height=height, scale=1)
"""

class WxjdSpider(scrapy.Spider):
    name = 'wxjd'
    allowed_domains = []
    # allowed_domains = ['reexam-app.cnipa.gov.cn','cpquery.cnipa.gov.cn']
    start_urls = ['http://reexam-app.cnipa.gov.cn/reexam_out2020New/wuxiao/wuxiaolb.jsp']
    index_name = 'china_review_decision_publication'
    spider_cookie_key = 'spider_cookie'

    def get_publication_date(self, ts):
        return int(datetime.strptime(ts, '%Y%m%d').timestamp() * 1000)

    def parse(self, response):
        if not os.path.exists('./images/'):os.makedirs('./images/')
        if not os.path.exists('./pdf_file/'):os.makedirs('./pdf_file/')
        if response.url == 'exceptions':
            return
        list_li = response.xpath('//div[@class="list_rep"]/ul[@class="tbody"]/li')
        # print('list_li:', len(list_li))
        for li in list_li:
            href = li.xpath('./div[@class="t01"]/a/@href').extract_first()
            if not href: continue
            item = WuxiaojuedingItem()
            #决定号
            item["decision_num"] = li.xpath(".//div[@class='con_text_01']/text()").extract_first()
            #专利号
            item["application_num"] = li.xpath('./div[@class="t02"]/text()').extract_first()
            #发明名称
            item["title"] = li.xpath('./div[@class="t03"]/span[2]/@title').extract_first()
            #专利权人
            item["patentee_spidser"] = li.xpath("./div[@class='t04']/span[2]/@title").extract_first()
            #无效宣告请求人
            item["invalids_applicant_spidser"] = li.xpath("./div[@class='t05']/span[2]/@title").extract_first()

            #发文日
            publication_date = li.xpath("./div[@class='t06']/text()").extract_first()
            item["publication_date"] = self.get_publication_date(publication_date)
            item['publication_date_new']=li.xpath("./div[@class='t06']/text()").extract_first()


            #详情页url
            url_html=li.xpath('./div[@class="t01"]/a/@href').extract_first()
            item["url_html"] = url_html

            # 创建时间
            item['create_time'] = int(round(time.time() * 1000))
            # 修改时间
            item['modify_time'] = int(round(time.time() * 1000))

            #item["esid"] = get_md5(item["decision_num"]+item["application_num"]+str(item["publication_date_new"]))
            item["esid"] = get_md5(str(item["decision_num"])+str(item["application_num"])+str(item["publication_date_new"])+str(item["title"]) + str(item["patentee_spidser"])+str(item["invalids_applicant_spidser"]))
            #查询ES如何在ES可以查询到，就不再请求详情页了
            try:
                result = es_utils.get_one(self.index_name,es_utils.Query(es_utils.QueryType.EQ,'esid',item["esid"]),show_fields=['url'])
                if result.get('url'): continue
            except:pass
            headers1={'Host':'cpquery.cnipa.gov.cn','Connection': 'keep-alive',}
            headers1['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
            cookie=redis_server.hget(self.spider_cookie_key,self.spider_cookie_key).decode()
            # print('cookie:',cookie)
            logging.info('------- 详情页URL为:%s -------' % (item["url_html"]))
            yield scrapy.Request(
                url=url_html,
                callback=self.detail_page,
                meta={'item':item},
                headers=headers1,
                cookies={i.split('=')[0]: i.split('=')[1] for i in cookie.split('; ')}
            )


        ###总页
        #total_page = response.xpath('//font[@class="huilan14"]/text()').extract_first()
        #if total_page:
        #    total_page_num = re.findall('共(\d+)页', str(total_page))
        #else:
        #    total_page_num = re.findall('共(\d+)页', response.text)
        #total_page_num = int(total_page_num[0])
        #print('total_page_num:',total_page_num
        #print(type(total_page_num))
        total_page_num = 4
        # 下一页
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'user-agent': random.choice(useragents)}
        form_data = {"currnetPage": 2}
        next_url = 'http://reexam-app.cnipa.gov.cn/reexam_out2020New/wuxiao/wuxiaolb.jsp'
        yield scrapy.Request(url=next_url,headers=headers, method='POST',
                             body=urlencode(form_data),callback=self.next_page,
                             meta={'currnetPage': 2,'total_page':total_page_num})

    def next_page(self,response):
        if response.url == 'exceptions':
            return
        list_li = response.xpath('//div[@class="list_rep"]/ul[@class="tbody"]/li')
        # print('list_li:', len(list_li))
        for li in list_li:
            href = li.xpath('./div[@class="t01"]/a/@href').extract_first()
            if not href: continue
            item = WuxiaojuedingItem()
            # 决定号
            item["decision_num"] = li.xpath(".//div[@class='con_text_01']/text()").extract_first()
            # 专利号
            item["application_num"] = li.xpath('./div[@class="t02"]/text()').extract_first()
            # 发明名称
            item["title"] = li.xpath('./div[@class="t03"]/span[2]/@title').extract_first()
            # 专利权人
            item["patentee_spidser"] = li.xpath("./div[@class='t04']/span[2]/@title").extract_first()
            # 无效宣告请求人
            item["invalids_applicant_spidser"] = li.xpath("./div[@class='t05']/span[2]/@title").extract_first()
            # 发文日
            publication_date = li.xpath("./div[@class='t06']/text()").extract_first()
            item["publication_date"] = self.get_publication_date(publication_date)
            item['publication_date_new'] = li.xpath("./div[@class='t06']/text()").extract_first()
            # 详情页url
            item["url_html"] = li.xpath('./div[@class="t01"]/a/@href').extract_first()

            # 创建时间
            item['create_time'] = int(round(time.time() * 1000))
            # 修改时间
            item['modify_time'] = int(round(time.time() * 1000))

            item["esid"] = get_md5(item["decision_num"] + item["application_num"] + str(item["publication_date_new"] + item["title"] + item["patentee_spidser"] + item["invalids_applicant_spidser"]))
            #查询ES如何在ES可以查询到，就不再请求详情页了
            try:
                result = es_utils.get_one(self.index_name, es_utils.Query(es_utils.QueryType.EQ, 'esid', item["esid"]),show_fields=['url'])
                if result.get('url'): continue
            except:pass
            headers1 = {'Host':'cpquery.cnipa.gov.cn','Connection': 'keep-alive'}
            headers1['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
            cookie=redis_server.hget(self.spider_cookie_key,self.spider_cookie_key).decode()
            headers1['cookie']= cookie
            logging.info('------- 详情页URL为:%s -------' % (item["url_html"]))
            logging.info('------- 当前字段 -------%s' % item)
            yield scrapy.Request(
                url=item["url_html"],
                callback=self.detail_page,
                meta={'item': item},
                headers=headers1,
                cookies={i.split('=')[0]:i.split('=')[1] for i in cookie.split(';')}
            )
        # 下一页
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'user-agent': random.choice(useragents)}
        total_page = response.meta['total_page']
        page_num = int(response.meta['currnetPage'])
        ## 判断 page_num 小于 total_nums总页
        if page_num <= int(total_page):
            form_data = {"currnetPage": page_num+1}
            next_url = 'http://reexam-app.cnipa.gov.cn/reexam_out2020New/wuxiao/wuxiaolb.jsp'
            # print('form_data:', form_data)
            yield scrapy.Request(url=next_url,headers=headers, method='POST',
                                 body=urlencode(form_data),callback=self.next_page,
                                 meta={'currnetPage': page_num+1,'total_page':total_page})

#主要原因是，我的这边有的html_url 里面有图片，但是没有生成pdf生成url
    def detail_page(self,response):
        item=response.meta['item']
        path0 = './images/{}/'.format(item["esid"])
        if not os.path.exists(path0):
            os.makedirs(path0)
        # thumb_urls = response.text.split('var thumburl =')
        thumb_urls = response.text.split('var picurl =')
        logging.info('------- %s图片数量为%s -------' % (item["esid"], len(thumb_urls)))
        if len(thumb_urls)<= 1:
            logging.info('------- item为:%s -------' % str(item))
            item.pop('url_html')
            yield item
        else:
            #1.下载图片
            is_true=False
            for i in range(len(thumb_urls)):
                thumb_url = thumb_urls[i].strip()
                if not thumb_url.startswith('"/freeze.main?'):
                    continue
                if not is_true:is_true = True
                img_url = 'http://cpquery.cnipa.gov.cn'+thumb_url.split(';')[0].replace('"', '').replace('\'', '').replace('+','').replace(' ', '').strip()
                headers = {'Host':'cpquery.cnipa.gov.cn','Connection': 'keep-alive',}
                headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
                for j in range(6):
                    try:
                        headers['cookie'] = redis_server.hget(self.spider_cookie_key,self.spider_cookie_key).decode()
                        file_data = requests.get(url=img_url, allow_redirects=True, headers=headers,timeout=60)
                        # print('status_code:',file_data.status_code)
                        if file_data.status_code==200:
                            with open('./images/{}/{}.png'.format(item['esid'],i),'wb') as handler:
                                handler.write(file_data.content)
                            break
                    except:pass
            if is_true:
                # 2.合成pdf
                localfile = './pdf_file/'+item["esid"]+'.pdf'
                path1 = '%s.pdf' % item["esid"]
                result2=self.jpg_to_pdf(img_dir=path0, pdf_name=localfile) #合成pdf
                if result2:
                    info_status = self.up_qiniu(path1, localfile)  # 上传到七牛云
                    logging.info('------- 上传七牛云的状态%s -------' % str(info_status))
                    if info_status != 200:
                        if os.path.exists(localfile):
                            os.remove(localfile)
                    else:
                        #3.更新ES
                        url = 'http://spider.pharmcube.com/{}'.format(path1)  # 七牛云PDF路径
                        logging.info('------- 当前%s文件更新ES -------%s' % (path1, item['esid']))
                        item["url"]=url
                        logging.info('------- item为:%s -------' %str(item))
                        try:
                            result1 = es_utils.get_one(self.index_name,es_utils.Query(es_utils.QueryType.EQ, 'esid', item["esid"]),show_fields=['esid','url'])
                        except:result1=None
                        if result1:
                            logging.info('------- 该esid:%s已存在,更新url:%s -------' %(item["esid"],url))
                            data = {"url": url, "esid": item['esid'],'modify_time':item['modify_time']}

                            es_utils.update(self.index_name, d=data)
                        else:
                            yield item

    # 方法1 将图片合成pdf
    # pip install PyPDF2
    # pip install reportlab
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
            if count >5:
                break
        return info_status

    def save_file(self,name, content):
        with open(name, 'a+', encoding='utf-8') as f:
            f.write(content + '\n')

    #方法1 将图片合成pdf
    # def pic2pdf(self,img_dir='./images/', pdf_name='result.pdf'):
    #     import fitz  # pip install PyMuPDF
    #     import glob
    #     [os.removedirs(img_dir + i) for i in os.listdir(img_dir) if not i.endswith('png')] #删除文件夹
    #     doc = fitz.open()
    #     temp_pdf = 'temp.pdf'
    #     for img in sorted(glob.glob("{}/*".format(img_dir))):  # 读取图片，确保按文件名排序
    #         imgdoc = fitz.open(img)  # 打开图片
    #         pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
    #         imgpdf = fitz.open("pdf", pdfbytes)
    #         doc.insertPDF(imgpdf)  # 将当前页插入文档
    #     if os.path.exists(temp_pdf): os.remove(temp_pdf)
    #     doc.save(pdf_name)  # 保存pdf文件
    #     doc.close()







