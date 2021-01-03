
import pymongo
from pharmcube_spider.run_env import get_run_env_dict

class MongoUtils:

    def __init__(self):
        run_env_dict = get_run_env_dict()['mongo']
        self.client = pymongo.MongoClient(host=run_env_dict['host'], port=run_env_dict['port'])
        self.db = self.client[run_env_dict['db']]

    # data : dict
    def insert_one(self, mongo_data, coll_name):
        coll = self.db[coll_name]
        coll.insert_one(document=mongo_data)

    def insert_many(self, mongo_list, coll_name):
        coll = self.db[coll_name]
        coll.insert_many(documents=mongo_list)

    # 修改指定字段的数据，如果不存在则直接创建
    def update_one(self, query, value, coll_name):
        coll = self.db[coll_name]
        coll.update_one(query, value, True)

    def update_many(self, query, value, coll_name):
        coll = self.db[coll_name]
        coll.update_many(query, value, True)

    def find_all(self, coll_name):
        coll = self.db[coll_name]
        return coll.find()

    def get_count(self, coll_name):
        coll = self.db[coll_name]
        return coll.count()

    def delete_one(self, query, coll_name):
        coll = self.db[coll_name]
        coll.delete_one(query)

    def find_query(self, query, coll_name):
        coll = self.db[coll_name]
        return coll.find(query)



if __name__ == '__main__':

    '''
    json数组查询
        query = {'send_project_list.send_project_name':'ipo_us'} #send_email_list
    
    mongo list
        #查询list里面的数据
        query = {'$or': [{'send_project_name':'drug_us_orange'}, {'send_project_name': 'drug_us_orange1'}]}  # $or; $and
        #往list追加数据
        query = {"name": "zxx"}
        value = {"$addToSet": {"send_project_name": "12345"}}
        #往list删除数据
        query = {"name": "zxx"}
        value = {"$pop": {"send_project_name": "12345"}}
        
    results = MongoUtils().find_query(query=query, coll_name='a_detail')
    for result in results:
    
    '''



    '''
    query = {"fund_name_id": "1"}
    value = {"$set": {"alexa": "12345"}}  # addToSet
    MongoUtils().update_one(query=query,value=value,coll_name='a_detail')
    '''

