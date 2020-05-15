import configparser
import os

from DBUtils.PooledDB import PooledDB
import pymysql

from ROOT_PATH import root


class MysqlPool(object):
    """
    example:
    with MysqlPool() as db:
        db.cursor.execute("select uid from data_user_douyin limit 500")
        db.conn.commit()
        data = db.cursor.fetchall()
    """
    conf = configparser.ConfigParser()
    conf.read(os.path.join(root, "conf.ini"), encoding="utf-8")
    items = dict(conf.items('mysql'))
    config = {
        'creator': pymysql,
        'host': items["host"],
        'port': 3306,
        'user': items["user"],
        'password': items["password"],
        'db': items["db"],
        'maxconnections': 30,
        'cursorclass': pymysql.cursors.DictCursor
    }

    pool = PooledDB(**config)

    def __enter__(self):
        self.conn = MysqlPool.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()
