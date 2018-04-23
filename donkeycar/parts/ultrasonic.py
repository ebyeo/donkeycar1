"""
Ultrasonic
"""

import time
import numpy as np
import RPi.GPIO as GPIO
import sys

ULTRASONIC_DEFAULT_DISTANCE = 800.00
ULTRASONIC_RETRY = 3
ULTRASONIC_MEAN_LENGTH = 5
#ULTRASONIC_TIMEOUT = 0.05
ULTRASONIC_TIMEOUT = 0.1

MOCKULTRASONIC_DEFAULT_DISTANCE = 800.0
CACHEULTRASONICCLIENT_DEFAULT_DISTANCE = 800.0

################################################################################

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
        #for i in range(1, ULTRASONIC_MEAN_LENGTH):
        #   self.distance_array = self.distance_array + [0] 

        self.on = True

        #self.getid(self.gpio_trigger, self.gpio_echo)

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
        #self.distance = self.poll_distance()
        self.distance = self.poll_distance_with_smoothing()
        return self.distance

    def shutdown(self):
        print('Shutdown ultrasonic', self.name)
        self.on = False
        time.sleep(1)
        GPIO.cleanup()

    def poll_distance(self):
        #print("a")

        #if GPIO.input(self.gpio_echo) == 1:
        #    return ULTRASONIC_DEFAULT_DISTANCE-1

        n=0
        while GPIO.input(self.gpio_echo) == 1:
            time.sleep(0.001)  # sleep for 1ms to wait for echo pin to become low
            #time.sleep(0.00001)
            #n=n+1
            #if n > 100000:
            #    return (ULTRASONIC_DEFAULT_DISTANCE)

        #print("b")
        distance = 0

        # set Trigger to HIGH
        GPIO.output(self.gpio_trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)

        #StartTime = StopTime = time.time()

        # save StartTime
        #while GPIO.input(self.gpio_echo) == 0:
        #    StartTime = time.time()
        #    if StartTime - StopTime > ULTRASONIC_TIMEOUT:
        #       distance = ULTRASONIC_DEFAULT_DISTANCE
        #       break

        #if distance == ULTRASONIC_DEFAULT_DISTANCE:
        #    print("ULTRASONIC_TIMEOUT")
        #    return (ULTRASONIC_DEFAULT_DISTANCE-2)

        just_arrived=0
        # save time of arrival
        #StopTime = StartTime

        #print("c %i" % GPIO.input(self.gpio_echo))

        n=0
        # wait for echo pin to become high
        while GPIO.input(self.gpio_echo) == 0:
            #time.sleep(0.001)  # sleep for 1ms
            n=n+1
            if n > 3000:
                #print("d %i %i" % (GPIO.input(self.gpio_echo), n))
                return (ULTRASONIC_DEFAULT_DISTANCE+1)
        #print("d %i %i" % (GPIO.input(self.gpio_echo), n))

        # test echo pin again in case the previous high is a fake one
        n=0
        while GPIO.input(self.gpio_echo) == 0:
            n=n+1
            if n > 3000:
                #print("e %i %i" % (GPIO.input(self.gpio_echo), n))
                return (ULTRASONIC_DEFAULT_DISTANCE+2)
        #print("e %i %i" % (GPIO.input(self.gpio_echo), n))

        StartTime = StopTime = time.time()

        n=0
        while GPIO.input(self.gpio_echo) == 1:
            n=n+1

            StopTime = time.time()  # update stop time
            #if StopTime - StartTime > ULTRASONIC_TIMEOUT:
            #   print("echo time longer than %f seconds" % ULTRASONIC_TIMEOUT)
            #   distance = ULTRASONIC_DEFAULT_DISTANCE
            #   break
        #print("f %i %i" % (GPIO.input(self.gpio_echo), n))

        #if distance == ULTRASONIC_DEFAULT_DISTANCE:
        #    return (ULTRASONIC_DEFAULT_DISTANCE-3)

        # Convert the timer values into centimetres
        distance = (StopTime - StartTime) * 34300 / 2
        #print("distance = %.4f" % distance)

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
        if distance < ULTRASONIC_DEFAULT_DISTANCE:
            array_len = len(self.distance_array)

            # append current value to array, up to ULTRASONIC_MEAN_LENGTH items
            if array_len < ULTRASONIC_MEAN_LENGTH:
                self.distance_array = self.distance_array + [distance]

            # pop out first value, push in current value
            else:
                self.distance_array = self.distance_array[1:] + [distance]

        mean_distance = np.mean(self.distance_array)
        print("%.4f %.4f" % (distance, mean_distance))

        return mean_distance

################################################################################

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

################################################################################

class CacheUltrasonicServer(Ultrasonic):
    def __init__(self, gpio_trigger=23, gpio_echo=27, poll_delay=1, name=''):

        super().__init__(gpio_trigger, gpio_echo, poll_delay, name)

        from pymemcache.client import base
        self.client = base.Client(('localhost', 11211))

    def update(self):
        while self.on:
            self.distance = self.poll_distance_with_smoothing()
            self.client.set('ultrasonic_' + self.name, self.distance)
            time.sleep(self.poll_delay)
            
    def run(self):
        self.distance = self.poll_distance_with_smoothing()
        self.client.set('ultrasonic_' + self.name, self.distance)
        return self.distance

    def shutdown(self):
        super().shutdown()
        self.client.close()

################################################################################

# to be called in the donkeycar loop
class CacheUltrasonicClient():
    def __init__(self, gpio_trigger = 12, gpio_echo = 16, poll_delay=1, name=''):
        from pymemcache.client import base
        self.client = base.Client(('localhost', 11211))

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
        self.client.close()

    def poll_distance(self):
        distance = self.client.get('ultrasonic_' + self.name)

        if not distance:
            distance = CACHEULTRASONICCLIENT_DEFAULT_DISTANCE
        else:
            distance = float(distance)

        return distance

if __name__ == "__main__":

    from sys import argv
    args = argv

    if (len(args) == 2):
        if args[1] != 'client':
            print("If you wish to run as client, eg python ultrasonic.py client")
            exit(1)
        else:
            iter = 0
            u = CacheUltrasonicClient(gpio_trigger=0, gpio_echo=0, name = 'front_left')

            while iter < 1000:
                data = u.run()
                print('ultrasonic: ', float(data))
                time.sleep(1/20)
                iter += 1

    elif (len(args) != 5):
        print("Enter trigger and echo pin number as arguments, eg python ultrasonic.py server 16 13 front_left")
        exit(1)

    else:
        u = Ultrasonic(gpio_trigger=int(args[2]), gpio_echo=int(args[3]), name = args[4])
        while True:
            data = u.run()
            print('ultrasonic: ', data)
            time.sleep(0.05)
            #time.sleep(ULTRASONIC_TIMEOUT)
