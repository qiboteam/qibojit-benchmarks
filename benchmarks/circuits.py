import numpy as np
from qibo import models, gates


def variational_circuit(nqubits, nlayers=1, theta=None, use_varlayer=False):
    if theta is None:
        theta = 2 * np.pi * np.random.random(2 * nlayers * nqubits)

    if use_varlayer:
        theta = theta_values.reshape((2 * nlayers, nqubits))
        pairs = list((i, i + 1) for i in range(0, nqubits - 1, 2))
        for l in range(nlayers):
            yield gates.VariationalLayer(range(nqubits), pairs,
                                         gates.RY, gates.CZ,
                                         theta[2 * l], theta[2 * l + 1])
            for i in range(1, nqubits - 2, 2):
                yield gates.CZ(i, i + 1)
            yield gates.CZ(0, nqubits - 1)

    else:
        theta = iter(theta_values)
        for l in range(nlayers):
            for i in range(nqubits):
                yield gates.RY(i, next(theta))
            for i in range(0, nqubits - 1, 2):
                yield gates.CZ(i, i + 1)
            for i in range(nqubits):
                yield gates.RY(i, next(theta))
            for i in range(1, nqubits - 2, 2):
              yield gates.CZ(i, i + 1)
            yield gates.CZ(0, nqubits - 1)


def one_qubit_gate(nqubits, gate_type="H", params={}, nlayers=1):
    gate = lambda q: getattr(gates, gate_type)(q, **params)
    for _ in range(nlayers):
        for i in range(nqubits):
            yield gate(i)


def two_qubit_gate(nqubits, gate_type="CNOT", params={}, nlayers=1):
    gate = lambda q: getattr(gates, gate_type)(q, q + 1, **params)
    for _ in range(nlayers):
        for i in range(0, nqubits - 1, 2):
            yield gate(i)
        for i in range(1, nqubits - 1, 2):
            yield gate(i)
