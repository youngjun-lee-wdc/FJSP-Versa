class Activity:
	def __init__(self, test, idActivity):
		self.__test = test
		self.__idActivity = idActivity
		self.__operationsToBeDone = []
		self.__operationDone = None

	# Display the activity nicer
	def __str__(self):
		output = "Test # " + str(self.idTest) + " Activity #" + str(self.__idActivity) + "\n"

		output += "Operations to be done\n"
		for operation in self.__operationsToBeDone:
			output += str(operation) + "\n"

		output += "Operation done\n"
		output += str(self.__operationDone) + "\n"

		return output

	# Return the test's id of the activity
	@property
	def idTest(self):
		return self.__test.idTest

	# Return the activity's id
	@property
	def idActivity(self):
		return self.__idActivity

	# Add an operation to the activity
	def addOperation(self, operation):
		self.__operationsToBeDone.append(operation)

	# Return if the activity is done
	@property
	def isDone(self):
		return not (self.__operationDone is None)

	# Return the list of all the operations yet to be done
	@property
	def nextOperations(self):
		return self.__operationsToBeDone

	# Return the shortest operation available
	@property
	def shortestOperation(self):
		candidateOperation = None
		for operation in self.__operationsToBeDone:
			if candidateOperation is None or operation.duration < candidateOperation.duration:
				candidateOperation = operation
		return operation

	# Return the list of all the operations already done
	@property
	def operationDone(self):
		return self.__operationDone

	# Allow a machine to say to an activity that it finished an operation
	def terminateOperation(self, operation):
		# Remove the operation from the list of the operations yet to be done
		self.__operationsToBeDone = list(
			filter(lambda element: element.idOperation != operation.idOperation, self.__operationsToBeDone))
		# Append the operation to the list of the operations already done
		self.__operationDone = operation
		self.__test.activityIsDone(self)

	@property
	def shopTime(self):
		return self.operationDone.duration if self.isDone else max(self.__operationsToBeDone,
																	 key=lambda operation: operation.duration)

	@property
	def isFeasible(self):
		return self.__test.checkIfPreviousActivityIsDone(self.__idActivity)

	@property
	def isPending(self):
		return len(list(filter(lambda element: element.isPending, self.__operationsToBeDone))) > 0

	def getOperation(self, idOperation):
		for operation in self.__operationsToBeDone:
			if operation.idOperation == idOperation:
				return operation
