from PyQt6.QtCore import QObject
import RPi.GPIO as GPIO
import time

class Nozzle(QObject):
    
    step_sleep = 0.001
    step_count = 4096  # 5.625*(1/64) per step, 4096 steps is 360°
    direction = 1  # 1 for clockwise, -1 for counter-clockwise
    
    # pins will be changed for hat input
    in1 = 17
    in2 = 18
    in3 = 27
    in4 = 22
    
    def __init__(self):

        # setting up
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        
        # initializing
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        
        self.step_sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]
        self.motor_pins = [self.in1, self.in2, self.in3, self.in4]
        self.position = 0
        
        self.upper_limit = 1012
        self.lower_limit = -1012
        
    def clockwise(self):
        if self.position >= (self.upper_limit):
            print("Motor is at limit, cannot rotate further.")
            return
        self.direction = 1
        self.rotate()
    
    def counter_clockwise(self):
        if self.position <= (self.lower_limit):
            print("Motor is at limit, cannot rotate further.")
            return
        self.direction = -1
        self.rotate()
        
    def rotate(self):
        
        
        step_check = 0
        for step in range(8):
            for pin in range(0, len(self.motor_pins)):
                GPIO.output(self.motor_pins[pin], self.step_sequence[step_check][pin])
            
            step_check = (step_check + self.direction) % 8
            time.sleep(self.step_sleep)
            self.position += self.direction
        
        
        
    def move_to(self, position):
        
        steps_to_move = abs(position - self.position)
        
        if position > self.position:
            self.direction = 1
        else:
            self.direction = -1
            
        for _ in range(steps_to_move):
            self.rotate()
            time.sleep(self.step_sleep)
            
        self.stop()
        
        
        
    def stop(self):
        GPIO.output(self.motor_pins[0], GPIO.LOW)
        GPIO.output(self.motor_pins[1], GPIO.LOW)
        GPIO.output(self.motor_pins[2], GPIO.LOW)
        GPIO.output(self.motor_pins[3], GPIO.LOW)
        
    def cleanup(self):
        GPIO.output(self.motor_pins[0], GPIO.LOW)
        GPIO.output(self.motor_pins[1], GPIO.LOW)
        GPIO.output(self.motor_pins[2], GPIO.LOW)
        GPIO.output(self.motor_pins[3], GPIO.LOW)
        GPIO.cleanup()
        
    
    