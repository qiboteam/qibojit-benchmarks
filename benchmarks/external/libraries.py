from abc import abstractmethod


class AbstractBackend:

    @abstractmethod
    def from_qasm(self, qasm):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, circuit):
        raise NotImplementedError


class Qibo(AbstractBackend):

    def __init__(self):
        from qibo import models
        self.models = models

    def from_qasm(self, qasm):
        return self.models.Circuit.from_qasm(qasm)

    def __call__(self, circuit):
        return circuit()


class Qiskit(AbstractBackend):

    def __init__(self):
        from qiskit import QuantumCircuit
        self.QuantumCircuit = QuantumCircuit

    def from_qasm(self, qasm):
        return self.QuantumCircuit.from_qasm_str(self.qasm)

    def __call__(self, circuit):
        return circuit()


def get(backend_name):
    if backend_name == "qibo":
        return Qibo()
    elif backend_name == "qiskit":
        return Qiskit()
    raise KeyError(f"Unknown simulation library {backend_name}.")
