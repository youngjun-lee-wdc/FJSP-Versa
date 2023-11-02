# FJSP-Versa

Flexible job shop problem algorithm solved using genetic algorithm approach for scheduling and automating management of test cases. 

## Test Data Format
test.fjs  
```
3   3   1
3   2   a   4   b   3   1   c   2   1   a   2
3   1   b   2   1   c   1   1   b   4
2   1   a   4   1   b   3
```

The first row is reserved for test overview.
- 1st number represents the total number of test suites to be executed.
- 2nd number represents the total number of DUTs available.
- 3rd number represents the avg number of machines per in a test suite.

Every subsequent row represents a test suite.
- 1st number of a row always represents the total number of tests in the test suite.
- Every grouping thereafter represents a test.
  - 1st number in a  grouping represents the number of alt DUTs that can be used for the test.
  - 2nd number in a grouping represents the ID of the DUT.
  - 3rd number in a grouping represents the unit of time it takes to complete the test.
  - Example: In test suite 1 above, 3 tests are to be completed:
    - 1st test can be processed by 2 alt DUTs (a,b) taking 4 and 3 units of time respectively.
    - 2nd test can be processed by 1 DUT (c) and takes 2 units of time.
    - 3rd test can be processed by 1 DUT (a) and takes 2 units of time.

## Usage

```bash
python main.py /path/to/file
```
If /path/to/file is omitted, the default value is set to data/test.fjs

