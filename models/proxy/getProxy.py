from models.dataBase.Redis import rds


def getOneProxy():
    proxy = rds.srandmember("useful_proxies").decode()
    proxyMeta = f"http://{proxy}"
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


if __name__ == '__main__':
    print(getOneProxy())
