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
    """Applies a specific one qubit gate to all qubits."""

    def __init__(self, nqubits, nlayers="1", gate="H", **params):
        super().__init__(nqubits)
        self.nlayers = int(nlayers)
        self.gate = getattr(gates, gate)
        self.angles = {k: float(v) for k, v in params.items()}
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers,
                           "gate": gate, "angles": angles}

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(self.nqubits):
                yield self.gate(i, **self.angles)


class TwoQubitGate(OneQubitGate):
    """Applies a specific two qubit gate to all pairs of adjacent qubits."""

    def __init__(self, nqubits, nlayers="1", gate="CNOT", **params):
        super().__init__(nqubits, nlayers, gate, **params)

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(0, self.nqubits - 1, 2):
                yield self.gate(i, i + 1, **self.params)
            for i in range(1, self.nqubits - 1, 2):
                yield self.gate(i, i + 1, **self.params)


class QFT(BaseCircuit):
    """Applies the Quantum Fourier Transform."""

    def __init__(self, nqubits, swaps="True"):
        super().__init__(nqubits)
        self.swaps = swaps == "True"
        self.parameters = {"nqubits": nqubits, "swaps": swaps}

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
    """Example variational circuit consisting of alternating layers of RY and CZ gates."""

    def __init__(self, nqubits, nlayers=1, varlayer="False"):
        super().__init__(nqubits)
        self.nlayers = int(nlayers)
        self.varlayer = varlayer == "True"
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers,
                           "varlayer": varlayer}

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


class BernsteinVazirani(BaseCircuit):
    """Applies the Bernstein-Vazirani algorithm from Qiskit/openqasm.

    See `https://github.com/Qiskit/openqasm/tree/0af8b8489f32d46692b3a3a1421e98c611cd86cc/benchmarks/bv`
    for the OpenQASM code.
    Note that `Barrier` gates are excluded for simulation.
    """

    def __init__(self, nqubits):
        super().__init__(nqubits)
        self.parameters = {"nqubits": nqubits}

    def __iter__(self):
        yield gates.X(self.nqubits - 1)
        for i in range(self.nqubits):
            yield gates.H(i)
        for i in range(self.nqubits - 1):
            yield gates.CNOT(i, self.nqubits - 1)
        for i in range(self.nqubits - 1):
            yield gates.H(i)
        for i in range(self.nqubits - 1):
            yield gates.M(i)


class HiddenShift(BaseCircuit):
    """Applies the Hidden Shift algorithm.

    See `https://github.com/quantumlib/Cirq/blob/master/examples/hidden_shift_algorithm.py`
    for the Cirq code.
    If the shift (hidden bitstring) is not given then it is randomly generated
    using `np.random.randint`.
    """

    def __init__(self, nqubits, shift=""):
        super().__init__(nqubits)
        if len(shift):
            if len(shift) != nqubits:
                raise ValueError("Shift bitstring of length {} was given for "
                                 "circuit of {} qubits."
                                 "".format(len(shift), nqubits))
            self.shift = [int(x) for x in shift]
        else:
            self.shift = np.random.randint(0, 2, size=(self.nqubits,))
        self.parameters = {"nqubits": nqubits, "shift": shift}

    def oracle(self):
        for i in range(self.nqubits // 2):
            yield gates.CZ(2 * i, 2 * i + 1)

    def __iter__(self):
        for i in range(self.nqubits):
            yield gates.H(i)
        for i, ish in enumerate(self.shift):
            if ish:
                yield gates.X(i)
        for gate in self.oracle():
            yield gate
        for i, ish in enumerate(self.shift):
            if ish:
                yield gates.X(i)
        for i in range(self.nqubits):
            yield gates.H(i)
        for gate in self.oracle():
            yield gate
        for i in range(self.nqubits):
            yield gates.H(i)
        yield gates.M(*range(self.nqubits))


class QAOA(BaseCircuit):

    def __init__(self, nqubits, nparams="2", graph=""):
        super().__init__(nqubits)
        import networkx
        self.nparams = int(nparams)
        if len(graph):
            import json
            with open(graph, "r") as file:
                data = json.load(file)
            self.graph = networkx.readwrite.json_graph.node_link_graph(data)
        else:
            self.graph = networkx.random_regular_graph(3, self.nqubits)
        self.parameters = {"nqubits": nqubits, "nparams": nparams,
                           "graph": graph}

    @staticmethod
    def RZZ(q0, q1, theta):
        phase = np.exp(1j * theta)
        phasec = np.conj(phase)
        matrix = np.diag([phasec, phase, phase, phasec])
        return gates.Unitary(matrix, q0, q1)

    def maxcut_unitary(self, betas, gammas):
        for beta, gamma in zip(betas, gammas):
            for i, j in self.graph.edges:
                yield self.RZZ(i, j, -0.5 * gamma)
            for i in range(self.nqubits):
                yield gates.RX(i, theta=2 * beta)

    def dump(self, dir):
        """Saves graph data as JSON in given directory."""
        import json
        data = networkx.readwrite.json_graph.node_link_data(self.graph)
        with open(dir, "w") as file:
            json.dump(data, file)

    def __iter__(self):
        betas = np.random.uniform(-np.pi, np.pi, size=self.nparams)
        gammas = np.random.uniform(-np.pi, np.pi, size=self.nparams)
        # Prepare uniform superposition
        for i in range(self.nqubits):
            yield gates.H(i)
        # Apply QAOA unitary
        for gate in self.maxcut_unitary(betas, gammas):
            yield gate
        # Measure
        yield gates.M(*range(self.nqubits))


class CircuitConstructor:

    circuit_map = {
        "qft": QFT,
        "QFT": QFT,
        "one-qubit-gate": OneQubitGate,
        "two-qubit-gate": TwoQubitGate,
        "variational": VariationalCircuit,
        "variational-circuit": VariationalCircuit,
        "bernstein-vazirani": BernsteinVazirani,
        "bv": BernsteinVazirani,
        "hidden-shift": HiddenShift,
        "hs": HiddenShift,
        "qaoa": QAOA
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
