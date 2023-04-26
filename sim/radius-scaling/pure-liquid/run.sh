#!/bin/bash

MIN=1
MAX=10
STEP=1

N_CPU=8   # For each simulation
N_MAX=1   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in $(seq ${MIN} ${MAX} ${STEP})
do
    mkdir $con
    mpirun -np $N_CPU lmp -in in.thread.lmp -var dir $con > $con/bash.out &
    echo "Running simulation $con "
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi
done
wait

