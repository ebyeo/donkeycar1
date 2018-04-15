"""
Obstacle Detection

Returns true if there is an obstacle in the direction of the sensor

Actions are:
- forward - no obstacle in front or within range, go forward
- overtake-right - overtake obstacle in front by changing lane to the right, priority to overtake on the right
- overtake-left - if overtaking right is not possible due to neighbouring vehicle, overtake on the left
- stop - if there is no way to avoid obstacle, stop immediately
- reverse - for future considerations
"""

import donkeycar.constant as Constant

OBSTACLE_DISTANCE_LENGTH = 5

class Obstacle():
    def __init__(self):
        # initialize default action to go forward
        self.action = Constant.OBSTACLE_ACTION_FORWARD

        self.front_distance_array = []
        for i in range(OBSTACLE_DISTANCE_LENGTH):
            self.front_distance_array = self.front_distance_array + [10000]
        self.front_left_distance_array = []
        for i in range(OBSTACLE_DISTANCE_LENGTH):
            self.front_left_distance_array = self.front_left_distance_array + [10000]

        self.front_right_distance_array = []
        for i in range(OBSTACLE_DISTANCE_LENGTH):
            self.front_right_distance_array = self.front_right_distance_array + [10000]

    def compute_action(self):
        if self.ultrasonic_front_distance <= 50 and self.ultrasonic_front_distance >= 0:
            stop = True
            for i in range(OBSTACLE_DISTANCE_LENGTH-1):
                if (self.front_distance_array[i] < self.front_distance_array[i + 1]):
                    stop = False
                    break

            if stop:
                return Constant.OBSTACLE_ACTION_STOP

        if self.ultrasonic_front_right_distance <= 50 and self.ultrasonic_front_right_distance >= 0:
            stop = True
            for i in range(OBSTACLE_DISTANCE_LENGTH-1):
                if (self.front_right_distance_array[i] < self.front_right_distance_array[i + 1]):
                    stop = False
                    break

            if stop:
                return Constant.OBSTACLE_ACTION_STOP

        if self.ultrasonic_front_left_distance <= 50 and self.ultrasonic_front_left_distance >= 0:
            stop = True
            for i in range(OBSTACLE_DISTANCE_LENGTH-1):
                if (self.front_left_distance_array[i] < self.front_left_distance_array[i + 1]):
                    stop = False
                    break

            if stop:
                return Constant.OBSTACLE_ACTION_STOP
					
        return Constant.OBSTACLE_ACTION_FORWARD

    def run(self, img_arr=None, ultrasonic_front_distance=None, ultrasonic_front_left_distance=None, ultrasonic_front_right_distance=None):
        self.img_arr = img_arr

        self.ultrasonic_front_distance = ultrasonic_front_distance
        self.front_distance_array = self.front_distance_array[1:] + [self.ultrasonic_front_distance]

        self.ultrasonic_front_left_distance = ultrasonic_front_left_distance
        self.front_left_distance_array = self.front_left_distance_array[1:] + [self.ultrasonic_front_left_distance]

        self.ultrasonic_front_right_distance = ultrasonic_front_right_distance
        self.front_right_distance_array = self.front_right_distance_array[1:] + [self.ultrasonic_front_right_distance]

        self.action = self.compute_action()
		
        return self.action
		
    def shutdown(self):
        # indicate that the thread should be stopped
        print('stopping obstacle detection')

if __name__ == "__main__":
    o = Obstacle()
    print('obstacle:', o.run(ultrasonic_front_distance = 55, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))
    print('obstacle:', o.run(ultrasonic_front_distance = 54, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))
    print('obstacle:', o.run(ultrasonic_front_distance = 53, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))
    print('obstacle:', o.run(ultrasonic_front_distance = 62, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))
    print('obstacle:', o.run(ultrasonic_front_distance = 51, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))
    print('obstacle:', o.run(ultrasonic_front_distance = 50, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))
    print('obstacle:', o.run(ultrasonic_front_distance = 45, ultrasonic_front_left_distance = 55, ultrasonic_front_right_distance = 55))

