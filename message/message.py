import json

class WaterPlantRequest(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)


class SetScheduleRequest(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)


class SendMoistureStatMessage(object):

    def __init__(self, plantId, moistureValue):
        self.plantId = plantId
        self.moistureValue = moistureValue

    def toJson(self):
        return json.dumps(self.__dict__)
