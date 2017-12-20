#!/usr/bin/python3

import RPi.GPIO as GPIO
import sys
import time
import datetime
import os
import picamera
import configparser
from catmailer import mailphoto

def main():
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
        print("config file parsed")
    else:
        MAILFROMADDRESS = sys.argv[1]
        MAILFROMPASS = sys.argv[2]
        MAILTOADDRESS = sys.argv[3]
    
    BASEDIR = "/opt/catcam/"
    GPIO.setmode(GPIO.BOARD)
    GPIO_PIR = 12
    GPIO.setup(GPIO_PIR,GPIO.IN)
    
    laststate = 0
    camera = picamera.PiCamera()
    #camera.led = False
    #camera.hflip = True
    #camera.vflip = True
    
    try:
        #set camera resolution and delay to custom settings in config file
        camera.resolution = (config['Picture']['Width'], config['Picture']['Height'])
        delayduration = config['Picture']['Delay']
    except:
        #no resolution/delay found in config.ini or settings are corrupt
        camera.resolution = ( 640, 480 )
        delayduration = 0.3
    
    def takephoto():
        camera.annotate_foreground = picamera.Color('black')
        camera.annotate_background = picamera.Color('white')
        camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    
        filename = BASEDIR + "images/" + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".jpg"
        time.sleep(0.3)
        camera.capture(filename)
        mailphoto(MAILFROMADDRESS,MAILFROMPASS,MAILTOADDRESS,filename)
    
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

if __name__ == "__main__":
    main()