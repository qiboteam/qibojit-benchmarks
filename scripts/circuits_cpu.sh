#! /usr/bin/bash

FILENAME=circuits_cpu.dat
NQUBITS=30
export CUDA_VISIBLE_DEVICES=""
NREPS=20
for CIRCUIT in qft variational bv supremacy bc qv
do
  for LIBRARY in qibo qiskit qsim qulacs projectq hybridq
  do
    python compare.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --library $LIBRARY --nreps $NREPS
    echo
  done
done
