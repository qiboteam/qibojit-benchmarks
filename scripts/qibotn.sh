#! /usr/bin/bash
# Generates data for qibotn breakdown bar plot with dry run vs simulation

# Command-line parameters
: "${filename:=qibotn.dat}"
: "${precision:=double}"
: "${circuit:=qft}"
: "${nreps_cpu:=5}"
: "${nreps_gpu:=10}"


for nqubits in 16 18 20 22 24 26 28
do
    echo "nqubits = $nqubits"
    # CUDA_VISIBLE_DEVICES=0 python compare.py --circuit $circuit --nqubits $nqubits --filename $filename \
    #                                          --library-options backend=qibotn,platform=cupy --nreps $nreps_gpu --precision $precision
    echo "qibotn with quimb done."
    # CUDA_VISIBLE_DEVICES=0 python compare.py --circuit $circuit --nqubits $nqubits --filename $filename \
    #                                          --library-options backend=qibotn,platform=cuquantum --nreps $nreps_gpu --precision $precision
    echo "qibotn with cuquantum done."
    #  CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename $filename \
    #                                            --library-options backend=qibotn,platform=numba --nreps $nreps_cpu --precision $precision
    echo "qibotn with cpu done."
done
