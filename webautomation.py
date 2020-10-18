import subprocess
import time
import psycopg2
from datetime import datetime

while(True):
    subprocess.call(" python /home/pi/script.py 1", shell=True)
    conn = psycopg2.connect(database="performance", user='pi', password='Sox2017!', host='192.168.0.235', port= '5432')
    cur = conn.cursor()
    today = datetime.now()
    query = """INSERT INTO job_status VALUES (%s, %s, %s)"""
    values = ('web_automation','True', today) #value will be the job status and so is the name 
    cur.execute(query, values)
    conn.commit()
    conn.close()
    time.sleep(300)