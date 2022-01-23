#! /usr/bin/bash

: "${filename:=qibojit.dat}"
: "${circuit:=qft}"
: "${precision:=double}"
: "${nreps:=10}"
: "${platform:=cupy}"


for nqubits in {3..31}
do
    CUDA_VISIBLE_DEVICES=0  python compare.py --circuit $circuit --nqubits $nqubits --filename $filename \
                                              --library-options backend=qibojit,platform=$platform \
                                              --nreps $nreps --precision $precision
done
