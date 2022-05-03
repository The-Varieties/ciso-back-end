from django.db import connection
import math
import json
import requests as req
import datetime
import time
from datetime import timedelta, timezone


# Fetching from database functions
def fetch_metric_db (instance, time_interval='5 minutes', order_by='desc', metric='cpu'):
    """ Fetching values from node_cpu_seconds_total table

    Args:
        time_interval (str, optional): Fetch from past given time. Defaults to '5 minutes'.
        order_by (str, optional): Either showing in ascending or descending order based on time. Defaults to 'desc'.

    Returns:
        total_idle: cpu values from idle and iowait modes
        total_non_idle: cpu values from non idle and iowait modes
    """
    with connection.cursor() as curr:
        match metric:
            case 'cpu':
                if order_by == 'desc':                   
                    query = 'select time, val(mode_id) as mode, sum(value) ' \
                            'from node_cpu_seconds_total where ' \
                            'time > now() - %(val)s::interval and val(hostname_id) = %(instance)s ' \
                            'group by time, mode_id order by time desc limit 8;'
                else:
                    query = 'select time, val(mode_id) as mode, sum(value) ' \
                            'from node_cpu_seconds_total where ' \
                            'time > now() - %(val)s::interval and val(hostname_id) = %(instance)s ' \
                            'group by time, mode_id order by time asc limit 8;'
                
                
            
                curr.execute(query, {'val': time_interval, 'instance': instance})
                
                records = curr.fetchall()
                                    
                total_idle = 0
                total_non_idle = 0           
                
                for row in records:
                    if row[1] in ["idle", "iowait"]:
                        total_idle += row[2]
                    else:
                        total_non_idle += row[2]
                    
                return total_idle, total_non_idle 
            
            case 'ram':
                query = 'select sum(value) from "node_memory_MemAvailable_bytes" ' \
                        'where time > now() - %(val)s::interval and val(hostname_id) = %(instance)s ' \
                        'union ' \
                        'select sum(value) from "node_memory_MemTotal_bytes" where ' \
                        'time > now() - %(val)s::interval and val(hostname_id) = %(instance)s;'
                        
                curr.execute(query, {'val': time_interval, 'instance': instance})
                
                records = curr.fetchall()
                
                available_memory = 0
                total_memory = 0
                
                for row in records:
                    if available_memory:
                        total_memory = row[0]
                    else:
                        available_memory = row[0]
                
                return available_memory, total_memory
    
                
def fetch_instance_details_db (instance, type):
    with connection.cursor() as curr:
        match type:
            case 'total_ram':
                query = 'select value from "node_memory_MemTotal_bytes" ' \
                        'where val(hostname_id) = %(instance)s limit 1;'
                curr.execute(query, {'instance': instance})
                record = curr.fetchone()
                return math.ceil(record[0] / (1024**3))
                
            case 'uptime':
                query = 'select (extract(epoch from now()) ' \
                        ' - (select value from node_boot_time_seconds ' \
                        'where val(hostname_id) = %(instance)s order by time desc limit 1));'
                curr.execute(query, {'instance': instance})
                record = curr.fetchone()
                
                total_time = round(record[0] / 3600, 2)
                time_unit = ""
                
                
                if (total_time < 0):
                    total_time = round(record[0] / 60)
                    time_unit = "minutes"
                elif (total_time >= 24):
                    total_time = math.trunc(total_time / 24)
                    time_unit = "days"
                    
                return "{0} {1}".format(total_time, time_unit)
                    
            case 'cpu_count':
                query = "select count(distinct cpu_id) from node_cpu_seconds_total where val(mode_id) = 'system' and val(hostname_id) = %(instance)s;"
                curr.execute(query, {'instance': instance})
                
                record = curr.fetchone()
                
                return record[0]
                
            case 'server_info':
                query = 'select jsonb(labels) from node_uname_info where val(hostname_id) = %(instance)s limit 1;'
                curr.execute(query, {'instance': instance})
                
                record = curr.fetchone()
                
                return record[0]
    

def get_server_info(instance):
    data = fetch_instance_details_db('node_exporter', 'server_info')
    obj = json.loads(data)
    return obj
        
def get_cpu_usage(time_interval, instance): 
    prev_idle, prev_non_idle = fetch_metric_db(time_interval=time_interval, order_by="asc", instance=instance)
    curr_idle, curr_non_idle = fetch_metric_db(time_interval=time_interval, instance=instance)
    
    prev_total = prev_idle + prev_non_idle
    curr_total = curr_idle + curr_non_idle
    
    total_diff = curr_total - prev_total
    idle_diff = curr_idle - prev_idle
    
    cpu_percentage = ((total_diff - idle_diff)/total_diff) * 100
    
    return cpu_percentage

def get_ram_usage(time_interval, instance):
    available_mem, total_mem = fetch_metric_db(time_interval=time_interval, metric='ram', instance=instance)
    
    ram_percentage = (1 - (available_mem / total_mem)) * 100

    return ram_percentage


def get_usage_classifier(instance, under_threshold=35, over_threshold=95):
    # 0 -> optimized
    # 1 -> under
    # 2 -> over  
    usage_category = 0
    
    cpu_usage_percentage = float(get_cpu_usage('7 days', 'node_exporter'))
    ram_usage_percentage = float(get_ram_usage('7 days', 'node_exporter'))
      
    if cpu_usage_percentage > over_threshold and ram_usage_percentage > over_threshold:
        usage_category = 2
    elif cpu_usage_percentage < under_threshold and ram_usage_percentage < under_threshold:
        usage_category = 1
    
    return usage_category

def get_recommendations(usage_category):
    
    if usage_category == 2:
        recommendations = [{
            'recommedantion': 'Upsize the overutilized EC2 instance',
            'details': 'Upsize the EC2 instances by selecting the right instance family to add more hardware resources',
            'steps': ['Navigate to the EC2 dashboard in your AWS', 
                      'Select the overutilized instance and stop it', 
                      'Change the current instance type to upsize it', 
                      'After choosing the right instance type, then apply it', 
                      'Start the EC2 instance again']
        }, {
            'recommendation': 'Perform horizontal scaling',
            'details': 'Increase the capacity of Auto Scaling Group (ASG) to handle the workload by adding more EC2 instances to the group, which consists of the overutilized EC2 instance.',
            'steps': ['Navigate to the EC2 dashboard in your AWS', 
                      'In the left panel, choose Auto Scaling Groups', 
                      'Select the AWS ASG, which you want to upgrade', 
                      'From the Details tab, click the Edit button to edit the selected ASG configuration', 
                      'Increase the number of EC2 instances that can be run in that ASG by raising the existing number in the Desired and Max fields',
                      'Finally click Save to apply the changes']
        }]
    
    elif usage_category == 1:
        recommendations = [{
            'recommendation': 'Downsize the underutilized EC2 instance',
            'details': 'Downsize the EC2 instances by selecting the right instance family to fit the current workload, so it will reduce operation costs',
            'steps': ['Navigate to the EC2 dashboard in your AWS',
                      'Select the underutilized instance and stop it',
                      'Change the current instance type to downsize it',
                      'After choosing the right instance type, then apply it',
                      'Start the EC2 instance again']
        }]
        
    return recommendations   

def get_targets_for_prometheus():
    #  response_data = [{
    #         "targets": ["node-exporter:9100", "ec2-44-204-214-30.compute-1.amazonaws.com:9100"],
    #         "labels": {
    #             "hostname": "node"
    #         }
#     }]
    with connection.cursor() as curr:
        query = "SELECT instance_id, instance_name, instance_ipv4 from database_instance GROUP BY instance_id, instance_name"
        curr.execute(query) 
        
        records = curr.fetchall()
        response_data = []
        
        for row in records:
            target_dict = {}
            target_dict["targets"] = [row[2]]
            target_dict["labels"] = {"hostname": row[1]}

            response_data.append(target_dict)
        return response_data


def data_visualization(instance, time_interval, metric):
    """Providing time-series data for the metrics in time range

    Args:
        instance (string): the hostname of the instance
        time_interval (string): the time interval for the range of the time series, which is either '24 hours', '7 days', or '30 days'
        metric (string): the chosen metric to be visualized, which is either 'cpu' or 'ram' 

    Returns:
        JSON: {
                "name": "ram",
                "time": "last 24 hours",
                "hostname": "node",
                "results": [
                    {
                        "sub": "total",
                        "values": [
                            [
                                "2022-05-03T14:31:51+07:00",
                                "6149365760"
                            ],
                            [
                                "2022-05-03T15:31:51+07:00",
                                "6149365760"
                            ],
                            [
                                "2022-05-03T16:31:51+07:00",
                                "6149365760"
                            ],
                            [
                                "2022-05-03T17:31:51+07:00",
                                "6149365760"
                            ],
                            [
                                "2022-05-03T19:31:51+07:00",
                                "6149365760"
                            ],
                            [
                                "2022-05-03T20:31:51+07:00",
                                "6149365760"
                            ]
                        ]
              }, {...}
    """    
    
    url = "http://prometheus:9090/api/v1/query_range"
    response = {
        'name': metric,
        'time': 'last %s' % (time_interval)
    }
    
   
    if (time_interval == '24 hours'):
        rate = "1h"
        start = time.mktime((datetime.datetime.now() - datetime.timedelta(days=1)).timetuple())
    elif (time_interval == '7 days'):
        rate = "1d"
        start = time.mktime((datetime.datetime.now() - datetime.timedelta(days=7)).timetuple())
    elif (time_interval == '30 days'):
        rate = "1d"
        start = time.mktime((datetime.datetime.now() - datetime.timedelta(days=30)).timetuple())

    end = time.mktime(datetime.datetime.now().timetuple())
    local_zone = timezone(timedelta(hours=7))
    
    if str.lower(metric) == 'cpu': 
        cpus = {
            'system': 'avg(rate(node_cpu_seconds_total{hostname=~"%s", mode="system"}[%s])) by (hostname) *100' % (instance, rate),
            'user': 'avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="user"}[%s])) * 100' % (instance, rate),
            'iowait': 'avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="iowait"}[%s])) by (hostname) *100' % (instance, rate),
            'idle': '(1 - avg(rate(node_cpu_seconds_total{hostname=~"%s",mode="idle"}[%s])) by (hostname))*100' % (instance, rate)
        }
                
        array_subs = []

        for key in cpus:  
            params = {'query': cpus[key], 'step': rate, 'start': start, 'end': end}
            data = req.get(url, params=params).json()
            if key == 'system':
                response['hostname'] = data['data']['result'][0]['metric']['hostname']
            dict_result = {
                'sub': key,
            }
            values = data['data']['result'][0]['values']
            for i in range(len(values)):
                dt = datetime.datetime.fromtimestamp(values[i][0])
                dt_local = dt.astimezone(local_zone)
                values[i][0] = dt_local
            dict_result['values'] = values
            
            array_subs.append(dict_result)
        
        response['results'] = array_subs
        
     
        return response
    
    elif str.lower(metric) == 'ram':
        rams = {
            'total': 'node_memory_MemTotal_bytes{hostname=~"%s"}' % (instance),
            'used': 'node_memory_MemTotal_bytes{hostname=~"%s"} - node_memory_MemAvailable_bytes{hostname=~"%s"}' % (instance, instance),
            'available': 'node_memory_MemAvailable_bytes{hostname=~"%s"}' % (instance)
        }
        
        array_subs = []
        
        for key in rams:  
            params = {'query': rams[key], 'step': rate, 'start': start, 'end': end}
            data = req.get(url, params=params).json()
            if key == 'total':
                response['hostname'] = data['data']['result'][0]['metric']['hostname']
            dict_result = {
                'sub': key,
            }
            values = data['data']['result'][0]['values']
            for i in range(len(values)):
                dt = datetime.datetime.fromtimestamp(values[i][0])
                dt_local = dt.astimezone(local_zone)
                values[i][0] = dt_local
            dict_result['values'] = values
            
            array_subs.append(dict_result)
        
        response['results'] = array_subs
        
     
        return response
    
    


    

        
