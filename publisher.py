from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

host = "a1cai3u3kh553t-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/pi/4925Project"
clientId = "photon"
topic = "demo-topic"

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}AmazonRootCA1.cer".format(certPath), "{}iot-private.pem.key".format(certPath), "{}iot-certificate.pem.crt".format(certPath))

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    message = {}
    message['message'] = "demo-topic-sample-message"
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(10)
myAWSIoTMQTTClient.disconnect()
