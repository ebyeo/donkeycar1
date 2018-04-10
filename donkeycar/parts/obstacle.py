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

class Obstacle():
    def __init__(self):
        # initialize default action to go forward
        self.action = Constant.OBSTACLE_ACTION_FORWARD
    
    def compute_action(self):
        return Constant.OBSTACLE_ACTION_FORWARD

    def run(self, img_arr=None, ultrasonic_front_distance=None, ultrasonic_front_left_distance=None, ultrasonic_front_right_distance=None):
        self.img_arr = img_arr
        self.ultrasonic_front_distance = ultrasonic_front_distance
        self.ultrasonic_front_left_distance = ultrasonic_front_left_distance
        self.ultrasonic_front_right_distance = ultrasonic_front_right_distance
        self.action = self.compute_action()
		
        return self.action
		
    def shutdown(self):
        # indicate that the thread should be stopped
        print('stopping obstacle detection')

if __name__ == "__main__":
    o = Obstacle()
    print('obstacle:', o.run(ultrasonic_front_distance = 55))

