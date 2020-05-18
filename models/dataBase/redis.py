import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1, max_connections=50)
rds = redis.Redis(connection_pool=pool)
