NQUBITS = [3, 4, 5]
BACKENDS = ["qibojit", "qibotf", "tensorflow", "numpy"]


def pytest_generate_tests(metafunc):
    if "nqubits" in metafunc.fixturenames:
        metafunc.parametrize("nqubits", NQUBITS)
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", BACKENDS)