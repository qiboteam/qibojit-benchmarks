#! /usr/bin/bash

# Command-line parameters
: "${circuit:=qft}"
: "${precision:=double}"

# Internal settings
NREPS_A=20
NREPS_B=3

# NumPy backend
for nqubits in {3..24}
do
  CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_cpu.dat \
		                  						          --library-options backend=numpy --nreps $NREPS_A --precision $precision
  echo
done
for nqubits in {25..28}
do
  CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_cpu.dat \
		                  						          --library-options backend=numpy --nreps $NREPS_B --precision $precision
  echo
done

# Other backends
for nqubits in {3..24}
do
  for backend in tensorflow qibotf qibojit
  do
    CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_cpu.dat \
                                              --library-options backend=$backend --nreps $NREPS_A --precision $precision
    echo
    CUDA_VISIBLE_DEVICES=0  python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_gpu.dat \
                                              --library-options backend=$backend --nreps $NREPS_A --precision $precision
    echo
  done
done
for nqubits in {25..31}
do
  for backend in tensorflow qibotf qibojit
  do
    CUDA_VISIBLE_DEVICES="" python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_cpu.dat \
                                              --library-options backend=$backend --nreps $NREPS_B --precision $precision
    echo
    CUDA_VISIBLE_DEVICES=0  python compare.py --circuit $circuit --nqubits $nqubits --filename qibo_gpu.dat \
                                    --library-options backend=$backend --nreps $NREPS_B --precision $precision
    echo
  done
done
