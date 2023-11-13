import sys

from colorama import init
from termcolor import colored


class Scheduler:
    def __init__(self, duts, maxOperations, tests):
        init()  # Init colorama for color display
        self.OriginalStdout = sys.stdout
        self.Duts = duts
        self.TestsToBeDone = tests
        self.TestsDone = []
        self.MaxOperations = maxOperations

    # Run the scheduler with an heuristic
    def run(self, heuristic, verbose=True):
        # Disable print if verbose is False
        if not verbose:
            sys.stdout = None

        currentStep = 0
        while len(self.TestsToBeDone) > 0:
            currentStep += 1

            bestCandidates = heuristic(
                self.TestsToBeDone, self.MaxOperations, currentStep)
            for idDut, candidates in bestCandidates.items():
                # raise ValueError(self.Duts)
                dutsList = [dut.idDut for dut in self.Duts]
                dutIdx = dutsList.index(idDut)
                dut = self.Duts[dutIdx]

                for activity, operation in candidates:
                    if not (dut.isWorkingAtMaxCapacity() or activity.isPending):
                        dut.addOperation(activity, operation)

            for dut in self.Duts:
                dut.work()

            for test in self.TestsToBeDone:
                if test.isDone:
                    self.TestsToBeDone = list(
                        filter(lambda element: element.idTest != test.idTest, self.TestsToBeDone))
                    self.TestsDone.append(test)
        print(colored("[SCHEDULER]", "green"), "Done in " +
              str(currentStep) + " units of time")

        # Reenable stdout
        if not verbose:
            sys.stdout = self.OriginalStdout

        return currentStep
