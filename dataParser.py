import os
import re
from activity import Activity

from test import Test
from dut import Dut
from operation import Operation


def parse(path):
	with open(os.path.join(os.getcwd(), path), "r") as data:
		totalTests, totalDuts, maxOperations = re.findall('\S+', data.readline())
		numberTotalTests, numberTotalDuts, numberMaxOperations = int(totalTests), int(totalDuts), int(float(
			maxOperations))
		testsList = []
		duts = set()

		# Current test's id
		idTest = 1
		# print(number_total_tests, number_total_duts, number_max_operations)


		for key, line in enumerate(data):
			# invalid test data 
			if key >= numberTotalTests:
				break
			# Split data with multiple spaces as separator
			parsedLine = re.findall('\S+', line)
			# print(parsed_line)
			# Current test
			test = Test(idTest)
			# print(test)
			# Current test's id
			idActivity = 1
			# Current item of the parsed line
			i = 1

			while i < len(parsedLine):
				operationAlts = int(parsedLine[i])

				activity = Activity(test, idActivity)
				for idOperationAlt in range(1, operationAlts + 1):

					dutAlt = parsedLine[i+2 * idOperationAlt - 1]
					if dutAlt not in duts:
						duts.add(dutAlt)
					activity.addOperation(Operation(idOperationAlt, str(parsedLine[i + 2 * idOperationAlt - 1]),
													 int(parsedLine[i + 2 * idOperationAlt])))
					# operation is initialized with id_operation ie. the number in the list of operations, the id_machine (i want it to be a string instead of int) and the duration
				test.addActivity(activity)
				# jump to next operation sequence
				i += 1 + 2 * operationAlts
				idTest += 1
			testsList.append(test)
			idTest += 1
		dutsList = []
		# print(duts)
		for dut in duts:
			dutsList.append(Dut(dut, numberMaxOperations))

		return testsList, dutsList, numberMaxOperations

