class Heuristics:
	# When a choice between multiple operations is available, always pick the first one
	@staticmethod
	def select_first_operation(tests_to_be_done, max_operations, _):
		best_candidates = {}

		for test in tests_to_be_done:
			current_activity = test.current_activity
			best_operation = current_activity.shortest_operation

			if best_candidates.get(best_operation.id_dut) is None:
				best_candidates.update({best_operation.id_dut: [(current_activity, best_operation)]})
			elif len(best_candidates.get(best_operation.id_dut)) < max_operations:
				best_candidates.get(best_operation.id_dut).append((current_activity, best_operation))
			else:
				list_operations = best_candidates.get(best_operation.id_dut)

				for key, (_, operation) in enumerate(list_operations):
					if operation.duration < best_operation.duration:
						list_operations.pop(key)
						break

				if len(list_operations) < max_operations:
					list_operations.append((current_activity, best_operation))

		return best_candidates

	# LEPT rule
	@staticmethod
	def longest_expected_processing_time_first(jobs_to_be_done, max_operations, current_time):
		pass

	# Shortest slack per remaining operations
	# S/RO = [(Due date - Today’s date) - Total shop time remaining] / Number of operations remaining
	@staticmethod
	def shortest_slack_per_remaining_operations(jobs_to_be_done, max_operations, current_time):
		pass

	# Highest critical ratios
	# CR = Processing Time / (Due Date – Current Time)
	@staticmethod
	def highest_critical_ratios(tests_to_be_done, max_operations, current_time):
		best_candidates = {}
		critical_ratios = {}
		assignment = {}

		for test in tests_to_be_done:
			current_activity = test.current_activity

			# Compute critical ratio for each operation for an activity
			for operation in current_activity.next_operations:
				critical_ratio = operation.duration / (test.total_shop_time - current_time)
				critical_ratios.update({test.id_job: (current_activity, operation, critical_ratio)})

			for id_job, current_activity, operation, critical_ratio in critical_ratios.items():
				if assignment.get(operation.id_dut) is None:
					assignment.update({operation.id_dut: (current_activity, operation, critical_ratio)})

				elif len(assignment.get(operation.id_dut)) < max_operations:
					list_operations = assignment.get(operation.id_dut)
					list_operations.append((current_activity, operation, critical_ratio))
					best_candidates.update({operation.id_dut: list_operations})

	# TODO: end that

	# Assign randomly jobs to machine
	@staticmethod
	def random_operation_choice(tests_to_be_done, max_operations, _):
		import random
		best_candidates = {}
		dict_operations = {}

		for test in tests_to_be_done:
			current_activity = test.current_activity
			for operation in current_activity.next_operations:
				if dict_operations.get(operation.id_dut) is None:
					dict_operations.update({operation.id_dut: [(current_activity, operation)]})
				else:
					dict_operations.get(operation.id_dut).append((current_activity, operation))

		for dut, list_operations in dict_operations.items():
			best_candidates.update({dut: list(
				set([list_operations[random.randint(0, len(list_operations) - 1)] for _ in range(max_operations)]))})

		return best_candidates

	## Creation of Machine assignment and operation sequence lists (need improvement)
	##
	@staticmethod
	def initialisation_list(tests_to_be_done):
		dut_assignment = []
		operation_sequence = []
		for job in tests_to_be_done:
			for activity in job.activities_to_be_done:
				operation_sequence.append(job.id_job)
				dut_assignment.append(activity.next_operations[0].id_dut)
		print("machine assignment :")
		for dut in dut_assignment:
			print(str(dut))
		print("operation sequence :")
		for operation in operation_sequence:
			print(operation)
