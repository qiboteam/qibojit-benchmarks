from benchmarks.libraries import abstract


class QiskitDefault(abstract.AbstractBackend):

    def __init__(self, **backend_options):
        import qiskit
        from qiskit import QuantumCircuit
        from qiskit.providers.aer import StatevectorSimulator
        self.name = "qiskit-default"
        self.__version__ = qiskit.__version__
        self.QuantumCircuit = QuantumCircuit
        self.simulator = StatevectorSimulator(**backend_options)

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


class Qiskit(QiskitDefault):

    def __init__(self):
        super().__init__(fusion_enable=False)
        self.name = "qiskit"


class QiskitTwoQubitFusion(Qiskit):

    def __init__(self):
        super().__init__(fusion_max_qubit=2)
        self.name = "qiskit-twoqubitfusion"


class QiskitGpu(Qiskit):

    def __init__(self):
        super().__init__(method="statevector_gpu")
        self.name = "qiskit-gpu"
