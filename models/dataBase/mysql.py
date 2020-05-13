from DBUtils.PooledDB import PooledDB
import pymysql


class MysqlPool(object):
    """
    example:
    with MysqlPool() as db:
        db.cursor.execute("select uid from data_user_douyin limit 500")
        db.conn.commit()
        data = db.cursor.fetchall()
    """

    config = {
        'creator': pymysql,
        'host': "127.0.0.1",
        'port': 3306,
        'user': "root",
        'password': "1234567",
        'db': "douyin",
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
