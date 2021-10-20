"""Launches the qiskit fusion benchmark script for user given arguments."""
import argparse
from benchmarks.scripts import qiskit_fusion_benchmark


parser = argparse.ArgumentParser()
parser.add_argument("--nqubits", default=20, type=int,
                    help="Number of qubits in the circuit.")
parser.add_argument("--library", default="qibo", type=str,
                    help="Quantum simulation library to use in benchmark. "
                         "See README for the list of available libraries.")
parser.add_argument("--max-qubit", default=2, type=int,
                    help="Maximum qubit number to use in fusion algorithm.")

parser.add_argument("--circuit", default="qft", type=str,
                    help="Type of circuit to use. See README for the list of "
                         "available circuits.")
parser.add_argument("--options", default=None, type=str,
                    help="String with options for circuit creation. "
                         "It should have the form 'arg1=value1,arg2=value2,...' ."
                         "See README for the list of arguments that are "
                         "available for each circuit.")

parser.add_argument("--nreps", default=1, type=int,
                    help="Number of repetitions of the circuit execution. "
                         "Dry run is not included.")

parser.add_argument("--filename", default=None, type=str,
                    help="Directory of file to save the logs in json format."
                         "If not given the logs only be printed and not saved.")


if __name__ == "__main__":
    args = vars(parser.parse_args())
    args["circuit_name"] = args.pop("circuit")
    fusion_benchmark(**args)
