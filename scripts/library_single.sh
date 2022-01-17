#! /usr/bin/bash

: "${nreps:=10}"


for nqubits in 20 30
do
	for circuit in qft variational bv supremacy qv
  do
    for library in qibo qiskit qsim hybridq
    do
      CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename library_cpu.dat \
                                                --library $library --nreps $nreps --precision single
      echo
    done
    for library in qibo qiskit-gpu qsim-gpu qsim-cuquantum qcgpu hybridq-gpu
    do
      CUDA_VISIBLE_DEVICES=0  python compare.py --circuit $circuit --nqubits $nqubits --filename library_gpu.dat \
                                                --library $library --nreps $nreps --precision single
      echo
	  done
	done
done
