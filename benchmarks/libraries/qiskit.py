from benchmarks.libraries import abstract


class QiskitDefault(abstract.AbstractBackend):

    def __init__(self, **backend_options):
        import qiskit
        from qiskit import QuantumCircuit
        from qiskit.providers.aer import StatevectorSimulator
        self.name = "qiskit-default"
        self.__version__ = qiskit.__version__
        self.precision = "double"
        self.options = backend_options
        self.QuantumCircuit = QuantumCircuit
        self.StatevectorSimulator = StatevectorSimulator
        self.simulator = StatevectorSimulator(**backend_options)

    def from_qasm(self, qasm):
        # TODO: Consider using `circ = transpile(circ, simulator)`
        return self.QuantumCircuit.from_qasm_str(qasm)

    def __call__(self, circuit):
        result = self.simulator.run(circuit).result()
        return result.get_statevector(circuit)

    def get_precision(self):
        return self.precision

    def set_precision(self, precision):
        self.precision = precision
        self.options["precision"] = precision
        self.simulator = self.StatevectorSimulator(**self.options)

    def get_device(self):
        return None


class Qiskit(QiskitDefault):

    def __init__(self):
        super().__init__(fusion_enable=False)
        self.name = "qiskit"


class QiskitFusion(QiskitDefault):

    def __init__(self, max_qubits=2):
        super().__init__(fusion_max_qubit=max_qubits)
        self.name = "qiskit-twoqubitfusion"


class QiskitGpu(QiskitDefault):

    def __init__(self):
        super().__init__(fusion_enable=False, device="GPU")
        self.name = "qiskit-gpu"
