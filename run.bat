@echo off
start cmd /k "python models\proxy\freeProxy.py"
start cmd /k "celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --concurrency=10 -E"
start cmd /k "celery worker -A spider.videos.celeryapp.data_app -l info -n data_app -P eventlet -Q videos.data.li --concurrency=10 -E"