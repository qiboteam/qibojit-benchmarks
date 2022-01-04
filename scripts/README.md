# Example scripts

This folder contains example bash scripts that execute the `compare.py` benchmark for different circuit configurations and different libraries.
The provided scripts are the following:

### `circuit_cpu.sh`

Executes benchmarks for some of the circuits presented in Table 1 of the [HyQuas paper](https://dl.acm.org/doi/pdf/10.1145/3447818.3460357).
All circuits are executed with default options using the CPU libraries implemented in this repository i.e. Qibo, Qiskit, Qsim, Qulacs, ProjectQ and HybridQ.
Options:
 - ``filename``: where to store the logs (default: ``circuits_cpu.dat``)
 - ``precision``: ``single`` or ``double`` (default: ``double``)
 - ``nreps``: number of repetitions for each circuit (default: 20)
 - ``nqubits``: number of qubits for each circuit (default: 30)

### `circuit_gpu.sh`

Same as ``circuit_cpu.sh``, but using the GPU libraries implemented in this repository i.e. Qiskit, Qsim(+cuQuantum), Qulacs and QCGPU.

### `qibo_scaling_cpu.sh`

Executes a specific circuit with different size and different qibo CPU backends.
Options:
 - ``filename``: where to store the logs (default: ``qibo_scaling_cpu.dat``)
 - ``circuit``: the circuit to execute (default: ``qft``)
 - ``precision``: ``single`` or ``double`` (default: ``double``)
 - ``nreps``: number of repetitions for each circuit (default: 20)
 - ``min_qubits``: size of the smallest circuit to run (default: 3)
 - ``max_qubits``: size of the largest circuit to run (default: 30)

### `qibo_scaling_gpu.sh`

Same as ``qibo_scaling_cpu.sh``, but uses the GPU backends i.e. TensorFlow, Qibotf and Qibojit.

### ``qibojit_gpu.sh``
Similar to ``qibo_scaling_gpu.sh``, but uses only qibojit on GPU. Useful to compare the performance across different GPUs.

