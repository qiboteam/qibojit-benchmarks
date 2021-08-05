from abc import abstractmethod
from qiskit import QuantumCircuit


class BaseCircuit:

    def __init__(self, nqubits):
        self.nqubits = nqubits
        self.parameters = {}

    @abstractmethod
    def circuit(self):
        raise NotImplementedError

    def __str__(self):
        return ", ".join(f"{k}={v}" for k, v in self.parameters.items())


class QASMCircuit(BaseCircuit):
    """Circuit constructed from OpenQASM code."""

    def __init__(self, nqubits, qasm=""):
        super().__init__(nqubits)
        self.qasm = qasm
        self.parameters = {"nqubits": nqubits, "qasm": qasm}
        self._circuit = None

    def circuit(self):
        if self._circuit is None:
            self._circuit = QuantumCircuit.from_qasm_str(self.qasm)
        return self._circuit
