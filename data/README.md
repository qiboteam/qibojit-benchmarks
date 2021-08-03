# Example logs

This folder contains example logs saved when executing the `main.py` benchmarks for different circuit configurations and qubit numbers. For the bash scripts that generate these logs see the `scrips/` folder. In the `data.ipynb` notebook we load the results contained in the logs as pandas DataFrame's and we present them in markdown table format.

The following logs are given:

### `qibomachine_cpu_120721.sh`

Contains Quantum Fourier Transform benchmarks on CPU from 3 to 30 qubits with and without the `--transfer` flag using the qibojit and qibotf backends. Twenty repetitions are used for up to 25 qubits and a single repetition for more qubits.

### `qibomachine_gpu_120721.sh`

Contains Quantum Fourier Transform benchmarks on GPU from 3 to 30 qubits with and without the `--transfer` flag using the qibojit and qibotf backends. Twenty repetitions are used for up to 25 qubits and five repetitions for more qubits.

### `qibomachine_cpu_230721.sh` and `qibomachine_gpu_230721.sh`

Contains benchmark logs for the circuits presented in Table 1 of the [HyQuas paper](https://dl.acm.org/doi/pdf/10.1145/3447818.3460357). These are executed using the qibojit and qibotf backends with and without the `--transfer` flag for 3 to 30 qubits on GPU and 3 to 25 qubits on CPU.

### `qibomachine_cpu_withfile_240721.sh` and `qibomachine_gpu_withfile_240721.sh`

Contains benchmark logs for the hidden-shift and qaoa circuits. The hidden-shift circuit is executed for the random bitstrings written in the `graphs/random_bitstrings.dat` file. The MaxCut QAOA circuit is executed for the random graphs written in the json files under `graphs/`. The circuits are executed using the qibojit and qibotf backends for 3 to 30 qubits.
