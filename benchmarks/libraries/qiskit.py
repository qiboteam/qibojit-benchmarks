from benchmarks.libraries import abstract


class Qiskit(abstract.AbstractBackend):

    def __init__(self):
        import qiskit
        from qiskit import QuantumCircuit
        from qiskit import Aer
        self.name = "qiskit"
        self.__version__ = qiskit.__version__
        self.QuantumCircuit = QuantumCircuit
        self.simulator = Aer.get_backend('statevector_simulator')

    def from_qasm(self, qasm):
        # TODO: Consider using `circ = transpile(circ, simulator)`
        return self.QuantumCircuit.from_qasm_str(qasm)

    def __call__(self, circuit):
        result = self.simulator.run(circuit).result()
        return result.get_statevector(circuit)

    def get_precision(self):
        return "double"

    def get_device(self):
        return None
