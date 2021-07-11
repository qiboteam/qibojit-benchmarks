# Benchmarking quantum simulation

This repository contains benchmark scripts for quantum circuit simulation using
[Qibo](https://github.com/qiboteam/qibo) and multiple simulation engines.

## Installing prerequisites

Before executing the simulation please:

1. Install `Qibo >= 0.1.6rc1` from source or using:
    ```
    pip install qibo --pre
    ```

2. Install qibojit simulation backends with:
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

- [qibojit](https://github.com/qiboteam/qibojit): uses numba and cupy for custom kernel operations.
- [qibotf](https://github.com/qiboteam/qibotf): uses tf primitives with custom operators.
- [tensorflow](https://www.tensorflow.org/): uses tf default primitives.
- [numpy](https://numpy.org/): single-threaded CPU implementation.

For more details check the documentation [here](https://qibo.readthedocs.io/en/latest/installation.html).

## Running the benchmarks

The script in `benchmarks/main.py` executes the benchmark code following the supported configuration flags (check `python main.py -h`).

Before executing the code keep in mind the following:
- GPUs are the default devices for qibojit and qibotf. If you need CPU performance numbers do `export CUDA_VISIBLES_DEVICE=""` before executing the benchmark script.
- CPU simulations by default use physical cores as number of threads with qibojit and qibotf. To control this behaviour without touching the code do `export OMP_NUM_THREADS=<threads>` before executing the bencharmk script.
- The benchmark script provides several options, including the possibility to modify the default numba threading pooling technology.

## Benchmark output

The benchmark script prints a summary of the circuit and user selected flags together with:
- creation_time: time required to prepare the circuit for execution in seconds.
- dry_run_execution_time: first execution performance, includes JIT timings in seconds.
- dry_run_transfer_time: transfer time of results from GPU to CPU in seconds.
- simulation_times: list of timings for simulation based on `nreps` in seconds.
- transfer_times: list of timings for transfer of results form GPU to CPU in seconds.
- simulation_time: average simulation time for `nreps` repetitions in seconds.
- simulation_time_std: standard deviation of simulation_time in seconds.
- transfer_time: average transfer time of results from GPU to CPU for `nreps` repetitions in seconds.
- transfer_time_std: standard deviation of transfer_time in seconds.


## Implemented circuits

- `qft`: [quantum fourier transform](https://en.wikipedia.org/wiki/Quantum_Fourier_transform)
- `variational_circuit`: [variational quantum circuit layer as defined](https://qibo.readthedocs.io/en/latest/qibo.html#variational-layer)
