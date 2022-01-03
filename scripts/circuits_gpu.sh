#! /usr/bin/bash

: "${filename:=circuits_gpu.dat}"
: "${precision:=double}"
: "${nreps:=20}"
: "${nqubits:=30}"

export CUDA_VISIBLE_DEVICES=0

for circuit in qft variational bv supremacy bc qv
do
  for library in qibo qiskit-gpu qsim-gpu qsim-cuquantum qulacs-gpu qcgpu
  do
    python compare.py --circuit $circuit --nqubits $nqubits --filename $filename --library $library --nreps $nreps --precision $precision
    echo
  done
done
