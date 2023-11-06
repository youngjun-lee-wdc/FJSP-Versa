class Operation:
	def __init__(self, idOperation, idDut, duration):
		self.IdOperation = idOperation
		self.Duration = duration
		self.IdDut = idDut
		self.Time = None
		self.IsPending = False
		self.PlaceOfArrival = None

	# Display the operation nicer
	def __str__(self):
		output = "Operation n°" + str(self.IdOperation) + " -> Dut: " + str(
			self.IdDut) + ", Duration: " + str(self.Duration)

		if not (self.Time is None):
			output += ", Started at time " + str(self.Time)

		return output

	# Return the operation's id
	@property
	def idOperation(self):
		return self.IdOperation

	# Return if an operation is done at time t
	def isDone(self, t):
		return not (self.Time is None) and self.Time + self.Duration <= t

	# Return if a dut is already treating the operation
	@property
	def isPending(self):
		return self.IsPending

	# Set the pending status
	@isPending.setter
	def isPending(self, value):
		self.IsPending = value

	# Return the slot of the dut allocated for the treatment of the operation
	@property
	def placeOfArrival(self):
		return self.PlaceOfArrival

	# Set the slot of the dut allocated for the treatment of the operation
	@placeOfArrival.setter
	def placeOfArrival(self, value):
		self.PlaceOfArrival = value

	# Return the dut's id who has to do the operation
	@property
	def idDut(self):
		return self.IdDut

	# Return the operation's duration
	@property
	def duration(self):
		return self.Duration

	# Return at which time the operation started or None
	@property
	def time(self):
		return self.Time

	# Set the time at which the operation started
	@time.setter
	def time(self, value):
		if value < 0:
			raise ValueError("Time < 0 is not possible")
		self.Time = value
