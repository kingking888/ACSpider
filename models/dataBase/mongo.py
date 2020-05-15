from pymongo import MongoClient
from ROOT_PATH import root
import configparser
import os


class MongoDB:

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, "instance"):
            cls.instance = super(MongoDB, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read(os.path.join(root, "conf.ini"), encoding="utf-8")
        items = dict(conf.items('mongo'))
        self.client = MongoClient(items["host"], 27017)
        self.client.admin.authenticate(items["user"], items["password"])
        self.table = self.client[items["db"]][items["table"]]

    def update_one(self, _id, data):
        """通过id更新数据,存在更新，不存在插入"""
        result = self.table.update_one({"_id": _id}, {"$set": data}, True)
        return result


conn = MongoDB()
