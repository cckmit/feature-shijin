
import pymongo

MONGO_HOST, MONGO_PORT, MONGO_DB = '127.0.0.1', 27020, 'spider_py'

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

    def find_all(self,coll_name):
        coll = self.db[coll_name]
        return coll.find()

    def get_coll_count(self,coll_name):
        coll = self.db[coll_name]
        return coll.count()

