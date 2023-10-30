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
		# Current test's id
		id_test = 1
		print(number_total_tests, number_total_duts, number_max_operations)


		for key, line in enumerate(data):
			# invalid test data 
			if key >= number_total_tests:
				break
			# Split data with multiple spaces as separator
			parsed_line = re.findall('\S+', line)
			print(parsed_line)
			# Current job
			test = Test(id_test)
			# Current test's id
			id_test = 1
			# Current item of the parsed line
			i = 1

			while i < len(parsed_line):
				operation_alternates = int(parsed_line[i])

				activity = Activity(test, id_test)
				for id_operation in range(1, operation_alternates + 1):
					# print(parsed_line[i + 2 * id_operation - 1])
					
					activity.add_operation(Operation(id_operation, str(parsed_line[i + 2 * id_operation - 1]),
													 int(parsed_line[i + 2 * id_operation])))
					# operation is initialized with id_operation ie. the number in the list of operations, the id_machine (i want it to be a string instead of int) and the duration
				test.add_activity(activity)
				# jump to next operation sequence
				i += 1 + 2 * operation_alternates
				id_test += 1
		
		duts_list = []
		for id_dut in range(1, number_total_duts+1):
			dut = Dut(id_dut, number_max_operations)
			duts_list.append(dut)

		return tests_list, duts_list, number_max_operations

