@ECHO OFF
celery -A spider.douyin.celeryapp.app beat -l info -P eventlet --logfile=./log/crontab.log