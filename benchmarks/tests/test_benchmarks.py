import pytest
from benchmarks.scripts import circuit_benchmark


def assert_logs(logs, nqubits, backend, nreps=1):
    assert logs[-1]["nqubits"] == nqubits
    assert logs[-1]["backend"] == backend
    assert logs[-1]["simulation_times_mean"] >= 0
    assert logs[-1]["transfer_times_mean"] >= 0
    assert len(logs[-1]["simulation_times"]) == nreps
    assert len(logs[-1]["transfer_times"]) == nreps


@pytest.mark.parametrize("transfer", [False, True])
@pytest.mark.parametrize("nreps", [1, 5])
@pytest.mark.parametrize("swaps", [False, True])
def test_qft_benchmark(nqubits, backend, nreps, transfer, swaps):
    logs = circuit_benchmark(nqubits, backend, circuit_name="qft",
                             nreps=nreps, transfer=transfer,
                             options=f"swaps={swaps}")
    assert_logs(logs, nqubits, backend, nreps)
    target_options = f"nqubits={nqubits}, swaps={swaps}"
    assert logs[-1]["circuit"] == "qft"
    assert logs[-1]["options"] == target_options


@pytest.mark.parametrize("varlayer", [False, True])
def test_variational_benchmark(nqubits, backend, varlayer):
    logs = circuit_benchmark(nqubits, backend, circuit_name="variational",
                             options=f"varlayer={varlayer}")
    assert_logs(logs, nqubits, backend)
    target_options = f"nqubits={nqubits}, nlayers=1, varlayer={varlayer}"
    assert logs[-1]["circuit"] == "variational"
    assert logs[-1]["options"] == target_options

# TODO: Test OneQubitGate and TwoQubitGate circuits

def test_bernstein_vazirani_benchmark(nqubits, backend):
    logs = circuit_benchmark(nqubits, backend, circuit_name="bv")
    assert_logs(logs, nqubits, backend)
    assert logs[-1]["circuit"] == "bv"
    assert logs[-1]["options"] == f"nqubits={nqubits}"


@pytest.mark.parametrize("random", [True, False])
def test_hidden_shift_benchmark(nqubits, backend, random):
    shift = "" if random else nqubits * "0"
    logs = circuit_benchmark(nqubits, backend, circuit_name="hs",
                             options=f"shift={shift}")
    assert_logs(logs, nqubits, backend)
    target_options = f"nqubits={nqubits}, shift={shift}"
    assert logs[-1]["circuit"] == "hs"
    assert logs[-1]["options"] == target_options


def test_qaoa_benchmark(backend):
    logs = circuit_benchmark(4, backend, circuit_name="qaoa")
    assert_logs(logs, 4, backend)
    target_options = f"nqubits=4, nparams=2, graph="
    assert logs[-1]["circuit"] == "qaoa"
    assert logs[-1]["options"] == target_options


@pytest.mark.parametrize("depth", ["2", "5", "10"])
def test_supremacy_benchmark(nqubits, backend, depth):
    logs = circuit_benchmark(nqubits, backend, circuit_name="supremacy",
                             options=f"depth={depth}")
    assert_logs(logs, nqubits, backend)
    target_options = f"nqubits={nqubits}, depth={depth}, seed=123"
    assert logs[-1]["circuit"] == "supremacy"
    assert logs[-1]["options"] == target_options


@pytest.mark.parametrize("simtime", ["1", "2.5"])
def test_basis_change_benchmark(nqubits, backend, simtime):
    logs = circuit_benchmark(nqubits, backend, circuit_name="bc",
                             options=f"simulation_time={simtime}")
    assert_logs(logs, nqubits, backend)
    target_options = f"nqubits={nqubits}, simulation_time={simtime}, seed=123"
    assert logs[-1]["circuit"] == "bc"
    assert logs[-1]["options"] == target_options


@pytest.mark.parametrize("depth", ["2", "5", "8"])
def test_quantum_volume_benchmark(nqubits, backend, depth):
    logs = circuit_benchmark(nqubits, backend, circuit_name="qv",
                             options=f"depth={depth}")
    assert_logs(logs, nqubits, backend)
    target_options = f"nqubits={nqubits}, depth={depth}, seed=123"
    assert logs[-1]["circuit"] == "qv"
    assert logs[-1]["options"] == target_options
