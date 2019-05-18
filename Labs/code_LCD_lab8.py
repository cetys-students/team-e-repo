import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Input variables
RS = 13
RW = 6
E = 19

control_pins = [5, 0, 11, 9, 10, 22, 27, 17]

D0 = 17
D1 = 27
D2 = 22
D3 = 10
D4 = 9
D5 = 11
D6 = 0
D7 = 5

# Initialization ascii codes
init1 = [0, 0, 1, 1, 1, 0, 0, 0]
init2 = [0, 0, 0, 0, 1, 1, 0, 0]
init3 = [0, 0, 0, 0, 0, 1, 1, 0]

one = [0, 0, 0, 0, 0, 0, 0, 1]

dos_cincocinco = [1, 1, 1, 1, 1, 1, 1, 1]

esp = [0, 0, 1, 0, 0, 0, 0, 0]

# GPIO Pins initialization
GPIO.setup(RS, GPIO.OUT)
GPIO.setup(RW, GPIO.OUT)
GPIO.setup(E, GPIO.OUT)
GPIO.setup(D0, GPIO.OUT)
GPIO.setup(D1, GPIO.OUT)
GPIO.setup(D2, GPIO.OUT)
GPIO.setup(D3, GPIO.OUT)
GPIO.setup(D4, GPIO.OUT)
GPIO.setup(D5, GPIO.OUT)
GPIO.setup(D6, GPIO.OUT)
GPIO.setup(D7, GPIO.OUT)

def send_to_lcd(binary):
    for pin in range(0, 8):
        GPIO.output(control_pins[pin], binary[pin])

def convert_to_ascii(number):
    num = ord(str(number))
    ascii = format(num, '08b')
    ascii_array = [int(ascii[0]), int(ascii[1]), int(ascii[2]), int(ascii[3]), int(ascii[4]), int(ascii[5]), int(ascii[6]), int(ascii[7])]
    send_to_lcd(ascii_array)

def write_text(text):
        for x in range (0,len(text)):
            GPIO.output(RS, 1)
            convert_to_ascii(text[x])
            GPIO.output(E, 1)
            GPIO.output(E, 0)
            pass

def write_character(letra):
    GPIO.output(RS, 1)
    convert_to_ascii(letra)
    GPIO.output(E, 1)
    GPIO.output(E, 0)
    wait_lcd()

def init_lcd():
    # First Instruction
    GPIO.output(RS, 0)
    send_to_lcd(init1)
    GPIO.output(E, 1)
    GPIO.output(E, 0)
    time.sleep(0.009)
    # Second Instruction
    GPIO.output(RS, 0)
    send_to_lcd(init2)
    GPIO.output(E, 1)
    GPIO.output(E, 0)
    time.sleep(0.009)
    # Third Instruction
    GPIO.output(RS, 0)
    send_to_lcd(init3)
    GPIO.output(E, 1)
    GPIO.output(E, 0)
    time.sleep(0.009)

def clear_lcd():
    GPIO.output(RS, 0)
    send_to_lcd(one)
    GPIO.output(E, 1)
    GPIO.output(E, 0)

def wait_lcd():
    cicle = True
    time.sleep(0.009)

def first_line():
    GPIO.output(RS, 0)
    GPIO.output(D0, 0)
    GPIO.output(D1, 0)
    GPIO.output(D2, 0)
    GPIO.output(D3, 0)
    GPIO.output(D4, 0)
    GPIO.output(D5, 0)
    GPIO.output(D6, 0)
    GPIO.output(D7, 1)
    GPIO.output(E, 1)
    GPIO.output(E, 0)
    

init_lcd()
clear_lcd()