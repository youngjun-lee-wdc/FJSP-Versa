class Heuristics:
	# When a choice between multiple operations is available, always pick the first one
	@staticmethod
	def selectFirstOperation(testsToBeDone, maxOperations, _):
		bestCandidates = {}

		for test in testsToBeDone:
			currentActivity = test.currentActivity
			bestOperation = currentActivity.shortestOperation

			if bestCandidates.get(bestOperation.idDut) is None:
				bestCandidates.update({bestOperation.idDut: [(currentActivity, bestOperation)]})
			elif len(bestCandidates.get(bestOperation.idDut)) < maxOperations:
				bestCandidates.get(bestOperation.idDut).append((currentActivity, bestOperation))
			else:
				listOperations = bestCandidates.get(bestOperation.idDut)

				for key, (_, operation) in enumerate(listOperations):
					if operation.duration < bestOperation.duration:
						listOperations.pop(key)
						break

				if len(listOperations) < maxOperations:
					listOperations.append((currentActivity, bestOperation))

		return bestCandidates

	# LEPT rule
	@staticmethod
	def longestExpectedProcessingTimeFirst(testsToBeDone, maxOperations, currentTime):
		pass

	# Shortest slack per remaining operations
	# S/RO = [(Due date - Today’s date) - Total shop time remaining] / Number of operations remaining
	@staticmethod
	def shortestSlackPerRemainingOperations(testsToBeDone, maxOperations, currentTime):
		pass

	# Highest critical ratios
	# CR = Processing Time / (Due Date – Current Time)
	@staticmethod
	def highestCriticalRatios(testsToBeDone, maxOperations, currentTime):
		bestCandidates = {}
		criticalRatios = {}
		assignment = {}

		for test in testsToBeDone:
			currentActivity = test.currentActivity

			# Compute critical ratio for each operation for an activity
			for operation in currentActivity.nextOperations:
				criticalRatio = operation.duration / (test.totalShopTime - currentTime)
				criticalRatios.update({test.idTest: (currentActivity, operation, criticalRatio)})

			for idTest, currentActivity, operation, criticalRatio in criticalRatios.items():
				if assignment.get(operation.idDut) is None:
					assignment.update({operation.idDut: (currentActivity, operation, criticalRatio)})

				elif len(assignment.get(operation.idDut)) < maxOperations:
					listOperations = assignment.get(operation.idDut)
					listOperations.append((currentActivity, operation, criticalRatio))
					bestCandidates.update({operation.idDut: listOperations})

	# TODO: end that

	# Assign randomly tests to dut
	@staticmethod
	def randomOperationChoice(testsToBeDone, maxOperations, _):
		import random
		bestCandidates = {}
		dictOperations = {}

		for test in testsToBeDone:
			currentActivity = test.currentActivity
			for operation in currentActivity.nextOperations:
				if dictOperations.get(operation.idDut) is None:
					dictOperations.update({operation.idDut: [(currentActivity, operation)]})
				else:
					dictOperations.get(operation.idDut).append((currentActivity, operation))

		for dut, listOperations in dictOperations.items():
			bestCandidates.update({dut: list(
				set([listOperations[random.randint(0, len(listOperations) - 1)] for _ in range(maxOperations)]))})
		return bestCandidates

	## Creation of Dut assignment and operation sequence lists (need improvement)
	##
	@staticmethod
	def initialisationList(testsToBeDone):
		dutAssignment = []
		operationSequence = []
		for test in testsToBeDone:
			for activity in test.activitiesToBeDone:
				operationSequence.append(test.idTest)
				dutAssignment.append(activity.nextOperations[0].idDut)
		print("dut assignment :")
		for dut in dutAssignment:
			print(str(dut))
		print("operation sequence :")
		for operation in operationSequence:
			print(operation)
