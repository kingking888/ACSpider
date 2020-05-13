from celery import Celery
from spider.douyin.celeryconfig import DevelopConfig, DataConfig

app = Celery(
    'app',
    include=[
        'spider.douyin.tasks.tasks',
    ]
)
app.config_from_object(DevelopConfig)


data_app = Celery(
    'data_app',
    include=[
        'spider.douyin.tasks.data',
    ]
)
data_app.config_from_object(DataConfig)

