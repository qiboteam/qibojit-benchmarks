#! /usr/bin/bash

# Command-line parameters
: "${backend:=qibojit}"
: "${precision:=double}"
: "${nreps:=10}"


for nqubits in 18 24 28
do
    for circuit in qft variational supremacy qv bv
    do
        CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_circuits.dat \
                                                  --library-options backend=$backend --nreps $nreps --precision $precision
        echo
    done
done

