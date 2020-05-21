from kombu import Exchange, Queue, binding
from celery.schedules import crontab
from config.setting import RABBITMQ

def create_task_queues(exchange_name, binding_list):
    """
    批量创建Queue
    :param exchange_name:exchange名称
    :param binding_list:(routing_keys，queue)列表
    :return:[Queue(),Queue(),...]
    """
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
    """
    参照Routing Tasks定义路由器函数，在定义task name时和routing_key一致可以避免多写task_routes规则
    在task_routes直接传递route_task地址，route_task参数怎么用在文档里没找到
    :param name: task name
    :param args:
    :param kwargs:
    :param options:
    :param task:
    :param kw:
    :return:
    """
    return {
        "exchange": "videos.crawl",
        "exchange_type": "topic",
        "routing_key": name
    }


class AppConfig(object):
    """
    class配置写法，配置名称固定，celery4版本以后小写+下划线写法
    """
    broker_url = f"amqp://{RABBITMQ['user']}:{RABBITMQ['password']}@{RABBITMQ['host']}/"
    # 全局开启返回任务结果
    task_ignore_result = True
    # 只返回失败结果
    # task_store_errors_even_if_ignored = True
    task_serializer = "json"
    accept_content = ["json"]
    task_default_queue = "default"
    task_default_exchange = "default"
    task_default_routing_key = "default"
    imports = ["spider.videos.tasks.tasks"]
    # worker执行100个任务销毁，防止内存泄露
    celeryd_max_tasks_per_child = 100
    # 单个任务的运行时间不超过60s，超过会被SIGKILL信号杀死
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
