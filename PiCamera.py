# -*- coding: utf-8 -*-
# Main Modules
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from picamera import PiCamera
from fractions import Fraction
import datetime
import smtplib
from time import sleep
import RPi.GPIO as gpio
import datetime
# AWS Modules
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
# AWS Configuration
host = "a1cai3u3kh553t-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/pi/4925Project/"
clientId = "photon"
topic = "doorbell"

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

# Set the pin mode 
gpio.setmode(gpio.BCM)

# Connecting push button to GPIO Pin 18
gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_UP)

# Initializes the Pi Camera and sets it for night time photos
camera = PiCamera(resolution = (1280, 720))

#Setting up email parameters
toAddr = 'iotdoorbell@outlook.com'
fromAddr = 'iotdoorbell@outlook.com'
subject = 'Doorbell pressed, someone is at the door'

# Publish to the same topic in a loop forever
loopCount = 0

while True:
	
	# Obtains the value from button press
	inputCamera = gpio.input(18)

	# When pressed, it saves the current date and time as the file name
	if inputCamera == False:
		print("Camera Button Pressed")
		picturefile = camera.capture('/home/pi/4925Project/' +  datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.png')
		sleep(.2)
		camera.rotation = 180 #Innately takes a picture upside down, so it needs to turned 180 degrees
		camera.capture(picturefile)
		
		print("Image Captured")
		
		# Create the message
		msg = MIMEMultipart()
		msg['Subject'] = subject
		msg['From'] = fromAddr
		meg['To'] = toAddr
		
		# Attaches picture to email
		File = open(picturefile, 'rb')
		img = MIMEImage(File.read())
		File.close()
		msg.attach(img)
		
		# Credentials for fromAddr
		username = 'iotdoorbell@outlook.com'
		password = 'password4925'
	        
		# Setting up the email to be sent from a Microsoft account
	        server = smtplib.SMTP('smtp-mail.outlook.com:587')
	        server.starttls()
	        server.login(username,password)
	        server.sendmail(fromAddr, toAddr, msg.as_string)
	        server.quit()

		print("Email Sent")
		
    		message = {}
   		message['message'] = "Someone is at the door!"
    		messageJson = json.dumps(message)
	    	myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    		print('Published topic %s: %s\n' % (topic, messageJson))
    		loopCount += 1
    		time.sleep(10)
myAWSIoTMQTTClient.disconnect()
