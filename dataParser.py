import os
import re
from activity import Activity

from test import Test
from dut import Dut
from operation import Operation


def parse(path):
	with open(os.path.join(os.getcwd(), path), "r") as data:
		total_tests, total_duts, max_operations = re.findall('\S+', data.readline())
		number_total_tests, number_total_duts, number_max_operations = int(total_tests), int(total_duts), int(float(
			max_operations))
		tests_list = []
		duts = set()

		# Current test's id
		id_test = 1
		# print(number_total_tests, number_total_duts, number_max_operations)


		for key, line in enumerate(data):
			# invalid test data 
			if key >= number_total_tests:
				break
			# Split data with multiple spaces as separator
			parsed_line = re.findall('\S+', line)
			# print(parsed_line)
			# Current test
			test = Test(id_test)
			# print(test)
			# Current test's id
			id_activity = 1
			# Current item of the parsed line
			i = 1

			while i < len(parsed_line):
				operation_alternates = int(parsed_line[i])

				activity = Activity(test, id_activity)
				for id_operation_alt in range(1, operation_alternates + 1):

					dut_alt = parsed_line[i+2 * id_operation_alt - 1]
					if dut_alt not in duts:
						duts.add(dut_alt)
					activity.add_operation(Operation(id_operation_alt, str(parsed_line[i + 2 * id_operation_alt - 1]),
													 int(parsed_line[i + 2 * id_operation_alt])))
					# operation is initialized with id_operation ie. the number in the list of operations, the id_machine (i want it to be a string instead of int) and the duration
				test.add_activity(activity)
				# jump to next operation sequence
				i += 1 + 2 * operation_alternates
				id_test += 1
			tests_list.append(test)
			id_test += 1
		duts_list = []
		# print(duts)
		for dut in duts:
			duts_list.append(Dut(dut, number_max_operations))

		return tests_list, duts_list, number_max_operations

