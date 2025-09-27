# ColoState OpenMP Test Runner (omprun)
A python module designed to automate testing for OpenMP programs.
Tested using python 3.11 and 3.12.

## Installation
omprun can be installed using pip:
```
pip install git+https://github.com/jschott515/colostate-omprun.git
python3.11 -m pip install git+https://github.com/jschott515/colostate-omprun.git
```

# Tools
## `omprun`
Runs a series of trials using the provided test command. Has command line options to set the following:
* Range of threads to test
* Number of repetitions per thread
* Taskset mask
* Regular expression to parse result time from command output
* Output directory for results .csv files
* Optional brief description of test

### Basic Usage
- `omprun "./bin/PolyMultDCK.time-par 65535 128" --threads 1:8 --info "Testing my program!"`

Produces `omprun_09262025_194521.csv`
```
# Command: `./bin/PolyMultDCK.time-par 65535 128`
# Brief: Testing my program!
Threads,Time
1,0.02547157142857143
2,0.015355571428571428
3,0.011438857142857141
4,0.009935285714285714
5,0.00871457142857143
6,0.00854542857142857
7,0.008761
8,0.009985142857142857
```

For help:
- `omprun --help`
