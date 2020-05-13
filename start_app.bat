@ECHO OFF
celery worker -A spider.douyin.celeryapp.app -l info -P eventlet -Q douyin.test --logfile=./log/app.log