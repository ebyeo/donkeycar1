"""
Scripts to start the ultrasonic server.

Usage:
   run_ultrasonic.py (front)
   run_ultrasonic.py (front_left)
   run_ultrasonic.py (front_right)
"""

import time
import sys
from docopt import docopt
import donkeycar as dk
from donkeycar.parts.ultrasonic import CacheUltrasonicServer

def ultrasonic_front():
    return cfg.ULTRASONIC_FRONT_TRIGGER, cfg.ULTRASONIC_FRONT_ECHO, cfg.ULTRASONIC_FRONT_POLL_DELAY, 'front'

def ultrasonic_front_left():
    return cfg.ULTRASONIC_FRONT_LEFT_TRIGGER, cfg.ULTRASONIC_FRONT_LEFT_ECHO, cfg.ULTRASONIC_FRONT_LEFT_POLL_DELAY, 'front_left'

def ultrasonic_front_right():
    return cfg.ULTRASONIC_FRONT_RIGHT_TRIGGER, cfg.ULTRASONIC_FRONT_RIGHT_ECHO, cfg.ULTRASONIC_FRONT_RIGHT_POLL_DELAY, 'front_right'

if __name__ == "__main__":
    args = docopt(__doc__)
    cfg = dk.load_config()

    if args['front']:
        trigger, echo, poll_delay, name = ultrasonic_front()
    elif args['front_left']:
        trigger, echo, poll_delay, name = ultrasonic_front_left()
    elif args['front_right']:
        trigger, echo, poll_delay, name = ultrasonic_front_right()

    u = CacheUltrasonicServer(gpio_trigger=trigger, gpio_echo=echo, poll_delay = poll_delay, name = name)
    u.update()
