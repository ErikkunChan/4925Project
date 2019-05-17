# -*- coding: utf-8 -*-
# Libraries
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from picamera import PiCamera
from fractions import Fraction
import datetime
import smtplib
from time import sleep
import RPi.GPIO as gpio
import datetime

# Experimental ------------------------------------
#import boto3

#AWS_ACCESS_KEY = 'INSERT_AWS_ACCESS_KEY'
#AWS_SECRET_ACCESS = 'INSERT_AWS_SECRET_ACCESS'
#TOPIC_ARN = 'INSERT_TOPIC_ARN' # should similar with this arn:aws:sns:us-east-1:1234567890:door-status
# --------------------------------------------------

gpio.setmode(gpio.BCM)

# Connecting push button to GPIO Pin 18
gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_UP)

# Initializes the Pi Camera and sets it for night time photos
camera = PiCamera(resolution = (1280, 720),
		  framerate = Fraction(1, 6),
		  sensor_mode = 3)
camera.shutter_speed = 6000000
camera.iso = 800

#Setting up email parameters
toAddr = 'iotdoorbell@outlook.com'
fromAddr = 'iotdoorbell@outlook.com'
subject = 'Doorbell pressed, someone is at the door'

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
		
		# Experimental ---------------------------------------
		#snsClient = boto3.client(
            	#'sns',
            	#aws_access_key_id = AWS_ACCESS_KEY,
            	#aws_secret_access_key = AWS_SECRET_ACCESS,
            	#region_name = 'us-east-2'
        	#)
		
		#message = "Someone is at the door" 
                #print (message)
                #publish(snsClient, message)
		# -----------------------------------------------------
