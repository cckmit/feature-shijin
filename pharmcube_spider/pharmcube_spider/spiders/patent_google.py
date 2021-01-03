import scrapy


class PatentGoogleSpider(scrapy.Spider):
    name = 'patent_google'
    allowed_domains = ['patent_google.com']
    start_urls = ['http://patent_google.com/']

    def parse(self, response):
        pass
