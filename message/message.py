import json

class WaterPlantRequest(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

class SetScheduleRequest(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

class GetMoistureStatRequest(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

    def toJson(self):
        return json.dumps(self.__dict__)
