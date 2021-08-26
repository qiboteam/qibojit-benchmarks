from benchmarks.libraries import abstract


class Cirq(abstract.ParserBackend):

    def __init__(self):
        import cirq
        import numpy as np
        self.name = "cirq"
        self.__version__ = cirq.__version__
        self.cirq = cirq
        self.simulator = cirq.Simulator(dtype=np.complex128)

    def RX(self, theta):
        return self.cirq.XPowGate(exponent=theta)

    def RY(self, theta):
        return self.cirq.YPowGate(exponent=theta)

    def RZ(self, theta):
        return self.cirq.ZPowGate(exponent=theta)

    def CU1(self, theta):
        return self.cirq.CZPowGate(exponent=theta)

    def CU3(self, theta, phi, lam):
        gate = self.cirq.circuits.qasm_output.QasmUGate(theta, phi, lam)
        return gate.controlled(num_controls=1)

    def RZZ(self, theta):
        return self.cirq.ZZPowGate(exponent=theta)

    def __getattr__(self, x):
        return getattr(self.cirq, x)

    def __getitem__(self, x):
        return getattr(self.cirq, x)

    def from_qasm(self, qasm):
        from cirq.contrib.qasm_import import circuit_from_qasm, exception
        try:
            return circuit_from_qasm(qasm)
        except exception.QasmException:
            nqubits, gatelist = self.parse(qasm)
            qubits = [self.cirq.LineQubit(i) for i in range(nqubits)]
            circuit = self.cirq.Circuit()
            for gatename, qid, params in gatelist:
                if params is not None:
                    gate = getattr(self, gatename)(*params)
                else:
                    gate = getattr(self, gatename)
                circuit.append(gate(*(qubits[i] for i in qid)))
            return circuit

    def __call__(self, circuit):
        result = self.simulator.simulate(circuit)
        return result.final_state_vector

    def transpose_state(self, x):
        return x

    def get_precision(self):
        return "double"

    def get_device(self):
        return None
