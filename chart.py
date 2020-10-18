
from pymongo import MongoClient
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as dt
from datetime import datetime
import re
import numpy

connect = MongoClient('mongodb://localhost:27017')
db = connect.comperfm
collection = db.performance
time_format = '%m/%d/%Y %H:%M:%S'
x = []
y = []
for record in collection.find( {},  {'time':1,'_id':0}):
    txt1 = str(record.values())
    i = re.sub("[[]+", "", txt1)
    i = re.sub("[]]+", "", i)
    i = re.sub("[']+", "", i)
    i = re.sub("[u]+", "", i)
    i = re.sub("[,]+", "", i)
    i = datetime.strptime(i,time_format)
    y.append(i)
else:
    print('')
for record in collection.find( {},  {'time_taken':1,'_id':0}):
    txt2 = str(record.values())
    h = re.sub("[[]+", "", txt2)
    h = re.sub("[]]+", "", h)
    x.append(h)
else:
    print('')
    
    dates = dt.date2num(y)
    plt.plot_date(dates, x)
    plt.gcf().autofmt_xdate()
    #myFmt = dt.DateFormatter('%H:%M')
    plt.xlabel("Time", labelpad=15, fontsize=12, color="#073642");
    plt.ylabel("Response in Seconds", labelpad=15, fontsize=12, color="#073642");
    #plt.gca().xaxis.set_major_formatter(myFmt)
    plt.grid(True, color="#93a1a1", alpha=0.3)
    plt.rc('figure', figsize=(8, 5))
    plt.title("Meijer.com Home Page Responsiveness", bbox={'facecolor':'0.8', 'pad':5})
    plt.show()