import time  
import sys
import os
import psutil
import psycopg2
from datetime import datetime

cpu = psutil.cpu_percent(interval=2)
memory_used = psutil.virtual_memory().percent
memory_avail = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

print(memory_used)
print(memory_avail)