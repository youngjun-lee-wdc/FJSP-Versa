# FJSP-Versa

Flexible job shop problem algorithm solved using genetic algorithm approach for scheduling and automating management of test cases. 

## Usage

```bash
python main.py /path/to/file
```
If /path/to/file is omitted, the default value is set to data/test.fjs

## Test Data Format
test.fjs  
```
3   3   1
3   2   a   4   b   3   1   c   2   1   a   2
3   1   b   2   1   c   1   1   b   4
2   1   a   4   1   b   3
```

The first row is always reserved for test overview.
- First number represents the total number of test suites to be executed
- Second number represents the total number of DUTS available
- Third number represents the average number of machines per test in a test suite.

Every subsequent row represents a test suite. 
- First number of a row always represents the total number of tests in the test suite
- Every grouping thereafter represents a test.
  - The first number in a grouping represents the number of DUTS that can be used for the test
  - The second number in a grouping represents the ID of the DUT
  - The third number in a group represents the unit of time it takes to complete the test.
  - Eg. In test suite 1 above, 3 tests are to be completed:
    - The first test can be processed by 2 alternate DUTS (a and b) taking 4 and 3 units of time respectively.
    - The second test can be processed by 1 DUT (c) an takes 2 units of time.
    - The third test can be processed by 1 DUT (a) and takes 2 units of time. 
