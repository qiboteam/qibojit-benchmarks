import pytest
from qibo.models import Circuit
from benchmarks.circuits import qibo


@pytest.mark.parametrize("swaps", ["True", "False"])
def test_qft_circuit(swaps):
    circuit = Circuit(28)
    gates = circuits.QFT(28, swaps=swaps)
    circuit.add(gates)
    assert circuit.nqubits == 28
    if swaps == "True":
        assert circuit.depth == 56
        assert circuit.ngates == 420
    else:
        assert circuit.depth == 55
        assert circuit.ngates == 406


@pytest.mark.parametrize("varlayer", ["True", "False"])
def test_variational_circuit(varlayer):
    circuit = Circuit(28)
    gates = qibo.VariationalCircuit(28, varlayer=varlayer)
    circuit.add(gates)
    assert circuit.nqubits == 28
    if varlayer == "True":
        assert circuit.depth == 2
        assert circuit.ngates == 28
    else:
        assert circuit.depth == 4
        assert circuit.ngates == 84


def test_bernstein_vazirani_circuit():
    circuit = Circuit(28)
    gates = qibo.BernsteinVazirani(28)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.depth == 30
    assert circuit.ngates == 83


def test_hidden_shift_circuit():
    shift = "0111001011001001111011001101"
    circuit = Circuit(28)
    gates = qibo.HiddenShift(28, shift=shift)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.depth == 7
    assert circuit.ngates == 144


def test_qaoa_circuit():
    import pathlib
    folder = str(pathlib.Path(__file__).with_name("graphs") / "testgraph28.json")
    circuit = Circuit(28)
    gates = qibo.QAOA(28, graph=folder)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.ngates == 168
    assert circuit.depth == 18


def test_qasm_circuit():
    qasm = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[5];
    rz(pi*-0.4229927754) q[4];
    rz(pi*0.25) q[3];
    rz(pi*-0.25) q[4];
    cx q[3],q[4];
    h q[3];"""
    circuit = Circuit(5)
    gates = qibo.QASMCircuit(5, qasm=qasm)
    circuit.add(gates)
    assert circuit.nqubits == 5
    assert circuit.depth == 4
    assert circuit.ngates == 5


def test_supremacy_circuit():
    circuit = Circuit(28)
    gates = qibo.SupremacyCircuit(28, depth="40")
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.ngates == 880
    assert circuit.depth == 42


def test_basis_change_circuit():
    circuit = Circuit(28)
    gates = qibo.BasisChange(28)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.ngates == 9912
    assert circuit.depth == 1117


def test_quantum_volume_circuit():
    circuit = Circuit(28)
    gates = qibo.QuantumVolume(28, depth=10)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.ngates == 1540
    assert circuit.depth == 70
