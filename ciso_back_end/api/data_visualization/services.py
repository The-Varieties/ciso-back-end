from django.core.exceptions import BadRequest
import datetime
from datetime import timedelta, timezone
import requests as req
from ciso_back_end.commons.constant import PROMETHEUS_QUERY_RANGE_URL
from ciso_back_end.commons.utils import format_time_interval, convert_size

LOCAL_ZONE = timezone(timedelta(hours=7))


def get_data_visualization_cpu(instance, time_interval):
    end, rate, start = format_time_interval(time_interval)

    cpu_category_queries = {
        'system': 'avg(rate(node_cpu_seconds_total{hostname=~"%s", mode="system"}[%s])) by (hostname) *100' % (
            instance, rate),
        'user': 'avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="user"}[%s])) * 100' % (instance, rate),
        'iowait': 'avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="iowait"}[%s])) by (hostname) *100' % (
            instance, rate),
        'idle': '(1 - avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="idle"}[%s])) by (hostname))*100' % (
            instance, rate)
    }

    sub_list = []
    hostname = None

    for category in cpu_category_queries:
        params = {'query': cpu_category_queries[category], 'step': rate, 'start': start, 'end': end}
        data = req.get(PROMETHEUS_QUERY_RANGE_URL, params=params).json()

        if data['status'] == 'success':
            if category == 'system':
                hostname = data['data']['result'][0]['metric']['hostname']

            dict_result = {
                'sub': category,
            }
            values = _format_into_local_zone(data)
            dict_result['values'] = values

            sub_list.append(dict_result)
        else:
            raise BadRequest('Instance not found')

    return hostname, sub_list


def get_data_visualization_ram(instance, time_interval):
    end, rate, start = format_time_interval(time_interval)

    ram_category_queries = {
        'total': 'node_memory_MemTotal_bytes{hostname=~"%s"}' % instance,
        'used': 'node_memory_MemTotal_bytes{hostname=~"%s"} - node_memory_MemAvailable_bytes{hostname=~"%s"}'
                % (instance, instance),
        'available': 'node_memory_MemAvailable_bytes{hostname=~"%s"}' % instance
    }

    sub_list = []
    hostname = None

    for category in ram_category_queries:
        params = {'query': ram_category_queries[category], 'step': rate, 'start': start, 'end': end}
        data = req.get(PROMETHEUS_QUERY_RANGE_URL, params=params).json()
        if data['status'] == 'success':
            if category == 'total':
                hostname = data['data']['result'][0]['metric']['hostname']
            dict_result = {
                'sub': category,
            }
            values = _format_into_local_zone(data)
            dict_result['values'] = values

            sub_list.append(dict_result)
        else:
            raise BadRequest('Instance not found')

    return hostname, sub_list


def _format_into_local_zone(data):
    values = data['data']['result'][0]['values']
    for i in range(len(values)):
        dt = datetime.datetime.fromtimestamp(values[i][0])
        dt_local = dt.astimezone(LOCAL_ZONE)
        values[i][0] = dt_local
    return values
