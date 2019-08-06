import os
import json
import time
import logging

import board
import busio

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO


class Driver:

    def __init__(self, config):
        self.log = logging.getLogger()
        self.config = config

    def waterPlants(self, plantPort, duration):
        duration = int(duration)
        self.setup()
        if plantPort is self.config.get('PLANT_PORT_1'):
            pumpPin = self.config.get('PUMP_PIN_1')
        else:
            pumpPin = self.config.get('PUMP_PIN_2')

        try:
            GPIO.output(pumpPin, GPIO.LOW)  # Pump On
            time.sleep(duration)
            GPIO.output(pumpPin, GPIO.HIGH)  # Pump off
            log.info("Watered plant")
        except:
            log.exception("Error occured during watering plant!")
            self.destroy()

    def getSoilMoistureStat(self, plantPort):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        # Create single-ended input on channel 0
        chan = AnalogIn(ads, ADS.P0)
        return self.getNormalizedMoisturePercentValue(chan.value)


    def getNormalizedMoisturePercentValue(self, value):
        low = 9000 # for 100%
        high = 21000 # for 0%
        if value is None:
            return 0;
        if value > high:
            return 0
        if value <= low:
            return 100
        return  100 - ( ((float(value) - low ) / high) * 100 )

    def setup(self):
        GPIO.setmode(GPIO.BMC)  # GPIO.BOARD
        GPIO.setup(self.config.get('PUMP_PIN_1'), GPIO.OUT)
        GPIO.output(self.config.get('PUMP_PIN_1'), GPIO.HIGH)
        GPIO.setup(self.config.get('PUMP_PIN_2'), GPIO.OUT)
        GPIO.output(self.config.get('PUMP_PIN_2'), GPIO.HIGH)

    def destroy(self):
    	GPIO.output(self.config.get('PUMP_PIN_1'), GPIO.HIGH)     # pump off
    	GPIO.output(self.config.get('PUMP_PIN_2'), GPIO.HIGH)     # pump off
    	GPIO.cleanup()                                            # Release resource
