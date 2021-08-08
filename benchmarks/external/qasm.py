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

    def __init__(self, nqubits, nlayers="1", gate="h", angles=""):
        super().__init__(nqubits)
        self.gate = gate
        self.nlayers = int(nlayers)
        self.angles = angles
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers,
                           "gate": gate, "params": angles}

    def base_command(self, i):
        if self.angles:
            return "{}({}) q[{}];".format(self.gate, self.angles, i)
        else:
            return "{} q[{}];".format(self.gate, i)

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(self.nqubits):
                yield self.base_command(i)


class TwoQubitGate(OneQubitGate):
    """Applies a specific two qubit gate to all pairs of adjacent qubits."""

    def __init__(self, nqubits, nlayers="1", gate="cx", angles=""):
        super().__init__(nqubits, nlayers, gate, angles)

    def base_command(self, i):
        if self.angles:
            return "{}({}) q[{}],q[{}];".format(self.gate, self.angles, i, i + 1)
        else:
            return "{} q[{}],q[{}];".format(self.gate, i, i + 1)

    def __iter__(self):
        for _ in range(self.nlayers):
            for i in range(0, self.nqubits - 1, 2):
                yield self.base_command(i)
            for i in range(1, self.nqubits - 1, 2):
                yield self.base_command(i)


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

    def __init__(self, nqubits, nlayers="1", seed="123"):
        super().__init__(nqubits)
        self.nlayers = int(nlayers)
        self.seed = int(seed)
        self.parameters = {"nqubits": nqubits, "nlayers": nlayers, "seed": seed}

    def __iter__(self):
        nparams = 2 * self.nlayers * self.nqubits
        np.random.seed(self.seed)
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
        yield f"x q[{self.nqubits - 1}];"
        for i in range(self.nqubits):
            yield f"h q[{i}];"
        for i in range(self.nqubits - 1):
            yield f"cx q[{i}],q[{self.nqubits - 1}];"
        for i in range(self.nqubits - 1):
            yield f"h q[{i}];"
        #for i in range(self.nqubits - 1):
        #    yield f"measure m[{i}];"


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
            yield f"cz q[{2 * i}],q[{2 * i + 1}];"

    def __iter__(self):
        for i in range(self.nqubits):
            yield f"h q[{i}];"
        for i, ish in enumerate(self.shift):
            if ish:
                yield f"x q[{i}];"
        for gate in self.oracle():
            yield gate
        for i, ish in enumerate(self.shift):
            if ish:
                yield f"x q[{i}];"
        for i in range(self.nqubits):
            yield f"h q[{i}];"
        for gate in self.oracle():
            yield gate
        for i in range(self.nqubits):
            yield f"h q[{i}];"
        #for i in range(self.nqubits):
        #    yield f"measure m[{i}];"

# TODO: Add QAOA circuit

class SupremacyCircuit(BaseCircuit):
    """Random circuit by Boixo et al 2018 for demonstrating quantum supremacy.

    See `https://github.com/quantumlib/Cirq/blob/v0.11.0/cirq-core/cirq/experiments/google_v2_supremacy_circuit.py`
    for the Cirq code.
    This circuit is constructed using `cirq` by exporting to OpenQASM and
    importing back to Qibo.
    """

    def __init__(self, nqubits, depth="2", seed="123"):
        super().__init__(nqubits)
        self.depth = int(depth)
        self.seed = int(seed)
        self.parameters = {"nqubits": nqubits, "depth": depth, "seed": seed}
        self.cirq_circuit = None

    def __iter__(self):
        raise NotImplementedError("Iteration is not available for "
                                  "`SupremacyCircuit` because it is prepared "
                                  "using Cirq.")

    def to_qasm(self):
        if self.cirq_circuit is None:
            import cirq
            from cirq.experiments import google_v2_supremacy_circuit as spc
            qubits = [cirq.GridQubit(i, 0) for i in range(self.nqubits)]
            self.cirq_circuit = spc.generate_boixo_2018_supremacy_circuits_v2(qubits, self.depth, self.seed)
        return self.cirq_circuit.to_qasm()
