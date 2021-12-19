def get(backend_name, max_qubits=0):
    if backend_name == "qibo":
        from benchmarks.libraries.qibo import Qibo
        return Qibo(max_qubits)
    elif backend_name == "qibojit":
        from benchmarks.libraries.qibo import QiboJit
        return QiboJit(max_qubits)
    elif backend_name == "qibotf":
        from benchmarks.libraries.qibo import QiboTF
        return QiboTF(max_qubits)

    elif backend_name == "qiskit":
        from benchmarks.libraries.qiskit import Qiskit
        return Qiskit(max_qubits)
    elif backend_name == "qiskit-gpu":
        from benchmarks.libraries.qiskit import QiskitGpu
        return QiskitGpu(max_qubits)

    elif backend_name == "cirq":
        from benchmarks.libraries.cirq import Cirq
        return Cirq()
    elif backend_name == "qsim":
        from benchmarks.libraries.cirq import QSim
        return QSim(max_qubits)
    elif backend_name == "qsim-gpu":
        from benchmarks.libraries.cirq import QSimGpu
        return QSimGpu(max_qubits)
    elif backend_name == "qsim-cuquantum":
        from benchmarks.libraries.cirq import QSimCuQuantum
        return QSimCuQuantum(max_qubits)
    elif backend_name == "tfq":
        from benchmarks.libraries.cirq import TensorflowQuantum
        return TensorflowQuantum()

    elif backend_name == "qulacs":
        from benchmarks.libraries.qulacs import Qulacs
        return Qulacs()
    elif backend_name == "qulacs-gpu":
        from benchmarks.libraries.qulacs import QulacsGpu
        return QulacsGpu()

    elif backend_name == "qcgpu":
        from benchmarks.libraries.qcgpu import QCGPU
        return QCGPU()

    elif backend_name == "hybridq":
        from benchmarks.libraries.hybridq import HybridQ
        return HybridQ(max_qubits)
    elif backend_name == "hybridq-gpu":
        from benchmarks.libraries.hybridq import HybridQGPU
        return HybridQGPU(max_qubits)

    raise KeyError(f"Unknown simulation library {backend_name}.")
