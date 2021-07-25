"""Generate random bitstrings for Hidden Shift circuit benchmarks."""
import numpy as np


file = open("random_bitstrings.dat", "w")

for nqubits in range(3, 31):
    bitstring = np.random.randint(0, 2, (nqubits,))
    bitstring = "".join(str(x) for x in bitstring)
    file.write(bitstring)
    file.write("\n")
    print(bitstring)

file.close()
