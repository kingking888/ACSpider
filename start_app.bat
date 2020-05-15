@ECHO OFF
celery worker -A spider.videos.celeryapp.app -l warn -n app -P eventlet -Q videos.li --logfile=./log/app.log --concurrency=20 -E
rem celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --concurrency=20 -E