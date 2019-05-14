from picamera import PiCamera
from time import sleep
import RPi.GPIO as gpio
import datetime

gpio.setmode(gpio.BCM)

# Connecting push button to GPIO Pin 18
gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_UP)

# Initializes the Pi Camera and sets Exposure Mode
camera= PiCamera()
camera.exposure_mode = 'antishake'
	
while True:
	
	# Obtains the value from button press
	inputCamera = gpio.input(18)

	# When pressed, it saves the current date and time as the file name
	if inputCamera == False:
		print('Camera Button Pressed')
		camera.capture('/home/pi/Documents/' +  datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S') + '.png')
		sleep(.2)
