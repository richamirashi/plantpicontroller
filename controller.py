#!/usr/bin/env python

from utils.utils import getConfig, loopForever, setupLogging
from iot.IotManager import setupIotClient
from schedule.scheduler import Scheduler
from schedule.schedule import Schedule
from message.message import SetScheduleRequest, GetMoistureStatRequest, WaterPlantRequest
from db.dbmanager import DBManager

# Flag to disable watering of plants
debug = True

# QOS
QOS = 1

########  Callbacks to handle subcription messages #######

def waterPlantSubscribeCallback(client, userdata, message):
    log.info("----------  waterPlantSubscribeCallback ---------------")
    log.info("Topic : " + str(message.topic))
    log.info("Message: " + str(message.payload))
    log.info("-------------------------------")

    # Parse request
    request = WaterPlantRequest(message.payload)

    # update database
    dbmanager.updateLastWateredTime(request.plantPort)

    # Take action and water plants
    if not debug:
        driver.waterPlants(request.plantPort, request.duration)


def createScheduleSubscribeCallback(client, userdata, message):
    log.info("----------  createScheduleSubscribeCallback ---------------")
    log.info("Topic : " + str(message.topic))
    log.info("Message: " + str(message.payload))
    log.info("-------------------------------")

    # take action and set the schedule
    request = SetScheduleRequest(message.payload)
    schedule = Schedule(request.plantPort, request.scheduledDuration, request.scheduledFrequency, request.scheduledStartTime)
    scheduler.setSchedule(schedule)

def moistureStatsSubscribeCallback(client, userdata, message):
    log.info("----------  moistureStatsSubscribeCallback ---------------")
    log.info("Topic : " + str(message.topic))
    log.info("Message: " + str(message.payload))
    log.info("-------------------------------")

    # Parse request
    request = GetMoistureStatRequest(message.payload)

    moistureStat = "DEBUG"

    if not debug:
        # Get soil moisture stats
        moistureStat = driver.getSoilMoistureStat(request.plantPort)

    # update database
    dbmanager.updateSoilMoistureStat(request.plantPort, moistureStat)

def main():
    """
        Program starts here
    """

    # start subscriptions in background
    waterPlantTopic = config.get('WATER_PLANT_TOPIC').format(deviceid=config.get('DEVICE_ID'), type=config.get('REQUEST'))
    plantMQTTClient.subscribeAsync(waterPlantTopic, QOS, messageCallback=waterPlantSubscribeCallback)

    createScheduleTopic = config.get('CREATE_SCHEDULE_TOPIC').format(deviceid=config.get('DEVICE_ID'), type=config.get('REQUEST'))
    plantMQTTClient.subscribeAsync(createScheduleTopic, QOS, messageCallback=createScheduleSubscribeCallback)

    moistureStatsTopic = config.get('MOISTURE_STATS_TOPIC').format(deviceid=config.get('DEVICE_ID'), type=config.get('REQUEST'))
    plantMQTTClient.subscribeAsync(moistureStatsTopic, QOS, messageCallback=moistureStatsSubscribeCallback)

    # loop forever
    scheduler.loopForever()

    log.info("Stopping pi contoller")


if __name__ == '__main__':
    log = setupLogging()
    log.info("Starting pi controller")

    config = getConfig()
    log.info("Using config : " + str(config))

    # connect to aws iot
    plantMQTTClient = setupIotClient(config)
    log.info("IOT client connected sucessfully!")

    # Connect to db
    dbmanager = DBManager(config)

    # Set driver
    driver = None
    if not debug:
        from device.driver import Driver
        driver = Driver(config)

    # Global scheduler object
    scheduler = Scheduler(debug, config, dbmanager, driver)

    main()
