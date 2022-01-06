#! /usr/bin/bash

: "${filename:=circuits_cpu.dat}"
: "${library:=qibo}"
: "${precision:=double}"
: "${nreps:=20}"
: "${nqubits:=30}"

export CUDA_VISIBLE_DEVICES=""

for circuit in qft variational bv supremacy qv
do
  python compare.py --circuit $circuit --nqubits $nqubits --filename $filename --library $library --nreps $nreps --precision $precision
  echo
done
