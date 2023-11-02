class Test:
	def __init__(self, idTest):
		self.__idTest = idTest
		self.__activitiesToBeDone = []
		self.__activitiesDone = []

	# Display the test nicer
	def __str__(self):
		output = ""

		for activity in self.__activitiesToBeDone:
			output += str(activity) + "\n"

		for activity in self.__activitiesDone:
			output += str(activity) + "\n"

		return output

	# Return the test's id
	@property
	def idTest(self):
		return self.__idTest

	# Add an activity to the test
	def addActivity(self, activity):
		self.__activitiesToBeDone.append(activity)

	# Return if the test is done
	@property
	def isDone(self):
		return len(self.activitiesDone) == 0

	# Return the activities yet to be done
	@property
	def activitiesToBeDone(self):
		return self.__activitiesToBeDone

	# Return the activities already done
	@property
	def activitiesDone(self):
		return self.__activitiesDone

	# Method an activity calls to signal it's done
	def activityIsDone(self, activity):
		if not activity.isDone:
			raise EnvironmentError("This activity is not done")
		self.__activitiesToBeDone = list(
			filter(lambda element: element.idActivity != activity.idActivity, self.__activitiesToBeDone))
		self.__activitiesDone.append(activity)

	# Return the current activity that need to be processe
	@property
	def currentActivity(self):
		if len(self.activitiesToBeDone) == 0:
			raise EnvironmentError("All activities are already done")
		return self.__activitiesToBeDone[0]

	@property
	def remainingShopTime(self):
		return sum(map(lambda activity: activity.shopTime, self.activitiesToBeDone))

	@property
	def totalShopTime(self):
		return sum(map(lambda activity: activity.shopTime, self.activitiesToBeDone + self.activitiesDone))

	def checkIfPreviousActivityIsDone(self, activityId):
		if activityId == 1:
			return True
		for activity in self.__activitiesDone:
			if activity.idActivity == activityId - 1:
				return True
		return False

	def getActivity(self, idActivity):
		for activity in self.__activitiesToBeDone:
			if activity.idActivity == idActivity:
				return activity
