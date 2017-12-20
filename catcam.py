#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import datetime
import os
import picamera
import configparser
from catmailer import mailphoto

#checking argv
if len(sys.argv) != 4:
    print("No args given, trying to use config file")
    try:
        config = configparser.ConfigParser()
        config.read('/opt/catcam/config.ini')
        MAILFROMADDRESS = config['Mail']['MailFromAddress']
        MAILFROMPASS = config['Mail']['MailFromPass']
        MAILTOADDRESS = config['Mail']['MailToAddress']
    except:
        sys.exit("couldn't read input file")
else:
    MAILFROMADDRESS = sys.argv[1]
    MAILFROMPASS = sys.argv[2]
    MAILTOADDRESS = sys.argv[3]

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = 12
GPIO.setup(GPIO_PIR,GPIO.IN)

laststate = 0
camera = picamera.PiCamera()
camera.led = False
#camera.hflip = True
#camera.vflip = True
camera.resolution = (640, 480)

def takephoto():
    camera.annotate_foreground = Color('black')
    camera.annotate_background = Color('white')
    camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');

    camera.capture('/home/pi/image.jpg')
    mailphoto(MAILFROMADDRESS,MAILFROMPASS,MAILTOADDRESS)

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

