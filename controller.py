#!/usr/bin/env python

from utils.utils import getConfig, loopForever, setupLogging
from iot.IotManager import setupIotClient
from device.driver import waterPlants

########  Callbacks to handle subcription messages #######

def waterPlantSubscribeCallback(client, userdata, message):
    log.info("----------  waterPlantSubscribeCallback ---------------")
    log.info("Topic : " + str(message.topic))
    log.info("Message: " + str(message.payload))
    log.info("-------------------------------")

    # Take action and water plants
    waterPlants()

def main():
    """
        Program starts here
    """
    log.info("Starting pi controller")

    config = getConfig()
    log.info("Using config : " + str(config))

    # connect to aws iot
    plantMQTTClient = setupIotClient(config)
    log.info("IOT client connected sucessfully!")

    # start subscriptions in background
    waterPlantTopic = config.get('WATER_PLANT_TOPIC').format(deviceid=config.get('DEVICE_ID'))
    plantMQTTClient.subscribeAsync(waterPlantTopic, 1, messageCallback=waterPlantSubscribeCallback)

    # loop forever
    loopForever()

    log.info("Stopping pi contoller")


if __name__ == '__main__':
    log = setupLogging()
    main()
