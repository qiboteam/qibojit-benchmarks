from benchmarks.libraries import abstract


class Cirq(abstract.AbstractBackend):

    def __init__(self):
        import cirq
        import numpy as np
        self.name = "cirq"
        self.__version__ = cirq.__version__
        self.simulator = cirq.Simulator(dtype=np.complex128)

    def from_qasm(self, qasm):
        from cirq.contrib.qasm_import import circuit_from_qasm
        return circuit_from_qasm(qasm)

    def __call__(self, circuit):
        result = self.simulator.simulate(circuit)
        return result.final_state_vector

    def get_precision(self):
        return "double"

    def get_device(self):
        return None
