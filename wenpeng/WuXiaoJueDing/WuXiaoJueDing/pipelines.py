import json

from WuXiaoJueDing.utils import es_utils
from WuXiaoJueDing.spiders.const import ESIndex

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class WuxiaojuedingPipeline:
    def process_item(self, item, spider):
        es_data = json.dumps(dict(item), default=set_default)
        # with open('XinWenZiXun.txt','a+',encoding='utf-8') as d:
        #     d.write(json.dumps(es_data,ensure_ascii=False)+'\n')
        # # 数据存储到 es 中
        data = json.loads(es_data)
        # # logging.info('------- insert es data -------' + str(data['pm_id']))
        es_utils.insert_or_replace(ESIndex.PAPER_PUBMED, d=data)
        return item
