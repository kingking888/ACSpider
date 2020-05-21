from spider.videos.celeryapp import data_app
from models.dataBase.Mysql import MysqlPool
from models.dataBase.Mongo import liVideoTable


@data_app.task(name='videos.data.test')
def data_video_test(**kwargs):
    """
    存到mysql
    """
    words = kwargs.get("words")
    if words:
        for word in words:
            with MysqlPool() as db:
                sql = f"""INSERT INTO hot (title) VALUE ('{word["word"]}')"""
                db.cursor.execute(sql)
                db.conn.commit()


@data_app.task(name='videos.data.li.Video')
def data_li_video(**kwargs):
    """
    取数据，存到mongodb
    """
    liVideo = kwargs.get("liVideo")
    if liVideo:
        liVideoTable.updateOne(liVideo["contId"], liVideo)


@data_app.task(name='videos.data.li.Comment')
def data_li_comment(**kwargs):
    liComment = kwargs.get("liComment")
    if liComment:
        liVideoTable.updateOne(liComment["commentId"], liComment)
