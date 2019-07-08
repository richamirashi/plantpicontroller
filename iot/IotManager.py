from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def setupIotClient(config):
    """
        Create, configure, and connect a iot client.
    """
    myAWSIoTMQTTClient = AWSIoTMQTTClient(config.get('MQTT_CLIENT'))
    myAWSIoTMQTTClient.configureEndpoint(config.get('HOST_NAME'), config.get('PORT'))
    myAWSIoTMQTTClient.configureCredentials(config.get('ROOT_CA'), config.get('PRIVATE_KEY'), config.get('CERT_FILE'))

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Establish connection
    myAWSIoTMQTTClient.connect()

    return myAWSIoTMQTTClient
