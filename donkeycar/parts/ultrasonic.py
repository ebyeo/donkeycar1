"""
Ultrasonic
"""

import time
import numpy as np
import RPi.GPIO as GPIO
import sys

ULTRASONIC_DEFAULT_DISTANCE = 800.00
ULTRASONIC_RETRY = 3
ULTRASONIC_MEAN_LENGTH = 3
ULTRASONIC_TIMEOUT = 0.05

MOCKULTRASONIC_DEFAULT_DISTANCE = 800.0
CACHEULTRASONICCLIENT_DEFAULT_DISTANCE = 800.0

class Ultrasonic():
    def __init__(self, gpio_trigger=23, gpio_echo=27, poll_delay=1, name=''):

        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.poll_delay = poll_delay
        self.name = name

        #self.gpio_trigger = int(sys.argv[1])
        #self.gpio_echo = int(sys.argv[2])
        #self.poll_delay = int(sys.argv[3])
        #self.name = sys.argv[4]
		
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

        self.distance = 0.0
        self.distance_array = []
        for i in range(1, ULTRASONIC_MEAN_LENGTH):
           self.distance_array = self.distance_array + [0] 

        self.on = True

        self.getid(self.gpio_trigger, self.gpio_echo)

    def getid(self, gpio_trigger, gpio_echo):
        if (gpio_trigger==18 and gpio_echo==17):
            self.id = 1
        elif (gpio_trigger==23 and gpio_echo==27):
            self.id = 2
        elif (gpio_trigger==24 and gpio_echo==22):
            self.id = 3
        elif (gpio_trigger==25 and gpio_echo==5):
            self.id = 4
        elif (gpio_trigger==12 and gpio_echo==6):
            self.id = 5
        elif (gpio_trigger==16 and gpio_echo==13):
            self.id = 6
        elif (gpio_trigger==20 and gpio_echo==19):
            self.id = 7
        elif (gpio_trigger==21 and gpio_echo==26):
            self.id = 8
        else:
            self.id = 0
            print(self.name, ": Unknown trigger", gpio_trigger, "or echo", gpio_echo)

    def update(self):
        while self.on:
            self.distance = self.poll_distance_with_smoothing()
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
        GPIO.cleanup()

    def poll_distance(self):

        if GPIO.input(self.gpio_echo) == 1:
            return ULTRASONIC_DEFAULT_DISTANCE

        distance = 0

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
            if StartTime - StopTime > ULTRASONIC_TIMEOUT:
               distance = ULTRASONIC_DEFAULT_DISTANCE
               break

        if distance == ULTRASONIC_DEFAULT_DISTANCE:
            return (ULTRASONIC_DEFAULT_DISTANCE)

        # save time of arrival
        StopTime = StartTime
        while GPIO.input(self.gpio_echo) == 1:
            StopTime = time.time()
            if StopTime - StartTime > ULTRASONIC_TIMEOUT:
               distance = ULTRASONIC_DEFAULT_DISTANCE
               break

        if distance == ULTRASONIC_DEFAULT_DISTANCE:
            return (ULTRASONIC_DEFAULT_DISTANCE)

        # Convert the timer values into centimetres
        distance = (StopTime - StartTime) * 34300 / 2

        return distance

    def poll_distance_with_retry(self):
        retry = 0
        distance = self.poll_distance()
        while distance == ULTRASONIC_DEFAULT_DISTANCE:
            distance = self.poll_distance()
            retry = retry + 1
            if retry == ULTRASONIC_RETRY:
                retry = 0
                break

        return distance
            
    def poll_distance_with_smoothing(self):
        distance = self.poll_distance()

        self.distance_array = self.distance_array[1:] + [distance]

        return np.mean(self.distance_array)

class MockUltrasonic():
    def __init__(self, gpio_trigger = 12, gpio_echo = 16, poll_delay=1, name=''):
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.poll_delay = poll_delay
        self.name = name
        self.distance = MOCKULTRASONIC_DEFAULT_DISTANCE
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
        print('Shutdown mock ultrasonic', self.name)
        self.on = False
        time.sleep(1)
		
    def poll_distance(self):
        return MOCKULTRASONIC_DEFAULT_DISTANCE
		
class CacheUltrasonicServer(Ultrasonic):
    def __init__(self, gpio_trigger=23, gpio_echo=27, poll_delay=1, name=''):

        super().__init__(self, gpio_trigger=gpio_trigger, gpio_echo=gpio_echo, poll_delay=poll_delay, name=name)
		
        from pymemcache.client import base
        client = base.Client(('localhost', 11211))

    def update(self):
        while self.on:
            self.distance = self.poll_distance_with_smoothing()
            client.set('ultrasonic_' + self.name, self.distance)
            time.sleep(self.poll_delay)
            
    def run(self):
        self.distance = self.poll_distance()
        client.set('ultrasonic_' + self.name, self.distance)
        return self.distance

    def shutdown(self):
        super().shutdown()
        client.close()

# to be called in the donkeycar loop
class CacheUltrasonicClient():
    def __init__(self, gpio_trigger = 12, gpio_echo = 16, poll_delay=1, name=''):
        from pymemcache.client import base
        client = base.Client(('localhost', 11211))

        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        self.poll_delay = poll_delay
        self.name = name
        self.distance = CACHEULTRASONICCLIENT_DEFAULT_DISTANCE
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
        print('Shutdown cache ultrasonic client', self.name)
        self.on = False
        time.sleep(1)
		
    def poll_distance(self):
        distance = client.get('ultrasonic_' + self.name)
        if not distance:
		    distance = CACHEULTRASONICCLIENT_DEFAULT_DISTANCE
			
        return distance

if __name__ == "__main__":

    from sys import argv
    args = argv
    if (len(args) != 3):
        print("Enter trigger and echo pin number as arguments, eg python ultrasonic.py 23 27")
        exit(1)

    iter = 0
    u = CacheUltrasonicServer(gpio_trigger=int(args[1]), gpio_echo=int(args[2]))
    while iter < 1000:
        data = u.run()
        print('ultrasonic: ', data)
        time.sleep(1/20)
        iter += 1
