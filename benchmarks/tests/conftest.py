NQUBITS = [3, 4, 5]
BACKENDS = ["qibojit", "qibotf", "tensorflow", "numpy"]
LIBRARIES = ["qibo", "qiskit", "qulacs"]


def pytest_generate_tests(metafunc):
    if "nqubits" in metafunc.fixturenames:
        metafunc.parametrize("nqubits", NQUBITS)
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", BACKENDS)
    if "library" in metafunc.fixturenames:
        metafunc.parametrize("library", LIBRARIES)
    if "transfer" in metafunc.fixturenames:
        metafunc.parametrize("transfer", [False, True])
