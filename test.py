import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.cleanup()

GPIO.setup(4,GPIO.OUT)

