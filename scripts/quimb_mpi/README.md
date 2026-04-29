# Quimb MPI Benchmark Suite

Demonstrates MPI-enabled tensor network simulation using quimb with 2 MPI processes.

## Files

- **quimb_mpi.sh** — Main benchmark sweep script using `mpirun -np 2`
- **expectation_mps_mpi.json** — Expectation mode with MPS (default for expectation)
- **expectation_dense_mpi.json** — Expectation mode, dense tensor network
- **dense_vector_mps_mpi.json** — State extraction with MPS (default for state)
- **dense_vector_dense_mpi.json** — State extraction, dense tensor network

## Key Differences from `/scripts/quimb/`

- Each `python compare.py` call wrapped with `mpirun -np 2` to enable MPI parallelization
- All JSON configs include `"MPI_enabled": true`
- Default file names include `_mpi` suffix to distinguish from single-process configs
- Filenames in logs clearly show MPI mode (e.g., `expectation_mps_mpi.json`)

## Configuration Files

### Expectation Modes (computing Hamiltonian expectation values)
- **expectation_mps_mpi.json**: MPI-enabled, uses Matrix Product State (MPS) tensor network ansatz; good for larger systems with limited bond dimension
- **expectation_dense_mpi.json**: MPI-enabled, uses dense tensor network; full contraction without MPS truncation

### State Modes (full state vector computation)
- **dense_vector_mps_mpi.json**: MPI-enabled, extracts full state using MPS contraction (faster, bounded memory)
- **dense_vector_dense_mpi.json**: MPI-enabled, extracts full state using dense tensor (maximum memory usage)

## Usage

```bash
cd /ssd_data/tankya2/code/ASC_2026_prism/ASC-2026/qibojit-benchmarks/scripts/quimb_mpi

# Run with defaults (all matching dense_vector*.json and expectation*.json configs)
./quimb_mpi.sh

# Test only expectation mode, custom qubit sizes
modes="expectation" nqubits_list="8 10 12" ./quimb_mpi.sh

# Test dense vector only with one explicit config
state_cfg=dense_vector_dense_mpi.json modes="dense_vector" ./quimb_mpi.sh

# Restrict the sweep to a chosen subset of configs
EXPECTATION_CONFIGS="expectation_mps_mpi.json expectation_dense_mpi.json" ./quimb_mpi.sh

# Use 4 MPI processes (if testing scalability)
np=4 ./quimb_mpi.sh
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

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nqubits_list` | `6 8 10` | Space-separated qubit counts to benchmark |
| `circuits` | `qaoa` | Space-separated circuit names |
| `modes` | `dense_vector expectation` | Benchmark modes (dense_vector, expectation) |
| `nlayers` | `2` | Layers for layered circuits (variational, qaoa) |
| `np` | `2` | Number of MPI processes (mpirun -np) |
| `nreps` | `1` | Repetitions per benchmark |
| `filename` | `quimb_benchmark_mpi.dat` | Output log file |
| `precision` | `complex128` | NumPy dtype (complex128 or complex64) |
| `exp_cfg` | unset | Optional single expectation config; when unset, all `expectation*.json` files are swept |
| `state_cfg` | unset | Optional single dense-vector config; when unset, all `dense_vector*.json` files are swept |
| `EXPECTATION_CONFIGS` | unset | Optional space-separated subset of expectation configs to run |
| `STATE_CONFIGS` | unset | Optional space-separated subset of dense-vector configs to run |

## Results

Results are stored in `/qibojit-benchmarks/benchmarks/results/` with filename prefix `quimb_benchmark_mpi.dat` by default (configurable via `filename=` env var).

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
[expectation MPI]   quimb + variational @ 6q:    0.2019...
[qibojit ref]       numba + variational @ 6q:    0.2019...  ✓ aligned
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

## Notes

- **Intel MPI Fabric:** On Prism, automatically sets `I_MPI_FABRICS=shm` (shared-memory fabric) for single-node local runs
- **Observable:** X on first qubit, identity on rest (configurable via `pauli_pattern` in JSON)
- **Reference:** qibojit (numba backend) included automatically with aligned observable for validation
- **RZZ Gate:** Full support for QAOA and algorithms using two-qubit Ising rotations
- **cu1 Gate:** Fully supported in expectation value mode (QFT compatible)
- **Numerical Alignment:** All benchmarks automatically include qibojit reference with identical observable for validation

## MPI Enable/Disable

To test without MPI, use configs from `/scripts/quimb/` instead:

```bash
# Compare: MPI vs no MPI
./quimb_mpi.sh                    # with MPI (2 processes)
cd ../quimb && ./quimb_local.sh   # without MPI (single process)
```

## Tensor Network Options

Quimb supports both MPS (Matrix Product State) and dense tensor network contractions. By default the script sweeps every matching JSON file in this folder, or you can target individual configs:

```bash
# Compare MPS vs dense at same nqubits with MPI
exp_cfg=expectation_mps_mpi.json nqubits_list="12" ./quimb_mpi.sh
exp_cfg=expectation_dense_mpi.json nqubits_list="12" ./quimb_mpi.sh
```

MPS is typically faster and uses bounded memory, while dense provides full accuracy without truncation.

## Additional Notes

- **Bond Dimension:** MPS modes use max_bond_dimension=20 by default; adjust in JSON for memory/accuracy tradeoff
- **SVD Cutoff:** Set to 1e-10 for high accuracy; increase for faster execution with acceptable loss tolerance
- **Scaling:** MPI parallelization enables larger systems; test with np=4, np=8, etc. for scaling studies
- **Single-Node MPI:** Default `-np 2` demonstrates MPI capability on local machine; for cluster runs, adjust `-np` and node configuration
