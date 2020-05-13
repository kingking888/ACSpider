from kombu import Exchange, Queue, binding
from celery.schedules import crontab


def create_task_queues(binding_list):
    binding_map = {}
    exchange = Exchange('douyin.crawl', type='topic')

    queues = []
    for routing_key, queue_name in binding_list:
        binding_map.setdefault(queue_name, [])
        binding_map[queue_name].append(routing_key)

    for queue_name, routing_keys in binding_map.items():
        queues.append(
            Queue(
                queue_name,
                [binding(exchange, routing_key=routing_key) for routing_key in routing_keys],
                queue_arguments={'x-queue-mode': 'lazy', 'x-max-priority': 10},
            )
        )
    return queues


def route_task(name, args, kwargs, options, task=None, **kw):
    return {
        'exchange': 'douyin.crawl',
        'exchange_type': 'topic',
        'routing_key': name
    }


class DevelopConfig(object):
    broker_url = 'amqp://guest:guest@127.0.0.1/'
    task_ignore_result = True
    task_serializer = 'json'
    accept_content = ['json']
    task_default_queue = 'default'
    task_default_exchange = 'default'
    task_default_routing_key = 'default'
    imports = ['spider.douyin.tasks.tasks']
    celeryd_max_tasks_per_child = 50

    bindings = [

        ('douyin.test.#', 'douyin.test'),

    ]

    task_queues = create_task_queues(bindings)
    task_routes = (route_task,)

    enable_utc = True
    timezone = "Asia/Shanghai"

    beat_schedule = {
        'video_monitor': {
            'task': 'douyin.test.crawl',
            'schedule': crontab(minute='*/1'),
        },
    }


def data_route_task(name, args, kwargs, options, task=None, **kw):
    return {
        'exchange': 'douyin.data',
        'exchange_type': 'topic',
        'routing_key': name
    }


class DataConfig(object):
    broker_url = 'amqp://guest:guest@127.0.0.1/'
    task_ignore_result = True
    task_serializer = 'json'
    accept_content = ['json']
    task_default_queue = 'default'
    task_default_exchange = 'default'
    task_default_routing_key = 'default'

    exchange = Exchange('douyin.data', type='topic')
    task_queues = [
        Queue(
            'douyin.data.test',
            [binding(exchange, routing_key='douyin.data.test.#')],
            queue_arguments={'x-queue-mode': 'lazy'}
        ),
    ]
    task_routes = (data_route_task,)
    enable_utc = True
    timezone = "Asia/Shanghai"
