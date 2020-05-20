from kombu import Exchange, Queue, binding
from celery.schedules import crontab
from config.setting import RABBITMQ


def create_task_queues(exchange_name, binding_list):
    binding_map = {}
    exchange = Exchange(exchange_name, type="topic")

    queues = []
    for routing_key, queue_name in binding_list:
        binding_map.setdefault(queue_name, [])
        binding_map[queue_name].append(routing_key)

    for queue_name, routing_keys in binding_map.items():
        queues.append(
            Queue(
                queue_name,
                [binding(exchange, routing_key=routing_key) for routing_key in routing_keys],
                queue_arguments={"x-queue-mode": "lazy", "x-max-priority": 10},
            )
        )
    return queues


def route_task(name, args, kwargs, options, task=None, **kw):
    return {
        "exchange": "videos.crawl",
        "exchange_type": "topic",
        "routing_key": name
    }


class AppConfig(object):
    broker_url = f"amqp://{RABBITMQ['user']}:{RABBITMQ['password']}@{RABBITMQ['host']}/"
    task_ignore_result = True
    task_serializer = "json"
    accept_content = ["json"]
    task_default_queue = "default"
    task_default_exchange = "default"
    task_default_routing_key = "default"
    imports = ["spider.videos.tasks.tasks"]
    celeryd_max_tasks_per_child = 50
    celeryd_task_time_limit = 60
    bindings = [

        ("videos.test.#", "videos.test"),
        ("videos.li.#", "videos.li"),

    ]

    task_queues = create_task_queues("videos.crawl", bindings)
    task_routes = (route_task,)

    enable_utc = True
    timezone = "Asia/Shanghai"

    beat_schedule = {
        "test": {
            "task": "videos.test.crawl",
            "schedule": crontab(minute="*/1"),
        }
    }


def data_route_task(name, args, kwargs, options, task=None, **kw):
    return {
        "exchange": "videos.data",
        "exchange_type": "topic",
        "routing_key": name
    }


class DataAppConfig(object):
    broker_url = f"amqp://{RABBITMQ['user']}:{RABBITMQ['password']}@{RABBITMQ['host']}/"
    task_ignore_result = True
    task_serializer = "json"
    accept_content = ["json"]
    task_default_queue = "default"
    task_default_exchange = "default"
    task_default_routing_key = "default"
    bindings = [

        ("videos.data.test.#", "videos.data.test"),
        ("videos.data.li.#", "videos.data.li"),

    ]
    task_queues = create_task_queues("videos.data", bindings)
    task_routes = (data_route_task,)
    enable_utc = True
    timezone = "Asia/Shanghai"
