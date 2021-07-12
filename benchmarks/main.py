"""
Generic benchmark script that runs circuits defined in `benchmark_models.py`.

The type of the circuit is selected using the ``--type`` flag.
"""
import argparse
import time
from logger import JsonLogger


parser = argparse.ArgumentParser()
parser.add_argument("--nqubits", default=20, type=int)
parser.add_argument("--backend", default="qibojit", type=str)
parser.add_argument("--precision", default="double", type=str)
parser.add_argument("--nreps", default=1, type=int)
parser.add_argument("--filename", default=None, type=str)

parser.add_argument("--circuit", default="qft", type=str)
parser.add_argument("--options", default=None, type=str)
parser.add_argument("--nshots", default=None, type=int)

parser.add_argument("--memory", default=None, type=int)
parser.add_argument("--threading", default=None, type=str)
parser.add_argument("--transfer", action="store_true")


def main(nqubits, backend, circuit_name, precision="double", options=None,
         nreps=1, nshots=None, memory=None, threading=None,
         transfer=False, filename=None):
    """Runs benchmarks for different circuit types.

    Args:
        nqubits (int): Number of qubits in the circuit.
        backend (str): Qibo backend to use for simulation.
        precision (str): Numerical precision of the simulation.
            Choose between 'double' and 'single'.
            Default is 'double'.
        circuit_name (str): Type of Circuit to use.
            See ``circuits.py`` for available types.
        nreps (int): Number of repetitions of circuit execution.
            Dry run is not included. Default is 1.
        nshots (int): Number of measurement shots.
            Logs the time required to sample frequencies (no samples).
            If ``None`` no measurements are performed.
            Default is ``None``.
        transfer (bool): If ``True`` it transfers the array from GPU to CPU.
        filename (str): Name of file to write logs.
            If ``None`` logs will not be saved.
    """
    # TODO: Complete docstring
    if args.get("backend") == "qibojit" and threading is not None:
        from utils import select_numba_threading
        threading = select_numba_threading(threading)

    if args.get("backend") in {"qibotf", "tensorflow"} and memory is not None:
        from utils import limit_gpu_memory
        memory = limit_gpu_memory(memory)

    logs = JsonLogger(filename=filename, nqubits=nqubits,
                      nreps=nreps, nshots=nshots, transfer=transfer,
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

    from circuits import CircuitConstructor
    gates = CircuitConstructor(circuit_name, nqubits, options)
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

    simulation_times, transfer_times = [], []
    for _ in range(nreps):
        start_time = time.time()
        result = circuit(nshots=nshots)
        simulation_times.append(time.time() - start_time)
        start_time = time.time()
        if transfer:
            result = result.numpy()
        transfer_times.append(time.time() - start_time)

    logs.log(dtype=str(result.dtype),
             simulation_times=simulation_times,
             transfer_times=transfer_times)
    logs.average("simulation_times")
    logs.average("transfer_times")

    start_time = time.time()
    if nshots is not None:
        freqs = result.frequencies()
    logs.log(measurement_time=time.time() - start_time)

    logs.dump()


if __name__ == "__main__":
    args = vars(parser.parse_args())
    args["circuit_name"] = args.pop("circuit")
    main(**args)
