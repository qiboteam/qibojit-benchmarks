# Generates the multigpu bar plot
# Assumes a machine with four GPUs

: "${filename:=multigpu.dat}"
: "${precision:=double}"
: "${nreps:=1}"

# TODO: temporarily reduce expectations to a single GPU
# export CUDA_VISIBLE_DEVICES=0,1,2,3
export CUDA_VISIBLE_DEVICES=0

for circuit in qft; do # variational supremacy qv bv
  # for backend in qibojit qibotf; do
  #   python compare.py --circuit $circuit --nqubits 10 --filename $filename \
  #     --library-options backend=$backend,accelerators=1/GPU:0+1/GPU:1+1/GPU:2+1/GPU:3 \
  #     --nreps $nreps --precision $precision
  #   echo
  # done

  # for backend in qibojit qibotf; do
  #   python compare.py --circuit $circuit --nqubits 10 --filename $filename \
  #     --library-options backend=$backend,accelerators=2/GPU:2+2/GPU:3 \
  #     --nreps $nreps --precision $precision
  #   echo
  # done

  for backend in qibojit qibotf; do
    python compare.py --circuit $circuit --nqubits 10 --filename $filename \
      --library-options backend=$backend,accelerators=4/GPU:0 \
      --nreps $nreps --precision $precision
    echo
  done
done
