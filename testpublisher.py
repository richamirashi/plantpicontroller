#!/usr/bin/env python

import sys
import time
import random
import logging
import json
from datetime import datetime

from utils.utils import getConfig, loopForever, setupLogging
from iot.IotManager import setupIotClient

def main():

    log.info("Starting publisher")

    config = getConfig()
    log.info("Unsing config : " + str(config))

    # connect to aws iot
    plantMQTTClient = setupIotClient(config)
    log.info("IOT client connected sucessfully!")

    message = {}
    message['message'] = "Test message"
    messageJson = json.dumps(message)
    waterPlantTopic = config.get('WATER_PLANT_TOPIC').format(deviceid=config.get('DEVICE_ID'))
    plantMQTTClient.publish(waterPlantTopic, messageJson, 1)

    time.sleep(2)

if __name__ == '__main__':
    log = setupLogging()
    main()
