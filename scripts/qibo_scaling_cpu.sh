#! /usr/bin/bash

FILENAME=qibo_scaling_cpu.dat
CIRCUIT=qft
export CUDA_VISIBLE_DEVICES=""
NREPS=20
for NQUBITS in {3..30}
do
  for BACKEND in numpy tensorflow qibotf qibojit
  do
    python compare.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --nreps $NREPS
    echo
  done
done
