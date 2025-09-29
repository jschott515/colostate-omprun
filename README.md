# ColoState OpenMP Test Utilities (omprun/splot)
A python module designed to automate testing for OpenMP programs.
Tested using python 3.11 and 3.12.

## Installation
omprun can be installed using pip:
```
pip install git+https://github.com/jschott515/colostate-omprun.git
python3.11 -m pip install git+https://github.com/jschott515/colostate-omprun.git
```

# Tools
## OpenMP Runner `omprun`
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
1,0.28424185714285716
2,0.151376
3,0.10371257142857145
4,0.07669871428571429
5,0.06335714285714286
6,0.05276642857142858
7,0.04689285714285713
8,0.038781857142857146
```

For help:
- `omprun --help`

## Speedup Plotter `splot`
Plots the speedup of a program from a '.csv' and saves the figure as a '.png'.

### Basic Usage
- `splot "results/omprun_09262025_194521.csv"`

(Produces `omprun_09262025_194521.png`)
![image](/docs/examples/omprun_09262025_194521.png)

For help:
- `splot --help`

### Experimental 'Recursive' Mode
- `splot "results/" -r`

(Produces figures for all '.csv' files under `results/`)
