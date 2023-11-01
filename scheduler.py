import sys

from colorama import init
from termcolor import colored


class Scheduler:
	def __init__(self, duts, max_operations, tests):
		init()  # Init colorama for color display
		self.__original_stdout = sys.stdout
		self.__duts = duts
		self.__tests_to_be_done = tests
		self.__tests_done = []
		self.__max_operations = max_operations

	# Run the scheduler with an heuristic
	def run(self, heuristic, verbose=True):
		# Disable print if verbose is False
		if not verbose:
			sys.stdout = None

		current_step = 0

		while len(self.__tests_to_be_done) > 0:
			current_step += 1

			best_candidates = heuristic(self.__tests_to_be_done, self.__max_operations, current_step)
			for id_dut, candidates in best_candidates.items():
				dutsList = [dut.id_dut for dut in self.__duts]
				idx = dutsList.index(id_dut)
				dut = self.__duts[idx]
				for activity, operation in candidates:
					if not (dut.is_working_at_max_capacity() or activity.is_pending):
						dut.add_operation(activity, operation)

			for dut in self.__duts:
				dut.work()

			for test in self.__tests_to_be_done:
				if test.is_done:
					self.__tests_to_be_done = list(
						filter(lambda element: element.id_test != test.id_test, self.__tests_to_be_done))
					self.__tests_done.append(test)

		print(colored("[SCHEDULER]", "green"), "Done in " + str(current_step) + " units of time")

		# Reenable stdout
		if not verbose:
			sys.stdout = self.__original_stdout


		return current_step
