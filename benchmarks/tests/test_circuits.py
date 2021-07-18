import pytest
from benchmarks import circuits
from qibo.models import Circuit


def test_bernstein_vazirani_circuit():
    circuit = Circuit(28)
    gates = circuits.BernsteinVazirani(28)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.depth == 30
    assert circuit.ngates == 83
