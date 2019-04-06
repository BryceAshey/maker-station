
#!/usr/bin/python3

# some of this script by Alex Eames https://raspi.tv  
# https://raspi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3  
import busio
import json
import megaio
import os
import RPi.GPIO as GPIO 
import signal

from adafruit_pca9685 import PCA9685
from array import *
from board import SCL, SDA
from phue import Bridge
from time import sleep

relay_state = [False, False, False, False, False, False, False, False, False]
spare_led = False

def flip_led(channel, flip):
    cycle = 0
    if(flip):
        cycle = 0x7fff
    pca.channels[channel].duty_cycle = cycle # https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython

def switch_hue(channel):
    print('Switching HUE %s'%channel)
    # Switch LED will be handled by hue_check_state method
    b.set_group(channel, 'on', not b.get_group(channel, 'on'))

def switch_relay(channel, relay_num):
    print('Switching USB %s'%channel)
    relay_state[relay_num] = not relay_state[relay_num]
    if(relay_state[relay_num]):
        megaio.set_relay(0, relay_num, 1)
    else:
        megaio.set_relay(0, relay_num, 0)
    flip_led(channel, relay_state[relay_num])

def gpio_button_pressed(channel):  
    print('Rising edge detected on %s'%channel)
    global spare_led
    if(channel == 5): # Top Row
        switch_hue(1)
    elif(channel == 6):
        switch_relay(1, 1)
    elif(channel == 7):
        switch_relay(2, 2)
    elif(channel == 8): # Row 2
        switch_hue(2)
    elif(channel == 9):
        switch_relay(4, 3)
    elif(channel == 10):
        switch_relay(5, 4)
    elif(channel == 11): # Row 3
        switch_hue(3)
    elif(channel == 12):
        switch_relay(7, 5)
    elif(channel == 13):
        switch_relay(8, 6)
    elif(channel == 14): # Row 4
        switch_hue(4)
    elif(channel == 15):
        switch_relay(10, 7)
    elif(channel == 16):
        switch_relay(11, 8)
    elif(channel == 17): #Bottom Row
        switch_hue(5)
    elif(channel == 18):
        switch_hue(6)
    elif(channel == 19):
        print('Spare 0')
        spare_led = not spare_led
        flip_led(14, spare_led)
        
def hue_check_state():
    try:
        hue_all_rooms = b.get_group()
        for position in range(1, len(hue_all_rooms)+1):
            hue_room = b.get_group(position, 'on')
            if(position == 1):
                flip_led(0, hue_room)
            elif(position == 2):
                flip_led(3, hue_room)
            elif(position == 3):
                flip_led(6, hue_room)
            elif(position == 4):
                flip_led(9, hue_room)
            elif(position == 5):
                flip_led(12, hue_room)
            elif(position == 6):
                flip_led(13, hue_room)

    except Exception as e:
        print(e)
        
def setup_sigterm():
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

def setup_gpio_button():
    GPIO.setmode(GPIO.BCM)
    i = 5
    while i <= 19:
        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(i, GPIO.RISING, callback=gpio_button_pressed, bouncetime=300)  
        i += 1

def setup_pca():
    global i2c_bus 
    global pca
    i2c_bus = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c_bus)
    pca.frequency = 60
        
def setup_hue():
    global b
    b = Bridge(os.environ['HUE_BRIDGE_IP'], os.environ['HUE_BRIDGE_USERNAME'])
    b.connect()
    
def init():
    setup_sigterm()
    setup_pca()
    setup_hue()
    setup_gpio_button()

def shutdown_handler(signum, frame):
    GPIO.cleanup()
    exit(0)

if __name__ == '__main__':
    try:
        init()

        # loop till the cows come home
        while True:
            hue_check_state()
            sleep(1)

    except KeyboardInterrupt:  
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    GPIO.cleanup()   