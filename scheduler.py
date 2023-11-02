import sys

from colorama import init
from termcolor import colored


class Scheduler:
	def __init__(self, duts, maxOperations, tests):
		init()  # Init colorama for color display
		self.__originalStdout = sys.stdout
		self.__duts = duts
		self.__testsToBeDone = tests
		self.__testsDone = []
		self.__maxOperations = maxOperations

	# Run the scheduler with an heuristic
	def run(self, heuristic, verbose=True):
		# Disable print if verbose is False
		if not verbose:
			sys.stdout = None

		currentStep = 0

		while len(self.__testsToBeDone) > 0:
			currentStep += 1

			bestCandidates = heuristic(self.__testsToBeDone, self.__maxOperations, currentStep)
			for idDut, candidates in bestCandidates.items():
				dutsList = [dut.idDut for dut in self.__duts]
				idx = dutsList.index(idDut)
				dut = self.__duts[idx]
				for activity, operation in candidates:
					if not (dut.isWorkingAtMaxCapacity() or activity.isPending):
						dut.addOperation(activity, operation)

			for dut in self.__duts:
				dut.work()

			for test in self.__testsToBeDone:
				if test.is_done:
					self.__testsToBeDone = list(
						filter(lambda element: element.idTest != test.idTest, self.__testsToBeDone))
					self.__testsDone.append(test)

		print(colored("[SCHEDULER]", "green"), "Done in " + str(currentStep) + " units of time")

		# Reenable stdout
		if not verbose:
			sys.stdout = self.__originalStdout


		return currentStep
