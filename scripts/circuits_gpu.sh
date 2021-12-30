#! /usr/bin/bash

FILENAME=circuits_gpu.dat
NQUBITS=30
export CUDA_VISIBLE_DEVICES=0
NREPS=20
for CIRCUIT in qft variational bv supremacy bc qv
do
  for LIBRARY in qibo qiskit-gpu qsim-gpu qsim-cuquantum qulacs-gpu qcgpuss
  do
    python compare.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --library $LIBRARY --nreps $NREPS
    echo
  done
done
