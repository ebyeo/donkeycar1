"""
For testing performance
"""

import time
import csv
from donkeycar.parts.fuzzy import fuzzy

###############################################################################

def main():

    # Read car data from csv if available
    ifile = open("picar-readings.csv", "r")
    reader = csv.reader(ifile, delimiter=",")

    # instantiate fuzzy car to:
    # define fuzzy partitions and membership functions and
    # set the inference engine
    myFuzzyCar = fuzzy()

    rownum = 0
    car = []
    for row in reader:

        car.append(row)
        if rownum == 0:
            print('rownum, angleIn, left_distance, center_distance, right_distance, angleComputed, angleOut, pi-interval, interval')
        else:
            angleIn = float(car[rownum][0])
            left_distance = float(car[rownum][1])
            center_distance = float(car[rownum][2])
            right_distance = float(car[rownum][3])
            angleOut = float(car[rownum][4])
            interval = float(car[rownum][5])

            # check to make sure data is valid
            if myFuzzyCar.checkData(angleIn, left_distance, center_distance, right_distance) == False:
                return

            a = time.time()
            # evaluate each row by defuzzification
            outputAngle = myFuzzyCar.defuzzify()

            # print output
            print("%2i,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f" %
                  (rownum, angleIn, left_distance, center_distance, right_distance, outputAngle, angleOut, interval, time.time() - a))

        rownum += 1

    ifile.close()
    return 0

if __name__ == "__main__":
    main()

###############################################################################

"""
Result:
"""
