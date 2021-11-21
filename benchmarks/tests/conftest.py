NQUBITS = [3, 4, 5]
BACKENDS = ["qibojit", "numpy"]
LIBRARIES = ["qibo", "qiskit", "cirq", "qulacs", "hybridq"]
LIBRARIES_GPU = ["qiskit-gpu", "qulacs-gpu", "qcgpu"]


# Check if GPU is available for tests
try:
    from cupy import cuda # pylint: disable=E0401
    gpu_available = cuda.runtime.getDeviceCount()
except:
    gpu_available = 0
if gpu_available:
    LIBRARIES.extend(LIBRARIES_GPU)


def pytest_generate_tests(metafunc):
    if "nqubits" in metafunc.fixturenames:
        metafunc.parametrize("nqubits", NQUBITS)
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", BACKENDS)
    if "library" in metafunc.fixturenames:
        metafunc.parametrize("library", LIBRARIES)
    if "max_qubits" in metafunc.fixturenames:
        metafunc.parametrize("max_qubits", [0, 1, 2, 3])
    if "transfer" in metafunc.fixturenames:
        metafunc.parametrize("transfer", [False, True])
