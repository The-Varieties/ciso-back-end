import math
import requests as req
from rest_framework.exceptions import APIException
from ciso_back_end.commons.constant import PROMETHEUS_QUERY_URL
from ciso_back_end.commons.utils import format_time_rate
from ciso_back_end.commons.values.usage_category import UsageCategory


def get_cpu_usage_v2(time_interval, instance):
    rate = format_time_rate(time_interval)

    params = {'query': '100 - (avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="idle"}[%s])) * 100)'
                       % (instance, rate)}
    result = req.get(PROMETHEUS_QUERY_URL, params=params).json()

    if result['status'] == 'success':
        cpu_usage = float(result['data']['result'][0]['value'][1])
        return cpu_usage
    else:
        raise APIException()


def get_ram_usage_v2(instance):
    params = {
        'query': '(1 - (node_memory_MemAvailable_bytes{hostname=~"%s"} / (node_memory_MemTotal_bytes{'
                 'hostname=~"%s"})))* 100' % (instance, instance)}

    result = req.get(PROMETHEUS_QUERY_URL, params=params).json()

    if result['status'] == 'success':
        ram_usage = float(result['data']['result'][0]['value'][1])
        return ram_usage
    else:
        raise APIException()


def get_instance_total_ram(instance):
    params = {'query': 'sum(node_memory_MemTotal_bytes{hostname=~"%s"})' % instance}
    result = req.get(PROMETHEUS_QUERY_URL, params=params).json()
    return math.ceil(int(result['data']['result'][0]['value'][1]) / (1024 ** 3))


def get_instance_uptime(instance):
    params = {'query': 'avg(time() - node_boot_time_seconds{hostname=~"%s"})' % instance}
    result = req.get(PROMETHEUS_QUERY_URL, params=params).json()

    total_time = round(float(result['data']['result'][0]['value'][1]) / 3600, 2)
    time_unit = ""

    if total_time < 0:
        total_time = round(result['data']['result'] / 60)
        time_unit = "minutes"
    elif total_time >= 24:
        total_time = math.trunc(total_time / 24)
        time_unit = "days"

    return "{0} {1}".format(total_time, time_unit)


def get_instance_cpu_count(instance):
    params = {'query': 'count(node_cpu_seconds_total{hostname=~"%s", mode="system"})' % instance}
    result = req.get(PROMETHEUS_QUERY_URL, params=params).json()

    return result['data']['result']


def get_instance_server_info(instance):
    params = {'query': 'node_uname_info {hostname=~"%s"}' % instance}
    result = req.get(PROMETHEUS_QUERY_URL, params=params).json()

    return result['data']['result']


def get_usage_classifier(instance, time_interval='7 days', under_threshold=35, over_threshold=95):
    usage_category = UsageCategory.Optimized

    cpu_usage_percentage = get_cpu_usage_v2(time_interval, instance)
    ram_usage_percentage = get_ram_usage_v2(instance)

    if cpu_usage_percentage and ram_usage_percentage:
        if cpu_usage_percentage > over_threshold or ram_usage_percentage > over_threshold:
            usage_category = UsageCategory.OverUtilized
        elif cpu_usage_percentage < under_threshold or ram_usage_percentage < under_threshold:
            usage_category = UsageCategory.UnderUtilized

        recommendations = _get_recommendations(usage_category=usage_category)

        return cpu_usage_percentage, ram_usage_percentage, usage_category.name, recommendations
    else:
        raise APIException()


def _get_recommendations(usage_category):
    recommendations = ''

    if usage_category == UsageCategory.OverUtilized:
        recommendations = [{
            'recommendation': 'Upsize the over-utilized EC2 instance',
            'details': 'Upsize the EC2 instances by selecting the right instance family to add more hardware resources',
            'steps': ['Navigate to the EC2 dashboard in your AWS',
                      'Select the over-utilized instance and stop it',
                      'Change the current instance type to upsize it',
                      'After choosing the right instance type, then apply it',
                      'Start the EC2 instance again']
        }, {
            'recommendation': 'Perform horizontal scaling',
            'details': 'Increase the capacity of Auto Scaling Group (ASG) to handle the workload by adding more EC2 '
                       'instances to the group, which consists of the over-utilized EC2 instance.',
            'steps': ['Navigate to the EC2 dashboard in your AWS',
                      'In the left panel, choose Auto Scaling Groups',
                      'Select the AWS ASG, which you want to upgrade',
                      'From the Details tab, click the Edit button to edit the selected ASG configuration',
                      'Increase the number of EC2 instances that can be run in that ASG by raising the existing '
                      'number in the Desired and Max fields',
                      'Finally click Save to apply the changes']
        }]

    elif usage_category == UsageCategory.UnderUtilized:
        recommendations = [{
            'recommendation': 'Downsize the underutilized EC2 instance',
            'details': 'Downsize the EC2 instances by selecting the right instance family to fit the current '
                       'workload, so it will reduce operation costs',
            'steps': ['Navigate to the EC2 dashboard in your AWS',
                      'Select the underutilized instance and stop it',
                      'Change the current instance type to downsize it',
                      'After choosing the right instance type, then apply it',
                      'Start the EC2 instance again']
        }]

    return recommendations
