import scrapy
import logging

'''
全球论文库

'''

class PaperPubmedSpider(scrapy.Spider):
    name = 'paper-pubmed'
    allowed_domains = []
    start_urls = ['https://www.baidu.com/']

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        total_url = len(self.crawler.engine.slot.inprogress)  # 当前正在运行请求
        prepare_url = len(self.crawler.engine.slot.scheduler)  # 待采集URL条数
        logging.info(f"待采集URL条数：{prepare_url}，当前运行请求数：{total_url}")
        #proxy = CommonUtils().randomProxyIP()
        spider_url = response.url
        if( 'baidu.com' in spider_url):
            logging.info('======= 当前追加待采集的论文id ======= ')
            with open(file='/home/zengxiangxu/pubmed.txt', encoding='utf-8') as file:
                pm_id_list = file.readlines()
                for pm_id in pm_id_list:
                    detail_url = f'https://pubmed.ncbi.nlm.nih.gov/{pm_id}'.replace('\n','')
                    logging.info(detail_url)
                    yield scrapy.Request(detail_url, callback=self.parse, meta={'pm_id': pm_id})
                   # yield scrapy.Request(detail_url, callback=self.parse, meta={'pm_id': pm_id,"proxy": proxy})

        # 全球论文库
        if ( 'pubmed.ncbi.nlm.nih.gov' in spider_url):
            pm_id = long(response.meta['pm_id'])
            doc = pq(response.body)
            error_page = doc('.error-page').text().lower()
            if('is not available' in error_page  and 'please consider searching' in error_page):
                logging.info(f'当前论文数据视为无效，被过滤：{pm_id}')
                return

            doc('.article-source #full-view-journal').remove()
            journal_info = doc('.article-source:first').text()
            full_text_links = set()
            for item in doc('.full-text-links-list a').items():
                full_text_links.add(item.attr('href'))

            doi = ''
            for doi_element in doc('#short-view-identifiers li span').items():
                if( 'doi:' in doi_element.text().lower() ):
                    doi = doi_element.text().replace('DOI:', '').strip()
                    break

            author_addr_dict = {}
            for author_addr_element in doc('.affiliations .item-list li').items():
                key = author_addr_element.find('sup').text()
                author_addr_element.find('sup').remove()
                value = author_addr_element.text()
                author_addr_dict[key] = value
            author = []
            for author_name_element in doc('.authors-list:first .authors-list-item').items():
                key = author_name_element.find("sup").text()
                author_name_element.find("sup").remove()
                value = author_name_element.text()
                author_info_dict = {}
                author_info_dict['name'] = value
                if key in author_addr_dict.keys():
                    author_info_dict['addr'] = author_addr_dict[key]
                author.append(author_info_dict)

            title = doc('.heading-title:first').text()
            doc('.abstr h3').remove()
            abstract_info = doc('#abstract').html()
            abstract_info_nolabel = doc('#abstract').text()
            nct_id = ''
            nct_id_str = ''
            for item in doc('.abstract p').items():
                if('clinicaltrials.gov' in item.text().lower()):
                    nct_id = item.find('a').text()
                    nct_id_str = item.html()
            medical_source_url = ''
            for item in  doc('.linkout-category-links li').items():
                if('clinicaltrials.gov' in item.text().lower()):
                    medical_source_url = item.find('a').attr('href')

            secondary_source_id = doc('.supplemental-data-actions-trigger').text()
            mesh_terms = get_link(doc, '#mesh-terms', 'mesh_terms_name', 'mesh_terms_url')
            substances = get_link(doc, '#substances', 'substances_name', 'substances_url')
            publication_types = get_link(doc, '#publication-types', 'publication_types_name', 'publication_types_url')



def get_link(doc, label_str, name, name_url):
    data_arr = []
    elements = doc(label_str)
    if(elements.size() == 0 ):
        return data_arr
    elements.find('.keyword-actions-links').remove()
    elements.find('.supplemental-data-actions-links').remove()
    li_elements = elements.find('.keywords-list li')
    if('supplemental-data' in label_str):
        li_elements = elements.find('.supplemental-data-list li')
    for li_element in li_elements.items():
        if(li_element.find('button').size() == 0):
            continue
        key = li_element.find('button').text()
        data_obj = {}
        data_obj[name] = key
        splits = key.split('/')
        if('supplemental-data' in label_str):
            data_obj[name_url] = "https://www.clinicaltrials.gov/show/"+splits[len(splits)-1]
        else:
            data_obj[name_url] = "https://www.ncbi.nlm.nih.gov/mesh?sort=date&term=" + splits[0].replace(" ", "+")
        data_arr.append(data_obj)
    return data_arr