from test import Test
from activity import Activity
from operation import Operation
from dut import Dut

import os
import re


def parse(path):
    with open(os.path.join(os.getcwd(), path), "r") as data:
        totalTests, totalDuts, maxOperations = re.findall(
            '\S+', data.readline())
        numberTotalTests, numberTotalDuts, numberMaxOperations = int(totalTests), int(totalDuts), int(float(
            maxOperations))
        testsList = []
        duts = set()
        # Current job's id
        idTest = 1

        for key, line in enumerate(data):
            if key >= numberTotalTests:
                break
            # Split data with multiple spaces as separator
            parsedLine = re.findall('\S+', line)
            # Current job
            test = Test(idTest)
            # Current activity's id
            idActivity = 1
            # Current item of the parsed line
            i = 1
            while i < len(parsedLine):
                # Total number of operations for the activity
                numberOperations = int(parsedLine[i])
                # Current activity
                activity = Activity(test, idActivity)
                for idOperation in range(1, numberOperations + 1):
                    dutAlt = parsedLine[i + 2 * idOperation - 1]
                    if dutAlt not in duts:
                        duts.add(dutAlt)

                    activity.addOperation(Operation(idOperation, parsedLine[i + 2 * idOperation - 1],
                                                    int(parsedLine[i + 2 * idOperation])))
                    # operation is initialized with idOperation ie. the number in the list of operations, the idDut (i want it to be a string instead of int) and the duration
                test.addActivity(activity)
                i += 1 + 2 * numberOperations
                idActivity += 1

            testsList.append(test)
            idTest += 1


    # Duts
    dutsList = []
    for dut in duts:
        dutsList.append(Dut(dut, numberMaxOperations))

    return testsList, dutsList, numberMaxOperations
