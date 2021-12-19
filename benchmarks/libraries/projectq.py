import projectq
import numpy as np
from benchmarks.libraries import abstract

class ProjectQ(abstract.ParserBackend):

    def __init__(self):
        import projectq
        self.name = "projectq"
        self.projectq = projectq
        self.__version__ = None

    def RX(self, theta):
        return self.projectq.ops.Rx(theta)

    def RY(self, theta):
        return self.projectq.ops.Ry(theta)

    def RZ(self, theta):
        return self.projectq.ops.Rz(theta)

    def U1(self, theta):
        return self.projectq.ops.R(theta)

    def SWAP(self):
        return self.projectq.ops.Swap
    
    def CRX(self, theta):
        return self.projectq.ops.C(self.RX(theta))

    def CRY(self, theta):
        return self.projectq.ops.C(self.RY(theta))

    def CRZ(self, theta):
        return self.projectq.ops.CRz(theta)
    
    def CU1(self, theta):
        U1 = self.projectq.ops.R(theta)
        return self.projectq.ops.C(U1, n_qubits=1)

    def CU3(self, theta):
        raise NotImplementedError

    def RZZ(self, theta):
        return self.projectq.ops.Rzz(theta)

    def __getattr__(self, x):
        return getattr(self.projectq.ops, x)

    def __item__(self, x):
        return getattr(self.projectq.ops, x)

    def from_qasm(self, qasm):
        nqubits, gatelist = self.parse(qasm)
        eng = self.projectq.MainEngine(projectq.backends.Simulator())
        self.eng = eng
        qureg = eng.allocate_qureg(nqubits)
        for gatename, qubits, params in gatelist:
            gate = getattr(self, gatename)
            if params is not None:
                parameters = list(params)
                if len(qubits) > 1:
                    gate(*parameters) | tuple(qureg[i] for i in qubits)
                else:
                    gate(*parameters) | qureg[qubits[0]]
            elif len(qubits) > 1:
                if gatename == "SWAP":
                    gate() | tuple(qureg[i] for i in qubits)
                else:
                    gate | tuple(qureg[i] for i in qubits)
            else:
                gate | qureg[qubits[0]]

        return qureg 

    def __call__(self, qureg):
        self.eng.flush()
        self.qubit_id , wave = self.eng.backend.cheat()
        # measure everything to avoid error when running
        self.projectq.ops.All(self.projectq.ops.Measure) | qureg
        return np.array(wave)

    def transpose_state(self, x):
        shape = tuple(x.shape)
        nqubits = int(np.log2(shape[0]))
        x = np.reshape(x, nqubits * (2,))
        x = np.transpose(x, range(nqubits - 1, -1, -1))
        x = np.transpose(x, tuple(self.qubit_id[key] for key in self.qubit_id))
        x = np.reshape(x, shape)
        return x

    def get_precision(self):
        return "double"

    def get_device(self):
        return None
