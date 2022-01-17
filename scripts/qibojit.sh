#! /usr/bin/bash

: "${filename:=qibojit.dat}"
: "${circuit:=qft}"
: "${precision:=double}"
: "${nreps:=10}"


for nqubits in {3..31}
do
    CUDA_VISIBLE_DEVICES=0  python compare.py --circuit $circuit --nqubits $nqubits --filename $filename \
                                              --library-options backend=qibojit --nreps $nreps --precision $precision
done
