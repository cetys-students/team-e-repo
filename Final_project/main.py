from AltIMU_v5 import AltIMUv5
#import Adafruit_ADS1x15
import time
import math
from math import sqrt, fabs
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button_pin = 23
button_motor4 = 10
sampling_period = 0.1

motor1_pin1 = 24
motor1_pin2 = 25
motor2_pin1 = 13
motor2_pin2 = 16
motor3_pin1 = 17
motor3_pin2 = 4
motor4_pin1 = 11
motor4_pin2 = 9

GPIO.setup(button_pin, GPIO.IN)    #Button calibrate
GPIO.setup(button_motor4, GPIO.IN)
GPIO.setup(motor1_pin1, GPIO.OUT)
GPIO.setup(motor1_pin2, GPIO.OUT)
GPIO.setup(motor2_pin1, GPIO.OUT)
GPIO.setup(motor2_pin2, GPIO.OUT)
GPIO.setup(motor3_pin1, GPIO.OUT)
GPIO.setup(motor3_pin2, GPIO.OUT)
GPIO.setup(motor4_pin1, GPIO.OUT)
GPIO.setup(motor4_pin2, GPIO.OUT)


altimu = AltIMUv5()
altimu.enable()

angle = 0
sample_1 = 0
sample_2 = 0
bias=0

cont = 0

flag = False

print("Positionate the sensor")

while True:
    if GPIO.input(button_pin) == 1:
        print("Button pressed")
        flag = True
    if flag == True:
        if cont <= 100:
            cal = altimu.get_gyroscope_cal()
            time.sleep(sampling_period)
            bias += cal[2]
            cont = cont + 1
            print("Calibrating")
        else:
            if cont == 101:
                bias/=100
                cont = cont + 1
                print("Calibration finished")
            
            cal = altimu.get_accelerometer_cal()
            
            cal_gyro = altimu.get_gyroscope_cal()
            sample_1 = cal_gyro[2] - bias
            time.sleep(sampling_period)
            cal_gyro = altimu.get_gyroscope_cal()
            sample_2 = cal_gyro[2]- bias
            time.sleep(sampling_period)
            
            angle = angle + (sample_1 + sample_2)*sampling_period 
            
            textx = str("%.3f" % cal[0])
            texty = str("%.3f" % cal[1])
            textz = str("%.3f" % cal[2])

            if cal[1] > 0.6:
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor1_pin1,1)
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,0)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor4_pin1,0)
            elif cal[1] < -0.6:
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor1_pin2,1)
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,0)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor4_pin1,0)
            elif cal[0] > 0.6:
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor2_pin1,1)
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,0)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor4_pin1,0)
            elif cal[0] < -0.6:
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor2_pin2,1)
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,0)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor4_pin1,0)
            elif angle > 45:
                GPIO.output(motor3_pin1,0)
                GPIO.output(motor3_pin2,1)
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor4_pin1,0)
            elif angle <-45:
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,1)
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor4_pin1,0)
            elif GPIO.input(button_motor4)==1:
                GPIO.output(motor4_pin1, 1)
                GPIO.output(motor4_pin2,0)
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,0)
            else:
                GPIO.output(motor1_pin1,0)
                GPIO.output(motor1_pin2,0)
                GPIO.output(motor2_pin1,0)
                GPIO.output(motor2_pin2,0)
                GPIO.output(motor3_pin2,0)
                GPIO.output(motor3_pin1,0)
                GPIO.output(motor4_pin1,0)
                GPIO.output(motor4_pin2,1)
            
            if GPIO.input(button_pin)==1:
                angle=0
                print("Position reseted")
            print(angle)
