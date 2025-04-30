import RPi.GPIO as GPIO
import time

in1 = 5

GPIO.setmode( GPIO.BCM )
GPIO.setup(in1, GPIO.IN)

while True:
    if GPIO.input(in1) == GPIO.HIGH:
        print("Pin in1 is HIGH")
        break
    time.sleep(0.1)
