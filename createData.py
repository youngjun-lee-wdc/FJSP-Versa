import json
import csv
from typing import TypedDict, Mapping, Any


class DUT(TypedDict):
    TypeAndCapacity: str


def getDuts(testPlan: str):

    with open(testPlan) as file:
        csvFile = csv.DictReader(file)
        duts = {}

        '''
          DUTs are formatted as 
            {
                Server:
                    {
                        Type + Capacity: {
                            ...,
                            ...,
                            ...,
                        }
                    }
            }
        '''

        for line in csvFile:
            parent = line['parent']
            # get list of all rows where the type is "DUT"
            if line['Type'] == 'DUT':
                if parent not in duts:
                    duts[parent] = {}
                # duts.get(parent, {parent: {}})
                # print(duts)
                text = line['text'].split(" - ")
                typeAndCapacity = text[0] + '_' + text[1]
                if typeAndCapacity not in duts[parent]:
                    duts[parent][typeAndCapacity] = [line['id']]
                else:
                    duts[parent][typeAndCapacity].append(line['id'])
            elif line['Type'] == 'VM':
                duration = line['max_duration']
                print(duration)
                parent = line['parent']

        print(duts)
        for idx, server in enumerate(duts):
            # print(idx)
            print(server)
            with open("data/GenData" + str(idx + 1) + ".fjs", 'w') as file:
                file.write(str(len(server)))
                file.write("  2")
                file.write("  5")
    # with open('GanttTasksTestClean.csv') as file:
        # csvFile = csv.DictReader(file)
        # for line in csvFile:
            # parent = line['parent']
            # if line['Type'] == 'VM':
                # duration  = line['max_duration']
                # print(line)
                # print(duts[parent].keys())
                # altMachines = len(duts[parent])
                # print(altMachines)
        return duts


TESTPLAN = 'TestsData.csv'
getDuts(TESTPLAN)
