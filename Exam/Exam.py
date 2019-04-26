from AltIMU_v5 import AltIMUv5
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


altimu = AltIMUv5()
altimu.enable()

button_pin = 26
led_pin = 19
GPIO.setup(button_pin, GPIO.IN)    # Button
GPIO.setup(led_pin, GPIO.OUT)      # LED Pin

print('Press the button')

sampling_period = 0.1
sample_x = 0
sample_y = 0
biasx = 0
biasy = 0
threshold = 40
GPIO.output(led_pin, 0)


def calibration():
    global biasx, biasy
    for x in range(0, 99):
        cal = altimu.get_gyroscope_cal()
        time.sleep(sampling_period)
        biasx += cal[0]
        biasy += cal[1]
    
    biasx /= 100    # Average bias value for the x axis
    biasy /= 100    # Average bias value for the y axis


def get_movement():
    global sample_x, sample_y, sampling_period, biasx, biasy, threshold
    while True:
            cal = altimu.get_gyroscope_cal()
            sample_x = cal[0] - biasx
            sample_y = cal[1] - biasy
            time.sleep(sampling_period)

            # Turn the LED on if the measurement surpasses the threshold
            if abs(sample_x) >= threshold or abs(sample_y) >= threshold:
                GPIO.output(led_pin, 1)
                time.sleep(1)
                GPIO.output(led_pin, 0)


#### main ####
                
while True:   
    if GPIO.input(button_pin) == 1:
        print('Calibrating')
        calibration()
        print('Ready')
        get_movement()
        
###############
