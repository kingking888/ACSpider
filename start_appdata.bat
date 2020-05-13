@ECHO OFF
celery worker -A spider.douyin.celeryapp.data_app -l info -P eventlet -Q douyin.data.test --logfile=./log/data_app.log