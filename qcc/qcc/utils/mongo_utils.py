
import pymongo

MONGO_HOST, MONGO_PORT, MONGO_DB = '127.0.0.1', 27017, 'spider_py'

class MongoUtils:

    def __init__(self):
        self.client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.client[MONGO_DB]

    # data : dict
    def insert_one(self,mongo_data,coll_name):
        coll = self.db[coll_name]
        coll.insert_one(document = mongo_data)

    def insert_many(self,mongo_list,coll_name):
        coll = self.db[coll_name]
        coll.insert_many(documents = mongo_list)

    # 修改指定字段的数据，如果不存在则直接创建
    def update_one(self, query, value, coll_name):
        coll = self.db[coll_name]
        coll.update_one(query, value, True)

    def find_all(self,coll_name):
        coll = self.db[coll_name]
        return coll.find()

    def get_count(self,coll_name):
        coll = self.db[coll_name]
        return coll.count()

    def delete_one(self, query, coll_name):
        coll = self.db[coll_name]
        coll.delete_one(query)


if __name__ == '__main__':
    '''
    query = {"fund_name_id": "1"}
    value = {"$set": {"alexa": "12345"}}
    MongoUtils().update_one(query=query,value=value,coll_name='a_detail')
    '''
    query = {"id" : "4613"}
    MongoUtils().delete_one(query=query,coll_name='drug_en_title')