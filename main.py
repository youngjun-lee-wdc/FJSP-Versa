import copy
import sys
import timeit
from dataParser import parse
from drawer import Drawer
from geneticScheduler import GeneticScheduler


if len(sys.argv) == 1:
    path = "data/test.fjs"
else:
    path = sys.argv[1]

testsList, dutsList, numMaxOps = parse(path)
# parse(path)
numTotalDuts = len(dutsList)
numTotalTests = len(dutsList)

print(testsList)
print(dutsList)


while True:
    tempTestsList = copy.deepcopy(testsList)
    tempDutsList = copy.deepcopy(dutsList)
    popString = input("Total population [default=20]: ")
    try:
        totalPop = int(popString)
    except ValueError:
        totalPop = 20
    
    genString = input("Max Generation [default=400]: ")
    try:
        maxGen = int(genString)
    except ValueError:
        maxGen = 400
    
    startTime = timeit.default_timer()
    schedule = GeneticScheduler(tempDutsList, tempTestsList)
    schedule.runGenetic(totalPop, maxGen, verbose=True)
    stopTime = timeit.default_timer()
    print("Finished in " + str(stopTime - startTime) + " seconds")

    draw = input("Draw the schedule ? [Y/N, default=Y] ")
    if draw == "n" or draw == "N":
        continue
    else:
        Drawer.drawSchedule(numTotalDuts, 1, tempTestsList, filename="outputGenetic.png")
    del schedule
    del tempTestsList, tempDutsList
    break


