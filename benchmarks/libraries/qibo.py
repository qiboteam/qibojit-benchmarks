from benchmarks.libraries import abstract


class Qibo(abstract.AbstractBackend):

    def __init__(self, max_qubits=0):
        import qibo
        from qibo import models
        self.name = "qibo"
        self.qibo = qibo
        self.models = models
        self.__version__ = qibo.__version__
        self.max_qubits = max_qubits

    def from_qasm(self, qasm):
        circuit = self.models.Circuit.from_qasm(qasm)
        if self.max_qubits > 1:
            circuit = circuit.fuse(self.max_qubits)
        return circuit

    def __call__(self, circuit):
        # transfer final state to numpy array because that's what happens
        # for all backends
        return circuit().numpy()

    def transpose_state(self, x):
        return x

    def get_precision(self):
        return self.qibo.get_precision()

    def set_precision(self, precision):
        self.qibo.set_precision(precision)

    def get_device(self):
        return self.qibo.get_device()


class QiboJit(Qibo):

    def __init__(self, max_qubits):
        super().__init__(max_qubits)
        self.qibo.set_backend("qibojit")
        self.name = "qibojit"


class QiboTF(Qibo):

    def __init__(self, max_qubits):
        super().__init__(max_qubits)
        self.qibo.set_backend("qibotf")
        self.name = "qibotf"
