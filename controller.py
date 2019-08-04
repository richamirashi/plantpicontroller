#!/usr/bin/env python

from utils.utils import getConfig, loopForever, setupLogging
from iot.IotManager import setupIotClient
from schedule.scheduler import Scheduler
from schedule.schedule import Schedule
from message.message import SetScheduleRequest

########  Callbacks to handle subcription messages #######

# Flag to disable watering of plants
debug = True

# Global scheduler object
scheduler = Scheduler(debug)

def waterPlantSubscribeCallback(client, userdata, message):
    log.info("----------  waterPlantSubscribeCallback ---------------")
    log.info("Topic : " + str(message.topic))
    log.info("Message: " + str(message.payload))
    log.info("-------------------------------")
    # Take action and water plants
    if not debug:
        from device.driver import waterPlants
        waterPlants()

def createScheduleSubscribeCallback(client, userdata, message):
    log.info("----------  createScheduleSubscribeCallback ---------------")
    log.info("Topic : " + str(message.topic))
    log.info("Message: " + str(message.payload))
    log.info("-------------------------------")

    # take action and set the schedule
    request = SetScheduleRequest(message.payload)
    schedule = Schedule(request.plantPort, request.duration, request.frequency, request.scheduledStartTime)
    scheduler.setSchedule(schedule)

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
    waterPlantTopic = config.get('WATER_PLANT_TOPIC').format(deviceid=config.get('DEVICE_ID'), type=config.get('REQUEST'))
    plantMQTTClient.subscribeAsync(waterPlantTopic, 1, messageCallback=waterPlantSubscribeCallback)

    createScheduleTopic = config.get('CREATE_SCHEDULE_TOPIC').format(deviceid=config.get('DEVICE_ID'), type=config.get('REQUEST'))
    plantMQTTClient.subscribeAsync(createScheduleTopic, 1, messageCallback=createScheduleSubscribeCallback)

    # loop forever
    scheduler.loopForever()

    log.info("Stopping pi contoller")


if __name__ == '__main__':
    log = setupLogging()
    main()
