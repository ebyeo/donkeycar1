"""
Ultrasonic
"""

import time
import numpy as np


class Ultrasonic():
    def __init__(self, gpio_trigger = 18, gpio_echo = 24, poll_delay=1):
        import RPi.GPIO as GPIO
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
		
		self.poll_delay = poll_delay
		
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)
		
        self.on = True

    def update(self):
        while self.on:
            self.distance = distance()
            time.sleep(self.poll_delay)
            
    def run_threaded(self):
        return self.distance
		
    def run(self):
        self.distance = distance()
        return self.distance

    def shutdown(self):
        self.on = False
		GPIO.cleanup()

    def distance():
        # set Trigger to HIGH
        GPIO.output(self.gpio_trigger, True)
		
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)
		
        StartTime = time.time()
        StopTime = time.time()
		
        # save StartTime
        while GPIO.input(self.gpio_echo) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.gpio_echo) == 1:
            StopTime = time.time()
			
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		distance = (TimeElapsed * 34300) / 2
		
		return distance
		
if __name__ == "__main__":
    iter = 0
    u = Ultrasonic()
    while iter < 100:
        data = p.run()
        print(data)
        time.sleep(1.0)
        iter += 1