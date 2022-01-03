#! /usr/bin/bash

: "${filename:=qibojit_gpu.dat}"
: "${circuit:=qft}"
: "${precision:=double}"
: "${nreps:=20}"
: "${min_qubits:=3}"
: "${max_qubits:=30}"

export CUDA_VISIBLE_DEVICES=0

for ((nqubits=min_qubits; nqubits<=max_qubits; nqubits++));
do
    python compare.py --circuit $circuit --nqubits $nqubits --filename $filename --library-options backend=qibojit --nreps $nreps  --precision $precision
    echo
done
