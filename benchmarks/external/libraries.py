from benchmarks.external import abstract


class Qibo(abstract.AbstractBackend):

    def __init__(self):
        from qibo import models
        self.models = models

    def from_qasm(self, qasm):
        return self.models.Circuit.from_qasm(qasm)

    def __call__(self, circuit):
        return circuit()


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


class Qulacs(abstract.ParserBackend):

    def __init__(self):
        import numpy as np
        import qulacs
        self.np = np
        self.qulacs = qulacs

    def CU1(self, control, target, theta):
        matrix = self.np.diag([1, self.np.exp(1j * theta)])
        gate = self.qulacs.gate.DenseMatrix([target], matrix)
        gate.add_control_qubit(control, 1)
        return gate

    def from_qasm(self, qasm):
        nqubits, gatelist = self.parse(qasm)
        circuit = self.qulacs.QuantumCircuit(nqubits)
        for gatename, args in gatelist:
            try:
                gate = getattr(self.qulacs.gate, gatename)
            except AttributeError:
                gate = getattr(self, gatename)
            circuit.add_gate(gate(*args))
        return circuit

    def __call__(self, circuit):
        nqubits = circuit.get_qubit_count()
        state = self.qulacs.StateVector(nqubits)
        circuit.update_quantum_state(state)
        return state.get_vector()


def get(backend_name):
    if backend_name == "qibo":
        return Qibo()
    elif backend_name == "qiskit":
        return Qiskit()
    elif backend_name == "qulacs":
        return Qulacs()
    raise KeyError(f"Unknown simulation library {backend_name}.")
