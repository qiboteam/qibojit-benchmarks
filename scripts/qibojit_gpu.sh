#! /usr/bin/bash

GPUNAME=quadro_t2000
FILENAME=qibojit_gpu_$GPUNAME.dat
CIRCUIT=qft
PRECISION=double
export CUDA_VISIBLE_DEVICES=0
NREPS=20
for NQUBITS in {3..30}
do
    python compare.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --library-options backend=qibojit --nreps $NREPS  --precision $PRECISION
    echo
done
