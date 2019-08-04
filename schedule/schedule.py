from datetime import datetime

class Schedule:

    def __init__(self, plantPort, duration, frequency, scheduledStartTime):
        self.plantPort = plantPort
        self.duration = duration # In seconds
        self.frequency = int(frequency)  # In days
        scheduledDateTime = datetime.strptime(scheduledStartTime, '%Y-%m-%d %H:%M:%S')
        self.scheduledStartTime = scheduledDateTime
