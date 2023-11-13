import random
import os


class Drawer:
	@staticmethod
	def drawSchedule(numberDuts, maxOperations, tests, filename=None):
		import matplotlib.pyplot as plt
		import matplotlib.patches as patches

		# Vertical space between operation
		verticalSpace = 1
		# Vertical height of an operation
		verticalHeight = 2

		# Dictionary of the operations done, the key correspond to the machine id
		operationsDone = {}
		for test in tests:
			for activity in test.activitiesDone:
				# Add all done operations
				operation = activity.operationDone
				# If it's the first operation add on the machine, initialize the list
				if operationsDone.get(operation.idDut) is None:
					listOperations = []
				# Else, get the previously added operations
				else:
					listOperations = operationsDone.get(operation.idDut)

				# Append the current operation with its job's id and activity's id
				listOperations.append((test.idTest, activity.idActivity, operation))
				# Update the dictionary
				operationsDone.update({operation.idDut: listOperations})

		# Define random colors for tests
		colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(len(tests))]

		# Draw
		plt.clf()
		plot = plt.subplot()

		for idDut, listOperations in operationsDone.items():
			for idTest, idActivity, operation in listOperations:
				# X coord corresponds to the operation's time
				# Y coord corresponds to the order of the operation
				# according to its machine's id, its place of arrival and the max operations allowed simultaneously
				dutsList = [dut for dut in operationsDone.keys()]
				idx = dutsList.index(idDut) + 1
				# dut = dutsList[idx]
				x, y = operation.time, 1 + idx * maxOperations * (
						verticalSpace + verticalHeight) + operation.placeOfArrival * (
							   verticalSpace + verticalHeight)
				# Plot a rectangle with a width of the operation's duration
				plot.add_patch(
					patches.Rectangle(
						(x, y),
						operation.duration,
						verticalHeight,
						facecolor=colors[idTest - 1]
					)
				)

		# Display the machines' number as the y-axis legend
		plt.yticks([1 + (i + 1) * maxOperations * (verticalSpace + verticalHeight) + (
				maxOperations * (verticalHeight + verticalSpace) - verticalSpace) / 2 for i in
					range(numberDuts)], ["Dut " + str(idDut) for idDut in operationsDone.keys()])
		# Auto-scale to see all the operations
		plot.autoscale()

		# Display a rectangle with the color and the job's id as the x-axis legend
		handles = []
		for idTest, color in enumerate(colors):
			handles.append(patches.Patch(color=color, label='Test ' + str(idTest + 1)))
		plt.legend(handles=handles)

		# Show the schedule order
		plt.show()
		# Saving the scheduler order
		if not (filename is None):
			plt.savefig(os.path.join("output", filename), bbox_inches='tight')
