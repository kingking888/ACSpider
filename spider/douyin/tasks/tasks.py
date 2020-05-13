from spider.douyin.celeryapp import app, data_app
import requests


@app.task(
    name='douyin.test.crawl',
    bind=True,
    max_retries=8,
    retry_backoff=True,
    rate_limit='1/s',
)
def get_hot_search_list(self):
    url = "https://aweme.snssdk.com/aweme/v1/hot/search/list/"
    headers = {"Charset": "UTF-8",
               "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G9350 Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 haokan/5.11.0.10 (Baidu; P1 5.1.1)/gnusmas_22_1.1.5_0539G-MS/1014613h/F27F5C565733789471232729BAB5C37C%7CO/1/5.11.0.10/511001/1",
               }
    res = requests.get(url, headers=headers, timeout=5)
    words = res.json()["data"]["word_list"]
    data_app.send_task('douyin.data.test', kwargs={"words": words})


if __name__ == '__main__':
    app.send_task("douyin.test.crawl")
