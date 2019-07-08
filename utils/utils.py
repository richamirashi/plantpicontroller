import sys
import time
import yaml
import logging

def loopForever():
    while True:
        time.sleep(1)

def getConfig():
    with open("config.yaml", 'r') as stream:
        return yaml.safe_load(stream)

def setupLogging():
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # log to file
    """
    fileHandler = logging.FileHandler(".log".format(logPath, fileName))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    """

    # Console logger
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger
