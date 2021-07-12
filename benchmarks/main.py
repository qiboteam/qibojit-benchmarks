"""Launches the circuit benchmark script for user given arguments."""
import argparse
from scripts import circuit_benchmark


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


if __name__ == "__main__":
    args = vars(parser.parse_args())
    args["circuit_name"] = args.pop("circuit")
    circuit_benchmark(**args)
