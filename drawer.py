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

	# Plot a 2d graph
	@staticmethod
	# def drawSchedule(numberDuts, maxOperations, test, filename=None):
	def plot2d(filename, xdata, ydata, title, xlabel, ylabel, approximate=False, minDegree=2, maxDegree=8):
		import matplotlib.pyplot as plt
		plt.clf()
		plot = plt.subplot()
		plot.setTitle(title)
		plot.setXlabel(xlabel)
		plot.setYlabel(ylabel)
		plot.plot(xdata, ydata, 'o' if approximate else '-')
		
		if approximate:
			import numpy as np
			from scipy.interpolate import UnivariateSpline
			from colorama import init
			from termcolor import colored
			init()
			
			# Compute an interval of 150 points
			x = np.linspace(xdata[0], xdata[-1], 150)
			
			# Compute a spline to measure the error between the approximation and the data set
			spline = UnivariateSpline(xdata, ydata)
			ySpline = spline(x)
			plot.plot(x, ySpline, 'C0')
			
			# Compute different polynomial approximations
			legends = ["Original data", "Spline approximation"]
			# Save best polynomial approximation
			bestDegree = bestCoefficients = bestResidual = bestYPoly = None
			
			# Computing different polynomial approximations
			for degree in range(minDegree, maxDegree + 1):
				# Find a polynomial to fit the spline
				coefficients = np.polyfit(xdata, ydata, degree)
				poly = np.poly1d(coefficients)
				yPoly = poly(x)
				# Compute the residual (the error)
				residual = np.linalg.norm(ySpline - yPoly, 2)
				# Display current polynomial approximation residual
				print(colored("[DRAWER]", "magenta"), "Polynomial approximation of degree", str(degree),
					  "-> Residual =", residual)
				# Checking if it's a better approximation
				if bestResidual is None or residual < bestResidual:
					bestDegree, bestCoefficients, bestResidual, bestYPoly = degree, coefficients, residual, yPoly
					
			# Displaying best polynomial found
			legends.append("Approximation of degree " + str(bestDegree))
			print(colored("[DRAWER]", "magenta"), "Best approximation found is a polynomial of degree",
				  str(bestDegree))
			print("\t", "Coefficients:", bestCoefficients)
			print("\t", "Residual:", bestResidual)
			# Plotting resulting polynomial
			plot.plot(x, bestYPoly, '--')
			plot.legend(legends)
			
		plot.autoscale()
		plt.show()
		if not (filename is None):
			plt.savefig(os.path.join("output", filename), bbox_inches='tight')

	# Plot a 3d graph
	@staticmethod
	def plot3d(filename, xdata, ydata, zdata, title, xlabel, ylabel, zlabel):
		from mplToolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt

		plt.clf()
		fig = plt.figure()
		plot = fig.gca(projection='3d')
		plot.setTitle(title)
		plot.setXlabel(xlabel)
		plot.setYlabel(ylabel)
		plot.setZlabel(zlabel)
		plot.scatter(xdata, ydata, zdata, c='b', marker='o')
		plot.autoscale()
		plt.show()
		if not (filename is None):
			plt.savefig(os.path.join("output", filename), bbox_inches='tight')
