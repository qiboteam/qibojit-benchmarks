# Benchmarking quantum simulation

This repository contains benchmark scripts for quantum circuit simulation using
[Qibo](https://github.com/qiboteam/qibo) and multiple simulation engines.

## Installing prerequisites

Before executing the simulation please:

1. Install `Qibo >= 0.1.6rc1` from source or using:
    ```
    pip install qibo --pre
    ```

2. Install `qibojit >= 0.0.2` simulation backend with:
    ```
    pip install qibojit
    ```
    Visit the [CuPy website](https://cupy.dev/) and install the binary/source code version that matches your CUDA version.

3. (optional) Install qibotf simulation backend with:
    ```
    pip install qibotf
    ```
    This will install TensorFlow 2.5.0 automatically, please make sure you have the supported CUDA version.

## Supported simulation backends

- [qibojit](https://github.com/qiboteam/qibojit): uses numba on CPU and cupy on GPU for custom operations.
- [qibotf](https://github.com/qiboteam/qibotf): uses tf primitives with custom operators on CPU and GPU.
- [tensorflow](https://www.tensorflow.org/): uses tf default primitives.
- [numpy](https://numpy.org/): single-threaded CPU implementation.

For more details check the documentation [here](https://qibo.readthedocs.io/en/latest/installation.html).

## Running the benchmarks

The script in `benchmarks/main.py` executes the benchmark code following the supported configuration flags (check `python main.py -h`):

```
$ python main.py -h

usage: main.py [-h] [--nqubits NQUBITS] [--backend BACKEND] [--circuit CIRCUIT]
               [--options OPTIONS] [--nreps NREPS] [--nshots NSHOTS] [--transfer]
               [--precision PRECISION] [--memory MEMORY] [--threading THREADING]
               [--filename FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --nqubits NQUBITS     Number of qubits in the circuit.
  --backend BACKEND     Qibo backend to use for simulation.
  --circuit CIRCUIT     Type of circuit to use. See README for the list of available circuits.
  --options OPTIONS     String with options for circuit creation. It should have the form
                        'arg1=value1,arg2=value2,...' .See README for the list of arguments
                        that are available for each circuit.
  --nreps NREPS         Number of repetitions of the circuit execution. Dry run is not
                        included.
  --nshots NSHOTS       Number of measurement shots. If used the time required to measure
                        frequencies (no samples) is measured and logged. If it is ``None`` no
                        measurements are performed.
  --transfer            If used the final state array is converted to numpy.If the simulation
                        device is GPU this requires a transfer from GPU memory to CPU.
  --precision PRECISION
                        Numerical precision of the simulation.Choose between 'double' and
                        'single'.
  --memory MEMORY       Limit the GPU memory usage when using Tensorflow based backends. The
                        memory limit should be given in MB. Tensorflow reserves the full
                        available memory by default.
  --threading THREADING
                        Switches the numba threading layer when using the qibojit backend on
                        CPU. See https://numba.pydata.org/numba-doc/latest/user/threading-
                        layer.html#selecting-a-named-threading-layer for a list of available
                        threading layers.
  --filename FILENAME   Directory of file to save the logs in json format.If not given the
                        logs only be printed and not saved.
```

Before executing the code keep in mind the following:
- GPUs are the default devices for qibojit and qibotf. If you need CPU performance numbers do `export CUDA_VISIBLES_DEVICE=""` before executing the benchmark script.
- CPU simulations by default use physical cores as number of threads with qibojit and qibotf. To control this behaviour without touching the code do `export OMP_NUM_THREADS=<threads>` (or `export NUMBA_NUM_THREADS=<threads>` for qibojit numba backend) before executing the benchmark script.
- The benchmark script provides several options, including the possibility to modify the default numba threading pooling technology, (see [docs](https://numba.pydata.org/numba-doc/latest/developer/threading_implementation.html#notes-on-numba-s-threading-implementation)) or limiting the GPU memory used be Tensorflow. See `python main.py -h` for more details.

The `scripts/` folder contains some example bash scripts that execute circuit benchmarks for different numbers of qubits.

## Benchmark output

The benchmark script prints a summary of the circuit and user selected flags together with:
- import_time: time required to import the `qibo` library and build the selected backend in seconds.
- creation_time: time required to prepare the circuit for execution in seconds.
- dry_run_execution_time: first execution performance, includes JIT timings in seconds.
- dry_run_transfer_time: time required to convert the final state to numpy array in seconds.
- simulation_times: list of timings for simulation based on `nreps` in seconds.
- transfer_times: list of timings for conversion to numpy array in seconds.
- simulation_times_mean: average simulation time for `nreps` repetitions in seconds.
- simulation_times_std: standard deviation of simulation_time in seconds.
- transfer_times_mean: average transfer time for `nreps` repetitions in seconds.
- transfer_time_std: standard deviation of transfer_times in seconds.
- measurement_time: time required to sample frequencies for `nshots` measurement shots in seconds (relevant only if the `--nshots` argument is given).

Note that if a GPU is used for simulation then transfer times measure the time required to copy the final state from the GPU memory to CPU.

If `--filename` is given the above logs are saved in json format in the given directory.


## Implemented circuits

- `one-qubit-gate`: circuit consisting of a single one qubit gate. The gate is applied to every qubit in the circuit. Available options:
  - `gate`: String defining the one qubit gate to be benchmarked (eg. "H"). Default is "H"
  - `nlayers`: Number of times that the gate is applied to each qubit. Default is 1.
  - additional parameters (eg. `theta`, etc.) required for parametrized gates.
- `two-qubit-gate`: circuit consisting of a single two qubit gate. The gate is applied to every pair of adjacent qubits in the circuit (assuming one dimensional topology).
  - `gate`: String defining the one qubit gate to be benchmarked. Default is CNOT.
  - `nlayers`: Number of times that the gate is applied to each qubit. Default is 1.
  - additional parameters (eg. `theta`, etc.) required for parametrized gates.
- `qft`: [quantum fourier transform](https://en.wikipedia.org/wiki/Quantum_Fourier_transform)
  - `swaps`: Boolean controling if swaps are applied after the main QFT circuit. Default is True.
- `variational`: variational quantum circuit consisting a layer of RY rotations followed be a layer of CZ entangling gates. Can be created using either standard qibot gates or the optimized [VariationalLayer](https://qibo.readthedocs.io/en/latest/qibo.html#variational-layer) gate.
  - `nlayers`: Number of times that the gate is applied to each qubit.
  - `varlayer`: Boolean controling whether the VariationalLayer or standard gates are used. Default is False.
