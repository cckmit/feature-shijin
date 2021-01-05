# Define here the models for your scraped items

import scrapy


class WuxiaojuedingItem(scrapy.Item):
    esid = scrapy.Field()  # 唯一值
    decision_num = scrapy.Field()    #决定号
    application_num=scrapy.Field()  #专利号
    title = scrapy.Field()   #发明名称
    patentee_spidser = scrapy.Field()   #专利权人
    invalids_applicant_spidser = scrapy.Field()  #无效宣告请求人
    publication_date = scrapy.Field()  #发文日(时间戳格式)
    publication_date_new = scrapy.Field()  #发文日（初始格式）
    url = scrapy.Field()  #七牛云pdfurl
    url_html = scrapy.Field()  #详情页url
    create_time = scrapy.Field()
    modify_time = scrapy.Field()