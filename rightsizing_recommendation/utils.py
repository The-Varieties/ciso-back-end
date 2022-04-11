from django.db import connection

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
                query = ''
                if order_by == 'desc':                   
                    query = "select time, val(mode_id) as mode, sum(value) " \
                            "from node_cpu_seconds_total where " \
                            "time > now() - %(val)s::interval and val(job_id) = %(instance)s " \
                            "group by time, mode_id order by time desc limit 8"
                else:
                    query = "select time, val(mode_id) as mode, sum(value) " \
                            "from node_cpu_seconds_total where " \
                            "time > now() - %(val)s::interval and val(job_id) = %(instance)s " \
                            "group by time, mode_id order by time asc limit 8"
            
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
                        'where time > now() - %(val)s::interval and val(job_id) = %(instance)s ' \
                        'union ' \
                        'select sum(value) from "node_memory_MemTotal_bytes" where ' \
                        'time > now() - %(val)s::interval and val(job_id) = %(instance)s'
                        
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
                
def fetch_instance_details_db ():
    pass   
    
def get_cpu_usage(time_interval, instance): 
    
    prev_idle, prev_non_idle = fetch_metric_db(time_interval=time_interval, order_by="asc", instance=instance)
    curr_idle, curr_non_idle = fetch_metric_db(time_interval=time_interval, instance=instance)
    
    prev_total = prev_idle + prev_non_idle
    curr_total = curr_idle + curr_non_idle
    
    total_diff = curr_total - prev_total
    idle_diff = curr_idle - prev_idle
    
    cpu_percentage = ((total_diff - idle_diff)/total_diff) * 100
    
    return "{:.2f}%".format(cpu_percentage)

def get_ram_usage(time_interval, instance):
    available_mem, total_mem = fetch_metric_db(time_interval=time_interval, metric='ram', instance=instance)
    
    ram_percentage = (1 - (available_mem / total_mem)) * 100
    return "{:.2f}%".format(ram_percentage)

