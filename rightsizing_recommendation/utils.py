from django.db import connection

def fetch_cpu_db (time_interval='5 minutes', order_by='desc'):
    with connection.cursor() as curr:
        
        query = ''
        if order_by == 'desc':                   
            query = "select time, val(mode_id) as mode, sum(value) " \
                    "from node_cpu_seconds_total where " \
                    "time > now() - %(val)s::interval group by time, mode_id " \
                    "order by time desc limit 8"
        else:
            query = "select time, val(mode_id) as mode, sum(value) " \
                    "from node_cpu_seconds_total where " \
                    "time > now() - %(val)s::interval group by time, mode_id " \
                    "order by time asc limit 8"
    
        curr.execute(query, {'val': time_interval})
        
        records = curr.fetchall()
        
        total_idle = 0
        total_non_idle = 0
        
        for row in records:
            if row[1] in ["idle", "iowait"]:
                total_idle += row[2]
            else:
                total_non_idle += row[2]
        
        return total_idle, total_non_idle       
        
def get_cpu_usage(): 
    prev_idle, prev_non_idle = fetch_cpu_db('5 minutes', order_by="asc")
    curr_idle, curr_non_idle = fetch_cpu_db('5 minutes')
    
    prev_total = prev_idle + prev_non_idle
    curr_total = curr_idle + curr_non_idle
    
    total_diff = curr_total - prev_total
    idle_diff = curr_idle - prev_idle
    
    cpu_percentage = ((total_diff - idle_diff)/total_diff) * 100
    
    return "{:.2f}%".format(cpu_percentage)
