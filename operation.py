class Operation:
	def __init__(self, idOperation: int, idDut: str, duration: int):
		self.__idOperation = idOperation
		self.__duration = duration
		self.__idDut = idDut
		self.__time = None
		self.__isPending = False
		self.__placeOfArrival = None

	# Display the operation nicer
	def __str__(self):
		output = "Operation # " + str(self.__idOperation) + " -> Dut: " + str(
			self.__idDut) + ", Duration: " + str(self.__duration)

		if not (self.__time is None):
			output += ", Started at time " + str(self.__time)

		return output

	# Return the operation's id
	@property
	def idOperation(self):
		return self.__idOperation

	# Return if an operation is done at time t
	def isDone(self, t):
		return not (self.__time is None) and self.__time + self.__duration <= t

	# Return if a machine is already treating the operation
	@property
	def isPending(self):
		return self.__isPending

	# Set the pending status
	@isPending.setter
	def isPending(self, value):
		self.__isPending = value

	# Return the slot of the machine allocated for the treatment of the operation
	@property
	def placeOfArrival(self):
		return self.__placeOfArrival

	# Set the slot of the machine allocated for the treatment of the operation
	@placeOfArrival.setter
	def placeOfArrival(self, value):
		self.__placeOfArrival = value

	# Return the machine's id who has to do the operation
	@property
	def idDut(self):
		return self.__idDut

	# Return the operation's duration
	@property
	def duration(self):
		return self.__duration

	# Return at which time the operation started or None
	@property
	def time(self):
		return self.__time

	# Set the time at which the operation started
	@time.setter
	def time(self, value):
		if value < 0:
			raise ValueError("Time < 0 is not possible")
		self.__time = value
