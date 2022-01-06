#! /usr/bin/bash

: "${filename:=qibo_gpu.dat}"
: "${backend=qibojit}"
: "${precision:=double}"
: "${nreps:=20}"
: "${nqubits:=30}"

export CUDA_VISIBLE_DEVICES=0

for circuit in qft variational bv supremacy qv
do
  python compare.py --circuit $circuit --nqubits $nqubits --filename $filename --library-options backend=$backend --nreps $nreps --precision $precision
  echo
done
