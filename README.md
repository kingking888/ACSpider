# ACSpider
##### 简单轻便可自由拓展的爬虫框架，基于celery，支持分布式 多节点 高并发 定时任务
##### 集成免费proxy pool，爬取10家免费代理网站，可拓展其他代理
### 下载安装
* 下载源码：

```shell
git clone git@github.com:heyaug/ACSpider.git

或者直接到https://github.com/heyaug/ACSpider 下载zip文件
```

* 安装依赖:

```shell
pip install -r requirements.txt
```

* 配置config/setting.py:

```shell
# Config/setting.py 为项目配置文件

# 需要配置rabbitMQ
RABBITMQ = {
    "host": "127.0.0.1",
    "user": "guest",
    "password": "guest"
}

# 如果使用代理池，需要配置redis
REDIS = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 1,
    "max_connections": 50
}
# 其他数据库可自由拓展
```

* 启动

```shell
在ACSpider目录下：
# 启动爬虫worker
celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --concurrency=10 -E
# 启动保存数据worker
celery worker -A spider.videos.celeryapp.data_app -l info -n data_app -P eventlet -Q videos.data.li --concurrency=10 -E
# 如有代理需要爬取免费代理
python models\proxy\freeProxy.py

# demo
# 执行ACSpider\spider\videos\tasks\tasks.py的publishLiVideos()
```

### 拓展
###### 1、celery主要配置文件在 spider/videos/celeryapp.py和spider/videos/celeryconfig.py
###### 2、爬虫相关配置在AppConfig，新爬虫在bindings增加(routing key，queue name),修改exchange在route_task和create_task_queues处，如需定时任务在beat_schedule添加配置
###### 3、爬虫写法参照spider/videos/tasks/tasks.py，保存数据写法参照spider/videos/tasks/data.py

