from AltIMU_v5 import AltIMUv5
import time
import RPi.GPIO as GPIO
from code_LCD_lab8 import write_text
from code_LCD_lab8 import clear_lcd
from code_LCD_lab8 import first_line
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


altimu = AltIMUv5()
altimu.enable()

button_pin = 26
GPIO.setup(button_pin, GPIO.IN)

time.sleep(0.009)
write_text('Press the button')
time.sleep(0.009)
sampling_period = 0.1
 
angle = 0
sample_1 = 0
sample_2 = 0
initial_time = 0
bias = 0


# This calibration process is used to avoid bias in some axes
def calibration():
    clear_lcd()
    time.sleep(0.009)
    write_text('Calibrating...')
    time.sleep(0.009)
    global bias
    for x in range(0, 99):
        cal = altimu.get_gyroscope_cal()
        time.sleep(sampling_period)
        bias += cal[2]
    
    bias /= 100
    clear_lcd()
    time.sleep(0.009)


def get_angle():
    global sample_1, sample_2, angle, bias, initial_time
    initial_time = time.time()
    while True:
            cal = altimu.get_gyroscope_cal()
            sample_1 = cal[2] - bias
            time.sleep(sampling_period)
            cal = altimu.get_gyroscope_cal()
            sample_2 = cal[2] - bias
            time.sleep(sampling_period)
            # Integral of the angular speed,
            # sampling_period was doubled to take
            # both samples on a single turn
            angle = angle + (sample_1 + sample_2)*sampling_period
            # Print the angular position in the LCD
            if time.time() - initial_time > .5:
                text = str("%.3f" % angle)
                first_line()
                write_text("Angle ")
                write_text(text)
                write_text("   ")
                initial_time = time.time()
            # Reset the angular position to zero
            if GPIO.input(button_pin) == 1:
                angle = 0


# _____main_____
                
while True:   
    if GPIO.input(button_pin) == 1:
        calibration()
        get_angle()
        
# ______________
