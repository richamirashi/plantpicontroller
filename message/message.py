import json

class SendMoistureStatMessage(object):

    def __init__(self, plantId, moistureValue):
        self.plantId = plantId
        self.moistureValue = moistureValue

    def toJson(self):
        return json.dumps(self.__dict__)
