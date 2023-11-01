import copy
import sys
import timeit
from dataParser import parse
from geneticScheduler import GeneticScheduler


if len(sys.argv) == 1:
    path = "data/test.fjs"
else:
    path = sys.argv[1]

testsList, dutsList, numMaxOps = parse(path)
# parse(path)
numTotalDuts = len(dutsList)
numTotalTests = len(dutsList)

# print(number_total_duts)
# print(duts_list)
# print(duts_list[0].id_dut)

while True:
    tempTestsList = copy.deepcopy(testsList)
    tempDutsList = copy.deepcopy(dutsList)
    # popString = input("Total population [default=20]: ")
    # try:
    #     totalPop = int(popString)
    # except ValueError:
    #     totalPop = 20
    
    # genString = input("Max Generation [default=400]: ")
    # try:
    #     maxGen = int(genString)
    # except ValueError:
    #     maxGen = 400
    
    startTime = timeit.default_timer()
    schedule = GeneticScheduler(tempDutsList, tempTestsList)
    # schedule.runGenetic(totalPop, maxGen, verbose=True)
    schedule.runGenetic(20, 400, verbose=True)
    break


