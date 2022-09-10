import datetime
import math
import time

from django.core.exceptions import BadRequest


def format_time_interval(time_interval):
    rate = ""
    start = None
    if time_interval == '24 hours':
        rate = "1h"
        start = time.mktime((datetime.datetime.now() - datetime.timedelta(days=1)).timetuple())
    elif time_interval == '7 days':
        rate = "1d"
        start = time.mktime((datetime.datetime.now() - datetime.timedelta(days=7)).timetuple())
    elif time_interval == '30 days':
        rate = "1d"
        start = time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple())
    else:
        raise BadRequest('Time interval value must be either 24 hours, 7 days, or 30 days')
    end = time.mktime(datetime.datetime.now().timetuple())
    return end, rate, start


def format_time_rate(time_interval):
    rate = None
    if time_interval == '24 hours':
        rate = "1h"
    elif time_interval == '7 days':
        rate = "1d"
    elif time_interval == '30 days':
        rate = "1d"
    else:
        raise BadRequest('Time interval value must be either 24 hours, 7 days, or 30 days')
    return rate


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])