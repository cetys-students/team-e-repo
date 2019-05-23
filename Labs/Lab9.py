from AltIMU_v5 import AltIMUv5
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Declarations
altimu = AltIMUv5()
altimu.enable()

button_pin = 4
led_1 = 26
led_2 = 19
led_3 = 13
led_4 = 6
led_5 = 5

sampling_period = 0.1

relative_ang_x = 0
relative_ang_z = 0

bias_gyro_x = 0
bias_gyro_y = 0
bias_gyro_z = 0

ang_vel_x = 0
ang_vel_y = 0
ang_vel_z = 0

ang_vel_x2 = 0
ang_vel_y2 = 0
ang_vel_z2 = 0

ang_z = 0
ang_y = 0
ang_x = 0

acc_x2 = 0
acc_y2 = 0
acc_z2 = 0

acc_x = 0
acc_y = 0
acc_z = 0

GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)
GPIO.setup(led_3, GPIO.OUT)
GPIO.setup(led_4, GPIO.OUT)
GPIO.setup(led_5, GPIO.OUT)

GPIO.output(led_1, 0)
GPIO.output(led_2, 0)
GPIO.output(led_3, 0)
GPIO.output(led_4, 0)
GPIO.output(led_5, 0)

flagSteps = 0


# This function is used to eliminate the bias in the gyroscope
def calibration():
    print('Calibrating...')
    global bias_gyro_x, bias_gyro_y, bias_gyro_z
            
    for x in range(0, 99):
        cal_gyro = altimu.get_gyroscope_cal()
        time.sleep(sampling_period)
        
        bias_gyro_x += cal_gyro[0]
        bias_gyro_y += cal_gyro[1]
        bias_gyro_z += cal_gyro[2]
    
    bias_gyro_x /= 100
    bias_gyro_y /= 100
    bias_gyro_z /= 100


# This function is used to calculate the integral of the gyroscope velocity
# Also it is used to ser the previous and actual accelerometer values
def get_sample():
    global bias_gyro_x, bias_gyro_y, bias_gyro_z, acc_x2, acc_y2, acc_z2
    global ang_vel_x, ang_vel_y, ang_vel_z, ang_vel_x2, ang_vel_y2, ang_vel_z2
    global ang_z, ang_y, ang_x, acc_x, acc_y, acc_z

    acc_x2 = acc_x
    acc_y2 = acc_y
    acc_z2 = acc_z
    
    cal_gyro = altimu.get_gyroscope_cal()
    cal_acc = altimu.get_accelerometer_cal()
    ang_vel_x = cal_gyro[0] - bias_gyro_x
    ang_vel_y = cal_gyro[1] - bias_gyro_y
    ang_vel_z = cal_gyro[2] - bias_gyro_z
    acc_x = cal_acc[0]
    acc_y = cal_acc[1]
    acc_z = cal_acc[2]
    time.sleep(sampling_period)

    ang_z = ang_z + (ang_vel_z + ang_vel_z2) * sampling_period * 0.5
    ang_x = ang_x + (ang_vel_x + ang_vel_x2) * sampling_period * 0.5
    ang_y = ang_y + (ang_vel_y + ang_vel_y2) * sampling_period * 0.5
            
    ang_vel_x2 = ang_vel_x
    ang_vel_y2 = ang_vel_y
    ang_vel_z2 = ang_vel_z
    

#   main  #
print('Press the button')
while GPIO.input(button_pin) == 0:
    pass
calibration()
print("Ready")
initial_time = time.time()

while True:   
        get_sample()
        # Valid action 1, angle z needs to be located at -80 degrees
        if (ang_z < -80) and flagSteps == 0:
            GPIO.output(led_1, 1)
            flagSteps += 1
            relative_ang_x = ang_x
            initial_time = time.time()
        # Valid action 2, angle x needs to be moved at -80 degrees with respect to the previous action
        if ((ang_x - relative_ang_x) < -80) and flagSteps == 1:
            GPIO.output(led_2, 1)
            flagSteps += 1
            relative_ang_z = ang_z
            initial_time = time.time()
        # Valid action 3, angle z needs to be moved at 80 degrees with respect to the previous action
        if ((ang_z - relative_ang_z) > 80) and flagSteps == 2:
            GPIO.output(led_3, 1)
            flagSteps += 1
            initial_time = time.time()
        # Valid action 4, the acceleration difference between 2 recorded values needs to be higher to 1G
        if (acc_x - acc_x2) > 1 and flagSteps == 3:
            GPIO.output(led_4, 1)
            time.sleep(3)
        # This if resets the gyroscope positions, the LED's and blinks a LED indicating the action was performed
        # Only if the elapsed time without a valid action goes beyond 3 seconds
        if (time.time() - initial_time) > 3:
            GPIO.output(led_5, 1)
            flagSteps = 0
            ang_x = 0
            ang_y = 0
            ang_z = 0
            GPIO.output(led_1, 0)
            GPIO.output(led_2, 0)
            GPIO.output(led_3, 0)
            GPIO.output(led_4, 0)
            time.sleep(0.1)
            GPIO.output(led_5, 0)
            initial_time = time.time()
        
###############
