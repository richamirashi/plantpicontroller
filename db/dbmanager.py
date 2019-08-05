import boto.dynamodb
import time
import logging
from datetime import datetime

class DBManager:

    def __init__(self, config):
        self.conn = boto.dynamodb.connect_to_region(
            'us-west-2',
            aws_access_key_id=config.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=config.get('AWS_SECRET_KEY')
        )
        self.config = config
        self.log = logging.getLogger()

    def updateLastWateredTime(self, plantPort):
        try:
            currentTime = self.getFormattedCurrentTime()
            table = self.conn.get_table('plant')
            deviceId = self.config.get('DEVICE_ID')
            plantItem = table.get_item(
                hash_key=deviceId,
                range_key=plantPort
                )
            if plantItem is None:
                self.log.error("DB: updateLastWateredTime: unable to find plant item {}:{}".format(deviceId, plantPort))
                return
            plantItem['lastWatered'] = currentTime
            plantItem.put()
            self.log.info("DB: updateLastWateredTime: updated last watered time for: {}:{}".format(deviceId, plantPort))
        except:
            self.log.exception("DB: updateLastWateredTime: Exception occured while updating database")

    def updateSoilMoistureStat(self, plantPort, moistureStat):
        try:
            currentTime = self.getFormattedCurrentTime()
            table = self.conn.get_table('plant')
            deviceId = self.config.get('DEVICE_ID')
            plantItem = table.get_item(
                hash_key=deviceId,
                range_key=plantPort
                )
            if plantItem is None:
                self.log.error("DB: updateSoilMoistureStat: unable to find plant item {}:{}".format(deviceId, plantPort))
                return
            plantItem['moistureStatLastTimeStamp'] = currentTime
            plantItem['moistureStat'] = str(moistureStat)
            plantItem.put()
            self.log.info("DB: updateSoilMoistureStat: updated soil moisture start for: {}:{}".format(deviceId, plantPort))
        except:
            self.log.exception("DB: updateSoilMoistureStat: Exception occured while updating database")

    def getFormattedCurrentTime(self):
        currentTime = datetime.now()
        return currentTime.strftime('%Y-%m-%d %H:%M:%S')
