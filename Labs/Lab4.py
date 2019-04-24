import RPi.GPIO as GPIO
import time
import code_LCD

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

PIR_in = 20
PIR_out = 16

# PIR input and output
GPIO.setup(PIR_in, GPIO.IN)
GPIO.setup(PIR_out, GPIO.OUT)

# LED's array
LEDs = [12, 1, 7, 8, 25, 24, 23, 18, 15, 14]
for pin in range(0, 10):
	GPIO.setup(LEDs[pin], GPIO.OUT)


def write_people():
	code_LCD.write_text('P')
	code_LCD.write_text('E')
	code_LCD.write_text('O')
	code_LCD.write_text('P')
	code_LCD.write_text('L')
	code_LCD.write_text('E')
	code_LCD.write_text(':')


def update_digits(num):
	code_LCD.clear_lcd()
	write_people()
	if num < 10:
		code_LCD.write_text(num)
	else:
		num = [int(d) for d in str(num)]
		for digits in num:
			code_LCD.write_text(digits)


count_reps = 0
count_leds = 0

write_people()
code_LCD.write_text(count_reps)

while 1:
	GPIO.output(PIR_out, GPIO.input(PIR_in))
	if GPIO.input(PIR_in) == 1:
		count_reps = count_reps+1
		update_digits(count_reps)
		start_time = time.time()
		while GPIO.input(PIR_in) == 1:
			GPIO.output(PIR_out, GPIO.input(PIR_in))
			elapsed_time = time.time()-start_time
			if elapsed_time >= 5:
				GPIO.output(LEDs[count_leds], 1)
				if count_leds <= 8:
					count_leds = count_leds + 1
				start_time = time.time()
	for pin in range(0, 10):
		GPIO.output(LEDs[pin], 0)
		count_leds = 0


