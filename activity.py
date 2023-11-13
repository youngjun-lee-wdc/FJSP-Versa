class Activity:
	def __init__(self, test, idActivity):
		self.Test = test
		self.IdActivity = idActivity
		self.OperationsToBeDone = []
		self.OperationDone = None

	# Display the activity nicer
	def __str__(self):
		output = "Test n°" + str(self.idTest) + " Activity n°" + str(self.IdActivity) + "\n"

		output += "Operations to be done\n"
		for operation in self.OperationsToBeDone:
			output += str(operation) + "\n"

		output += "Operation done\n"
		output += str(self.OperationDone) + "\n"

		return output

	# Return the test's id of the activity
	@property
	def idTest(self):
		return self.Test.idTest

	# Return the activity's id
	@property
	def idActivity(self):
		return self.IdActivity

	# Add an operation to the activity
	def addOperation(self, operation):
		self.OperationsToBeDone.append(operation)

	# Return if the activity is done
	@property
	def isDone(self):
		return not (self.OperationDone is None)

	# Return the list of all the operations yet to be done
	@property
	def nextOperations(self):
		return self.OperationsToBeDone

	# Return the shortest operation available
	@property
	def shortestOperation(self):
		candidateOperation = None
		for operation in self.OperationsToBeDone:
			if candidateOperation is None or operation.duration < candidateOperation.duration:
				candidateOperation = operation
		return operation

	# Return the list of all the operations already done
	@property
	def operationDone(self):
		return self.OperationDone

	# Allow a machine to say to an activity that it finished an operation
	def terminateOperation(self, operation):
		# Remove the operation from the list of the operations yet to be done
		self.OperationsToBeDone = list(
			filter(lambda element: element.idOperation != operation.idOperation, self.OperationsToBeDone))
		# Append the operation to the list of the operations already done
		self.OperationDone = operation
		self.Test.activityIsDone(self)

	@property
	def shopTime(self):
		return self.operationDone.duration if self.isDone else max(self.OperationsToBeDone,
																	 key=lambda operation: operation.duration)

	@property
	def isPending(self):
		return len(list(filter(lambda element: element.isPending, self.OperationsToBeDone))) > 0

	def getOperation(self, idOperation):
		for operation in self.OperationsToBeDone:
			if operation.idOperation == idOperation:
				return operation
