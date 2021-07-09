"""
Generic benchmark script that runs circuits defined in `benchmark_models.py`.

The type of the circuit is selected using the ``--type`` flag.
"""
import argparse
import os
import time
import logger
import numpy as np
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # disable Tensorflow warnings


parser = argparse.ArgumentParser()
parser.add_argument("--nqubits", default=20, type=int)
parser.add_argument("--backend", default="qibojit", type=str)
parser.add_argument("--precision", default="double", type=str)
parser.add_argument("--nreps", default=1, type=int)
parser.add_argument("--filename", default=None, type=str)

parser.add_argument("--circuit", default="qft", type=str)
parser.add_argument("--params", default=None, type=str)
parser.add_argument("--nshots", default=None, type=int)

parser.add_argument("--memory", default=None, type=int)
parser.add_argument("--threading", default=None, type=str)
parser.add_argument("--transfer", action="store_true")


def main(nqubits, backend, circuit, precision="double", params=None,
         nreps=1, nshots=None, memory=None, threading=None,
         transfer=False, filename=None):
    """Runs benchmarks for different circuit types.

    Args:
        nqubits (int): Number of qubits in the circuit.
        backend (str): Qibo backend to use for simulation.
        precision (str): Numerical precision of the simulation.
            Choose between 'double' and 'single'.
            Default is 'double'.
        circuit (str): Type of Circuit to use.
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

    logs = logger.JsonLogger(filename)
    # Create log dict
    logs.append({
        "nqubits": nqubits, "circuit": circuit, "params": params,
        "nreps": nreps, "nshots": nshots, "transfer": transfer,
        "numba-threading": threading, "gpu-memory": memory
        })

    start_time = time.time()
    import qibo
    logs[-1]["import_time"] = time.time() - start_time

    qibo.set_backend(backend)
    qibo.set_precision(precision)
    logs[-1]["backend"] = qibo.get_backend()
    logs[-1]["precision"] = qibo.get_precision()
    logs[-1]["device"] = qibo.get_device()

    from circuits import CircuitConstructor
    gates = CircuitConstructor(circuit, params, nqubits)
    start_time = time.time()
    circuit = qibo.models.Circuit(nqubits)
    circuit.add(gates)
    if nshots is not None:
        # add measurement gates
        circuit.add(qibo.gates.M(*range(nqubits)))
    logs[-1]["creation_time"] = time.time() - start_time

    start_time = time.time()
    result = circuit(nshots=nshots)
    logs[-1]["dry_run_execution_time"] = time.time() - start_time
    start_time = time.time()
    if transfer:
        result = result.numpy()
    logs[-1]["dry_run_transfer_time"] = time.time() - start_time

    logs[-1]["simulation_times"], logs[-1]["transfer_times"] = [], []
    for _ in range(nreps):
        start_time = time.time()
        result = circuit(nshots=nshots)
        logs[-1]["simulation_times"].append(time.time() - start_time)
        start_time = time.time()
        if transfer:
            result = result.numpy()
        logs[-1]["transfer_times"].append(time.time() - start_time)

    logs[-1]["dtype"] = str(result.dtype)
    logs[-1]["simulation_time"] = np.mean(logs[-1]["simulation_times"])
    logs[-1]["simulation_time_std"] = np.std(logs[-1]["simulation_times"])
    logs[-1]["transfer_time"] = np.mean(logs[-1]["transfer_times"])
    logs[-1]["transfer_time_std"] = np.std(logs[-1]["transfer_times"])

    if nshots is not None:
        start_time = time.time()
        freqs = result.frequencies()
        logs[-1]["measurement_time"] = time.time() - start_time

    print()
    print(logs)
    logs.dump()
    print()


if __name__ == "__main__":
    args = vars(parser.parse_args())
    main(**args)
