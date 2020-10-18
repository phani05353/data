from crontab import CronTab

cron = CronTab(user='pi')

job = cron.new("python /home/pi/Desktop/message.py")

job.minute.every(1)

cron.write()
