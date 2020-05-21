@ECHO OFF
celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --concurrency=70 -E