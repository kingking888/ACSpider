from celery import Celery
from spider.videos.celeryconfig import AppConfig, DataAppConfig

app = Celery(
    'app',
    include=[
        'spider.videos.tasks.tasks',
    ]
)
app.config_from_object(AppConfig)


data_app = Celery(
    'data_app',
    include=[
        'spider.videos.tasks.data',
    ]
)
data_app.config_from_object(DataAppConfig)

if __name__ == '__main__':
    data_app.start()

