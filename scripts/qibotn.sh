#! /usr/bin/bash
# Script for 2-nodes-4-GPUs (2x4) configuration
# Command-line parameters
: "${circuit:=variational}"
: "${precision:=double}"
: "${nreps:=3}"
: "${filename:=qibotn_expectation_double_2x4.dat}"

node_list=/nodelist_2x4 #file containing the IP address of the resources, omit this if it is running on single-node-multi-gpu

for (nqubits = 10; nqubits <= 8000; nqubits += 100)
do
    #echo '{"MPI_enabled": true, "MPS_enabled": false, "NCCL_enabled": false, "expectation_enabled": true}' > cu_tensornet_mpi_expectation.json #can be pre-generated or can include it in script. Here is using pre-generated.
    mpirun -np 8 -hostfile $node_list python compare.py --circuit variational --circuit-options nlayers=3 --nqubits 4$nqubits --filename $filename \
                                            --library-options backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_mpi_expectation.json \
                                            --nreps $nreps --precision $precision
echo
    #echo '{"MPI_enabled": false, "MPS_enabled": false, "NCCL_enabled": true, "expectation_enabled": true}' > cu_tensornet_nccl_expectation.json
    mpirun -np 8 -hostfile $node_list python compare.py --circuit variational --circuit-options nlayers=3 --nqubits $nqubits --filename $filename \
                                            --library-options backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_nccl_expectation.json \
                                            --nreps $nreps --precision $precision
echo
    #echo '{"MPI_enabled": false, "MPS_enabled": false, "NCCL_enabled": false, "expectation_enabled": true}' > cu_tensornet_expectation.json
    python compare.py --circuit variational --circuit-options nlayers=3 --nqubits $nqubits --filename $filename \
                                            --library-options backend=qibotn,platform=cutensornet,computation_settings=cu_tensornet_expectation.json \
                                            --nreps $nreps --precision $precision
echo
    python compare.py --circuit variational --circuit-options nlayers=3 --nqubits $nqubits --filename $filename \
                                            --library-options backend=qibojit,platform=numba,expectation="XXXZ" \
                                            --nreps $nreps --precision $precision
echo
done

: <<'END_COMMENT'

END_COMMENT
