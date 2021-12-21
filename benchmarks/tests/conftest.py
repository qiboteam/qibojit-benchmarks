NQUBITS = "3,4,5"
BACKENDS = "qibojit,tensorflow,numpy"
LIBRARIES = "qibo,qiskit,qiskit-default,cirq,qulacs"


def pytest_addoption(parser):
    parser.addoption("--nqubits", type=str, default=NQUBITS)
    parser.addoption("--backends", type=str, default=BACKENDS)
    parser.addoption("--libraries", type=str, default=LIBRARIES)


def pytest_generate_tests(metafunc):
    nqubits = [int(n) for n in metafunc.config.option.nqubits.split(",")]
    backends = metafunc.config.option.backends.split(",")
    libraries = metafunc.config.option.libraries.split(",")

    if "nqubits" in metafunc.fixturenames:
        metafunc.parametrize("nqubits", nqubits)
    if "backend" in metafunc.fixturenames:
        metafunc.parametrize("backend", backends)
    if "library" in metafunc.fixturenames:
        metafunc.parametrize("library", libraries)
    if "transfer" in metafunc.fixturenames:
        metafunc.parametrize("transfer", [False, True])
