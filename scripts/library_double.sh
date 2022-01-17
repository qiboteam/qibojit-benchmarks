#! /usr/bin/bash

: "${nreps:=10}"


for nqubits in 20 30
do
	for circuit in qft variational bv supremacy qv
  do
    for library in qibo qiskit qulacs projectq hybridq
    do
      CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename library_cpu.dat \
                                                --library $library --nreps $nreps --precision double
      echo
    done
    for library in qibo qiskit-gpu qulacs-gpu hybridq-gpu
    do
      CUDA_VISIBLE_DEVICES=0  python compare.py --circuit $circuit --nqubits $nqubits --filename library_gpu.dat \
                                                --library $library --nreps $nreps --precision double
      echo
	  done
	done
done
