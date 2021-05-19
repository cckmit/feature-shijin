import logging
import urllib.parse
import scrapy,xlrd,re
from flash_news.utils import es_utils
from flash_news.utils.mongo_utils import MongoUtils
from flash_news.utils.md5_utils import MD5Utils
from scrapy.utils.project import get_project_settings
from scrapy_redis_cluster.connection import from_settings
from flash_news import const
from flash_news.utils.date_utils import DateUtils

'''
32   128  128
百度学术：
tapd网址：https://www.tapd.cn/60111173/prong/stories/view/1160111173001003324?from=wxnotification&corpid=wx65282324fd407a3a&agentid=1000002&jump_count=2
爬虫网址：https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=frontpage
'''

class Doctor(scrapy.Spider):
    name = 'baidu_academic'
    allowed_domains = []
    def start_requests(self):
        self.es_utils = es_utils
        self.mongo_utils = MongoUtils()
        self.md5_utils = MD5Utils()
        self.date_utils = DateUtils()
        self.redis_server = from_settings(get_project_settings())
        self.get_timestamp = DateUtils()
        # 打开文件
        data = xlrd.open_workbook("D:\software\百度下载\work\百度学术爬取医生名单.xlsx")
        # 查看工作表
        data.sheet_names()
        # 通过文件名获得工作表,获取工作表1
        table = data.sheet_by_name('Sheet1')
        doctor = table.col_values(1)
        hospital = table.col_values(2)
        doctor_hospital = dict(zip(doctor, hospital))
        for doctor, hospital in doctor_hospital.items():
            start_urls = ["https://xueshu.baidu.com/usercenter/data/authorchannel?cmd=search_author&_token=c58720f8a5813af438390526a661c8fc5ecf2ab120578e7df1a3b4afb7d8be29&_ts=1614649756&_sign=d4bc00763bfb289d1258c40619058e27&author={}&affiliate={}&curPageNum=1".format(urllib.parse.quote(doctor), urllib.parse.quote(hospital))]
            for url in start_urls:
                yield self.make_requests_from_url(url)

    # 拿到每个人的url
    def parse(self,response):
        # logging.info(f'待采集URL条数：{len(self.crawler.engine.slot.inprogress)}，当前运行请求数：{len(self.crawler.engine.slot.scheduler)}')
        page = response.text.replace("\\", "")
        spider_url = ''.join(re.findall(r'firstItem noborderItem"><a class="searchResult_pic" href=".*?"',page))[58:-1]
        if len(spider_url) > 3:
            url = "https://xueshu.baidu.com" + spider_url
            yield scrapy.Request(url=url, callback=self.baidu_academics)

    ## 详情页解析
    def baidu_academics(self,response):
        ## 医生ID
        scholarID = response.xpath('//span[@class="p_scholarID_id"]/text()').extract()
        scholarID = ''.join(scholarID)
        ## 医生名称
        doctor_name = response.xpath('//div[@class="p_name"]/text()').extract()
        doctor_name = ''.join(doctor_name)
        ## 所属医院
        hospital_name = response.xpath('//div[@class="p_affiliate"]/text()').extract()
        hospital_name = ''.join(hospital_name)
        ## 被引频次
        cited_frequency = response.xpath('//ul[@class="p_ach_wr"]/li[1]/p[2]/text()').extract()
        cited_frequency = ''.join(cited_frequency)
        ## 成果数
        Number_of_achievements = response.xpath('//ul[@class="p_ach_wr"]/li[2]/p[2]/text()').extract()
        Number_of_achievements = ''.join(Number_of_achievements)
        ## H指数
        H_index = response.xpath('//ul[@class="p_ach_wr"]/li[3]/p[2]/text()').extract()
        H_index = ''.join(H_index)
        ## G指数
        G_index = response.xpath('//ul[@class="p_ach_wr"]/li[4]/p[2]/text()').extract()
        G_index = ''.join(G_index)
        ## 领域
        field = response.xpath('//span[@class="person_domain person_text"]/a/text()').extract()
        field = ''.join(field)
        ## 期刊
        periodical = response.xpath('//div[@class="pie_map_wrapper"]/div[1]/div/p[1]/text()').extract()
        periodical = ''.join(periodical)
        ## 会议
        conference = response.xpath('//div[@class="pie_map_wrapper"]/div[2]/div/p[1]/text()').extract()
        conference = ''.join(conference)
        ## 专著
        monograph = response.xpath('//div[@class="pie_map_wrapper"]/div[3]/div/p[1]/text()').extract()
        monograph = ''.join(monograph)
        ## 其它
        other = response.xpath('//div[@class="pie_map_wrapper"]/div[4]/div/p[1]/text()').extract()
        other = ''.join(other)
        ## 合作机构1
        cooperative_institution1 = response.xpath('//ul[@class="co_affiliate_list"]/li[1]/span[1]/span/text()').extract()
        cooperative_institution1 = ''.join(cooperative_institution1)
        ## 合作次数1
        cooperative_number1 = response.xpath('//ul[@class="co_affiliate_list"]/li[1]/span[2]/span[2]/text()').extract()
        cooperative_number1 = ''.join(cooperative_number1)
        ## 合作机构2
        cooperative_institution2 = response.xpath('//ul[@class="co_affiliate_list"]/li[2]/span[1]/span/text()').extract()
        cooperative_institution2 = ''.join(cooperative_institution2)
        ## 合作次数2
        cooperative_number2 = response.xpath('//ul[@class="co_affiliate_list"]/li[2]/span[2]/span[2]/text()').extract()
        cooperative_number2 = ''.join(cooperative_number2)
        ## 合作机构3
        cooperative_institution3 = response.xpath('//ul[@class="co_affiliate_list"]/li[3]/span[1]/span/text()').extract()
        cooperative_institution3 = ''.join(cooperative_institution3)
        ## 合作次数3
        cooperative_number3 = response.xpath('//ul[@class="co_affiliate_list"]/li[3]/span[2]/span[2]/text()').extract()
        cooperative_number3 = ''.join(cooperative_number3)
        ## 合作机构4
        cooperative_institution4 = response.xpath('//ul[@class="co_affiliate_list"]/li[4]/span[1]/span/text()').extract()
        cooperative_institution4 = ''.join(cooperative_institution4)
        ## 合作次数4
        cooperative_number4 = response.xpath('//ul[@class="co_affiliate_list"]/li[4]/span[2]/span[2]/text()').extract()
        cooperative_number4 = ''.join(cooperative_number4)
        ## 合作机构5
        cooperative_institution5 = response.xpath('//ul[@class="co_affiliate_list"]/li[5]/span[1]/span/text()').extract()
        cooperative_institution5 = ''.join(cooperative_institution5)
        ## 合作次数5
        cooperative_number5 = response.xpath('//ul[@class="co_affiliate_list"]/li[5]/span[2]/span[2]/text()').extract()
        cooperative_number5 = ''.join(cooperative_number5)
        ## 合作机构6
        cooperative_institution6 = response.xpath('//ul[@class="co_affiliate_list"]/li[6]/span[1]/span/text()').extract()
        cooperative_institution6 = ''.join(cooperative_institution6)
        ## 合作次数6
        cooperative_number6 = response.xpath('//ul[@class="co_affiliate_list"]/li[6]/span[2]/span[2]/text()').extract()
        cooperative_number6 = ''.join(cooperative_number6)
        ## 合作机构7
        cooperative_institution7 = response.xpath('//ul[@class="co_affiliate_list"]/li[7]/span[1]/span/text()').extract()
        cooperative_institution7 = ''.join(cooperative_institution7)
        ## 合作次数7
        cooperative_number7 = response.xpath('//ul[@class="co_affiliate_list"]/li[7]/span[2]/span[2]/text()').extract()
        cooperative_number7 = ''.join(cooperative_number7)
        ## 合作机构8
        cooperative_institution8 = response.xpath('//ul[@class="co_affiliate_list"]/li[8]/span[1]/span/text()').extract()
        cooperative_institution8 = ''.join(cooperative_institution8)
        ## 合作次数8
        cooperative_number8 = response.xpath('//ul[@class="co_affiliate_list"]/li[8]/span[2]/span[2]/text()').extract()
        cooperative_number8 = ''.join(cooperative_number8)
        ## 合作机构9
        cooperative_institution9 = response.xpath('//ul[@class="co_affiliate_list"]/li[9]/span[1]/span/text()').extract()
        cooperative_institution9 = ''.join(cooperative_institution9)
        ## 合作次数9
        cooperative_number9 = response.xpath('//ul[@class="co_affiliate_list"]/li[9]/span[2]/span[2]/text()').extract()
        cooperative_number9 = ''.join(cooperative_number9)
        ## 合作机构10
        cooperative_institution10 = response.xpath('//ul[@class="co_affiliate_list"]/li[10]/span[1]/span/text()').extract()
        cooperative_institution10 = ''.join(cooperative_institution10)
        ## 合作次数10
        cooperative_number10 = response.xpath('//ul[@class="co_affiliate_list"]/li[10]/span[2]/span[2]/text()').extract()
        cooperative_number10 = ''.join(cooperative_number10)
        ## 进入合作学者 data传的entity_id
        data_id = response.xpath('//div[@class="person_image"]/a[2]/@href').extract()
        data_id = ''.join(data_id)[-32:]

        mongo_dict = {}
        mongo_dict['scholarID'] = scholarID
        mongo_dict['doctor_name'] = doctor_name
        mongo_dict['hospital_name'] = hospital_name
        mongo_dict['cited_frequency'] = cited_frequency
        mongo_dict['Number_of_achievements'] = Number_of_achievements
        mongo_dict['H_index'] = H_index
        mongo_dict['G_index'] = G_index
        mongo_dict['field'] = field
        mongo_dict['periodical'] = periodical
        mongo_dict['conference'] = conference
        mongo_dict['monograph'] = monograph
        mongo_dict['other'] = other
        mongo_dict['cooperative_institution1'] = cooperative_institution1
        mongo_dict['cooperative_number1'] = cooperative_number1
        mongo_dict['cooperative_institution2'] = cooperative_institution2
        mongo_dict['cooperative_number2'] = cooperative_number2
        mongo_dict['cooperative_institution3'] = cooperative_institution3
        mongo_dict['cooperative_number3'] = cooperative_number3
        mongo_dict['cooperative_institution4'] = cooperative_institution4
        mongo_dict['cooperative_number4'] = cooperative_number4
        mongo_dict['cooperative_institution5'] = cooperative_institution5
        mongo_dict['cooperative_number5'] = cooperative_number5
        mongo_dict['cooperative_institution6'] = cooperative_institution6
        mongo_dict['cooperative_number6'] = cooperative_number6
        mongo_dict['cooperative_institution7'] = cooperative_institution7
        mongo_dict['cooperative_number7'] = cooperative_number7
        mongo_dict['cooperative_institution8'] = cooperative_institution8
        mongo_dict['cooperative_number8'] = cooperative_number8
        mongo_dict['cooperative_institution9'] = cooperative_institution9
        mongo_dict['cooperative_number9'] = cooperative_number9
        mongo_dict['cooperative_institution10'] = cooperative_institution10
        mongo_dict['cooperative_number10'] = cooperative_number10
        mongo_dict['data_id'] = data_id
        logging.info(f'------- @@@insert mongo data ------- {doctor_name}')
        self.mongo_utils.insert_one(mongo_data=mongo_dict, coll_name=const.MongoTables.BAIDU_ACADEMIC)
        data = {"_token": "692432ab8be6b82c5b874d93a51047f376362132926c500baa501f01efab60ee",
                "_ts": "1614670925",
                "_sign": "4ef530fa37b0d6ee6d7ace90cecf27ff",
                "cmd": "show_co_affiliate",
                "entity_id": data_id}
        # SCRAPY 请求多个学者，在不同页面
        yield scrapy.FormRequest(url='https://xueshu.baidu.com/usercenter/data/author',formdata=data,callback=self.collaborate_student,meta={"data_id":data_id})

    ## 合作学者
    def collaborate_student(self,response):
        ## 合作学者1
        data_id = response.meta['data_id']
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[1]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[1]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id":data_id,"cooperative_scholar_number":cooperative_scholar_number})
        logging.info(f'------- @@@合作学者1 ------- {data_id}')

        ## 合作学者2
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[2]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[2]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者2 ------- {data_id}')

        ## 合作学者3
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[3]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[3]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者3 ------- {data_id}')

        ## 合作学者4
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[4]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[4]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者4 ------- {data_id}')

        ## 合作学者5
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[5]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[5]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者5 ------- {data_id}')

        ## 合作学者6
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[6]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[6]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者6 ------- {data_id}')

        ## 合作学者7
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[7]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[7]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者7 ------- {data_id}')

        ## 合作学者8
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[8]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[8]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者8 ------- {data_id}')

        ## 合作学者9
        data_id = response.meta['data_id']
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[9]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[9]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者9 ------- {data_id}')

        ## 合作学者10
        data_id = response.meta['data_id']
        cooperative_scholar_number = response.xpath('//div[@class="co_relmap_wrapper"]/a[10]/div/@paper-count').extract()
        cooperative_scholar_number = ''.join(cooperative_scholar_number)
        stu_url = response.xpath('//div[@class="co_relmap_wrapper"]/a[10]/@href').extract()
        stu_url = ''.join(stu_url)
        url = 'https://xueshu.baidu.com' + stu_url
        yield scrapy.Request(url=url, callback=self.collaborate_student_deep,meta={"data_id": data_id, "cooperative_scholar_number": cooperative_scholar_number})
        logging.info(f'------- @@@合作学者10 ------- {data_id}')

    ## 合作学者信息1
    def collaborate_student_deep(self,response):
        data_id = response.meta['data_id']
        cooperative_scholar_number = response.meta['cooperative_scholar_number']
        ## 合作学者 医生ID
        scholarID = response.xpath('//span[@class="p_scholarID_id"]/text()').extract()
        cooperative_schola_scholarID1 = ''.join(scholarID)
        ## 合作学者 医生名称
        doctor_name = response.xpath('//div[@class="p_name"]/text()').extract()
        cooperative_scholar_name1 = ''.join(doctor_name)
        ## 合作学者 所属医院
        hospital_name = response.xpath('//div[@class="p_affiliate"]/text()').extract()
        cooperative_scholar_hospital1 = ''.join(hospital_name)
        collaborate_student_deep1_dict = {}
        collaborate_student_deep1_dict["data_id"] = data_id
        collaborate_student_deep1_dict["cooperative_scholar_number"] = cooperative_scholar_number
        collaborate_student_deep1_dict["cooperative_schola_scholarID"] = cooperative_schola_scholarID1
        collaborate_student_deep1_dict["cooperative_scholar_name"] = cooperative_scholar_name1
        collaborate_student_deep1_dict["cooperative_scholar_hospital"] = cooperative_scholar_hospital1
        self.mongo_utils.insert_one(mongo_data=collaborate_student_deep1_dict, coll_name=const.MongoTables.BAIDU_STU)
        logging.info(f'@@@合作学者信息 ------- {cooperative_scholar_name1}')








