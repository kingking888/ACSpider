from spider.videos.celeryapp import data_app
from models.dataBase.mysql import MysqlPool
from models.dataBase.mongo import conn


@data_app.task(name='videos.data.test')
def data_video_test(**kwargs):
    words = kwargs.get("words")
    if words:
        for word in words:
            with MysqlPool() as db:
                sql = f"""INSERT INTO hot (title) VALUE ('{word["word"]}')"""
                db.cursor.execute(sql)
                db.conn.commit()


@data_app.task(name='videos.data.li')
def data_video_test(**kwargs):
    liVideo = kwargs.get("liVideo")
    if liVideo:
        conn.update_one(liVideo["contId"], liVideo)
