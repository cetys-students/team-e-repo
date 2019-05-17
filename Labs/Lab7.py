from AltIMU_v5 import AltIMUv5
import time
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led1_pin = 19
led2_pin = 26
button_pin = 4

GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)


altimu = AltIMUv5()
altimu.enable()

max_pos_x = 0
max_pos_y = 0
max_pos_z = 0

min_pos_x = 100
min_pos_y = 100
min_pos_z = 100

avg_x = 0
avg_y = 0
avg_z = 0

start_time = time.time()

last_pos_x = 0
last_pos_y = 0
last_pos_z = 0

bool_z = False
bool_x = False
bool_y = False

cont = 0

flag = False

while True:
    if GPIO.input(button_pin) == 1:
        flag = True
    if flag:
        if cont <= 100:
            accel = altimu.get_accelerometer_raw()
            cal = altimu.get_accelerometer_cal()
            avg_x = avg_x + cal[0]
            avg_y = avg_y + cal[1]
            avg_z = avg_z + cal[2]
            cont = cont + 1
        else:
            if cont == 101:
                avg_x = avg_x / 100
                avg_z = avg_z / 100
                avg_y = avg_y / 100
            
                max_pos_x = avg_x + 0.0999
                min_pos_x = avg_x - 0.0999
                
                max_pos_y = avg_y + 0.0999
                min_pos_y = avg_y - 0.0999
                
                max_pos_z = avg_z + 0.0999
                min_pos_z = avg_z - 0.0999

                cont = cont + 1
            
            accel = altimu.get_accelerometer_raw()
            cal = altimu.get_accelerometer_cal()

            x_difference = math.fabs(last_pos_x - cal[0])
            y_difference = math.fabs(last_pos_y - cal[1])
            z_difference = math.fabs(last_pos_z - cal[2])

            # If the differences are higher than 0.0999, it means an external acceleration is detected
            if x_difference <= 0.0999 and y_difference <= 0.0999 and z_difference <= 0.0999:
                GPIO.output(led2_pin, GPIO.HIGH)
                if max_pos_x > cal[0] > min_pos_x:
                    bool_x = True
                if max_pos_y > cal[1] > min_pos_y:
                    bool_y = True
                if max_pos_z > cal[2] > min_pos_z:
                    bool_z = True
                # If all the axes are between the max and min position, it means the altimu is in the desired position
                if bool_z and bool_y and bool_x:
                    GPIO.output(led1_pin, GPIO.HIGH)
                else:
                    GPIO.output(led1_pin, GPIO.LOW)
            else:
                GPIO.output(led1_pin, GPIO.LOW)
                GPIO.output(led2_pin, GPIO.LOW)
            
            bool_z = False
            bool_x = False
            bool_y = False
            
            if (time.time() - start_time) > 0.9:
                last_pos_x = cal[0]
                last_pos_y = cal[1]
                last_pos_z = cal[2]
                start_time = time.time()

