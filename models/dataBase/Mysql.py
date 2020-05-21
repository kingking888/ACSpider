from DBUtils.PooledDB import PooledDB
from config.setting import MYSQL
import pymysql


class MysqlPool(object):
    """
    效果未知
    example:
    with MysqlPool() as db:
        db.cursor.execute("select uid from data_user_douyin limit 500")
        db.conn.commit()
        data = db.cursor.fetchall()
    """
    config = {
        'creator': pymysql,
        'host': MYSQL["host"],
        'port': MYSQL["port"],
        'user': MYSQL["user"],
        'password': MYSQL["password"],
        'db': MYSQL["db"],
        'maxconnections': 30,
        'cursorclass': pymysql.cursors.DictCursor
    }

    pool = PooledDB(**config)

    def __enter__(self):
        self.cursor = self.conn.cursor()
        self.conn = MysqlPool.pool.connection()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    with MysqlPool() as db:
        sql = f"""INSERT INTO hot (title) VALUE ('tree')"""
        db.cursor.execute(sql)
        db.conn.commit()
