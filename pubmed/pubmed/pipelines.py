# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#数据存储到数据库中
import json
import logging
from pubmed.utils import es_utils
from pubmed.spiders.const import ESIndex

logger = logging.getLogger(__name__)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError
#file_write = open('/home/zengxiangxu/test.txt', 'a+') #往文件中追加数据

class PaperPubmedPipeline:
    def process_item(self, item, spider):
        es_data = json.dumps(dict(item), default=set_default)
        # 数据存储到 es 中
        data = json.loads(es_data)
        logging.info('------- insert es data -------'+str(data['pm_id']))
        es_utils.insert_or_replace(ESIndex.PAPER_PUBMED, d=data)
        # 数据存储到文件中
        #file_write.write(es_data+"\n")
        return item
