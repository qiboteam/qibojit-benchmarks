FILENAME=qibomachine_gpu_120721.dat
export CUDA_VISIBLE_DEVICES="0"
NREPS=20
for NQUBITS in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
do
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibotf --nreps $NREPS
  echo
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibojit --nreps $NREPS
  echo
done
NREPS=5
for NQUBITS in 26 27 28 29 30
do
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibotf --nreps $NREPS
  echo
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibojit --nreps $NREPS
  echo
done
NREPS=20
for NQUBITS in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
do
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibotf --nreps $NREPS --transfer
  echo
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibojit --nreps $NREPS --transfer
  echo
done
NREPS=5
for NQUBITS in 26 27 28 29 30
do
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibotf --nreps $NREPS --transfer
  echo
  python main.py --circuit qft --nqubits $NQUBITS --filename $FILENAME --backend qibojit --nreps $NREPS --transfer
  echo
done
