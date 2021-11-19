import numpy as np
from benchmarks.libraries import abstract


class HybridQ(abstract.ParserBackend):

    def __init__(self):
        from hybridq.gate import Gate
        self.name = "hybridq"
        self.__version__ = "0.7.7.post2"
        self.Gate = Gate
        self.max_qubits = 0

    def RX(self, theta):
        return self.Gate('RX', params=[theta])

    def RY(self, theta):
        return self.Gate('RY', params=[theta])

    def RZ(self, theta):
        return self.Gate('RZ', params=[theta])

    def CU1(self, theta):
        raise NotImplementedError

        matrix = np.diag([1, np.exp(1j * theta)])
        gate = self.qulacs.gate.DenseMatrix([target], matrix)
        gate.add_control_qubit(control, 1)
        return gate

    def CU3(self, theta, phi, lam):
        raise NotImplementedError

        cost, sint = np.cos(theta / 2.0), np.sin(theta / 2.0)
        pplus, pminus = np.exp(0.5j * (phi + lam)), np.exp(0.5j * (phi - lam))
        matrix = np.array([[np.conj(pplus) * cost, -np.conj(pminus) * sint],
                           [pminus * sint, pminus * cost]])
        gate = self.qulacs.gate.DenseMatrix([target], matrix)
        gate.add_control_qubit(control, 1)
        return gate

    def RZZ(self, theta):
        raise NotImplementedError

        phase = np.exp(0.5j * theta)
        phasec = np.conj(phase)
        matrix = np.diag([phasec, phase, phase, phasec])
        gate = self.qulacs.gate.DenseMatrix([target1, target2], matrix)
        return gate

    def __getattr__(self, x):
        return self.Gate(x)

    def __getitem__(self, x):
        return self.Gate(x)

    def from_qasm(self, qasm):
        from hybridq.circuit import Circuit
        nqubits, gatelist = self.parse(qasm)
        circuit = Circuit()
        for gatename, qubits, params in gatelist:
            if params is not None:
                gate = getattr(self, gatename)(*params)
            else:
                gate = getattr(self, gatename)
            circuit.append(gate.on(qubits))
        return circuit

    def __call__(self, circuit):
        from hybridq.circuit.simulation import simulate
        initial_state = len(circuit.all_qubits()) * '0'
        return simulate(circuit, optimize='evolution', initial_state=initial_state,
                        compress=self.max_qubits)

    def get_precision(self):
        return "single"

    def get_device(self):
        return None


class HybridQFusion(HybridQ):

    def __init__(self, max_qubits=2):
        super().__init__()
        self.name = "hybridq-fusion"
        self.max_qubits = max_qubits
