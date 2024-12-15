import os
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(4,GPIO.OUT)

try:
    while True:
        time.sleep(0.1)
except:
    GPIO.cleanup()



