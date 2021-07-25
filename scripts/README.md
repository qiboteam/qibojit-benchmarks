# Example scripts

This folder contains example bash scripts that execute the `main.py` benchmark for different circuit configurations and qubit numbers. The provided scripts are the following:

### `qftcpu.sh`

Executes Quantum Fourier Transform benchmarks on CPU from 3 to 30 qubits with and without the `--transfer` flag using the qibojit and qibotf backends. Twenty repetitions are used for up to 25 qubits and a single repetition for more qubits.

### `qftgpu.sh`

Executes Quantum Fourier Transform benchmarks on GPU from 3 to 30 qubits with and without the `--transfer` flag using the qibojit and qibotf backends. Twenty repetitions are used for up to 25 qubits and five repetitions for more qubits.

### `circuits.sh`

Executes benchmarks for the circuits presented in Table 1 of the [HyQuas paper](https://dl.acm.org/doi/pdf/10.1145/3447818.3460357).

The qft, bernstein-vazirani, supremacy, basis-change and quantum-volume circuits are executed with default options. The hidden-shift circuit is executed for the random bitstrings written in the `graphs/random_bitstrings.dat` file. The MaxCut QAOA circuit is executed for the random graphs written in the json files under `graphs/`.

All circuits are executed using the qibojit and qibotf backends with the `--transfer` flag for 3 to 30 qubits on GPU and 3 to 25 qubits on CPU. Note that the QAOA circuit is only executed for even qubit numbers.
