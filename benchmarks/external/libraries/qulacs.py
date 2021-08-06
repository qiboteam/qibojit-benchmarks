from benchmarks.external.libraries import abstract


class Qulacs(abstract.ParserBackend):

    def __init__(self):
        import numpy as np
        import qulacs
        self.np = np
        self.qulacs = qulacs

    def CU1(self, control, target, theta):
        # See `https://github.com/qulacs/qulacs/issues/278` for CU1 on Qulacs
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
