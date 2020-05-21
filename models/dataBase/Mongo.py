from pymongo import MongoClient
from config.setting import MONGO


class MongoDB:
    """
    常用语句，用self.con获取cursor
    避免重复创建
    """
    def __init__(self, db, table):
        self.client = MongoClient(MONGO["host"], MONGO["port"])
        if MONGO.get("user") and MONGO.get("password"):
            self.client.admin.authenticate(MONGO["user"], MONGO["password"])
        self.db = self.client[db]
        self.table = self.db[table]
        self.con = self.table

    def updateOne(self, _id, data):
        """通过id更新数据,存在更新，不存在插入"""
        result = self.con.update_one({"_id": _id}, {"$set": data}, True)
        return result


liVideoTable = MongoDB(db="videos", table="liVideo")

if __name__ == '__main__':
    liVideoTable.updateOne("15803215", {"data": "test"})
