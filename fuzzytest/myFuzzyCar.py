"""
For testing fuzzy.py
"""

import csv
from fuzzy import fuzzy

###############################################################################

def main():

    # Read car data from csv if available
    ifile = open("car.csv", "r")
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
            for i in range(len(car[rownum])):
                print("%s," % car[rownum][i], end='')
            print("OutputAngle")
        else:
            angle = float(car[rownum][1])
            left_distance = float(car[rownum][2])
            center_distance = float(car[rownum][3])
            right_distance = float(car[rownum][4])
            rule = car[rownum][5]

            # check to make sure data is valid
            if myFuzzyCar.checkData(angle, left_distance, center_distance, right_distance) == False:
                return

            # evaluate each row by defuzzification
            outputAngle = myFuzzyCar.defuzzify()

            # print output
            print("%2i,%.4f,%.4f,%.4f,%.4f,%s,%.4f" %
                  (rownum, angle, left_distance, center_distance, right_distance, rule, outputAngle))

        rownum += 1

    ifile.close()
    return 0

if __name__ == "__main__":
    main()

###############################################################################

"""
Result:
"""
