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

### Basic Usage
- `omprun "<Test Command>"`

For help:
- `omprun --help`
