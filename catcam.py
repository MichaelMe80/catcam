#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import datetime
import os
import picamera
from catmailer import mailphoto

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = 12
GPIO.setup(GPIO_PIR,GPIO.IN)

USER = sys.argv[1]
PASSWORD = sys.argv[2]

laststate = 0
camera = picamera.PiCamera()
#camera.hflip = True
#camera.vflip = True
camera.resolution = (640, 480)

def takephoto():
    camera.capture('/home/pi/image.jpg')
    mailphoto(USER,PASSWORD)

while True:
    newstate = GPIO.input(GPIO_PIR)
    if newstate == 1:
        if laststate == 0:
            #new movement
            takephoto()
            laststate = 1
            print("new movement")
    elif newstate == 0:
        if laststate == 1:
            #movement over
            laststate = 0
            print("movement is over")        
    #time.sleep(0.1)

