"""
Ultrasonic
"""

import time
import numpy as np
import RPi.GPIO as GPIO

class Ultrasonic():
    def __init__(self, gpio_trigger = 18, gpio_echo = 17, poll_delay=1, name=''):
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.poll_delay = poll_delay
        self.name = name
		
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

        self.distance = 0.0

        self.on = True

    def update(self):
        while self.on:
            self.distance = self.poll_distance()
            time.sleep(self.poll_delay)
            
    def run_threaded(self):
        return self.distance
		
    def run(self):
        self.distance = self.poll_distance()
        return self.distance

    def shutdown(self):
        print('Shutdown ultrasonic', self.name)
        self.on = False
        GPIO.cleanup()
        time.sleep(1)

    def poll_distance(self):

        # set Trigger to HIGH
        GPIO.output(self.gpio_trigger, True)
		
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)
		
        StartTime = time.time()
        StopTime = time.time()
		
        # save StartTime
        timeout = time.time() + 0.1
        while GPIO.input(self.gpio_echo) == 0:
            StartTime = time.time()
            if StartTime > timeout:
               break


        # save time of arrival
        timeout = time.time() + 0.1
        while GPIO.input(self.gpio_echo) == 1:
            StopTime = time.time()
            if StopTime > timeout:
               break
			
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance

class MockUltrasonic():
    def __init__(self, gpio_trigger = 12, gpio_echo = 16, poll_delay=1, name=''):
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.poll_delay = poll_delay
        self.name = name
        self.distance = 0.0
        self.on = True

    def update(self):
        while self.on:
            self.distance = self.poll_distance()
            time.sleep(self.poll_delay)
            
    def run_threaded(self):
        return self.distance
		
    def run(self):
        self.distance = self.poll_distance()
        return self.distance

    def shutdown(self):
        print('Shutdown ultrasonic', self.name)
        self.on = False
        time.sleep(1)
		
    def poll_distance(self):
        return 0.5
		
if __name__ == "__main__":
    iter = 0
    u = Ultrasonic()
    while iter < 10:
        data = u.run()
        print(data)
        time.sleep(1.0)
        iter += 1
