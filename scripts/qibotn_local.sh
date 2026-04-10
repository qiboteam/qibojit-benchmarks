#!/usr/bin/env bash
# Lightweight local benchmark script (single node, small sweep)
set -euo pipefail

: "${circuit:=variational}"
: "${precision:=complex128}"
: "${nreps:=1}"
: "${filename:=qibotn_expectation_local.dat}"
: "${np:=2}"
: "${nlayers:=2}"
: "${nqubits_list:=8 12 16}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
cd "${repo_root}"

# On Prism, Intel MPI may need shared-memory fabric for local runs.
if [[ -z "${I_MPI_FABRICS:-}" ]]; then
    export I_MPI_FABRICS=shm
fi

for nqubits in ${nqubits_list}; do
    echo "===== nqubits=${nqubits} ====="

    # MPI-enabled cutensornet expectation
    mpirun -np "${np}" python compare.py \
        --circuit "${circuit}" \
        --circuit-options "nlayers=${nlayers}" \
        --nqubits "${nqubits}" \
        --filename "${filename}" \
        --library-options backend=qibotn,platform=cutensornet,computation_settings=scripts/cu_tensornet_mpi_expectation.json \
        --nreps "${nreps}" \
        --precision "${precision}"

    # Single-process cutensornet expectation
    python compare.py \
        --circuit "${circuit}" \
        --circuit-options "nlayers=${nlayers}" \
        --nqubits "${nqubits}" \
        --filename "${filename}" \
        --library-options backend=qibotn,platform=cutensornet,computation_settings=scripts/cu_tensornet_expectation.json \
        --nreps "${nreps}" \
        --precision "${precision}"

    # qibojit reference
    python compare.py \
        --circuit "${circuit}" \
        --circuit-options "nlayers=${nlayers}" \
        --nqubits "${nqubits}" \
        --filename "${filename}" \
        --library-options backend=qibojit,platform=numba,expectation=XXXZ \
        --nreps "${nreps}" \
        --precision "${precision}"

    echo
 done
