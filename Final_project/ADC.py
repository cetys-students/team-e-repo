import time
import Adafruit_ADS1x15

import math
from math import sqrt, fabs
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

flagState = False

motor0_pin1 = 24
motor0_pin2 = 25
motor2_pin1 = 13
motor2_pin2 = 16
motor3_pin1 = 17
motor3_pin2 = 4
motor4_pin1 = 11
motor4_pin2 = 9


motor1_pin1 = 17
motor1_pin2 = 4


GPIO.setup(motor1_pin1, GPIO.OUT)
GPIO.setup(motor1_pin2, GPIO.OUT)
GPIO.setup(motor0_pin1, GPIO.OUT)
GPIO.setup(motor0_pin2, GPIO.OUT)
GPIO.setup(motor2_pin1, GPIO.OUT)
GPIO.setup(motor2_pin2, GPIO.OUT)
GPIO.setup(motor3_pin1, GPIO.OUT)
GPIO.setup(motor3_pin2, GPIO.OUT)
GPIO.setup(motor4_pin1, GPIO.OUT)
GPIO.setup(motor4_pin2, GPIO.OUT)

GPIO.output(motor0_pin1,0)
GPIO.output(motor0_pin2,0)
GPIO.output(motor1_pin1,0)
GPIO.output(motor1_pin2,0)
GPIO.output(motor2_pin1,0)
GPIO.output(motor2_pin2,0)
GPIO.output(motor3_pin1,0)
GPIO.output(motor3_pin2,0)
GPIO.output(motor4_pin1,0)
GPIO.output(motor4_pin2,0)
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 16

samples = 0

for i in range(0, 100):
    samples += adc.read_adc(0,gain=GAIN)

prom = samples/100

open_counter = 0
close_counter = 0

while True:
    values = 0
    for x in range(0, 40):
        values = values + adc.read_adc(0,gain=GAIN)
    values/=40
    dif = abs(values - prom)
    print('Average', prom, '   Current ', values, '    Dif', dif)
    if dif > 15:
        close_counter = close_counter + 1
        open_counter = 0
    else:
        open_counter = open_counter + 1
        close_counter = 0
        
    if open_counter >= 3:
        print('Open')
        if not flagState:
            GPIO.output(motor4_pin1,0)
            GPIO.output(motor4_pin2,0)
        else:
            GPIO.output(motor4_pin1,0)
            GPIO.output(motor4_pin2,1)
            flagState=False
        open_counter = 0
        close_counter = 0
    if close_counter >= 3:
        print('Close')
        if flagState:
            GPIO.output(motor4_pin2,0)
            GPIO.output(motor4_pin1,0)
        else:
            GPIO.output(motor4_pin2,0)
            GPIO.output(motor4_pin1,1)
            flagState=True
        open_counter = 0
        close_counter = 0
