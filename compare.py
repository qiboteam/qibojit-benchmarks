"""Launches the circuit benchmark script for user given arguments."""
import argparse
from benchmarks.scripts import library_benchmark


parser = argparse.ArgumentParser()
parser.add_argument("--nqubits", default=10, type=int,
                    help="Number of qubits in the circuit.")
parser.add_argument("--library", default="qibo", type=str,
                    help="Quantum simulation library to use in benchmark. "
                         "See README for the list of available libraries.")

parser.add_argument("--circuit", default="qft", type=str,
                    help="Type of circuit to use. See README for the list of "
                         "available circuits.")
parser.add_argument("--options", default=None, type=str,
                    help="String with options for circuit creation. "
                         "It should have the form 'arg1=value1,arg2=value2,...'. "
                         "See README for the list of arguments that are "
                         "available for each circuit.")
parser.add_argument("--precision", default=None, type=str,
                    help="Numerical precision of the simulation. "
                         "Choose between 'double' and 'single'.")
parser.add_argument("--max-qubits", default=0, type=int,
                    help="Maximum qubit number to use in gate fusion optimization.")


parser.add_argument("--nreps", default=1, type=int,
                    help="Number of repetitions of the circuit execution. "
                         "Dry run is not included.")
#parser.add_argument("--transfer", action="store_true",
#                    help="If used the final state array is converted to numpy. "
#                         "If the simulation device is GPU this requires a "
#                         "transfer from GPU memory to CPU.")

parser.add_argument("--filename", default=None, type=str,
                    help="Directory of file to save the logs in json format. "
                         "If not given the logs will only be printed and not saved.")


if __name__ == "__main__":
    args = vars(parser.parse_args())
    args["circuit_name"] = args.pop("circuit")
    library_benchmark(**args)
