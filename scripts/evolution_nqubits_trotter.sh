#! /usr/bin/bash

# Command-line parameters
: "${dt:=0.05}"
: "${precision:=double}"
: "${filename:=qibo_evolution_nqubits_trotter.dat}"

# Internal settings
NREPS_A=10
NREPS_B=3

# GPU qibojit backend
for nqubits in {3..24}
do
  for platform in cupy cuquantum
  do
    CUDA_VISIBLE_DEVICES="0" python evolution.py --nqubits $nqubits --dt $dt --filename $filename --nreps $NREPS_A \
  		                  	  					           --backend qibojit --platform $platform --precision $precision
    echo
  done
done
for nqubits in {24..31}
do
  for platform in cupy cuquantum
  do
    CUDA_VISIBLE_DEVICES="0" python evolution.py --nqubits $nqubits --dt $dt --filename $filename --nreps $NREPS_B \
  		                  	  					           --backend qibojit --platform $platform --precision $precision
    echo
  done
done

# GPU TensorFlow and QiboTF backends
for nqubits in {3..24}
do
  for backend in qibotf tensorflow
  do
    CUDA_VISIBLE_DEVICES="0" python evolution.py --nqubits $nqubits --dt $dt --filename $filename --nreps $NREPS_A \
  		                  						             --backend $backend --precision $precision
    echo
  done
done
for nqubits in {25..31}
do
  for backend in qibotf tensorflow
  do
    CUDA_VISIBLE_DEVICES="0" python evolution.py --nqubits $nqubits --dt $dt --filename $filename --nreps $NREPS_B \
  		                  						             --backend $backend --precision $precision
    echo
  done
done

# CPU all backends
for nqubits in {3..24}
do
  for backend in qibojit qibotf tensorflow numpy
  do
    CUDA_VISIBLE_DEVICES="" python evolution.py --nqubits $nqubits --dt $dt --filename $filename --nreps $NREPS_A \
  		                  						            --backend $backend --precision $precision
    echo
  done
done
for nqubits in {25..31}
do
  for backend in qibojit qibotf tensorflow numpy
  do
    CUDA_VISIBLE_DEVICES="" python evolution.py --nqubits $nqubits --dt $dt --filename $filename --nreps $NREPS_B \
  		                  						            --backend $backend --precision $precision
    echo
  done
done
