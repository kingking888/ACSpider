@ECHO OFF
celery -A spider.videos.celeryapp.app beat -l info --logfile=./log/crontab.log