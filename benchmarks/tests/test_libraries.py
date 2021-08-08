"""Check that execution of circuits from external simulation libraries agrees with Qibo."""
import pytest
import numpy as np
from qibo import models, gates
from benchmarks import circuits, qasm, libraries


def assert_circuit_execution(backend, qasm_circuit, qibo_circuit_iter, atol=1e-10):
    circuit = backend.from_qasm(qasm_circuit.to_qasm())
    final_state = backend(circuit)
    final_state = backend.transpose_state(final_state)
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
                          ("ry", "RY", {"theta": 0.3}),
                          ("rz", "RZ", {"theta": 0.2}),
                          ("u1", "U1", {"theta": 0.3}),
                          ("u2", "U2", {"phi": 0.2, "lam": 0.3}),
                          ("u3", "U3", {"theta": 0.1, "phi": 0.2, "lam": 0.3})])
def test_one_qubit_gate_parametrized(nqubits, library, gate, qibo_gate, params):
    order = ["theta", "phi", "lam"]
    if "lam" in params: # correct phase for different U2, U3 Qiskit conventions
        # see `https://qiskit.org/documentation/stubs/qiskit.circuit.library.U2Gate.html`
        params["lam"] = 4 * np.pi - params["phi"]
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


# disabled gates that are not supported by Qiskit OpenQASM
@pytest.mark.parametrize("gate,qibo_gate,params",
                         [#("crx", "CRX", {"theta": 0.1}),
                          #("crz", "CRZ", {"theta": 0.2}),
                          ("cu1", "CU1", {"theta": 0.3}),
                          #("cu2", "CU2", {"phi": 0.1, "lam": 0.3}),
                          ("cu3", "CU3", {"theta": 0.1, "phi": 0.2, "lam": 0.3})])
def test_two_qubit_gate_parametrized(nqubits, library, gate, qibo_gate, params):
    order = ["theta", "phi", "lam"]
    if "lam" in params: # correct phase for different U2, U3 Qiskit conventions
        # see `https://qiskit.org/documentation/stubs/qiskit.circuit.library.U2Gate.html`
        params["lam"] = 4 * np.pi - params["phi"]
    angles = ",".join(str(params.get(n)) for n in order if n in params)
    qasm_circuit = qasm.TwoQubitGate(nqubits, gate=gate, angles=angles)
    target_circuit = circuits.TwoQubitGate(nqubits, gate=qibo_gate, **params)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("swaps", ["False", "True"])
def test_qft(nqubits, library, swaps):
    qasm_circuit = qasm.QFT(nqubits, swaps=swaps)
    target_circuit = circuits.QFT(nqubits, swaps=swaps)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("nlayers", ["2", "5"])
def test_variational(nqubits, library, nlayers):
    qasm_circuit = qasm.VariationalCircuit(nqubits, nlayers=nlayers)
    target_circuit = circuits.VariationalCircuit(nqubits, nlayers=nlayers)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


def test_bernstein_vazirani(nqubits, library):
    qasm_circuit = qasm.BernsteinVazirani(nqubits)
    target_circuit = circuits.BernsteinVazirani(nqubits)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


def test_hidden_shift(nqubits, library):
    shift = "".join(str(x) for x in np.random.randint(0, 2, size=(nqubits,)))
    qasm_circuit = qasm.HiddenShift(nqubits, shift=shift)
    target_circuit = circuits.HiddenShift(nqubits, shift=shift)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)


@pytest.mark.parametrize("depth", ["2", "5", "10"])
def test_supremacy_circuit(nqubits, library, depth):
    qasm_circuit = qasm.SupremacyCircuit(nqubits, depth=depth)
    target_circuit = circuits.SupremacyCircuit(nqubits, depth=depth)
    backend = libraries.get(library)
    assert_circuit_execution(backend, qasm_circuit, target_circuit)
