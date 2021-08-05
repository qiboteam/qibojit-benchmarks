"""Check that execution of circuits from external library agrees with Qibo."""
import pytest
import numpy as np
from qibo import models, gates
from benchmarks import circuits
from benchmarks.external import qasm, libraries


def assert_circuit_execution(backend, qasm_circuit, qibo_circuit_iter, atol=1e-10):
    circuit = backend.from_qasm(qasm_circuit.to_qasm())
    final_state = backend(circuit)
    target_circuit = models.Circuit(qibo_circuit_iter.nqubits)
    target_circuit.add(qibo_circuit_iter)
    target_state = target_circuit()
    np.testing.assert_allclose(final_state, target_state, atol=atol)


@pytest.mark.parametrize("nlayers", ["1", "4"])
@pytest.mark.parametrize("gate, qibo_gate",
                         [("h", "H"), ("x", "X"), ("y", "Y"), ("z", "Z")])
def test_one_qubit_gate(nqubits, library, nlayers, gate, qibo_gate):
    qasm_circuit = qasm.OneQubitGate(nqubits, nlayers=nlayers, gate=gate)
    target_circuit = circuits.OneQubitGate(nqubits, nlayers=nlayers,
                                           gate=qibo_gate)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("gate,qibo_gate,params",
                         [("rx", "RX", {"theta": 0.1}),
                          ("rz", "RZ", {"theta": 0.2}),
                          ("u1", "U1", {"theta": 0.3}),
                          #("u2", "U2", {"phi": 0.2, "lam": 0.3}),
                          ("u3", "U3", {"theta": 0.1, "phi": 0.2, "lam": 0.3})])
def test_one_qubit_gate_parametrized(nqubits, library, gate, qibo_gate, params):
    order = ["theta", "phi", "lam"]
    angles = ",".join(str(params.get(n)) for n in order if n in params)
    qasm_circuit = qasm.OneQubitGate(nqubits, gate=gate, angles=angles)
    target_circuit = circuits.OneQubitGate(nqubits, gate=qibo_gate, **params)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("nlayers", ["1", "4"])
@pytest.mark.parametrize("gate,qibo_gate",
                         [("cx", "CNOT"), ("swap", "SWAP"),
                          ("cz", "CZ")])
def test_two_qubit_gate_benchmark(nqubits, library, nlayers, gate, qibo_gate):
    qasm_circuit = qasm.TwoQubitGate(nqubits, nlayers=nlayers, gate=gate)
    target_circuit = circuits.TwoQubitGate(nqubits, nlayers=nlayers,
                                           gate=qibo_gate)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("swaps", ["False", "True"])
def test_qft_benchmark(nqubits, library, swaps):
    qasm_circuit = qasm.QFT(nqubits, swaps=swaps)
    target_circuit = circuits.QFT(nqubits, swaps=swaps)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("nlayers", ["2", "5"])
def test_variational_benchmark(nqubits, library, nlayers):
    # TODO: Make `theta` parameters equivalent between two circuits
    qasm_circuit = qasm.VariationalCircuit(nqubits, nlayers=nlayers)
    target_circuit = circuits.VariationalCircuit(nqubits, nlayers=nlayers)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)
