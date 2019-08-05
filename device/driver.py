import os
import json
import time
import logging

import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

PUMP_PIN = 12           # pin12

log = logging.getLogger()

def waterPlants(plantPort, duration):
    duration = int(duration)
    setup()
    try:
        GPIO.output(PUMP_PIN, GPIO.LOW)  # Pump On
        time.sleep(duration)
        GPIO.output(PUMP_PIN, GPIO.HIGH)  # Pump off
        log.info("Watered plant")
    except:
        log.exception("Error occured during watering plant!")
        destroy()

def getSoilMoistureStat(plantPort):
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    # Create single-ended input on channel 0
    chan = AnalogIn(ads, ADS.P0)
    return getNormalizedMoisturePercentValue(chan.value)


def getNormalizedMoisturePercentValue(value):
    low = 9000 # for 100%
    high = 21000 # for 0%
    if value is None:
        return 0;
    if value > high:
        return 0
    if value <= low:
        return 100
    return  100 - ( ((float(value) - low ) / high) * 100 )

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP_PIN, GPIO.OUT)
    GPIO.output(PUMP_PIN, GPIO.HIGH)

def destroy():
	GPIO.output(PUMP_PIN, GPIO.HIGH)     # pump off
	GPIO.cleanup()                     # Release resource
