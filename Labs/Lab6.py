import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor

GPIO.setmode(GPIO.BCM)

# Set for the steps
control_pins = [14, 15, 18, 23]

for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

fullstep_seq_right = [[1, 1, 0, 0],
                      [0, 1, 1, 0],
                      [0, 0, 1, 1],
                      [1, 0, 0, 1]]

fullstep_seq_left = [[1, 0, 0, 1],
                     [0, 0, 1, 1],
                     [0, 1, 1, 0],
                     [1, 1, 0, 0]]

# Sensor configuration
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5)
ultrasonic.max_distance = 1

# Variables

# This means the number of full step sequences done to rotate 360 degrees
number_of_sequences = 512
matrix_x_position = 4
matrix_y_position = 4
# This means the sleep time for each step
sleep_time_step = 0.002

# Steps creation
def closest_object_step_finder()-> 'int':
    # Initial step is 0 and the final one is 2048 according to the data-sheet
    step = 0
    # Set to a high number supposing the initial closest object distance is infinite
    closest_object_distance = 100.0
    for i in range(number_of_sequences):
        for y_position in range(matrix_y_position):
            for x_position in range(matrix_x_position):
                GPIO.output(control_pins[x_position], fullstep_seq_right[y_position][x_position])
                # Multiplied by 100 to get cm
                cm_distance = ultrasonic.distance*100
                if cm_distance < closest_object_distance:
                    closest_object_distance = cm_distance
                step = i
                time.sleep(sleep_time_step)
    return step


def closest_object_pointer(closest_object_step: 'int'):
    for i in range(closest_object_step):
        for y_position in range(matrix_y_position):
            for x_position in range(matrix_x_position):
                GPIO.output(control_pins[x_position], fullstep_seq_left[y_position][x_position])
                time.sleep(sleep_time_step)


# Main Program

object_step = closest_object_step_finder()
# 512 minus the object step to find the position going backwards to avoid cable mixes
object_step_backwards = 512 - object_step
print("Position of the object going backwards: ", object_step_backwards)
closest_object_pointer(object_step_backwards)



