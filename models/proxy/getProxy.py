from models.dataBase.Redis import rds


def getOneProxy():
    """
    从redis取一条代理，需要先运行freeProxy获取
    :return:
    """
    proxy = rds.srandmember("useful_proxies").decode()
    proxyMeta = f"http://{proxy}"
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


if __name__ == '__main__':
    print(getOneProxy())
