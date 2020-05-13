import datetime
import time


def timestamp10_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp13_to_date(timestamp):
    return datetime.datetime.fromtimestamp(int(int(timestamp) / 1000))


def date_to_timestamp(date):
    if isinstance(date, str):
        return int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
    elif isinstance(date, datetime.datetime):
        return int(date.timestamp())
