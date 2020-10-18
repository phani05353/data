import time

from gpiozero import MotionSensor


pir = MotionSensor(21)

while True:
    if pir.motion_detected:
        print('Motion detected')
        time.sleep(10)