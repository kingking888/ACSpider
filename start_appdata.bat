@ECHO OFF
rem celery worker -A spider.videos.celeryapp.data_app -l warn -n data_app -P eventlet -Q videos.data.li --logfile=./log/data_app.log --concurrency=30 -E
celery worker -A spider.videos.celeryapp.data_app -l info -n data_app -P eventlet -Q videos.data.li --concurrency=10 -E