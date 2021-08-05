import numpy as np
from abc import abstractmethod


class BaseCircuit:

    def __init__(self, nqubits):
        self.nqubits = nqubits
        self.parameters = {}

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    def to_qasm(self):
        code = ['OPENQASM 2.0;', 'include "qelib1.inc";',
                f'qreg q[{self.nqubits}];', f'creg m[{self.nqubits}];']
        code.extend(iter(self))
        return "\n".join(code)

    def __str__(self):
        return ", ".join(f"{k}={v}" for k, v in self.parameters.items())


class OneQubitGate(BaseCircuit):
    """Applies a specific one qubit gate to all qubits."""

    def __init__(self, nqubits, nlayers="1", gate="h", **params):
        super().__init__(nqubits)
        self.gate = gate
        self.nlayers = int(nlayers)
        self.angles = {k: float(v) for k, v in params.items()}
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers,
                           "gate": gate, "params": params}

    def __iter__(self):
        # TODO: Fix angles
        for _ in range(self.nlayers):
            for i in range(self.nqubits):
                yield "{} q[{}];".format(self.gate, i)


class TwoQubitGate(OneQubitGate):
    """Applies a specific two qubit gate to all pairs of adjacent qubits."""

    def __init__(self, nqubits, nlayers="1", gate="cx", **params):
        super().__init__(nqubits, nlayers, gate, **params)

    def __iter__(self):
        # TODO: Fix angles
        for _ in range(self.nlayers):
            for i in range(0, self.nqubits - 1, 2):
                yield "{} q[{}],q[{}];".format(self.gate, i, i + 1)
            for i in range(1, self.nqubits - 1, 2):
                yield "{} q[{}],q[{}];".format(self.gate, i, i + 1)


class QFT(BaseCircuit):
    """Applies the Quantum Fourier Transform."""

    def __init__(self, nqubits, swaps="True"):
        super().__init__(nqubits)
        self.swaps = swaps == "True"
        self.parameters = {"nqubits": nqubits, "swaps": swaps}

    def __iter__(self):
        for i1 in range(self.nqubits):
            yield f"h q[{i1}];"
            for i2 in range(i1 + 1, self.nqubits):
                theta = np.pi / 2 ** (i2 - i1)
                yield f"cu1({theta}) q[{i2}],q[{i1}];"

        if self.swaps:
            for i in range(self.nqubits // 2):
                yield f"swap q[{i}],q[{self.nqubits - i - 1}];"


class VariationalCircuit(BaseCircuit):
    """Example variational circuit consisting of alternating layers of RY and CZ gates."""

    def __init__(self, nqubits, nlayers="1"):
        super().__init__(nqubits)
        self.nlayers = int(nlayers)
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers}

    def __iter__(self):
        nparams = 2 * self.nlayers * self.nqubits
        theta = iter(2 * np.pi * np.random.random(nparams))
        for l in range(self.nlayers):
            for i in range(self.nqubits):
                yield f"ry({next(theta)}) q[{i}];"
            for i in range(0, self.nqubits - 1, 2):
                yield f"cz q[{i}],q[{i + 1}];"
            for i in range(self.nqubits):
                yield f"ry({next(theta)}) q[{i}];"
            for i in range(1, self.nqubits - 2, 2):
                yield f"cz q[{i}],q[{i + 1}];"
            yield f"cz q[{0}],q[{self.nqubits - 1}];"
