class Dut:
	def __init__(self, dutId: str, maxOperations: int):
		self.__dutId = dutId
		self.__isWorking = False
		self.__operationsDone = []
		self.__processedOperations = []
		self.__maxOperations = maxOperations
		self.__currentTime = 0
		self.__availablePlaces = [i for i in range(maxOperations)]

	# Return the machine's id
	@property
	def idDut(self):
		return self.__dutId

	# Return the operations done by the machine
	@property
	def operationsDone(self):
		return self.__operationsDone

	# Return if the machine is working at max capacity
	def isWorkingAtMaxCapacity(self):
		return len(self.__processedOperations) == self.__maxOperations

	# Add an operation to the treatment list of the machine
	def addOperation(self, activity, operation):
		if self.isWorkingAtMaxCapacity():
			raise EnvironmentError("Machine already working at max capacity")
		
		if operation.idDut != self.__dutId:
			raise EnvironmentError("Operation assigned to the wrong machine")

		operation.time = self.__currentTime
		operation.isPending = True
		operation.placeOfArrival = self.__availablePlaces.pop(0)

		self.__processedOperations.append((activity, operation))

	# Method to simulate a work process during one unit of time
	def work(self):
		self.__currentTime += 1
		for activity, operation in self.__processedOperations:
			if operation.time + operation.duration <= self.__currentTime:
				self.__processedOperations = list(filter(lambda element: not (
						element[0].idTest == activity.idTest and element[0].idActivity == activity.idActivity and
						element[1].idOperation == operation.idOperation), self.__processedOperations))
				self.__availablePlaces.append(operation.placeOfArrival)
				activity.terminateOperation(operation)
				self.__operationsDone.append(operation)
