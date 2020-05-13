from spider.douyin.celeryapp import data_app
from models.dataBase.mysql import MysqlPool


@data_app.task(name='douyin.data.test')
def save_douyin_hot_search(**kwargs):
    words = kwargs.get("words")
    if words:
        for word in words:
            with MysqlPool() as db:
                sql = f"""INSERT INTO hot (title) VALUE ('{word["word"]}')"""
                db.cursor.execute(sql)
                db.conn.commit()
