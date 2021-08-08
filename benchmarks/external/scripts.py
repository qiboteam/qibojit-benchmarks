"""Benchmark scripts."""
import time
from benchmarks.logger import JsonLogger


def library_benchmark(nqubits, library, circuit_name, options=None,
                      nreps=1, precision="double", filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps)

    start_time = time.time()
    from benchmarks.external import libraries
    backend = libraries.get(library)
    logs.log(import_time=time.time() - start_time)

    logs.log(library=backend.name,
             precision=backend.get_precision(),
             device=backend.get_device(),
             version=backend.__version__)

    from benchmarks.external.qasm import CircuitConstructor
    gates = CircuitConstructor(circuit_name, nqubits, options)
    logs.log(circuit=circuit_name, options=str(gates))
    start_time = time.time()
    circuit = backend.from_qasm(gates.to_qasm())
    logs.log(creation_time=time.time() - start_time)

    start_time = time.time()
    result = backend(circuit)
    logs.log(dry_run_time=time.time() - start_time)
    start_time = time.time()
    #if transfer:
    #    result = result.numpy()
    logs.log(dry_run_transfer_time=time.time() - start_time)

    simulation_times, transfer_times = [], []
    for _ in range(nreps):
        start_time = time.time()
        result = backend(circuit)
        simulation_times.append(time.time() - start_time)
        start_time = time.time()
        #if transfer:
        #    result = result.numpy()
        transfer_times.append(time.time() - start_time)

    logs.log(dtype=str(result.dtype),
             simulation_times=simulation_times,
             transfer_times=transfer_times)
    logs.average("simulation_times")
    logs.average("transfer_times")
    logs.dump()
    return logs
