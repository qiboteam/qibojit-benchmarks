NQUBITS = [3, 4, 5]
BACKENDS = ["qibojit", "qibotf", "tensorflow", "numpy"]
LIBRARIES = ["qibo", "qiskit", "qiskit-default", "cirq", "tfq", "qulacs"]
LIBRARIES_GPU = ["qiskit-gpu", "qulacs-gpu", "qcgpu"]

# disable GPU because it is not supported by GitHub CI
# LIBRARIES.extend(LIBRARIES_GPU)


def pytest_generate_tests(metafunc):
    if "nqubits" in metafunc.fixturenames:
        metafunc.parametrize("nqubits", NQUBITS)
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", BACKENDS)
    if "library" in metafunc.fixturenames:
        metafunc.parametrize("library", LIBRARIES)
    if "transfer" in metafunc.fixturenames:
        metafunc.parametrize("transfer", [False, True])
