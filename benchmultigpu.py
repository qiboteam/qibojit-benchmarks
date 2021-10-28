import argparse
import time
from benchmarks.logger import JsonLogger


parser = argparse.ArgumentParser()
parser.add_argument("--nqubits", default=10, type=int,
                    help="Number of qubits in the circuit.")
parser.add_argument("--library", default="qibo", type=str,
                    help="Quantum simulation library to use in benchmark. "
                         "See README for the list of available libraries.")
parser.add_argument("--accelerators", default=None, type=str,
                    help="String specifying the multi-GPU configuration to use.")


parser.add_argument("--circuit", default="qft", type=str,
                    help="Type of circuit to use. See README for the list of "
                         "available circuits.")
parser.add_argument("--options", default=None, type=str,
                    help="String with options for circuit creation. "
                         "It should have the form 'arg1=value1,arg2=value2,...' ."
                         "See README for the list of arguments that are "
                         "available for each circuit.")
parser.add_argument("--precision", default=None, type=str,
                    help="Numerical precision of the simulation."
                         "Choose between 'double' and 'single'.")

parser.add_argument("--nreps", default=1, type=int,
                    help="Number of repetitions of the circuit execution. "
                         "Dry run is not included.")

parser.add_argument("--filename", default=None, type=str,
                    help="Directory of file to save the logs in json format."
                         "If not given the logs only be printed and not saved.")


def parse_accelerators(accelerators):
    """Transforms string that specifies accelerators to dictionary.
    The string that is parsed has the following format:
        n1device1,n2device2,n3device3,...
    and is transformed to the dictionary:
        {'device1': n1, 'device2': n2, 'device3': n3, ...}
    Example:
        2/GPU:0,2/GPU:1 --> {'/GPU:0': 2, '/GPU:1': 2}
    """
    if accelerators is None:
        return None

    def read_digit(x):
        i = 0
        while x[i].isdigit():
            i += 1
        return x[i:], int(x[:i])

    acc_dict = {}
    for entry in accelerators.split(","):
        device, n = read_digit(entry)
        if device in acc_dict:
            acc_dict[device] += n
        else:
            acc_dict[device] = n
    return acc_dict


def main(nqubits, library, circuit_name, accelerators, options=None,
                      precision=None, nreps=1, filename=None):
    """Runs benchmark for different quantum simulation libraries.

    See ``benchmarks/compare.py`` for documentation of each argument.
    """
    logs = JsonLogger(filename)
    logs.log(nqubits=nqubits, nreps=nreps)

    start_time = time.time()
    from benchmarks.libraries.qibo import QiboMultiGpu
    backend = QiboMultiGpu(accelerators)
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

    simulation_times, transfer_times = [], []
    for _ in range(nreps):
        start_time = time.time()
        result = backend(circuit)
        simulation_times.append(time.time() - start_time)
        start_time = time.time()
        del(result)

    logs.log(dtype=dtype, simulation_times=simulation_times)
    logs.average("simulation_times")
    logs.dump()
    return logs


if __name__ == "__main__":
    args = vars(parser.parse_args())
    args["circuit_name"] = args.pop("circuit")
    args["accelerators"] = parse_accelerators(args.pop("accelerators"))
    main(**args)
