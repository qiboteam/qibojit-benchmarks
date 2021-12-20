NQUBITS = [3, 4, 5]
BACKENDS = ["qibojit", "tensorflow", "numpy"]
LIBRARIES = ["qibo", "qiskit", "qiskit-default", "cirq", "qulacs"]


def pytest_addoption(parser):
    parser.addoption("--qiskit_gpu", action="store_true", default=False)
    parser.addoption("--qulacs_gpu", action="store_true", default=False)
    parser.addoption("--qcgpu", action="store_true", default=False)


def pytest_generate_tests(metafunc):

    # Check if GPU is available for tests
    try:
        from cupy import cuda # pylint: disable=E0401
        gpu_available = cuda.runtime.getDeviceCount()
    except:
        gpu_available = 0
    if gpu_available:
        if metafunc.config.option.qiskit_gpu:
            LIBRARIES.append("qiskit-gpu")
        if metafunc.config.option.qulacs_gpu:
            LIBRARIES.append("qulacs-gpu")
        if metafunc.config.option.qcgpu:
            LIBRARIES.append("qcgpu")

    if "nqubits" in metafunc.fixturenames:
        metafunc.parametrize("nqubits", NQUBITS)
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", BACKENDS)
    if "library" in metafunc.fixturenames:
        metafunc.parametrize("library", LIBRARIES)
    if "transfer" in metafunc.fixturenames:
        metafunc.parametrize("transfer", [False, True])
