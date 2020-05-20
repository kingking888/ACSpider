import redis
from config.setting import REDIS

pool = redis.ConnectionPool(host=REDIS["host"], port=REDIS["port"], db=REDIS["db"],
                            max_connections=REDIS["max_connections"])
rds = redis.Redis(connection_pool=pool)

if __name__ == '__main__':
    print(rds.srandmember("useful_proxies").decode())
