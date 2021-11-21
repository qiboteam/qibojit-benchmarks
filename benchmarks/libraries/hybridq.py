import numpy as np
from benchmarks.libraries import abstract


class HybridQ(abstract.ParserBackend):

    def __init__(self, max_qubits=0):
        from hybridq.gate import Gate, MatrixGate
        self.name = "hybridq"
        self.__version__ = "0.7.7.post2"
        self.Gate = Gate
        self.MatrixGate = MatrixGate
        self.max_qubits = max_qubits
        # TODO: Make sure there are no hidden thresholds that disable fusion

    def RX(self, theta):
        return self.Gate('RX', params=[theta])

    def RY(self, theta):
        return self.Gate('RY', params=[theta])

    def RZ(self, theta):
        return self.Gate('RZ', params=[theta])

    def U1(self, theta):
        phase = np.exp(1j * theta)
        matrix = np.diag([1, phase])
        return self.MatrixGate(U=matrix)

    def U2(self, phi, lam):
        plus = np.exp(0.5j * (phi + lam))
        minus = np.exp(0.5j * (phi - lam))
        matrix = np.array([[np.conj(plus), np.conj(minus)], [minus, plus]]) / np.sqrt(2)
        return self.MatrixGate(U=matrix)

    def U3(self, theta, phi, lam):
        return self.Gate('U3', params=[theta, phi, lam])

    def CU1(self, theta):
        return self.Gate('CPHASE', params=[theta])

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
            if params:
                gate = getattr(self, gatename)(*params)
            else:
                gate = getattr(self, gatename)
            circuit.append(gate.on(qubits))
        return circuit

    def __call__(self, circuit):
        from hybridq.circuit.simulation import simulate
        initial_state = len(circuit.all_qubits()) * '0'
        final_state = simulate(circuit, optimize='evolution',
                               initial_state=initial_state,
                               simplify=False,
                               compress=self.max_qubits)
        return final_state.ravel()

    def transpose_state(self, x):
        return x

    def get_precision(self):
        return "single"

    def get_device(self):
        return None
