import time
import logging
from datetime import datetime, timedelta

class Scheduler:
    schedule1 = None
    schedule2 = None
    debug = False

    def __init__(self, debug, config, dbmanager, driver):
        self.debug = debug
        self.config = config
        self.log = logging.getLogger()
        self.dbmanager = dbmanager
        self.driver = driver

    def loopForever(self):
        while True:
            self.checkSchedule()
            time.sleep(1)

    # TODO: Add lock to avoid race condition
    def setSchedule(self, schedule):
        if schedule.plantPort == self.config.get('PLANT_PORT_1'):
            self.schedule1 = schedule
            self.log.info("Schedule set for plant port 1")
        if schedule.plantPort == self.config.get('PLANT_PORT_2'):
            self.schedule2 = schedule
            self.log.info("Schedule set for plant port 2")

    def checkSchedule(self):
        currentTime = datetime.now()

        # For plant1
        if self.schedule1 != None:

            if currentTime > self.schedule1.scheduledStartTime:
                self.log.info("Schedule 1 Condition meet to water plant")
                self.log.info("Schedule 1: CurrentTime: {}".format(currentTime))
                self.log.info("Schedule 1: scheduledStartTime: {}".format(self.schedule1.scheduledStartTime))
                # Water plants
                if not self.debug:
                    self.driver.waterPlants(self.config.get('PLANT_PORT_1'), self.schedule1.scheduledDuration)

                # update database
                self.dbmanager.updateLastWateredTime(self.config.get('PLANT_PORT_1'))

                # Reset schedule
                self.schedule1.scheduledStartTime += timedelta(self.schedule1.scheduledFrequency)

        # For plant2
        if self.schedule2 != None:
            if currentTime > self.schedule2.scheduledStartTime:
                self.log.info("Schedule 2 Condition meet to water plant")
                self.log.info("Schedule 2 Condition meet to water plant")
                self.log.info("Schedule 2: CurrentTime: {}".format(currentTime))
                self.log.info("Schedule 2: scheduledStartTime: {}".format(self.schedule2.scheduledStartTime))
                # Water plants
                if not self.debug:
                    self.driver.waterPlants(self.config.get('PLANT_PORT_2'), self.schedule2.scheduledDuration)

                # update database
                self.dbmanager.updateLastWateredTime(self.config.get('PLANT_PORT_2'))

                # Reset schedule
                self.schedule2.scheduledStartTime += timedelta(self.schedule2.scheduledFrequency)
