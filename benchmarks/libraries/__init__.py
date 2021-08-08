def get(backend_name):
    if backend_name == "qibo":
        from benchmarks.libraries.qibo import Qibo
        return Qibo()
    elif backend_name == "qiskit":
        from benchmarks.libraries.qiskit import Qiskit
        return Qiskit()
    elif backend_name == "qulacs":
        from benchmarks.libraries.qulacs import Qulacs
        return Qulacs()
    raise KeyError(f"Unknown simulation library {backend_name}.")
