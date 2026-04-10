# Quimb Benchmark Suite

Local (single-process) tensor network simulation benchmarking using quimb backend.

## Files

- **quimb_local.sh** — Main benchmark sweep script (no MPI)
- **expectation_mps.json** — Expectation mode with MPS (default for expectation)
- **expectation_dense.json** — Expectation mode, dense tensor network
- **dense_vector_mps.json** — State extraction with MPS (default for state)
- **dense_vector_dense.json** — State extraction, dense tensor network

## Configuration Files

### Expectation Modes (computing Hamiltonian expectation values)
- **expectation_mps.json**: Uses Matrix Product State (MPS) tensor network ansatz; good for larger systems with limited bond dimension
- **expectation_dense.json**: Uses dense tensor network; full contraction without MPS truncation

### State Modes (full state vector computation)
- **dense_vector_mps.json**: Extracts full state using MPS contraction (faster, bounded memory)
- **dense_vector_dense.json**: Extracts full state using dense tensor (maximum memory usage)

## Usage

```bash
cd /ssd_data/tankya2/code/ASC_2026_prism/ASC-2026/qibojit-benchmarks/scripts/quimb

# Run with defaults (MPS modes, both dense_vector and expectation)
./quimb_local.sh

# Test only expectation mode, custom qubit sizes
modes="expectation" nqubits_list="8 10 12" ./quimb_local.sh

# Test dense vector only with dense TN ansatz (no MPS)
state_cfg=dense_vector_dense.json modes="dense_vector" ./quimb_local.sh

# Test variational and BV circuits
circuits="variational bv" nqubits_list="6 8 10" nreps=3 ./quimb_local.sh
```

## Supported Circuits

### ✓ Fully Supported (Numerically Validated)

| Circuit | Alias | Parameters | Status | Notes |
|---------|-------|------------|--------|-------|
| **qft** | — | none | ✓ Works | Quantum Fourier Transform; aligned with qibojit |
| **variational** | — | nlayers | ✓ Works | Parameterized circuit; aligned with qibojit |
| **bv** | bernstein-vazirani | none | ✓ Works | Bernstein-Vazirani algorithm; aligned with qibojit |
| **hs** | hidden-shift | none | ✓ Works | Hidden-shift problem; aligned with qibojit |
| **qaoa** | — | nlayers | ✓ Works | QAOA with RZZ gate support; aligned with qibojit |

### ❌ Not Supported

| Circuit | Issue | Notes |
|---------|-------|-------|
| **qv** | Qiskit API compatibility | quantum-volume uses deprecated qiskit `.qasm()` method (v3.0+); not specific to quimb |

### Implementation Notes
- **RZZ Gate:** Full support for QAOA and algorithms using two-qubit Ising rotations
- **cu1 Gate:** Fully supported in expectation value mode (QFT compatible)
- **Numerical Alignment:** All benchmarks automatically include qibojit (numba) reference with identical observable for validation

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nqubits_list` | `6 8 10` | Space-separated qubit counts to benchmark |
| `circuits` | `qft variational bv` | Space-separated circuit names |
| `modes` | `dense_vector expectation` | Benchmark modes (dense_vector, expectation) |
| `nlayers` | `2` | Layers for layered circuits (variational, qaoa) |
| `nreps` | `1` | Repetitions per benchmark |
| `filename` | `quimb_benchmark_local.dat` | Output log file |
| `precision` | `complex128` | NumPy dtype (complex128 or complex64) |
| `exp_cfg` | `expectation_mps.json` | Expectation mode config file |
| `state_cfg` | `dense_vector_mps.json` | State mode config file |

## Results

Results are logged to `/qibojit-benchmarks/benchmarks/results/` with filename `quimb_benchmark_local.dat` (configurable).

Each benchmark includes:
- **import_time** — Backend initialization time
- **creation_time** — Circuit creation time
- **dry_run_time** — First execution time (warm-up)
- **simulation_times** — Execution times for nreps runs
- **expectation_result** — Observable expectation values (for expectation mode)

## Observable

By default, expectation uses:
- **X on qubit 0**, identity on remaining qubits
- Configurable via `pauli_pattern` in JSON config (e.g., `"XIIII"` for 5 qubits)

## Reference Validation

Each benchmark run automatically includes a **qibojit (numba) reference** with the same observable configuration, enabling direct numerical comparison for validation.

Example:
```
[expectation MPI] quimb + qft @ 6q:     0.2019...
[qibojit ref]     numba + qft @ 6q:     0.2019...  ✓ aligned
```

## MPI Support

For MPI-enabled benchmarking (multiple processes), see the parallel suite in `/scripts/quimb_mpi/`:

```bash
cd /ssd_data/tankya2/code/ASC_2026_prism/ASC-2026/qibojit-benchmarks/scripts/quimb_mpi
./quimb_mpi.sh  # runs with mpirun -np 2
```

## Tensor Network Options

Quimb supports both MPS (Matrix Product State) and dense tensor network contractions. These can be mixed:

```bash
# Compare MPS vs dense at same nqubits
exp_cfg=expectation_mps.json nqubits_list="12" ./quimb_local.sh
exp_cfg=expectation_dense.json nqubits_list="12" ./quimb_local.sh
```

MPS is typically faster and uses bounded memory, while dense provides full accuracy without truncation.

## Notes

- **Intel MPI Fabric:** On Prism cluster, shared-memory fabric (`I_MPI_FABRICS=shm`) is automatically enabled for single-node runs
- **QFT Support:** Fixed cu1 gate compatibility in quimb backend; no platform-specific gate limitations
- **Bond Dimension:** MPS modes use max_bond_dimension=20 by default; adjust in JSON for memory/accuracy tradeoff
