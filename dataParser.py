

import os
import re
from activity import Activity

from job import Job
from dut import Machine
from operation import Operation


def parse(path):
	with open(os.path.join(os.getcwd(), path), "r") as data:
		total_jobs, total_machines, max_operations = re.findall('\S+', data.readline())
		number_total_jobs, number_total_machines, number_max_operations = int(total_jobs), int(total_machines), int(float(
			max_operations))
		jobs_list = []
		# Current job's id
		id_job = 1
		print(number_total_jobs, number_total_machines, number_max_operations)


		for key, line in enumerate(data):
			if key >= number_total_jobs:
				break
			# Split data with multiple spaces as separator
			parsed_line = re.findall('\S+', line)
			print(parsed_line)
			# Current job
			job = Job(id_job)
			# Current activity's id
			id_activity = 1
			# Current item of the parsed line
			i = 1

			while i < len(parsed_line):
				number_operations = int(parsed_line[i])
				# print(number_operations)

				activity = Activity(job, id_activity)
				for id_operation in range(1, number_operations + 1):
					# print(parsed_line[i + 2 * id_operation - 1])
					
					activity.add_operation(Operation(id_operation, str(parsed_line[i + 2 * id_operation - 1]),
													 int(parsed_line[i + 2 * id_operation])))
					# operation is initialized with id_operation ie. the number in the list of operations, the id_machine (i want it to be a string instead of int) and the duration
				job.add_activity(activity)
				# jump to next operation sequence
				i += 1 + 2 * number_operations
				id_activity += 1
		
		machines_list = []
		for id_machine in range(1, number_total_machines+1):
			machine = Machine(id_machine, number_max_operations)
			machines_list.append(machine)

		return jobs_list, machines_list, number_max_operations

