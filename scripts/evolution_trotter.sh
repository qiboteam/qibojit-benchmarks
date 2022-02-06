#! /usr/bin/bash

# Command-line parameters
: "${nqubits:=10}"
: "${precision:=double}"
: "${filename:=qibo_evolution_trotter.dat}"
: "${nreps:=10}"

# GPU qibojit backend
for (( dt=0.005; dt<=0.1; dt+=0.005 ))
do
  for platform in cupy cuquantum
  do
    CUDA_VISIBLE_DEVICES="0" python evolution.py --nqubits $nqubits --filename $filename --nreps $nreps \
  		                  	  					           --backend $backend --platform $platform --precision $precision
    echo
  done
done

# GPU TensorFlow and QiboTF backends
for (( dt=0.005; dt<=0.1; dt+=0.005 ))
do
  for backend in qibotf tensorflow
  do
    CUDA_VISIBLE_DEVICES="0" python evolution.py --nqubits $nqubits --filename $filename --nreps $nreps \
  		                  						             --backend $backend --precision $precision
    echo
  done
done

# CPU all backends
for (( dt=0.005; dt<=0.1; dt+=0.005 ))
do
  for backend in qibojit qibotf tensorflow numpy
  do
    CUDA_VISIBLE_DEVICES="" python evolution.py --nqubits $nqubits --filename $filename --nreps $nreps \
  		                  						            --backend $backend --precision $precision
    echo
  done
done
