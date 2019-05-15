import time
import os
import logging
import motor_runner
import RPi.GPIO as GPIO

from time import sleep
import RPi.GPIO as GPIO




from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)



def run_motor(self, params, packet):
 
 print("oayload", int(float(packet.payload)))
 
 logging.warning('topic'+packet.topic)
 SetAngle(int(float(packet.payload)))
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 50)
pwm.start(0)
 
delay_period = 0.01

logging.warning('Watch out!')
myMQTTClient = AWSIoTMQTTClient("raspberryPiHome") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
 
myMQTTClient.configureEndpoint("a1hvpyzsj18z2s.iot.us-east-2.amazonaws.com", 8883)
 
certRootPath = '/home/pi/Documents/awt-iot/'
myMQTTClient.configureCredentials("{}root-ca.pem".format(certRootPath), "{}cloud.pem.key".format(certRootPath), "{}cloud.pem.crt".format(certRootPath))
 
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
 
myMQTTClient.connect()
myMQTTClient.subscribe("home/runMotor", 1, run_motor)

def looper():
    while True:
        time.sleep(5)

looper()
def function_handler(event, context):
    pwm.stop()
    GPIO.cleanup()
    return
