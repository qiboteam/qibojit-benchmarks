"""Benchmark scripts."""
import time
from benchmarks.logger import JsonLogger


def circuit_benchmark(nqubits, backend, circuit_name, options=None,
                      nreps=1, nshots=None, transfer=False,
                      precision="double", memory=None, threading=None,
                      filename=None):
    """Runs benchmark for different circuit types.

    See ``benchmarks/main.py`` for documentation of each argument.
    """
    if backend == "qibojit" and threading is not None:
        from benchmarks.utils import select_numba_threading
        threading = select_numba_threading(threading)

    if backend in {"qibotf", "tensorflow"} and memory is not None:
        from benchmarks.utils import limit_gpu_memory
        memory = limit_gpu_memory(memory)

    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps, nshots=nshots, transfer=transfer,
             numba_threading=threading, gpu_memory=memory)

    start_time = time.time()
    import qibo
    logs.log(import_time=time.time() - start_time)

    qibo.set_backend(backend)
    qibo.set_precision(precision)
    logs.log(backend=qibo.get_backend(),
             precision=qibo.get_precision(),
             device=qibo.get_device(),
             version=qibo.__version__)

    from benchmarks import circuits
    gates = circuits.get(circuit_name, nqubits, options, qibo=True)
    logs.log(circuit=circuit_name, options=str(gates))
    start_time = time.time()
    circuit = qibo.models.Circuit(nqubits)
    circuit.add(gates)
    if nshots is not None:
        # add measurement gates
        circuit.add(qibo.gates.M(*range(nqubits)))
    logs.log(creation_time=time.time() - start_time)

    start_time = time.time()
    result = circuit(nshots=nshots)
    logs.log(dry_run_time=time.time() - start_time)
    start_time = time.time()
    if transfer:
        result = result.numpy()
    logs.log(dry_run_transfer_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)

    simulation_times, transfer_times = [], []
    for _ in range(nreps):
        start_time = time.time()
        result = circuit(nshots=nshots)
        simulation_times.append(time.time() - start_time)
        start_time = time.time()
        if transfer:
            result = result.numpy()
        transfer_times.append(time.time() - start_time)
        del(result)

    logs.log(dtype=dtype, simulation_times=simulation_times,
             transfer_times=transfer_times)
    logs.average("simulation_times")
    logs.average("transfer_times")

    if nshots is not None:
        result = circuit(nshots=nshots)
        start_time = time.time()
        freqs = result.frequencies()
        logs.log(measurement_time=time.time() - start_time)
        del result
    else:
        logs.log(measurement_time=0)
        logs.dump()

    return logs


def library_benchmark(nqubits, library, circuit_name, options=None,
                      precision=None, nreps=1, filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps)

    start_time = time.time()
    from benchmarks import libraries
    backend = libraries.get(library)
    logs.log(import_time=time.time() - start_time)
    if precision is not None:
        backend.set_precision(precision)

    logs.log(library=backend.name,
             precision=backend.get_precision(),
             device=backend.get_device(),
             version=backend.__version__)

    from benchmarks import circuits
    gates = circuits.get(circuit_name, nqubits, options)
    logs.log(circuit=circuit_name, options=str(gates))
    start_time = time.time()
    circuit = backend.from_qasm(gates.to_qasm())
    logs.log(creation_time=time.time() - start_time)

    start_time = time.time()
    result = backend(circuit)
    logs.log(dry_run_time=time.time() - start_time)
    dtype = str(result.dtype)
    del(result)

    simulation_times = []
    for _ in range(nreps):
        start_time = time.time()
        result = backend(circuit)
        simulation_times.append(time.time() - start_time)
        del(result)

    logs.log(dtype=dtype, simulation_times=simulation_times)
    logs.average("simulation_times")
    logs.dump()
    return logs
