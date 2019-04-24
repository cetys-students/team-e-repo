import RPi.GPIO as GPIO
import time
import code_LCD as LCD

R1 = 6
R2 = 13
R3 = 19
R4 = 26
C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)
GPIO.setup(8, GPIO.IN)
GPIO.setup(7, GPIO.IN)
GPIO.setup(1, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN)
GPIO.setup(C2, GPIO.IN)
GPIO.setup(C3, GPIO.IN)
GPIO.setup(C4, GPIO.IN)

# GPIO 19 as PWM with 1000HZ frequency
p = GPIO.PWM(18, 100)
# Generate PWM signal with 0% duty cycle
p.start(0)


def read_matrix():
    GPIO.output(R1, 0)
    GPIO.output(R2, 0)
    GPIO.output(R3, 0)
    GPIO.output(R4, 1)
    if GPIO.input(C4) == 1:
        return '1'
    if GPIO.input(C3) == 1:
        return '2'
    if GPIO.input(C2) == 1:
        return '3'
    if GPIO.input(C1) == 1:
        return 'A'
    GPIO.output(R4, 0)
    GPIO.output(R2, 1)
    if GPIO.input(C4) == 1:
        return '4'
    if GPIO.input(C3) == 1:
        return '5'
    if GPIO.input(C2) == 1:
        return '6'
    if GPIO.input(C1) == 1:
        return 'B'
    GPIO.output(R2, 0)
    GPIO.output(R3, 1)
    if GPIO.input(C4) == 1:
        return '7'
    if GPIO.input(C3) == 1:
        return '8'
    if GPIO.input(C2) == 1:
        return '9'
    if GPIO.input(C1) == 1:
        return 'C'
    GPIO.output(R3, 0)
    GPIO.output(R1, 1)
    if GPIO.input(C4) == 1:
        return '*'
    if GPIO.input(C3) == 1:
        return '0'
    if GPIO.input(C2) == 1:
        return '#'
    if GPIO.input(C1) == 1:
        return 'D'
    return 'F'


def read_adc():
    # Turn on the RW of the ADC
    GPIO.output(1, GPIO.HIGH)
    # Generate a little time sleep to give time to the ADC to refresh the output
    time.sleep(0.001)
    adc_byte = 0
    if GPIO.input(14) == 1:
        adc_byte = adc_byte + 1
    if GPIO.input(15) == 1:
        adc_byte = adc_byte + 2
    if GPIO.input(3) == 1:
        adc_byte = adc_byte + 4
    if GPIO.input(23) == 1:
        adc_byte = adc_byte + 8
    if GPIO.input(24) == 1:
        adc_byte = adc_byte + 16
    if GPIO.input(25) == 1:
        adc_byte = adc_byte + 32
    if GPIO.input(8) == 1:
        adc_byte = adc_byte + 64
    if GPIO.input(7) == 1:
        adc_byte = adc_byte + 128  
    GPIO.output(1, GPIO.LOW)
    return adc_byte


unit_system_mode = 0
pwm = 0
spin_count = 0
analog_value = 0
count_flag = True
start_time = time.time()
while 1:
    analog_value = read_adc()
    if (analog_value > 110) and (analog_value < 150):
        count_flag = True
    p.start(pwm)
    if ((analog_value < 110) or (analog_value > 150)) and count_flag:
        spin_count = spin_count + 1
        count_flag = False
    pressed_key = read_matrix()
    if pressed_key == '0':
        pwm = 0
    if pressed_key == '1':
        pwm = 11
    if pressed_key == '2':
        pwm = 22
    if pressed_key == '3':
        pwm = 33
    if pressed_key == '4':
        pwm = 44
    if pressed_key == '5':
        pwm = 55
    if pressed_key == '6':
        pwm = 66
    if pressed_key == '7':
        pwm = 77
    if pressed_key == '8':
        pwm = 88
    if pressed_key == '9':
        pwm = 99
    if pressed_key == 'A':
        unit_system_mode = 0
    if pressed_key == 'B':
        unit_system_mode = 1
    if pressed_key == 'C':
        unit_system_mode = 2
    if pressed_key == 'D':
        unit_system_mode = 3
    elapsed_time = time.time() - start_time
    
    if elapsed_time > 1:
        LCD.clear_lcd()
        start_time = time.time()
        if unit_system_mode == 0:
            # Multiplied RPS*60 to get RPM
            spin_count = spin_count * 60
            LCD.write_text("RPM: ")
        if unit_system_mode == 1:
            # Multiplied RPS*60 to get RPM and divided by 60 to get Hertz
            # count = count
            LCD.write_text("HERTZ: ")
        if unit_system_mode == 2:
            # RPS equals 2pi radians, RPS was multiplied by 2pi rad to get rad/s
            spin_count = spin_count * 3.1416 * 2
            LCD.write_text("rad/s: ")
        if unit_system_mode == 3:
            # RPS equals 360 degrees, RPS was multiplied by 360 to get degrees/s
            spin_count = spin_count * 360
            LCD.write_text("deg/s: ")
        LCD.write_text(spin_count)
        spin_count = 0

    


