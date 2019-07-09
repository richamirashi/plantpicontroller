import os
import json
import time
import logging

import RPi.GPIO as GPIO

PUMP_PIN = 12           # pin12

log = logging.getLogger()

def waterPlants():
    setup()
    try:
        GPIO.output(PUMP_PIN, GPIO.LOW)  # Pump On
        time.sleep(6)
        GPIO.output(PUMP_PIN, GPIO.HIGH)  # Pump off
        log.info("Watered plant")
    except:
        log.exception("Error occured during watering plant!")
        destroy()

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP_PIN, GPIO.OUT)
    GPIO.output(PUMP_PIN, GPIO.HIGH)

def destroy():
	GPIO.output(PUMP_PIN, GPIO.HIGH)     # pump off
	GPIO.cleanup()                     # Release resource
