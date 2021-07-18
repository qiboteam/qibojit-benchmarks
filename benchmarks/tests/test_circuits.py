import pytest
from benchmarks import circuits
from qibo.models import Circuit


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


def test_bernstein_vazirani_circuit():
    circuit = Circuit(28)
    gates = circuits.BernsteinVazirani(28)
    circuit.add(gates)
    assert circuit.nqubits == 28
    assert circuit.depth == 30
    assert circuit.ngates == 83
