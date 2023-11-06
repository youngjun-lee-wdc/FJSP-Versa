class Dut:
	def __init__(self, idDut: str, maxOperations: int):
		self.IdDut = idDut
		self.IsWorking = False
		self.OperationsDone = []
		self.ProcessedOperations = []
		self.MaxOperations = maxOperations
		self.CurrentTime = 0
		self.AvailablePlaces = [i for i in range(maxOperations)]

	# Return the machine's id
	@property
	def idDut(self):
		return self.IdDut

	# Return the operations done by the machine
	@property
	def operationsDone(self):
		return self.OperationsDone

	# Return if the machine is working at max capacity
	def isWorkingAtMaxCapacity(self):
		return len(self.ProcessedOperations) == self.MaxOperations

	# Add an operation to the treatment list of the machine
	def addOperation(self, activity, operation):
		if self.isWorkingAtMaxCapacity():
			raise EnvironmentError("Dut already working at max capacity")
		if operation.idDut != self.IdDut:
			raise EnvironmentError("Operation assigned to the wrong machine")

		operation.time = self.CurrentTime
		operation.isPending = True
		operation.placeOfArrival = self.AvailablePlaces.pop(0)

		self.ProcessedOperations.append((activity, operation))

	# Method to simulate a work process during one unit of time
	def work(self):
		self.CurrentTime += 1
		for activity, operation in self.ProcessedOperations:
			if operation.time + operation.duration <= self.CurrentTime:
				self.ProcessedOperations = list(filter(lambda element: not (
						element[0].idTest == activity.idTest and element[0].idActivity == activity.idActivity and
						element[1].idOperation == operation.idOperation), self.ProcessedOperations))
				self.AvailablePlaces.append(operation.placeOfArrival)
				activity.terminateOperation(operation)
				self.OperationsDone.append(operation)
