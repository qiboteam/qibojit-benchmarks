FILENAME=qibomachine_cpu_230721.dat
export CUDA_VISIBLE_DEVICES=""
NREPS=10
for NQUBITS in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
  for CIRCUIT in qft variational bv supremacy bc qv
  do
    for BACKEND in qibotf qibojit
    do
      python main.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --nreps $NREPS --transfer
      echo
    done
  done
done
NREPS=1
for NQUBITS in 21 22 23 24 25
do
  for CIRCUIT in qft variational bv supremacy bc qv
  do
    for BACKEND in qibotf qibojit
    do
      python main.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --nreps $NREPS --transfer
      echo
    done
  done
done
FILENAME=qibomachine_gpu_230721.dat
export CUDA_VISIBLE_DEVICES="0"
NREPS=10
for NQUBITS in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
  for CIRCUIT in qft variational bv supremacy bc qv
  do
    for BACKEND in qibotf qibojit
    do
      python main.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --nreps $NREPS --transfer
      echo
    done
  done
done
NREPS=1
for NQUBITS in 21 22 23 24 25 26 27 28 29 30
do
  for CIRCUIT in qft variational bv supremacy bc qv
  do
    for BACKEND in qibotf qibojit
    do
      python main.py --circuit $CIRCUIT --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --nreps $NREPS --transfer
      echo
    done
  done
done
FILENAME=qibomachine_gpu_withfile_240721.dat
export CUDA_VISIBLE_DEVICES="0"
BITSTRING_FILE="graphs/random_bitstrings.dat"
NQUBITS=3
while read BITSTRING;
do
  for BACKEND in qibotf qibojit
  do
    python main.py --circuit hs --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --transfer --options "shift=$BITSTRING"
    echo
  done
  NQUBITS=$((NQUBITS + 1))
done < $BITSTRING_FILE
for NQUBITS in 4 6 8 10 12 14 16 18 20 22 24 26 28 30
do
  for BACKEND in qibotf qibojit
  do
    python main.py --circuit qaoa --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --transfer --options "graph=graphs/randomgraph_3_$NQUBITS.json"
    echo
  done
done
FILENAME=qibomachine_cpu_withfile_240721.dat
export CUDA_VISIBLE_DEVICES=""
for NQUBITS in 4 6 8 10 12 14 16 18 20 22 24 26
do
  for BACKEND in qibotf qibojit
  do
    python main.py --circuit qaoa --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --transfer --options "graph=graphs/randomgraph_3_$NQUBITS.json"
    echo
  done
done
BITSTRING_FILE="graphs/random_bitstrings.dat"
NQUBITS=3
while read BITSTRING;
do
  for BACKEND in qibotf qibojit
  do
    python main.py --circuit hs --nqubits $NQUBITS --filename $FILENAME --backend $BACKEND --transfer --options "shift=$BITSTRING"
    echo
  done
  NQUBITS=$((NQUBITS + 1))
done < $BITSTRING_FILE
