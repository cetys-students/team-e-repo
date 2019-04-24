import RPi.GPIO as GPIO
import time

# GPIO configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(10, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(0, GPIO.IN)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

# GPIO 19 as PWM with 1000HZ frequency
motor_pwm = GPIO.PWM(19, 100)
# generate a PWM signal with 0% duty cycle
motor_pwm.start(0)

adc_byte = 2
buzzer_sleep_time = 0
while 1:
	# Change duty cycle for generating the buzzer sound
	# Sleep for 100 ms
	motor_pwm.ChangeDutyCycle(70)
	time.sleep(buzzer_sleep_time)
	motor_pwm.ChangeDutyCycle(0)
	time.sleep(buzzer_sleep_time)

	adc_byte = 0
	# Turn on the ADC RW pin to get the samples
	GPIO.output(26, GPIO.HIGH)
	if GPIO.input(4) == 1:
		adc_byte = adc_byte + 1
	if GPIO.input(17) == 1:
		adc_byte = adc_byte + 2
	if GPIO.input(27) == 1:
		adc_byte = adc_byte + 4
	if GPIO.input(22) == 1:
		adc_byte = adc_byte + 8
	if GPIO.input(10) == 1:
		adc_byte = adc_byte + 16
	if GPIO.input(9) == 1:
		adc_byte = adc_byte + 32
	if GPIO.input(11) == 1:
		adc_byte = adc_byte + 64
	if GPIO.input(0) == 1:
		adc_byte = adc_byte + 128
	GPIO.output(26, GPIO.LOW)

	if adc_byte < 10:
		buzzer_sleep_time = 1
	elif adc_byte < 15:
		buzzer_sleep_time = 0.5
	elif adc_byte < 20:
		buzzer_sleep_time = 0.25
	elif adc_byte < 25:
		buzzer_sleep_time = 0.15
	elif adc_byte < 30:
		buzzer_sleep_time = 0.10
	elif adc_byte < 35:
		buzzer_sleep_time = 0.05
