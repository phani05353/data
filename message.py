import time  
import sys
import os
import psutil
import psycopg2
from datetime import datetime

Server = 'PI-3'
  

temp_c = os.popen("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'").readline()

  # Format the data
temp_c = float(temp_c)
temp_f = float("{0:.2f}".format(temp_c))
  
cpu = psutil.cpu_percent(interval=2)
memory_used = psutil.virtual_memory().percent
memory_avail = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

  # Print and stream
  
conn = psycopg2.connect(database="performance", user='pi', password='Sox2017', host='127.0.0.1', port= '5432')
cur = conn.cursor()
today = datetime.now()
query = """INSERT INTO server_status VALUES (%s, %s, %s,%s)"""
values = (Server,today,temp_c,"server_temperature")
cur.execute(query, values)
conn.commit()
query = """INSERT INTO server_status VALUES (%s, %s, %s,%s)"""
values = (Server,today,cpu,"server_cpu")
cur.execute(query, values)
conn.commit()
query = """INSERT INTO server_status VALUES (%s, %s, %s,%s)"""
values = (Server,today,memory_used, "server_memory_used")
cur.execute(query, values)
conn.commit()
query = """INSERT INTO job_status VALUES (%s, %s, %s)"""
values = ('pi3_stats','true', today) 
cur.execute(query, values)
conn.commit()
conn.close()

