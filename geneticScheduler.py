import copy
import sys
import random

from heuristics import Heuristics

from deap import base
from deap import creator

from scheduler import Scheduler

from colorama import init
from termcolor import colored


class GeneticScheduler:
    '''Genetic Scheduler class '''

    def __init__(self, duts, tests):
        init()  # Init colorama for color display
        self.OriginalStdout = sys.stdout
        self.Toolbox = base.Toolbox()
        self.Duts = duts
        self.Tests = tests

    # Constraint order
    @staticmethod
    def constraintOrderRespected(individual):
        list = [(activity.idTest, activity.idActivity)
                for (activity, _) in individual]
        for key, (idTest, idActivity) in enumerate(list):
            if idActivity == 1:
                continue
            elif not list.index((idTest, idActivity - 1)) < key:
                return False
        return True

    # Initialize an individual for the genetic algorithm
    def initIndividual(self, indClass, size):
        tempTestsList = copy.deepcopy(self.Tests)
        tempDutsList = copy.deepcopy(self.Duts)

        # Run the scheduler
        s = Scheduler(tempDutsList, 1, tempTestsList)
        s.run(Heuristics.randomOperationChoice, verbose=False)

        # Retriving all the activities and the operation done
        listActivities = []
        for tempTest in tempTestsList:
            for tempActivity in tempTest.activitiesDone:
                activity = self.Tests[tempActivity.idTest -
                                      1].getActivity(tempActivity.idActivity)
                operation = activity.getOperation(
                    tempActivity.operationDone.idOperation)
                listActivities.append(
                    (tempActivity.operationDone.time, activity, operation))
        # Ordering activities by time
        listActivities = sorted(listActivities, key=lambda x: x[0])
        individual = [(activity, operation)
                      for (_, activity, operation) in listActivities]
        del tempTestsList, tempDutsList
        return indClass(individual)

    # Initialize a population
    def initPopulation(self, totalPopulation):
        return [self.Toolbox.individual() for _ in range(totalPopulation)]

    # Compute the time an individual take
    def computeTime(self, individual):
        # List matching the activities to the time it takes place
        listTime = []
        # Operation schedule on duts indexed by duts' id
        schedule = {}
        for dut in self.Duts:
            schedule.update({dut.idDut: []})
        # Operation done indexed by test's id
        operationsDone = {}
        for test in self.Tests:
            operationsDone.update({test.idTest: []})

        # For each item in individual, we compute the actual time at which the operation considered start
        for activity, operation in individual:
            # Get at which time the previous operation is done
            timeLastOperation, lastOperationTest = operationsDone.get(activity.idTest)[-1] if len(
                operationsDone.get(activity.idTest)) > 0 else (0, None)
            timeLastDut, lastOperationDut = schedule.get(operation.idDut)[-1] if len(
                schedule.get(operation.idDut)) > 0 else (0, None)

            if lastOperationDut is None and lastOperationTest is None:
                time = 0
            elif lastOperationDut is None:
                time = timeLastOperation + lastOperationTest.duration
            elif lastOperationTest is None:
                time = timeLastDut + lastOperationDut.duration
            else:
                time = max(timeLastDut + lastOperationDut.duration,
                           timeLastOperation + lastOperationTest.duration)

            listTime.append(time)

            operationsDone.update({activity.idTest: operationsDone.get(
                activity.idTest) + [(time, operation)]})
            schedule.update({operation.idDut: schedule.get(
                operation.idDut) + [(time, operation)]})

        # We compute the total time we need to process all the tests
        totalTime = 0
        for dut in self.Duts:
            if len(schedule.get(dut.idDut)) > 0:
                time, operation = schedule.get(dut.idDut)[-1]
                if time + operation.duration > totalTime:
                    totalTime = time + operation.duration

        return totalTime, listTime

    # Evaluate the fitness for an individual, in our case it means compute the total time an individual take
    def evaluateIndividual(self, individual):
        return self.computeTime(individual)[0],

    # Create a mutant based on an individual
    # In our case it means select another operation within an activity with multiple choices for an operation
    @staticmethod
    def mutateIndividual(individual):
        # Select the possible candidates, meaning the activities with multiple choices for an operation
        candidates = list(filter(lambda element: len(
            element[0].nextOperations) > 1, individual))
        # If some candidates have been found, mutate a random one
        if len(candidates) > 0:
            mutantActivity, previousOperation = candidates[random.randint(
                0, len(candidates) - 1)]
            idMutantActivity = [element[0]
                                for element in individual].index(mutantActivity)
            mutantOperation = previousOperation
            while mutantOperation.idOperation == previousOperation.idOperation:
                mutantOperation = mutantActivity.nextOperations[
                    random.randint(0, len(mutantActivity.nextOperations) - 1)]
            individual[idMutantActivity] = (mutantActivity, mutantOperation)
        # Remove the previous fitness value because it is deprecated
        del individual.fitness.values
        # Return the mutant
        return individual

    # Permute an individual
    # In our case it means select an activity and permute it with another
    # It needs to meet some constraint to be efficient:
    # You can't move an activity before or after another one from the same test
    @staticmethod
    def computeBounds(permutation, consideredIndex):
        consideredActivity, _ = permutation[consideredIndex]
        minIndex = key = 0
        maxIndex = len(permutation) - 1
        while key < maxIndex:
            activity, _ = permutation[key]
            if activity.idTest == consideredActivity.idTest:
                if minIndex < key < consideredIndex:
                    minIndex = key
                if consideredIndex < key < maxIndex:
                    maxIndex = key
            key += 1
        return minIndex, maxIndex

    def permuteIndividual(self, individual):
        permutationPossible = False
        consideredIndex = consideredPermutationIndex = 0
        while not permutationPossible:
            consideredIndex = minIndex = maxIndex = 0
            # Loop until we can make some moves, i.e. when maxIndex - minIndex > 2
            while maxIndex - minIndex <= 2:
                consideredIndex = random.randint(0, len(individual) - 1)
                minIndex, maxIndex = self.computeBounds(
                    individual, consideredIndex)

            # Select a random activity within those bounds (excluded) to permute with
            consideredPermutationIndex = random.randint(
                minIndex + 1, maxIndex - 1)
            minIndexPermutation, maxIndexPermutation = self.computeBounds(individual,
                                                                          consideredPermutationIndex)
            if minIndexPermutation < consideredIndex < maxIndexPermutation:
                permutationPossible = consideredIndex != consideredPermutationIndex

        # A possible permutation has been found
        individual[consideredIndex], individual[consideredPermutationIndex] = individual[
            consideredPermutationIndex], \
            individual[consideredIndex]
        return individual

    # Move an activity inside the scheduler (different than swapping)
    def moveIndividual(self, individual):
        consideredIndex = minIndex = maxIndex = 0
        # Loop until we can make some moves, i.e. when maxIndex - minIndex > 2
        while maxIndex - minIndex <= 2:
            # print(individual)
            consideredIndex = random.randint(0, len(individual) - 1)
            minIndex, maxIndex = self.computeBounds(
                individual, consideredIndex)
        # Loop until we find a different index to move to
        newIndex = random.randint(minIndex + 1, maxIndex - 1)
        while consideredIndex == newIndex:
            newIndex = random.randint(minIndex + 1, maxIndex - 1)
        # Move the activity inside the scheduler
        individual.insert(newIndex, individual.pop(consideredIndex))
        return individual

    def evolveIndividual(self, individual, mutationProbability, permutationProbability, moveProbability):
        # print(individual)
        futureIndividual = copy.deepcopy(individual)
        if random.randint(0, 100) < mutationProbability:
            futureIndividual = self.mutateIndividual(futureIndividual)
        if random.randint(0, 100) < permutationProbability:
            futureIndividual = self.permuteIndividual(futureIndividual)
        if random.randint(0, 100) < moveProbability:
            # print(futureIndividual)
            futureIndividual = self.moveIndividual(futureIndividual)

        return futureIndividual

    # Run a tournament between individuals within a population to get some of them
    @staticmethod
    def runTournament(population, total=10):
        # Because you can't have a bigger population as a result of the tournament, we assert that constraint
        assert total <= len(population)
        newPopulation = []
        while len(newPopulation) < total:
            firstIndividual = population[random.randint(
                0, len(population) - 1)]
            secondIndividual = population[random.randint(
                0, len(population) - 1)]
            if firstIndividual.fitness.values[0] < secondIndividual.fitness.values[0]:
                newPopulation.append(firstIndividual)
                population.remove(firstIndividual)
            else:
                newPopulation.append(secondIndividual)
                population.remove(secondIndividual)
        del population
        return newPopulation

    # Simulate the individual with the duts
    def runSimulation(self, individual):
        totalTime, listTime = self.computeTime(individual)
        for key, (individualActivity, individualOperation) in enumerate(individual):
            activity = self.Tests[individualActivity.idTest -
                                  1].getActivity(individualActivity.idActivity)
            operation = activity.getOperation(individualOperation.idOperation)
            operation.time = listTime[key]
            operation.placeOfArrival = 0
            activity.terminateOperation(operation)
        return totalTime

    # Run the genetic scheduler
    def runGenetic(self, totalPopulation=10, maxGeneration=100, verbose=False):
        assert totalPopulation > 0, maxGeneration > 0
        # Disable print if verbose is False
        if not verbose:
            sys.stdout = None

        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.Toolbox.register(
            "individual", self.initIndividual, creator.Individual, size=1)
        self.Toolbox.register("mutate", self.mutateIndividual)
        self.Toolbox.register("permute", self.permuteIndividual)
        self.Toolbox.register("evaluate", self.evaluateIndividual)

        print(colored("[GENETIC]", "cyan"), "Generating population")
        population = self.initPopulation(totalPopulation)
        best = population[0]
        best.fitness.values = self.evaluateIndividual(best)

        print(colored("[GENETIC]", "cyan"),
              "Starting evolution for", maxGeneration, "generations")
        for currentGeneration in range(maxGeneration):
            # Generate mutation and permutation probabilities for the next generation
            mutationProbability = random.randint(0, 100)
            permutationProbability = random.randint(0, 100)
            moveProbability = random.randint(0, 100)
            # Evolve the population
            print(colored("[GENETIC]", "cyan"),
                  "Evolving to generation", currentGeneration + 1)
            mutants = list(set([random.randint(0, totalPopulation - 1) for _ in
                                range(random.randint(1, totalPopulation))]))
            print(colored("[GENETIC]", "cyan"), "For this generation,", len(
                mutants), "individual(s) will mutate")
            for key in mutants:
                individual = population[key]
                population.append(
                    self.evolveIndividual(individual, mutationProbability, permutationProbability, moveProbability))
            # Evaluate the entire population
            fitnesses = list(map(self.evaluateIndividual, population))
            for ind, fit in zip(population, fitnesses):
                ind.fitness.values = fit
                if best.fitness.values[0] > ind.fitness.values[0]:
                    print(colored("[GENETIC]", "cyan"), "A better individual has been found. New best time = ",
                          ind.fitness.values[0])
                    best = copy.deepcopy(ind)
            population = self.runTournament(population, total=totalPopulation)

        print(colored("[GENETIC]", "cyan"), "Evolution finished")
        if self.constraintOrderRespected(best):
            print(colored("[GENETIC]", "cyan"),
                  "Best time found equals", best.fitness.values[0])
            print(colored("[GENETIC]", "cyan"), "Simulating work on duts")
            totalTime = self.runSimulation(best)
            print(colored("[GENETIC]", "cyan"), "Simulation finished")
            print(colored("[GENETIC]", "cyan"), "Genetic scheduler finished")
        else:
            print(colored("[GENETIC]", "cyan"),
                  "The individual doesn't match the constraint order")

        # Reenable stdout
        if not verbose:
            sys.stdout = self.OriginalStdout

        return totalTime
