# BLIPSS
Breakthrough Listen Investigation for Periodic Spectral Signals (BLIPSS) is a software pipeline that utilizes the Fast Folding Algorithm (FFA) in [`riptide-ffa`](https://github.com/v-morello/riptide) to search for channel-wide periodic signals in radio dynamic spectra.

---

## Table of Contents
- [Package dependencies](#dependencies)
- [Installation](#installation)
- [Repository Organization](#organization)
- [Functionalities and Usage](#usage)
    - [blipss.py](#blipss_exec)
    - [inject_signal.py](#injectsignal)
    - [simulate_data.py](#simulatedata)
    - ON vs. OFF comparison (under development)
    - Final summary plots (under development)
- [Troubleshooting](#troubleshooting)

## Package Dependencies <a name="dependencies"></a>
```blipss``` is written in Python 3.8.5, and has the following package dependencies.
- astropy >= 4.0
- [`blimpy`](https://github.com/UCBerkeleySETI/blimpy) >= 2.0.0
- matplotlib >= 3.1.0
- mpi4py >= 3.1.1
- numpy >= 1.18.1
- pandas >= 1.3.4
- [`riptide-ffa`](https://github.com/v-morello/riptide) >= 0.2.3
- scipy >= 1.6.0
- tqdm >= 4.32.1

## Installation <a name="installation"></a>
1. Clone this repository to your local machine. To do so, execute the following at the command line.
```
git clone git@github.com:UCBerkeleySETI/blipss.git
```
2. Verify that your local Python 3 installation satisfies all dependencies of ```blipss```. If not, either manually install the missing dependencies or run the below calls.
```
cd blipss
pip install pybind11
python setup.py install
python setup.py clean
```
Note: `pybind11` is a prerequisite for installing [`riptide-ffa`](https://github.com/v-morello/riptide).

## Repository Organization <a name="organization"></a>
The repository is organized as two major folders, which are: <br>
1. `config`: A folder containing sample input configuration scripts for various use cases <br>
2. `executables`: Primary executable files for different tasks. Unless absolutely required, avoid editing executable scripts to ensure smooth operation. <br> <br>

For every functionality (say `inject_signal.py`), you will find relevant configuration scripts and executable files under the `config` and `executables` folders respectively. <br> <br>

To run an executable file, use the `-i` flag to supply its companion configuration script in the command line. For example, if you are running a command line terminal from the ``blipss`` repository, initiate an instance of ``inject_signal.py`` using:
```
python executables/inject_signal.py -i config/inject_signal.cfg
```
Comments at the top of every executable file provide program execution syntax.

## Functionalities and Usage <a name="usage"></a>
The BLIPSS pipeline currently has three chief exectutable files, which are:
1. ``blipss.py`` <a name="blipss_exec"></a> <br>
The `blipss.py` file executes channel-wise FFA on input data files (filterbank or hdf5), identifies harmonics of detected periods, and outputs a .csv file of candidates. Here is a schematic of the `blipss.py` workflow. <br>

![BLIPSS workflow (Jan 27, 2022)](https://github.com/akshaysuresh1/blipss/blob/main/images/blipss_design_2022Jan27.png?raw=True)

Columns in the output .csv file include 'Channel', 'Radio frequency (MHz)', 'Bins', 'Best width', 'Period (s)', 'S/N', and 'Harmonic flag'. <br>

The current implementation takes about 35 min. to run on a single mid-resolution filterbank product (1.07 s sampling, 2.86 kHz, 1703936 channels). For processing multiple input files in parallel, enable MPI via:
```
mpiexec -n <nproc> python -m mpi4py blipss.py -i <Configuration script of inputs> | tee <Log file>
```

---

2. ``inject_signal.py``: <a name="injectsignal"></a>
Inject one or more channel-wide periodic signals into a real-world data set. Fake periodic signals are assumed to have a boxcar single pulse shape with uniform pulse amplitude distribution.<br>

Execution syntax:
```
python inject_signal.py -i <Configuration script of inputs> | tee <Log file>
```

---

3. ``simulate_data.py``: <a name="simulatedata"></a>
Build an artificial data set with one or more channel-wide periodic signals superposed on normally distributed, white noise background. Again, the injected fake periodic signals have boxcar single pulse shapes and uniform pulse amplitude distributions.

Execution syntax:
```
python simulate_data.py -i <Configuration script of inputs> | tee <Log file>
```

## Troubleshooting <a name="troubleshooting"></a>
Please submit an issue to voice any problems or requests.

Improvements to the code are always welcome.
