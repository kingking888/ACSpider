@ECHO OFF
rem -P eventlet 协程并发效果更好
rem -l info 日志等级
rem -n app worker name
rem -Q 指定队列
rem --logfile=./log/app.log 指定日志位置
rem --concurrency=20或-C 20 并发数量
rem 启动设置 https://docs.celeryproject.org/en/stable/userguide/workers.html
rem celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --logfile=./log/app.log --concurrency=20 -E
celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --concurrency=10 -E