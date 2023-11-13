class Heuristics:
    # Assign randomly tests to dut
    @staticmethod
    def randomOperationChoice(testsToBeDone, maxOperations, _):
        import random
        bestCandidates = {}
        dictOperations = {}

        for test in testsToBeDone:
            currentActivity = test.currentActivity
            for operation in currentActivity.nextOperations:
                if dictOperations.get(operation.idDut) is None:
                    dictOperations.update(
                        {operation.idDut: [(currentActivity, operation)]})
                else:
                    dictOperations.get(operation.idDut).append(
                        (currentActivity, operation))

        for dut, listOperations in dictOperations.items():
            bestCandidates.update({dut: list(
                set([listOperations[random.randint(0, len(listOperations) - 1)] for _ in range(maxOperations)]))})
        return bestCandidates
