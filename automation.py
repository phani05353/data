import subprocess
import psycopg2
from datetime import datetime

subprocess.call(" python /home/pi/temp.py 1", shell=True)
conn = psycopg2.connect(database="performance", user='pi', password='Sox2017!', host='192.168.0.235', port= '5432')
cur = conn.cursor()
today = datetime.now()
query = """INSERT INTO job_status VALUES (%s, %s, %s)"""
values = ('temp_sensor','true', today) #value will be the job status and so is the name 
cur.execute(query, values)
conn.commit()
conn.close()
