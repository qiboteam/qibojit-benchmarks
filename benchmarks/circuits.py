from abc import ABC, abstractmethod
import numpy as np
from qibo import gates


# TODO: Update this to the class format
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


class BaseCircuit(ABC):

    def __init__(self, nqubits, params=None):
        self.nqubits = nqubits

    @staticmethod
    def parse(params):
        p = {}
        if params is not None:
            for param in params.split(","):
                k, v = param.split("=")
                p[k] = v
        return p

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError


class OneQubitGate(BaseCircuit):

    def __init__(self, nqubits, params=None):
        super().__init__(nqubits)
        p = self.parse(params)
        self.nlayers = int(p.pop("nlayers")) if "nlayers" in p else 1
        self.gate = getattr(gates, p.pop("gate") if "gate" in p else "H")
        self.params = {k: float(v) for k, v in p.items()}

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(self.nqubits):
                yield self.gate(i, **self.params)


class TwoQubitGate(BaseCircuit):

    def __init__(self, nqubits, params=None):
        super().__init__(nqubits)
        p = self.parse(params)
        self.nlayers = int(p.pop("nlayers")) if "nlayers" in p else 1
        self.gate = getattr(gates, p.pop("gate") if "gate" in p else "CNOT")
        self.params = {k: float(v) for k, v in p.items()}

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(0, self.nqubits - 1, 2):
                yield self.gate(i, i + 1)
            for i in range(1, self.nqubits - 1, 2):
                yield self.gate(i, i + 1)


class QFT(BaseCircuit):

    def __init__(self, nqubits, params=None):
        super().__init__(nqubits)
        self.swaps = params is not None and "swap" in params

    def __iter__(self):
        for i1 in range(self.nqubits):
            yield gates.H(i1)
            for i2 in range(i1 + 1, self.nqubits):
                theta = np.pi / 2 ** (i2 - i1)
                yield gates.CU1(i2, i1, theta)

        if self.swaps:
            for i in range(self.nqubits // 2):
                yield gates.SWAP(i, self.nqubits - i - 1)


class CircuitConstructor:

    def __new__(cls, circuit_name, params, nqubits):
        if circuit_name == "qft":
            return QFT(nqubits, params)
        elif circuit_name == "one-qubit-gate":
            return OneQubitGate(nqubits, params)
        elif circuit_name == "two-qubit-gate":
            return TwoQubitGate(nqubits, params)
        raise NotImplementedError(f"Cannot find circuit {circuit_name}.")
