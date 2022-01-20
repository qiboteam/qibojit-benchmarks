from benchmarks.libraries import abstract
from benchmarks.logger import log


class Qibo(abstract.AbstractBackend):

    def __init__(self, max_qubits="0", backend="qibojit", platform=None):
        import qibo
        if platform:
            qibo.set_backend(backend=backend, platform=platform)
        else:
            qibo.set_backend(backend=backend)
        from qibo import models
        self.name = "qibo"
        self.qibo = qibo
        self.models = models
        self.__version__ = qibo.__version__
        self.max_qubits = int(max_qubits)

    def from_qasm(self, qasm):
        circuit = self.models.Circuit.from_qasm(qasm)
        if self.max_qubits > 1:
            if self.max_qubits > 2:
                log.warn("Fusion with {} qubits is not yet supported by Qibo. "
                         "Using max_qubits=2.".format(self.max_qubits))
            circuit = circuit.fuse()
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
