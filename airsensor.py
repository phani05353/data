import time
import board
import busio
import adafruit_ccs811
import psycopg2
from datetime import datetime

i2c_bus = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c_bus)

while(True):
    conn = psycopg2.connect(database="performance", user='pi', password='Sox2017!', host='192.168.0.235', port= '5432')
    cur = conn.cursor()
    today = datetime.now()
    query = """INSERT INTO airquality VALUES (%s, %s, %s)"""
    values = (ccs811.eco2,ccs811.tvoc, today)
    cur.execute(query, values)
    conn.commit()
    time.sleep(20)