import sys
from dataParser import parse


if len(sys.argv) == 1:
    path = "data/test.fjs"
else:
    path = sys.argv[1]

tests_list, duts_list, number_max_operations = parse(path)
# parse(path)
number_total_duts = len(duts_list)
number_total_tests = len(tests_list)

# print(number_total_duts)
# print(duts_list[0].id_machine)