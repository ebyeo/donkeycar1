"""
This part reads the parameters for input steering angle,
distance from left obstacle, distance from front (center) obstacle and
distance from right obstacle.
If obstacle is detected, it output the corrected angle
in an attempt to avoid the obstacle.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

################################################################################
# constants

# fuzzy trapezium membership for distance (cm)
MIN_DISTANCE = 0
MAX_DISTANCE = 140
FUZ_DISTANCE = 10

FUZZY_DIST_NEAR_LEFT_LO = MIN_DISTANCE
FUZZY_DIST_NEAR_LEFT_HI = 50
FUZZY_DIST_MED_LEFT_LO  = 40
FUZZY_DIST_MED_LEFT_HI  = 100
FUZZY_DIST_FAR_LEFT_LO  = 90
FUZZY_DIST_FAR_LEFT_HI  = MAX_DISTANCE

FUZZY_DIST_NEAR_CENT_LO = MIN_DISTANCE
FUZZY_DIST_NEAR_CENT_HI = 50
FUZZY_DIST_MED_CENT_LO  = 40
FUZZY_DIST_MED_CENT_HI  = 100
FUZZY_DIST_FAR_CENT_LO  = 90
FUZZY_DIST_FAR_CENT_HI  = MAX_DISTANCE

FUZZY_DIST_NEAR_RIGHT_LO = MIN_DISTANCE
FUZZY_DIST_NEAR_RIGHT_HI = 50
FUZZY_DIST_MED_RIGHT_LO  = 40
FUZZY_DIST_MED_RIGHT_HI  = 100
FUZZY_DIST_FAR_RIGHT_LO  = 90
FUZZY_DIST_FAR_RIGHT_HI  = MAX_DISTANCE

# fuzzy trapezium membership for angle (degrees)
MIN_ANGLE_VAL = -1.0
MAX_ANGLE_VAL =  1.0
FUZ_ANGLE = 0.1

FUZZY_ANGLE_FAR_LEFT_MIN = MIN_ANGLE_VAL
FUZZY_ANGLE_FAR_LEFT_MAX = -0.5
FUZZY_ANGLE_MID_LEFT_MIN = -0.7
FUZZY_ANGLE_MID_LEFT_MAX = -0.1
FUZZY_ANGLE_CENTER_MIN   = -0.3
FUZZY_ANGLE_CENTER_MAX   =  0.3
FUZZY_ANGLE_MID_RITE_MIN =  0.7
FUZZY_ANGLE_MID_RITE_MAX =  0.1
FUZZY_ANGLE_FAR_RITE_MIN =  0.5
FUZZY_ANGLE_FAR_RITE_MAX = MAX_ANGLE_VAL

DEBUGLEVEL = 0

################################################################################

class fuzzy:

    # constructor
    def __init__(self):

        self.fuzzify()
        self.inference()

    # --------------------------------------------------------------------------
    # This method verifies the correctness of the data:
    # (1) checks angle lies in correct range
    # (2) checks left, center and right distance lie in correct range
    #
    def checkData(self, angle, left_dist, center_dist, right_dist):

        if angle < MIN_ANGLE_VAL or angle > MAX_ANGLE_VAL:
            print("Invalid input angle %.2d" % angle)
            return False

        if left_dist < 0:
            print("Invalid left distance %.4f" % left_dist)
            return False

        if center_dist < 0:
            print("Invalid center distance %.4f" % center_dist)
            return False

        if right_dist < 0:
            print("Invalid right distance %.4f" % right_dist)
            return False

        self.input_angle = angle
        self.left_distance = left_dist
        self.center_distance = center_dist
        self.right_distance = right_dist
        return True

    # --------------------------------------------------------------------------
    # This method performs the fuzzification:
    # (1) sets the fuzzy partitions of each linguistic variable and
    # (2) sets the membership function of each linguistic term of the variable
    #
    def fuzzify(self):

        # set up input angle
        x = np.arange(-1, 1, 0.1)
        self.inputAngle = ctrl.Antecedent(x, "InputAngle")
        self.inputAngle['farleft']  = fuzz.trapmf(self.inputAngle.universe, [-1, -1, -0.7, -0.5])
        self.inputAngle['midleft']  = fuzz.trapmf(self.inputAngle.universe, [-0.7, -0.5, -0.3, -0.1])
        self.inputAngle['center']   = fuzz.trapmf(self.inputAngle.universe, [-0.3, -0.1, 0.1, 0.3])
        self.inputAngle['midright'] = fuzz.trapmf(self.inputAngle.universe, [0.1, 0.3, 0.5, 0.7])
        self.inputAngle['farright'] = fuzz.trapmf(self.inputAngle.universe, [0.5, 0.7, 1, 1])

        # set up left distance
        x = np.arange(0, MAX_DISTANCE+1, 10)
        self.leftDistance = ctrl.Antecedent(x, "LeftDistance")
        self.leftDistance['near'] = fuzz.trapmf(self.leftDistance.universe, [0, 0, 40, 50])
        self.leftDistance['med']  = fuzz.trapmf(self.leftDistance.universe, [40, 50, 90,100])
        self.leftDistance['far']  = fuzz.trapmf(self.leftDistance.universe, [90, 100, MAX_DISTANCE, MAX_DISTANCE])

        # set up center distance
        x = np.arange(0, MAX_DISTANCE+1, 10)
        self.centerDistance = ctrl.Antecedent(x, "CenterDistance")
        self.centerDistance['near'] = fuzz.trapmf(self.centerDistance.universe, [0, 0, 40, 50])
        self.centerDistance['med']  = fuzz.trapmf(self.centerDistance.universe, [40, 50, 90, 100])
        self.centerDistance['far']  = fuzz.trapmf(self.centerDistance.universe, [90, 100, MAX_DISTANCE, MAX_DISTANCE])

        # set up right distance
        x = np.arange(0, MAX_DISTANCE+1, 10)
        self.rightDistance = ctrl.Antecedent(x, "RightDistance")
        self.rightDistance['near'] = fuzz.trapmf(self.rightDistance.universe, [0, 0, 40, 50])
        self.rightDistance['med']  = fuzz.trapmf(self.rightDistance.universe, [40, 50, 90, 100])
        self.rightDistance['far']  = fuzz.trapmf(self.rightDistance.universe, [90, 100, MAX_DISTANCE, MAX_DISTANCE])

        # set up output angle as a consequent
        x = np.arange(-1, 1, 0.1)
        self.outputAngleCon = ctrl.Consequent(x, 'OutputAngle')
        self.outputAngleCon['farleft']  = fuzz.trapmf(self.outputAngleCon.universe, [-1, -1, -0.7, -0.5])
        self.outputAngleCon['midleft']  = fuzz.trapmf(self.outputAngleCon.universe, [-0.7, -0.5, -0.3, -0.1])
        self.outputAngleCon['center']   = fuzz.trapmf(self.outputAngleCon.universe, [-0.3, -0.1, 0.1, 0.3])
        self.outputAngleCon['midright'] = fuzz.trapmf(self.outputAngleCon.universe, [0.1, 0.3, 0.5, 0.7])
        self.outputAngleCon['farright'] = fuzz.trapmf(self.outputAngleCon.universe, [0.5, 0.7, 1, 1])

        if DEBUGLEVEL == 1:
            self.leftDistance.view()
            self.centerDistance.view()
            self.rightDistance.view()
            self.inputAngle.view()
            self.outputAngleCon.view()

        return

    # --------------------------------------------------------------------------
    # This method:
    # (1) sets the rule base
    # (2) sets the inference engine to use the rule base
    #
    def inference(self):

        # rules 01 - 27
        # farleft inputAngle & leftDistance & centerDistance & rightDistance -> outputAngleCon
        rule01 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['farleft'])
        rule02 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule03 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['farleft'])
        rule04 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['farleft'])
        rule05 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule06 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['farleft'])
        rule07 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farleft'])
        rule08 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule09 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule10 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule11 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule12 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule13 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule14 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule15 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['farleft'])
        rule16 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule17 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule18 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule19 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule20 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule21 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule22 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule23 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule24 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule25 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule26 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule27 = ctrl.Rule(self.inputAngle['farleft'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        # rules 28 - 54
        # midleft inputAngle & leftDistance & centerDistance & rightDistance -> outputAngleCon
        rule28 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['midleft'])
        rule29 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule30 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule31 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midleft'])
        rule32 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule33 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule34 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['midleft'])
        rule35 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule36 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['midleft'])

        rule37 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule38 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule39 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule40 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule41 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule42 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule43 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule44 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule45 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['midleft'])

        rule46 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule47 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule48 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule49 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule50 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule51 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule52 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule53 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule54 = ctrl.Rule(self.inputAngle['midleft'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['midleft'])

        # rules 55 - 81
        # center inputAngle & leftDistance & centerDistance & rightDistance -> outputAngleCon
        rule55 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule56 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule57 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule58 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule59 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule60 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule61 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule62 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule63 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule64 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule65 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule66 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule67 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule68 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midright'])
        rule69 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule70 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule71 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule72 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule73 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['center'])
        rule74 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule75 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule76 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule77 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule78 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule79 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule80 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule81 = ctrl.Rule(self.inputAngle['center'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['center'])

        # rules 82 - 108
        # midright inputAngle & leftDistance & centerDistance & rightDistance -> outputAngleCon
        rule82 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule83 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule84 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule85 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule86 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule87 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule88 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule89 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule90 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule91 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule92 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule93 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule94 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule95 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midright'])
        rule96 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule97 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule98 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['midright'])
        rule99 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule100 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule101 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule102 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule103 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule104 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midright'])
        rule105 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule106 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['midright'])
        rule107 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['midright'])
        rule108 = ctrl.Rule(self.inputAngle['midright'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['midright'])

        # rules 109 - 135
        # farright inputAngle & leftDistance & centerDistance & rightDistance -> outputAngleCon
        rule109 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule110 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule111 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule112 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule113 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['midleft'])
        rule114 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['midleft'])
        rule115 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule116 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farleft'])
        rule117 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['far'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule118 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule119 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule120 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule121 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule122 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule123 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule124 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule125 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule126 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['med'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farleft'])

        rule127 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule128 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['med'], self.outputAngleCon['center'])
        rule129 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['far'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule130 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule131 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule132 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['med'] & self.rightDistance['near'], self.outputAngleCon['center'])
        rule133 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['far'], self.outputAngleCon['farright'])
        rule134 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['med'], self.outputAngleCon['farright'])
        rule135 = ctrl.Rule(self.inputAngle['farright'] & self.leftDistance['near'] & self.centerDistance['near'] & self.rightDistance['near'], self.outputAngleCon['farright'])

        # set up control system for output angle
        self.outputAngleCS = ctrl.ControlSystem(
            [rule01, rule02, rule03, rule04, rule05, rule06, rule07, rule08, rule09, rule10,
             rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
             rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,
             rule31, rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40,
             rule41, rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50,
             rule51, rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60,
             rule61, rule62, rule63, rule64, rule65, rule66, rule67, rule68, rule69, rule70,
             rule71, rule72, rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80,
             rule81, rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89, rule90,
             rule91, rule92, rule93, rule94, rule95, rule96, rule97, rule98, rule99, rule100,
             rule101, rule102, rule103, rule104, rule105, rule106, rule107, rule108, rule109, rule110,
             rule111, rule112, rule113, rule114, rule115, rule116, rule117, rule118, rule119, rule120,
             rule121, rule122, rule123, rule124, rule125, rule126, rule127, rule128, rule129, rule130,
             rule131, rule132, rule133, rule134, rule135
             ])
        self.outputAngleEval = ctrl.ControlSystemSimulation(self.outputAngleCS)

        return

    # --------------------------------------------------------------------------
    # This method evaluates the given data with inference engine
    # and defuzzifies the output
    # Returns output angle
    #
    def defuzzify(self):

        self.outputAngleEval.input['InputAngle']     = self.input_angle
        self.outputAngleEval.input['LeftDistance']   = self.left_distance
        self.outputAngleEval.input['CenterDistance'] = self.center_distance
        self.outputAngleEval.input['RightDistance']  = self.right_distance
        self.outputAngleEval.compute()
        outputAngle = self.outputAngleEval.output['OutputAngle']

        return outputAngle

