def get(backend_name):
    if backend_name == "qibo":
        from benchmarks.libraries.qibo import Qibo
        return Qibo()
    elif backend_name == "qibojit":
        from benchmarks.libraries.qibo import QiboJit
        return QiboJit()
    elif backend_name == "qibotf":
        from benchmarks.libraries.qibo import QiboTF
        return QiboTF()
    elif backend_name == "qiskit":
        from benchmarks.libraries.qiskit import Qiskit
        return Qiskit()
    elif backend_name == "qiskit-nofusion":
        from benchmarks.libraries.qiskit import Qiskit
        return Qiskit(fusion_enable=False)
    elif backend_name == "qulacs":
        from benchmarks.libraries.qulacs import Qulacs
        return Qulacs()
    raise KeyError(f"Unknown simulation library {backend_name}.")
