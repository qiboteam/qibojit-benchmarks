#!/usr/bin/env bash
# Local quimb benchmark sweep.
# Tests both dense vector (non-expectation) and expectation across multiple
# qubit sizes and circuit types.
#
# Usage examples:
#   ./quimb_local.sh
#   nqubits_list="6 8 10" circuits="variational bv" ./quimb_local.sh
#   modes="expectation" nreps=3 ./quimb_local.sh
set -euo pipefail

: "${precision:=complex128}"
: "${nreps:=3}"
: "${filename:=quimb_benchmark_local.dat}"
: "${nlayers:=2}"
: "${nqubits_list:=6 8 10}"
: "${circuits:=supremacy qft variational bv qaoa}"
: "${modes:=dense_vector expectation}"
: "${exp_cfg:=expectation_mps.json}"
: "${state_cfg:=dense_vector_mps.json}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
exp_cfg_path="${script_dir}/${exp_cfg}"
state_cfg_path="${script_dir}/${state_cfg}"
cd "${repo_root}"

# Read pauli_pattern from quimb expectation config (if present).
base_pauli_pattern="$(python - <<PY
import json
try:
    with open(r"${exp_cfg_path}", "r") as f:
        data = json.load(f)
    print(data.get("pauli_pattern", ""))
except Exception:
    print("")
PY
)"

# On Prism, Intel MPI needs shared-memory fabric for single-node runs.
if [[ -z "${I_MPI_FABRICS:-}" ]]; then
    export I_MPI_FABRICS=shm
fi

for nqubits in ${nqubits_list}; do
    for circuit in ${circuits}; do
        circuit_opts="nlayers=${nlayers}"
        # These circuits do not use nlayers — omit it to avoid unknown-option errors.
        if [[ "${circuit}" == "qft" || "${circuit}" == "QFT" || \
              "${circuit}" == "supremacy" || "${circuit}" == "Supremacy" || \
              "${circuit}" == "bv" || "${circuit}" == "bernstein-vazirani" || \
              "${circuit}" == "hs" || "${circuit}" == "hidden-shift" || \
              "${circuit}" == "qaoa" || "${circuit}" == "qv" || \
              "${circuit}" == "quantum-volume" ]]; then
            circuit_opts=""
        fi

        echo "===== nqubits=${nqubits}  circuit=${circuit} ====="

        # Build qibojit pattern aligned to the effective quimb observable at this nqubits.
        # If base pattern is shorter, pad with I; if longer, truncate.
        ref_pattern="$(python - <<PY
p = "${base_pauli_pattern}".upper()
n = int("${nqubits}")
if not p:
    p = "X" + "I" * (max(n - 1, 0))
if len(p) < n:
    p = p + ("I" * (n - len(p)))
else:
    p = p[:n]
print(p)
PY
)"

        # dense_vector is the preferred name; statevector is kept as a legacy alias.
        if echo "${modes}" | grep -Eqw "dense_vector|statevector"; then
            echo "  [dense_vector]"
            python compare.py \
                --circuit "${circuit}" \
                ${circuit_opts:+--circuit-options "${circuit_opts}"} \
                --nqubits "${nqubits}" \
                --filename "${filename}" \
                --library-options backend=qibotn,platform=quimb,computation_settings=${state_cfg_path} \
                --nreps "${nreps}" \
                --precision "${precision}"
        fi

        if echo "${modes}" | grep -qw "expectation"; then
            echo "  [expectation]"
            python compare.py \
                --circuit "${circuit}" \
                ${circuit_opts:+--circuit-options "${circuit_opts}"} \
                --nqubits "${nqubits}" \
                --filename "${filename}" \
                --library-options backend=qibotn,platform=quimb,computation_settings=${exp_cfg_path} \
                --nreps "${nreps}" \
                --precision "${precision}"
        fi

        echo "  [qibojit reference]"
        python compare.py \
            --circuit "${circuit}" \
            ${circuit_opts:+--circuit-options "${circuit_opts}"} \
            --nqubits "${nqubits}" \
            --filename "${filename}" \
            --library-options backend=qibojit,platform=numba,expectation=${ref_pattern} \
            --nreps "${nreps}" \
            --precision "${precision}"

        echo
    done
done
