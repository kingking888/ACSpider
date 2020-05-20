import re

import celery
import requests
import time
from spider.videos.celeryapp import app, data_app
from utils.encrypt import md5_string
from utils.randomStr import randomString


@app.task(
    name='videos.test.crawl',
    bind=True,
    max_retries=8,
    retry_backoff=True,
    rate_limit='1/s',
)
def videoTest(self):
    url = "https://aweme.snssdk.com/aweme/v1/hot/search/list/"
    headers = {"Charset": "UTF-8",
               "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G9350 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 haokan/5.11.0.10 (Baidu; P1 5.1.1)/gnusmas_22_1.1.5_0539G-MS/1014613h/F27F5C565733789471232729BAB5C37C%7CO/1/5.11.0.10/511001/1",
               }
    res = requests.get(url, headers=headers, timeout=5)
    words = res.json()
    data_app.send_task('videos.data.test', kwargs={"words": words})


@app.task(
    name='videos.li.crawl',
    bind=True,
    max_retries=8,
    retry_backoff=True,
    rate_limit='150/s',
)
def videoLi(self, url):
    try:
        XSerialNum = str(int(time.time()))
        XClientID = "861" + randomString(12)
        XClientHash = md5_string(XSerialNum + XClientID)
        headers = {
            "X-Client-Version": "6.7.2",
            "X-Channel-Code": "lsp-yyb",
            "X-Client-Agent": "OneP9us_HD1910_5.1.1",
            "X-IMSI": "46000",
            "X-Long-Token": "",
            "X-Platform-Version": "5.1.1",
            "X-Client-Hash": XClientHash,
            "X-User-ID": "",
            "X-Platform-Type": "2",
            "X-Client-ID": XClientID,
            "X-Serial-Num": XSerialNum,
            "Host": "app.pearvideo.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"}
        res = requests.get(url, headers=headers, timeout=5).json()
        resultCode = res.get("resultCode")
        if resultCode == '1':
            content = res.get("content")
            data_app.send_task('videos.data.li', kwargs={"liVideo": content})
            return
        if resultCode == '5':
            return
        raise Exception("no data")
    except Exception as e:
        celery.app.base.logger.warn(e)
        app.send_task("videos.li.crawl", args=(url,))


@app.task(
    name='videos.li.comment',
    bind=True,
    max_retries=8,
    retry_backoff=True,
    rate_limit='150/s',
)
def videoLiComment(self, commentUrl):
    try:
        XSerialNum = str(int(time.time()))
        XClientID = "861" + randomString(12)
        XClientHash = md5_string(XSerialNum + XClientID)
        headers = {
            "X-Client-Version": "6.7.2",
            "X-Channel-Code": "lsp-yyb",
            "X-Client-Agent": "OneP9us_HD1910_5.1.1",
            "X-IMSI": "46000",
            "X-Long-Token": "",
            "X-Platform-Version": "5.1.1",
            "X-Client-Hash": XClientHash,
            "X-User-ID": "",
            "X-Platform-Type": "2",
            "X-Client-ID": XClientID,
            "X-Serial-Num": XSerialNum,
            "Host": "app.pearvideo.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"}
        res = requests.get(commentUrl, headers=headers, timeout=5).json()
        resultCode = res.get("resultCode")
        commentList = res.get("commentList")
        nextUrl = res.get("nextUrl")
        postId = re.findall("postId=(\d+)?&", commentUrl)[0]
        if len(commentList) > 0:
            for comment in commentList:
                comment.update({"postId": postId})
                data_app.send_task('videos.data.li.Comment', kwargs={"liComment": comment})
            if nextUrl:
                app.send_task("videos.li.comment", args=(nextUrl,))
            return

        if resultCode == '1' and len(commentList) == 0:
            return
        raise Exception
    except Exception as e:
        celery.app.base.logger.warn(e)
        app.send_task("videos.li.comment", args=(commentUrl,))


if __name__ == '__main__':
    def publishLiVideos():
        for i in range(1000000, 1674000):
            li_url = f"http://app.pearvideo.com/clt/jsp/v4/content.jsp?contId={i}"
            app.send_task("videos.li.crawl", args=(li_url,))


    def publishVideoComments():
        from models.dataBase.Mongo import liVideoTable
        postIds = set()
        for i in liVideoTable.con.find({}, {"postId": 1}):
            postId = i.get("postId")
            if postId and postId not in postIds:
                url = f"http://app.pearvideo.com/clt/jsp/v4/getComments.jsp?postId={postId}&score=&filterIds="
                app.send_task("videos.li.comment", args=(url,))
                postIds.add(postId)


    publishLiVideos()
    # publishVideoComments()
