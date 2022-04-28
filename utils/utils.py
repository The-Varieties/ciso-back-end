from django.db import connection
import math
import json


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


def get_usage_classifier(instance):
    # 0 -> optimized
    # 1 -> under
    # 2 -> over  
    usage_category = 0
    
    cpu_usage_percentage = float(get_cpu_usage('7 days', 'node_exporter'))
    ram_usage_percentage = float(get_ram_usage('7 days', 'node_exporter'))
    
    if cpu_usage_percentage > 90:
        usage_category = 2
    elif cpu_usage_percentage < 60 and ram_usage_percentage < 60:
        usage_category = 1
    
    return usage_category

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

        
