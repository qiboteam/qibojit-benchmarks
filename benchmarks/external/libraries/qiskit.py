import numpy as np
from benchmarks.external.libraries import abstract


class Qiskit(abstract.AbstractBackend):

    def __init__(self):
        from qiskit import QuantumCircuit
        from qiskit import Aer
        self.QuantumCircuit = QuantumCircuit
        self.simulator = Aer.get_backend('statevector_simulator')

    def from_qasm(self, qasm):
        # TODO: Consider using `circ = transpile(circ, simulator)`
        return self.QuantumCircuit.from_qasm_str(qasm)

    def __call__(self, circuit):
        result = self.simulator.run(circuit).result()
        return result.get_statevector(circuit)

    def transpose_state(self, x):
        """Switch order of qubits in state vector to be compatible to Qibo."""
        shape = tuple(x.shape)
        nqubits = int(np.log2(shape[0]))
        x = np.reshape(x, nqubits * (2,))
        x = np.transpose(x, range(nqubits - 1, -1, -1))
        return np.reshape(x, shape)
