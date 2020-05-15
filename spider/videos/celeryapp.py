from celery import Celery
from spider.videos.celeryconfig import DevelopConfig, DataConfig

app = Celery(
    'app',
    include=[
        'spider.videos.tasks.tasks',
    ]
)
app.config_from_object(DevelopConfig)


data_app = Celery(
    'data_app',
    include=[
        'spider.videos.tasks.data',
    ]
)
data_app.config_from_object(DataConfig)

