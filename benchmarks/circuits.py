import numpy as np
from abc import ABC, abstractmethod
from qibo import gates


class BaseCircuit:

    def __init__(self, nqubits):
        self.nqubits = nqubits
        self.parameters = {}

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    def __str__(self):
        return ", ".join(f"{k}={v}" for k, v in self.parameters.items())


class OneQubitGate(BaseCircuit):

    def __init__(self, nqubits, nlayers="1", gate="H", **params):
        super().__init__(nqubits)
        self.nlayers = int(nlayers)
        self.gate = getattr(gates, gate)
        self.angles = {k: float(v) for k, v in params.items()}
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers,
                           "gate": gate, "angles": self.angles}

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(self.nqubits):
                yield self.gate(i, **self.angles)


class TwoQubitGate(OneQubitGate):

    def __init__(self, nqubits, nlayers="1", gate="CNOT", **params):
        super().__init__(nqubits, nlayers, gate, **params)

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(0, self.nqubits - 1, 2):
                yield self.gate(i, i + 1, **self.params)
            for i in range(1, self.nqubits - 1, 2):
                yield self.gate(i, i + 1, **self.params)


class QFT(BaseCircuit):

    def __init__(self, nqubits, swaps="True"):
        super().__init__(nqubits)
        self.swaps = swaps == "True"
        self.parameters = {"nqubits": nqubits, "swaps": self.swaps}

    def __iter__(self):
        for i1 in range(self.nqubits):
            yield gates.H(i1)
            for i2 in range(i1 + 1, self.nqubits):
                theta = np.pi / 2 ** (i2 - i1)
                yield gates.CU1(i2, i1, theta)

        if self.swaps:
            for i in range(self.nqubits // 2):
                yield gates.SWAP(i, self.nqubits - i - 1)


class VariationalCircuit(BaseCircuit):

    def __init__(self, nqubits, nlayers=1, varlayer="False"):
        super().__init__(nqubits)
        self.nlayers = int(nlayers)
        self.varlayer = varlayer == "True"
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers,
                           "varlayer": self.varlayer}

    def varlayer_circuit(self, theta):
        theta = theta.reshape((2 * self.nlayers, self.nqubits))
        pairs = list((i, i + 1) for i in range(0, self.nqubits - 1, 2))
        for l in range(self.nlayers):
            yield gates.VariationalLayer(range(self.nqubits), pairs,
                                         gates.RY, gates.CZ,
                                         theta[2 * l], theta[2 * l + 1])
            for i in range(1, self.nqubits - 2, 2):
                yield gates.CZ(i, i + 1)
            yield gates.CZ(0, self.nqubits - 1)

    def standard_circuit(self, theta):
        theta = iter(theta)
        for l in range(self.nlayers):
            for i in range(self.nqubits):
                yield gates.RY(i, next(theta))
            for i in range(0, self.nqubits - 1, 2):
                yield gates.CZ(i, i + 1)
            for i in range(self.nqubits):
                yield gates.RY(i, next(theta))
            for i in range(1, self.nqubits - 2, 2):
              yield gates.CZ(i, i + 1)
            yield gates.CZ(0, self.nqubits - 1)

    def __iter__(self):
        theta = 2 * np.pi * np.random.random(2 * self.nlayers * self.nqubits)
        if self.varlayer:
            return self.varlayer_circuit(theta)
        else:
            return self.standard_circuit(theta)


class CircuitConstructor:

    circuit_map = {
        "qft": QFT,
        "QFT": QFT,
        "one-qubit-gate": OneQubitGate,
        "two-qubit-gate": TwoQubitGate,
        "variational": VariationalCircuit,
        "variational-circuit": VariationalCircuit
        }

    def __new__(cls, circuit_name, nqubits, options=None):
        if circuit_name not in cls.circuit_map:
            raise NotImplementedError(f"Cannot find circuit {circuit_name}.")
        kwargs = cls.parse(options)
        return cls.circuit_map.get(circuit_name)(nqubits, **kwargs)

    @staticmethod
    def parse(options):
        kwargs = {}
        if options is not None:
            for parameter in options.split(","):
                if "=" in parameter:
                    k, v = parameter.split("=")
                    kwargs[k] = v
                else:
                    raise ValueError(f"Cannot parse parameter {parameter}.")
        return kwargs
