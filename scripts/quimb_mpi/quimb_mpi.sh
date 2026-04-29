#!/usr/bin/env bash
# MPI-enabled quimb benchmark sweep (2 processes).
# Tests both dense vector (non-expectation) and expectation across multiple
# qubit sizes and circuit types, using mpirun -np 2 to demonstrate MPI capability.
#
# Usage examples:
#   ./quimb_mpi.sh
#   nqubits_list="6 8 10" circuits="variational bv" ./quimb_mpi.sh
#   modes="expectation" nreps=3 ./quimb_mpi.sh
#   state_cfg=dense_vector_dense_mpi.json modes="dense_vector" ./quimb_mpi.sh
set -euo pipefail

: "${precision:=complex128}"
: "${nreps:=3}"
: "${filename:=quimb_benchmark_mpi.dat}"
: "${nlayers:=2}"
: "${nqubits_list:=6 8 10}"
: "${circuits:=supremacy qft variational qaoa}"
: "${modes:=dense_vector expectation}"
: "${np:=2}"
: "${exp_cfg:=}"
: "${state_cfg:=}"
: "${EXPECTATION_CONFIGS:=}"
: "${STATE_CONFIGS:=}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
cd "${repo_root}"

config_list_from_prefix() {
    local prefix="$1"
    local single_cfg="$2"
    local override_list="$3"

    if [[ -n "${override_list}" ]]; then
        for cfg in ${override_list}; do
            printf '%s\n' "${cfg}"
        done
        return
    fi

    if [[ -n "${single_cfg}" ]]; then
        printf '%s\n' "${single_cfg}"
        return
    fi

    shopt -s nullglob
    local matches=( "${script_dir}/${prefix}"*.json )
    shopt -u nullglob

    for path in "${matches[@]}"; do
        basename "${path}"
    done
}

require_existing_configs() {
    local mode="$1"
    shift

    for cfg in "$@"; do
        if [[ ! -f "${script_dir}/${cfg}" ]]; then
            echo "Missing ${mode} config: ${script_dir}/${cfg}" >&2
            exit 1
        fi
    done
}

read_pauli_pattern() {
    local cfg_path="$1"

    python - "${cfg_path}" <<'PY'
import json
import sys

try:
    with open(sys.argv[1], "r") as f:
        data = json.load(f)
    print(data.get("pauli_pattern", ""))
except Exception:
    print("")
PY
}

build_ref_pattern() {
    local base_pauli_pattern="$1"
    local nqubits="$2"

    python - "${base_pauli_pattern}" "${nqubits}" <<'PY'
import sys

p = sys.argv[1].upper()
n = int(sys.argv[2])

if not p:
    p = "X" + "I" * max(n - 1, 0)
if len(p) < n:
    p = p + ("I" * (n - len(p)))
else:
    p = p[:n]
print(p)
PY
}

run_qibojit_reference() {
    local nqubits="$1"
    local circuit="$2"
    local circuit_opts="$3"
    local exp_cfg_name="$4"
    local exp_cfg_path="${script_dir}/${exp_cfg_name}"
    local base_pauli_pattern
    local ref_pattern

    base_pauli_pattern="$(read_pauli_pattern "${exp_cfg_path}")"
    ref_pattern="$(build_ref_pattern "${base_pauli_pattern}" "${nqubits}")"

    echo "  [qibojit reference] cfg=${exp_cfg_name}"
    python compare.py \
        --circuit "${circuit}" \
        ${circuit_opts:+--circuit-options "${circuit_opts}"} \
        --nqubits "${nqubits}" \
        --filename "${filename}" \
        --library-options backend=qibojit,platform=numba,expectation=${ref_pattern} \
        --nreps "${nreps}" \
        --precision "${precision}"
}

mapfile -t expectation_cfgs < <(
    config_list_from_prefix "expectation" "${exp_cfg}" "${EXPECTATION_CONFIGS}"
)
mapfile -t state_cfgs < <(
    config_list_from_prefix "dense_vector" "${state_cfg}" "${STATE_CONFIGS}"
)

run_dense_mode=false
run_expectation_mode=false

if echo "${modes}" | grep -Eqw "dense_vector|statevector"; then
    run_dense_mode=true
fi

if echo "${modes}" | grep -qw "expectation"; then
    run_expectation_mode=true
fi

if [[ "${run_dense_mode}" == true && ${#state_cfgs[@]} -eq 0 ]]; then
    echo "No dense-vector JSON configs found in ${script_dir}" >&2
    exit 1
fi

if [[ "${run_expectation_mode}" == true && ${#expectation_cfgs[@]} -eq 0 ]]; then
    echo "No expectation JSON configs found in ${script_dir}" >&2
    exit 1
fi

require_existing_configs "dense-vector" "${state_cfgs[@]}"
require_existing_configs "expectation" "${expectation_cfgs[@]}"

# On Prism, Intel MPI needs shared-memory fabric for single-node runs.
if [[ -z "${I_MPI_FABRICS:-}" ]]; then
    export I_MPI_FABRICS=shm
fi

echo "Dense-vector configs : ${state_cfgs[*]:-none}"
echo "Expectation configs  : ${expectation_cfgs[*]:-none}"

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

        echo "===== nqubits=${nqubits}  circuit=${circuit}  np=${np} ====="

        # dense_vector is the preferred name; statevector is kept as a legacy alias.
        if [[ "${run_dense_mode}" == true ]]; then
            for cfg_name in "${state_cfgs[@]}"; do
                state_cfg_path="${script_dir}/${cfg_name}"
                echo "  [dense_vector MPI] cfg=${cfg_name}"
                mpirun -np "${np}" python compare.py \
                    --circuit "${circuit}" \
                    ${circuit_opts:+--circuit-options "${circuit_opts}"} \
                    --nqubits "${nqubits}" \
                    --filename "${filename}" \
                    --library-options backend=qibotn,platform=quimb,computation_settings=${state_cfg_path} \
                    --nreps "${nreps}" \
                    --precision "${precision}"
            done
        fi

        if [[ "${run_expectation_mode}" == true ]]; then
            for cfg_name in "${expectation_cfgs[@]}"; do
                exp_cfg_path="${script_dir}/${cfg_name}"
                echo "  [expectation MPI] cfg=${cfg_name}"
                mpirun -np "${np}" python compare.py \
                    --circuit "${circuit}" \
                    ${circuit_opts:+--circuit-options "${circuit_opts}"} \
                    --nqubits "${nqubits}" \
                    --filename "${filename}" \
                    --library-options backend=qibotn,platform=quimb,computation_settings=${exp_cfg_path} \
                    --nreps "${nreps}" \
                    --precision "${precision}"

                run_qibojit_reference "${nqubits}" "${circuit}" "${circuit_opts}" "${cfg_name}"
            done
        fi

        echo
    done
done
