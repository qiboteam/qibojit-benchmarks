"""Launches the adiabatic evolution benchmark script for user given arguments."""
import argparse
from benchmarks.scripts import evolution_benchmark


parser = argparse.ArgumentParser()
parser.add_argument("--nqubits", default=4, type=int,
                    help="Number of qubits in the system to evolve.")
parser.add_argument("--dt", default=1e-2, type=float,
                    help="Time step size to use for time discretization.")

parser.add_argument("--solver", default="exp", type=str,
                    help="Which solver to use for integration (exponential or RK methods)")
parser.add_argument("--dense", action="store_true",
                    help="If ``True`` it uses the full Hamiltonian matrix "
                         "otherwise the Trotter decomposition is used.")

parser.add_argument("--backend", default="qibojit", type=str,
                    help="Qibo backend to use.")
parser.add_argument("--platform", default=None, type=str,
                    help="Qibo platform to use.")

parser.add_argument("--filename", default=None, type=str,
                    help="Directory of file to save the logs in json format. "
                         "If not given the logs will only be printed and not saved.")


if __name__ == "__main__":
    args = vars(parser.parse_args())
    evolution_benchmark(**args)
