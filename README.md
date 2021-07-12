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

- [qibojit](https://github.com/qiboteam/qibojit): uses numba on CPU and cupy on GPU for custom operations.
- [qibotf](https://github.com/qiboteam/qibotf): uses tf primitives with custom operators on CPU and GPU.
- [tensorflow](https://www.tensorflow.org/): uses tf default primitives.
- [numpy](https://numpy.org/): single-threaded CPU implementation.

For more details check the documentation [here](https://qibo.readthedocs.io/en/latest/installation.html).

## Running the benchmarks

The script in `benchmarks/main.py` executes the benchmark code following the supported configuration flags:

```
$ python main.py -h

usage: main.py [-h] [--nqubits NQUBITS] [--backend BACKEND]
                    [--circuit CIRCUIT] [--options OPTIONS]
                    [--nreps NREPS] [--nshots NSHOTS] [--transfer]
                    [--precision PRECISION] [--memory MEMORY]
                    [--threading THREADING] [--filename FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --nqubits NQUBITS
  --backend BACKEND
  --precision PRECISION
  --nreps NREPS
  --filename FILENAME
  --circuit CIRCUIT
  --params PARAMS
  --nshots NSHOTS
  --memory MEMORY
  --threading THREADING
  --transfer
```

Check `python main.py -h` for complete documentation of each flag.

Before executing the code keep in mind the following:
- GPUs are the default devices for qibojit and qibotf. If you need CPU performance numbers do `export CUDA_VISIBLES_DEVICE=""` before executing the benchmark script.
- CPU simulations by default use physical cores as number of threads with qibojit and qibotf. To control this behaviour without touching the code do `export OMP_NUM_THREADS=<threads>` (or `export NUMBA_NUM_THREADS=<threads>` for qibojit numba backend) before executing the benchmark script.
- The benchmark script provides several options, including the possibility to modify the default numba threading pooling technology, (see [docs](https://numba.pydata.org/numba-doc/latest/developer/threading_implementation.html#notes-on-numba-s-threading-implementation)) or limiting the GPU memory used be Tensorflow. See `python main.py -h` for more details.

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

- `one-qubit-gate`: circuit consisting of a single one qubit gate. The gate is applied to every qubit in the circuit.
- `two-qubit-gate`: circuit consisting of a single two qubit gate. The gate is applied to every pair of adjacent qubits in the circuit (assuming one dimensional topology).
- `qft`: [quantum fourier transform](https://en.wikipedia.org/wiki/Quantum_Fourier_transform)
- `variational`: variational quantum circuit consisting a layer of `RY` rotations followed be a layer of `CZ` entangling gates. Can be created using either standard qibot gates or the optimized [`VariationalLayer`](https://qibo.readthedocs.io/en/latest/qibo.html#variational-layer) gate.
