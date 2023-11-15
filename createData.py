import json
import csv
from typing import TypedDict, Mapping, Any
from itertools import chain


class DUT(TypedDict):
    TypeAndCapacity: str
    Ids: list[str]



import csv
from itertools import chain

class DataProcessor:
    def __init__(self, testPlanFile):
        self.testPlanFile = testPlanFile
        self.duts = {}
        self.tests = []
        self.vms = {}

    def __str__(self):
        return f"Duts: {self.duts}\nTests: {self.tests}\nVms: {self.vms}"

    def getDuts(self):
        return self.duts
    
    def getTests(self):
        return self.tests

    def getVms(self):
        return self.vms

    def processDuts(self, line):
        parent = line['parent']

        if line['Type'] == 'DUT':
            if parent not in self.duts:
                self.duts[parent] = {}
            
            textParts = line['text'].split(" - ")
            typeAndCapacity = textParts[0] + '_' + textParts[1]

            if typeAndCapacity not in self.duts[parent]:
                self.duts[parent][typeAndCapacity] = [line['id']]
            else:
                self.duts[parent][typeAndCapacity].append(line['id'])

    def processVMs(self, line):
        parent = line['parent']

        if line['Type'] == 'VM':
            duration = line['max_duration']
            parent = line['parent']
            print(line)
            self.tests.append(line['id'])

            if parent in self.duts:
                for dut in self.duts[parent]:
                    if dut in line['text']:
                        self.duts[parent][dut].append(line['id'])
                        break
        
        if line['Type'] == 'VM' and parent not in self.duts:
            self.vms[parent] = line['id']

    def generateOutputFiles(self):
        for idx, server in enumerate(self.duts):
            availableDuts = list(chain(*self.duts[server].values()))
            print(availableDuts)

            with open(f"data/GenData{idx + 1}.fjs", 'w') as file:
                file.write(str(len(availableDuts)))
                file.write('\n')
                file.write('\n'.join(availableDuts))

    def processTestPlan(self):
        with open(self.testPlanFile) as file:
            csvFile = csv.DictReader(file)

            for line in csvFile:
                self.processDuts(line)
                self.processVMs(line)


if __name__ == "__main__":
    testPlanFilePath = "path/to/your/test_plan.csv"
    dataProcessor = DataProcessor(testPlanFilePath)
    dataProcessor.processTestPlan()
    dataProcessor.generateOutputFiles()
