import time  
import sys
import os
import psutil
import psycopg2
from datetime import datetime

Server = 'PI-2'
  

temp_c = os.popen("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'").readline()

  # Format the data
temp_c = float(temp_c)
temp_f = float("{0:.2f}".format(temp_c))
  
cpu = psutil.cpu_percent(interval=2)
memory_used = psutil.virtual_memory().percent
memory_avail = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

  # Print and stream
  
conn = psycopg2.connect(database="performance", user='pi', password='Sox2017!', host='192.168.0.235', port= '5432')
cur = conn.cursor()
today = datetime.now()
query = """INSERT INTO server_stats VALUES (%s, %s, %s)"""
values = (Server,temp_f, today)
cur.execute(query, values)
conn.commit()
query = """INSERT INTO server_stats_cpu VALUES (%s, %s, %s)"""
values = (Server,cpu, today)
cur.execute(query, values)
conn.commit()
query = """INSERT INTO server_stats_memory_used VALUES (%s, %s, %s)"""
values = (Server,memory_used, today)
cur.execute(query, values)
conn.commit()
query = """INSERT INTO server_stats_memory_avail VALUES (%s, %s, %s)"""
values = (Server,memory_avail, today)
cur.execute(query, values)
conn.commit()
query = """INSERT INTO job_status VALUES (%s, %s, %s)"""
values = ('pi2_stats','true', today)
cur.execute(query, values)
conn.commit()
conn.close()

