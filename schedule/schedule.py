from datetime import datetime

class Schedule:

    def __init__(self, plantPort, scheduledDuration, scheduledFrequency, scheduledStartTime):
        self.plantPort = plantPort
        self.scheduledDuration = int(scheduledDuration) # In seconds
        self.scheduledFrequency = int(scheduledFrequency)  # In days
        scheduledDateTime = datetime.strptime(scheduledStartTime, '%Y-%m-%d %H:%M:%S')
        self.scheduledStartTime = scheduledDateTime
