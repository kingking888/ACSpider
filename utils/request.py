import random
import requests
from lxml import html


def retry(times=1):
    """
    装饰器，主要用于重试
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            t = times
            while t > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"{func.__name__}:{e}")
                    t -= 1

        return wrapper

    return decorator


@retry(times=3)
def getHtmlTree(url):
    """
    获取html树
    """
    headers = {'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               }
    htm = requests.get(url=url, headers=headers, timeout=10).content
    return html.etree.HTML(htm)


@retry(times=3)
def ex_request(url):
    """
    执行requests
    """
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    ]
    headers = {'User-Agent': random.choice(ua_list),
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    return requests.get(url=url, headers=headers, timeout=10)
