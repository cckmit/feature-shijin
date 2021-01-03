import logging

import scrapy

from pharmcube_spider import const
from pharmcube_spider.utils import pdf_utils


from pyquery import PyQuery as pq

class CdeSpider(scrapy.Spider):
    name = 'cde'
    allowed_domains = []
    start_urls = ['https://www.baidu.com']

    def start_requests(self):
        self.pdf_utils = pdf_utils
        const.spider_init(self)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        spider_url = response.url
        logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')

        with open('/home/zengxiangxu/test.txt', encoding='utf-8') as f:
            info = f.read()
            doc = pq(info)
            left_elements = doc('.info-left')
            html = str(left_elements.html())
            html = html.replace('<a ', '<span ').replace('</a>', '</span>')  # 移除所有超链接
            pdf_list = []
            pdf_dict = {}
            pdf_dict['html'] = html
            pdf_name = self.md5_utils.get_md5(html) + '.pdf'
            pdf_dict['pdf_name'] = const.STORE_PATH + pdf_name
            pdf_list.append(pdf_dict)
            self.pdf_utils.auto_html2pdf(pdf_list)  # 合并PDF
            logging.info(f'------- pdf 合并完成 --------{const.STORE_PATH + pdf_name}')

        doc = pq(response.text)

        if 'baidu.com' in spider_url:
            pass



    def close(spider, reason):
        logging.info('------ cde数据采集完毕，开始统计被删除的数据 -------')

